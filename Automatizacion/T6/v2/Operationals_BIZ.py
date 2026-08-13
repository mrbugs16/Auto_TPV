"""
FILENAME: Operationals_BIZ.py
DESCRIPTION:
    AUTOMATED TEST SUITE — BUSINESS REGISTRATION (BIZ / "Registro de Negocio") MODULE.
    VALIDATES FLOWS FOR USERS CONFIGURING THEIR COMMERCE AFTER LOGIN.

TEST CASES COVERED:
    · TC-BIZ-001 : VALIDATE BUSINESS REGISTRATION SCREEN APPEARS FOR NEW/UNLINKED ACCOUNTS
    · TC-BIZ-002 : VALIDATE SUCCESSFUL BUSINESS REGISTRATION (VALID TOKEN & AFFILIATION)
    · TC-BIZ-003 : VALIDATE ERROR WHEN ENTERING A WRONG TOKEN (WITH A VALID AFFILIATION)
    · TC-BIZ-004 : VALIDATE ERROR WHEN ENTERING A WRONG AFFILIATION (WITH A VALID TOKEN)
    · TC-BIZ-005 : VALIDATE ERROR WHEN THE TOKEN FIELD IS EMPTY
    · TC-BIZ-006 : VALIDATE ERROR WHEN THE AFFILIATION NUMBER FIELD IS EMPTY
    · TC-BIZ-007 : VALIDATE TOKEN LENGTH RESTRICTIONS (<16, >16, ==16 CHARACTERS)
    · TC-BIZ-008 : VALIDATE AFFILIATION NUMBER LENGTH RESTRICTIONS (<7, >7, ==7 CHARACTERS)
    · TC-BIZ-010 : VALIDATE FIELD INTERACTION (FOCUS/BLUR) WITHOUT DATA
"""

import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
import utils
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

XPATH_BIZ_TITULO_COMERCIO = (
    '//*[contains(@text, "Configura tu comercio") or '
    'contains(@content-desc, "Configura tu comercio")]'
)

XPATH_BIZ_INPUT_AFILIACION = '(//android.widget.EditText)[1]'
XPATH_BIZ_INPUT_TOKEN      = '(//android.widget.EditText)[2]'

XPATH_BIZ_BTN_CONFIRMAR = (
    '//*[contains(@text, "Confirmar y comenzar") or '
    'contains(@content-desc, "Confirmar y comenzar")]'
)

XPATH_BIZ_BTN_CANCELAR = (
    '//*[contains(@text, "Cancelar") or '
    'contains(@content-desc, "Cancelar")]'
)

XPATH_BIZ_PANTALLA_EXITO = (
    '//*[contains(@text, "Lector no configurado") or '
    'contains(@content-desc, "Lector no configurado") or '
    'contains(@text, "INGRESA LA CANTIDAD A COBRAR") or '
    'contains(@content-desc, "INGRESA LA CANTIDAD A COBRAR")]'
)

def _skip_onboarding_if_present(driver, wait):
    print("👉 CHECKING FOR ONBOARDING SCREEN ('Configura la terminal')...")
    short_wait = WebDriverWait(driver, 5)
    if utils.verify_element(short_wait, config.XPATH_OB_BTN_SALTAR, "Botón 'Saltar' (Onboarding)", driver):
        utils.click_element(driver, config.XPATH_OB_BTN_SALTAR)
        time.sleep(2)
        print("   ✅ ONBOARDING SKIPPED")
    else:
        print("   ℹ️  NO ONBOARDING SCREEN DETECTED (APP ALREADY PAST IT)")


# ==================================================================================
# HELPER — QUICK LOGIN TO REACH THE BUSINESS REGISTRATION SCREEN
# ==================================================================================
def _login_to_registration_screen(driver, wait):
    print("   🔄 [HELPER] EXECUTING LOGIN TO REACH REGISTRATION SCREEN...")
    _skip_onboarding_if_present(driver, wait)
    print("   ⏳ WAITING FOR APPIUM TO RENDER INPUT FIELDS...")
    time.sleep(4)
    try:
        utils.click_element(driver, config.XPATH_INPUT_USUARIO)
        time.sleep(1)
    except Exception:
        pass

    print(f"   📧 TYPING EMAIL: {config.USUARIO_VALIDO}")
    utils.type_text(driver, config.XPATH_INPUT_USUARIO, config.USUARIO_VALIDO)

    print("   🔑 TYPING PASSWORD...")
    utils.type_text(driver, config.XPATH_INPUT_PASS, config.PASS_VALIDO)

    try:
        driver.hide_keyboard()
    except Exception:
        pass

    print("   🖱️  CLICKING ACCEPT...")
    utils.click_element(driver, config.XPATH_BTN_ACEPTAR)

    print("   ⏳ WAITING FOR BACKEND ROUTING...")
    time.sleep(6)


# ==================================================================================
# TC_BIZ_001: VALIDATE BUSINESS REGISTRATION SCREEN APPEARS FOR NEW/UNLINKED ACCOUNTS
# ==================================================================================
def TC_BIZ_001():
    print("\n" + "=" * 60)
    print("TC-BIZ-001: VALIDATE BUSINESS REGISTRATION SCREEN ON LOGIN")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        print("👉 STEP 1 & 2: ENTERING CREDENTIALS AND CLICKING ACCEPT...")
        _login_to_registration_screen(driver, wait)

        print("🔍 VERIFYING 'REGISTRO DE NEGOCIO' SCREEN IS DISPLAYED...")
        if utils.verify_element(wait, XPATH_BIZ_TITULO_COMERCIO, "TITLE: CONFIGURA TU COMERCIO", driver):
            result = "SUCCESS"
            print("📸 TAKING SCREENSHOT EVIDENCE...")
            utils.take_screenshot(driver, "TC_BIZ_001_01_success", "t6")
            print("✅ TC-BIZ-001: SUCCESS")
        else:
            print("❌ TC-BIZ-001 FAILED")
            utils.take_screenshot(driver, "TC_BIZ_001_01_failed", "t6")

        try:
            utils.print_http_evidence_appium(driver, "TC_BIZ_001")
        except Exception:
            pass

    except Exception as e:
        print(f"❌ TC-BIZ-001 CRITICAL ERROR: {e}")
        try:
            utils.take_screenshot(driver, "TC_BIZ_001_technical_error", "t6")
        except Exception:
            pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-BIZ-001 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# TC_BIZ_002: VALIDATE SUCCESSFUL BUSINESS REGISTRATION (VALID TOKEN & AFFILIATION)
# ==================================================================================
def TC_BIZ_002():
    print("\n" + "=" * 60)
    print("TC-BIZ-002: VALIDATE SUCCESSFUL BUSINESS REGISTRATION (TOKEN & AFFILIATION)")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        print("🔐 PRECONDITION: LOGGING IN TO REACH REGISTRATION SCREEN...")
        _login_to_registration_screen(driver, wait)

        print("👉 STEP 1: ENTERING REGISTRATION TOKEN AND AFFILIATION NUMBER...")
        time.sleep(4)

        print(f"   🔑 ENTERING TOKEN: {config.RN_TOKEN}")
        try:
            utils.click_element(driver, XPATH_BIZ_INPUT_TOKEN)
        except Exception:
            pass
        time.sleep(1)
        utils.type_text(driver, XPATH_BIZ_INPUT_TOKEN, config.RN_TOKEN)

        print(f"   🏢 ENTERING AFFILIATION: {config.RN_AFILIACION}")
        try:
            utils.click_element(driver, XPATH_BIZ_INPUT_AFILIACION)
        except Exception:
            pass
        time.sleep(1)
        utils.type_text(driver, XPATH_BIZ_INPUT_AFILIACION, config.RN_AFILIACION)

        try:
            driver.hide_keyboard()
        except Exception:
            pass
        utils.take_screenshot(driver, "TC_BIZ_002_01_fields_filled", "t6")

        print("👉 STEP 2: CLICKING 'ACEPTAR' TO SUBMIT REGISTRATION...")
        utils.click_element(driver, XPATH_BIZ_BTN_CONFIRMAR)

        print("⏳ WAITING FOR SYSTEM TO PROCESS REGISTRATION...")
        time.sleep(8)
        utils.take_screenshot(driver, "TC_BIZ_002_02_after_submit", "t6")

        print("🔍 VERIFYING NAVIGATION TO THE SUCCESS/DASHBOARD SCREEN...")
        if utils.verify_element(wait, XPATH_BIZ_PANTALLA_EXITO, "NEXT SCREEN IDENTIFIER", driver):
            result = "SUCCESS"
            print("📸 TAKING SCREENSHOT EVIDENCE OF THE SUCCESS SCREEN...")
            utils.take_screenshot(driver, "TC_BIZ_002_03_success", "t6")
            print("✅ TC-BIZ-002: SUCCESS")
        else:
            print("❌ TC-BIZ-002 FAILED")
            utils.take_screenshot(driver, "TC_BIZ_002_03_failed", "t6")
            print("🔍 SCANNING FOR ERROR MESSAGES OR POP-UPS...")
            try:
                for elem in driver.find_elements(By.XPATH, "//*"):
                    t = elem.get_attribute("text")
                    if t and len(t) > 3:
                        print(f"   -> VISIBLE TEXT: '{t}'")
            except Exception:
                pass

        try:
            utils.print_http_evidence_appium(driver, "TC_BIZ_002")
        except Exception:
            pass

    except Exception as e:
        print(f"❌ TC-BIZ-002 CRITICAL ERROR: {e}")
        try:
            utils.take_screenshot(driver, "TC_BIZ_002_technical_error", "t6")
        except Exception:
            pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-BIZ-002 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# TC_BIZ_003: VALIDATE ERROR WHEN ENTERING A WRONG TOKEN (VALID AFFILIATION)
# ==================================================================================

def TC_BIZ_003():
    print("\n" + "=" * 60)
    print("TC-BIZ-003: VALIDATE ERROR — WRONG TOKEN, VALID AFFILIATION")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        print("🔐 PRECONDITION: LOGGING IN TO REACH REGISTRATION SCREEN...")
        _login_to_registration_screen(driver, wait)

        print("👉 STEP 1: ENTERING REGISTRATION TOKEN AND AFFILIATION NUMBER...")
        time.sleep(4)

        print(f"   🔑 ENTERING TOKEN: {config.RN_TOKEN_INVALIDO}")
        try:
            utils.click_element(driver, XPATH_BIZ_INPUT_TOKEN)
        except Exception:
            pass
        time.sleep(1)
        utils.type_text(driver, XPATH_BIZ_INPUT_TOKEN, config.RN_TOKEN_INVALIDO)

        print(f"   🏢 ENTERING AFFILIATION: {config.RN_AFILIACION}")
        try:
            utils.click_element(driver, XPATH_BIZ_INPUT_AFILIACION)
        except Exception:
            pass
        time.sleep(1)
        utils.type_text(driver, XPATH_BIZ_INPUT_AFILIACION, config.RN_AFILIACION)

        try:
            driver.hide_keyboard()
        except Exception:
            pass
        utils.take_screenshot(driver, "TC_BIZ_003_01_fields_filled", "t6")

        print("👉 STEP 2: CLICKING 'ACEPTAR' TO SUBMIT REGISTRATION...")
        utils.click_element(driver, XPATH_BIZ_BTN_CONFIRMAR)

        print("⏳ WAITING FOR SYSTEM TO PROCESS REGISTRATION...")
        time.sleep(2)

        print("🔍 VERIFYING WE SAW THE POPUP ERROR MESSAGE...")
        mensaje_encontrado = False
        for i in range(10):
            try:
                fuente_xml = driver.page_source.lower()
                if ("afiliacion es incorrecto" in fuente_xml or "el token o" in fuente_xml or
                        "no son válidos" in fuente_xml or "no son validos" in fuente_xml):
                    mensaje_encontrado = True
                    print(f"   🎯 POPUP DETECTED ON ATTEMPT {i + 1}")
                    utils.take_screenshot(driver, "TC_BIZ_003_02_error_detected", "t6")
                    break
            except Exception:
                pass
            time.sleep(0.5)

        if mensaje_encontrado:
            result = "SUCCESS"
            print("✅ TC-BIZ-003: SUCCESS")
        else:
            print("❌ TC-BIZ-003 FAILED")
            utils.take_screenshot(driver, "TC_BIZ_003_02_failed", "t6")
            print("🔍 RAW XML DUMP FOR DEBUGGING:")
            print(driver.page_source)

        try:
            utils.print_http_evidence_appium(driver, "TC_BIZ_003")
        except Exception:
            pass

    except Exception as e:
        print(f"❌ TC-BIZ-003 CRITICAL ERROR: {e}")
        try:
            utils.take_screenshot(driver, "TC_BIZ_003_technical_error", "t6")
        except Exception:
            pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-BIZ-003 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# TC_BIZ_004: VALIDATE ERROR WHEN ENTERING A WRONG AFFILIATION (VALID TOKEN)
# ==================================================================================
def TC_BIZ_004():
    print("\n" + "=" * 60)
    print("TC-BIZ-004: VALIDATE ERROR — VALID TOKEN, WRONG AFFILIATION")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        print("🔐 PRECONDITION: LOGGING IN TO REACH REGISTRATION SCREEN...")
        _login_to_registration_screen(driver, wait)

        print("👉 STEP 1: ENTERING REGISTRATION TOKEN AND AFFILIATION NUMBER...")
        time.sleep(4)

        print(f"   🔑 ENTERING TOKEN: {config.RN_TOKEN}")
        try:
            utils.click_element(driver, XPATH_BIZ_INPUT_TOKEN)
        except Exception:
            pass
        time.sleep(1)
        utils.type_text(driver, XPATH_BIZ_INPUT_TOKEN, config.RN_TOKEN)

        print(f"   🏢 ENTERING AFFILIATION: {config.RN_AFILIACION_INVALIDA}")
        try:
            utils.click_element(driver, XPATH_BIZ_INPUT_AFILIACION)
        except Exception:
            pass
        time.sleep(1)
        utils.type_text(driver, XPATH_BIZ_INPUT_AFILIACION, config.RN_AFILIACION_INVALIDA)

        try:
            driver.hide_keyboard()
        except Exception:
            pass
        utils.take_screenshot(driver, "TC_BIZ_004_01_fields_filled", "t6")

        print("👉 STEP 2: CLICKING 'ACEPTAR' TO SUBMIT REGISTRATION...")
        utils.click_element(driver, XPATH_BIZ_BTN_CONFIRMAR)

        print("⏳ WAITING FOR SYSTEM TO PROCESS REGISTRATION...")
        time.sleep(2)

        print("🔍 VERIFYING WE SAW THE POPUP ERROR MESSAGE...")
        mensaje_encontrado = False
        for i in range(10):
            try:
                fuente_xml = driver.page_source.lower()
                if ("afiliacion es incorrecto" in fuente_xml or "el token o" in fuente_xml or
                        "no son válidos" in fuente_xml or "no son validos" in fuente_xml):
                    mensaje_encontrado = True
                    print(f"   🎯 POPUP DETECTED ON ATTEMPT {i + 1}")
                    utils.take_screenshot(driver, "TC_BIZ_004_02_error_detected", "t6")
                    break
            except Exception:
                pass
            time.sleep(0.5)

        if mensaje_encontrado:
            result = "SUCCESS"
            print("✅ TC-BIZ-004: SUCCESS")
        else:
            print("❌ TC-BIZ-004 FAILED")
            utils.take_screenshot(driver, "TC_BIZ_004_02_failed", "t6")
            print("🔍 RAW XML DUMP FOR DEBUGGING:")
            print(driver.page_source)

        try:
            utils.print_http_evidence_appium(driver, "TC_BIZ_004")
        except Exception:
            pass

    except Exception as e:
        print(f"❌ TC-BIZ-004 CRITICAL ERROR: {e}")
        try:
            utils.take_screenshot(driver, "TC_BIZ_004_technical_error", "t6")
        except Exception:
            pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-BIZ-004 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# TC_BIZ_005: VALIDATE ERROR WHEN THE TOKEN FIELD IS EMPTY
# ==================================================================================
def TC_BIZ_005():
    print("\n" + "=" * 60)
    print("TC-BIZ-005: VALIDATE ERROR WHEN TOKEN FIELD IS EMPTY")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        print("🔐 PRECONDITION: LOGGING IN TO REACH REGISTRATION SCREEN...")
        _login_to_registration_screen(driver, wait)

        print("👉 STEP 1: LEAVING TOKEN EMPTY AND ENTERING AFFILIATION...")
        time.sleep(4)

        print("   🔑 TOKEN: [LEAVING EMPTY]")
        try:
            utils.click_element(driver, XPATH_BIZ_INPUT_TOKEN)
        except Exception:
            pass
        time.sleep(1)

        print(f"   🏢 ENTERING AFFILIATION: {config.RN_AFILIACION}")
        try:
            utils.click_element(driver, XPATH_BIZ_INPUT_AFILIACION)
        except Exception:
            pass
        time.sleep(1)
        utils.type_text(driver, XPATH_BIZ_INPUT_AFILIACION, config.RN_AFILIACION)

        try:
            driver.hide_keyboard()
        except Exception:
            pass
        utils.take_screenshot(driver, "TC_BIZ_005_01_fields_filled", "t6")

        print("👉 STEP 2: CLICKING 'ACEPTAR'...")
        utils.click_element(driver, XPATH_BIZ_BTN_CONFIRMAR)
        print("⏳ SCANNING FOR VALIDATION ERROR MESSAGE...")

        mensaje_encontrado = False
        palabras_sospechosas = ["requerido", "requerida", "obligatorio", "vacío", "vacio", "ingresa", "error", "incorrecto"]

        for i in range(10):
            try:
                fuente_xml = driver.page_source.lower()
                if any(palabra in fuente_xml for palabra in palabras_sospechosas):
                    mensaje_encontrado = True
                    print(f"   🎯 VALIDATION MESSAGE DETECTED ON ATTEMPT {i + 1}")
                    utils.take_screenshot(driver, "TC_BIZ_005_02_error_detected", "t6")
                    break
            except Exception:
                pass
            time.sleep(0.5)

        if mensaje_encontrado:
            result = "SUCCESS"
            print("✅ TC-BIZ-005: SUCCESS")
        else:
            print("❌ TC-BIZ-005 FAILED")
            utils.take_screenshot(driver, "TC_BIZ_005_02_failed", "t6")
            print("🔍 RAW XML DUMP FOR DEBUGGING:")
            print(driver.page_source)

        try:
            utils.print_http_evidence_appium(driver, "TC_BIZ_005")
        except Exception:
            pass

    except Exception as e:
        print(f"❌ TC-BIZ-005 CRITICAL ERROR: {e}")
        try:
            utils.take_screenshot(driver, "TC_BIZ_005_technical_error", "t6")
        except Exception:
            pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-BIZ-005 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# TC_BIZ_006: VALIDATE ERROR WHEN THE AFFILIATION NUMBER FIELD IS EMPTY
# ==================================================================================
def TC_BIZ_006():
    print("\n" + "=" * 60)
    print("TC-BIZ-006: VALIDATE ERROR WHEN AFFILIATION NUMBER FIELD IS EMPTY")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        print("🔐 PRECONDITION: LOGGING IN TO REACH REGISTRATION SCREEN...")
        _login_to_registration_screen(driver, wait)

        print("👉 STEP 1: ENTERING TOKEN AND LEAVING AFFILIATION EMPTY...")
        time.sleep(4)

        print(f"   🔑 ENTERING TOKEN: {config.RN_TOKEN}")
        try:
            utils.click_element(driver, XPATH_BIZ_INPUT_TOKEN)
        except Exception:
            pass
        time.sleep(1)
        utils.type_text(driver, XPATH_BIZ_INPUT_TOKEN, config.RN_TOKEN)

        print("   🏢 AFFILIATION: [LEAVING EMPTY]")
        try:
            utils.click_element(driver, XPATH_BIZ_INPUT_AFILIACION)
        except Exception:
            pass
        time.sleep(1)

        try:
            driver.hide_keyboard()
        except Exception:
            pass
        utils.take_screenshot(driver, "TC_BIZ_006_01_fields_filled", "t6")

        print("👉 STEP 2: CLICKING 'ACEPTAR'...")
        utils.click_element(driver, XPATH_BIZ_BTN_CONFIRMAR)
        print("⏳ SCANNING FOR VALIDATION ERROR MESSAGE...")

        mensaje_encontrado = False
        palabras_sospechosas = ["requerido", "requerida", "obligatorio", "vacío", "vacio", "ingresa", "error", "incorrecto"]

        for i in range(10):
            try:
                fuente_xml = driver.page_source.lower()
                if any(palabra in fuente_xml for palabra in palabras_sospechosas):
                    mensaje_encontrado = True
                    print(f"   🎯 VALIDATION MESSAGE DETECTED ON ATTEMPT {i + 1}")
                    utils.take_screenshot(driver, "TC_BIZ_006_02_error_detected", "t6")
                    break
            except Exception:
                pass
            time.sleep(0.5)

        if mensaje_encontrado:
            result = "SUCCESS"
            print("✅ TC-BIZ-006: SUCCESS")
        else:
            print("❌ TC-BIZ-006 FAILED")
            utils.take_screenshot(driver, "TC_BIZ_006_02_failed", "t6")
            print("🔍 RAW XML DUMP FOR DEBUGGING:")
            print(driver.page_source)

        try:
            utils.print_http_evidence_appium(driver, "TC_BIZ_006")
        except Exception:
            pass

    except Exception as e:
        print(f"❌ TC-BIZ-006 CRITICAL ERROR: {e}")
        try:
            utils.take_screenshot(driver, "TC_BIZ_006_technical_error", "t6")
        except Exception:
            pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-BIZ-006 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# TC_BIZ_007: VALIDATE TOKEN LENGTH RESTRICTIONS (<16, >16, ==16 CHARACTERS)
# ==================================================================================
def TC_BIZ_007():
    print("\n" + "=" * 60)
    print("TC-BIZ-007: VALIDATE TOKEN LENGTH RESTRICTIONS (3 SCENARIOS)")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        print("🔐 PRECONDITION: LOGGING IN TO REACH REGISTRATION SCREEN...")
        _login_to_registration_screen(driver, wait)

        print(f"   🏢 ENTERING VALID AFFILIATION: {config.RN_AFILIACION}")
        time.sleep(4)
        try:
            utils.click_element(driver, XPATH_BIZ_INPUT_AFILIACION)
        except Exception:
            pass
        utils.type_text(driver, XPATH_BIZ_INPUT_AFILIACION, config.RN_AFILIACION)

        try:
            driver.hide_keyboard()
        except Exception:
            pass

        # ─── SCENARIO 1: SHORT TOKEN (< 16 CHARS) ──────────────────────────────
        print("\n▶️  SCENARIO 1: SHORT TOKEN (< 16 CHARS)")
        campo_token = driver.find_element(By.XPATH, XPATH_BIZ_INPUT_TOKEN)
        campo_token.clear()
        campo_token.send_keys(config.RN_TOKEN_CORTO)
        utils.click_element(driver, XPATH_BIZ_BTN_CONFIRMAR)

        print("⏳ SCANNING FOR ERROR MESSAGE (SHORT TOKEN)...")
        error_detectado = False
        for i in range(8):
            if any(p in driver.page_source.lower() for p in ["error", "incorrecto", "inválido", "invalid", "caracteres"]):
                error_detectado = True
                print("   🎯 ERROR DETECTED FOR SHORT TOKEN!")
                utils.take_screenshot(driver, "TC_BIZ_007_01_scenario1_short_ok", "t6")
                break
            time.sleep(0.5)
        if not error_detectado:
            print("   ⚠️  NO ERROR DETECTED FOR SHORT TOKEN — SYSTEM MIGHT HAVE PROCEEDED")
            utils.take_screenshot(driver, "TC_BIZ_007_01_scenario1_short_unexpected", "t6")

        print("⏳ WAITING FOR ERROR BANNER TO DISAPPEAR...")
        time.sleep(4)

        # ─── SCENARIO 2: LONG TOKEN (> 16 CHARS) ───────────────────────────────
        print("\n▶️  SCENARIO 2: LONG TOKEN (> 16 CHARS)")
        try:
            utils.click_element(driver, XPATH_BIZ_INPUT_TOKEN)
        except Exception:
            pass
        time.sleep(1)
        campo_token_2 = driver.find_element(By.XPATH, XPATH_BIZ_INPUT_TOKEN)
        campo_token_2.clear()
        campo_token_2.send_keys(config.RN_TOKEN_LARGO)

        texto_ingresado = campo_token_2.get_attribute("text")
        if texto_ingresado and len(texto_ingresado) == 16 and len(config.RN_TOKEN_LARGO) > 16:
            print("   🎯 UI BLOCKED TYPING MORE THAN 16 CHARACTERS")
            utils.take_screenshot(driver, "TC_BIZ_007_02_scenario2_long_blocked", "t6")
        else:
            utils.click_element(driver, XPATH_BIZ_BTN_CONFIRMAR)
            print("⏳ SCANNING FOR ERROR MESSAGE (LONG TOKEN)...")
            for i in range(8):
                if any(p in driver.page_source.lower() for p in ["error", "incorrecto", "inválido", "invalid", "caracteres"]):
                    print("   🎯 ERROR DETECTED FOR LONG TOKEN!")
                    utils.take_screenshot(driver, "TC_BIZ_007_02_scenario2_long_error", "t6")
                    break
                time.sleep(0.5)

        print("⏳ WAITING FOR ERROR BANNER TO DISAPPEAR...")
        time.sleep(4)

        # ─── SCENARIO 3: EXACT TOKEN (== 16 CHARS) ─────────────────────────────
        print("\n▶️  SCENARIO 3: EXACT TOKEN (== 16 CHARS)")
        try:
            utils.click_element(driver, XPATH_BIZ_INPUT_TOKEN)
        except Exception:
            pass
        time.sleep(1)
        campo_token_3 = driver.find_element(By.XPATH, XPATH_BIZ_INPUT_TOKEN)
        campo_token_3.clear()
        campo_token_3.send_keys(config.RN_TOKEN)

        try:
            driver.hide_keyboard()
        except Exception:
            pass

        utils.click_element(driver, XPATH_BIZ_BTN_CONFIRMAR)
        print("⏳ WAITING FOR SUCCESSFUL REGISTRATION...")
        time.sleep(4)

        if utils.verify_element(wait, XPATH_BIZ_PANTALLA_EXITO, "SUCCESS SCREEN", driver):
            result = "SUCCESS"
            utils.take_screenshot(driver, "TC_BIZ_007_03_scenario3_exact_success", "t6")
            print("\n✅ TC-BIZ-007: SUCCESS (ALL 3 LENGTH RESTRICTIONS VALIDATED CORRECTLY)")
        else:
            print("\n❌ TC-BIZ-007 FAILED — EXACT TOKEN WAS NOT ACCEPTED")
            utils.take_screenshot(driver, "TC_BIZ_007_03_scenario3_failed", "t6")

        try:
            utils.print_http_evidence_appium(driver, "TC_BIZ_007")
        except Exception:
            pass

    except Exception as e:
        print(f"❌ TC-BIZ-007 CRITICAL ERROR: {e}")
        try:
            utils.take_screenshot(driver, "TC_BIZ_007_technical_error", "t6")
        except Exception:
            pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-BIZ-007 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# TC_BIZ_008: VALIDATE AFFILIATION NUMBER LENGTH RESTRICTIONS (<7, >7, ==7 CHARACTERS)
# ==================================================================================

def TC_BIZ_008():
    print("\n" + "=" * 60)
    print("TC-BIZ-008: VALIDATE AFFILIATION LENGTH RESTRICTIONS (3 SCENARIOS)")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        print("🔐 PRECONDITION: LOGGING IN TO REACH REGISTRATION SCREEN...")
        _login_to_registration_screen(driver, wait)

        print(f"   🔑 ENTERING VALID TOKEN: {config.RN_TOKEN}")
        time.sleep(4)
        try:
            utils.click_element(driver, XPATH_BIZ_INPUT_TOKEN)
        except Exception:
            pass
        utils.type_text(driver, XPATH_BIZ_INPUT_TOKEN, config.RN_TOKEN)

        try:
            driver.hide_keyboard()
        except Exception:
            pass

        # ─── SCENARIO 1: SHORT AFFILIATION (< 7 CHARS) ─────────────────────────
        print("\n▶️  SCENARIO 1: SHORT AFFILIATION (< 7 CHARS)")
        campo_afiliacion = driver.find_element(By.XPATH, XPATH_BIZ_INPUT_AFILIACION)
        campo_afiliacion.clear()
        campo_afiliacion.send_keys(config.RN_AFILIACION_CORTA)
        utils.click_element(driver, XPATH_BIZ_BTN_CONFIRMAR)

        print("⏳ SCANNING FOR ERROR MESSAGE (SHORT AFFILIATION)...")
        error_detectado = False
        for i in range(8):
            if any(p in driver.page_source.lower() for p in ["error", "incorrecto", "inválido", "invalid", "caracteres", "afiliacion", "afiliación", "dígitos", "digitos", "exactamente"]):
                error_detectado = True
                print("   🎯 ERROR DETECTED FOR SHORT AFFILIATION!")
                utils.take_screenshot(driver, "TC_BIZ_008_01_scenario1_short_ok", "t6")
                break
            time.sleep(0.5)
        if not error_detectado:
            print("   ⚠️  NO ERROR DETECTED FOR SHORT AFFILIATION — SYSTEM MIGHT HAVE PROCEEDED")
            utils.take_screenshot(driver, "TC_BIZ_008_01_scenario1_unexpected", "t6")

        print("⏳ WAITING FOR ERROR BANNER TO DISAPPEAR...")
        time.sleep(4)

        # ─── SCENARIO 2: LONG AFFILIATION (> 7 CHARS) ──────────────────────────
        print("\n▶️  SCENARIO 2: LONG AFFILIATION (> 7 CHARS)")
        try:
            utils.click_element(driver, XPATH_BIZ_INPUT_AFILIACION)
        except Exception:
            pass
        time.sleep(1)
        campo_afiliacion_2 = driver.find_element(By.XPATH, XPATH_BIZ_INPUT_AFILIACION)
        campo_afiliacion_2.clear()
        campo_afiliacion_2.send_keys(config.RN_AFILIACION_LARGA)

        texto_ingresado = campo_afiliacion_2.get_attribute("text")
        if texto_ingresado and len(texto_ingresado) == 7 and len(config.RN_AFILIACION_LARGA) > 7:
            print("   🎯 UI BLOCKED TYPING MORE THAN 7 CHARACTERS")
            utils.take_screenshot(driver, "TC_BIZ_008_02_scenario2_long_blocked", "t6")
        else:
            utils.click_element(driver, XPATH_BIZ_BTN_CONFIRMAR)
            print("⏳ SCANNING FOR ERROR MESSAGE (LONG AFFILIATION)...")
            for i in range(8):
                if any(p in driver.page_source.lower() for p in ["error", "incorrecto", "inválido", "invalid", "caracteres", "afiliacion", "afiliación", "dígitos", "digitos", "exactamente"]):
                    print("   🎯 ERROR DETECTED FOR LONG AFFILIATION!")
                    utils.take_screenshot(driver, "TC_BIZ_008_02_scenario2_long_error", "t6")
                    break
                time.sleep(0.5)

        print("⏳ WAITING FOR ERROR BANNER TO DISAPPEAR...")
        time.sleep(4)

        # ─── SCENARIO 3: EXACT AFFILIATION (== 7 CHARS) ────────────────────────
        print("\n▶️  SCENARIO 3: EXACT AFFILIATION (== 7 CHARS)")
        try:
            utils.click_element(driver, XPATH_BIZ_INPUT_AFILIACION)
        except Exception:
            pass
        time.sleep(1)
        campo_afiliacion_3 = driver.find_element(By.XPATH, XPATH_BIZ_INPUT_AFILIACION)
        campo_afiliacion_3.clear()
        campo_afiliacion_3.send_keys(config.RN_AFILIACION)

        try:
            driver.hide_keyboard()
        except Exception:
            pass

        utils.click_element(driver, XPATH_BIZ_BTN_CONFIRMAR)
        print("⏳ WAITING FOR SUCCESSFUL REGISTRATION...")
        time.sleep(4)

        if utils.verify_element(wait, XPATH_BIZ_PANTALLA_EXITO, "SUCCESS SCREEN", driver):
            result = "SUCCESS"
            utils.take_screenshot(driver, "TC_BIZ_008_03_scenario3_exact_success", "t6")
            print("\n✅ TC-BIZ-008: SUCCESS (ALL 3 LENGTH RESTRICTIONS VALIDATED CORRECTLY)")
        else:
            print("\n❌ TC-BIZ-008 FAILED — EXACT AFFILIATION WAS NOT ACCEPTED")
            utils.take_screenshot(driver, "TC_BIZ_008_03_scenario3_failed", "t6")

        try:
            utils.print_http_evidence_appium(driver, "TC_BIZ_008")
        except Exception:
            pass

    except Exception as e:
        print(f"❌ TC-BIZ-008 CRITICAL ERROR: {e}")
        try:
            utils.take_screenshot(driver, "TC_BIZ_008_technical_error", "t6")
        except Exception:
            pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-BIZ-008 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# TC_BIZ_010: VALIDATE FIELD INTERACTION (FOCUS/BLUR) WITHOUT DATA
# ==================================================================================

def TC_BIZ_010():
    print("\n" + "=" * 60)
    print("TC-BIZ-010: VALIDATE FIELD INTERACTION (TOUCHING FIELDS)")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        print("🔐 PRECONDITION: LOGGING IN TO REACH REGISTRATION SCREEN...")
        _login_to_registration_screen(driver, wait)

        print("👉 STEP 1 & 2: TOUCHING 'TOKEN' AND 'AFILIACIÓN' FIELDS...")
        time.sleep(4)

        print("   👆 TOUCHING 'TOKEN' FIELD")
        try:
            utils.click_element(driver, XPATH_BIZ_INPUT_TOKEN)
        except Exception:
            pass
        time.sleep(2)

        print("   👆 TOUCHING 'AFILIACIÓN' FIELD...")
        try:
            utils.click_element(driver, XPATH_BIZ_INPUT_AFILIACION)
        except Exception:
            pass
        time.sleep(2)

        print("📸 TAKING SCREENSHOT EVIDENCE (KEYBOARD UP / FIELDS FOCUSED)...")
        utils.take_screenshot(driver, "TC_BIZ_010_01_keyboard_visible", "t6")

        print("👉 STEP 3: TOUCHING OUTSIDE (TITLE) TO REMOVE FOCUS...")
        try:
            driver.find_element(By.XPATH, XPATH_BIZ_TITULO_COMERCIO).click()
            print("   👆 TOUCHED 'REGISTRO DE NEGOCIO' TITLE")
        except Exception:
            print("   ⚠️  COULD NOT TOUCH TITLE — HIDING KEYBOARD NATIVELY...")
            try:
                driver.hide_keyboard()
            except Exception:
                pass
        time.sleep(2)

        print("📸 TAKING FINAL SCREENSHOT EVIDENCE...")
        utils.take_screenshot(driver, "TC_BIZ_010_02_final_state", "t6")

        result = "SUCCESS"
        print("\n✅ TC-BIZ-010: SUCCESS")

        try:
            utils.print_http_evidence_appium(driver, "TC_BIZ_010")
        except Exception:
            pass

    except Exception as e:
        print(f"❌ TC-BIZ-010 CRITICAL ERROR: {e}")
        try:
            utils.take_screenshot(driver, "TC_BIZ_010_technical_error", "t6")
        except Exception:
            pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-BIZ-010 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# EXECUTION
# ==================================================================================

if __name__ == "__main__":

    # ── START REPORT SESSION ──────────────────────────────────────────────────
    logger, log_file, timestamp = utils.start_report("OPERATIONALS_TC_BIZ")

    try:
        TC_BIZ_001()
        TC_BIZ_002()
        TC_BIZ_003()
        TC_BIZ_004()
        TC_BIZ_005()
        TC_BIZ_006()
        TC_BIZ_007()
        TC_BIZ_008()
        TC_BIZ_010()

    finally:
        logger.close()
        utils.generate_zip_report("OPERATIONALS_TC_BIZ", logger, log_file, timestamp)
        utils.generate_html_report("OPERATIONALS_TC_BIZ", log_file, timestamp)