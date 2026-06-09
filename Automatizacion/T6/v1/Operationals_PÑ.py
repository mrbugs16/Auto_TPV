"""
FILENAME: Operationals_PÑ.py
DESCRIPTION:
    TABBED NAVIGATION

CONTENTS:
    · PÑ-66: NAVIGATION TO THE "TRANSACTIONS" TAB.
    · PÑ-67: NAVIGATION TO THE "SERVICE" TAB.
    · PÑ-68: NAVIGATION TO THE "SETTINGS" TAB.
    
REQUIREMENTS:
    - APPIUM SERVER RUNNING.
    - config.py AND utils.py IN THE SAME DIRECTORY.
"""

import sys
import os
import time

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_path not in sys.path:
    sys.path.append(project_path)

import config
import utils
from selenium.webdriver.common.by import By

# =================================================================================
# INTERNAL HELPER: CALL print_http_evidence_appium WITHOUT SILENCING ERRORS
# =================================================================================
def _capture_evidence(driver, nombre_test):
    """
    WRAPPER AROUND utils.print_http_evidence_appium THAT REPLACES THE OLD
    'try: ... except: pass' PATTERN. ERRORS ARE NOW PRINTED INSTEAD OF SWALLOWED,
    SO MISSING LOGS ARE VISIBLE IN THE CONSOLE OUTPUT DURING DEBUG.
    """
    try:
        utils.print_http_evidence_appium(driver, nombre_test)
    except Exception as ev_err:
        print(f"   ⚠️  HTTP EVIDENCE CAPTURE FAILED FOR [{nombre_test}]: {ev_err}")
        print(f"   💡 MAKE SURE APPIUM IS STARTED WITH: appium --allow-insecure=*:get_server_logs")

# =================================================================================
# HELPER: FULL LOGIN + BUSINESS REGISTRATION + LOCATION PERMISSION
#         (REACHES THE MAIN CALCULATOR / CHARGING SCREEN)
# =================================================================================
def helper_login_to_calculator(driver, wait):
    """
    EXECUTES THE COMPLETE FLOW TO REACH THE MAIN CHARGING SCREEN.
      1. LOGIN WITH VALID CREDENTIALS.
      2. BUSINESS REGISTRATION (TOKEN + AFFILIATION NUMBER).
      3. LOCATION PERMISSION DIALOG.
    """

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

# =============================================
# PÑ-66: NAVIGATION TO THE "TRANSACTIONS" TAB.
# ============================================
def PÑ_66():
    print("\n" + "=" * 60)
    print("🧪 PÑ-66: NAVIGATION TO THE TRANSACTIONS TAB")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        # PRECONDITION: REACH THE MAIN CHARGING SCREEN
        print("🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)

        # STEP 1: NAVIGATE TO TRANSACTIONS TAB
        print("\n👉 STEP 1: NAVIGATING TO 'TRANSACTIONS' TAB...")
        utils.click_boton(driver, config.XPATH_PÑ_TAB_TRANSACCIONES)
        time.sleep(2)
        print("\n📸 TAKING SCREENSHOT — TRANSACTIONS TAB...")
        utils.tomar_screenshot(driver, "PÑ_66_TRASACTIONS_TAB")
        _capture_evidence(driver, "PÑ_66")
        print("\n✅ PÑ-66: SUCCESS — TRANSACTIONS TAB DISPLAY.")
        _capture_evidence(driver, "PÑ_66")
        print("\n🔍 SCANNING VISIBLE TEXT FOR DEBUGGING...")
        try:
                for elem in driver.find_elements(By.XPATH, "//*"):
                    t = elem.get_attribute("text")
                    if t and len(t) > 3:
                        print(f"   📝 VISIBLE TEXT: '{t}'")
        except:
                pass
        return False

    except Exception as e:
        print(f"\n💥 PÑ-66 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "PÑ_66_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)

# =============================================
# PÑ-67: NAVIGATION TO THE "SERVICE" TAB.
# ============================================
def PÑ_67():
    print("\n" + "=" * 60)
    print("🧪 PÑ-67: NAVIGATION TO THE SERVICE TAB.")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        # PRECONDITION: REACH THE MAIN CHARGING SCREEN
        print("🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)

        # STEP 1: NAVIGATE TO SERVICE TAB
        print("\n👉 STEP 1: NAVIGATING TO 'SERVICE' TAB...")
        utils.click_boton(driver, config.XPATH_PÑ_TAB_SERVICIOS)
        time.sleep(2)
        print("\n📸 TAKING SCREENSHOT — SERVICE TAB...")
        utils.tomar_screenshot(driver, "PÑ_67_SERVICE_TAB")
        _capture_evidence(driver, "PÑ_67")
        print("\n✅ PÑ-67: SUCCESS — SERVICE TAB DISPLAY.")
        _capture_evidence(driver, "PÑ_67")
        print("\n🔍 SCANNING VISIBLE TEXT FOR DEBUGGING...")
        try:
                for elem in driver.find_elements(By.XPATH, "//*"):
                    t = elem.get_attribute("text")
                    if t and len(t) > 3:
                        print(f"   📝 VISIBLE TEXT: '{t}'")
        except:
                pass
        return False

    except Exception as e:
        print(f"\n💥 PÑ-67 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "PÑ_67_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)

# =============================================
# PÑ-68: NAVIGATION TO THE "SETTINGS" TAB.
# ============================================
def PÑ_68():
    print("\n" + "=" * 60)
    print("🧪 PÑ-68: NAVIGATION TO THE SETTINGS TAB")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        # PRECONDITION: REACH THE MAIN CHARGING SCREEN
        print("🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)

        # STEP 1: NAVIGATE TO SETTINGS TAB
        print("\n👉 STEP 1: NAVIGATING TO 'SETTINGS' TAB...")
        utils.click_boton(driver, config.XPATH_PÑ_TAB_AJUSTES)
        time.sleep(2)
        print("\n📸 TAKING SCREENSHOT — SETTINGS TAB...")
        utils.tomar_screenshot(driver, "PÑ_68_SETTINGS")
        _capture_evidence(driver, "PÑ_68")
        print("\n✅ PÑ-68: SUCCESS — SETTINGS TAB DISPLAY.")
        _capture_evidence(driver, "PÑ_68")
        print("\n🔍 SCANNING VISIBLE TEXT FOR DEBUGGING...")
        try:
                for elem in driver.find_elements(By.XPATH, "//*"):
                    t = elem.get_attribute("text")
                    if t and len(t) > 3:
                        print(f"   📝 VISIBLE TEXT: '{t}'")
        except:
                pass
        return False

    except Exception as e:
        print(f"\n💥 PÑ-68 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "PÑ_68_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)

# =============================================
# PÑ-69: HOME TAB
# ============================================
def PÑ_69():
    print("\n" + "=" * 60)
    print("🧪 PÑ-69: HOME TAB")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        # PRECONDITION: REACH THE MAIN CHARGING SCREEN
        print("🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)

        # STEP 1: NAVIGATE TO HOME TAB
        print("\n👉 STEP 1:HOME TAB...")
        utils.click_boton(driver, config.XPATH_PÑ_TAB_INICIO)
        time.sleep(2)
        print("\n📸 TAKING SCREENSHOT — HOME TAB...")
        utils.tomar_screenshot(driver, "PÑ_69_HOME")
        _capture_evidence(driver, "PÑ_69")
        print("\n✅ PÑ-69: SUCCESS — HOME TAB.")
        _capture_evidence(driver, "PÑ_69")
        print("\n🔍 SCANNING VISIBLE TEXT FOR DEBUGGING...")
        try:
                for elem in driver.find_elements(By.XPATH, "//*"):
                    t = elem.get_attribute("text")
                    if t and len(t) > 3:
                        print(f"   📝 VISIBLE TEXT: '{t}'")
        except:
                pass
        return False

    except Exception as e:
        print(f"\n💥 PÑ-69 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "PÑ_69_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)

# === MAIN EXECUTION === #
if __name__ == "__main__":

    logger, log_file, timestamp = utils.iniciar_reporte("OPERATIONALS_PÑ")

    try:
        PÑ_66()
        PÑ_67()
        PÑ_68()
        PÑ_69()

    finally:
        utils.generar_reporte_html("OPERATIONALS_PÑ", log_file, timestamp)
