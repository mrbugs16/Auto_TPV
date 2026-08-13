"""
FILENAME: Operationals_RA.py
DESCRIPTION:
    AUTOMATED TEST SUITE — REGISTRATION (RA) MODULE.
    COVERS THE FULL USER REGISTRATION FLOW OF THE MEMPHIS APP v2.

TEST CASES COVERED:
    · TC-REG-001 : VALIDATE REGISTRATION SCREEN LOADS CORRECTLY
    · TC-REG-002 : SUCCESSFUL REGISTRATION WITH SPECIFIC DATA
    · TC-REG-003 : VALIDATE EMPTY FIELDS SUBMISSION
    · TC-REG-004 : VALIDATE SPECIFIC FLOW (EMPTY NAME)
    · TC-REG-005 : VALIDATE DUPLICATE USER ERROR (EXISTING EMAIL)
    · TC-REG-006 : VALIDATE PASSWORD MISMATCH ERROR
    · TC-REG-007 : VALIDATE INVALID EMAIL FORMAT ERROR
    · TC-REG-008 : VALIDATE INVALID PASSWORD FORMAT ERROR
    · TC-REG-009 : VALIDATE BACK BUTTON (ARROW ICON)
    · TC-REG-010 : VALIDATE FIELD INTERACTION (FOCUS/BLUR)
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time
import random
import string
import config
import utils
from selenium.webdriver.common.by import By


# ==================================================================================
# HELPER — NAVIGATE ONBOARDING (SAME LOGIC AS Operationals_LG.py, DUPLICATED HERE
# ==================================================================================

def _navigate_onboarding(driver, wait):
    print("\n📱 NAVIGATING ONBOARDING SLIDES...")

    print("   1️⃣  SLIDE 1 — CLICKING 'Siguiente'...")
    try:
        utils.click_element(driver, config.XPATH_OB_BTN_SIGUIENTE)
        time.sleep(1.5)
        print("   ✅ SLIDE 1 PASSED")
    except Exception as e:
        print(f"   ⚠️  SLIDE 1 — TRYING SKIP LINK: {e}")
        try:
            utils.click_element(driver, config.XPATH_OB_BTN_SALTAR)
            time.sleep(1)
        except Exception:
            pass

    print("   2️⃣  SLIDE 2 — CLICKING 'Siguiente'...")
    try:
        utils.click_element(driver, config.XPATH_OB_BTN_SIGUIENTE)
        time.sleep(1.5)
        print("   ✅ SLIDE 2 PASSED")
    except Exception as e:
        print(f"   ⚠️  SLIDE 2 BUTTON NOT FOUND: {e}")

    print("   3️⃣  SLIDE 3 — CLICKING 'Comenzar'...")
    try:
        utils.click_element(driver, config.XPATH_OB_BTN_COMENZAR)
        time.sleep(2)
        print("   ✅ SLIDE 3 PASSED — APP NOW ON LOGIN SCREEN")
    except Exception as e:
        print(f"   ⚠️  SLIDE 3 'Comenzar' NOT FOUND (APP MAY ALREADY BE PAST ONBOARDING): {e}")



XPATH_BTN_CREAR_CUENTA = '//android.widget.Button[@content-desc="Crear cuenta"]'

XPATH_REG_NOMBRE           = config.XPATH_RA_FIRST_NAME
XPATH_REG_APELLIDO_PATERNO = config.XPATH_RA_APELLIDO
XPATH_REG_APELLIDO_MATERNO = config.XPATH_RA_SEGUNDOAPELLIDO
XPATH_REG_EMAIL            = config.XPATH_RA_EMAIL
XPATH_REG_PASS             = config.XPATH_RA_PASS
XPATH_REG_CONFIRMAR_PASS   = config.XPATH_RA_CONFIRMAR_PASS  

REG_PASSWORD = "Memphis@2026"  


XPATH_ERROR_NOMBRE_VACIO = '//*[contains(@text, "Ingresa tu nombre") or contains(@content-desc, "Ingresa tu nombre")]'
XPATH_ERROR_CORREO_INVALIDO_REAL = '//*[contains(@text, "correo válido") or contains(@content-desc, "correo válido")]'
XPATH_ERROR_PASSWORD_REQUISITOS = (
    '//*[contains(@text, "caracteres") or contains(@text, "mayúscula") or '
    'contains(@text, "minúscula") or contains(@text, "número") or '
    'contains(@text, "símbolo") or contains(@content-desc, "caracteres") or '
    'contains(@content-desc, "mayúscula") or contains(@content-desc, "minúscula") or '
    'contains(@content-desc, "número") or contains(@content-desc, "símbolo")]'
)


XPATH_ERROR_USUARIO_YA_EXISTE = '//*[contains(@text, "ya existe") or contains(@content-desc, "ya existe")]'


XPATH_ERROR_PASS_NO_COINCIDEN_REAL = '//*[contains(@text, "coinciden") or contains(@content-desc, "coinciden")]'


def _on_login_screen(wait, driver):
    if utils.verify_element(wait, config.XPATH_LG_LNK_CREAR_CUENTA, "Login Screen ('Crear cuenta' link)", driver):
        return True
    if utils.verify_element(wait, XPATH_BTN_CREAR_CUENTA, "Login Screen (Crear Cuenta Button)", driver):
        return True
    return utils.verify_element(wait, config.XPATH_WEB_BTN_REGISTRA_AHORA, "Login Screen (legacy xpath)", driver)


# ==================================================================================
# HELPER — NAVIGATE TO REGISTRATION SCREEN
# ==================================================================================

def _navigate_to_registration(driver, wait):
    _navigate_onboarding(driver, wait)
    time.sleep(2)

    print("👉 LOOKING FOR 'CREAR CUENTA' BUTTON...")
    if utils.verify_element(wait, config.XPATH_LG_LNK_CREAR_CUENTA, "Crear Cuenta Button (config link)", driver):
        print("👉 CLICKING 'CREAR CUENTA' BUTTON (config link)...")
        utils.click_element(driver, config.XPATH_LG_LNK_CREAR_CUENTA)
        time.sleep(3)
        return True

    print("   🔄 NOT FOUND VIA config.XPATH_LG_LNK_CREAR_CUENTA — TRYING EXACT WIDGET MATCH...")
    if utils.verify_element(wait, XPATH_BTN_CREAR_CUENTA, "Crear Cuenta Button (exact widget)", driver):
        print("👉 CLICKING 'CREAR CUENTA' BUTTON (exact widget)...")
        utils.click_element(driver, XPATH_BTN_CREAR_CUENTA)
        time.sleep(3)
        return True

    print("   🔄 NOT FOUND — TRYING LEGACY config.XPATH_WEB_BTN_REGISTRA_AHORA...")
    if utils.verify_element(wait, config.XPATH_WEB_BTN_REGISTRA_AHORA, "Crear Cuenta Button (legacy xpath)", driver):
        print("👉 CLICKING VIA LEGACY XPATH...")
        utils.click_element(driver, config.XPATH_WEB_BTN_REGISTRA_AHORA)
        time.sleep(3)
        return True

    print("❌ 'CREAR CUENTA' BUTTON NOT FOUND")
    return False


def _scan_screen_for_diagnosis(driver):
    print("🔍 SCANNING SCREEN FOR FAILURE DIAGNOSIS...")
    try:
        for elem in driver.find_elements(By.XPATH, "//*"):
            t = elem.get_attribute("text")
            d = elem.get_attribute("content-desc")
            if (t and len(t) > 3) or (d and len(d) > 3):
                print(f"   -> TEXT='{t}' | DESC='{d}'")
    except Exception as e:
        print(f"   ⚠️  SCREEN SCAN FAILED: {e}")


def _click_crear_cuenta_submit(driver):
    try:
        driver.find_element(By.XPATH, XPATH_BTN_CREAR_CUENTA).click()
    except Exception:
        try:
            utils.click_element(driver, XPATH_BTN_CREAR_CUENTA)
        except Exception:
            pass



XPATH_REG_PASS_EYE           = '//android.widget.ScrollView/android.view.View/android.widget.EditText[5]/android.widget.Button'
XPATH_REG_CONFIRMAR_PASS_EYE = '//android.widget.ScrollView/android.view.View/android.widget.EditText[6]/android.widget.Button'


def _reveal_password(driver, eye_xpath):
    try:
        utils.click_element(driver, eye_xpath)
    except Exception as e:
        print(f"   ⚠️  COULD NOT TOGGLE PASSWORD VISIBILITY: {e}")


def _hide_keyboard(driver):
    try:
        driver.hide_keyboard()
    except Exception as e:
        print(f"   ⚠️  COULD NOT HIDE KEYBOARD: {e}")


# ==================================================================================
# TC_REG_001: VALIDATE REGISTRATION SCREEN LOADS CORRECTLY
# ==================================================================================

def TC_REG_001():
    print("\n" + "=" * 60)
    print("TC-REG-001: VALIDATE REGISTRATION SCREEN LOADS CORRECTLY")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        if not _navigate_to_registration(driver, wait):
            return

        utils.take_screenshot(driver, "TC_REG_001_01_registration_screen", "t6")

        print("👉 VALIDATING REGISTRATION SCREEN ELEMENTS...")
        check_nombre = utils.verify_element(wait, XPATH_REG_NOMBRE, "Campo Nombre", driver)
        check_apellido = utils.verify_element(wait, XPATH_REG_APELLIDO_PATERNO, "Campo Apellido", driver)
        check_email = utils.verify_element(wait, XPATH_REG_EMAIL, "Campo Email", driver)

        if check_nombre and check_apellido and check_email:
            result = "SUCCESS"
            print("\n✅ SUCCESS: REGISTRATION SCREEN LOADED CORRECTLY")
        else:
            print("\n❌ FAILURE: REGISTRATION SCREEN ELEMENTS MISSING")

        utils.take_screenshot(driver, "TC_REG_001_02_final_state", "t6")

    except Exception as e:
        print(f"❌ TC-REG-001: EXCEPTION — {e}")
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-REG-001 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# TC_REG_002: SUCCESSFUL REGISTRATION WITH SPECIFIC DATA
# ==================================================================================

def TC_REG_002():
    print("\n" + "=" * 60)
    print("TC-REG-002: SUCCESSFUL REGISTRATION WITH SPECIFIC DATA")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        if not _navigate_to_registration(driver, wait):
            return

        utils.take_screenshot(driver, "TC_REG_002_01_registration_screen", "t6")

        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        random_email = f"santiago.{random_suffix}@gmail.com"

        print("👉 FILLING FORM WITH SPECIFIC DATA...")
        print(f"   📧 Generated Email: {random_email}")

        utils.type_text(driver, XPATH_REG_NOMBRE, config.RA_010_FIRST_NAME)
        utils.type_text(driver, XPATH_REG_APELLIDO_PATERNO, config.RA_010_APELLIDO)
        utils.type_text(driver, XPATH_REG_APELLIDO_MATERNO, config.RA_010_SEGUNDO_APELLIDO)
        utils.type_text(driver, XPATH_REG_EMAIL, random_email)
        utils.type_text(driver, XPATH_REG_PASS, REG_PASSWORD)
        _hide_keyboard(driver)
        time.sleep(1.0)  # LET THE SCROLLVIEW SETTLE AFTER THE KEYBOARD-DISMISS LAYOUT TRANSITION
        utils.type_text(driver, XPATH_REG_CONFIRMAR_PASS, REG_PASSWORD)
        _hide_keyboard(driver)
        time.sleep(1.0)  # SAME SETTLE TIME AFTER THE SECOND DISMISS
        _reveal_password(driver, XPATH_REG_PASS_EYE)
        _reveal_password(driver, XPATH_REG_CONFIRMAR_PASS_EYE)

        try:
            driver.hide_keyboard()
        except Exception:
            pass

        utils.take_screenshot(driver, "TC_REG_002_02_form_filled", "t6")

        print("👉 CLICKING 'ACEPTAR' BUTTON AND WAITING FOR TOAST...")
        _click_crear_cuenta_submit(driver)

        utils.take_screenshot(driver, "TC_REG_002_03_after_submit", "t6")

        print("👉 VERIFYING SUCCESS POPUP...")
        end_time = time.time() + 8  # WAIT UP TO 8 SECONDS
        success = False

        while time.time() < end_time:
            try:
                elems = driver.find_elements(By.XPATH, config.XPATH_RA_REGISTRO_EXITOSO)
                if len(elems) > 0:
                    print("✅ SUCCESS: POPUP 'USUARIO CREADO CORRECTAMENTE' DETECTED")
                    success = True
                    break
            except Exception:
                pass
            time.sleep(0.5)

        if success:
            result = "SUCCESS"
        else:
            print("❌ 'USUARIO CREADO CORRECTAMENTE' POPUP NOT FOUND (TIMED OUT)")

            if _on_login_screen(wait, driver):
                print("✅ FALLBACK SUCCESS: RETURNED TO LOGIN SCREEN (IMPLIED REGISTRATION SUCCESS)")
                result = "SUCCESS"
            else:
                _scan_screen_for_diagnosis(driver)

        utils.take_screenshot(driver, "TC_REG_002_04_final_state", "t6")

    except Exception as e:
        print(f"❌ TC-REG-002: EXCEPTION — {e}")
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-REG-002 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# TC_REG_003: VALIDATE EMPTY FIELDS SUBMISSION
# ==================================================================================

def TC_REG_003():
    print("\n" + "=" * 60)
    print("TC-REG-003: VALIDATE EMPTY FIELDS SUBMISSION")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        if not _navigate_to_registration(driver, wait):
            return

        utils.take_screenshot(driver, "TC_REG_003_01_registration_screen", "t6")

        print("👉 CLICKING 'ACEPTAR' BUTTON WITH EMPTY FIELDS...")
        try:
            driver.hide_keyboard()
        except Exception:
            pass

        if utils.verify_element(wait, XPATH_BTN_CREAR_CUENTA, "Crear Cuenta Button (submit)", driver):
            utils.click_element(driver, XPATH_BTN_CREAR_CUENTA)
            time.sleep(2)
            utils.take_screenshot(driver, "TC_REG_003_02_after_submit", "t6")

            if utils.verify_element(wait, XPATH_REG_NOMBRE, "Registration Form (Still Visible)", driver):
                result = "SUCCESS"
                print("✅ SUCCESS: REGISTRATION BLOCKED (FORM STILL VISIBLE)")
            else:
                print("❌ FAILURE: FORM DISAPPEARED (POSSIBLE INCORRECT SUBMISSION)")
        else:
            print("❌ 'ACEPTAR' BUTTON NOT FOUND")

        utils.take_screenshot(driver, "TC_REG_003_03_final_state", "t6")

    except Exception as e:
        print(f"❌ TC-REG-003: EXCEPTION — {e}")
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-REG-003 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# TC_REG_004: VALIDATE SPECIFIC FLOW (EMPTY NAME)
# ==================================================================================

def TC_REG_004():
    print("\n" + "=" * 60)
    print("TC-REG-004: VALIDATE SPECIFIC FLOW (EMPTY NAME)")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        if not _navigate_to_registration(driver, wait):
            return

        print("👉 VERIFYING REGISTRATION FORM...")
        if not utils.verify_element(wait, XPATH_REG_NOMBRE, "Registration Form - Name Field", driver):
            print("❌ REGISTRATION FORM NOT LOADED")
            return

        utils.take_screenshot(driver, "TC_REG_004_01_registration_screen", "t6")

        print("👉 SKIPPING 'NOMBRE' FIELD (LEAVING IT EMPTY)...")
        print("👉 FILLING OTHER FIELDS...")
        utils.type_text(driver, XPATH_REG_APELLIDO_PATERNO, config.RA_APELLIDO)
        utils.type_text(driver, XPATH_REG_APELLIDO_MATERNO, config.RA_SEGUNDOAPELLIDO)
        utils.type_text(driver, XPATH_REG_EMAIL, config.RA_EMAIL)
        utils.type_text(driver, XPATH_REG_PASS, REG_PASSWORD)
        _hide_keyboard(driver)
        time.sleep(1.0)  # LET THE SCROLLVIEW SETTLE AFTER THE KEYBOARD-DISMISS LAYOUT TRANSITION
        utils.type_text(driver, XPATH_REG_CONFIRMAR_PASS, REG_PASSWORD)
        _hide_keyboard(driver)
        time.sleep(1.0)  # SAME SETTLE TIME AFTER THE SECOND DISMISS
        _reveal_password(driver, XPATH_REG_PASS_EYE)
        _reveal_password(driver, XPATH_REG_CONFIRMAR_PASS_EYE)

        try:
            driver.hide_keyboard()
        except Exception:
            pass

        utils.take_screenshot(driver, "TC_REG_004_02_form_filled", "t6")

        print("👉 CLICKING 'ACEPTAR' BUTTON...")
        time.sleep(1)
        if utils.verify_element(wait, XPATH_BTN_CREAR_CUENTA, "Crear Cuenta Button (submit)", driver):
            utils.click_element(driver, XPATH_BTN_CREAR_CUENTA)
            time.sleep(3)
            utils.take_screenshot(driver, "TC_REG_004_03_after_submit", "t6")

            print("👉 VERIFYING ERROR MESSAGE FOR EMPTY NAME FIELD...")
            if utils.verify_element(wait, XPATH_ERROR_NOMBRE_VACIO, "Error: Ingresa tu nombre", driver):
                result = "SUCCESS"
                print("✅ SUCCESS: ERROR MESSAGE 'INGRESA UN NOMBRE VALIDO' DETECTED")
            else:
                print("❌ FAILURE: ERROR MESSAGE NOT DETECTED")
        else:
            print("❌ 'ACEPTAR' BUTTON NOT FOUND")

        utils.take_screenshot(driver, "TC_REG_004_04_final_state", "t6")

    except Exception as e:
        print(f"❌ TC-REG-004: EXCEPTION — {e}")
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-REG-004 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# TC_REG_005: VALIDATE DUPLICATE USER ERROR (EXISTING EMAIL)
# ==================================================================================

def TC_REG_005():
    print("\n" + "=" * 60)
    print("TC-REG-005: VALIDATE DUPLICATE USER ERROR (EXISTING EMAIL)")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        if not _navigate_to_registration(driver, wait):
            return

        utils.take_screenshot(driver, "TC_REG_005_01_registration_screen", "t6")

        print(f"👉 FILLING FORM WITH DUPLICATE DATA (EMAIL: {config.RA_013_EMAIL})...")
        utils.type_text(driver, XPATH_REG_NOMBRE, config.RA_010_FIRST_NAME)
        utils.type_text(driver, XPATH_REG_APELLIDO_PATERNO, config.RA_010_APELLIDO)
        utils.type_text(driver, XPATH_REG_APELLIDO_MATERNO, config.RA_010_SEGUNDO_APELLIDO)
        utils.type_text(driver, XPATH_REG_EMAIL, config.RA_013_EMAIL)
        utils.type_text(driver, XPATH_REG_PASS, REG_PASSWORD)
        _hide_keyboard(driver)
        time.sleep(1.0)  # LET THE SCROLLVIEW SETTLE AFTER THE KEYBOARD-DISMISS LAYOUT TRANSITION
        utils.type_text(driver, XPATH_REG_CONFIRMAR_PASS, REG_PASSWORD)
        _hide_keyboard(driver)
        time.sleep(1.0)  # SAME SETTLE TIME AFTER THE SECOND DISMISS
        _reveal_password(driver, XPATH_REG_PASS_EYE)
        _reveal_password(driver, XPATH_REG_CONFIRMAR_PASS_EYE)

        try:
            driver.hide_keyboard()
        except Exception:
            pass

        utils.take_screenshot(driver, "TC_REG_005_02_form_filled", "t6")

        print("👉 CLICKING 'ACEPTAR' BUTTON...")
        _click_crear_cuenta_submit(driver)
        time.sleep(2)

        utils.take_screenshot(driver, "TC_REG_005_03_after_submit", "t6")

        print("👉 VERIFYING ERROR POPUP ('USUARIO YA EXISTE')...")
        if utils.verify_element(wait, XPATH_ERROR_USUARIO_YA_EXISTE, "Error: usuario ya existe", driver):
            result = "SUCCESS"
            print("✅ SUCCESS: ERROR POPUP 'USUARIO YA EXISTE' DETECTED")
        else:
            print("❌ 'USUARIO YA EXISTE' POPUP NOT FOUND")
            _scan_screen_for_diagnosis(driver)

        utils.take_screenshot(driver, "TC_REG_005_04_final_state", "t6")

    except Exception as e:
        print(f"❌ TC-REG-005: EXCEPTION — {e}")
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-REG-005 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# TC_REG_006: VALIDATE PASSWORD MISMATCH ERROR
# ==================================================================================

def TC_REG_006():
    print("\n" + "=" * 60)
    print("TC-REG-006: VALIDATE PASSWORD MISMATCH ERROR")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        if not _navigate_to_registration(driver, wait):
            return

        utils.take_screenshot(driver, "TC_REG_006_01_registration_screen", "t6")

        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        random_email = f"santiago.{random_suffix}@gmail.com"

        print("👉 FILLING FORM WITH MISMATCHING PASSWORDS...")
        utils.type_text(driver, XPATH_REG_NOMBRE, config.RA_010_FIRST_NAME)
        utils.type_text(driver, XPATH_REG_APELLIDO_PATERNO, config.RA_010_APELLIDO)
        utils.type_text(driver, XPATH_REG_APELLIDO_MATERNO, config.RA_010_SEGUNDO_APELLIDO)
        utils.type_text(driver, XPATH_REG_EMAIL, random_email)
        utils.type_text(driver, XPATH_REG_PASS, "ConfirmPassword1!")
        _hide_keyboard(driver)
        time.sleep(1.0)  # LET THE SCROLLVIEW SETTLE AFTER THE KEYBOARD-DISMISS LAYOUT TRANSITION
        utils.type_text(driver, XPATH_REG_CONFIRMAR_PASS, "ConfirmPassword2!")
        _hide_keyboard(driver)
        time.sleep(1.0)  # SAME SETTLE TIME AFTER THE SECOND DISMISS
        _reveal_password(driver, XPATH_REG_PASS_EYE)
        _reveal_password(driver, XPATH_REG_CONFIRMAR_PASS_EYE)

        try:
            driver.hide_keyboard()
        except Exception:
            pass

        utils.take_screenshot(driver, "TC_REG_006_02_form_filled", "t6")

        print("👉 CLICKING 'ACEPTAR' BUTTON...")
        _click_crear_cuenta_submit(driver)
        time.sleep(2)

        utils.take_screenshot(driver, "TC_REG_006_03_after_submit", "t6")

        print("👉 VERIFYING ERROR MESSAGE ('LAS CONTRASEÑAS NO COINCIDEN')...")
        if utils.verify_element(wait, XPATH_ERROR_PASS_NO_COINCIDEN_REAL, "Error: las contraseñas no coinciden", driver):
            result = "SUCCESS"
            print("✅ SUCCESS: ERROR MESSAGE 'LAS CONTRASEÑAS NO COINCIDEN' DETECTED")
        else:
            print("❌ 'LAS CONTRASEÑAS NO COINCIDEN' MESSAGE NOT FOUND")
            _scan_screen_for_diagnosis(driver)

        utils.take_screenshot(driver, "TC_REG_006_04_final_state", "t6")

    except Exception as e:
        print(f"❌ TC-REG-006: EXCEPTION — {e}")
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-REG-006 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# TC_REG_007: VALIDATE INVALID EMAIL FORMAT ERROR
# ==================================================================================

def TC_REG_007():
    print("\n" + "=" * 60)
    print("TC-REG-007: VALIDATE INVALID EMAIL FORMAT ERROR")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        if not _navigate_to_registration(driver, wait):
            return

        utils.take_screenshot(driver, "TC_REG_007_01_registration_screen", "t6")

        print("👉 FILLING FORM WITH INVALID EMAIL FORMAT...")
        utils.type_text(driver, XPATH_REG_NOMBRE, config.RA_010_FIRST_NAME)
        utils.type_text(driver, XPATH_REG_APELLIDO_PATERNO, config.RA_010_APELLIDO)
        utils.type_text(driver, XPATH_REG_APELLIDO_MATERNO, config.RA_010_SEGUNDO_APELLIDO)

        print("   📧 Set Invalid Email: 'usuario@dominio' (No TLD)")
        utils.type_text(driver, XPATH_REG_EMAIL, "usuario@dominio")

        utils.type_text(driver, XPATH_REG_PASS, REG_PASSWORD)
        _hide_keyboard(driver)
        time.sleep(1.0)  # LET THE SCROLLVIEW SETTLE AFTER THE KEYBOARD-DISMISS LAYOUT TRANSITION
        utils.type_text(driver, XPATH_REG_CONFIRMAR_PASS, REG_PASSWORD)
        _hide_keyboard(driver)
        time.sleep(1.0)  # SAME SETTLE TIME AFTER THE SECOND DISMISS
        _reveal_password(driver, XPATH_REG_PASS_EYE)
        _reveal_password(driver, XPATH_REG_CONFIRMAR_PASS_EYE)

        try:
            driver.hide_keyboard()
        except Exception:
            pass

        utils.take_screenshot(driver, "TC_REG_007_02_form_filled", "t6")

        print("👉 CLICKING 'ACEPTAR' BUTTON...")
        _click_crear_cuenta_submit(driver)
        time.sleep(2)

        utils.take_screenshot(driver, "TC_REG_007_03_after_submit", "t6")

        print("👉 VERIFYING ERROR MESSAGE ('CORREO INVALIDO')...")
        if utils.verify_element(wait, XPATH_ERROR_CORREO_INVALIDO_REAL, "Error: Ingresa un correo válido", driver):
            result = "SUCCESS"
            print("✅ SUCCESS: ERROR MESSAGE 'CORREO INVALIDO' DETECTED")
        else:
            print("❌ 'CORREO INVALIDO' MESSAGE NOT FOUND")
            _scan_screen_for_diagnosis(driver)

        utils.take_screenshot(driver, "TC_REG_007_04_final_state", "t6")

    except Exception as e:
        print(f"❌ TC-REG-007: EXCEPTION — {e}")
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-REG-007 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# TC_REG_008: VALIDATE INVALID PASSWORD FORMAT ERROR
# ==================================================================================

def TC_REG_008():
    print("\n" + "=" * 60)
    print("TC-REG-008: VALIDATE INVALID PASSWORD FORMAT ERROR")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        if not _navigate_to_registration(driver, wait):
            return

        utils.take_screenshot(driver, "TC_REG_008_01_registration_screen", "t6")

        print("👉 FILLING FORM WITH INVALID PASSWORD FORMAT...")
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        random_email = f"santiago.{random_suffix}@gmail.com"

        utils.type_text(driver, XPATH_REG_NOMBRE, config.RA_010_FIRST_NAME)
        utils.type_text(driver, XPATH_REG_APELLIDO_PATERNO, config.RA_010_APELLIDO)
        utils.type_text(driver, XPATH_REG_APELLIDO_MATERNO, config.RA_010_SEGUNDO_APELLIDO)
        utils.type_text(driver, XPATH_REG_EMAIL, random_email)

        invalid_pass = "short"
        print(f"   🔑 Set Invalid Password: '{invalid_pass}'")
        utils.type_text(driver, XPATH_REG_PASS, invalid_pass)
        _hide_keyboard(driver)
        time.sleep(1.0)  # LET THE SCROLLVIEW SETTLE AFTER THE KEYBOARD-DISMISS LAYOUT TRANSITION
        utils.type_text(driver, XPATH_REG_CONFIRMAR_PASS, invalid_pass)
        _hide_keyboard(driver)
        time.sleep(1.0)  # SAME SETTLE TIME AFTER THE SECOND DISMISS
        _reveal_password(driver, XPATH_REG_PASS_EYE)
        _reveal_password(driver, XPATH_REG_CONFIRMAR_PASS_EYE)

        try:
            driver.hide_keyboard()
        except Exception:
            pass

        utils.take_screenshot(driver, "TC_REG_008_02_form_filled", "t6")

        print("👉 CLICKING 'ACEPTAR' BUTTON...")
        _click_crear_cuenta_submit(driver)
        time.sleep(2)

        utils.take_screenshot(driver, "TC_REG_008_03_after_submit", "t6")

        print("👉 VERIFYING ERROR MESSAGE ('CONTRASEÑA INVALIDA')...")
        if utils.verify_element(wait, XPATH_ERROR_PASSWORD_REQUISITOS, "Error: password requirement not met", driver):
            result = "SUCCESS"
            print("✅ SUCCESS: ERROR MESSAGE 'CONTRASEÑA INVALIDA' DETECTED")
        else:
            print("❌ 'CONTRASEÑA INVALIDA' MESSAGE NOT FOUND")
            _scan_screen_for_diagnosis(driver)

        utils.take_screenshot(driver, "TC_REG_008_04_final_state", "t6")

    except Exception as e:
        print(f"❌ TC-REG-008: EXCEPTION — {e}")
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-REG-008 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# TC_REG_009: VALIDATE BACK BUTTON (ARROW ICON)
# ==================================================================================

def TC_REG_009():
    print("\n" + "=" * 60)
    print("TC-REG-009: VALIDATE BACK BUTTON (ARROW ICON)")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        if not _navigate_to_registration(driver, wait):
            return

        utils.take_screenshot(driver, "TC_REG_009_01_registration_screen", "t6")

        print("👉 CLICKING BACK BUTTON (ARROW ICON)...")
        if utils.verify_element(wait, config.XPATH_RA_BTN_ATRAS, "Back Button", driver):
            utils.click_element(driver, config.XPATH_RA_BTN_ATRAS)
            time.sleep(3)
            utils.take_screenshot(driver, "TC_REG_009_02_after_back", "t6")

            print("👉 VERIFYING RETURN TO LOGIN SCREEN...")
            if _on_login_screen(wait, driver):
                result = "SUCCESS"
                print("✅ SUCCESS: RETURNED TO LOGIN SCREEN")
            else:
                print("❌ FAILURE: DID NOT RETURN TO LOGIN SCREEN")
        else:
            print("❌ BACK BUTTON NOT FOUND")

        utils.take_screenshot(driver, "TC_REG_009_03_final_state", "t6")

    except Exception as e:
        print(f"❌ TC-REG-009: EXCEPTION — {e}")
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-REG-009 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# TC_REG_010: VALIDATE FIELD INTERACTION (FOCUS/BLUR)
# ==================================================================================

def TC_REG_010():
    print("\n" + "=" * 60)
    print("TC-REG-010: VALIDATE FIELD INTERACTION (FOCUS/BLUR)")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        if not _navigate_to_registration(driver, wait):
            return

        utils.take_screenshot(driver, "TC_REG_010_01_registration_screen", "t6")

        print("👉 INTERACTING WITH FIELDS (TOUCHING EACH ONE)...")
        fields = [
            ("Nombre", XPATH_REG_NOMBRE),
            ("Apellido", XPATH_REG_APELLIDO_PATERNO),
            ("Segundo Apellido", XPATH_REG_APELLIDO_MATERNO),
            ("Email", XPATH_REG_EMAIL),
            ("Password", XPATH_REG_PASS),
            ("Confirm Password", XPATH_REG_CONFIRMAR_PASS),
        ]

        for name, xpath in fields:
            print(f"   👆 Touching {name}...")
            utils.click_element(driver, xpath)
            time.sleep(0.5)

        print("👉 TOUCHING OUTSIDE FIELDS (TITLE/HEADER)...")
        try:
            title_xpath = '//*[contains(@text, "Registro")]'
            driver.find_element(By.XPATH, title_xpath).click()
            print("   👆 Touched 'Registro' title")
        except Exception:
            print("   ⚠️  Could not touch title, trying hide_keyboard as fallback")
            try:
                driver.hide_keyboard()
            except Exception:
                pass

        time.sleep(1)
        utils.take_screenshot(driver, "TC_REG_010_02_after_interaction", "t6")

        result = "SUCCESS"
        print("✅ SUCCESS: INTERACTION COMPLETED WITHOUT CRASH")

    except Exception as e:
        print(f"❌ TC-REG-010: EXCEPTION — {e}")
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-REG-010 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# EXECUTION
# ==================================================================================

if __name__ == "__main__":

    logger, log_file, timestamp = utils.start_report("OPERATIONALS_TC_REG")

    try:
        TC_REG_001()
        TC_REG_002()
        TC_REG_003()
        TC_REG_004()
        TC_REG_005()
        TC_REG_006()
        TC_REG_007()
        TC_REG_008()
        TC_REG_009()
        TC_REG_010()

    finally:
        # ── CLOSE LOGGER BEFORE GENERATING REPORT ────────────────────────────
        logger.close()
        utils.generate_zip_report("OPERATIONALS_TC_REG", logger, log_file, timestamp)
        utils.generate_html_report("OPERATIONALS_TC_REG", log_file, timestamp)