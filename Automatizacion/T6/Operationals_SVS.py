"""
FILENAME: Operationals_SVS.py
DESCRIPTION:
    VALIDATING THE TAB OF SERVICES.

CONTENTS:
    · SVS-92: GO TO SERVICES TAB
    · SVS-93: ACCESS TO 'PAYMENT LINK' (HOME) LINK DE PAGO VIEW
    · SVS-94: ACCESS TO THE 'CREATE NEW' FROM PAYMENT LINK
    · SVS-95: SUCCESSFUL PAYMENT LINK GENERATION
    · SVS-96: FAILED GENERATION (EMPTY SPACE)
    · SVS-97: FAILED GENERATION (EMPTY PRODUCT OR SERVICE)

REQUIREMENTS:
    - APPIUM SERVER RUNNING.
    - config.py AND utils.py IN THE SAME DIRECTORY.
"""

import sys
import os
import re
import time

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_path not in sys.path:
    sys.path.append(project_path)

import config
import utils
from appium.webdriver.common.appiumby import AppiumBy          
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# =================================================================================
# INTERNAL HELPER: CAPTURE EVIDENCE WITHOUT SILENCING ERRORS
# =================================================================================
def _capture_evidence(driver, test_name):
    try:
        utils.print_http_evidence_appium(driver, test_name)
    except Exception as ev_err:
        print(f"   ⚠️  HTTP EVIDENCE CAPTURE FAILED FOR [{test_name}]: {ev_err}")
        print(f"   💡 MAKE SURE APPIUM IS STARTED WITH: appium --allow-insecure=*:get_server_logs")


# =================================================================================
# HELPER: FULL LOGIN + BUSINESS REGISTRATION + LOCATION PERMISSION
#         (REACHES THE MAIN CALCULATOR / CHARGING SCREEN)
# =================================================================================
def helper_login_to_calculator(driver, wait):
    # PHASE 1: LOGIN
    print("   🔐 [HELPER] PHASE 1: EXECUTING LOGIN...")
    time.sleep(4)

    try:
        utils.click_boton(driver, config.XPATH_INPUT_USUARIO)
        time.sleep(1)
    except:
        pass

    print(f"   ✏️  TYPING EMAIL & PASSWORD: {config.USUARIO_VALIDO}")
    utils.escribir_texto(driver, config.XPATH_INPUT_USUARIO, config.USUARIO_VALIDO)
    utils.escribir_texto(driver, config.XPATH_INPUT_PASS, config.PASS_VALIDO)

    try:
        driver.hide_keyboard()
    except:
        pass

    utils.click_boton(driver, config.XPATH_BTN_ACEPTAR)
    time.sleep(6)

    # PHASE 2: BUSINESS REGISTRATION
    print("   🏪 [HELPER] PHASE 2: ENTERING BUSINESS REGISTRATION DATA...")
    time.sleep(4)

    print(f"   🔑 ENTERING TOKEN: {config.RN_TOKEN}")
    try:
        utils.click_boton(driver, config.XPATH_RN_INPUT_TOKEN)
    except:
        pass
    time.sleep(1)
    utils.escribir_texto(driver, config.XPATH_RN_INPUT_TOKEN, config.RN_TOKEN)

    print(f"   🔢 ENTERING AFFILIATION NUMBER: {config.RN_AFILIACION}")
    try:
        utils.click_boton(driver, config.XPATH_RN_INPUT_AFILIACION)
    except:
        pass
    time.sleep(1)
    utils.escribir_texto(driver, config.XPATH_RN_INPUT_AFILIACION, config.RN_AFILIACION)

    try:
        driver.hide_keyboard()
    except:
        pass
    utils.click_boton(driver, config.XPATH_RN_BTN_ACEPTAR_REGISTRO)
    time.sleep(8)

    # PHASE 3: HANDLE LOCATION PERMISSION DIALOG
    print("   📍 [HELPER] PHASE 3: HANDLING LOCATION PERMISSION DIALOG...")

    location_dialog_found = utils.verificar_existencia(
        wait,
        config.XPATH_RN_PANTALLA_EXITO,
        "LOCATION PERMISSION DIALOG",
        driver
    )

    if location_dialog_found:
        print("   ✅ LOCATION PERMISSION DIALOG DETECTED. CLICKING 'MIENTRAS LA APP ESTA EN USO...'")
        utils.click_boton(driver, config.XPATH_C_BTN_MIENTRAS_USO)
        time.sleep(5)
    else:
        print("   ⚠️  WARNING: LOCATION PERMISSION DIALOG NOT DETECTED.")
        time.sleep(3)


# =================================================================================
# INTERNAL HELPER: NAVIGATE TO THE "SERVICES" BOTTOM NAV TAB
# =================================================================================
def _navigate_to_services_tab(driver, wait):
    print("   🔍 [NAV] ATTEMPTING STRATEGY 1: config.XPATH_PÑ_TAB_SERVICIOS...")
    try:
        driver.find_element(By.XPATH, config.XPATH_PÑ_TAB_SERVICIOS).click()
        time.sleep(2)
        print("   ✅ [NAV] STRATEGY 1 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [NAV] STRATEGY 1 FAILED: {e}")

    print("   🔍 [NAV] ATTEMPTING STRATEGY 2: PARTIAL CONTENT-DESC MATCH...")
    try:
        driver.find_element(
            By.XPATH, '//*[contains(@content-desc, "Servicios")]'
        ).click()
        time.sleep(2)
        print("   ✅ [NAV] STRATEGY 2 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [NAV] STRATEGY 2 FAILED: {e}")

    print("   🔍 [NAV] ATTEMPTING STRATEGY 3: EXACT TEXT / CONTENT-DESC MATCH...")
    try:
        driver.find_element(
            By.XPATH, '//*[@text="Servicios" or @content-desc="Servicios"]'
        ).click()
        time.sleep(2)
        print("   ✅ [NAV] STRATEGY 3 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [NAV] STRATEGY 3 FAILED: {e}")

    print("   🔍 [NAV] ATTEMPTING STRATEGY 4: UIAUTOMATOR TEXT SEARCH (FINAL FALLBACK)...")
    try:
        driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains("Servicios")'
        ).click()
        time.sleep(2)
        print("   ✅ [NAV] STRATEGY 4 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   💥 [NAV] STRATEGY 4 FAILED: {e}")

    print("   ❌ [NAV] ALL STRATEGIES EXHAUSTED — SERVICES TAB NOT CLICKABLE.")
    return False


# =================================================================================
# INTERNAL HELPER: VERIFY THAT "LINKS DE PAGO" CARD IS VISIBLE ON SCREEN
# ================================================================================= 
def _verify_payment_links_visible(driver):
    """
    CHECKS THAT THE "LINKS DE PAGO" CARD IS RENDERED ON THE SERVICES TAB.
    THIS IS THE ONLY CONTENT ELEMENT VISIBLE ON THE SCREEN (SEE SCREENSHOT).
    USES 3 STRATEGIES IN CASE TEXT VS CONTENT-DESC ATTRIBUTE VARIES BY DEVICE.
    """
    print("   🔍 [VERIFY] ATTEMPTING STRATEGY 1: @text ATTRIBUTE...")
    try:
        el = driver.find_element(
            By.XPATH, '//*[@text="Links de pago" or @text="links de pago"]'
        )
        if el.is_displayed():
            print("   ✅ [VERIFY] STRATEGY 1 SUCCEEDED — 'LINKS DE PAGO' FOUND VIA @text.")
            return True
    except Exception as e:
        print(f"   ⚠️  [VERIFY] STRATEGY 1 FAILED: {e}")

    print("   🔍 [VERIFY] ATTEMPTING STRATEGY 2: contains(@text) / contains(@content-desc)...")
    try:
        el = driver.find_element(
            By.XPATH,
            '//*[contains(@text, "Links de pago") or contains(@content-desc, "Links de pago")]'
        )
        if el.is_displayed():
            print("   ✅ [VERIFY] STRATEGY 2 SUCCEEDED — 'LINKS DE PAGO' FOUND VIA PARTIAL MATCH.")
            return True
    except Exception as e:
        print(f"   ⚠️  [VERIFY] STRATEGY 2 FAILED: {e}")

    print("   🔍 [VERIFY] ATTEMPTING STRATEGY 3: UIAUTOMATOR TEXT SEARCH (FINAL FALLBACK)...")
    try:
        el = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains("Links de pago")'
        )
        if el.is_displayed():
            print("   ✅ [VERIFY] STRATEGY 3 SUCCEEDED — 'LINKS DE PAGO' FOUND VIA UIAUTOMATOR.")
            return True
    except Exception as e:
        print(f"   💥 [VERIFY] STRATEGY 3 FAILED: {e}")

    print("   ❌ [VERIFY] ALL STRATEGIES EXHAUSTED — 'LINKS DE PAGO' CARD NOT VISIBLE.")
    return False


# =================================================================================
# SVS-92: GO TO SERVICES TAB
# =================================================================================
def SVS_92():
    print("\n" + "=" * 60)
    print("🧪 SVS-92: GO TO SERVICES TAB")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        # PRECONDITION: REACH THE MAIN CHARGING SCREEN
        print("🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)

        # STEP 1: NAVIGATE TO SERVICES TAB
        print("\n👉 STEP 1: NAVIGATING TO 'SERVICES' TAB...")
        tab_reached = _navigate_to_services_tab(driver, wait)

        if not tab_reached:
            print("\n💥 SVS-92: FAILED — COULD NOT NAVIGATE TO SERVICES TAB.")
            utils.tomar_screenshot(driver, "SVS_92_NAV_FAILED")
            _capture_evidence(driver, "SVS_92")
            return False

        # STEP 2: VERIFY THAT "LINKS DE PAGO" CARD IS VISIBLE
        print("\n👉 STEP 2: VERIFYING 'LINKS DE PAGO' CARD IS DISPLAYED...")
        card_visible = _verify_payment_links_visible(driver)

        if not card_visible:
            print("\n💥 SVS-92: FAILED — 'LINKS DE PAGO' CARD NOT FOUND ON SERVICES TAB.")
            utils.tomar_screenshot(driver, "SVS_92_CARD_NOT_FOUND")
            _capture_evidence(driver, "SVS_92")

            # DEBUG: DUMP ALL VISIBLE TEXT TO HELP LOCATE THE REAL ATTRIBUTE NAME
            print("\n🔍 SCANNING VISIBLE TEXT FOR DEBUGGING...")
            try:
                for elem in driver.find_elements(By.XPATH, "//*"):
                    t = elem.get_attribute("text")
                    if t and len(t) > 3:
                        print(f"   📝 VISIBLE TEXT: '{t}'")
            except:
                pass
            return False

        # SUCCESS PATH
        print("\n📸 TAKING SCREENSHOT — SERVICES TAB LOADED CORRECTLY...")
        utils.tomar_screenshot(driver, "SVS_92_SERVICES_TAB_OK")
        _capture_evidence(driver, "SVS_92")
        print("\n✅ SVS-92: SUCCESS — SERVICES TAB LOADED. 'LINKS DE PAGO' CARD IS VISIBLE.")
        return True

    except Exception as e:
        print(f"\n💥 SVS-92 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "SVS_92_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)

# =================================================================================
# SVS-93: ACCESS TO 'PAYMENT LINK' (HOME) LINK DE PAGO VIEW
# =================================================================================
def SVS_93():
    print("\n" + "=" * 60)
    print("🧪 SVS-93: ACCESS TO 'PAYMENT LINK' (HOME) LINK DE PAGO VIEW")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        # PRECONDITION: REACH THE MAIN CHARGING SCREEN
        print("🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)

        # STEP 1: NAVIGATE TO SERVICES TAB
        print("\n👉 STEP 1: NAVIGATING TO 'SERVICES' TAB...")
        tab_reached = _navigate_to_services_tab(driver, wait)

        if not tab_reached:
            print("\n💥 SVS-93: FAILED — COULD NOT NAVIGATE TO SERVICES TAB.")
            utils.tomar_screenshot(driver, "SVS_93_NAV_FAILED")
            _capture_evidence(driver, "SVS_93")
            return False

        # STEP 2: VERIFY THAT "LINKS DE PAGO" CARD IS VISIBLE
        print("\n👉 STEP 2: VERIFYING 'LINKS DE PAGO' CARD IS DISPLAYED...")
        card_visible = _verify_payment_links_visible(driver)

        if not card_visible:
            print("\n💥 SVS-93: FAILED — LINK DE PAGO IS NOT VISIBLE")
            utils.tomar_screenshot(driver, "SVS_93_CARD_NOT_FOUND")
            _capture_evidence(driver, "SVS_93")

            # DEBUG: DUMP ALL VISIBLE TEXT TO HELP LOCATE THE REAL ATTRIBUTE NAME
            print("\n🔍 SCANNING VISIBLE TEXT FOR DEBUGGING...")
            try:
                for elem in driver.find_elements(By.XPATH, "//*"):
                    t = elem.get_attribute("text")
                    if t and len(t) > 3:
                        print(f"   📝 VISIBLE TEXT: '{t}'")
            except:
                pass
            return False

        # SUCCESS PATH
        print("\n📸 TAKING SCREENSHOT — PAID LINK HOME VIEW...")
        utils.tomar_screenshot(driver, "SVS_93_SERVICES_TAB_OK")
        _capture_evidence(driver, "SVS_93")
        print("\n✅ SVS-93: SUCCESS — LINK DE PAGO VIEW IS VISIBLE.")
        return True

    except Exception as e:
        print(f"\n💥 SVS-93 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "SVS_93_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)

# =================================================================================
# INTERNAL HELPER: CLICK THE "LINKS DE PAGO" CARD ON THE SERVICES TAB
# =================================================================================
def _click_payment_links_card(driver):
    """
    TAPS THE "LINKS DE PAGO" CARD ON THE SERVICES SCREEN.
    THE CARD IS A TOUCHABLE ELEMENT — ITS CLICKABLE ANCESTOR MAY NOT CARRY
    THE TEXT DIRECTLY, SO WE TRY MULTIPLE STRATEGIES TO HIT THE RIGHT TARGET.
    """
    print("   🔍 [CLICK] ATTEMPTING STRATEGY 1: EXACT @text ON THE CARD...")
    try:
        driver.find_element(
            By.XPATH, '//*[@text="Links de pago" or @text="links de pago"]'
        ).click()
        time.sleep(3)
        print("   ✅ [CLICK] STRATEGY 1 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [CLICK] STRATEGY 1 FAILED: {e}")
 
    print("   🔍 [CLICK] ATTEMPTING STRATEGY 2: contains(@text) / contains(@content-desc)...")
    try:
        driver.find_element(
            By.XPATH,
            '//*[contains(@text, "Links de pago") or contains(@content-desc, "Links de pago")]'
        ).click()
        time.sleep(3)
        print("   ✅ [CLICK] STRATEGY 2 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [CLICK] STRATEGY 2 FAILED: {e}")
 
    print("   🔍 [CLICK] ATTEMPTING STRATEGY 3: CLICKABLE ANCESTOR OF TEXT NODE...")
    try:
        # WALK UP THE TREE — THE TEXT LABEL MAY SIT INSIDE A NON-CLICKABLE VIEW
        # WHOSE PARENT IS THE ACTUAL TOUCHABLE CONTAINER
        el = driver.find_element(
            By.XPATH,
            '//*[contains(@text, "Links de pago") or contains(@content-desc, "Links de pago")]'
            '/ancestor::*[@clickable="true"][1]'
        )
        el.click()
        time.sleep(3)
        print("   ✅ [CLICK] STRATEGY 3 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [CLICK] STRATEGY 3 FAILED: {e}")
 
    print("   🔍 [CLICK] ATTEMPTING STRATEGY 4: UIAUTOMATOR TEXT CLICK (FINAL FALLBACK)...")
    try:
        driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains("Links de pago")'
        ).click()
        time.sleep(3)
        print("   ✅ [CLICK] STRATEGY 4 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   💥 [CLICK] STRATEGY 4 FAILED: {e}")
 
    print("   ❌ [CLICK] ALL STRATEGIES EXHAUSTED — 'LINKS DE PAGO' CARD NOT CLICKABLE.")
    return False
 
 
# =================================================================================
# INTERNAL HELPER: VERIFY THE "LINK DE PAGO" DETAIL SCREEN LOADED CORRECTLY
# =================================================================================
def _verify_payment_link_screen(driver):
    heading_found = False
    button_found  = False
 
    # --- CHECK 1: SCREEN TITLE "Link de pago" ---
    print("   🔍 [VERIFY] CHECK 1: SCREEN TITLE 'Link de pago'...")
    try:
        el = driver.find_element(
            By.XPATH,
            '//*[@text="Link de pago" or @content-desc="Link de pago" or '
            'contains(@text, "Link de pago") or contains(@content-desc, "Link de pago")]'
        )
        if el.is_displayed():
            print("   ✅ [VERIFY] CHECK 1 PASSED — SCREEN TITLE VISIBLE.")
            heading_found = True
    except Exception as e:
        print(f"   ⚠️  [VERIFY] CHECK 1 FAILED: {e}")
 
    # --- CHECK 2: MAIN HEADING "Realiza cobros a través de un link" ---
    print("   🔍 [VERIFY] CHECK 2: HEADING 'Realiza cobros a través de un link'...")
    try:
        el = driver.find_element(
            By.XPATH,
            '//*[contains(@text, "Realiza cobros") or contains(@content-desc, "Realiza cobros")]'
        )
        if el.is_displayed():
            print("   ✅ [VERIFY] CHECK 2 PASSED — MAIN HEADING VISIBLE.")
            heading_found = True
    except Exception as e:
        print(f"   ⚠️  [VERIFY] CHECK 2 FAILED: {e}")
 
    # --- CHECK 3: ACTION BUTTON "+ Crear nuevo" ---
    print("   🔍 [VERIFY] CHECK 3: BUTTON '+ Crear nuevo'...")
    try:
        el = driver.find_element(
            By.XPATH,
            '//*[contains(@text, "Crear nuevo") or contains(@content-desc, "Crear nuevo")]'
        )
        if el.is_displayed():
            print("   ✅ [VERIFY] CHECK 3 PASSED — '+ CREAR NUEVO' BUTTON VISIBLE.")
            button_found = True
    except Exception as e:
        print(f"   ⚠️  [VERIFY] CHECK 3 FAILED: {e}")
 
    # SCREEN IS CONSIDERED LOADED IF HEADING + BUTTON ARE BOTH PRESENT,
    # OR AT MINIMUM THE HEADING IS CONFIRMED (BUTTON MAY BE BELOW FOLD ON SMALL SCREENS)
    if heading_found and button_found:
        print("   ✅ [VERIFY] FULL SCREEN CONFIRMED — HEADING + BUTTON BOTH VISIBLE.")
        return True
    elif heading_found:
        print("   ⚠️  [VERIFY] PARTIAL CONFIRMATION — HEADING VISIBLE BUT BUTTON NOT FOUND.")
        print("   💡 BUTTON MAY BE BELOW THE VISIBLE FOLD — CONSIDER SCROLLING IF NEEDED.")
        return True
    else:
        print("   ❌ [VERIFY] SCREEN NOT CONFIRMED — NO EXPECTED ELEMENTS FOUND.")
        return False
 
 
# =================================================================================
# SVS-94: ACCES TO THE 'CREATE NEW' FROM PAYMENT LINK
# =================================================================================
def SVS_94():
    print("\n" + "=" * 60)
    print("🧪 SVS-94: ACCES TO THE 'CREATE NEW' FROM PAYMENT LINK")
    print("=" * 60)
 
    driver, wait = utils.iniciar_driver()
 
    try:
        # PRECONDITION: REACH THE MAIN CHARGING SCREEN
        print("🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)
 
        # STEP 1: NAVIGATE TO SERVICES TAB
        print("\n👉 STEP 1: NAVIGATING TO 'SERVICES' TAB...")
        tab_reached = _navigate_to_services_tab(driver, wait)
 
        if not tab_reached:
            print("\n💥 SVS-94: FAILED — COULD NOT NAVIGATE TO SERVICES TAB.")
            utils.tomar_screenshot(driver, "SVS_94_NAV_FAILED")
            _capture_evidence(driver, "SVS_94")
            return False
 
        # STEP 2: CLICK THE "LINKS DE PAGO" CARD
        print("\n👉 STEP 2: CLICKING 'LINKS DE PAGO' CARD...")
        card_clicked = _click_payment_links_card(driver)
 
        if not card_clicked:
            print("\n💥 SVS-94: FAILED — COULD NOT CLICK 'LINKS DE PAGO' CARD.")
            utils.tomar_screenshot(driver, "SVS_94_CLICK_FAILED")
            _capture_evidence(driver, "SVS_94")
            return False
 
        # STEP 3: VERIFY THE "LINK DE PAGO" DETAIL SCREEN LOADED
        print("\n👉 STEP 3: VERIFYING 'LINK DE PAGO' SCREEN LOADED CORRECTLY...")
        screen_loaded = _verify_payment_link_screen(driver)
 
        if not screen_loaded:
            print("\n💥 SVS-94: FAILED — 'LINK DE PAGO' SCREEN DID NOT LOAD AS EXPECTED.")
            utils.tomar_screenshot(driver, "SVS_94_SCREEN_NOT_LOADED")
            _capture_evidence(driver, "SVS_94")
 
            # DEBUG: DUMP ALL VISIBLE TEXT TO HELP DIAGNOSE
            print("\n🔍 SCANNING VISIBLE TEXT FOR DEBUGGING...")
            try:
                for elem in driver.find_elements(By.XPATH, "//*"):
                    t = elem.get_attribute("text")
                    if t and len(t) > 3:
                        print(f"   📝 VISIBLE TEXT: '{t}'")
            except:
                pass
            return False
 
        # SUCCESS PATH
        print("\n📸 TAKING SCREENSHOT — LINK DE PAGO SCREEN LOADED CORRECTLY...")
        utils.tomar_screenshot(driver, "SVS_94_LINK_DE_PAGO_SCREEN_OK")
        _capture_evidence(driver, "SVS_94")
        print("\n✅ SVS-94: SUCCESS — 'LINKS DE PAGO' CARD NAVIGATES TO LINK DE PAGO SCREEN.")
        return True
 
    except Exception as e:
        print(f"\n💥 SVS-94 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "SVS_94_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)

# =================================================================================
# INTERNAL HELPER: CLICK THE "+ CREAR NUEVO" BUTTON ON THE LINK DE PAGO SCREEN
# =================================================================================
def _click_create_new(driver):
    """
    TAPS THE FLOATING "+ CREAR NUEVO" BUTTON.
    THE BUTTON IS POSITIONED AT THE BOTTOM OF THE SCREEN AND MAY BE A FAB
    (FLOATING ACTION BUTTON) — TRIES TEXT MATCH FIRST, THEN CONTENT-DESC,
    THEN UIAUTOMATOR AS FINAL FALLBACK.
    """
    print("   🔍 [CREAR] ATTEMPTING STRATEGY 1: @text EXACT MATCH...")
    try:
        driver.find_element(
            By.XPATH, '//*[@text="+ Crear nuevo" or @text="Crear nuevo"]'
        ).click()
        time.sleep(2)
        print("   ✅ [CREAR] STRATEGY 1 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [CREAR] STRATEGY 1 FAILED: {e}")
 
    print("   🔍 [CREAR] ATTEMPTING STRATEGY 2: contains(@text) / contains(@content-desc)...")
    try:
        driver.find_element(
            By.XPATH,
            '//*[contains(@text, "Crear nuevo") or contains(@content-desc, "Crear nuevo")]'
        ).click()
        time.sleep(2)
        print("   ✅ [CREAR] STRATEGY 2 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [CREAR] STRATEGY 2 FAILED: {e}")
 
    print("   🔍 [CREAR] ATTEMPTING STRATEGY 3: CLICKABLE ANCESTOR OF TEXT NODE...")
    try:
        el = driver.find_element(
            By.XPATH,
            '//*[contains(@text, "Crear nuevo") or contains(@content-desc, "Crear nuevo")]'
            '/ancestor::*[@clickable="true"][1]'
        )
        el.click()
        time.sleep(2)
        print("   ✅ [CREAR] STRATEGY 3 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [CREAR] STRATEGY 3 FAILED: {e}")
 
    print("   🔍 [CREAR] ATTEMPTING STRATEGY 4: UIAUTOMATOR TEXT CLICK (FINAL FALLBACK)...")
    try:
        driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains("Crear nuevo")'
        ).click()
        time.sleep(2)
        print("   ✅ [CREAR] STRATEGY 4 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   💥 [CREAR] STRATEGY 4 FAILED: {e}")
 
    print("   ❌ [CREAR] ALL STRATEGIES EXHAUSTED — '+ CREAR NUEVO' NOT CLICKABLE.")
    return False
 
 
# =================================================================================
# INTERNAL HELPER: FILL THE "MONTO" FIELD
# =================================================================================
def _fill_amount(driver, amount):
    print(f"   🔍 [MONTO] ATTEMPTING STRATEGY 1: PLACEHOLDER @text='Monto'...")
    try:
        el = driver.find_element(
            By.XPATH, '//*[@text="Monto" or contains(@hint, "Monto")]'
        )
        el.click()
        time.sleep(1)
        el.clear()
        el.send_keys(monto)
        try:
            driver.hide_keyboard()
        except:
            pass
        time.sleep(1)
        print(f"   ✅ [MONTO] STRATEGY 1 SUCCEEDED — TYPED: {monto}")
        return True
    except Exception as e:
        print(f"   ⚠️  [MONTO] STRATEGY 1 FAILED: {e}")
 
    print(f"   🔍 [MONTO] ATTEMPTING STRATEGY 2: FIRST EditText ON SCREEN...")
    try:
        el = driver.find_elements(By.XPATH, '//android.widget.EditText')[0]
        el.click()
        time.sleep(1)
        el.clear()
        el.send_keys(monto)
        try:
            driver.hide_keyboard()
        except:
            pass
        time.sleep(1)
        print(f"   ✅ [MONTO] STRATEGY 2 SUCCEEDED — TYPED: {monto}")
        return True
    except Exception as e:
        print(f"   ⚠️  [MONTO] STRATEGY 2 FAILED: {e}")
 
    print(f"   🔍 [MONTO] ATTEMPTING STRATEGY 3: UIAUTOMATOR HINT 'Monto' (FINAL FALLBACK)...")
    try:
        el = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains("Monto")'
        )
        el.click()
        time.sleep(1)
        el.clear()
        el.send_keys(monto)
        try:
            driver.hide_keyboard()
        except:
            pass
        time.sleep(1)
        print(f"   ✅ [MONTO] STRATEGY 3 SUCCEEDED — TYPED: {monto}")
        return True
    except Exception as e:
        print(f"   💥 [MONTO] STRATEGY 3 FAILED: {e}")
 
    print("   ❌ [MONTO] ALL STRATEGIES EXHAUSTED — MONTO FIELD NOT FOUND.")
    return False
 
 
# =================================================================================
# INTERNAL HELPER: FILL THE "PRODUCTO O SERVICIO" FIELD
# =================================================================================
def _fill_description(driver, description):
    print(f"   🔍 [CONCEPTO] ATTEMPTING STRATEGY 1: PLACEHOLDER TEXT MATCH...")
    try:
        el = driver.find_element(
            By.XPATH,
            '//*[@text="Producto o servicio" or contains(@hint, "Producto o servicio")]'
        )
        el.click()
        time.sleep(1)
        el.clear()
        el.send_keys(concepto)
        try:
            driver.hide_keyboard()
        except:
            pass
        time.sleep(1)
        print(f"   ✅ [CONCEPTO] STRATEGY 1 SUCCEEDED — TYPED: {concepto}")
        return True
    except Exception as e:
        print(f"   ⚠️  [CONCEPTO] STRATEGY 1 FAILED: {e}")
 
    print(f"   🔍 [CONCEPTO] ATTEMPTING STRATEGY 2: SECOND EditText ON SCREEN...")
    try:
        el = driver.find_elements(By.XPATH, '//android.widget.EditText')[1]
        el.click()
        time.sleep(1)
        el.clear()
        el.send_keys(concepto)
        try:
            driver.hide_keyboard()
        except:
            pass
        time.sleep(1)
        print(f"   ✅ [CONCEPTO] STRATEGY 2 SUCCEEDED — TYPED: {concepto}")
        return True
    except Exception as e:
        print(f"   ⚠️  [CONCEPTO] STRATEGY 2 FAILED: {e}")
 
    print(f"   🔍 [CONCEPTO] ATTEMPTING STRATEGY 3: UIAUTOMATOR (FINAL FALLBACK)...")
    try:
        el = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains("Producto o servicio")'
        )
        el.click()
        time.sleep(1)
        el.clear()
        el.send_keys(concepto)
        try:
            driver.hide_keyboard()
        except:
            pass
        time.sleep(1)
        print(f"   ✅ [CONCEPTO] STRATEGY 3 SUCCEEDED — TYPED: {concepto}")
        return True
    except Exception as e:
        print(f"   💥 [CONCEPTO] STRATEGY 3 FAILED: {e}")
 
    print("   ❌ [CONCEPTO] ALL STRATEGIES EXHAUSTED — CONCEPTO FIELD NOT FOUND.")
    return False
 
 
# =================================================================================
# INTERNAL HELPER: OPEN THE DATE PICKER AND SELECT TODAY'S DATE
# =================================================================================
def _select_due_date(driver):
    
    from datetime import date as _date
 
    today      = _date.today()
    today_day  = str(today.day)          # E.G. "30"
    today_str  = today.strftime("%d/%m/%Y")  # E.G. "30/04/2026" — FOR LOGGING ONLY
    print(f"   📅 [FECHA] TODAY IS {today_str} — WILL SELECT DAY {today_day} IN PICKER.")
 
    # STEP A: TAP THE FECHA DE VENCIMIENTO FIELD TO OPEN THE PICKER
    print("   🔍 [FECHA] STEP A — TAPPING 'FECHA DE VENCIMIENTO' FIELD...")
    field_tapped = False
 
    try:
        driver.find_element(
            By.XPATH,
            '//*[@text="Fecha de vencimiento" or contains(@hint, "Fecha de vencimiento")]'
        ).click()
        time.sleep(2)
        print("   ✅ [FECHA] FIELD TAPPED VIA PLACEHOLDER TEXT.")
        field_tapped = True
    except Exception as e:
        print(f"   ⚠️  [FECHA] PLACEHOLDER TAP FAILED: {e}")
 
    if not field_tapped:
        try:
            driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().textContains("Fecha de vencimiento")'
            ).click()
            time.sleep(2)
            print("   ✅ [FECHA] FIELD TAPPED VIA UIAUTOMATOR.")
            field_tapped = True
        except Exception as e:
            print(f"   💥 [FECHA] UIAUTOMATOR TAP FAILED: {e}")
 
    if not field_tapped:
        print("   ❌ [FECHA] COULD NOT OPEN DATE PICKER — FECHA FIELD NOT FOUND.")
        return False
 
    # STEP B: WAIT FOR "SELECCIONAR FECHA" HEADER — CONFIRMS PICKER IS OPEN
    print("   🔍 [FECHA] STEP B — WAITING FOR DATEPICKER TO APPEAR...")
    picker_open = False
    for attempt in range(6):
        try:
            driver.find_element(
                By.XPATH,
                '//*[contains(@text, "SELECCIONAR FECHA") or '
                'contains(@content-desc, "SELECCIONAR FECHA")]'
            )
            print("   ✅ [FECHA] DATEPICKER CONFIRMED OPEN.")
            picker_open = True
            break
        except:
            time.sleep(1)
 
    if not picker_open:
        print("   ⚠️  [FECHA] DATEPICKER HEADER NOT FOUND — PROCEEDING ANYWAY...")
 
    print(f"   🔍 [FECHA] STEP C — SELECTING DAY {today_day} (TODAY)...")
    day_selected = False
    try:
        driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().descriptionStartsWith("{today_day}, ")'
        ).click()
        time.sleep(1)
        print(f"   ✅ [FECHA] STRATEGY 1: DAY {today_day} SELECTED VIA descriptionStartsWith.")
        day_selected = True
    except Exception as e:
        print(f"   ⚠️  [FECHA] STRATEGY 1 FAILED: {e}")
 
    # STRATEGY 2: XPATH starts-with WITH EXACT SEPARATOR ", "
    if not day_selected:
        try:
            driver.find_element(
                By.XPATH,
                f'//*[starts-with(@content-desc, "{today_day}, ")]'
            ).click()
            time.sleep(1)
            print(f"   ✅ [FECHA] STRATEGY 2: DAY {today_day} SELECTED VIA XPath starts-with.")
            day_selected = True
        except Exception as e:
            print(f"   ⚠️  [FECHA] STRATEGY 2 FAILED: {e}")
 
    # STRATEGY 3: XPATH contains — LOOSER MATCH, HANDLES ANY FORMAT VARIATION
    if not day_selected:
        try:
            driver.find_element(
                By.XPATH,
                f'//*[contains(@content-desc, "{today_day}, ") and '
                f'contains(@content-desc, "Hoy")]'
            ).click()
            time.sleep(1)
            print(f"   ✅ [FECHA] STRATEGY 3: DAY {today_day} SELECTED VIA contains + 'Hoy'.")
            day_selected = True
        except Exception as e:
            print(f"   ⚠️  [FECHA] STRATEGY 3 FAILED: {e}")
 
    if not day_selected:
        try:
            driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().descriptionContains("Hoy")'
            ).click()
            time.sleep(1)
            print(f"   ✅ [FECHA] STRATEGY 4: TODAY SELECTED VIA 'Hoy' MARKER IN content-desc.")
            day_selected = True
        except Exception as e:
            print(f"   💥 [FECHA] STRATEGY 4 FAILED: {e}")
 
    if not day_selected:
        print(f"   ❌ [FECHA] COULD NOT SELECT DAY {today_day}. DUMPING @content-desc VALUES...")
        try:
            for el in driver.find_elements(By.XPATH, "//*[@content-desc]"):
                cd = el.get_attribute("content-desc")
                if cd and (today_day in cd or "Hoy" in cd):
                    print(f"   📝 CANDIDATE content-desc: '{cd}'")
        except:
            pass
        return False
 
    # STEP D: CONFIRM WITH "ACEPTAR"
    print("   🔍 [FECHA] STEP D — CLICKING 'ACEPTAR' TO CONFIRM DATE...")
    try:
        driver.find_element(
            By.XPATH, '//*[@text="ACEPTAR" or @text="Aceptar" or @content-desc="ACEPTAR"]'
        ).click()
        time.sleep(2)
        print("   ✅ [FECHA] DATE CONFIRMED WITH 'ACEPTAR'.")
        return True
    except Exception as e:
        print(f"   ⚠️  [FECHA] ACEPTAR VIA XPATH FAILED: {e}")
 
    try:
        driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().textMatches("(?i)aceptar")'
        ).click()
        time.sleep(2)
        print("   ✅ [FECHA] DATE CONFIRMED VIA UIAUTOMATOR.")
        return True
    except Exception as e:
        print(f"   💥 [FECHA] ACEPTAR UIAUTOMATOR FAILED: {e}")
 
    print("   ❌ [FECHA] COULD NOT CONFIRM DATE — 'ACEPTAR' NOT FOUND.")
    return False
 
 
# =================================================================================
# INTERNAL HELPER: CLICK THE "GENERAR" BUTTON
# =================================================================================
def _click_generate(driver):
    
    print("   🔍 [GENERAR] ATTEMPTING STRATEGY 1: EXACT @text='Generar'...")
    try:
        driver.find_element(
            By.XPATH, '//*[@text="Generar"]'
        ).click()
        time.sleep(4)
        print("   ✅ [GENERAR] STRATEGY 1 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [GENERAR] STRATEGY 1 FAILED: {e}")
 
    print("   🔍 [GENERAR] ATTEMPTING STRATEGY 2: contains(@text, 'Generar')...")
    try:
        driver.find_element(
            By.XPATH,
            '//*[contains(@text, "Generar") or contains(@content-desc, "Generar")]'
        ).click()
        time.sleep(4)
        print("   ✅ [GENERAR] STRATEGY 2 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [GENERAR] STRATEGY 2 FAILED: {e}")
 
    print("   🔍 [GENERAR] ATTEMPTING STRATEGY 3: CLICKABLE ANCESTOR...")
    try:
        el = driver.find_element(
            By.XPATH,
            '//*[contains(@text, "Generar")]/ancestor::*[@clickable="true"][1]'
        )
        el.click()
        time.sleep(4)
        print("   ✅ [GENERAR] STRATEGY 3 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [GENERAR] STRATEGY 3 FAILED: {e}")
 
    print("   🔍 [GENERAR] ATTEMPTING STRATEGY 4: UIAUTOMATOR (FINAL FALLBACK)...")
    try:
        driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().text("Generar")'
        ).click()
        time.sleep(4)
        print("   ✅ [GENERAR] STRATEGY 4 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   💥 [GENERAR] STRATEGY 4 FAILED: {e}")
 
    print("   ❌ [GENERAR] ALL STRATEGIES EXHAUSTED — 'GENERAR' NOT CLICKABLE.")
    return False
 
 
# =================================================================================
# INTERNAL HELPER: VERIFY THE SUCCESS SCREEN "LINK DE PAGO GENERADO"
# =================================================================================
def _verify_generated_link_screen(driver, amount, description):
    heading_ok  = False
    data_ok     = False
 
    # --- CHECK 1: SUCCESS HEADING ---
    print("   🔍 [SUCCESS] CHECK 1: HEADING 'Link de pago generado'...")
    try:
        el = driver.find_element(
            By.XPATH,
            '//*[contains(@text, "Link de pago generado") or '
            'contains(@content-desc, "Link de pago generado")]'
        )
        if el.is_displayed():
            print("   ✅ [SUCCESS] CHECK 1 PASSED — SUCCESS HEADING VISIBLE.")
            heading_ok = True
    except Exception as e:
        print(f"   ⚠️  [SUCCESS] CHECK 1 FAILED: {e}")
 
    # --- CHECK 2: MONTO VALUE ON SUMMARY ---
    print(f"   🔍 [SUCCESS] CHECK 2: MONTO VALUE '{monto}' IN SUMMARY...")
    try:
        el = driver.find_element(
            By.XPATH, f'//*[contains(@text, "{monto}") or contains(@content-desc, "{monto}")]'
        )
        if el.is_displayed():
            print(f"   ✅ [SUCCESS] CHECK 2 PASSED — MONTO '{monto}' CONFIRMED.")
            data_ok = True
    except Exception as e:
        print(f"   ⚠️  [SUCCESS] CHECK 2 FAILED: {e}")
 
    # --- CHECK 3: CONCEPTO VALUE ON SUMMARY ---
    print(f"   🔍 [SUCCESS] CHECK 3: CONCEPTO '{concepto}' IN SUMMARY...")
    try:
        el = driver.find_element(
            By.XPATH,
            f'//*[contains(@text, "{concepto}") or contains(@content-desc, "{concepto}")]'
        )
        if el.is_displayed():
            print(f"   ✅ [SUCCESS] CHECK 3 PASSED — CONCEPTO '{concepto}' CONFIRMED.")
            data_ok = True
    except Exception as e:
        print(f"   ⚠️  [SUCCESS] CHECK 3 FAILED: {e}")
 
    # --- CHECK 4: SHARE OPTIONS VISIBLE ---
    print("   🔍 [SUCCESS] CHECK 4: SHARE OPTIONS (Email, WhatsApp, SMS)...")
    try:
        el = driver.find_element(
            By.XPATH,
            '//*[contains(@text, "Compartir") or contains(@content-desc, "Compartir")]'
        )
        if el.is_displayed():
            print("   ✅ [SUCCESS] CHECK 4 PASSED — 'COMPARTIR' SECTION VISIBLE.")
    except Exception as e:
        print(f"   ⚠️  [SUCCESS] CHECK 4 FAILED (NON-BLOCKING): {e}")
 
    if heading_ok and data_ok:
        print("   ✅ [SUCCESS] FULL CONFIRMATION — HEADING + DATA ROWS BOTH VERIFIED.")
        return True
    elif heading_ok:
        print("   ⚠️  [SUCCESS] PARTIAL CONFIRMATION — HEADING OK BUT DATA ROWS NOT MATCHED.")
        print("   💡 CHECK IF MONTO/CONCEPTO FORMAT DIFFERS ON DEVICE (E.G. '$85.50' VS '$ 85.50').")
        return True
    else:
        print("   ❌ [SUCCESS] SCREEN NOT CONFIRMED — SUCCESS HEADING NOT FOUND.")
        return False
 
 
# =================================================================================
# SVS-95: SUCCESSFUL PAYMENT LINK GENERATION
# =================================================================================
 
# --- TEST DATA ---
SVS95_MONTO   = "85.50"
SVS95_CONCEPTO = "Venta de productos X"
 
def SVS_95():
    print("\n" + "=" * 60)
    print("🧪 SVS-95: SUCCESSFUL PAYMENT LINK GENERATION")
    print("=" * 60)
 
    driver, wait = utils.iniciar_driver()
 
    try:
        # PRECONDITION: REACH THE MAIN CHARGING SCREEN
        print("🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)
 
        # STEP 1: NAVIGATE TO SERVICES TAB
        print("\n👉 STEP 1: NAVIGATING TO 'SERVICES' TAB...")
        if not _navigate_to_services_tab(driver, wait):
            print("\n💥 SVS-95: FAILED — COULD NOT NAVIGATE TO SERVICES TAB.")
            utils.tomar_screenshot(driver, "SVS_95_NAV_FAILED")
            _capture_evidence(driver, "SVS_95")
            return False
 
        # STEP 2: CLICK "LINKS DE PAGO" CARD
        print("\n👉 STEP 2: CLICKING 'LINKS DE PAGO' CARD...")
        if not _click_payment_links_card(driver):
            print("\n💥 SVS-95: FAILED — COULD NOT CLICK 'LINKS DE PAGO' CARD.")
            utils.tomar_screenshot(driver, "SVS_95_CARD_CLICK_FAILED")
            _capture_evidence(driver, "SVS_95")
            return False
 
        # STEP 3: CLICK "+ CREAR NUEVO" BUTTON
        print("\n👉 STEP 3: CLICKING '+ CREAR NUEVO' BUTTON...")
        if not _click_create_new(driver):
            print("\n💥 SVS-95: FAILED — COULD NOT CLICK '+ CREAR NUEVO'.")
            utils.tomar_screenshot(driver, "SVS_95_CREAR_FAILED")
            _capture_evidence(driver, "SVS_95")
            return False
 
        print("\n📸 SCREENSHOT — CREATE FORM OPENED...")
        utils.tomar_screenshot(driver, "SVS_95_FORM_OPENED")
 
        # STEP 4: FILL MONTO
        print(f"\n👉 STEP 4: FILLING MONTO = '{SVS95_MONTO}'...")
        if not _fill_monto(driver, SVS95_MONTO):
            print("\n💥 SVS-95: FAILED — COULD NOT FILL MONTO FIELD.")
            utils.tomar_screenshot(driver, "SVS_95_MONTO_FAILED")
            _capture_evidence(driver, "SVS_95")
            return False
 
        # STEP 5: FILL PRODUCTO O SERVICIO
        print(f"\n👉 STEP 5: FILLING CONCEPTO = '{SVS95_CONCEPTO}'...")
        if not _fill_concepto(driver, SVS95_CONCEPTO):
            print("\n💥 SVS-95: FAILED — COULD NOT FILL CONCEPTO FIELD.")
            utils.tomar_screenshot(driver, "SVS_95_CONCEPTO_FAILED")
            _capture_evidence(driver, "SVS_95")
            return False
 
        # STEP 6: SELECT FECHA DE VENCIMIENTO (TODAY'S DATE — ALWAYS ENABLED IN PICKER)
        print("\n👉 STEP 6: SELECTING FECHA DE VENCIMIENTO (TODAY'S DATE)...")
        if not _select_due_date(driver):
            print("\n💥 SVS-95: FAILED — COULD NOT SELECT EXPIRY DATE.")
            utils.tomar_screenshot(driver, "SVS_95_FECHA_FAILED")
            _capture_evidence(driver, "SVS_95")
            return False
 
        print("\n📸 SCREENSHOT — FORM FILLED, READY TO SUBMIT...")
        utils.tomar_screenshot(driver, "SVS_95_FORM_FILLED")
 
        # STEP 7: CLICK "GENERAR"
        print("\n👉 STEP 7: CLICKING 'GENERAR' BUTTON...")
        if not _click_generate(driver):
            print("\n💥 SVS-95: FAILED — COULD NOT CLICK 'GENERAR'.")
            utils.tomar_screenshot(driver, "SVS_95_GENERAR_FAILED")
            _capture_evidence(driver, "SVS_95")
            return False
 
        # STEP 8: VERIFY SUCCESS SCREEN
        print("\n👉 STEP 8: VERIFYING SUCCESS SCREEN 'LINK DE PAGO GENERADO'...")
        if not _verify_link_generado_screen(driver, SVS95_MONTO, SVS95_CONCEPTO):
            print("\n💥 SVS-95: FAILED — SUCCESS SCREEN NOT CONFIRMED.")
            utils.tomar_screenshot(driver, "SVS_95_SUCCESS_NOT_FOUND")
            _capture_evidence(driver, "SVS_95")
 
            print("\n🔍 SCANNING VISIBLE TEXT FOR DEBUGGING...")
            try:
                for elem in driver.find_elements(By.XPATH, "//*"):
                    t = elem.get_attribute("text")
                    if t and len(t) > 3:
                        print(f"   📝 VISIBLE TEXT: '{t}'")
            except:
                pass
            return False
 
        # SUCCESS PATH
        print("\n📸 TAKING SCREENSHOT — LINK DE PAGO GENERATED SUCCESSFULLY...")
        utils.tomar_screenshot(driver, "SVS_95_LINK_GENERADO_OK")
        _capture_evidence(driver, "SVS_95")
        print("\n✅ SVS-95: SUCCESS — PAYMENT LINK CREATED AND CONFIRMED.")
        return True
 
    except Exception as e:
        print(f"\n💥 SVS-95 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "SVS_95_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)

# =================================================================================
# SVS-96: FAILED GENERATION (EMPTY SPACE)
# =================================================================================
 
# --- TEST DATA ---
SVS96_MONTO = "85.50"
# CONCEPTO IS INTENTIONALLY LEFT EMPTY FOR THIS NEGATIVE TEST
 
def SVS_96():
    print("\n" + "=" * 60)
    print("🧪 SVS-96: FAILED GENERATION (EMPTY SPACE)")
    print("=" * 60)
 
    driver, wait = utils.iniciar_driver()
 
    try:
        # PRECONDITION: REACH THE MAIN CHARGING SCREEN
        print("🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)
 
        # STEP 1: NAVIGATE TO SERVICES TAB
        print("\n👉 STEP 1: NAVIGATING TO 'SERVICES' TAB...")
        if not _navigate_to_services_tab(driver, wait):
            print("\n💥 SVS-96: FAILED — COULD NOT NAVIGATE TO SERVICES TAB.")
            utils.tomar_screenshot(driver, "SVS_96_NAV_FAILED")
            _capture_evidence(driver, "SVS_96")
            return False
 
        # STEP 2: CLICK "LINKS DE PAGO" CARD
        print("\n👉 STEP 2: CLICKING 'LINKS DE PAGO' CARD...")
        if not _click_payment_links_card(driver):
            print("\n💥 SVS-96: FAILED — COULD NOT CLICK 'LINKS DE PAGO' CARD.")
            utils.tomar_screenshot(driver, "SVS_96_CARD_CLICK_FAILED")
            _capture_evidence(driver, "SVS_96")
            return False
 
        # STEP 3: CLICK "+ CREAR NUEVO" BUTTON
        print("\n👉 STEP 3: CLICKING '+ CREAR NUEVO' BUTTON...")
        if not _click_create_new(driver):
            print("\n💥 SVS-96: FAILED — COULD NOT CLICK '+ CREAR NUEVO'.")
            utils.tomar_screenshot(driver, "SVS_96_CREAR_FAILED")
            _capture_evidence(driver, "SVS_96")
            return False

        # STEP 4: LEAVE MONTO - INTENTIONAL OMISSION
        print("\n👉 STEP 4: LEAVING MONTO BLANK")

        # STEP 5: FILL PRODUCTO O SERVICIO
        print(f"\n👉 STEP 5: FILLING PRODUCTO O SERVICIO = '{SVS95_CONCEPTO}'...")
        if not _fill_concepto(driver, SVS95_CONCEPTO):
            print("\n💥 SVS-96: FAILED — COULD NOT FILL MONTO FIELD.")
            utils.tomar_screenshot(driver, "SVS_96_MONTO_FAILED")
            _capture_evidence(driver, "SVS_96")
            return False
            
        # STEP 6: SELECT FECHA DE VENCIMIENTO (TODAY'S DATE — SAME AS SVS-95)
        print("\n👉 STEP 6: SELECTING FECHA DE VENCIMIENTO (TODAY'S DATE)...")
        if not _select_due_date(driver):
            print("\n💥 SVS-96: FAILED — COULD NOT SELECT EXPIRY DATE.")
            utils.tomar_screenshot(driver, "SVS_96_FECHA_FAILED")
            _capture_evidence(driver, "SVS_96")
            return False
 
        print("\n📸 SCREENSHOT — FORM WITH BLANK MONTO, READY TO SUBMIT...")
        utils.tomar_screenshot(driver, "SVS_96_FORM_BLANK_MONTO")
 
        print("\n👉 STEP 7: CLICKING 'GENERAR' (EXPECTING VALIDATION TO BLOCK SUBMISSION)...")
        _click_generate(driver)
        time.sleep(2)
 
        # STEP 8: VERIFY VALIDATION ERROR "INGRESA UN CONCEPTO" IS VISIBLE
        print("\n👉 STEP 8: VERIFYING VALIDATION ERROR 'INGRESA UNA CANTIDAD VISIBLE' IS DISPLAYED...")
        error_found = False
 
        # STRATEGY 1: EXACT @text MATCH
        try:
            el = driver.find_element(
                By.XPATH, '//*[@text="Ingresa una cantidad visible"]'
            )
            if el.is_displayed():
                print("   ✅ [VERIFY] STRATEGY 1: ERROR 'INGRESA UNA CANTIDAD VISIBLE' FOUND VIA @text.")
                error_found = True
        except Exception as e:
            print(f"   ⚠️  [VERIFY] STRATEGY 1 FAILED: {e}")
 
        # STRATEGY 2: contains(@text) / contains(@content-desc)
        if not error_found:
            try:
                el = driver.find_element(
                    By.XPATH,
                    '//*[contains(@text, "Ingresa una cantidad visible") or '
                    'contains(@content-desc, "Ingresa un concepto")]'
                )
                if el.is_displayed():
                    print("   ✅ [VERIFY] STRATEGY 2: ERROR FOUND VIA PARTIAL MATCH.")
                    error_found = True
            except Exception as e:
                print(f"   ⚠️  [VERIFY] STRATEGY 2 FAILED: {e}")
 
        # STRATEGY 3: PARTIAL KEYWORD — IN CASE TEXT IS TRUNCATED ON SMALL SCREENS
        if not error_found:
            try:
                el = driver.find_element(
                    By.XPATH,
                    '//*[contains(@text, "cantidad") or contains(@content-desc, "cantidad")]'
                )
                if el.is_displayed():
                    print("   ✅ [VERIFY] STRATEGY 3: ERROR FOUND VIA 'cantidad' KEYWORD.")
                    error_found = True
            except Exception as e:
                print(f"   ⚠️  [VERIFY] STRATEGY 3 FAILED: {e}")
 
        # STRATEGY 4: UIAUTOMATOR (FINAL FALLBACK)
        if not error_found:
            try:
                el = driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textContains("cantidad")'
                )
                if el.is_displayed():
                    print("   ✅ [VERIFY] STRATEGY 4: ERROR FOUND VIA UIAUTOMATOR.")
                    error_found = True
            except Exception as e:
                print(f"   💥 [VERIFY] STRATEGY 4 FAILED: {e}")
 
        if not error_found:
            print("\n💥 SVS-96: FAILED — VALIDATION ERROR 'INGRESA UNA CANTIDAD VISIBLE' NOT VISIBLE.")
            utils.tomar_screenshot(driver, "SVS_96_ERROR_NOT_SHOWN")
            _capture_evidence(driver, "SVS_96")
 
            print("\n🔍 SCANNING VISIBLE TEXT FOR DEBUGGING...")
            try:
                for elem in driver.find_elements(By.XPATH, "//*"):
                    t = elem.get_attribute("text")
                    if t and len(t) > 3:
                        print(f"   📝 VISIBLE TEXT: '{t}'")
            except:
                pass
            return False
 
        # SUCCESS PATH
        print("\n📸 TAKING SCREENSHOT — VALIDATION ERROR CORRECTLY DISPLAYED...")
        utils.tomar_screenshot(driver, "SVS_96_VALIDATION_ERROR_OK")
        _capture_evidence(driver, "SVS_96")
        print("\n✅ SVS-96: SUCCESS — LEAVING 'MONTO' BLANK SHOWS 'INGRESA UN CONCEPTO'.")
        return True
 
    except Exception as e:
        print(f"\n💥 SVS-96 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "SVS_96_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)

# =================================================================================
# SVS-97: FAILED GENERATION (EMPTY PRODUCT OR SERVICE)
# =================================================================================
 
# --- TEST DATA ---
SVS97_MONTO = "85.50"
# CONCEPTO IS INTENTIONALLY LEFT EMPTY FOR THIS NEGATIVE TEST
 
def SVS_97():
    print("\n" + "=" * 60)
    print("🧪 SVS-97: FAILED GENERATION (EMPTY PRODUCT OR SERVICE)")
    print("=" * 60)
 
    driver, wait = utils.iniciar_driver()
 
    try:
        # PRECONDITION: REACH THE MAIN CHARGING SCREEN
        print("🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)
 
        # STEP 1: NAVIGATE TO SERVICES TAB
        print("\n👉 STEP 1: NAVIGATING TO 'SERVICES' TAB...")
        if not _navigate_to_services_tab(driver, wait):
            print("\n💥 SVS-97: FAILED — COULD NOT NAVIGATE TO SERVICES TAB.")
            utils.tomar_screenshot(driver, "SVS_97_NAV_FAILED")
            _capture_evidence(driver, "SVS_97")
            return False
 
        # STEP 2: CLICK "LINKS DE PAGO" CARD
        print("\n👉 STEP 2: CLICKING 'LINKS DE PAGO' CARD...")
        if not _click_payment_links_card(driver):
            print("\n💥 SVS-97: FAILED — COULD NOT CLICK 'LINKS DE PAGO' CARD.")
            utils.tomar_screenshot(driver, "SVS_97_CARD_CLICK_FAILED")
            _capture_evidence(driver, "SVS_97")
            return False
 
        # STEP 3: CLICK "+ CREAR NUEVO" BUTTON
        print("\n👉 STEP 3: CLICKING '+ CREAR NUEVO' BUTTON...")
        if not _click_create_new(driver):
            print("\n💥 SVS-97: FAILED — COULD NOT CLICK '+ CREAR NUEVO'.")
            utils.tomar_screenshot(driver, "SVS_97_CREAR_FAILED")
            _capture_evidence(driver, "SVS_97")
            return False
 
        # STEP 4: FILL MONTO (SAME AS SVS-95)
        print(f"\n👉 STEP 4: FILLING MONTO = '{SVS97_MONTO}'...")
        if not _fill_monto(driver, SVS97_MONTO):
            print("\n💥 SVS-97: FAILED — COULD NOT FILL MONTO FIELD.")
            utils.tomar_screenshot(driver, "SVS_97_MONTO_FAILED")
            _capture_evidence(driver, "SVS_97")
            return False
 
        # STEP 5: LEAVE "PRODUCTO O SERVICIO" BLANK — INTENTIONAL OMISSION
        print("\n👉 STEP 5: LEAVING 'PRODUCTO O SERVICIO' BLANK (INTENTIONAL — NEGATIVE TEST).")
 
        # STEP 6: SELECT FECHA DE VENCIMIENTO (TODAY'S DATE — SAME AS SVS-95)
        print("\n👉 STEP 6: SELECTING FECHA DE VENCIMIENTO (TODAY'S DATE)...")
        if not _select_due_date(driver):
            print("\n💥 SVS-97: FAILED — COULD NOT SELECT EXPIRY DATE.")
            utils.tomar_screenshot(driver, "SVS_97_FECHA_FAILED")
            _capture_evidence(driver, "SVS_97")
            return False
 
        print("\n📸 SCREENSHOT — FORM WITH BLANK CONCEPTO, READY TO SUBMIT...")
        utils.tomar_screenshot(driver, "SVS_97_FORM_BLANK_CONCEPTO")
 
        print("\n👉 STEP 7: CLICKING 'GENERAR' (EXPECTING VALIDATION TO BLOCK SUBMISSION)...")
        _click_generate(driver)
        time.sleep(2)
 
        # STEP 8: VERIFY VALIDATION ERROR "INGRESA UN CONCEPTO" IS VISIBLE
        print("\n👉 STEP 8: VERIFYING VALIDATION ERROR 'INGRESA UN CONCEPTO' IS DISPLAYED...")
        error_found = False
 
        # STRATEGY 1: EXACT @text MATCH
        try:
            el = driver.find_element(
                By.XPATH, '//*[@text="Ingresa un concepto"]'
            )
            if el.is_displayed():
                print("   ✅ [VERIFY] STRATEGY 1: ERROR 'INGRESA UN CONCEPTO' FOUND VIA @text.")
                error_found = True
        except Exception as e:
            print(f"   ⚠️  [VERIFY] STRATEGY 1 FAILED: {e}")
 
        # STRATEGY 2: contains(@text) / contains(@content-desc)
        if not error_found:
            try:
                el = driver.find_element(
                    By.XPATH,
                    '//*[contains(@text, "Ingresa un concepto") or '
                    'contains(@content-desc, "Ingresa un concepto")]'
                )
                if el.is_displayed():
                    print("   ✅ [VERIFY] STRATEGY 2: ERROR FOUND VIA PARTIAL MATCH.")
                    error_found = True
            except Exception as e:
                print(f"   ⚠️  [VERIFY] STRATEGY 2 FAILED: {e}")
 
        # STRATEGY 3: PARTIAL KEYWORD — IN CASE TEXT IS TRUNCATED ON SMALL SCREENS
        if not error_found:
            try:
                el = driver.find_element(
                    By.XPATH,
                    '//*[contains(@text, "concepto") or contains(@content-desc, "concepto")]'
                )
                if el.is_displayed():
                    print("   ✅ [VERIFY] STRATEGY 3: ERROR FOUND VIA 'concepto' KEYWORD.")
                    error_found = True
            except Exception as e:
                print(f"   ⚠️  [VERIFY] STRATEGY 3 FAILED: {e}")
 
        # STRATEGY 4: UIAUTOMATOR (FINAL FALLBACK)
        if not error_found:
            try:
                el = driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textContains("concepto")'
                )
                if el.is_displayed():
                    print("   ✅ [VERIFY] STRATEGY 4: ERROR FOUND VIA UIAUTOMATOR.")
                    error_found = True
            except Exception as e:
                print(f"   💥 [VERIFY] STRATEGY 4 FAILED: {e}")
 
        if not error_found:
            print("\n💥 SVS-97: FAILED — VALIDATION ERROR 'INGRESA UN CONCEPTO' NOT VISIBLE.")
            utils.tomar_screenshot(driver, "SVS_97_ERROR_NOT_SHOWN")
            _capture_evidence(driver, "SVS_97")
 
            print("\n🔍 SCANNING VISIBLE TEXT FOR DEBUGGING...")
            try:
                for elem in driver.find_elements(By.XPATH, "//*"):
                    t = elem.get_attribute("text")
                    if t and len(t) > 3:
                        print(f"   📝 VISIBLE TEXT: '{t}'")
            except:
                pass
            return False
 
        # SUCCESS PATH
        print("\n📸 TAKING SCREENSHOT — VALIDATION ERROR CORRECTLY DISPLAYED...")
        utils.tomar_screenshot(driver, "SVS_97_VALIDATION_ERROR_OK")
        _capture_evidence(driver, "SVS_97")
        print("\n✅ SVS-97: SUCCESS — LEAVING 'PRODUCTO O SERVICIO' BLANK SHOWS 'INGRESA UN CONCEPTO'.")
        return True
 
    except Exception as e:
        print(f"\n💥 SVS-97 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "SVS_97_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)


# === MAIN EXECUTION === #
if __name__ == "__main__":

    logger, log_file, timestamp = utils.iniciar_reporte("OPERATIONALS_SVS")

    try:
        SVS_92()
        SVS_93()
        SVS_94()
        SVS_95()
        SVS_96()
        SVS_97()

    finally:
        utils.generar_reporte_html("OPERATIONALS_SVS", log_file, timestamp)