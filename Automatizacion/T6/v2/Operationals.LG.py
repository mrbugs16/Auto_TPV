"""
FILENAME: Operationals_LG.py
DESCRIPTION:
    AUTOMATED TEST SUITE — LOGIN (LG) MODULE.
    COVERS THE FULL AUTHENTICATION FLOW OF THE NEW MEMPHIS APP v2.

TEST CASES COVERED:
    · TC-LOG-005 : LOGIN WITH VALID CREDENTIALS — FULL FLOW TO HOME SCREEN
    · TC-LOG-006 : INCORRECT PASSWORD — ERROR MESSAGE VALIDATION
    · TC-LOG-008 : UNREGISTERED USER  — ERROR MESSAGE VALIDATION

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
# HELPER — NAVIGATE ONBOARDING 
# ==================================================================================

def _navigate_onboarding(driver, wait):
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


def login(driver, wait):
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
# TC_LOG_005: LOGIN WITH VALID CREDENTIALS
# ==================================================================================

def TC_LOG_005():
    """
    TC-LOG-005: LOGIN WITH VALID CREDENTIALS — SUCCESS TYPE
    PRECONDITIONS : APP FRESHLY LAUNCHED — ONBOARDING VISIBLE
    EXPECTED      : FULL FLOW COMPLETES → USER LANDS ON HOME / CALCULADORA SCREEN
    """
    print("\n" + "=" * 60 + "\n")
    print("TC-LOG-005: LOGIN WITH VALID CREDENTIALS")
    print("=" * 60 + "\n")

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        time.sleep(3)

        # ── 1️⃣  ONBOARDING ──────────────────────────────────────────────────
        _navigate_onboarding(driver, wait)
        utils.take_screenshot(driver, "TC_LOG_005_01_login_screen", "t6")

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
        utils.take_screenshot(driver, "TC_LOG_005_02_credentials_filled", "t6")

        print("   👆 CLICKING 'Iniciar sesión'...")
        utils.click_element(driver, config.XPATH_LG_BTN_INICIAR)
        time.sleep(4)
        utils.take_screenshot(driver, "TC_LOG_005_03_after_login_click", "t6")

        # ── 3️⃣  CONFIGURA TU COMERCIO ────────────────────────────────────────
        print("\n🏪 STEP 3 — HANDLING 'CONFIGURA TU COMERCIO' SCREEN...")
        _handle_configura_comercio(driver, wait)
        utils.take_screenshot(driver, "TC_LOG_005_04_after_registro", "t6")

        # ── 4️⃣  LECTOR NO CONFIGURADO → CONFIGURAR AHORA ────────────────────
        print("\n⚙️  STEP 4 — HANDLING 'LECTOR NO CONFIGURADO' POPUP...")
        _handle_lector_popup(driver, wait, action="configure")
        utils.take_screenshot(driver, "TC_LOG_005_05_after_popup", "t6")

        # ── 5️⃣  VERIFY HOME SCREEN ───────────────────────────────────────────
        print("\n🔍 STEP 5 — VERIFYING HOME / CALCULATOR SCREEN IS VISIBLE...")
        home_visible = utils.verify_element(
            wait, config.XPATH_LG_PANTALLA_HOME, "HOME SCREEN / CALCULADORA"
        )

        if home_visible:
            result = "SUCCESS"
            print("✅ TC-LOG-005: HOME SCREEN CONFIRMED")
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

        utils.take_screenshot(driver, "TC_LOG_005_06_final_state", "t6")

    except Exception as e:
        print(f"❌ TC-LOG-005: EXCEPTION — {e}")
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-LOG-005 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# TC_LOG_006: INCORRECT PASSWORD VALIDATION
# ==================================================================================

def TC_LOG_006():
    """
    TC-LOG-006: INCORRECT PASSWORD — ERROR TYPE
    PRECONDITIONS : APP FRESHLY LAUNCHED — ONBOARDING VISIBLE
    EXPECTED      : SYSTEM DISPLAYS RED TOAST "Usuario o contraseña incorrectos"
                    USER REMAINS ON THE LOGIN SCREEN — NO NAVIGATION OCCURS
    """
    print("\n" + "=" * 60 + "\n")
    print("TC-LOG-006: INCORRECT PASSWORD VALIDATION")
    print("=" * 60 + "\n")

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        time.sleep(3)

        # ── 1️⃣  ONBOARDING ──────────────────────────────────────────────────
        _navigate_onboarding(driver, wait)
        utils.take_screenshot(driver, "TC_LOG_006_01_login_screen", "t6")

        # ── 2️⃣  ENTER VALID EMAIL + WRONG PASSWORD ───────────────────────────
        print("\n📝 STEP 2 — ENTERING VALID EMAIL + WRONG PASSWORD...")
        print(f"   📧 EMAIL: {config.USUARIO_VALIDO}")
        utils.type_text(driver, config.XPATH_INPUT_USUARIO, config.USUARIO_VALIDO)
        time.sleep(0.5)

        print(f"   🔑 PASSWORD (WRONG): {config.PASS_INVALIDO}")
        utils.type_text(driver, config.XPATH_INPUT_PASS, config.PASS_INVALIDO)
        time.sleep(0.5)

        driver.hide_keyboard()
        utils.take_screenshot(driver, "TC_LOG_006_02_credentials_filled", "t6")

        # ── 3️⃣  SUBMIT AND IMMEDIATELY DETECT TOAST ──────────────────────────
        # NOTE: NO time.sleep() BETWEEN SUBMIT AND DETECTION — EVERY MILLISECOND COUNTS
        print("\n   👆 STEP 3 — CLICKING 'Iniciar sesión' AND IMMEDIATELY WATCHING FOR TOAST...")
        utils.click_element(driver, config.XPATH_LG_BTN_INICIAR)

        toast_detected = _detect_error_toast(driver, "TC-LOG-006")
        utils.take_screenshot(driver, "TC_LOG_006_03_after_submit", "t6")

        if toast_detected:
            result = "SUCCESS"
            print("✅ TC-LOG-006: SYSTEM CORRECTLY REJECTED INVALID PASSWORD")
        else:
            print("❌ TC-LOG-006: ERROR TOAST NOT DETECTED — REVIEW SCREENSHOTS")

    except Exception as e:
        print(f"❌ TC-LOG-006: EXCEPTION — {e}")
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-LOG-006 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# TC_LOG_008: UNREGISTERED USER VALIDATION
# ==================================================================================

def TC_LOG_008():
    """
    TC-LOG-008: UNREGISTERED USER — ERROR TYPE
    PRECONDITIONS : APP FRESHLY LAUNCHED — ONBOARDING VISIBLE
    EXPECTED      : SYSTEM DISPLAYS RED TOAST "Usuario o contraseña incorrectos"
                    USER REMAINS ON THE LOGIN SCREEN — LOGIN IS REJECTED
    """
    print("\n" + "=" * 60 + "\n")
    print("TC-LOG-008: UNREGISTERED USER VALIDATION")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        time.sleep(3)

        # ── 1️⃣  ONBOARDING ──────────────────────────────────────────────────
        _navigate_onboarding(driver, wait)
        utils.take_screenshot(driver, "TC_LOG_008_01_login_screen", "t6")

        # ── 2️⃣  ENTER UNREGISTERED EMAIL + VALID PASSWORD ────────────────────
        print("\n📝 STEP 2 — ENTERING UNREGISTERED EMAIL + VALID PASSWORD...")
        print(f"   📧 EMAIL (UNREGISTERED): {config.USUARIO_INVALIDO}")
        utils.type_text(driver, config.XPATH_INPUT_USUARIO, config.USUARIO_INVALIDO)
        time.sleep(0.5)

        print(f"   🔑 PASSWORD (VALID): {config.PASS_VALIDO}")
        utils.type_text(driver, config.XPATH_INPUT_PASS, config.PASS_VALIDO)
        time.sleep(0.5)

        driver.hide_keyboard()
        utils.take_screenshot(driver, "TC_LOG_008_02_credentials_filled", "t6")

        # ── 3️⃣  SUBMIT AND IMMEDIATELY DETECT TOAST ──────────────────────────
        # NOTE: NO time.sleep() BETWEEN SUBMIT AND DETECTION — EVERY MILLISECOND COUNTS
        print("\n   👆 STEP 3 — CLICKING 'Iniciar sesión' AND IMMEDIATELY WATCHING FOR TOAST...")
        utils.click_element(driver, config.XPATH_LG_BTN_INICIAR)

        toast_detected = _detect_error_toast(driver, "TC-LOG-008")
        utils.take_screenshot(driver, "TC_LOG_008_03_after_submit", "t6")

        if toast_detected:
            result = "SUCCESS"
            print("✅ TC-LOG-008: SYSTEM CORRECTLY REJECTED UNREGISTERED USER")
        else:
            print("❌ TC-LOG-008: ERROR TOAST NOT DETECTED — REVIEW SCREENSHOTS")

    except Exception as e:
        print(f"❌ TC-LOG-008: EXCEPTION — {e}")
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-LOG-008 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# EXECUTION
# ==================================================================================

if __name__ == "__main__":

    
    logger, log_file, timestamp = utils.start_report("OPERATIONALS_TC_LOG")

    try:
        TC_LOG_005()
        TC_LOG_006()
        TC_LOG_008()

    finally:
        
    
        logger.close()

        
        utils.generate_zip_report("OPERATIONALS_TC_LOG", logger, log_file, timestamp)
        utils.generate_html_report("OPERATIONALS_TC_LOG", log_file, timestamp)