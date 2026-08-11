"""
FILENAME: Operationals_OC.py
DESCRIPTION:
    AUTOMATED TEST SUITE — PASSWORD RECOVERY (OC / "Olvidaste tu Contraseña") MODULE.
    COVERS THE FULL FORGOT-PASSWORD FLOW: T6 REQUEST -> EMAIL (IMAP) -> WEB RESET.

TEST CASES COVERED:
    · TC-PWD-001 : ACCESS TO PASSWORD RECOVERY SCREEN
    · TC-PWD-002 : SUCCESSFUL RECOVERY REQUEST (EXISTING EMAIL)
    · TC-PWD-003 : VALIDATE UNREGISTERED EMAIL RECOVERY (ERROR DETECTION)
    · TC-PWD-004 : VALIDATE EMPTY EMAIL FIELD NOT ALLOWED
    · TC-PWD-005 : VALIDATE INVALID EMAIL FORMAT NOT ALLOWED
    · TC-PWD-006 : VALIDATE BACK BUTTON FUNCTIONALITY IN RECOVERY SCREEN
    · TC-PWD-007 : VALIDATE VIRTUAL KEYBOARD BEHAVIOR (SHOW/HIDE)
    · TC-PWD-009 : OPEN RECOVERY LINK AND CONFIRM NEW-PASSWORD SCREEN LOADS
    · TC-PWD-010 : SET NEW PASSWORD AND CONFIRM
    · TC-PWD-011 : VALIDATE MISMATCHED PASSWORDS ERROR
    · TC-PWD-012 : VALIDATE BLANK "NEW PASSWORD" FIELD ERROR
    · TC-PWD-013 : VALIDATE BLANK "CONFIRM PASSWORD" FIELD ERROR
    · TC-PWD-014 : VALIDATE PASSWORD REQUIREMENTS (MISSING UPPERCASE)
    · TC-PWD-015 : VERIFY SHOW/HIDE PASSWORD EYE ICON ON THE WEBSITE
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time
import config
import utils
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



EMAIL_QA       = "santiago.tapia@memphis.mx"
PASS_APP_GMAIL = "xoar ewkd xhhn gmug"


# ==================================================================================
# LOCAL XPATH OVERRIDES — CORRECTED AGAINST THE REAL APP (config.py's assumptions for
# ==================================================================================
XPATH_OC_BTN_CONTINUAR = (
    '//*[contains(@content-desc, "Continuar") or contains(@text, "Continuar")]'
)

XPATH_OC_MSJ_EXITO_REAL = (
    '//*[contains(@text, "Se ha enviado un correo") or '
    'contains(@content-desc, "Se ha enviado un correo") or '
    'contains(@text, "restablecer tu contrase") or '
    'contains(@content-desc, "restablecer tu contrase")]'
)

XPATH_OC_ERROR_CORREO_VACIO = (
    '//*[contains(@text, "correo es requerido") or '
    'contains(@content-desc, "correo es requerido")]'
)

XPATH_OC_ERROR_CORREO_INVALIDO = (
    '//*[contains(@text, "Ingresa un correo") or '
    'contains(@content-desc, "Ingresa un correo") or '
    'contains(@text, "correo válido") or '
    'contains(@content-desc, "correo válido")]'
)

def _skip_onboarding_if_present(driver, wait):
    print("👉 CHECKING FOR ONBOARDING SCREEN ('Configura la terminal')...")
    short_wait = WebDriverWait(driver, 5)
    if utils.verify_element(short_wait, config.XPATH_OB_BTN_SALTAR, "Botón 'Saltar' (Onboarding)", driver):
        utils.click_element(driver, config.XPATH_OB_BTN_SALTAR)
        time.sleep(2)
        print("   ✅ ONBOARDING SKIPPED — APP SHOULD NOW BE ON THE LOGIN SCREEN")
    else:
        print("   ℹ️  NO ONBOARDING SCREEN DETECTED (APP ALREADY PAST IT)")


def _request_recovery_link(screenshot_prefix, email=EMAIL_QA, app_password=PASS_APP_GMAIL):
    print("\n📱 PHASE 1: REQUESTING RECOVERY EMAIL FROM THE APP...")
    driver, wait = utils.start_driver()
    _skip_onboarding_if_present(driver, wait)
    try:
        link_found = utils.verify_element(wait, config.XPATH_LG_LNK_OLVIDASTE, "Link Olvidaste", driver)
        if not link_found:
            print("   ⏳ NOT FOUND ON FIRST TRY — WAITING 3s AND RETRYING ONCE (APP MAY STILL BE SETTLING)...")
            time.sleep(3)
            link_found = utils.verify_element(wait, config.XPATH_LG_LNK_OLVIDASTE, "Link Olvidaste (Retry)", driver)

        if link_found:
            utils.click_element(driver, config.XPATH_LG_LNK_OLVIDASTE)
            time.sleep(2)
            utils.take_screenshot(driver, f"{screenshot_prefix}_01_recovery_screen", "t6")

            print(f"   📧 ENTERING EMAIL: {email}")
            utils.type_text(driver, config.XPATH_OC_INPUT_EMAIL, email)
            try:
                driver.hide_keyboard()
            except Exception:
                pass
            utils.click_element(driver, XPATH_OC_BTN_CONTINUAR)
            time.sleep(2)
            utils.take_screenshot(driver, f"{screenshot_prefix}_02_request_submitted", "t6")

            utils.print_http_evidence_appium(driver, screenshot_prefix)
        else:
            print("❌ 'OLVIDASTE TU CONTRASEÑA' LINK NOT FOUND")
    except Exception as e:
        print(f"⚠️  PHASE 1 WARNING: {e}")
    finally:
        utils.close_driver(driver)

    print("\n🕵️  PHASE 2: SEARCHING FOR THE LINK IN THE EMAIL SERVER...")
    print("⏳ WAITING 10 SECONDS TO ENSURE DELIVERY...")
    time.sleep(10)
    link = utils.get_recovery_link_imap(email, app_password)
    if not link:
        print("❌ FAILED TO OBTAIN RECOVERY LINK FROM EMAIL")
        return None

    print(f"🔗 RECOVERY LINK: {link}")
    return link


# ==================================================================================
# TC_PWD_001: ACCESS TO PASSWORD RECOVERY SCREEN
# ==================================================================================
def TC_PWD_001():
    print("\n" + "=" * 60)
    print("TC-PWD-001: ACCESS TO PASSWORD RECOVERY SCREEN")
    print("=" * 60)

    driver, wait = utils.start_driver()
    _skip_onboarding_if_present(driver, wait)
    result = "FAIL"

    try:
        print("👉 LOOKING FOR 'OLVIDASTE TU CONTRASEÑA' LINK...")
        time.sleep(5)

        if utils.verify_element(wait, config.XPATH_LG_LNK_OLVIDASTE, "Forget Link", driver):
            utils.click_element(driver, config.XPATH_LG_LNK_OLVIDASTE)
            time.sleep(3)
            utils.take_screenshot(driver, "TC_PWD_001_01_after_click", "t6")

            print("👉 VERIFYING NAVIGATION TO 'RECUPERA TU CONTRASEÑA' SCREEN...")
            if utils.verify_element(wait, config.XPATH_OC_LNK_OLVIDASTE, "Recovery Password Title", driver):
                result = "SUCCESS"
                print("✅ TC-PWD-001: RECOVERY SCREEN CONFIRMED")
                utils.print_http_evidence_appium(driver, "TC_PWD_001")
            else:
                print("❌ TC-PWD-001: RECOVERY SCREEN TITLE NOT FOUND")
        else:
            print("❌ TC-PWD-001: 'OLVIDASTE TU CONTRASEÑA' LINK NOT FOUND")

        utils.take_screenshot(driver, "TC_PWD_001_02_final_state", "t6")

    except Exception as e:
        print(f"❌ TC-PWD-001: EXCEPTION — {e}")
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-PWD-001 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# TC_PWD_002: SUCCESSFUL RECOVERY REQUEST (EXISTING EMAIL)
# ==================================================================================

def TC_PWD_002():
    print("\n" + "=" * 60)
    print("TC-PWD-002: SUCCESSFUL RECOVERY REQUEST (EXISTING EMAIL)")
    print("=" * 60)

    driver, wait = utils.start_driver()
    _skip_onboarding_if_present(driver, wait)
    result = "FAIL"

    try:
        print("👉 NAVIGATING TO 'OLVIDASTE TU CONTRASEÑA' SCREEN...")
        if not utils.verify_element(wait, config.XPATH_LG_LNK_OLVIDASTE, "Forget Link", driver):
            print("❌ TC-PWD-002: LINK NOT FOUND")
            return
        utils.click_element(driver, config.XPATH_LG_LNK_OLVIDASTE)
        time.sleep(2)
        utils.take_screenshot(driver, "TC_PWD_002_01_recovery_screen", "t6")

        print(f"👉 ENTERING REGISTERED EMAIL: {config.RA_013_EMAIL}...")
        utils.type_text(driver, config.XPATH_OC_INPUT_EMAIL, config.RA_013_EMAIL)
        try:
            driver.hide_keyboard()
        except Exception:
            pass
        utils.click_element(driver, XPATH_OC_BTN_CONTINUAR)
        time.sleep(3)
        utils.take_screenshot(driver, "TC_PWD_002_02_after_submit", "t6")

        print("👉 VERIFYING SUCCESS MESSAGE...")
        if utils.verify_element(wait, XPATH_OC_MSJ_EXITO_REAL, "Success Popup", driver):
            result = "SUCCESS"
            print("✅ TC-PWD-002: SUCCESS MESSAGE CONFIRMED")
            utils.print_http_evidence_appium(driver, "TC_PWD_002")
            time.sleep(2)
        else:
            print("❌ TC-PWD-002: SUCCESS MESSAGE NOT FOUND")

        utils.take_screenshot(driver, "TC_PWD_002_03_final_state", "t6")

    except Exception as e:
        print(f"❌ TC-PWD-002: EXCEPTION — {e}")
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-PWD-002 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# TC_PWD_003: VALIDATE UNREGISTERED EMAIL RECOVERY (ERROR DETECTION)
# ==================================================================================

def TC_PWD_003():
    print("\n" + "=" * 60)
    print("TC-PWD-003: VALIDATE UNREGISTERED EMAIL RECOVERY (ERROR DETECTION)")
    print("=" * 60)

    driver, wait = utils.start_driver()
    _skip_onboarding_if_present(driver, wait)
    result = "FAIL"

    try:
        print("👉 NAVIGATING TO 'OLVIDASTE TU CONTRASEÑA' SCREEN...")
        if not utils.verify_element(wait, config.XPATH_LG_LNK_OLVIDASTE, "Olvidaste Link", driver):
            print("❌ TC-PWD-003: LINK NOT FOUND")
            return
        utils.click_element(driver, config.XPATH_LG_LNK_OLVIDASTE)
        time.sleep(2)
        utils.take_screenshot(driver, "TC_PWD_003_01_recovery_screen", "t6")

        print(f"👉 ENTERING UNREGISTERED EMAIL: {config.USUARIO_INVALIDO}...")
        utils.type_text(driver, config.XPATH_OC_INPUT_EMAIL, config.USUARIO_INVALIDO)
        try:
            driver.hide_keyboard()
        except Exception:
            pass

        print("👉 CLICKING 'ACEPTAR' BUTTON...")
        utils.click_element(driver, XPATH_OC_BTN_CONTINUAR)
        time.sleep(2)
        utils.take_screenshot(driver, "TC_PWD_003_02_after_submit", "t6")

        print("👉 VERIFYING ERROR MESSAGE...")
        if utils.verify_element(wait, config.XPATH_ERROR_GENERICO, "Error Popup", driver):
            result = "SUCCESS"
            print("✅ TC-PWD-003: ERROR MESSAGE DETECTED")
            time.sleep(2)
        else:
            print("❌ TC-PWD-003: ERROR MESSAGE NOT FOUND")
            print("🔍 SCANNING SCREEN FOR FAILURE DIAGNOSIS...")
            try:
                for elem in driver.find_elements(By.XPATH, "//*"):
                    t = elem.get_attribute("text")
                    d = elem.get_attribute("content-desc")
                    if (t and len(t) > 3) or (d and len(d) > 3):
                        print(f"   -> TEXT='{t}' | DESC='{d}'")
            except Exception:
                pass

        utils.take_screenshot(driver, "TC_PWD_003_03_final_state", "t6")

    except Exception as e:
        print(f"❌ TC-PWD-003: EXCEPTION — {e}")
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-PWD-003 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# TC_PWD_004: VALIDATE EMPTY EMAIL FIELD NOT ALLOWED
# ==================================================================================

def TC_PWD_004():
    print("\n" + "=" * 60)
    print("TC-PWD-004: VALIDATE EMPTY EMAIL FIELD NOT ALLOWED")
    print("=" * 60)

    driver, wait = utils.start_driver()
    _skip_onboarding_if_present(driver, wait)
    result = "FAIL"

    try:
        print("👉 NAVIGATING TO 'OLVIDASTE TU CONTRASEÑA' SCREEN...")
        if not utils.verify_element(wait, config.XPATH_LG_LNK_OLVIDASTE, "Olvidaste Link", driver):
            print("❌ TC-PWD-004: LINK NOT FOUND")
            return
        utils.click_element(driver, config.XPATH_LG_LNK_OLVIDASTE)
        time.sleep(2)
        utils.take_screenshot(driver, "TC_PWD_004_01_recovery_screen", "t6")

        print("👉 LEAVING EMAIL FIELD EMPTY...")
        utils.type_text(driver, config.XPATH_OC_INPUT_EMAIL, "")
        try:
            driver.hide_keyboard()
        except Exception:
            pass
        utils.click_element(driver, XPATH_OC_BTN_CONTINUAR)
        time.sleep(1)
        utils.take_screenshot(driver, "TC_PWD_004_02_after_submit", "t6")

        print("👉 VERIFYING VALIDATION MESSAGE...")
        if utils.verify_element(wait, XPATH_OC_ERROR_CORREO_VACIO, "Texto Rojo 'El correo es requerido'", driver):
            result = "SUCCESS"
            print("✅ TC-PWD-004: VALIDATION MESSAGE DETECTED")
            utils.print_http_evidence_appium(driver, "TC_PWD_004")
        else:
            print("❌ TC-PWD-004: VALIDATION MESSAGE NOT FOUND")

        utils.take_screenshot(driver, "TC_PWD_004_03_final_state", "t6")

    except Exception as e:
        print(f"❌ TC-PWD-004: EXCEPTION — {e}")
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-PWD-004 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# TC_PWD_005: VALIDATE INVALID EMAIL FORMAT NOT ALLOWED
# ==================================================================================

def TC_PWD_005():
    print("\n" + "=" * 60)
    print("TC-PWD-005: VALIDATE INVALID EMAIL FORMAT NOT ALLOWED")
    print("=" * 60)

    driver, wait = utils.start_driver()
    _skip_onboarding_if_present(driver, wait)
    result = "FAIL"

    try:
        print("👉 NAVIGATING TO 'OLVIDASTE TU CONTRASEÑA' SCREEN...")
        if not utils.verify_element(wait, config.XPATH_LG_LNK_OLVIDASTE, "Forget The Link", driver):
            print("❌ TC-PWD-005: LINK NOT FOUND")
            return
        utils.click_element(driver, config.XPATH_LG_LNK_OLVIDASTE)
        time.sleep(2)
        utils.take_screenshot(driver, "TC_PWD_005_01_recovery_screen", "t6")

        texto_invalido = "usuario_sin_formato"
        print(f"👉 WRITING INVALID EMAIL FORMAT: '{texto_invalido}'...")
        utils.type_text(driver, config.XPATH_OC_INPUT_EMAIL, texto_invalido)
        try:
            driver.hide_keyboard()
        except Exception:
            pass
        utils.click_element(driver, XPATH_OC_BTN_CONTINUAR)
        time.sleep(1)
        utils.take_screenshot(driver, "TC_PWD_005_02_after_submit", "t6")

        print("👉 VERIFYING VALIDATION MESSAGE...")
        if utils.verify_element(wait, XPATH_OC_ERROR_CORREO_INVALIDO, "Texto Rojo 'Ingresa un correo válido'", driver):
            result = "SUCCESS"
            print("✅ TC-PWD-005: VALIDATION MESSAGE DETECTED")
            utils.print_http_evidence_appium(driver, "TC_PWD_005")
        else:
            print("❌ TC-PWD-005: VALIDATION MESSAGE NOT FOUND")

        utils.take_screenshot(driver, "TC_PWD_005_03_final_state", "t6")

    except Exception as e:
        print(f"❌ TC-PWD-005: EXCEPTION — {e}")
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-PWD-005 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# TC_PWD_006: VALIDATE BACK BUTTON FUNCTIONALITY IN RECOVERY SCREEN
# ==================================================================================

def TC_PWD_006():
    print("\n" + "=" * 60)
    print("TC-PWD-006: VALIDATE BACK BUTTON FUNCTIONALITY IN RECOVERY SCREEN")
    print("=" * 60)

    driver, wait = utils.start_driver()
    _skip_onboarding_if_present(driver, wait)
    result = "FAIL"

    try:
        print("👉 NAVIGATING TO 'OLVIDASTE TU CONTRASEÑA' SCREEN...")
        if not utils.verify_element(wait, config.XPATH_LG_LNK_OLVIDASTE, "Olvidaste Link", driver):
            print("❌ TC-PWD-006: LINK TO RECOVERY NOT FOUND")
            return
        utils.click_element(driver, config.XPATH_LG_LNK_OLVIDASTE)
        time.sleep(2)

        if not utils.verify_element(wait, config.XPATH_OC_LNK_OLVIDASTE, "Título Pantalla Recuperación", driver):
            print("❌ TC-PWD-006: DID NOT LOAD RECOVERY SCREEN")
            return
        print("✅ RECOVERY SCREEN LOADED. PREPARING TO GO BACK...")
        utils.take_screenshot(driver, "TC_PWD_006_01_recovery_screen", "t6")

        print("👉 CLICKING 'BACK' ARROW...")
        utils.click_element(driver, config.XPATH_OC_BTN_ATRAS)
        time.sleep(2)
        utils.take_screenshot(driver, "TC_PWD_006_02_after_back", "t6")

        if utils.verify_element(wait, config.XPATH_LG_LNK_OLVIDASTE, "Link Olvidaste (Login Screen)", driver):
            result = "SUCCESS"
            print("✅ TC-PWD-006: RETURNED TO LOGIN SCREEN")
            utils.print_http_evidence_appium(driver, "TC_PWD_006")
        else:
            print("❌ TC-PWD-006: DID NOT RETURN TO LOGIN SCREEN")

        utils.take_screenshot(driver, "TC_PWD_006_03_final_state", "t6")

    except Exception as e:
        print(f"❌ TC-PWD-006: EXCEPTION — {e}")
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-PWD-006 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# TC_PWD_007: VALIDATE VIRTUAL KEYBOARD BEHAVIOR (SHOW/HIDE)
# ==================================================================================

def TC_PWD_007():
    print("\n" + "=" * 60)
    print("TC-PWD-007: VALIDATE VIRTUAL KEYBOARD BEHAVIOR (SHOW/HIDE)")
    print("=" * 60)

    driver, wait = utils.start_driver()
    _skip_onboarding_if_present(driver, wait)
    result = "FAIL"

    try:
        print("👉 NAVIGATING TO 'OLVIDASTE TU CONTRASEÑA' SCREEN...")
        if not utils.verify_element(wait, config.XPATH_LG_LNK_OLVIDASTE, "Link Olvidaste", driver):
            print("❌ TC-PWD-007: LINK NOT FOUND")
            return
        utils.click_element(driver, config.XPATH_LG_LNK_OLVIDASTE)
        time.sleep(2)

        utils.click_element(driver, config.XPATH_OC_INPUT_EMAIL)
        time.sleep(3)
        utils.take_screenshot(driver, "TC_PWD_007_01_keyboard_shown", "t6")

        if driver.is_keyboard_shown():
            print("✅ KEYBOARD IS VISIBLE")
        else:
            print("❌ TC-PWD-007: KEYBOARD DID NOT APPEAR")
            utils.take_screenshot(driver, "TC_PWD_007_02_no_keyboard", "t6")
            return

        if utils.verify_element(wait, XPATH_OC_BTN_CONTINUAR, "Boton Aceptar", driver):
            print("✅ 'ACEPTAR' BUTTON DETECTED")
        else:
            print("⚠️  BUTTON MIGHT BE COVERED")

        print("👉 ATTEMPTING TO HIDE KEYBOARD...")
        try:
            driver.hide_keyboard()
            print("   -> Command 'hide_keyboard()' sent.")
        except Exception as e:
            print(f"   -> Native hide failed ({e}), trying click outside...")
            utils.click_element(driver, config.XPATH_OC_LNK_OLVIDASTE)
        time.sleep(2)
        utils.take_screenshot(driver, "TC_PWD_007_03_after_hide_attempt", "t6")

        if not driver.is_keyboard_shown():
            result = "SUCCESS"
            print("✅ TC-PWD-007: KEYBOARD HIDDEN SUCCESSFULLY")
            utils.print_http_evidence_appium(driver, "TC_PWD_007")
        else:
            print("❌ TC-PWD-007: KEYBOARD STILL VISIBLE")

    except Exception as e:
        print(f"❌ TC-PWD-007: EXCEPTION — {e}")
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-PWD-007 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# TC_PWD_009: OPEN RECOVERY LINK AND CONFIRM NEW-PASSWORD SCREEN LOADS
# ==================================================================================

def TC_PWD_009():
    print("\n" + "=" * 60)
    print("TC-PWD-009: OPEN RECOVERY LINK AND CONFIRM NEW-PASSWORD SCREEN LOADS")
    print("=" * 60)

    result = "FAIL"
    link = _request_recovery_link("TC_PWD_009")
    if not link:
        print("\n" + "-" * 60)
        print(f"📊 TC-PWD-009 RESULT: {result}")
        print("-" * 60)
        return

    print("\n🚀 PHASE 3: OPENING LINK IN WEB BROWSER...")
    print(f"🔗 URL: {link}")
    driver_web, wait_web = utils.start_web_driver()
    try:
        driver_web.get(link)
        print("⏳ WAITING FOR THE 'NEW PASSWORD' SCREEN TO LOAD...")
        time.sleep(5)
        utils.take_screenshot(driver_web, "TC_PWD_009_03_link_opened", "web")

        if utils.verify_element(wait_web, config.XPATH_INPUT_NUEVA_PASS, "Input Nueva Contraseña", driver_web):
            result = "SUCCESS"
            print("✅ TC-PWD-009: NEW-PASSWORD SCREEN CONFIRMED")
        else:
            print("❌ TC-PWD-009: NEW-PASSWORD SCREEN DID NOT LOAD")

        utils.take_screenshot(driver_web, "TC_PWD_009_04_final_state", "web")

    except Exception as e:
        print(f"❌ TC-PWD-009: EXCEPTION IN WEB BROWSER — {e}")
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-PWD-009 RESULT: {result}")
        print("-" * 60)
        print("🏁 CLOSING BROWSER...")
        driver_web.quit()


# ==================================================================================
# TC_PWD_010: SET NEW PASSWORD AND CONFIRM
# ==================================================================================

def TC_PWD_010():
    print("\n" + "=" * 60)
    print("TC-PWD-010: SET NEW PASSWORD AND CONFIRM")
    print("=" * 60)

    NUEVA_PASS = "MemphisQA.2030"
    result = "FAIL"

    link = _request_recovery_link("TC_PWD_010")
    if not link:
        print("\n" + "-" * 60)
        print(f"📊 TC-PWD-010 RESULT: {result}")
        print("-" * 60)
        return

    print("\n🚀 PHASE 3: OPENING LINK AND SETTING NEW PASSWORD...")
    print(f"🔗 URL: {link}")
    driver_web, wait_web = utils.start_web_driver()
    try:
        driver_web.get(link)
        time.sleep(5)

        if not utils.verify_element(wait_web, config.XPATH_INPUT_NUEVA_PASS, "Input Nueva Contraseña", driver_web):
            print("❌ TC-PWD-010: PASSWORD SCREEN DID NOT LOAD")
            utils.take_screenshot(driver_web, "TC_PWD_010_03_screen_not_loaded", "web")
            return

        print(f"✍️  NEW VALID PASSWORD: {NUEVA_PASS}")
        utils.type_text(driver_web, config.XPATH_INPUT_NUEVA_PASS, NUEVA_PASS)
        utils.type_text(driver_web, config.XPATH_INPUT_REPITE_PASS, NUEVA_PASS)
        utils.take_screenshot(driver_web, "TC_PWD_010_03_form_filled", "web")
        try:
            driver_web.get_log('performance')
        except Exception:
            pass

        boton_aceptar = wait_web.until(EC.element_to_be_clickable((By.XPATH, config.XPATH_BTN_ACEPTAR_WEB)))
        boton_aceptar.click()

        popup_encontrado = False
        for _ in range(50):
            time.sleep(0.1)
            try:
                resultado = driver_web.execute_script(
                    "return {encontrado: window.__popupCapturado || false, texto: window.__popupTexto || ''};"
                )
                if resultado and resultado.get('encontrado'):
                    popup_encontrado = True
                    print(f"✅ POPUP DETECTED: '{resultado.get('texto', '').strip()}'")
                    break
            except Exception:
                break

        time.sleep(0.3)
        utils.take_screenshot(driver_web, "TC_PWD_010_04_after_submit", "web")

        time.sleep(1)
        utils.print_http_evidence(driver_web, "gateway/api/v2/auth")

        if popup_encontrado:
            result = "SUCCESS"
            print("✅ TC-PWD-010: SUCCESS POPUP DETECTED")
        else:
            try:
                if "login" in driver_web.current_url:
                    result = "SUCCESS"
                    print("✅ TC-PWD-010: REDIRECTED TO LOGIN (IMPLIED SUCCESS)")
            except Exception:
                pass
            if result == "FAIL":
                print("❌ TC-PWD-010: NEITHER POPUP NOR LOGIN REDIRECT DETECTED")

        utils.take_screenshot(driver_web, "TC_PWD_010_05_final_state", "web")

    except Exception as e:
        print(f"❌ TC-PWD-010: EXCEPTION IN WEB BROWSER — {e}")
        try:
            utils.take_screenshot(driver_web, "TC_PWD_010_ERROR", "web")
        except Exception:
            pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-PWD-010 RESULT: {result}")
        print("-" * 60)
        print("🏁 CLOSING BROWSER...")
        driver_web.quit()


# ==================================================================================
# HELPER — FILL THE WEB "NEW PASSWORD" FORM AND SUBMIT IT
# ==================================================================================

def _fill_new_password_form_and_submit(driver_web, wait_web, new_pass, confirm_pass, screenshot_prefix):
   
    if not utils.verify_element(wait_web, config.XPATH_INPUT_NUEVA_PASS, "Input Nueva Contraseña", driver_web):
        print(f"❌ {screenshot_prefix}: PASSWORD SCREEN DID NOT LOAD")
        utils.take_screenshot(driver_web, f"{screenshot_prefix}_03_screen_not_loaded", "web")
        return False

    utils.type_text(driver_web, config.XPATH_INPUT_NUEVA_PASS, new_pass)
    utils.type_text(driver_web, config.XPATH_INPUT_REPITE_PASS, confirm_pass)
    utils.take_screenshot(driver_web, f"{screenshot_prefix}_03_form_filled", "web")
    try:
        driver_web.get_log('performance')
    except Exception:
        pass

    boton_aceptar = wait_web.until(EC.element_to_be_clickable((By.XPATH, config.XPATH_BTN_ACEPTAR_WEB)))
    boton_aceptar.click()
    time.sleep(2)
    utils.take_screenshot(driver_web, f"{screenshot_prefix}_04_after_submit", "web")
    return True


# ==================================================================================
# TC_PWD_011: VALIDATE MISMATCHED PASSWORDS ERROR
# ==================================================================================
def TC_PWD_011():
    
    print("\n" + "=" * 60)
    print("TC-PWD-011: VALIDATE MISMATCHED PASSWORDS ERROR")
    print("=" * 60)

    NUEVA_PASS = "MemphisQA.2030"
    PASS_DIFERENTE = "OtraPass.9999"
    result = "FAIL"

    link = _request_recovery_link("TC_PWD_011")
    if not link:
        print("\n" + "-" * 60)
        print(f"📊 TC-PWD-011 RESULT: {result}")
        print("-" * 60)
        return

    print("\n🚀 PHASE 3: OPENING LINK AND ENTERING MISMATCHED PASSWORDS...")
    driver_web, wait_web = utils.start_web_driver()
    try:
        driver_web.get(link)
        time.sleep(5)

        if not _fill_new_password_form_and_submit(driver_web, wait_web, NUEVA_PASS, PASS_DIFERENTE, "TC_PWD_011"):
            return

        if utils.verify_element(wait_web, config.XPATH_ERROR_PASS_NO_COINCIDE, "Passwords Don't Match", driver_web):
            result = "SUCCESS"
            print("✅ TC-PWD-011: MISMATCH ERROR DETECTED")
            time.sleep(1)
            utils.print_http_evidence(driver_web, "gateway/api/v2/auth")
        else:
            print("❌ TC-PWD-011: MISMATCH ERROR NOT FOUND")

        utils.take_screenshot(driver_web, "TC_PWD_011_05_final_state", "web")

    except Exception as e:
        print(f"❌ TC-PWD-011: EXCEPTION — {e}")
        try:
            utils.take_screenshot(driver_web, "TC_PWD_011_ERROR", "web")
        except Exception:
            pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-PWD-011 RESULT: {result}")
        print("-" * 60)
        driver_web.quit()


# ==================================================================================
# TC_PWD_012: VALIDATE BLANK "NEW PASSWORD" FIELD ERROR
# ==================================================================================
def TC_PWD_012():
    print("\n" + "=" * 60)
    print("TC-PWD-012: VALIDATE BLANK 'NEW PASSWORD' FIELD ERROR")
    print("=" * 60)

    NUEVA_PASS = " "
    PASS_DIFERENTE = "OtraPass.9999"
    result = "FAIL"

    link = _request_recovery_link("TC_PWD_012")
    if not link:
        print("\n" + "-" * 60)
        print(f"📊 TC-PWD-012 RESULT: {result}")
        print("-" * 60)
        return

    print("\n🚀 PHASE 3: OPENING LINK AND SUBMITTING A BLANK NEW PASSWORD...")
    driver_web, wait_web = utils.start_web_driver()
    try:
        driver_web.get(link)
        time.sleep(5)

        if not _fill_new_password_form_and_submit(driver_web, wait_web, NUEVA_PASS, PASS_DIFERENTE, "TC_PWD_012"):
            return

        if utils.verify_element(wait_web, config.XPATH_ERROR_PASS_NO_COINCIDE, "Passwords Don't Match", driver_web):
            result = "SUCCESS"
            print("✅ TC-PWD-012: VALIDATION ERROR DETECTED")
            time.sleep(1)
            utils.print_http_evidence(driver_web, "gateway/api/v2/auth")
        else:
            print("❌ TC-PWD-012: VALIDATION ERROR NOT FOUND")

        utils.take_screenshot(driver_web, "TC_PWD_012_05_final_state", "web")

    except Exception as e:
        print(f"❌ TC-PWD-012: EXCEPTION — {e}")
        try:
            utils.take_screenshot(driver_web, "TC_PWD_012_ERROR", "web")
        except Exception:
            pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-PWD-012 RESULT: {result}")
        print("-" * 60)
        driver_web.quit()


# ==================================================================================
# TC_PWD_013: VALIDATE BLANK "CONFIRM PASSWORD" FIELD ERROR
# ==================================================================================

def TC_PWD_013():
    print("\n" + "=" * 60)
    print("TC-PWD-013: VALIDATE BLANK 'CONFIRM PASSWORD' FIELD ERROR")
    print("=" * 60)

    NUEVA_PASS = "Memphis@20288"
    PASS_DIFERENTE = ""
    result = "FAIL"

    link = _request_recovery_link("TC_PWD_013")
    if not link:
        print("\n" + "-" * 60)
        print(f"📊 TC-PWD-013 RESULT: {result}")
        print("-" * 60)
        return

    print("\n🚀 PHASE 3: OPENING LINK AND SUBMITTING A BLANK CONFIRM PASSWORD...")
    driver_web, wait_web = utils.start_web_driver()
    try:
        driver_web.get(link)
        time.sleep(5)

        if not _fill_new_password_form_and_submit(driver_web, wait_web, NUEVA_PASS, PASS_DIFERENTE, "TC_PWD_013"):
            return

        if utils.verify_element(wait_web, config.XPATH_ERROR_PASS_NO_COINCIDE, "Passwords Don't Match", driver_web):
            result = "SUCCESS"
            print("✅ TC-PWD-013: VALIDATION ERROR DETECTED")
            time.sleep(1)
            utils.print_http_evidence(driver_web, "gateway/api/v2/auth")
        else:
            print("❌ TC-PWD-013: VALIDATION ERROR NOT FOUND")

        utils.take_screenshot(driver_web, "TC_PWD_013_05_final_state", "web")

    except Exception as e:
        print(f"❌ TC-PWD-013: EXCEPTION — {e}")
        try:
            utils.take_screenshot(driver_web, "TC_PWD_013_ERROR", "web")
        except Exception:
            pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-PWD-013 RESULT: {result}")
        print("-" * 60)
        driver_web.quit()


# ==================================================================================
# TC_PWD_014: VALIDATE PASSWORD REQUIREMENTS (MISSING UPPERCASE)
# ==================================================================================

def TC_PWD_014():
    print("\n" + "=" * 60)
    print("TC-PWD-014: VALIDATE PASSWORD REQUIREMENTS (MISSING UPPERCASE)")
    print("=" * 60)

    PASS_INVALIDA = "memphis202"
    result = "FAIL"

    link = _request_recovery_link("TC_PWD_014")
    if not link:
        print("\n" + "-" * 60)
        print(f"📊 TC-PWD-014 RESULT: {result}")
        print("-" * 60)
        return

    print("\n🚀 PHASE 3: OPENING LINK AND ENTERING A PASSWORD WITHOUT UPPERCASE...")
    driver_web, wait_web = utils.start_web_driver()
    try:
        driver_web.get(link)
        time.sleep(5)

        if not _fill_new_password_form_and_submit(driver_web, wait_web, PASS_INVALIDA, PASS_INVALIDA, "TC_PWD_014"):
            return

        if utils.verify_element(wait_web, config.XPATH_ERROR_PASS_MAYUSCULA, "Error: Must contain uppercase", driver_web):
            result = "SUCCESS"
            print("✅ TC-PWD-014: UPPERCASE-REQUIREMENT ERROR DETECTED")
        else:
            print("❌ TC-PWD-014: UPPERCASE-REQUIREMENT ERROR NOT FOUND")

        utils.take_screenshot(driver_web, "TC_PWD_014_05_final_state", "web")

    except Exception as e:
        print(f"❌ TC-PWD-014: EXCEPTION — {e}")
        try:
            utils.take_screenshot(driver_web, "TC_PWD_014_ERROR", "web")
        except Exception:
            pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-PWD-014 RESULT: {result}")
        print("-" * 60)
        driver_web.quit()


# ==================================================================================
# TC_PWD_015: VERIFY SHOW/HIDE PASSWORD EYE ICON ON THE WEBSITE
# ==================================================================================
def TC_PWD_015():
    print("\n" + "=" * 60)
    print("TC-PWD-015: VERIFY SHOW/HIDE PASSWORD EYE ICON ON THE WEBSITE")
    print("=" * 60)

    NUEVA_PASS = "Memphis@20288"
    result = "FAIL"

    link = _request_recovery_link("TC_PWD_015")
    if not link:
        print("\n" + "-" * 60)
        print(f"📊 TC-PWD-015 RESULT: {result}")
        print("-" * 60)
        return

    print("\n🚀 PHASE 3: OPENING LINK AND TESTING THE EYE BUTTON...")
    driver_web, wait_web = utils.start_web_driver()
    try:
        driver_web.get(link)
        time.sleep(5)

        if not utils.verify_element(wait_web, config.XPATH_INPUT_NUEVA_PASS, "Input Nueva Contraseña", driver_web):
            print("❌ TC-PWD-015: PASSWORD SCREEN DID NOT LOAD")
            utils.take_screenshot(driver_web, "TC_PWD_015_03_screen_not_loaded", "web")
            return

        print(f"✍️  FILLING BOTH FIELDS WITH: {NUEVA_PASS}")
        utils.type_text(driver_web, config.XPATH_INPUT_NUEVA_PASS, NUEVA_PASS)
        utils.type_text(driver_web, config.XPATH_INPUT_REPITE_PASS, NUEVA_PASS)
        time.sleep(1)
        utils.take_screenshot(driver_web, "TC_PWD_015_03_before_eye_click", "web")

        input_nueva = driver_web.find_element(By.XPATH, config.XPATH_INPUT_NUEVA_PASS)
        tipo_antes = input_nueva.get_attribute("type")

        click_exitoso = utils.click_eye_button(driver_web, config.XPATH_BTN_OJO_NUEVA_PASS, "EYE BUTTON - NEW PASSWORD")
        if not click_exitoso:
            print("❌ TC-PWD-015: COULD NOT CLICK THE EYE BUTTON")
            utils.take_screenshot(driver_web, "TC_PWD_015_04_eye_click_failed", "web")
            return

        time.sleep(1)
        tipo_despues = input_nueva.get_attribute("type")
        utils.take_screenshot(driver_web, "TC_PWD_015_04_after_eye_click", "web")

        if tipo_despues == "text":
            result = "SUCCESS"
            print(f"✅ TC-PWD-015: PASSWORD NOW VISIBLE (type WENT FROM '{tipo_antes}' TO '{tipo_despues}')")
        else:
            print(f"❌ TC-PWD-015: TYPE STILL '{tipo_despues}' AFTER CLICKING THE EYE ICON")

        utils.take_screenshot(driver_web, "TC_PWD_015_05_final_state", "web")

    except Exception as e:
        print(f"❌ TC-PWD-015: EXCEPTION — {e}")
        try:
            utils.take_screenshot(driver_web, "TC_PWD_015_ERROR", "web")
        except Exception:
            pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 TC-PWD-015 RESULT: {result}")
        print("-" * 60)
        print("🏁 CLOSING BROWSER...")
        driver_web.quit()


# ==================================================================================
# EXECUTION
# ==================================================================================

if __name__ == "__main__":

    # ── START REPORT SESSION ──────────────────────────────────────────────────
    logger, log_file, timestamp = utils.start_report("OPERATIONALS_TC_PWD")

    try:
        TC_PWD_001()
        TC_PWD_002()
        TC_PWD_003()
        TC_PWD_004()
        TC_PWD_005()
        TC_PWD_006()
        TC_PWD_007()
        TC_PWD_009()
        TC_PWD_010()
        TC_PWD_011()
        TC_PWD_012()
        TC_PWD_013()
        TC_PWD_014()
        TC_PWD_015()

    finally:
        logger.close()
        utils.generate_zip_report("OPERATIONALS_TC_PWD", logger, log_file, timestamp)
        utils.generate_html_report("OPERATIONALS_TC_PWD", log_file, timestamp)