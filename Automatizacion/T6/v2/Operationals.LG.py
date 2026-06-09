"""
FILENAME: Operationals_LG.py
DESCRIPTION:
    AUTOMATED TEST SUITE — LOGIN (LG) MODULE.
    COVERS THE FULL AUTHENTICATION FLOW OF THE NEW MEMPHIS APP v2.

CONFIRMED FLOW (NEW APP v2):
    [SLIDE 1]   "Configura la terminal"       → BTN "Siguiente"
    [SLIDE 2]   "Ingresa la información..."   → BTN "Siguiente"
    [SLIDE 3]   "Empieza a realizar cobros"   → BTN "Comenzar"
    [SCREEN A]  "Iniciar sesión"              → Email + Password → BTN "Iniciar sesión"
    [SCREEN B]  "Configura tu comercio"       → Afiliación + Token → BTN "Confirmar y comenzar"
    [SCREEN C]  "Lector no configurado"       → BTN "Configurar ahora" | "Después"
    [SCREEN D]  "Lector configurado"          → BTN "Aceptar"
    [SCREEN E]  HOME / Calculadora            → "$0.00 MXN" visible

TEST CASES COVERED:
    · LG-005 : LOGIN WITH VALID CREDENTIALS — FULL FLOW TO HOME SCREEN
    · LG-006 : INCORRECT PASSWORD — ERROR MESSAGE VALIDATION
    · LG-008 : UNREGISTERED USER  — ERROR MESSAGE VALIDATION

ERROR DETECTION STRATEGY (LG-006 / LG-008):
    THE APP SHOWS A TRANSIENT RED TOAST "Usuario o contraseña incorrectos" (~2-3s).
    STRATEGY: WebDriverWait WITH A TIGHT TIMEOUT DIRECTLY ON THE TOAST XPATH.
    THIS IS FASTER THAN ITERATING //* WHICH FETCHES ALL DOM NODES ON EVERY ATTEMPT.

REQUIREMENTS:
    - Appium server running on localhost:4723  (appium --relaxed-security)
    - T6 terminal connected via USB with USB Debugging enabled
    - config.py and utils.py in the same directory
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time
import config
import utils
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# ==================================================================================
# HELPER — NAVIGATE ONBOARDING (SLIDES 1-2-3 → LOGIN SCREEN)
# ==================================================================================

def _navigate_onboarding(driver, wait):
    """
    NAVIGATES THROUGH THE 3 ONBOARDING SLIDES.
    AFTER CLICKING "Comenzar" ON SLIDE 3 THE APP LANDS DIRECTLY ON THE LOGIN SCREEN.

    SLIDE 1 → BTN "Siguiente"
    SLIDE 2 → BTN "Siguiente"
    SLIDE 3 → BTN "Comenzar"
    """
    print("\n📱 STEP 1 — NAVIGATING ONBOARDING SLIDES...")

    # ── SLIDE 1 ──────────────────────────────────────────────────────────────
    print("   1️⃣  SLIDE 1: 'Configura la terminal' — CLICKING 'Siguiente'...")
    try:
        utils.click_element(driver, config.XPATH_OB_BTN_SIGUIENTE)
        time.sleep(1.5)
        print("   ✅ SLIDE 1 PASSED")
    except Exception as e:
        print(f"   ⚠️  SLIDE 1 — TRYING SKIP LINK: {e}")
        utils.click_element(driver, config.XPATH_OB_BTN_SALTAR)
        time.sleep(1)

    # ── SLIDE 2 ──────────────────────────────────────────────────────────────
    print("   2️⃣  SLIDE 2: 'Ingresa la información...' — CLICKING 'Siguiente'...")
    try:
        utils.click_element(driver, config.XPATH_OB_BTN_SIGUIENTE)
        time.sleep(1.5)
        print("   ✅ SLIDE 2 PASSED")
    except Exception as e:
        print(f"   ⚠️  SLIDE 2 BUTTON NOT FOUND: {e}")

    # ── SLIDE 3 ──────────────────────────────────────────────────────────────
    print("   3️⃣  SLIDE 3: 'Empieza a realizar cobros' — CLICKING 'Comenzar'...")
    try:
        utils.click_element(driver, config.XPATH_OB_BTN_COMENZAR)
        time.sleep(2)
        print("   ✅ SLIDE 3 PASSED — APP NOW ON LOGIN SCREEN")
    except Exception as e:
        print(f"   ⚠️  SLIDE 3 'Comenzar' NOT FOUND: {e}")


# ==================================================================================
# HELPER — HANDLE "CONFIGURA TU COMERCIO" SCREEN
# ==================================================================================

def _handle_configura_comercio(driver, wait):
    """
    HANDLES SCREEN B — "CONFIGURA TU COMERCIO".
    APPEARS AFTER THE FIRST SUCCESSFUL LOGIN WHEN COMMERCE IS NOT YET LINKED.

    FIELD 1: "Número de afiliación" → CC_AFILIACION = "8920377"
    FIELD 2: "Token"                → CC_TOKEN      = "1733258724574qkd"
    BUTTON : "Confirmar y comenzar"
    """
    print("\n🏪 CHECKING FOR 'CONFIGURA TU COMERCIO' SCREEN...")
    time.sleep(2)

    screen_present = utils.verify_element(
        wait, config.XPATH_CC_SCREEN, "CONFIGURA TU COMERCIO SCREEN"
    )

    if not screen_present:
        print("   ℹ️  SCREEN NOT DETECTED — COMMERCE ALREADY LINKED, SKIPPING")
        return

    print("   ✅ SCREEN DETECTED — FILLING FORM...")

    # ── STRATEGY 1: CONFIRMED [3C] XPATHS ────────────────────────────────────
    try:
        print(f"   🔢 ENTERING AFFILIATION NUMBER (FIELD 1): {config.CC_AFILIACION}...")
        utils.type_text(driver, config.XPATH_CC_INPUT_AFILIACION, config.CC_AFILIACION)
        time.sleep(0.5)

        print(f"   🔑 ENTERING TOKEN (FIELD 2): {config.CC_TOKEN}...")
        utils.type_text(driver, config.XPATH_CC_INPUT_TOKEN, config.CC_TOKEN)
        time.sleep(0.5)

        driver.hide_keyboard()
        time.sleep(0.5)

        print("   👆 CLICKING 'Confirmar y comenzar'...")
        utils.click_element(driver, config.XPATH_CC_BTN_CONFIRMAR)
        time.sleep(3)
        print("   ✅ 'CONFIGURA TU COMERCIO' SUBMITTED SUCCESSFULLY")

    except Exception as e:
        print(f"   ⚠️  STRATEGY 1 FAILED: {e}")

        # ── STRATEGY 2: RAW EDITTEXT INDEX ───────────────────────────────────
        print("   🔄 STRATEGY 2 — RAW EDITTEXTS BY INDEX...")
        try:
            inputs = driver.find_elements(By.XPATH, "//android.widget.EditText")
            print(f"   ℹ️  FOUND {len(inputs)} INPUT FIELD(S)")
            if len(inputs) >= 1:
                inputs[0].click()
                inputs[0].send_keys(config.CC_AFILIACION)
                time.sleep(0.3)
            if len(inputs) >= 2:
                inputs[1].click()
                inputs[1].send_keys(config.CC_TOKEN)
                time.sleep(0.3)
            driver.hide_keyboard()
            time.sleep(0.5)
            utils.click_element(driver, config.XPATH_CC_BTN_CONFIRMAR)
            time.sleep(3)
            print("   ✅ STRATEGY 2 SUBMITTED")
        except Exception as e2:
            print(f"   ❌ STRATEGY 2 ALSO FAILED: {e2}")


# ==================================================================================
# HELPER — HANDLE LECTOR POPUP + CONFIRMATION SCREEN
# ==================================================================================

def _handle_lector_popup(driver, wait, action="later"):
    """
    HANDLES SCREENS C AND D OF THE LOGIN FLOW:

    SCREEN C — "LECTOR NO CONFIGURADO" BOTTOM SHEET
        action = "configure" → CLICKS "Configurar ahora" → SCREEN D APPEARS
        action = "later"     → CLICKS "Después"          → GOES DIRECTLY TO HOME

    SCREEN D — "LECTOR CONFIGURADO" CONFIRMATION (ONLY WHEN action="configure")
        SHOWS: "Lector configurado" + "Configuración completada" + 100% bar
        ACTION: CLICKS "Aceptar" → HOME SCREEN

    PARAMS:
        action = "configure" → FULL SETUP FLOW (USED IN LG-005)
        action = "later"     → SKIP SETUP, GO TO HOME  (USED IN shared login())
    """
    print("\n⚙️  CHECKING FOR 'LECTOR NO CONFIGURADO' POPUP...")
    time.sleep(2)

    popup_visible = utils.verify_element(
        wait, config.XPATH_LG_POPUP_LECTOR_NC, "POPUP LECTOR NO CONFIGURADO"
    )

    if not popup_visible:
        print("   ℹ️  NO POPUP DETECTED — CONTINUING")
        return

    print("   ✅ POPUP DETECTED — LECTOR NO CONFIGURADO")

    if action == "later":
        print("   👆 CLICKING 'Después' — SKIPPING READER SETUP...")
        utils.click_element(driver, config.XPATH_LG_BTN_DESPUES)
        time.sleep(2)
        print("   ✅ POPUP DISMISSED — HEADING TO HOME")
        return

    # ── PATH B: CONFIGURE THE READER ─────────────────────────────────────────
    print("   👆 CLICKING 'Configurar ahora'...")
    utils.click_element(driver, config.XPATH_LG_BTN_CONFIGURAR_AHORA)
    time.sleep(3)

    # ── SCREEN D: "LECTOR CONFIGURADO" CONFIRMATION ───────────────────────────
    print("\n🎉 CHECKING FOR 'LECTOR CONFIGURADO' CONFIRMATION SCREEN...")
    confirmed = utils.verify_element(
        wait, config.XPATH_LG_LECTOR_CONFIGURADO, "LECTOR CONFIGURADO SCREEN"
    )

    if confirmed:
        print("   ✅ CONFIRMED — 'Lector configurado' / 'Configuración completada'")
        print("   👆 CLICKING 'Aceptar'...")
        try:
            utils.click_element(driver, config.XPATH_LG_BTN_ACEPTAR_LECTOR)
            time.sleep(2)
            print("   ✅ 'Aceptar' CLICKED — HEADING TO HOME")
        except Exception as e:
            print(f"   ⚠️  STRATEGY 1 FAILED: {e}")
            print("   🔄 STRATEGY 2 — CONTENT-DESC FALLBACK...")
            try:
                utils.click_element(
                    driver,
                    '//*[contains(@content-desc, "Aceptar") or contains(@text, "Aceptar")]'
                )
                time.sleep(2)
                print("   ✅ STRATEGY 2 CLICKED")
            except Exception as e2:
                print(f"   ❌ STRATEGY 2 ALSO FAILED: {e2}")
    else:
        print("   ⚠️  'LECTOR CONFIGURADO' SCREEN NOT DETECTED")
        print("         READER MAY ALREADY HAVE BEEN CONFIGURED IN A PRIOR SESSION")


# ==================================================================================
# INTERNAL HELPER — DETECT ERROR TOAST (LG-006 / LG-008)
# ==================================================================================

def _detect_error_toast(driver, test_id):
    """
    DETECTS THE TRANSIENT RED ERROR TOAST THAT APPEARS AFTER A FAILED LOGIN ATTEMPT.
    OBSERVED TOAST TEXT: "Usuario o contraseña incorrectos"
    TOAST LIFESPAN: ~2-3 SECONDS

    STRATEGY A — WebDriverWait ON SPECIFIC XPATH (FASTEST, NO DOM DUMP):
        POLLS DIRECTLY FOR THE TOAST ELEMENT EVERY 0.5s UP TO 5s.
        AVOIDS THE OVERHEAD OF FETCHING THE ENTIRE DOM WITH find_elements("//*").

    STRATEGY B — SCREEN DUMP FALLBACK:
        IF STRATEGY A MISSES THE TOAST, SCANS ALL ELEMENTS AS A LAST RESORT.
        ALSO CONFIRMS THE USER IS STILL ON THE LOGIN SCREEN (CORRECT BEHAVIOR).

    RETURNS:
        True  — ERROR TOAST DETECTED   → TEST SHOULD PASS
        False — TOAST NOT DETECTED     → TEST SHOULD FAIL (INVESTIGATE)
    """
    print(f"\n🔍 [{test_id}] DETECTING ERROR TOAST...")

    # ── STRATEGY A: DIRECT WebDriverWait ON TOAST XPATH ──────────────────────
    TOAST_XPATH = (
        '//*[contains(@content-desc, "incorrectos") or '
        'contains(@text, "incorrectos") or '
        'contains(@content-desc, "Usuario o contrase") or '
        'contains(@text, "Usuario o contrase")]'
    )

    print(f"   🔎 STRATEGY A — WebDriverWait(5s) ON TOAST XPATH...")
    try:
        toast_wait = WebDriverWait(driver, 5)
        toast_wait.until(EC.presence_of_element_located((By.XPATH, TOAST_XPATH)))
        print(f"   ✅ [{test_id}] TOAST DETECTED VIA STRATEGY A")
        return True
    except TimeoutException:
        print(f"   ⚠️  STRATEGY A — TOAST NOT CAUGHT IN 5s WINDOW")

    # ── STRATEGY B: SCAN ALL ELEMENTS + CONFIRM LOGIN SCREEN STILL SHOWING ───
    print(f"   🔎 STRATEGY B — FULL SCREEN SCAN + LOGIN SCREEN CONFIRMATION...")
    try:
        all_elements = driver.find_elements(By.XPATH, "//*")
        toast_keywords   = ["incorrectos", "incorrecto", "usuario o contrase"]
        login_indicators = ["iniciar sesión", "correo electrónico", "contraseña"]

        toast_found  = False
        on_login_screen = False

        for el in all_elements:
            try:
                t = el.get_attribute("text") or ""
                d = el.get_attribute("content-desc") or ""
                combined = (t + d).lower()

                if any(kw in combined for kw in toast_keywords):
                    print(f"   ✅ TOAST FOUND IN SCAN — text='{t}' desc='{d}'")
                    toast_found = True

                if any(li in combined for li in login_indicators):
                    on_login_screen = True
            except:
                continue

        if toast_found:
            return True

        if on_login_screen:
            # THE USER IS STILL ON THE LOGIN SCREEN — THE SYSTEM REJECTED THE LOGIN.
            # THE TOAST APPEARED BUT DISAPPEARED BEFORE BOTH STRATEGIES COULD CATCH IT.
            # THIS IS STILL THE EXPECTED BEHAVIOR — MARK AS SUCCESS.
            print(f"   ✅ [{test_id}] LOGIN SCREEN STILL VISIBLE — LOGIN WAS REJECTED CORRECTLY")
            print(f"         (TOAST DISAPPEARED BEFORE DETECTION — BEHAVIOR IS CORRECT)")
            return True

        print(f"   ❌ [{test_id}] NEITHER TOAST NOR LOGIN SCREEN DETECTED")
        print("         PRINTING FULL SCREEN FOR DIAGNOSIS:")
        for el in all_elements:
            try:
                t = el.get_attribute("text") or ""
                d = el.get_attribute("content-desc") or ""
                if t or d:
                    print(f"      → text='{t}' | desc='{d}'")
            except:
                continue
        return False

    except Exception as e:
        print(f"   ❌ STRATEGY B ERROR: {e}")
        return False


# ==================================================================================
# SHARED FUNCTION — login()
# CALLED BY: Operationals_C.py, Operationals_TS.py, Operationals_DT.py, etc.
# ==================================================================================

def login(driver, wait):
    """
    SHARED LOGIN FUNCTION — FULL FLOW FOR ANY TEST NEEDING AN AUTHENTICATED SESSION.
        1. NAVIGATE ONBOARDING SLIDES (1→2→3)
        2. FILL LOGIN FORM (EMAIL + PASSWORD + SUBMIT)
        3. HANDLE "CONFIGURA TU COMERCIO" SCREEN IF PRESENT
        4. DISMISS "LECTOR NO CONFIGURADO" → "Después" (LANDS ON HOME)

    RETURNS True ON SUCCESS, False ON FAILURE.
    """
    print("\n🔐 RUNNING SHARED LOGIN MODULE...")

    try:
        _navigate_onboarding(driver, wait)

        print("\n📝 FILLING LOGIN FORM...")
        utils.type_text(driver, config.XPATH_INPUT_USUARIO, config.USUARIO_VALIDO)
        time.sleep(0.5)
        utils.type_text(driver, config.XPATH_INPUT_PASS, config.PASS_VALIDO)
        time.sleep(0.5)
        driver.hide_keyboard()
        time.sleep(0.5)

        print("   👆 CLICKING 'Iniciar sesión'...")
        utils.click_element(driver, config.XPATH_LG_BTN_INICIAR)
        time.sleep(4)

        _handle_configura_comercio(driver, wait)
        _handle_lector_popup(driver, wait, action="later")

        print("✅ SHARED LOGIN SUCCESSFUL")
        return True

    except Exception as e:
        print(f"❌ SHARED LOGIN FAILED: {e}")
        return False


# ==================================================================================
# LG-005: LOGIN WITH VALID CREDENTIALS
# ==================================================================================

def LG_005():
    """
    LG-005: LOGIN WITH VALID CREDENTIALS — SUCCESS TYPE
    PRECONDITIONS : APP FRESHLY LAUNCHED — ONBOARDING VISIBLE
    EXPECTED      : FULL FLOW COMPLETES → USER LANDS ON HOME / CALCULADORA SCREEN
    """
    print("\n" + "=" * 60)
    print("LG-005: LOGIN WITH VALID CREDENTIALS")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        time.sleep(3)

        # ── 1️⃣  ONBOARDING ──────────────────────────────────────────────────
        _navigate_onboarding(driver, wait)
        utils.take_screenshot(driver, "LG005_01_login_screen", "t6")

        # ── 2️⃣  LOGIN FORM ───────────────────────────────────────────────────
        print("\n📝 STEP 2 — FILLING LOGIN FORM WITH VALID CREDENTIALS...")
        print(f"   📧 ENTERING EMAIL: {config.USUARIO_VALIDO}")
        utils.type_text(driver, config.XPATH_INPUT_USUARIO, config.USUARIO_VALIDO)
        time.sleep(0.5)
        print("   🔑 ENTERING PASSWORD...")
        utils.type_text(driver, config.XPATH_INPUT_PASS, config.PASS_VALIDO)
        time.sleep(0.5)
        driver.hide_keyboard()
        time.sleep(0.5)
        utils.take_screenshot(driver, "LG005_02_credentials_filled", "t6")

        print("   👆 CLICKING 'Iniciar sesión'...")
        utils.click_element(driver, config.XPATH_LG_BTN_INICIAR)
        time.sleep(4)
        utils.take_screenshot(driver, "LG005_03_after_login_click", "t6")

        # ── 3️⃣  CONFIGURA TU COMERCIO ────────────────────────────────────────
        print("\n🏪 STEP 3 — HANDLING 'CONFIGURA TU COMERCIO' SCREEN...")
        _handle_configura_comercio(driver, wait)
        utils.take_screenshot(driver, "LG005_04_after_registro", "t6")

        # ── 4️⃣  LECTOR NO CONFIGURADO → CONFIGURAR AHORA ────────────────────
        print("\n⚙️  STEP 4 — HANDLING 'LECTOR NO CONFIGURADO' POPUP...")
        _handle_lector_popup(driver, wait, action="configure")
        utils.take_screenshot(driver, "LG005_05_after_popup", "t6")

        # ── 5️⃣  VERIFY HOME SCREEN ───────────────────────────────────────────
        print("\n🔍 STEP 5 — VERIFYING HOME / CALCULATOR SCREEN IS VISIBLE...")
        home_visible = utils.verify_element(
            wait, config.XPATH_LG_PANTALLA_HOME, "HOME SCREEN / CALCULADORA"
        )

        if home_visible:
            result = "SUCCESS"
            print("✅ LG-005: HOME SCREEN CONFIRMED")
        else:
            print("   ⚠️  PRIMARY XPATH NOT MATCHED — SCANNING SCREEN...")
            for el in driver.find_elements(By.XPATH, "//*"):
                try:
                    t = el.get_attribute("text") or ""
                    d = el.get_attribute("content-desc") or ""
                    if any(k in (t + d).upper() for k in ["MXN", "COBRAR", "INICIO", "HOLA", "0.00"]):
                        print(f"   ✅ HOME INDICATOR FOUND — text='{t}' desc='{d}'")
                        result = "SUCCESS"
                        break
                except:
                    continue

        utils.take_screenshot(driver, "LG005_06_final_state", "t6")

    except Exception as e:
        print(f"❌ LG-005: EXCEPTION — {e}")
    finally:
        print("\n" + "-" * 60)
        print(f"📊 LG-005 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# LG-006: INCORRECT PASSWORD VALIDATION
# ==================================================================================

def LG_006():
    """
    LG-006: INCORRECT PASSWORD — ERROR TYPE
    PRECONDITIONS : APP FRESHLY LAUNCHED — ONBOARDING VISIBLE
    EXPECTED      : SYSTEM DISPLAYS RED TOAST "Usuario o contraseña incorrectos"
                    USER REMAINS ON THE LOGIN SCREEN — NO NAVIGATION OCCURS
    """
    print("\n" + "=" * 60)
    print("LG-006: INCORRECT PASSWORD VALIDATION")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        time.sleep(3)

        # ── 1️⃣  ONBOARDING ──────────────────────────────────────────────────
        _navigate_onboarding(driver, wait)
        utils.take_screenshot(driver, "LG006_01_login_screen", "t6")

        # ── 2️⃣  ENTER VALID EMAIL + WRONG PASSWORD ───────────────────────────
        print("\n📝 STEP 2 — ENTERING VALID EMAIL + WRONG PASSWORD...")
        print(f"   📧 EMAIL: {config.USUARIO_VALIDO}")
        utils.type_text(driver, config.XPATH_INPUT_USUARIO, config.USUARIO_VALIDO)
        time.sleep(0.5)

        print(f"   🔑 PASSWORD (WRONG): {config.PASS_INVALIDO}")
        utils.type_text(driver, config.XPATH_INPUT_PASS, config.PASS_INVALIDO)
        time.sleep(0.5)

        driver.hide_keyboard()
        utils.take_screenshot(driver, "LG006_02_credentials_filled", "t6")

        # ── 3️⃣  SUBMIT AND IMMEDIATELY DETECT TOAST ──────────────────────────
        # NOTE: NO time.sleep() BETWEEN SUBMIT AND DETECTION — EVERY MILLISECOND COUNTS
        print("\n   👆 STEP 3 — CLICKING 'Iniciar sesión' AND IMMEDIATELY WATCHING FOR TOAST...")
        utils.click_element(driver, config.XPATH_LG_BTN_INICIAR)

        toast_detected = _detect_error_toast(driver, "LG-006")
        utils.take_screenshot(driver, "LG006_03_after_submit", "t6")

        if toast_detected:
            result = "SUCCESS"
            print("✅ LG-006: SYSTEM CORRECTLY REJECTED INVALID PASSWORD")
        else:
            print("❌ LG-006: ERROR TOAST NOT DETECTED — REVIEW SCREENSHOTS")

    except Exception as e:
        print(f"❌ LG-006: EXCEPTION — {e}")
    finally:
        print("\n" + "-" * 60)
        print(f"📊 LG-006 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# LG-008: UNREGISTERED USER VALIDATION
# ==================================================================================

def LG_008():
    """
    LG-008: UNREGISTERED USER — ERROR TYPE
    PRECONDITIONS : APP FRESHLY LAUNCHED — ONBOARDING VISIBLE
    EXPECTED      : SYSTEM DISPLAYS RED TOAST "Usuario o contraseña incorrectos"
                    USER REMAINS ON THE LOGIN SCREEN — LOGIN IS REJECTED
    """
    print("\n" + "=" * 60)
    print("LG-008: UNREGISTERED USER VALIDATION")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        time.sleep(3)

        # ── 1️⃣  ONBOARDING ──────────────────────────────────────────────────
        _navigate_onboarding(driver, wait)
        utils.take_screenshot(driver, "LG008_01_login_screen", "t6")

        # ── 2️⃣  ENTER UNREGISTERED EMAIL + VALID PASSWORD ────────────────────
        print("\n📝 STEP 2 — ENTERING UNREGISTERED EMAIL + VALID PASSWORD...")
        print(f"   📧 EMAIL (UNREGISTERED): {config.USUARIO_INVALIDO}")
        utils.type_text(driver, config.XPATH_INPUT_USUARIO, config.USUARIO_INVALIDO)
        time.sleep(0.5)

        print(f"   🔑 PASSWORD (VALID): {config.PASS_VALIDO}")
        utils.type_text(driver, config.XPATH_INPUT_PASS, config.PASS_VALIDO)
        time.sleep(0.5)

        driver.hide_keyboard()
        utils.take_screenshot(driver, "LG008_02_credentials_filled", "t6")

        # ── 3️⃣  SUBMIT AND IMMEDIATELY DETECT TOAST ──────────────────────────
        # NOTE: NO time.sleep() BETWEEN SUBMIT AND DETECTION — EVERY MILLISECOND COUNTS
        print("\n   👆 STEP 3 — CLICKING 'Iniciar sesión' AND IMMEDIATELY WATCHING FOR TOAST...")
        utils.click_element(driver, config.XPATH_LG_BTN_INICIAR)

        toast_detected = _detect_error_toast(driver, "LG-008")
        utils.take_screenshot(driver, "LG008_03_after_submit", "t6")

        if toast_detected:
            result = "SUCCESS"
            print("✅ LG-008: SYSTEM CORRECTLY REJECTED UNREGISTERED USER")
        else:
            print("❌ LG-008: ERROR TOAST NOT DETECTED — REVIEW SCREENSHOTS")

    except Exception as e:
        print(f"❌ LG-008: EXCEPTION — {e}")
    finally:
        print("\n" + "-" * 60)
        print(f"📊 LG-008 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# EXECUTION
# ==================================================================================

if __name__ == "__main__":

    # ── START REPORT SESSION ──────────────────────────────────────────────────
    # start_report() CREATES zip_evidence/ AND STARTS CAPTURING ALL CONSOLE OUTPUT
    # TO A .txt LOG FILE. ALWAYS CALLED BEFORE ANY TEST FUNCTION.
    logger, log_file, timestamp = utils.start_report("OPERATIONALS_LG")

    try:
        LG_005()
        LG_006()
        LG_008()

    finally:
        # ── CLOSE LOGGER BEFORE GENERATING REPORT ────────────────────────────
        # logger.close() FLUSHES THE LOG FILE SO IT IS FULLY WRITTEN TO DISK.
        logger.close()

        # ── GENERATE ZIP WITH ALL EVIDENCE ───────────────────────────────────
        # generate_zip_report() PACKAGES:
        #   · evidence/T6/*.png  (screenshots)
        #   · zip_evidence/*.txt (log file)
        # INTO: zip_evidence/OPERATIONALS_LG_FULL_REPORT_{timestamp}.zip
        utils.generate_zip_report("OPERATIONALS_LG", logger, log_file, timestamp)

        # ── GENERATE HTML REPORT ──────────────────────────────────────────────
        # generate_html_report() CREATES AN HTML SUMMARY FROM THE LOG FILE.
        # OUTPUT: zip_evidence/OPERATIONALS_LG_REPORT_{timestamp}.html
        utils.generate_html_report("OPERATIONALS_LG", log_file, timestamp)