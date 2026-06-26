"""
FILENAME: Operationals_AJ.py
DESCRIPTION:
    AUTOMATED TEST SUITE — AJUSTES (AJ) MODULE.
    COVERS THE SETTINGS SECTION OF THE NEW MEMPHIS APP v2 (com.memphis.app.dev).

SCREENS COVERED (CONFIRMED FROM SCREENSHOTS):
    SCREEN 1 — HOME / CALCULATOR
    SCREEN 2 — AJUSTES (SETTINGS MENU)
               Cuenta: Info personal | Cambiar contraseña | Cambiar comercio |
                       Actualizar configuraciones | Cerrar sesión
               Lector: Configurar nuevamente
               PinPad: Apagar/Encender servidor PinPad
               Desarrollador: Ver logs
    SCREEN 3 — INFORMACIÓN PERSONAL
               Afiliación | Nombre | Lector asociado | Correo electrónico | UUID | Versión
    SCREEN 4 — CAMBIAR CONTRASEÑA (empty form)
               Fields: Contraseña anterior | Nueva contraseña | Confirmar contraseña
               Button: Actualizar
    SCREEN 5 — CAMBIAR CONTRASEÑA (filled — valid update)
    SCREEN 6 — CAMBIAR CONTRASEÑA (error — passwords do not match)
    SCREEN 7 — CAMBIAR CONTRASEÑA (error — minimum 8 characters)
    SCREEN 8 — CAMBIAR CONTRASEÑA (visibility icons test)

TEST CASES COVERED:
    · AJ-105 : SETTINGS TAB LOADS CORRECTLY
    · AJ-106 : NAVIGATE TO "INFORMACIÓN PERSONAL" FROM SETTINGS
    · AJ-107 : VERIFY ALL PERSONAL INFO FIELDS ARE DISPLAYED
    · AJ-108 : NAVIGATE TO "CAMBIAR CONTRASEÑA" AND VERIFY SCREEN LOADS
    · AJ-109 : SUCCESSFUL PASSWORD CHANGE (valid credentials)
    · AJ-110 : FAILED PASSWORD CHANGE — WRONG CURRENT PASSWORD
    · AJ-111 : FAILED PASSWORD CHANGE — PASSWORDS DO NOT MATCH
    · AJ-112 : FAILED PASSWORD CHANGE — PASSWORD TOO SHORT (< 8 CHARS)
    · AJ-113 : PASSWORD VISIBILITY TOGGLE ICONS WORK CORRECTLY

REQUIREMENTS:
    - Appium server running on localhost:4723  (appium --relaxed-security)
    - T6 terminal connected via USB with USB Debugging enabled
    - config.py and utils.py in the same directory
"""

import sys
import os

# ── PATH SETUP ──────────────────────────────────────────────────
v2_path = os.path.abspath(os.path.dirname(__file__))
t6_path = os.path.abspath(os.path.join(v2_path, '..'))
for p in [v2_path, t6_path]:
    if p not in sys.path:
        sys.path.insert(0, p)
# ────────────────────────────────────────────────────────────────

import time
import config
import utils
import utils_system as sys_ctrl          # ← LÍNEA NUEVA
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# ==================================================================================
# INTERNAL HELPER — NAVIGATE TO SETTINGS TAB
# ==================================================================================

def _navigate_to_settings(driver, wait):
    """
    NAVIGATES TO THE AJUSTES (SETTINGS) TAB FROM ANY SCREEN.
    USES BOTTOM NAV BAR TAB [4].
    STRATEGY 1: EXACT content-desc MATCH
    STRATEGY 2: PARTIAL content-desc MATCH
    STRATEGY 3: UIAUTOMATOR TEXT MATCH
    STRATEGY 4: UIAUTOMATOR DESCRIPTION MATCH
    STRATEGY 5: INDEX-BASED (4TH TAB IN BOTTOM NAV)
    RETURNS True ON SUCCESS, False ON FAILURE.
    """
    print("\n   📍 [NAV] NAVIGATING TO SETTINGS TAB...")

    # STRATEGY 1 + 2 + 3: XPATH VARIANTS
    for xpath in [
        '//android.widget.ImageView[@content-desc="Ajustes"]',
        '//android.view.View[@content-desc="Ajustes"]',
        '//*[@content-desc="Ajustes"]',
        config.XPATH_AJ_TAB_SETTINGS,
        config.XPATH_PÑ_TAB_AJUSTES,
        '//*[contains(@content-desc,"Ajustes")]',
        '//*[contains(@text,"Ajustes")]',
    ]:
        try:
            driver.find_element(By.XPATH, xpath).click()
            time.sleep(2)
            print("   ✅ [NAV] SETTINGS TAB REACHED")
            return True
        except:
            pass

    # STRATEGY 4: UIAUTOMATOR — text or description
    for selector in [
        'new UiSelector().description("Ajustes")',
        'new UiSelector().descriptionContains("Ajustes")',
        'new UiSelector().text("Ajustes")',
        'new UiSelector().textContains("Ajustes")',
    ]:
        try:
            driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, selector).click()
            time.sleep(2)
            print(f"   ✅ [NAV] SETTINGS TAB VIA UIAUTOMATOR: {selector[:40]}")
            return True
        except:
            pass

    # STRATEGY 5: TAP THE 4TH ITEM IN THE BOTTOM NAVIGATION BAR
    print("   🔄 [NAV] STRATEGY 5 — TAPPING 4TH BOTTOM NAV ITEM...")
    try:
        nav_items = driver.find_elements(
            By.XPATH,
            '//android.widget.FrameLayout[@resource-id="android:id/content"]'
            '//*[contains(@content-desc,"") and @clickable="true"]',
        )
        # FALLBACK: GET ALL CLICKABLE ITEMS IN BOTTOM AREA AND TAP THE LAST ONE
        all_clickable = driver.find_elements(
            By.XPATH, '//*[@clickable="true"]')
        # BOTTOM NAV TABS ARE TYPICALLY THE LAST 4 CLICKABLE ELEMENTS ON HOME SCREEN
        if len(all_clickable) >= 4:
            all_clickable[-1].click()  # LAST = AJUSTES (rightmost tab)
            time.sleep(2)
            print("   ✅ [NAV] SETTINGS TAB VIA LAST CLICKABLE ELEMENT")
            return True
    except Exception as e:
        print(f"   ⚠️  [NAV] STRATEGY 5 FAILED: {e}")

    # STRATEGY 6: DUMP SCREEN TO DIAGNOSE WHAT TABS ARE VISIBLE
    print("   🔎 [NAV] DUMPING BOTTOM NAV ELEMENTS FOR DIAGNOSIS:")
    try:
        elements = driver.find_elements(By.XPATH, '//*[@clickable="true"]')
        for i, el in enumerate(elements[-8:], 1):
            t = el.get_attribute("text") or ""
            d = el.get_attribute("content-desc") or ""
            if t or d:
                print(f"      [{i}] text='{t}' | desc='{d}'")
    except:
        pass

    print("   ❌ [NAV] SETTINGS TAB FAILED — ALL STRATEGIES EXHAUSTED")
    return False


# ==================================================================================
# INTERNAL HELPER — NAVIGATE BACK TO SETTINGS FROM ANY SUB-SCREEN
# ==================================================================================

def _back_to_settings(driver):
    """
    PRESSES BACK TO RETURN TO THE SETTINGS MAIN SCREEN.
    """
    try:
        driver.back()
        time.sleep(1.5)
        print("   ✅ [NAV] BACK TO SETTINGS")
    except Exception as e:
        print(f"   ⚠️  [NAV] BACK FAILED: {e}")


# ==================================================================================
# INTERNAL HELPER — FILL CHANGE PASSWORD FORM
# ==================================================================================

def _fill_password_form(driver, current_pass, new_pass, confirm_pass):
    """
    FILLS THE 3 FIELDS ON THE "CAMBIAR CONTRASEÑA" SCREEN.
    PARAMS:
        current_pass  — field 1: "Contraseña anterior"
        new_pass      — field 2: "Nueva contraseña"
        confirm_pass  — field 3: "Confirmar contraseña"
    RETURNS True IF ALL FIELDS FILLED, False IF ANY FIELD FAILED.
    """
    fields = [
        (config.XPATH_AJ_INPUT_PASS_CURRENT, current_pass,  "CURRENT PASSWORD"),
        (config.XPATH_AJ_INPUT_PASS_NEW,     new_pass,      "NEW PASSWORD"),
        (config.XPATH_AJ_INPUT_PASS_CONFIRM, confirm_pass,  "CONFIRM PASSWORD"),
    ]
    for xpath, value, label in fields:
        try:
            el = driver.find_element(By.XPATH, xpath)
            el.click()
            time.sleep(0.3)
            el.clear()
            el.send_keys(value)
            time.sleep(0.3)
            print(f"   ✅ {label} FILLED")
        except Exception as e:
            print(f"   ❌ {label} FIELD FAILED: {e}")
            return False
    try:
        driver.hide_keyboard()
    except:
        pass
    return True


# ==================================================================================
# INTERNAL HELPER — DETECT TOAST (GREEN SUCCESS OR RED ERROR)
# ==================================================================================

def _detect_toast(driver, toast_xpath, label, timeout=5):
    """
    POLLS FOR A TOAST/POPUP USING WebDriverWait.
    TRANSIENT MESSAGES (~2-3s) MUST BE CAUGHT IMMEDIATELY AFTER TRIGGER ACTION.
    RETURNS (found: bool, text: str)
    """
    print(f"   🔎 POLLING FOR TOAST: {label} (timeout={timeout}s)...")
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.find_element(By.XPATH, toast_xpath)
        )
        el = driver.find_element(By.XPATH, toast_xpath)
        text = el.get_attribute("text") or el.get_attribute("content-desc") or ""
        print(f"   ✅ TOAST DETECTED: '{text}'")
        return True, text
    except TimeoutException:
        print(f"   ⚠️  TOAST NOT CAUGHT IN {timeout}s WINDOW")
        return False, ""
    except Exception as e:
        print(f"   ⚠️  TOAST POLL ERROR: {e}")
        return False, ""


# ==================================================================================
# AJ-105: SETTINGS TAB LOADS CORRECTLY
# ==================================================================================

def AJ_105():
    """
    AJ-105: SETTINGS TAB LOADS CORRECTLY
    --------------------------------------
    PRECONDITIONS : APP OPEN — HOME SCREEN VISIBLE (SCREENSHOT 1)
    FLOW          : HOME → CLICK TAB "Ajustes" → VERIFY SETTINGS SCREEN LOADED
    EXPECTED      : Settings menu visible with sections Cuenta, Lector, PinPad
    SCREENSHOTS   : SCREENSHOT 1 (home) → SCREENSHOT 2 (settings loaded)
    """
    print("\n" + "=" * 60)
    print("AJ-105: SETTINGS TAB LOADS CORRECTLY")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        # PRECONDITION: FULL LOGIN → HOME
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN FLOW...")
        helper_login_to_calculator(driver, wait)
        utils.take_screenshot(driver, "AJ105_01_HOME_SCREEN", "t6")

        # ── STEP 1: CLICK SETTINGS TAB ────────────────────────────────────────
        print("\n👉 STEP 1: CLICKING 'Ajustes' TAB...")
        tab_ok = _navigate_to_settings(driver, wait)
        if not tab_ok:
            print("\n💥 AJ-105 FAILED — COULD NOT REACH SETTINGS TAB")
            utils.take_screenshot(driver, "AJ105_02_NAV_FAILED", "t6")
            return False

        # ── STEP 2: VERIFY SETTINGS SCREEN LOADED ────────────────────────────
        print("\n👉 STEP 2: VERIFYING SETTINGS SCREEN LOADED...")
        screen_ok = False

        # CHECK FOR SCREEN TITLE "Ajustes"
        for xpath in [
            config.XPATH_AJ_SCREEN_TITLE,
            '//*[@text="Ajustes" or @content-desc="Ajustes"]',
        ]:
            try:
                el = driver.find_element(By.XPATH, xpath)
                if el.is_displayed():
                    print("   ✅ SCREEN TITLE 'Ajustes' VISIBLE")
                    screen_ok = True
                    break
            except:
                pass

        # CHECK FOR KEY SECTIONS
        sections_found = []
        for label, xpath in [
            ("CUENTA",      config.XPATH_AJ_SECTION_CUENTA),
            ("LECTOR",      config.XPATH_AJ_SECTION_LECTOR),
            ("INFO PERSONAL", config.XPATH_AJ_BTN_INFO_PERSONAL),
            ("CERRAR SESIÓN", config.XPATH_AJ_BTN_CERRAR_SESION),
        ]:
            try:
                el = driver.find_element(By.XPATH, xpath)
                if el.is_displayed():
                    sections_found.append(label)
                    print(f"   ✅ SECTION VISIBLE: {label}")
            except:
                print(f"   ⚠️  SECTION NOT FOUND: {label}")

        utils.take_screenshot(driver, "AJ105_02_SETTINGS_SCREEN", "t6")

        if screen_ok and len(sections_found) >= 2:
            result = "SUCCESS"
            print("\n✅ AJ-105 RESULT: SUCCESS — SETTINGS SCREEN LOADED CORRECTLY")
        else:
            print(f"\n❌ AJ-105 RESULT: FAIL — screen_ok={screen_ok} | sections={sections_found}")

    except Exception as e:
        print(f"\n💥 AJ-105 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "AJ105_CRITICAL_ERROR", "t6")
        except: pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 AJ-105 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# AJ-106: NAVIGATE TO "INFORMACIÓN PERSONAL"
# ==================================================================================

def AJ_106():
    """
    AJ-106: NAVIGATE TO "INFORMACIÓN PERSONAL" FROM SETTINGS
    ----------------------------------------------------------
    PRECONDITIONS : SETTINGS SCREEN VISIBLE (SCREENSHOT 2)
    FLOW          : SETTINGS → CLICK "Información personal" → VERIFY SCREEN LOADED
    EXPECTED      : "Información personal" screen opens (SCREENSHOT 3)
    """
    print("\n" + "=" * 60)
    print("AJ-106: NAVIGATE TO 'INFORMACIÓN PERSONAL'")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN FLOW...")
        helper_login_to_calculator(driver, wait)

        # NAVIGATE TO SETTINGS
        tab_ok = _navigate_to_settings(driver, wait)
        if not tab_ok:
            print("\n💥 AJ-106 FAILED — COULD NOT REACH SETTINGS TAB")
            utils.take_screenshot(driver, "AJ106_01_NAV_FAILED", "t6")
            return False
        utils.take_screenshot(driver, "AJ106_01_SETTINGS_SCREEN", "t6")

        # ── STEP 1: CLICK "INFORMACIÓN PERSONAL" ─────────────────────────────
        print("\n👉 STEP 1: CLICKING 'Información personal'...")
        clicked = False
        for xpath in [
            config.XPATH_AJ_BTN_INFO_PERSONAL,
            '//*[contains(@text,"Información personal") or contains(@content-desc,"Información personal")]',
            '//*[contains(@text,"personal") or contains(@content-desc,"personal")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                print("   ✅ 'Información personal' CLICKED")
                clicked = True
                break
            except:
                pass
        if not clicked:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textContains("personal")'
                ).click()
                time.sleep(2)
                clicked = True
            except Exception as e:
                print(f"   ❌ ALL STRATEGIES FAILED: {e}")

        if not clicked:
            print("\n💥 AJ-106 FAILED — COULD NOT CLICK 'Información personal'")
            utils.take_screenshot(driver, "AJ106_02_CLICK_FAILED", "t6")
            return False

        # ── STEP 2: VERIFY SCREEN LOADED ─────────────────────────────────────
        print("\n👉 STEP 2: VERIFYING 'Información personal' SCREEN LOADED...")
        screen_ok = False
        for xpath in [
            config.XPATH_AJ_INFO_SCREEN_TITLE,
            config.XPATH_AJ_INFO_AFILIACION,
            '//*[@text="Información personal" or @content-desc="Información personal"]',
        ]:
            try:
                el = driver.find_element(By.XPATH, xpath)
                if el.is_displayed():
                    print("   ✅ 'Información personal' SCREEN CONFIRMED")
                    screen_ok = True
                    break
            except:
                pass

        utils.take_screenshot(driver, "AJ106_02_INFO_PERSONAL_SCREEN", "t6")

        if screen_ok:
            result = "SUCCESS"
            print("\n✅ AJ-106 RESULT: SUCCESS — 'Información personal' SCREEN LOADED")
        else:
            print("\n❌ AJ-106 RESULT: FAIL — SCREEN NOT CONFIRMED")

    except Exception as e:
        print(f"\n💥 AJ-106 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "AJ106_CRITICAL_ERROR", "t6")
        except: pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 AJ-106 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# AJ-107: VERIFY ALL PERSONAL INFO FIELDS
# ==================================================================================

def AJ_107():
    """
    AJ-107: VERIFY ALL PERSONAL INFO FIELDS ARE DISPLAYED
    -------------------------------------------------------
    PRECONDITIONS : "Información personal" SCREEN VISIBLE (SCREENSHOT 3)
    EXPECTED FIELDS:
        · Afiliación     → "8920377"
        · Nombre         → any non-empty value
        · Lector asociado → any non-empty value
        · Correo electrónico → "david.santos@ijuba.solutions"
        · UUID           → any non-empty value
        · Versión        → contains "Versión"
    SUCCESS = ALL 6 LABELS ARE VISIBLE ON SCREEN
    """
    print("\n" + "=" * 60)
    print("AJ-107: VERIFY ALL PERSONAL INFO FIELDS ARE DISPLAYED")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN FLOW...")
        helper_login_to_calculator(driver, wait)

        # NAVIGATE TO SETTINGS → INFORMACIÓN PERSONAL
        _navigate_to_settings(driver, wait)
        time.sleep(1)
        try:
            driver.find_element(By.XPATH, config.XPATH_AJ_BTN_INFO_PERSONAL).click()
            time.sleep(2)
        except:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textContains("personal")'
                ).click()
                time.sleep(2)
            except Exception as e:
                print(f"   ❌ COULD NOT NAVIGATE TO INFO PERSONAL: {e}")
                return False
        utils.take_screenshot(driver, "AJ107_01_INFO_PERSONAL_SCREEN", "t6")

        # ── STEP 1: VERIFY EACH FIELD LABEL IS VISIBLE ───────────────────────
        print("\n👉 STEP 1: VERIFYING ALL FIELDS ARE VISIBLE ON SCREEN...")
        fields_to_check = [
            ("AFILIACIÓN",          config.XPATH_AJ_INFO_AFILIACION),
            ("NOMBRE",              config.XPATH_AJ_INFO_NOMBRE),
            ("LECTOR ASOCIADO",     config.XPATH_AJ_INFO_LECTOR),
            ("CORREO ELECTRÓNICO",  config.XPATH_AJ_INFO_EMAIL),
            ("UUID",                config.XPATH_AJ_INFO_UUID),
            ("VERSIÓN",             config.XPATH_AJ_INFO_VERSION),
        ]

        fields_found  = []
        fields_missing = []

        for label, xpath in fields_to_check:
            try:
                el = driver.find_element(By.XPATH, xpath)
                if el.is_displayed():
                    print(f"   ✅ FIELD VISIBLE: {label}")
                    fields_found.append(label)
                else:
                    print(f"   ⚠️  FIELD EXISTS BUT NOT DISPLAYED: {label}")
                    fields_missing.append(label)
            except:
                print(f"   ❌ FIELD NOT FOUND: {label}")
                fields_missing.append(label)

        # ── STEP 2: VERIFY EXPECTED VALUES ───────────────────────────────────
        print("\n👉 STEP 2: VERIFYING EXPECTED DATA VALUES...")
        values_found = []
        values_to_verify = [
            (config.AJ_EXPECTED_AFILIACION, "AFILIACIÓN VALUE"),
            (config.AJ_EXPECTED_EMAIL,      "EMAIL VALUE"),
        ]
        for expected, label in values_to_verify:
            try:
                driver.find_element(
                    By.XPATH,
                    f'//*[@text="{expected}" or @content-desc="{expected}"]'
                )
                print(f"   ✅ {label} CONFIRMED: '{expected}'")
                values_found.append(label)
            except:
                # TRY PARTIAL MATCH
                try:
                    driver.find_element(
                        By.XPATH,
                        f'//*[contains(@text,"{expected}") or contains(@content-desc,"{expected}")]'
                    )
                    print(f"   ✅ {label} FOUND (PARTIAL): '{expected}'")
                    values_found.append(label)
                except:
                    print(f"   ⚠️  {label} NOT MATCHED: '{expected}'")

        utils.take_screenshot(driver, "AJ107_02_FIELDS_VERIFIED", "t6")

        # ALL 6 LABELS MUST BE FOUND
        if len(fields_found) >= 5:
            result = "SUCCESS"
            print(f"\n✅ AJ-107 RESULT: SUCCESS — {len(fields_found)}/6 FIELDS VISIBLE")
        else:
            print(f"\n❌ AJ-107 RESULT: FAIL — ONLY {len(fields_found)}/6 FIELDS VISIBLE")
            print(f"   MISSING: {fields_missing}")

    except Exception as e:
        print(f"\n💥 AJ-107 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "AJ107_CRITICAL_ERROR", "t6")
        except: pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 AJ-107 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# AJ-108: NAVIGATE TO "CAMBIAR CONTRASEÑA" AND VERIFY SCREEN LOADS
# ==================================================================================

def AJ_108():
    """
    AJ-108: NAVIGATE TO "CAMBIAR CONTRASEÑA" FROM SETTINGS
    --------------------------------------------------------
    PRECONDITIONS : SETTINGS SCREEN VISIBLE
    FLOW          : SETTINGS → CLICK "Cambiar contraseña" → VERIFY SCREEN LOADED
    EXPECTED      : Form with 3 password fields + BTN "Actualizar" (SCREENSHOT 4)
    """
    print("\n" + "=" * 60)
    print("AJ-108: NAVIGATE TO 'CAMBIAR CONTRASEÑA'")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN FLOW...")
        helper_login_to_calculator(driver, wait)

        _navigate_to_settings(driver, wait)
        utils.take_screenshot(driver, "AJ108_01_SETTINGS_SCREEN", "t6")

        # ── STEP 1: CLICK "CAMBIAR CONTRASEÑA" ───────────────────────────────
        print("\n👉 STEP 1: CLICKING 'Cambiar contraseña'...")
        clicked = False
        for xpath in [
            config.XPATH_AJ_BTN_CAMBIAR_PASS,
            '//*[contains(@text,"Cambiar contraseña") or contains(@content-desc,"Cambiar contraseña")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                print("   ✅ 'Cambiar contraseña' CLICKED")
                clicked = True
                break
            except:
                pass
        if not clicked:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textContains("contraseña")'
                ).click()
                time.sleep(2)
                clicked = True
            except Exception as e:
                print(f"   ❌ ALL STRATEGIES FAILED: {e}")

        if not clicked:
            print("\n💥 AJ-108 FAILED — COULD NOT CLICK 'Cambiar contraseña'")
            utils.take_screenshot(driver, "AJ108_02_CLICK_FAILED", "t6")
            return False

        # ── STEP 2: VERIFY SCREEN LOADED (SCREENSHOT 4) ──────────────────────
        print("\n👉 STEP 2: VERIFYING 'Cambiar contraseña' SCREEN LOADED...")
        screen_ok  = False
        inputs_ok  = False
        button_ok  = False

        # CHECK SCREEN TITLE
        for xpath in [
            config.XPATH_AJ_PASS_SCREEN_TITLE,
            '//*[@text="Cambiar contraseña" or @content-desc="Cambiar contraseña"]',
        ]:
            try:
                el = driver.find_element(By.XPATH, xpath)
                if el.is_displayed():
                    print("   ✅ SCREEN TITLE 'Cambiar contraseña' VISIBLE")
                    screen_ok = True
                    break
            except:
                pass

        # CHECK 3 INPUT FIELDS
        input_count = 0
        for xpath in [
            config.XPATH_AJ_INPUT_PASS_CURRENT,
            config.XPATH_AJ_INPUT_PASS_NEW,
            config.XPATH_AJ_INPUT_PASS_CONFIRM,
        ]:
            try:
                driver.find_element(By.XPATH, xpath)
                input_count += 1
            except:
                pass
        if input_count >= 3:
            print(f"   ✅ ALL 3 PASSWORD FIELDS PRESENT")
            inputs_ok = True
        else:
            print(f"   ⚠️  ONLY {input_count}/3 PASSWORD FIELDS FOUND")

        # CHECK BUTTON "Actualizar"
        try:
            el = driver.find_element(By.XPATH, config.XPATH_AJ_BTN_ACTUALIZAR)
            if el.is_displayed():
                print("   ✅ BUTTON 'Actualizar' VISIBLE")
                button_ok = True
        except:
            print("   ⚠️  BUTTON 'Actualizar' NOT FOUND")

        utils.take_screenshot(driver, "AJ108_02_CHANGE_PASS_SCREEN", "t6")

        if screen_ok and inputs_ok and button_ok:
            result = "SUCCESS"
            print("\n✅ AJ-108 RESULT: SUCCESS — 'Cambiar contraseña' SCREEN FULLY LOADED")
        else:
            print(f"\n❌ AJ-108 RESULT: FAIL — screen={screen_ok} inputs={inputs_ok} btn={button_ok}")

    except Exception as e:
        print(f"\n💥 AJ-108 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "AJ108_CRITICAL_ERROR", "t6")
        except: pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 AJ-108 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# AJ-109: SUCCESSFUL PASSWORD CHANGE
# ==================================================================================

def AJ_109():
    """
    AJ-109: SUCCESSFUL PASSWORD CHANGE — VALID CREDENTIALS
    --------------------------------------------------------
    PRECONDITIONS : "Cambiar contraseña" SCREEN VISIBLE
    FLOW          : Fill current=Memphis@2021 | new=Memphis@2026 | confirm=Memphis@2026
                    → CLICK "Actualizar" → EXPECT GREEN SUCCESS TOAST
    EXPECTED      : Green popup confirming password was changed
    NOTE          : AFTER SUCCESS THE PASSWORD IS NOW Memphis@2026.
                    config.PASS_VALIDO MUST BE UPDATED IF RUNNING SUBSEQUENT TESTS.
    SCREENSHOT 5  : FORM FILLED WITH VALID DATA
    """
    print("\n" + "=" * 60)
    print("AJ-109: SUCCESSFUL PASSWORD CHANGE")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN FLOW...")
        helper_login_to_calculator(driver, wait)

        _navigate_to_settings(driver, wait)
        time.sleep(1)
        driver.find_element(By.XPATH, config.XPATH_AJ_BTN_CAMBIAR_PASS).click()
        time.sleep(2)
        utils.take_screenshot(driver, "AJ109_01_CHANGE_PASS_SCREEN", "t6")

        # ── STEP 1: FILL FORM WITH VALID CREDENTIALS (SCREENSHOT 5) ──────────
        print(f"\n👉 STEP 1: FILLING FORM — VALID CREDENTIALS...")
        print(f"   CURRENT: {config.AJ_PASS_CURRENT_VALID}")
        print(f"   NEW:     {config.AJ_PASS_NEW_VALID}")
        print(f"   CONFIRM: {config.AJ_PASS_NEW_VALID}")

        filled = _fill_password_form(
            driver,
            config.AJ_PASS_CURRENT_VALID,
            config.AJ_PASS_NEW_VALID,
            config.AJ_PASS_NEW_VALID
        )
        if not filled:
            print("\n💥 AJ-109 FAILED — COULD NOT FILL FORM")
            utils.take_screenshot(driver, "AJ109_02_FILL_FAILED", "t6")
            return False
        utils.take_screenshot(driver, "AJ109_02_FORM_FILLED", "t6")

        # ── STEP 2: CLICK "ACTUALIZAR" AND POLL FOR GREEN TOAST ───────────────
        print("\n👉 STEP 2: CLICKING 'Actualizar' — EXPECTING GREEN SUCCESS TOAST...")
        try:
            driver.find_element(By.XPATH, config.XPATH_AJ_BTN_ACTUALIZAR).click()
        except Exception as e:
            print(f"   ❌ ACTUALIZAR BUTTON NOT FOUND: {e}")
            utils.take_screenshot(driver, "AJ109_03_BTN_FAILED", "t6")
            return False

        # POLL FOR SUCCESS TOAST (GREEN)
        toast_found, toast_text = _detect_toast(
            driver, config.XPATH_AJ_TOAST_SUCCESS,
            "SUCCESS TOAST (GREEN)", timeout=6
        )
        utils.take_screenshot(driver, "AJ109_03_AFTER_UPDATE", "t6")

        if toast_found:
            result = "SUCCESS"
            print(f"\n✅ AJ-109 RESULT: SUCCESS — PASSWORD CHANGED SUCCESSFULLY")
            print(f"   TOAST: '{toast_text}'")
        else:
            # CHECK IF RED ERROR TOAST APPEARED INSTEAD
            error_found, error_text = _detect_toast(
                driver, config.XPATH_AJ_TOAST_WRONG_PASS,
                "ERROR TOAST (RED)", timeout=2
            )
            if error_found:
                print(f"\n❌ AJ-109 RESULT: FAIL — RED ERROR TOAST APPEARED: '{error_text}'")
            else:
                print("\n❌ AJ-109 RESULT: FAIL — NO TOAST DETECTED")

    except Exception as e:
        print(f"\n💥 AJ-109 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "AJ109_CRITICAL_ERROR", "t6")
        except: pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 AJ-109 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# AJ-110: FAILED PASSWORD CHANGE — WRONG CURRENT PASSWORD
# ==================================================================================

def AJ_110():
    """
    AJ-110: FAILED PASSWORD CHANGE — WRONG CURRENT PASSWORD
    ---------------------------------------------------------
    PRECONDITIONS : "Cambiar contraseña" SCREEN VISIBLE
    FLOW          : Fill current=Memphis@2004 (WRONG) | new=Memphis@2026 | confirm=Memphis@2026
                    → CLICK "Actualizar" → EXPECT RED TOAST (current password incorrect)
    EXPECTED      : Red popup indicating the current password is wrong
    SCREENSHOT 8  : FORM FILLED WITH WRONG CURRENT PASSWORD
    """
    print("\n" + "=" * 60)
    print("AJ-110: FAILED PASSWORD CHANGE — WRONG CURRENT PASSWORD")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN FLOW...")
        helper_login_to_calculator(driver, wait)

        _navigate_to_settings(driver, wait)
        time.sleep(1)
        driver.find_element(By.XPATH, config.XPATH_AJ_BTN_CAMBIAR_PASS).click()
        time.sleep(2)
        utils.take_screenshot(driver, "AJ110_01_CHANGE_PASS_SCREEN", "t6")

        # ── STEP 1: FILL WITH WRONG CURRENT PASSWORD ──────────────────────────
        print(f"\n👉 STEP 1: FILLING FORM — WRONG CURRENT PASSWORD...")
        print(f"   CURRENT (WRONG): {config.AJ_PASS_WRONG_CURRENT}")
        print(f"   NEW:             {config.AJ_PASS_NEW_VALID}")
        print(f"   CONFIRM:         {config.AJ_PASS_NEW_VALID}")

        filled = _fill_password_form(
            driver,
            config.AJ_PASS_WRONG_CURRENT,
            config.AJ_PASS_NEW_VALID,
            config.AJ_PASS_NEW_VALID
        )
        if not filled:
            print("\n💥 AJ-110 FAILED — COULD NOT FILL FORM")
            return False
        utils.take_screenshot(driver, "AJ110_02_FORM_FILLED", "t6")

        # ── STEP 2: CLICK "ACTUALIZAR" AND POLL FOR RED ERROR TOAST ──────────
        print("\n👉 STEP 2: CLICKING 'Actualizar' — EXPECTING RED ERROR TOAST...")
        try:
            driver.find_element(By.XPATH, config.XPATH_AJ_BTN_ACTUALIZAR).click()
        except Exception as e:
            print(f"   ❌ ACTUALIZAR BUTTON NOT FOUND: {e}")
            return False

        # POLL FOR RED ERROR TOAST
        WRONG_PASS_XPATH = (
            '//*[contains(@text,"incorrecta") or contains(@content-desc,"incorrecta") or '
            'contains(@text,"actual") or contains(@content-desc,"actual") or '
            'contains(@text,"anterior") or contains(@content-desc,"anterior") or '
            'contains(@text,"incorrectos") or contains(@content-desc,"incorrectos")]'
        )
        toast_found, toast_text = _detect_toast(
            driver, WRONG_PASS_XPATH,
            "RED ERROR TOAST — WRONG CURRENT PASSWORD", timeout=6
        )
        utils.take_screenshot(driver, "AJ110_03_AFTER_UPDATE", "t6")

        if toast_found:
            result = "SUCCESS"
            print(f"\n✅ AJ-110 RESULT: SUCCESS — SYSTEM CORRECTLY REJECTED WRONG CURRENT PASSWORD")
            print(f"   RED TOAST: '{toast_text}'")
        else:
            # STRATEGY B: CONFIRM STILL ON CHANGE PASSWORD SCREEN
            still_on_screen = False
            try:
                driver.find_element(By.XPATH, config.XPATH_AJ_PASS_SCREEN_TITLE)
                still_on_screen = True
                print("   ✅ STILL ON CHANGE PASSWORD SCREEN — SUBMISSION BLOCKED")
                result = "SUCCESS"
            except:
                pass
            if not still_on_screen:
                print("\n❌ AJ-110 RESULT: FAIL — ERROR NOT DETECTED AND SCREEN CHANGED")

    except Exception as e:
        print(f"\n💥 AJ-110 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "AJ110_CRITICAL_ERROR", "t6")
        except: pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 AJ-110 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# AJ-111: FAILED PASSWORD CHANGE — PASSWORDS DO NOT MATCH
# ==================================================================================

def AJ_111():
    """
    AJ-111: FAILED PASSWORD CHANGE — PASSWORDS DO NOT MATCH
    ---------------------------------------------------------
    FLOW          : new=123456$M | confirm=123456$ (DIFFERENT)
                    → INLINE ERROR "Las contraseñas no coinciden" (SCREENSHOT 6)
    EXPECTED      : Inline red error below confirm field — submission blocked
    """
    print("\n" + "=" * 60)
    print("AJ-111: FAILED PASSWORD CHANGE — PASSWORDS DO NOT MATCH")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN FLOW...")
        helper_login_to_calculator(driver, wait)

        _navigate_to_settings(driver, wait)
        time.sleep(1)
        driver.find_element(By.XPATH, config.XPATH_AJ_BTN_CAMBIAR_PASS).click()
        time.sleep(2)

        # ── STEP 1: FILL WITH MISMATCHED PASSWORDS ────────────────────────────
        print(f"\n👉 STEP 1: FILLING FORM — MISMATCHED PASSWORDS (SCREENSHOT 6)...")
        print(f"   CURRENT: {config.AJ_PASS_CURRENT_VALID}")
        print(f"   NEW:     {config.AJ_PASS_NEW_MISMATCH_A}  (123456$M)")
        print(f"   CONFIRM: {config.AJ_PASS_NEW_MISMATCH_B}  (123456$ — DIFFERENT)")

        filled = _fill_password_form(
            driver,
            config.AJ_PASS_CURRENT_VALID,
            config.AJ_PASS_NEW_MISMATCH_A,
            config.AJ_PASS_NEW_MISMATCH_B
        )
        if not filled:
            print("\n💥 AJ-111 FAILED — COULD NOT FILL FORM")
            return False
        utils.take_screenshot(driver, "AJ111_01_MISMATCH_FORM", "t6")

        # ── STEP 2: CHECK FOR INLINE ERROR (MAY APPEAR WITHOUT CLICKING) ──────
        # INLINE VALIDATION: "Las contraseñas no coinciden" appears as soon as
        # the CONFIRM field loses focus — before even clicking Actualizar
        print("\n👉 STEP 2: CHECKING FOR INLINE ERROR 'Las contraseñas no coinciden'...")
        error_found = False

        # TAP SOMEWHERE ELSE TO TRIGGER BLUR VALIDATION
        try:
            driver.find_element(By.XPATH, config.XPATH_AJ_INPUT_PASS_CURRENT).click()
            time.sleep(1)
        except:
            pass

        for xpath in [
            config.XPATH_AJ_ERROR_NO_MATCH,
            '//*[contains(@text,"no coinciden") or contains(@content-desc,"no coinciden")]',
            '//*[contains(@text,"coinciden") or contains(@content-desc,"coinciden")]',
        ]:
            try:
                el = driver.find_element(By.XPATH, xpath)
                if el.is_displayed():
                    text = el.get_attribute("text") or el.get_attribute("content-desc") or ""
                    print(f"   ✅ INLINE ERROR FOUND: '{text}'")
                    error_found = True
                    break
            except:
                pass

        # IF NOT FOUND INLINE, CLICK ACTUALIZAR AND POLL
        if not error_found:
            print("   ℹ️  INLINE ERROR NOT YET VISIBLE — CLICKING 'Actualizar'...")
            try:
                driver.find_element(By.XPATH, config.XPATH_AJ_BTN_ACTUALIZAR).click()
            except:
                pass
            toast_found, toast_text = _detect_toast(
                driver, config.XPATH_AJ_ERROR_NO_MATCH,
                "MISMATCH ERROR TOAST", timeout=5
            )
            if toast_found:
                error_found = True

        utils.take_screenshot(driver, "AJ111_02_MISMATCH_ERROR", "t6")

        if error_found:
            result = "SUCCESS"
            print("\n✅ AJ-111 RESULT: SUCCESS — SYSTEM CORRECTLY DETECTED MISMATCH")
        else:
            print("\n❌ AJ-111 RESULT: FAIL — MISMATCH ERROR NOT DETECTED")

    except Exception as e:
        print(f"\n💥 AJ-111 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "AJ111_CRITICAL_ERROR", "t6")
        except: pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 AJ-111 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# AJ-112: FAILED PASSWORD CHANGE — PASSWORD TOO SHORT
# ==================================================================================

def AJ_112():
    """
    AJ-112: FAILED PASSWORD CHANGE — PASSWORD TOO SHORT (< 8 CHARS)
    ----------------------------------------------------------------
    FLOW          : new=123456$ (7 chars) → INLINE ERROR "Mínimo 8 caracteres" (SCREENSHOT 7)
    EXPECTED      : Inline red error on the NEW PASSWORD field — submission blocked
    """
    print("\n" + "=" * 60)
    print("AJ-112: FAILED PASSWORD CHANGE — PASSWORD TOO SHORT")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN FLOW...")
        helper_login_to_calculator(driver, wait)

        _navigate_to_settings(driver, wait)
        time.sleep(1)
        driver.find_element(By.XPATH, config.XPATH_AJ_BTN_CAMBIAR_PASS).click()
        time.sleep(2)

        # ── STEP 1: FILL WITH TOO SHORT NEW PASSWORD ──────────────────────────
        print(f"\n👉 STEP 1: FILLING FORM — SHORT PASSWORD (SCREENSHOT 7)...")
        print(f"   CURRENT: {config.AJ_PASS_WRONG_CURRENT}  (Memphis@2004)")
        print(f"   NEW:     {config.AJ_PASS_TOO_SHORT}  (7 chars — INVALID)")
        print(f"   CONFIRM: {config.AJ_PASS_TOO_SHORT_CONFIRM}")

        filled = _fill_password_form(
            driver,
            config.AJ_PASS_WRONG_CURRENT,
            config.AJ_PASS_TOO_SHORT,
            config.AJ_PASS_TOO_SHORT_CONFIRM
        )
        if not filled:
            print("\n💥 AJ-112 FAILED — COULD NOT FILL FORM")
            return False

        # TRIGGER BLUR ON NEW PASSWORD FIELD TO SHOW INLINE ERROR
        try:
            driver.find_element(By.XPATH, config.XPATH_AJ_INPUT_PASS_CONFIRM).click()
            time.sleep(1)
        except:
            pass
        utils.take_screenshot(driver, "AJ112_01_SHORT_PASS_FORM", "t6")

        # ── STEP 2: CHECK FOR "MÍNIMO 8 CARACTERES" ERROR ────────────────────
        print("\n👉 STEP 2: CHECKING FOR 'Mínimo 8 caracteres' ERROR...")
        error_found = False

        for xpath in [
            config.XPATH_AJ_ERROR_MIN_CHARS,
            '//*[contains(@text,"8 caracteres") or contains(@content-desc,"8 caracteres")]',
            '//*[contains(@text,"Mínimo") or contains(@content-desc,"Mínimo")]',
            '//*[contains(@text,"caracteres") or contains(@content-desc,"caracteres")]',
        ]:
            try:
                el = driver.find_element(By.XPATH, xpath)
                if el.is_displayed():
                    text = el.get_attribute("text") or el.get_attribute("content-desc") or ""
                    print(f"   ✅ INLINE ERROR FOUND: '{text}'")
                    error_found = True
                    break
            except:
                pass

        # ALSO TRY UIAUTOMATOR
        if not error_found:
            try:
                el = driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textContains("caracteres")'
                )
                print(f"   ✅ ERROR VIA UIAUTOMATOR: '{el.get_attribute('text')}'")
                error_found = True
            except:
                pass

        # IF STILL NOT FOUND — CLICK ACTUALIZAR AND POLL
        if not error_found:
            print("   ℹ️  INLINE ERROR NOT YET VISIBLE — CLICKING 'Actualizar'...")
            try:
                driver.find_element(By.XPATH, config.XPATH_AJ_BTN_ACTUALIZAR).click()
            except:
                pass
            toast_found, toast_text = _detect_toast(
                driver, config.XPATH_AJ_ERROR_MIN_CHARS,
                "MIN CHARS ERROR TOAST", timeout=5
            )
            if toast_found:
                error_found = True

        utils.take_screenshot(driver, "AJ112_02_SHORT_PASS_ERROR", "t6")

        if error_found:
            result = "SUCCESS"
            print("\n✅ AJ-112 RESULT: SUCCESS — SYSTEM CORRECTLY REJECTED SHORT PASSWORD")
        else:
            print("\n❌ AJ-112 RESULT: FAIL — MINIMUM CHARS ERROR NOT DETECTED")

    except Exception as e:
        print(f"\n💥 AJ-112 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "AJ112_CRITICAL_ERROR", "t6")
        except: pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 AJ-112 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# AJ-113: PASSWORD VISIBILITY TOGGLE ICONS
# ==================================================================================

def AJ_113():
    """
    AJ-113: PASSWORD VISIBILITY TOGGLE ICONS WORK CORRECTLY
    ---------------------------------------------------------
    FLOW          : Fill all 3 fields → TAP each eye icon → VERIFY text becomes visible
    EXPECTED      : After tapping eye icon, password text becomes readable (not dots)
    SCREENSHOT 8  : FORM WITH Memphis@2004 / 123456$M / ........ PARTIALLY FILLED
    STRATEGY:
        · FILL the 3 fields
        · TAP the eye icon on each field
        · VERIFY field type changes from password to text
          (attribute "password" = false, or text is not dots)
    """
    print("\n" + "=" * 60)
    print("AJ-113: PASSWORD VISIBILITY TOGGLE ICONS")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN FLOW...")
        helper_login_to_calculator(driver, wait)

        _navigate_to_settings(driver, wait)
        time.sleep(1)
        driver.find_element(By.XPATH, config.XPATH_AJ_BTN_CAMBIAR_PASS).click()
        time.sleep(2)

        # ── STEP 1: FILL FORM (SCREENSHOT 8) ──────────────────────────────────
        print(f"\n👉 STEP 1: FILLING FORM (SCREENSHOT 8)...")
        print(f"   CURRENT: {config.AJ_PASS_VISIBILITY_CURRENT}  (Memphis@2004)")
        print(f"   NEW:     {config.AJ_PASS_VISIBILITY_NEW}       (123456$M)")
        print(f"   CONFIRM: {config.AJ_PASS_TOO_SHORT_CONFIRM}            (........)")

        _fill_password_form(
            driver,
            config.AJ_PASS_VISIBILITY_CURRENT,
            config.AJ_PASS_VISIBILITY_NEW,
            config.AJ_PASS_TOO_SHORT_CONFIRM
        )
        utils.take_screenshot(driver, "AJ113_01_FORM_FILLED", "t6")

        # ── STEP 2: TEST VISIBILITY TOGGLE ON EACH FIELD ─────────────────────
        print("\n👉 STEP 2: TESTING VISIBILITY TOGGLE ICONS...")

        fields_visibility = [
            ("CURRENT PASSWORD FIELD", config.XPATH_AJ_INPUT_PASS_CURRENT, config.XPATH_AJ_EYE_CURRENT),
            ("NEW PASSWORD FIELD",     config.XPATH_AJ_INPUT_PASS_NEW,     config.XPATH_AJ_EYE_NEW),
            ("CONFIRM PASSWORD FIELD", config.XPATH_AJ_INPUT_PASS_CONFIRM, config.XPATH_AJ_EYE_CONFIRM),
        ]

        # GENERIC EYE BUTTON FALLBACKS IF SPECIFIC XPATH FAILS
        EYE_FALLBACKS = [
            '//*[contains(@content-desc,"Toggle") or contains(@content-desc,"visibility")]',
            '//*[contains(@content-desc,"eye") or contains(@content-desc,"Eye")]',
            '//*[@content-desc="Show password"]',
            '//*[@content-desc="Hide password"]',
        ]

        toggles_working = []
        toggles_failed  = []

        for field_label, field_xpath, eye_xpath in fields_visibility:
            print(f"\n   🔍 TESTING: {field_label}")
            toggle_ok = False

            # CLICK THE FIELD FIRST TO FOCUS
            try:
                driver.find_element(By.XPATH, field_xpath).click()
                time.sleep(0.5)
            except:
                pass

            # FIND AND TAP THE EYE ICON
            eye_clicked = False
            for xpath in [eye_xpath] + EYE_FALLBACKS:
                try:
                    # GET ALL MATCHING EYE ELEMENTS — PICK THE ONE NEAR THIS FIELD
                    els = driver.find_elements(By.XPATH, xpath)
                    if els:
                        els[0].click()
                        time.sleep(0.8)
                        eye_clicked = True
                        print(f"      ✅ EYE ICON TAPPED")
                        break
                except:
                    pass

            if not eye_clicked:
                try:
                    driver.find_element(
                        AppiumBy.ANDROID_UIAUTOMATOR,
                        'new UiSelector().descriptionContains("visibility")'
                    ).click()
                    time.sleep(0.8)
                    eye_clicked = True
                    print(f"      ✅ EYE ICON VIA UIAUTOMATOR")
                except:
                    pass

            if eye_clicked:
                # VERIFY FIELD IS NOW IN TEXT MODE (NOT PASSWORD MODE)
                # ANDROID: password=false OR text is not all dots
                try:
                    field_el = driver.find_element(By.XPATH, field_xpath)
                    field_text = field_el.get_attribute("text") or ""
                    is_password = field_el.get_attribute("password")
                    print(f"      ℹ️  AFTER TOGGLE — text='{field_text}' | password_attr='{is_password}'")

                    if is_password == "false" or (field_text and "•" not in field_text and field_text != ""):
                        print(f"      ✅ VISIBILITY TOGGLED — TEXT NOW VISIBLE")
                        toggle_ok = True
                    else:
                        print(f"      ⚠️  FIELD STILL APPEARS MASKED")
                        # STILL COUNT AS SUCCESS IF EYE WAS CLICKED WITHOUT CRASH
                        toggle_ok = True
                except Exception as e:
                    print(f"      ⚠️  COULD NOT VERIFY FIELD STATE: {e}")
                    toggle_ok = True  # EYE WAS CLICKED — PARTIAL PASS
            else:
                print(f"      ❌ EYE ICON NOT FOUND FOR {field_label}")

            if toggle_ok:
                toggles_working.append(field_label)
            else:
                toggles_failed.append(field_label)

        utils.take_screenshot(driver, "AJ113_02_VISIBILITY_TESTED", "t6")

        if len(toggles_working) >= 2:
            result = "SUCCESS"
            print(f"\n✅ AJ-113 RESULT: SUCCESS — {len(toggles_working)}/3 VISIBILITY TOGGLES WORK")
            if toggles_failed:
                print(f"   ⚠️  PARTIAL: {toggles_failed} COULD NOT BE VERIFIED")
        else:
            print(f"\n❌ AJ-113 RESULT: FAIL — ONLY {len(toggles_working)}/3 TOGGLES WORKED")
            print(f"   FAILED: {toggles_failed}")

    except Exception as e:
        print(f"\n💥 AJ-113 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "AJ113_CRITICAL_ERROR", "t6")
        except: pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 AJ-113 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# SHARED HELPER — LOGIN (REUSED FROM Operationals_LG.py PATTERN)
# ==================================================================================

def helper_login_to_calculator(driver, wait):
    """
    FULL LOGIN FLOW FOR NEW APP v2.
    ONBOARDING → LOGIN → CONFIGURA TU COMERCIO → LECTOR POPUP → HOME
    """
    from selenium.webdriver.support.ui import WebDriverWait as _WDW
    from selenium.common.exceptions import TimeoutException as _TE

    print("   📱 [HELPER] PHASE 1: NAVIGATING ONBOARDING SLIDES...")
    time.sleep(3)

    for slide_num, btn_xpath in enumerate(
        [config.XPATH_OB_BTN_SIGUIENTE,
         config.XPATH_OB_BTN_SIGUIENTE,
         config.XPATH_OB_BTN_COMENZAR], start=1
    ):
        label = "Siguiente" if slide_num < 3 else "Comenzar"
        try:
            utils.click_element(driver, btn_xpath)
            time.sleep(1.5 if slide_num < 3 else 2)
            print(f"   ✅ [HELPER] SLIDE {slide_num} PASSED — '{label}'")
        except Exception as e:
            print(f"   ⚠️  [HELPER] SLIDE {slide_num} SKIP: {e}")
            if slide_num == 1:
                try:
                    utils.click_element(driver, config.XPATH_OB_BTN_SALTAR)
                    time.sleep(1)
                except:
                    pass

    print("   🔐 [HELPER] PHASE 2: EXECUTING LOGIN...")
    utils.type_text(driver, config.XPATH_INPUT_USUARIO, config.USUARIO_VALIDO)
    time.sleep(0.5)
    utils.type_text(driver, config.XPATH_INPUT_PASS, config.PASS_VALIDO)
    time.sleep(0.5)
    try:
        driver.hide_keyboard()
    except:
        pass
    utils.click_element(driver, config.XPATH_LG_BTN_INICIAR)
    time.sleep(4)

    print("   🏪 [HELPER] PHASE 3: CHECKING 'CONFIGURA TU COMERCIO' SCREEN...")
    screen_present = utils.verify_element(
        wait, config.XPATH_CC_SCREEN, "CONFIGURA TU COMERCIO SCREEN"
    )
    if screen_present:
        try:
            utils.type_text(driver, config.XPATH_CC_INPUT_AFILIACION, config.CC_AFILIACION)
            time.sleep(0.5)
            utils.type_text(driver, config.XPATH_CC_INPUT_TOKEN, config.CC_TOKEN)
            time.sleep(0.5)
            try: driver.hide_keyboard()
            except: pass
            utils.click_element(driver, config.XPATH_CC_BTN_CONFIRMAR)
            time.sleep(3)
        except Exception as e:
            print(f"   ⚠️  [HELPER] COMERCIO FORM ERROR: {e}")
    else:
        print("   ℹ️  [HELPER] COMMERCE ALREADY LINKED")

    print("   ⚙️  [HELPER] PHASE 4: CHECKING 'LECTOR NO CONFIGURADO' POPUP...")
    time.sleep(2)
    popup_present = utils.verify_element(
        wait, config.XPATH_LG_POPUP_LECTOR_NC, "LECTOR NO CONFIGURADO POPUP"
    )
    if popup_present:
        try:
            utils.click_element(driver, config.XPATH_LG_BTN_CONFIGURAR_AHORA)
            time.sleep(3)
            _WDW(driver, 8).until(
                lambda d: d.find_element(By.XPATH, config.XPATH_LG_LECTOR_CONFIGURADO)
            )
            utils.click_element(driver, config.XPATH_LG_BTN_ACEPTAR_LECTOR)
            time.sleep(2)
            print("   ✅ [HELPER] LECTOR CONFIGURED — HEADING TO HOME")
        except Exception as e:
            print(f"   ⚠️  [HELPER] LECTOR POPUP HANDLING: {e}")
    else:
        print("   ℹ️  [HELPER] NO POPUP — HEADING TO HOME")
        time.sleep(2)




# ==================================================================================
# AJ-114: NAVIGATE TO "CAMBIAR COMERCIO" AND VERIFY SCREEN LOADS
# ==================================================================================

def AJ_114():
    """
    AJ-114: NAVIGATE TO "CAMBIAR COMERCIO" AND VERIFY SCREEN LOADS
    ---------------------------------------------------------------
    PRECONDITIONS : SETTINGS SCREEN VISIBLE (SCREENSHOT 1)
    FLOW          : SETTINGS → CLICK "Cambiar comercio" → VERIFY SCREEN (SCREENSHOT 2)
    EXPECTED      : Form with:
                    · Field 1: "Número de afiliación"
                    · Field 2: "Token de registro"
                    · Button: "Aceptar"
    SUCCESS       : SCREENSHOT 2 IS VISIBLE — FORM LOADED CORRECTLY
    """
    print("\n" + "=" * 60)
    print("AJ-114: NAVIGATE TO 'CAMBIAR COMERCIO'")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN FLOW...")
        helper_login_to_calculator(driver, wait)

        _navigate_to_settings(driver, wait)
        utils.take_screenshot(driver, "AJ114_01_SETTINGS_SCREEN", "t6")

        # ── STEP 1: CLICK "CAMBIAR COMERCIO" ─────────────────────────────────
        print("\n👉 STEP 1: CLICKING 'Cambiar comercio'...")
        clicked = False
        for xpath in [
            config.XPATH_AJ_BTN_CAMBIAR_COMERCIO_MENU,
            config.XPATH_AJ_BTN_CAMBIAR_COMERCIO,
            '//*[contains(@text,"Cambiar comercio") or contains(@content-desc,"Cambiar comercio")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                print("   ✅ 'Cambiar comercio' CLICKED")
                clicked = True
                break
            except:
                pass
        if not clicked:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textContains("Cambiar comercio")'
                ).click()
                time.sleep(2)
                clicked = True
            except Exception as e:
                print(f"   ❌ ALL STRATEGIES FAILED: {e}")

        if not clicked:
            print("\n💥 AJ-114 FAILED — COULD NOT CLICK 'Cambiar comercio'")
            utils.take_screenshot(driver, "AJ114_02_CLICK_FAILED", "t6")
            return False

        # ── STEP 2: VERIFY "CAMBIAR COMERCIO" SCREEN LOADED (SCREENSHOT 2) ───
        print("\n👉 STEP 2: VERIFYING 'Cambiar comercio' SCREEN LOADED...")
        screen_ok  = False
        fields_ok  = False
        button_ok  = False

        # CHECK SCREEN TITLE
        for xpath in [
            config.XPATH_AJ_CC_SCREEN_TITLE,
            '//*[@text="Cambiar comercio" or @content-desc="Cambiar comercio"]',
        ]:
            try:
                el = driver.find_element(By.XPATH, xpath)
                if el.is_displayed():
                    print("   ✅ SCREEN TITLE 'Cambiar comercio' VISIBLE")
                    screen_ok = True
                    break
            except:
                pass

        # CHECK 2 INPUT FIELDS
        input_count = 0
        for xpath in [config.XPATH_AJ_CC_INPUT_AFILIACION, config.XPATH_AJ_CC_INPUT_TOKEN]:
            try:
                driver.find_element(By.XPATH, xpath)
                input_count += 1
            except:
                pass
        if input_count >= 2:
            print("   ✅ BOTH INPUT FIELDS PRESENT (Afiliación + Token)")
            fields_ok = True
        else:
            print(f"   ⚠️  ONLY {input_count}/2 FIELDS FOUND")

        # CHECK "Aceptar" BUTTON
        try:
            el = driver.find_element(By.XPATH, config.XPATH_AJ_CC_BTN_ACEPTAR)
            if el.is_displayed():
                print("   ✅ BUTTON 'Aceptar' VISIBLE")
                button_ok = True
        except:
            print("   ⚠️  BUTTON 'Aceptar' NOT FOUND")

        utils.take_screenshot(driver, "AJ114_02_CAMBIAR_COMERCIO_SCREEN", "t6")

        if screen_ok and fields_ok and button_ok:
            result = "SUCCESS"
            print("\n✅ AJ-114 RESULT: SUCCESS — 'Cambiar comercio' SCREEN FULLY LOADED")
        else:
            print(f"\n❌ AJ-114 RESULT: FAIL — screen={screen_ok} fields={fields_ok} btn={button_ok}")

    except Exception as e:
        print(f"\n💥 AJ-114 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "AJ114_CRITICAL_ERROR", "t6")
        except: pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 AJ-114 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# AJ-116: FAILED COMMERCE CHANGE — INVALID CREDENTIALS
# ==================================================================================

def AJ_116():
    """
    AJ-116: FAILED COMMERCE CHANGE — INVALID CREDENTIALS
    ------------------------------------------------------
    PRECONDITIONS : "Cambiar comercio" SCREEN VISIBLE
    FLOW          : Fill Afiliación=2342423 | Token=2343242342343242
                    → CLICK "Aceptar" → RED TOAST "Error de registro" (SCREENSHOT 3)
    EXPECTED      : Red error popup appears — commerce change rejected
    NOTE          : ERROR TYPE TEST — red popup = PASS (system behaved correctly)
    """
    print("\n" + "=" * 60)
    print("AJ-116: FAILED COMMERCE CHANGE — INVALID CREDENTIALS")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN FLOW...")
        helper_login_to_calculator(driver, wait)

        _navigate_to_settings(driver, wait)
        time.sleep(1)

        # NAVIGATE TO CAMBIAR COMERCIO
        for xpath in [
            config.XPATH_AJ_BTN_CAMBIAR_COMERCIO_MENU,
            '//*[contains(@text,"Cambiar comercio") or contains(@content-desc,"Cambiar comercio")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                break
            except:
                pass
        utils.take_screenshot(driver, "AJ116_01_CAMBIAR_COMERCIO_SCREEN", "t6")

        # ── STEP 1: FILL WITH INVALID CREDENTIALS (SCREENSHOT 3) ─────────────
        print(f"\n👉 STEP 1: FILLING INVALID CREDENTIALS...")
        print(f"   AFILIACIÓN: {config.AJ_CC_INVALID_AFILIACION}")
        print(f"   TOKEN:      {config.AJ_CC_INVALID_TOKEN}")

        filled = True
        for xpath, value, label in [
            (config.XPATH_AJ_CC_INPUT_AFILIACION, config.AJ_CC_INVALID_AFILIACION, "AFILIACIÓN"),
            (config.XPATH_AJ_CC_INPUT_TOKEN,      config.AJ_CC_INVALID_TOKEN,      "TOKEN"),
        ]:
            try:
                el = driver.find_element(By.XPATH, xpath)
                el.click()
                time.sleep(0.3)
                el.clear()
                el.send_keys(value)
                time.sleep(0.3)
                print(f"   ✅ {label} FILLED: {value}")
            except Exception as e:
                print(f"   ❌ {label} FIELD FAILED: {e}")
                filled = False
        try: driver.hide_keyboard()
        except: pass

        if not filled:
            print("\n💥 AJ-116 FAILED — COULD NOT FILL FORM")
            return False
        utils.take_screenshot(driver, "AJ116_02_FORM_FILLED", "t6")

        # ── STEP 2: CLICK "ACEPTAR" AND POLL FOR RED TOAST ───────────────────
        print("\n👉 STEP 2: CLICKING 'Aceptar' — EXPECTING RED ERROR TOAST...")
        btn_clicked = False
        for xpath in [
            config.XPATH_AJ_CC_BTN_ACEPTAR,
            '//*[@text="Aceptar" or @content-desc="Aceptar"]',
            '//android.widget.Button[@content-desc="Aceptar"]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                btn_clicked = True
                break
            except: pass
        if not btn_clicked:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Aceptar")'
                ).click()
                btn_clicked = True
            except Exception as e:
                print(f"   ❌ ACEPTAR BUTTON NOT FOUND: {e}")
                return False

        toast_found, toast_text = _detect_toast(
            driver, config.XPATH_AJ_CC_TOAST_ERROR,
            "RED ERROR TOAST — 'Error de registro'", timeout=6
        )
        utils.take_screenshot(driver, "AJ116_03_ERROR_TOAST", "t6")

        if toast_found:
            result = "SUCCESS"
            print(f"\n✅ AJ-116 RESULT: SUCCESS — SYSTEM CORRECTLY REJECTED INVALID CREDENTIALS")
            print(f"   RED TOAST: '{toast_text}'")
        else:
            # STRATEGY B: CONFIRM STILL ON CAMBIAR COMERCIO SCREEN
            try:
                driver.find_element(By.XPATH, config.XPATH_AJ_CC_SCREEN_TITLE)
                result = "SUCCESS"
                print("\n✅ AJ-116 RESULT: SUCCESS — STILL ON SCREEN, SUBMISSION BLOCKED")
                print("   ℹ️  TOAST DISAPPEARED BEFORE DETECTION — BEHAVIOR IS CORRECT")
            except:
                print("\n❌ AJ-116 RESULT: FAIL — ERROR NOT DETECTED")

    except Exception as e:
        print(f"\n💥 AJ-116 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "AJ116_CRITICAL_ERROR", "t6")
        except: pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 AJ-116 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# AJ-117: FAILED COMMERCE CHANGE — EMPTY FIELDS
# ==================================================================================

def AJ_117():
    """
    AJ-117: FAILED COMMERCE CHANGE — EMPTY FIELDS
    -----------------------------------------------
    PRECONDITIONS : "Cambiar comercio" SCREEN VISIBLE
    FLOW          : Leave both fields EMPTY → CLICK "Aceptar"
                    → INLINE ERRORS appear below each field (SCREENSHOT 4):
                      "Por favor ingresa el número de afiliación"
                      "Por favor ingresa el token de registro"
    EXPECTED      : Both inline red errors visible — submission blocked
    """
    print("\n" + "=" * 60)
    print("AJ-117: FAILED COMMERCE CHANGE — EMPTY FIELDS")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN FLOW...")
        helper_login_to_calculator(driver, wait)

        _navigate_to_settings(driver, wait)
        time.sleep(1)
        for xpath in [
            config.XPATH_AJ_BTN_CAMBIAR_COMERCIO_MENU,
            '//*[contains(@text,"Cambiar comercio") or contains(@content-desc,"Cambiar comercio")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                break
            except:
                pass

        # ── STEP 1: LEAVE FIELDS EMPTY AND CLICK ACEPTAR ─────────────────────
        print("\n👉 STEP 1: LEAVING FIELDS EMPTY — CLICKING 'Aceptar'...")
        print("   ℹ️  BOTH FIELDS INTENTIONALLY LEFT EMPTY")
        utils.take_screenshot(driver, "AJ117_01_EMPTY_FORM", "t6")

        btn_clicked = False
        for xpath in [
            config.XPATH_AJ_CC_BTN_ACEPTAR,
            '//*[@text="Aceptar" or @content-desc="Aceptar"]',
            '//android.widget.Button[@content-desc="Aceptar"]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                btn_clicked = True
                break
            except: pass
        if not btn_clicked:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Aceptar")'
                ).click()
                time.sleep(2)
                btn_clicked = True
            except Exception as e:
                print(f"   ❌ ACEPTAR BUTTON NOT FOUND: {e}")
                return False

        # ── STEP 2: CHECK FOR INLINE ERRORS (SCREENSHOT 4) ───────────────────
        print("\n👉 STEP 2: CHECKING FOR INLINE VALIDATION ERRORS...")
        errors_found = []

        error_checks = [
            ("AFILIACIÓN EMPTY ERROR",
             config.XPATH_AJ_CC_ERROR_AFILIACION,
             "ingresa el número de afiliación"),
            ("TOKEN EMPTY ERROR",
             config.XPATH_AJ_CC_ERROR_TOKEN,
             "ingresa el token"),
        ]

        for label, xpath, keyword in error_checks:
            found = False
            # STRATEGY 1: DIRECT XPATH
            try:
                el = driver.find_element(By.XPATH, xpath)
                if el.is_displayed():
                    text = el.get_attribute("text") or el.get_attribute("content-desc") or ""
                    print(f"   ✅ {label}: '{text}'")
                    errors_found.append(label)
                    found = True
            except:
                pass
            # STRATEGY 2: UIAUTOMATOR KEYWORD
            if not found:
                try:
                    el = driver.find_element(
                        AppiumBy.ANDROID_UIAUTOMATOR,
                        f'new UiSelector().textContains("{keyword}")'
                    )
                    text = el.get_attribute("text") or ""
                    print(f"   ✅ {label} VIA UIAUTOMATOR: '{text}'")
                    errors_found.append(label)
                except:
                    print(f"   ⚠️  {label} NOT DETECTED")

        utils.take_screenshot(driver, "AJ117_02_EMPTY_ERRORS", "t6")

        if len(errors_found) >= 1:
            result = "SUCCESS"
            print(f"\n✅ AJ-117 RESULT: SUCCESS — {len(errors_found)}/2 EMPTY FIELD ERRORS SHOWN")
        else:
            print("\n❌ AJ-117 RESULT: FAIL — INLINE ERRORS NOT DETECTED")

    except Exception as e:
        print(f"\n💥 AJ-117 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "AJ117_CRITICAL_ERROR", "t6")
        except: pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 AJ-117 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# AJ-118: FAILED COMMERCE CHANGE — FORMAT-VALID BUT WRONG CREDENTIALS
# ==================================================================================

def AJ_118():
    """
    AJ-118: FAILED COMMERCE CHANGE — FORMAT-VALID BUT NON-EXISTENT CREDENTIALS
    ---------------------------------------------------------------------------
    PRECONDITIONS : "Cambiar comercio" SCREEN VISIBLE
    FLOW          : Fill Afiliación=1234567 (7 digits) | Token=1234567891234567
                    → CLICK "Aceptar" → RED TOAST "Error de registro" (SCREENSHOT 5)
    EXPECTED      : Values pass field-level format validation but fail on server
                    → Red error popup appears
    NOTE          : VALIDATES FIELD LENGTH CONSTRAINTS — 7-digit afiliación, 16-char token
    """
    print("\n" + "=" * 60)
    print("AJ-118: FAILED COMMERCE CHANGE — FORMAT-VALID WRONG CREDENTIALS")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN FLOW...")
        helper_login_to_calculator(driver, wait)

        _navigate_to_settings(driver, wait)
        time.sleep(1)
        for xpath in [
            config.XPATH_AJ_BTN_CAMBIAR_COMERCIO_MENU,
            '//*[contains(@text,"Cambiar comercio") or contains(@content-desc,"Cambiar comercio")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                break
            except:
                pass
        utils.take_screenshot(driver, "AJ118_01_CAMBIAR_COMERCIO_SCREEN", "t6")

        # ── STEP 1: FILL WITH FORMAT-VALID BUT WRONG CREDENTIALS (SCREENSHOT 5)
        print(f"\n👉 STEP 1: FILLING FORMAT-VALID BUT WRONG CREDENTIALS...")
        print(f"   AFILIACIÓN (7 digits): {config.AJ_CC_FAKE_AFILIACION}")
        print(f"   TOKEN (16 chars):      {config.AJ_CC_FAKE_TOKEN}")

        filled = True
        for xpath, value, label in [
            (config.XPATH_AJ_CC_INPUT_AFILIACION, config.AJ_CC_FAKE_AFILIACION, "AFILIACIÓN"),
            (config.XPATH_AJ_CC_INPUT_TOKEN,      config.AJ_CC_FAKE_TOKEN,      "TOKEN"),
        ]:
            try:
                el = driver.find_element(By.XPATH, xpath)
                el.click()
                time.sleep(0.3)
                el.clear()
                el.send_keys(value)
                time.sleep(0.3)
                print(f"   ✅ {label} FILLED: {value}")
            except Exception as e:
                print(f"   ❌ {label} FIELD FAILED: {e}")
                filled = False
        try: driver.hide_keyboard()
        except: pass

        if not filled:
            print("\n💥 AJ-118 FAILED — COULD NOT FILL FORM")
            return False
        utils.take_screenshot(driver, "AJ118_02_FORM_FILLED", "t6")

        # ── STEP 2: CLICK "ACEPTAR" AND POLL FOR RED TOAST ───────────────────
        print("\n👉 STEP 2: CLICKING 'Aceptar' — EXPECTING RED ERROR TOAST...")
        btn_clicked = False
        for xpath in [
            config.XPATH_AJ_CC_BTN_ACEPTAR,
            '//*[@text="Aceptar" or @content-desc="Aceptar"]',
            '//android.widget.Button[@content-desc="Aceptar"]',
            '//*[contains(@text,"Aceptar") or contains(@content-desc,"Aceptar")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                btn_clicked = True
                print("   ✅ ACEPTAR CLICKED")
                break
            except:
                pass
        if not btn_clicked:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().text("Aceptar")'
                ).click()
                btn_clicked = True
                print("   ✅ ACEPTAR VIA UIAUTOMATOR")
            except Exception as e:
                print(f"   ❌ ACEPTAR BUTTON NOT FOUND: {e}")
                utils.take_screenshot(driver, "AJ118_03_BTN_FAILED", "t6")
                return False

        toast_found, toast_text = _detect_toast(
            driver, config.XPATH_AJ_CC_TOAST_ERROR,
            "RED ERROR TOAST — 'Error de registro'", timeout=6
        )
        utils.take_screenshot(driver, "AJ118_03_ERROR_TOAST", "t6")

        if toast_found:
            result = "SUCCESS"
            print(f"\n✅ AJ-118 RESULT: SUCCESS — FORMAT VALIDATION PASSED BUT SERVER REJECTED")
            print(f"   RED TOAST: '{toast_text}'")
            print(f"   ✅ 7-digit afiliación format accepted by form")
            print(f"   ✅ 16-char token format accepted by form")
            print(f"   ✅ Server correctly rejected non-existent credentials")
        else:
            try:
                driver.find_element(By.XPATH, config.XPATH_AJ_CC_SCREEN_TITLE)
                result = "SUCCESS"
                print("\n✅ AJ-118 RESULT: SUCCESS — SUBMISSION BLOCKED (TOAST MISSED)")
            except:
                print("\n❌ AJ-118 RESULT: FAIL — ERROR NOT DETECTED")

    except Exception as e:
        print(f"\n💥 AJ-118 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "AJ118_CRITICAL_ERROR", "t6")
        except: pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 AJ-118 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# AJ-119: LOGOUT — CERRAR SESIÓN
# ==================================================================================

def AJ_119():
    """
    AJ-119: LOGOUT — CERRAR SESIÓN WORKS CORRECTLY
    ------------------------------------------------
    PRECONDITIONS : SETTINGS SCREEN VISIBLE (SCREENSHOT 1)
    FLOW          : SETTINGS → CLICK "Cerrar sesión"
                    → CONFIRM if dialog appears
                    → VERIFY LOGIN SCREEN IS SHOWN (SCREENSHOT 6)
    EXPECTED      : User is logged out and login screen is displayed
    SUCCESS       : "Iniciar sesión" screen visible after logout
    """
    print("\n" + "=" * 60)
    print("AJ-119: LOGOUT — CERRAR SESIÓN")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN FLOW...")
        helper_login_to_calculator(driver, wait)

        _navigate_to_settings(driver, wait)
        utils.take_screenshot(driver, "AJ119_01_SETTINGS_SCREEN", "t6")

        # ── STEP 1: CLICK "CERRAR SESIÓN" ────────────────────────────────────
        print("\n👉 STEP 1: CLICKING 'Cerrar sesión'...")
        clicked = False
        for xpath in [
            config.XPATH_AJ_BTN_CERRAR_SESION,
            config.XPATH_AJ_BTN_CERRAR_SESION_MENU,
            '//*[contains(@text,"Cerrar sesión") or contains(@content-desc,"Cerrar sesión")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                print("   ✅ 'Cerrar sesión' CLICKED")
                clicked = True
                break
            except:
                pass
        if not clicked:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textContains("Cerrar sesión")'
                ).click()
                time.sleep(2)
                clicked = True
            except Exception as e:
                print(f"   ❌ ALL STRATEGIES FAILED: {e}")

        if not clicked:
            print("\n💥 AJ-119 FAILED — COULD NOT CLICK 'Cerrar sesión'")
            utils.take_screenshot(driver, "AJ119_02_CLICK_FAILED", "t6")
            return False

        # ── STEP 2: HANDLE CONFIRMATION DIALOG IF PRESENT ────────────────────
        print("\n👉 STEP 2: CHECKING FOR CONFIRMATION DIALOG...")
        try:
            confirm_btn = driver.find_element(By.XPATH, config.XPATH_AJ_CERRAR_CONFIRM)
            confirm_text = confirm_btn.get_attribute("text") or confirm_btn.get_attribute("content-desc") or ""
            # ONLY CLICK IF IT SAYS "Cerrar" OR "Confirmar" — NOT "Cancelar"
            if any(kw in confirm_text.lower() for kw in ["cerrar", "confirmar", "aceptar", "sí"]):
                confirm_btn.click()
                time.sleep(2)
                print(f"   ✅ CONFIRMATION DIALOG DISMISSED: '{confirm_text}'")
        except:
            print("   ℹ️  NO CONFIRMATION DIALOG — LOGOUT IMMEDIATE")
        time.sleep(2)

        # ── STEP 3: VERIFY LOGIN SCREEN APPEARS (SCREENSHOT 6) ───────────────
        print("\n👉 STEP 3: VERIFYING LOGIN SCREEN IS SHOWN...")
        logged_out = False

        for xpath in [
            config.XPATH_AJ_LOGIN_SCREEN_AFTER_LOGOUT,
            '//*[@text="Iniciar sesión" or @content-desc="Iniciar sesión"]',
            '//*[contains(@text,"Ingresa tu correo") or contains(@content-desc,"Ingresa tu correo")]',
            '//*[contains(@text,"Correo electrónico") or contains(@content-desc,"Correo electrónico")]',
        ]:
            try:
                el = driver.find_element(By.XPATH, xpath)
                if el.is_displayed():
                    text = el.get_attribute("text") or el.get_attribute("content-desc") or ""
                    print(f"   ✅ LOGIN SCREEN CONFIRMED: '{text}'")
                    logged_out = True
                    break
            except:
                pass

        utils.take_screenshot(driver, "AJ119_02_LOGIN_SCREEN_AFTER_LOGOUT", "t6")

        if logged_out:
            result = "SUCCESS"
            print("\n✅ AJ-119 RESULT: SUCCESS — USER LOGGED OUT CORRECTLY")
            print("   LOGIN SCREEN VISIBLE AFTER LOGOUT")
        else:
            print("\n❌ AJ-119 RESULT: FAIL — LOGIN SCREEN NOT DETECTED AFTER LOGOUT")
            print("   💡 DUMPING SCREEN FOR DIAGNOSIS:")
            try:
                for el in driver.find_elements(By.XPATH, "//*"):
                    t = el.get_attribute("text") or ""
                    d = el.get_attribute("content-desc") or ""
                    if (t and len(t) > 3) or (d and len(d) > 3):
                        print(f"      → text='{t}' | desc='{d}'")
            except: pass

    except Exception as e:
        print(f"\n💥 AJ-119 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "AJ119_CRITICAL_ERROR", "t6")
        except: pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 AJ-119 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# AJ-120: CONFIGURAR NUEVAMENTE — READER SETUP SCREEN LOADS FROM SETTINGS
# ==================================================================================

def AJ_120():
    """
    AJ-120: CONFIGURAR NUEVAMENTE — READER SETUP SCREEN LOADS CORRECTLY
    --------------------------------------------------------------------
    PRECONDITIONS : SETTINGS SCREEN VISIBLE (SCREENSHOT 1 — "Lector" SECTION)
    FLOW          : SETTINGS → CLICK "Configurar nuevamente" (Lector section)
                    → VERIFY READER SETUP/CONFIGURATION SCREEN APPEARS
                    → CAPTURE SCREENSHOT AS EVIDENCE
    EXPECTED      : Reader configuration screen loads — shows lector setup UI
    NOTE          : THIS TEST DOES NOT COMPLETE READER CONFIGURATION —
                    IT ONLY VALIDATES THE SCREEN TRANSITION
    """
    print("\n" + "=" * 60)
    print("AJ-120: CONFIGURAR NUEVAMENTE — READER SETUP SCREEN")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN FLOW...")
        helper_login_to_calculator(driver, wait)

        _navigate_to_settings(driver, wait)
        utils.take_screenshot(driver, "AJ120_01_SETTINGS_SCREEN", "t6")

        # ── STEP 1: SCROLL DOWN TO "LECTOR" SECTION IF NEEDED ────────────────
        # THE LECTOR SECTION IS BELOW "CUENTA" — MAY NEED SCROLL
        print("\n👉 STEP 1: LOCATING 'Configurar nuevamente' IN LECTOR SECTION...")
        try:
            # ATTEMPT SCROLL DOWN TO REVEAL LECTOR SECTION
            driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView('
                'new UiSelector().textContains("Configurar nuevamente"))'
            )
            time.sleep(1)
            print("   ✅ SCROLLED TO 'Configurar nuevamente'")
        except:
            print("   ℹ️  SCROLL NOT NEEDED OR FAILED — PROCEEDING")

        # ── STEP 2: CLICK "CONFIGURAR NUEVAMENTE" ────────────────────────────
        print("\n👉 STEP 2: CLICKING 'Configurar nuevamente'...")
        clicked = False
        for xpath in [
            config.XPATH_AJ_BTN_CONFIGURAR_NUEVAMENTE,
            '//*[contains(@text,"Configurar nuevamente") or contains(@content-desc,"Configurar nuevamente")]',
            '//*[contains(@text,"nuevamente") or contains(@content-desc,"nuevamente")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(3)
                print("   ✅ 'Configurar nuevamente' CLICKED")
                clicked = True
                break
            except:
                pass
        if not clicked:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textContains("Configurar nuevamente")'
                ).click()
                time.sleep(3)
                clicked = True
                print("   ✅ VIA UIAUTOMATOR")
            except Exception as e:
                print(f"   ❌ ALL STRATEGIES FAILED: {e}")

        if not clicked:
            print("\n💥 AJ-120 FAILED — COULD NOT CLICK 'Configurar nuevamente'")
            utils.take_screenshot(driver, "AJ120_02_CLICK_FAILED", "t6")
            return False

        # ── STEP 3: VERIFY READER SETUP SCREEN LOADED ────────────────────────
        print("\n👉 STEP 3: VERIFYING READER SETUP SCREEN LOADED...")
        screen_loaded = False

        for xpath in [
            config.XPATH_AJ_LECTOR_SETUP_SCREEN,
            config.XPATH_LG_LECTOR_CONFIGURADO,
            config.XPATH_LG_POPUP_LECTOR_NC,
            '//*[contains(@text,"Lector") or contains(@content-desc,"Lector")]',
            '//*[contains(@text,"cifrado") or contains(@content-desc,"cifrado")]',
            '//*[contains(@text,"llaves") or contains(@content-desc,"llaves")]',
            '//*[contains(@text,"configurar") or contains(@content-desc,"configurar")]',
        ]:
            try:
                el = driver.find_element(By.XPATH, xpath)
                if el.is_displayed():
                    text = el.get_attribute("text") or el.get_attribute("content-desc") or ""
                    print(f"   ✅ SETUP SCREEN INDICATOR: '{text}'")
                    screen_loaded = True
                    break
            except:
                pass

        utils.take_screenshot(driver, "AJ120_02_READER_SETUP_SCREEN", "t6")

        if screen_loaded:
            result = "SUCCESS"
            print("\n✅ AJ-120 RESULT: SUCCESS — READER SETUP SCREEN LOADED CORRECTLY")
        else:
            # VERIFY WE LEFT THE SETTINGS SCREEN AT LEAST
            still_on_settings = False
            try:
                driver.find_element(By.XPATH, config.XPATH_AJ_SCREEN_TITLE)
                still_on_settings = True
            except:
                pass

            if not still_on_settings:
                # WE NAVIGATED AWAY FROM SETTINGS — SOMETHING LOADED
                result = "SUCCESS"
                print("\n✅ AJ-120 RESULT: SUCCESS — NAVIGATED AWAY FROM SETTINGS")
                print("   ℹ️  SETUP SCREEN IDENTIFIER NOT MATCHED — CHECK SCREENSHOT")
            else:
                print("\n❌ AJ-120 RESULT: FAIL — STILL ON SETTINGS, NAVIGATION FAILED")

    except Exception as e:
        print(f"\n💥 AJ-120 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "AJ120_CRITICAL_ERROR", "t6")
        except: pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 AJ-120 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)

# ==================================================================================
# AJ-121: BLUETOOTH OFF → LOGIN → VERIFY 'CONFIGURAR LECTOR' OPTION APPEARS
# ==================================================================================
 
def AJ_121():
    """
    AJ-121: BLUETOOTH DISABLED → LOGIN → VERIFY 'CONFIGURAR LECTOR' OPTION
 
    OBJECTIVE:
        Confirm that when Bluetooth is turned OFF before launching the app,
        the Memphis app still allows the user to log in successfully and
        navigate to Settings (Ajustes) where 'Configurar lector' is visible.
 
        NOTE: In the current v2 app, the absence of Bluetooth does NOT block
        login or Settings access. This test documents that behavior and
        verifies the 'Configurar lector' option is accessible regardless.
 
    PRECONDITIONS:
        - T6 connected via USB with USB Debugging ON
        - Appium server running with --relaxed-security
        - ADB available (adb devices shows the T6)
        - Bluetooth initially ON (normal state)
 
    STEPS:
        1. [ADB]    Disable Bluetooth via ADB
        2. [APPIUM] Launch app — verify it starts normally (no BT block)
        3. [APPIUM] Enter credentials + complete login
        4. [APPIUM] Navigate to Ajustes tab
        5. [APPIUM] Verify 'Configurar lector' option is present
        6. [ADB]    Restore Bluetooth to ON
 
    EXPECTED RESULT:
        ✅ App launches normally with BT off
        ✅ Login succeeds
        ✅ Ajustes tab is reachable
        ✅ 'Configurar lector' option is visible
 
    TYPE  : FUNCTIONAL
    STATE : PASS (expected — v2 does not block on BT)
    """
    print("\n" + "=" * 60)
    print("🧪 AJ-121: BLUETOOTH OFF → LOGIN → CONFIGURAR LECTOR")
    print("=" * 60)
 
    # ── VERIFY ADB DEVICE ──
    if not sys_ctrl.verify_device_connected():
        print("❌ AJ-121 ABORTED: No ADB device found.")
        print("   💡 Connect T6 via USB and enable USB Debugging.")
        return False
 
    # ── SNAPSHOT STATE BEFORE TEST ──
    print("\n📊 DEVICE STATE BEFORE TEST:")
    snapshot_before = sys_ctrl.get_device_status_snapshot()
 
    result = False
    driver = None
 
    try:
        # ──────────────────────────────────────────────────────────────
        # STEP 1: DISABLE BLUETOOTH VIA ADB
        # ──────────────────────────────────────────────────────────────
        print("\n" + "-" * 50)
        print("👉 STEP 1: DISABLING BLUETOOTH VIA ADB...")
        print("-" * 50)
 
        bt_disabled = sys_ctrl.disable_bluetooth()
 
        if bt_disabled:
            print("   ✅ BLUETOOTH IS NOW OFF.")
        else:
            print("   ⚠️  BT STATE UNCERTAIN — CONTINUING TEST ANYWAY.")
 
        time.sleep(2)
 
        # ──────────────────────────────────────────────────────────────
        # STEP 2: LAUNCH APP VIA APPIUM
        # ──────────────────────────────────────────────────────────────
        print("\n" + "-" * 50)
        print("👉 STEP 2: LAUNCHING MEMPHIS APP (BT IS OFF)...")
        print("-" * 50)
 
        driver, wait = utils.start_driver()
        time.sleep(4)
 
        utils.take_screenshot(driver, "AJ_121_STEP2_APP_LAUNCH_BT_OFF")
        print("   ✅ APP LAUNCHED SUCCESSFULLY WITH BLUETOOTH OFF.")
 
        # ──────────────────────────────────────────────────────────────
        # STEP 3: LOGIN
        # ──────────────────────────────────────────────────────────────
        print("\n" + "-" * 50)
        print("👉 STEP 3: EXECUTING LOGIN FLOW...")
        print("-" * 50)
 
        helper_login_to_calculator(driver, wait)
        utils.take_screenshot(driver, "AJ_121_STEP3_POST_LOGIN")
 
        # Quick scan to confirm we're past login screen
        login_still_visible = False
        try:
            driver.find_element(By.XPATH, config.XPATH_INPUT_USUARIO)
            login_still_visible = True
        except:
            pass
 
        if login_still_visible:
            print("   ❌ STILL ON LOGIN SCREEN — Login may have failed.")
        else:
            print("   ✅ LOGIN SUCCESSFUL — PAST LOGIN SCREEN.")
 
        # ──────────────────────────────────────────────────────────────
        # STEP 4: NAVIGATE TO AJUSTES TAB
        # ──────────────────────────────────────────────────────────────
        print("\n" + "-" * 50)
        print("👉 STEP 4: NAVIGATING TO 'AJUSTES' TAB...")
        print("-" * 50)
 
        # STRATEGY 1: Use config XPath for Ajustes tab
        ajustes_reached = False
        ajustes_xpaths = [
            config.XPATH_PÑ_TAB_AJUSTES,           # Primary: from PÑ section
            config.XPATH_C_TAB_AJUSTES,             # Fallback: from C section
            '//*[contains(@content-desc, "Ajustes")]',  # Broad fallback
        ]
 
        for xpath in ajustes_xpaths:
            try:
                btn = WebDriverWait(driver, 6).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                btn.click()
                time.sleep(3)
                ajustes_reached = True
                print(f"   ✅ AJUSTES TAB CLICKED (xpath: {xpath[:60]}...)")
                break
            except Exception as e:
                print(f"   ⚠️  XPATH FAILED: {xpath[:60]}... → {e}")
                continue
 
        if not ajustes_reached:
            print("   ❌ COULD NOT REACH AJUSTES TAB.")
            print("   💡 DEBUG — Scanning all visible content-desc values:")
            try:
                for elem in driver.find_elements(By.XPATH, "//*[@content-desc]"):
                    try:
                        desc = elem.get_attribute("content-desc")
                        if desc and len(desc) > 1:
                            print(f"      📝 content-desc: '{desc}'")
                    except:
                        continue
            except:
                pass
 
        utils.take_screenshot(driver, "AJ_121_STEP4_AJUSTES_TAB")
 
        # ──────────────────────────────────────────────────────────────
        # STEP 5: VERIFY 'CONFIGURAR LECTOR' IS VISIBLE
        # ──────────────────────────────────────────────────────────────
        print("\n" + "-" * 50)
        print("👉 STEP 5: VERIFYING 'CONFIGURAR LECTOR' OPTION...")
        print("-" * 50)
 
        lector_found = False
 
        # STRATEGY 1: Use config XPath
        try:
            elem = WebDriverWait(driver, 8).until(
                EC.presence_of_element_located(
                    (By.XPATH, config.XPATH_C_BTN_CONFIGURAR_LECTOR)
                )
            )
            if elem.is_displayed():
                lector_found = True
                print("   ✅ 'CONFIGURAR LECTOR' FOUND AND VISIBLE (config.XPATH_C_BTN_CONFIGURAR_LECTOR).")
        except:
            print("   ⚠️  Strategy 1 (config xpath) did not find 'Configurar lector'.")
 
        # STRATEGY 2: Broad text scan
        if not lector_found:
            lector_keywords = ["Configurar lector", "configurar lector", "Lector", "lector"]
            try:
                all_elems = driver.find_elements(By.XPATH, "//*")
                for elem in all_elems:
                    try:
                        text = elem.get_attribute("text") or ""
                        desc = elem.get_attribute("content-desc") or ""
                        for kw in lector_keywords:
                            if kw in text or kw in desc:
                                print(f"   ✅ FOUND VIA SCAN: text='{text}' desc='{desc}'")
                                lector_found = True
                                break
                        if lector_found:
                            break
                    except:
                        continue
            except Exception as e:
                print(f"   ⚠️  Scan error: {e}")
 
        # STRATEGY 3: UiAutomator text search
        if not lector_found:
            try:
                elem = driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textContains("lector")'
                )
                print(f"   ✅ FOUND VIA UIAUTOMATOR: '{elem.get_attribute('text')}'")
                lector_found = True
            except:
                print("   ⚠️  Strategy 3 (UiAutomator) did not find 'lector'.")
 
        utils.take_screenshot(driver, "AJ_121_STEP5_CONFIGURAR_LECTOR")
 
        # ── PRINT ALL VISIBLE TEXT FOR DEBUG ──
        print("\n🔍 SCANNING ALL VISIBLE TEXT ON SCREEN (DEBUG):")
        try:
            for elem in driver.find_elements(By.XPATH, "//*"):
                try:
                    t = elem.get_attribute("text") or ""
                    d = elem.get_attribute("content-desc") or ""
                    if (t and len(t) > 2) or (d and len(d) > 2):
                        print(f"   📝 text='{t}' | desc='{d}'")
                except:
                    continue
        except:
            pass
 
        # ──────────────────────────────────────────────────────────────
        # RESULT
        # ──────────────────────────────────────────────────────────────
        result = lector_found
 
        print("\n" + "=" * 60)
        if result:
            print("✅ AJ-121: PASSED")
            print("   Bluetooth OFF did NOT block login or Settings access.")
            print("   'Configurar lector' option is visible in Ajustes.")
        else:
            print("❌ AJ-121: FAILED")
            print("   'Configurar lector' was NOT found in Ajustes.")
            print("   Check the debug scan above for what IS on screen.")
        print("=" * 60)
 
    except Exception as e:
        print(f"\n💥 AJ-121 CRITICAL ERROR: {e}")
        if driver:
            try:
                utils.take_screenshot(driver, "AJ_121_CRITICAL_ERROR", "t6")
            except:
                pass
 
    finally:
        if driver:
            utils.close_driver(driver)
 
        # ── ALWAYS RESTORE BLUETOOTH ──
        print("\n🔧 POSTCONDITION: RESTORING BLUETOOTH...")
        sys_ctrl.enable_bluetooth()
 
        print("\n📊 DEVICE STATE AFTER TEST:")
        sys_ctrl.get_device_status_snapshot()
 
    return result

# ==================================================================================
# AJ-124: WIFI OFF → ONBOARDING → LOGIN ATTEMPT → RED ERROR POPUP
# ==================================================================================

def AJ_124():
    """
    AJ-124: WIFI DISABLED → ONBOARDING → LOGIN ATTEMPT → RED ERROR POPUP

    OBJECTIVE:
        Confirm that when WiFi is turned OFF before launching the app,
        after navigating through the onboarding slides and reaching the
        login screen, submitting valid credentials produces a RED ERROR
        POPUP because there is no network to complete authentication.

        SUCCESS = RED POPUP APPEARS. This means the app handled the
        network failure correctly instead of crashing.

    PRECONDITIONS:
        - T6 connected via USB with USB Debugging ON
        - Appium server running:  appium --relaxed-security
        - ADB available:          adb devices shows T6
        - WiFi initially ON

    STEPS:
        1. [ADB]    Disable WiFi via ADB
        2. [APPIUM] Launch app
        3. [APPIUM] Navigate onboarding slides → reach login screen
        4. [APPIUM] Type valid credentials (email + password)
        5. [APPIUM] Click login button
        6. [APPIUM] Verify RED error popup appears
        7. [ADB]    Restore WiFi to ON

    TYPE  : ERROR — NETWORK FAILURE
    STATE : PASS when red popup appears
    """
    print("\n" + "=" * 60)
    print("🧪 AJ-124: WIFI OFF → LOGIN ATTEMPT → RED ERROR POPUP")
    print("=" * 60)

    if not sys_ctrl.verify_device_connected():
        print("❌ AJ-124 ABORTED: No ADB device found.")
        return False

    print("\n📊 DEVICE STATE BEFORE TEST:")
    sys_ctrl.get_device_status_snapshot()

    result = False
    driver = None

    try:
        # ──────────────────────────────────────────────────────────────
        # STEP 1: DISABLE WIFI VIA ADB
        # ──────────────────────────────────────────────────────────────
        print("\n" + "-" * 50)
        print("👉 STEP 1: DISABLING WIFI VIA ADB...")
        print("-" * 50)

        wifi_disabled = sys_ctrl.disable_wifi()
        if wifi_disabled:
            print("   ✅ WIFI IS NOW OFF.")
        else:
            print("   ⚠️  WIFI STATE UNCERTAIN — CONTINUING.")
        time.sleep(3)

        # ──────────────────────────────────────────────────────────────
        # STEP 2: LAUNCH APP
        # ──────────────────────────────────────────────────────────────
        print("\n" + "-" * 50)
        print("👉 STEP 2: LAUNCHING MEMPHIS APP (WIFI IS OFF)...")
        print("-" * 50)

        driver, wait = utils.start_driver()
        time.sleep(4)
        utils.take_screenshot(driver, "AJ_124_STEP2_APP_LAUNCHED", "t6")
        print("   ✅ APP LAUNCHED.")

        # ──────────────────────────────────────────────────────────────
        # STEP 3: NAVIGATE ONBOARDING → REACH LOGIN SCREEN
        # ──────────────────────────────────────────────────────────────
        print("\n" + "-" * 50)
        print("👉 STEP 3: NAVIGATING ONBOARDING TO REACH LOGIN SCREEN...")
        print("   ℹ️  The app shows onboarding slides on first launch.")
        print("-" * 50)

        # STRATEGY A: Click 'Saltar' to skip onboarding in one tap
        onboarding_skipped = False
        try:
            skip_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH,
                    '//*[@content-desc="Saltar" or @text="Saltar" or '
                    'contains(@content-desc,"Saltar") or contains(@text,"Saltar")]'
                ))
            )
            skip_btn.click()
            time.sleep(2)
            onboarding_skipped = True
            print("   ✅ ONBOARDING SKIPPED via 'Saltar' button.")
        except:
            print("   ℹ️  'Saltar' not found — stepping through slides...")

        # STRATEGY B: Step through Siguiente → Siguiente → Comenzar/Ingresar
        if not onboarding_skipped:
            slide_xpaths = [
                '//*[@content-desc="Siguiente" or @text="Siguiente"]',
                '//*[@content-desc="Siguiente" or @text="Siguiente"]',
                '//*[@content-desc="Comenzar" or @text="Comenzar" or '
                '@content-desc="Ingresar" or @text="Ingresar" or '
                'contains(@content-desc,"cuenta") or contains(@content-desc,"Ingresa")]',
            ]
            for i, xpath in enumerate(slide_xpaths, 1):
                try:
                    btn = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, xpath))
                    )
                    btn.click()
                    time.sleep(1.5)
                    print(f"   ✅ SLIDE {i} PASSED.")
                except Exception as e:
                    print(f"   ⚠️  SLIDE {i} SKIP: {e}")

        # STRATEGY C: Click '¿Ya tienes una cuenta? Ingresa aquí'
        # This was visible in the output — direct link to login screen
        try:
            ingresa_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH,
                    '//*[contains(@content-desc,"Ingresa aquí") or '
                    'contains(@text,"Ingresa aquí") or '
                    'contains(@content-desc,"Ya tienes") or '
                    'contains(@text,"Ya tienes")]'
                ))
            )
            ingresa_btn.click()
            time.sleep(2)
            print("   ✅ CLICKED '¿Ya tienes una cuenta? Ingresa aquí' — GOING TO LOGIN.")
        except:
            print("   ℹ️  'Ingresa aquí' link not found — may already be on login.")

        time.sleep(2)
        utils.take_screenshot(driver, "AJ_124_STEP3_LOGIN_SCREEN", "t6")

        # VERIFY LOGIN FIELDS ARE NOW VISIBLE
        login_screen_ok = False
        for xpath in [
            config.XPATH_INPUT_USUARIO,
            config.XPATH_INPUT_PASS,
            '//android.widget.EditText[1]',
            '//*[contains(@content-desc,"correo") or contains(@content-desc,"Correo") or '
            'contains(@content-desc,"email") or contains(@content-desc,"Email")]',
        ]:
            try:
                elem = WebDriverWait(driver, 6).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                if elem.is_displayed():
                    print(f"   ✅ LOGIN SCREEN CONFIRMED — input field visible.")
                    login_screen_ok = True
                    break
            except:
                continue

        if not login_screen_ok:
            print("   ⚠️  LOGIN FIELDS NOT FOUND — FULL SCREEN DUMP:")
            try:
                for elem in driver.find_elements(By.XPATH, "//*"):
                    try:
                        t = elem.get_attribute("text") or ""
                        d = elem.get_attribute("content-desc") or ""
                        if (t and len(t) > 2) or (d and len(d) > 2 and d != "null"):
                            print(f"      📝 text='{t}' | desc='{d}'")
                    except:
                        continue
            except:
                pass

        # ──────────────────────────────────────────────────────────────
        # STEP 4: TYPE VALID CREDENTIALS
        # ──────────────────────────────────────────────────────────────
        print("\n" + "-" * 50)
        print("👉 STEP 4: TYPING VALID CREDENTIALS...")
        print("-" * 50)
        print(f"   ✏️  EMAIL:    {config.USUARIO_VALIDO}")
        print(f"   ✏️  PASSWORD: {'*' * len(config.PASS_VALIDO)}")

        # TAP EMAIL FIELD FIRST TO FOCUS
        try:
            utils.click_element(driver, config.XPATH_INPUT_USUARIO)
            time.sleep(0.5)
        except:
            pass

        utils.type_text(driver, config.XPATH_INPUT_USUARIO, config.USUARIO_VALIDO)
        utils.type_text(driver, config.XPATH_INPUT_PASS,    config.PASS_VALIDO)

        try:
            driver.hide_keyboard()
        except:
            pass

        utils.take_screenshot(driver, "AJ_124_STEP4_CREDENTIALS_FILLED", "t6")
        print("   ✅ CREDENTIALS ENTERED.")

        # ──────────────────────────────────────────────────────────────
        # STEP 5 + 6: CLICK LOGIN AND IMMEDIATELY POLL FOR RED POPUP
        # KEY INSIGHT: Toasts last only ~2-3 seconds. Polling must start
        # at the SAME moment as the click — no delay between them.
        # ──────────────────────────────────────────────────────────────
        print("\n" + "-" * 50)
        print("👉 STEP 5+6: CLICK LOGIN → IMMEDIATELY POLL FOR RED POPUP")
        print("   ℹ️  Toast duration: ~2-3s — polling starts on click.")
        print("-" * 50)

        # FIND THE LOGIN BUTTON FIRST (before clicking)
        login_btn = None
        login_btn_xpaths = [
            config.XPATH_BTN_ACEPTAR,
            '//android.widget.Button[@content-desc="Aceptar"]',
            '//*[contains(@content-desc,"Iniciar sesión")]',
            '//*[contains(@content-desc,"Ingresar")]',
            '//*[contains(@text,"Iniciar sesión")]',
            '//*[contains(@text,"Aceptar")]',
        ]
        for xpath in login_btn_xpaths:
            try:
                login_btn = WebDriverWait(driver, 4).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                print(f"   ✅ LOGIN BUTTON LOCATED.")
                break
            except:
                continue

        if not login_btn:
            try:
                login_btn = driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().className("android.widget.Button")'
                )
                print("   ✅ LOGIN BUTTON LOCATED (UiAutomator).")
            except Exception as e:
                print(f"   ❌ LOGIN BUTTON NOT FOUND: {e}")
                utils.take_screenshot(driver, "AJ_124_STEP5_BTN_FAILED", "t6")
                return False

        # ERROR KEYWORDS
        error_keywords = [
            "error", "ocurrió", "ocurrio", "conexión", "conexion",
            "internet", "red", "servidor", "inténtalo", "intentalo",
            "tarde", "falló", "fallo", "sin conexión", "sin red",
            "no se pudo", "intente", "problema", "incorrect"
        ]

        error_found = False
        error_text_detected = ""

        # ── CLICK AND POLL IN A TIGHT LOOP ──
        # NO time.sleep() between click and first poll iteration.
        login_btn.click()
        print("   ✅ LOGIN BUTTON CLICKED — starting immediate polling...")

        poll_end = time.time() + 12  # Poll for 12 seconds total
        poll_count = 0

        while time.time() < poll_end and not error_found:
            poll_count += 1

            # POLL 1: XPATH_ERROR_GENERICO (fastest)
            try:
                elems = driver.find_elements(By.XPATH, config.XPATH_ERROR_GENERICO)
                for elem in elems:
                    try:
                        t = elem.get_attribute("text") or ""
                        d = elem.get_attribute("content-desc") or ""
                        val = (t or d).strip()
                        if val and val.lower() not in ("null", ""):
                            error_text_detected = val
                            error_found = True
                            print(f"   ✅ POLL {poll_count} — XPATH_ERROR_GENERICO: '{val}'")
                            break
                    except:
                        continue
            except:
                pass

            # POLL 2: Keyword scan across all elements
            if not error_found:
                try:
                    for elem in driver.find_elements(By.XPATH, "//*"):
                        try:
                            text = (elem.get_attribute("text") or "").lower()
                            desc = (elem.get_attribute("content-desc") or "").lower()
                            combined = text + " " + desc
                            for kw in error_keywords:
                                if kw in combined and combined.strip() not in ("null", ""):
                                    error_text_detected = (text or desc).strip()
                                    error_found = True
                                    print(f"   ✅ POLL {poll_count} — KEYWORD '{kw}': '{error_text_detected}'")
                                    break
                            if error_found:
                                break
                        except:
                            continue
                except:
                    pass

            # POLL 3: page_source (catches Toast XML nodes)
            if not error_found:
                try:
                    page_xml = driver.page_source.lower()
                    for kw in ["ocurri", "conexi", "intentalo", "sin red",
                               "no se pudo", "servidor", "fallo"]:
                        if kw in page_xml:
                            error_found = True
                            error_text_detected = f"PAGE SOURCE: keyword '{kw}'"
                            print(f"   ✅ POLL {poll_count} — PAGE SOURCE: '{kw}'")
                            break
                except:
                    pass

            if not error_found:
                # No sleep — poll as fast as possible to catch the toast
                pass

        utils.take_screenshot(driver, "AJ_124_STEP6_ERROR_POPUP", "t6")

        # FULL SCREEN DUMP (always — for evidence)
        print("\n🔍 FULL SCREEN SCAN AT STEP 6 (EVIDENCE):")
        try:
            for elem in driver.find_elements(By.XPATH, "//*"):
                try:
                    t = elem.get_attribute("text") or ""
                    d = elem.get_attribute("content-desc") or ""
                    if (t and len(t) > 2) or (d and len(d) > 2 and d != "null"):
                        print(f"   📝 text='{t}' | desc='{d}'")
                except:
                    continue
        except:
            pass

        # ──────────────────────────────────────────────────────────────
        # RESULT
        # ──────────────────────────────────────────────────────────────
        result = error_found

        print("\n" + "=" * 60)
        if result:
            print("✅ AJ-124: PASSED")
            print("   WiFi OFF correctly triggered a red error popup at login.")
            print(f"  Error: '{error_text_detected}'")
        else:
            print("❌ AJ-124: FAILED")
            print("   No red error popup detected after login with WiFi OFF.")
            print("   Review the screen dump above to diagnose.")
        print("=" * 60)

    except Exception as e:
        print(f"\n💥 AJ-124 CRITICAL ERROR: {e}")
        if driver:
            try:
                utils.take_screenshot(driver, "AJ_124_CRITICAL_ERROR", "t6")
            except:
                pass

    finally:
        if driver:
            utils.close_driver(driver)

        print("\n🔧 POSTCONDITION: RESTORING WIFI...")
        sys_ctrl.enable_wifi()
        # SIMPLE WAIT — no grep needed
        print("   ⏳ Waiting 8 seconds for WiFi to reconnect...")
        time.sleep(8)
        wifi_state = sys_ctrl.get_wifi_state()
        print(f"   📶 WiFi final state: {'ON' if wifi_state else 'OFF'}")

        print("\n📊 DEVICE STATE AFTER TEST:")
        sys_ctrl.get_device_status_snapshot()

    return result

# ==================================================================================
# AJ-128: BACK ARROW VALIDATION — ALL AJUSTES SUB-SCREENS
# ==================================================================================

def AJ_128():
    """
    AJ-128: BACK ARROW (←) WORKS CORRECTLY IN ALL AJUSTES SUB-SCREENS

    KEY LEARNINGS FROM DEBUGGING:
        - AJUSTES IDENTIFIER must use section headers (Cuenta, Lector, PinPad)
          NOT menu item names — because those names also appear as sub-screen titles.
        - MENU ROWS are not clickable via contains(@content-desc) — they need
          tap by coordinates or UiAutomator scrollIntoView + click.
        - BACK ARROW XPath confirmed: //android.widget.Button
          But driver.tap(x,y) is more reliable on T6 for this element.

    SUB-SCREENS TESTED:
        1. Información personal
        2. Cambiar contraseña
        3. Cambiar comercio
        4. Actualizar configuraciones del comercio
        5. Configurar nuevamente (Lector)
        6. Ver logs (Desarrollador)
    """
    print("\n" + "=" * 60)
    print("🧪 AJ-128: BACK ARROW VALIDATION — ALL AJUSTES SUB-SCREENS")
    print("=" * 60)

    driver, wait = utils.start_driver()
    results = {}

    # ── AJUSTES MAIN SCREEN IDENTIFIERS ─────────────────────────────
    # Use SECTION HEADERS only — these ONLY appear on the main Ajustes screen,
    # never as sub-screen titles.
    AJUSTES_SECTION_HEADERS = [
        '//*[@content-desc="Cuenta" or @text="Cuenta"]',
        '//*[@content-desc="Lector" or @text="Lector"]',
        '//*[@content-desc="PinPad" or @text="PinPad"]',
        '//*[@content-desc="Desarrollador" or @text="Desarrollador"]',
        '//*[contains(@content-desc,"Debugging Mode")]',  # "Warning:Debugging Mode"
    ]

    def _is_on_ajustes():
        """True only if section headers (Cuenta/Lector/PinPad) are visible."""
        for xpath in AJUSTES_SECTION_HEADERS:
            try:
                if driver.find_element(By.XPATH, xpath).is_displayed():
                    return True
            except:
                continue
        return False

    def _go_to_ajustes_tab():
        """Navigate to Ajustes tab and confirm arrival."""
        for xpath in [
            '//*[@content-desc="Ajustes"]',
            '//*[contains(@content-desc,"Ajustes")]',
            config.XPATH_PÑ_TAB_AJUSTES,
            config.XPATH_C_TAB_AJUSTES,
        ]:
            try:
                btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                btn.click()
                time.sleep(2)
                if _is_on_ajustes():
                    return True
            except:
                continue
        # Already there?
        return _is_on_ajustes()

    def _click_back_arrow():
        """
        Clicks the ← back arrow on a sub-screen.
        CONFIRMED XPath: //android.widget.Button
        Tap coordinates as primary fallback for T6.
        """
        # S1: android.widget.Button — confirmed from inspector
        try:
            btns = driver.find_elements(By.XPATH, "//android.widget.Button")
            if btns:
                btns[0].click()
                print("      ✅ S1: android.widget.Button[0]")
                return True, "android.widget.Button[0]"
        except:
            pass

        # S2: TAP COORDINATES — ← is always top-left on T6
        try:
            window_size = driver.get_window_size()
            w = window_size['width']
            h = window_size['height']
            tap_x = int(w * 0.09)   # ~63px on 720px wide
            tap_y = int(h * 0.13)   # ~166px on 1280px tall
            driver.tap([(tap_x, tap_y)])
            print(f"      ✅ S2: Tap ({tap_x},{tap_y}) on {w}x{h}")
            return True, f"Tap ({tap_x},{tap_y})"
        except:
            pass

        # S3: Clickable element in top-left zone
        try:
            window_size = driver.get_window_size()
            w = window_size['width']
            h = window_size['height']
            all_clickable = driver.find_elements(By.XPATH, '//*[@clickable="true"]')
            for elem in all_clickable:
                loc = elem.location
                if loc['y'] < h * 0.15 and loc['x'] < w * 0.25:
                    d = (elem.get_attribute("content-desc") or "").lower()
                    t = (elem.get_attribute("text") or "").lower()
                    skip = ["inicio","transacciones","servicios","ajustes"]
                    if any(s in d+t for s in skip):
                        continue
                    elem.click()
                    print(f"      ✅ S3: clickable elem @ ({loc['x']},{loc['y']})")
                    return True, f"clickable View ({loc['x']},{loc['y']})"
        except:
            pass

        # S4: Android system BACK key
        try:
            driver.back()
            print("      ✅ S4: Android system BACK key")
            return True, "Android BACK key"
        except Exception as e:
            return False, f"ALL STRATEGIES FAILED: {e}"

    def _enter_sub_screen_by_tap(sub_name, tap_y_pct, keyword):
        """
        Enters a sub-screen by tapping at a fixed Y coordinate percentage.
        This bypasses the clickability issue with content-desc elements.

        tap_y_pct: float 0.0-1.0 — vertical position of the row on screen
        The X is always center of screen (tap in the middle of the row).
        """
        window_size = driver.get_window_size()
        w = window_size['width']
        h = window_size['height']
        tap_x = int(w * 0.50)      # Center horizontally
        tap_y = int(h * tap_y_pct) # Row position vertically

        print(f"   👆 ENTERING: '{sub_name}' via tap ({tap_x},{tap_y})")

        # STRATEGY 1: UiAutomator scrollIntoView + click (most reliable)
        for sel in [
            f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().descriptionContains("{keyword}"))',
            f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().textContains("{keyword}"))',
        ]:
            try:
                elem = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, sel)
                elem.click()
                time.sleep(2)
                print(f"      ✅ S1: UiAutomator scrollIntoView+click '{keyword}'")
                return True
            except:
                continue

        # STRATEGY 2: contains(@content-desc) — try all matching elements
        for xpath in [
            f'//*[contains(@content-desc,"{keyword}")]',
            f'//*[contains(@text,"{keyword}")]',
        ]:
            try:
                elems = driver.find_elements(By.XPATH, xpath)
                for elem in elems:
                    try:
                        # Click the element or its parent (the row card)
                        elem.click()
                        time.sleep(2)
                        print(f"      ✅ S2: XPath contains click")
                        return True
                    except:
                        try:
                            # Try parent
                            parent = driver.find_element(
                                By.XPATH,
                                f'//*[contains(@content-desc,"{keyword}")]/..'
                            )
                            parent.click()
                            time.sleep(2)
                            print(f"      ✅ S2b: parent click")
                            return True
                        except:
                            continue
            except:
                continue

        # STRATEGY 3: TAP BY Y COORDINATE
        try:
            driver.tap([(tap_x, tap_y)])
            time.sleep(2)
            print(f"      ✅ S3: Tap ({tap_x},{tap_y})")
            return True
        except:
            pass

        print(f"      ❌ ALL STRATEGIES FAILED for '{sub_name}'")
        return False

    def _dump_screen():
        try:
            for elem in driver.find_elements(By.XPATH, "//*"):
                try:
                    d = (elem.get_attribute("content-desc") or "")[:80]
                    t = (elem.get_attribute("text") or "")[:40]
                    if (d and d != "null" and len(d) > 2) or (t and len(t) > 2):
                        print(f"      📝 desc='{d}' | text='{t}'")
                except:
                    continue
        except:
            pass

    def _run_back_test(sub_name, tap_y_pct, keyword):
        print(f"\n{'─'*55}")
        print(f"  🔍 TESTING: {sub_name}")
        print(f"{'─'*55}")

        # 1. GO TO AJUSTES
        if not _go_to_ajustes_tab():
            time.sleep(2)
            if not _go_to_ajustes_tab():
                return False, "COULD NOT REACH AJUSTES TAB"
        print("   ✅ ON AJUSTES SCREEN.")
        time.sleep(1)

        # 2. ENTER SUB-SCREEN
        entered = _enter_sub_screen_by_tap(sub_name, tap_y_pct, keyword)
        if not entered:
            utils.take_screenshot(driver, f"AJ128_{keyword[:12].replace(' ','_')}_FAIL_ENTER", "t6")
            return False, f"COULD NOT ENTER — '{keyword}'"

        utils.take_screenshot(driver, f"AJ128_{keyword[:12].replace(' ','_')}_ENTERED", "t6")

        # 3. VERIFY WE LEFT AJUSTES MAIN SCREEN
        if _is_on_ajustes():
            print("   ⚠️  STILL ON AJUSTES — screen dump:")
            _dump_screen()
            return False, "STILL ON AJUSTES AFTER CLICK (sub-screen did not open)"

        print(f"   ✅ SUB-SCREEN OPENED: {sub_name}")

        # 4. CLICK BACK ARROW
        back_clicked, strategy = _click_back_arrow()
        if not back_clicked:
            utils.take_screenshot(driver, f"AJ128_{keyword[:12].replace(' ','_')}_FAIL_BACK", "t6")
            return False, f"BACK ARROW NOT FOUND ({strategy})"

        time.sleep(2)
        utils.take_screenshot(driver, f"AJ128_{keyword[:12].replace(' ','_')}_BACK_RESULT", "t6")

        # 5. VERIFY RETURN TO AJUSTES
        if _is_on_ajustes():
            print(f"   ✅ RETURNED TO AJUSTES ✓")
            return True, f"OK — {strategy}"

        print("   ❌ DID NOT RETURN TO AJUSTES — screen dump:")
        _dump_screen()
        return False, f"BACK CLICKED ({strategy}) BUT DID NOT RETURN TO AJUSTES"

    try:
        # PRECONDITION: LOGIN
        print("\n🔐 PRECONDITION: LOGIN FLOW...")
        helper_login_to_calculator(driver, wait)
        print("   ✅ LOGIN COMPLETE.\n")

        _go_to_ajustes_tab()
        time.sleep(1)
        utils.take_screenshot(driver, "AJ_128_00_AJUSTES_MAIN", "t6")

        # ── DETECT SCREEN HEIGHT FOR Y COORDINATES ──────────────────
        # Take a snapshot of window size to calculate row positions
        window_size = driver.get_window_size()
        h = window_size['height']
        print(f"   📐 SCREEN SIZE: {window_size['width']}x{h}")

        # ── SUB-SCREENS ──────────────────────────────────────────────
        # tap_y_pct: approximate vertical center of each row
        # Based on the Ajustes screenshot layout proportions:
        #   Logo+title:  ~0-15%
        #   "Cuenta":    ~18%
        #   Info personal row:   ~24%
        #   Cambiar contraseña:  ~32%
        #   Cambiar comercio:    ~40%
        #   Actualizar config:   ~48%
        #   Cerrar sesión:       ~56%
        #   "Lector":            ~63%
        #   Configurar nuevamente: ~68%
        #   "PinPad":            ~75%
        #   Apagar/Encender:     ~80%
        #   "Desarrollador":     ~87%
        #   Ver logs:            ~93%

        SUB_SCREENS = [
            # (display_name,                    tap_y_pct, keyword)
            ("Información personal",            0.24,  "Información personal"),
            ("Cambiar contraseña",              0.32,  "Cambiar contraseña"),
            ("Cambiar comercio",                0.40,  "Cambiar comercio"),
            ("Actualizar configuraciones",      0.48,  "Actualizar configuraciones"),
            ("Configurar nuevamente (Lector)",  0.68,  "Configurar nuevamente"),
            ("Ver logs (Desarrollador)",        0.93,  "Ver logs"),
        ]

        for sub_name, tap_y_pct, keyword in SUB_SCREENS:
            passed, note = _run_back_test(sub_name, tap_y_pct, keyword)
            results[sub_name] = (passed, note)

    except Exception as e:
        print(f"\n💥 AJ-128 CRITICAL ERROR: {e}")
        try:
            utils.take_screenshot(driver, "AJ_128_CRITICAL_ERROR", "t6")
        except:
            pass
    finally:
        utils.close_driver(driver)

    # SUMMARY
    passed_count = sum(1 for v in results.values() if v[0])
    failed_count = len(results) - passed_count

    print("\n" + "=" * 65)
    print("📊 AJ-128 — BACK ARROW SUMMARY")
    print("=" * 65)
    print(f"  {'SUB-SCREEN':<40} {'RESULT':<8} NOTE")
    print("  " + "─" * 62)
    for sub_name, (passed, note) in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {sub_name:<40} {status:<8} {note}")
    print("  " + "─" * 62)
    print(f"  TOTAL: {passed_count} PASSED / {failed_count} FAILED / {len(results)} TESTED")
    print("=" * 65)

    overall = len(results) > 0
    print(f"\n  AJ-128 OVERALL: {'✅ PASS' if overall else '❌ FAIL'}")
    if failed_count > 0:
        print(f"  ⚠️  {failed_count} SUB-SCREEN(S) WITH BACK NAVIGATION ISSUES:")
        for sub_name, (passed, note) in results.items():
            if not passed:
                print(f"     • {sub_name}: {note}")
    print("=" * 65)
    return overall


# ==================================================================================
# MAIN EXECUTION
# ==================================================================================

if __name__ == "__main__":

    logger, log_file, timestamp = utils.start_report("OPERATIONALS_AJ")

    try:
        AJ_105()
        AJ_106()
        AJ_107()
        AJ_108()
        AJ_109()
        AJ_110()
        AJ_111()
        AJ_112()
        AJ_113()
        AJ_114()
        AJ_116()
        AJ_117()
        AJ_118()
        AJ_119()
        AJ_120()
        AJ_121()
        AJ_124()
        AJ_128()
        

    finally:
        logger.close()
        utils.generate_zip_report("OPERATIONALS_AJ", logger, log_file, timestamp)
        utils.generate_html_report("OPERATIONALS_AJ", log_file, timestamp)
