"""
FILENAME: Operationals_UBI.py
DESCRIPTION:
    CHECKING UBICATION SCREEN

CONTENTS:
    · UBI-144: VERIFY LOCATION PERMISSION DIALOG LOADS CORRECTLY AFTER REGISTRATION
    · UBI-145: SELECT 'MIENTRAS LA APP ESTÁ EN USO' + 'PRECISA' AND VERIFY CALCULATOR LOADS
    · UBI-146: SELECT 'PRECISA' + 'SOLO ESTA VEZ' AND VERIFY CALCULATOR LOADS
    · UBI-147: SELECT 'PRECISA' + 'NO PERMITIR' → VERIFY 'PERMISO REQUERIDO' POPUP
    · UBI-148: SELECT 'APROXIMADA' + 'MIENTRAS LA APP EN USO' AND VERIFY CALCULATOR LOADS
    · UBI-149A: APROXIMADA + SOLO ESTA VEZ → COBRAR → PRECISION DIALOG → 'SOLO ESTA VEZ'
    · UBI-149B: APROXIMADA + SOLO ESTA VEZ → COBRAR → PRECISION DIALOG → 'SEGUIR USANDO APROXIMADA'
    · UBI-150: SELECT 'APROXIMADA' + 'NO PERMITIR' AND VERIFY CALCULATOR LOADS
    
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
    try:
        utils.print_http_evidence_appium(driver, nombre_test)
    except Exception as ev_err:
        print(f"   ⚠️  HTTP EVIDENCE CAPTURE FAILED FOR [{nombre_test}]: {ev_err}")
        print(f"   💡 MAKE SURE APPIUM IS STARTED WITH: appium --allow-insecure=*:get_server_logs")

# =================================================================================
# HELPER: FULL LOGIN + BUSINESS REGISTRATION
#         (REACHES THE LOCATION PERMISSION SCREEN)
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

    print("   ✅ [HELPER] LOGIN + REGISTRATION COMPLETE. READY FOR LOCATION PERMISSION TESTS.")


# =================================================================================
# UBI-144: VERIFY LOCATION PERMISSION DIALOG LOADS CORRECTLY AFTER REGISTRATION
# =================================================================================
def UBI_144():
    print("\n" + "=" * 60)
    print("🧪 UBI-144: VERIFY LOCATION PERMISSION DIALOG LOADS CORRECTLY")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        print("🔐 PRECONDITION: EXECUTING LOGIN + REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)
        time.sleep(3)

        print("\n👉 STEP 1: VERIFYING LOCATION PERMISSION DIALOG IS DISPLAYED...")

        dialog_visible = False
        elementos_encontrados = []

        # VERIFY DIALOG TITLE TEXT
        try:
            titulo = driver.find_element(By.XPATH,
                '//*[contains(@text, "permitir") or contains(@text, "ubicación") or contains(@text, "acceda")]'
            )
            if titulo.is_displayed():
                dialog_visible = True
                elementos_encontrados.append(f"TITLE: '{titulo.get_attribute('text')}'")
        except:
            pass

        # VERIFY 'MIENTRAS LA APP ESTÁ EN USO' BUTTON
        try:
            btn_mientras = driver.find_element(By.XPATH,
                '//*[contains(@text, "MIENTRAS LA APP") or contains(@text, "Mientras la app")]'
            )
            if btn_mientras.is_displayed():
                dialog_visible = True
                elementos_encontrados.append("BUTTON: 'MIENTRAS LA APP ESTÁ EN USO'")
        except:
            pass

        # VERIFY 'SOLO ESTA VEZ' BUTTON
        try:
            btn_solo = driver.find_element(By.XPATH,
                '//*[contains(@text, "SOLO ESTA VEZ") or contains(@text, "Solo esta vez")]'
            )
            if btn_solo.is_displayed():
                dialog_visible = True
                elementos_encontrados.append("BUTTON: 'SOLO ESTA VEZ'")
        except:
            pass

        # VERIFY 'NO PERMITIR' BUTTON
        try:
            btn_no = driver.find_element(By.XPATH,
                '//*[contains(@text, "NO PERMITIR") or contains(@text, "No permitir")]'
            )
            if btn_no.is_displayed():
                dialog_visible = True
                elementos_encontrados.append("BUTTON: 'NO PERMITIR'")
        except:
            pass

        # VERIFY 'Precisa' AND 'Aproximada' LABELS
        try:
            precisa = driver.find_element(By.XPATH, '//*[contains(@text, "Precisa")]')
            if precisa.is_displayed():
                elementos_encontrados.append("LABEL: 'Precisa'")
        except:
            pass

        try:
            aproximada = driver.find_element(By.XPATH, '//*[contains(@text, "Aproximada")]')
            if aproximada.is_displayed():
                elementos_encontrados.append("LABEL: 'Aproximada'")
        except:
            pass

        print(f"\n   📋 ELEMENTS FOUND: {len(elementos_encontrados)}")
        for elem in elementos_encontrados:
            print(f"      ✅ {elem}")

        if dialog_visible:
            print("\n📸 TAKING SCREENSHOT OF LOCATION PERMISSION DIALOG...")
            utils.tomar_screenshot(driver, "UBI_144_SUCCESS")
            _capture_evidence(driver, "UBI_144")
            print("\n✅ UBI-144: SUCCESS — LOCATION PERMISSION DIALOG LOADED CORRECTLY.")
            return True
        else:
            print("\n❌ UBI-144 FAILED — LOCATION PERMISSION DIALOG NOT DETECTED.")
            utils.tomar_screenshot(driver, "UBI_144_FAILED")
            _capture_evidence(driver, "UBI_144")
            print("\n🔍 SCANNING FOR VISIBLE TEXT ON CURRENT SCREEN FOR DEBUGGING...")
            try:
                todos = driver.find_elements(By.XPATH, "//*")
                for elem in todos:
                    t = elem.get_attribute("text")
                    if t and len(t) > 3:
                        print(f"   📝 VISIBLE TEXT: '{t}'")
            except:
                pass
            return False

    except Exception as e:
        print(f"\n💥 UBI-144 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "UBI_144_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)


# =================================================================================
# UBI-145: SELECT 'MIENTRAS LA APP ESTÁ EN USO' + 'PRECISA' AND VERIFY CALCULATOR LOADS
# =================================================================================
def UBI_145():
    print("\n" + "=" * 60)
    print("🧪 UBI-145: SELECT 'MIENTRAS LA APP ESTÁ EN USO' + 'PRECISA' → VERIFY CALCULATOR")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        print("🔐 PRECONDITION: EXECUTING LOGIN + REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)
        time.sleep(3)

        print("\n👉 STEP 1: VERIFYING LOCATION PERMISSION DIALOG IS DISPLAYED...")

        dialog_visible = False
        try:
            btn_mientras = driver.find_element(By.XPATH,
                '//*[contains(@text, "MIENTRAS LA APP") or contains(@text, "Mientras la app")]'
            )
            if btn_mientras.is_displayed():
                dialog_visible = True
                print("   ✅ LOCATION PERMISSION DIALOG DETECTED.")
        except:
            pass

        if not dialog_visible:
            print("   ❌ LOCATION PERMISSION DIALOG NOT FOUND.")
            utils.tomar_screenshot(driver, "UBI_145_NO_DIALOG")
            _capture_evidence(driver, "UBI_145")
            return False

        print("\n👉 STEP 2: SELECTING 'PRECISA' LOCATION OPTION...")

        precisa_selected = False
        try:
            precisa = driver.find_element(By.XPATH,
                '//*[contains(@text, "Precisa")]'
            )
            if precisa.is_displayed():
                precisa.click()
                precisa_selected = True
                print("   ✅ 'PRECISA' OPTION SELECTED.")
                time.sleep(1)
        except:
            pass

        if not precisa_selected:
            print("   ⚠️ WARNING: COULD NOT SELECT 'PRECISA' — IT MAY BE SELECTED BY DEFAULT.")

        utils.tomar_screenshot(driver, "UBI_145_BEFORE_CLICK")

        print("\n👉 STEP 3: CLICKING 'MIENTRAS LA APP ESTÁ EN USO' BUTTON...")

        try:
            btn_mientras = driver.find_element(By.XPATH,
                '//*[contains(@text, "MIENTRAS LA APP") or contains(@text, "Mientras la app")]'
            )
            btn_mientras.click()
            print("   ✅ 'MIENTRAS LA APP ESTÁ EN USO' BUTTON CLICKED.")
            time.sleep(5)
        except Exception as e:
            print(f"   ❌ FAILED TO CLICK 'MIENTRAS LA APP ESTÁ EN USO': {e}")
            utils.tomar_screenshot(driver, "UBI_145_CLICK_FAILED")
            _capture_evidence(driver, "UBI_145")
            return False

        print("\n👉 STEP 4: VERIFYING CALCULATOR / CHARGING SCREEN LOADED...")

        calculator_loaded = False
        elementos_encontrados = []

        
        try:
            cobrar = driver.find_element(By.XPATH, config.XPATH_C_PANTALLA_COBRO)
            if cobrar.is_displayed():
                calculator_loaded = True
                elementos_encontrados.append("BUTTON: 'COBRAR'")
        except:
            pass

        
        try:
            display = driver.find_element(By.XPATH, config.XPATH_C_DISPLAY_MONTO)
            if display.is_displayed():
                calculator_loaded = True
                elementos_encontrados.append("DISPLAY: '\$0.00'")
        except:
            pass

        
        popup_found = False
        try:
            popup = driver.find_element(By.XPATH,
                '//*[contains(@text, "exitoso") or contains(@text, "éxito") or contains(@text, "correcto")]'
            )
            if popup.is_displayed():
                popup_found = True
                print("   ⚠️ UNEXPECTED GREEN POPUP DETECTED — STILL VALIDATING CALCULATOR...")
        except:
            pass

        print(f"\n   📋 CALCULATOR ELEMENTS FOUND: {len(elementos_encontrados)}")
        for elem in elementos_encontrados:
            print(f"      ✅ {elem}")

        if not popup_found:
            print("   ✅ NO SUCCESS POPUP DETECTED — DIRECT TRANSITION TO CALCULATOR.")

        if calculator_loaded:
            print("\n📸 TAKING SCREENSHOT OF CALCULATOR SCREEN...")
            utils.tomar_screenshot(driver, "UBI_145_SUCCESS")
            _capture_evidence(driver, "UBI_145")
            print("\n✅ UBI-145: SUCCESS — LOCATION PERMISSION GRANTED AND CALCULATOR LOADED CORRECTLY.")
            return True
        else:
            print("\n❌ UBI-145 FAILED — CALCULATOR SCREEN DID NOT LOAD AFTER PERMISSION.")
            utils.tomar_screenshot(driver, "UBI_145_FAILED")
            _capture_evidence(driver, "UBI_145")
            print("\n🔍 SCANNING FOR VISIBLE TEXT ON CURRENT SCREEN FOR DEBUGGING...")
            try:
                todos = driver.find_elements(By.XPATH, "//*")
                for elem in todos:
                    t = elem.get_attribute("text")
                    if t and len(t) > 3:
                        print(f"   📝 VISIBLE TEXT: '{t}'")
            except:
                pass
            return False

    except Exception as e:
        print(f"\n💥 UBI-145 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "UBI_145_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)

# =================================================================================
# UBI-146: SELECT 'PRECISA' + 'SOLO ESTA VEZ' AND VERIFY CALCULATOR LOADS
# =================================================================================
def UBI_146():
    print("\n" + "=" * 60)
    print("🧪 UBI-146: SELECT 'PRECISA' + 'SOLO ESTA VEZ' AND VERIFY CALCULATOR LOADS")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        print("🔐 PRECONDITION: EXECUTING LOGIN + REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)
        time.sleep(3)

        print("\n👉 STEP 1: VERIFYING LOCATION PERMISSION DIALOG IS DISPLAYED...")

        dialog_visible = False
        try:
            btn_mientras = driver.find_element(By.XPATH,
                '//*[contains(@text, "MIENTRAS LA APP") or contains(@text, "Mientras la app")]'
            )
            if btn_mientras.is_displayed():
                dialog_visible = True
                print("   ✅ LOCATION PERMISSION DIALOG DETECTED.")
        except:
            pass

        if not dialog_visible:
            print("   ❌ LOCATION PERMISSION DIALOG NOT FOUND.")
            utils.tomar_screenshot(driver, "UBI_146_NO_DIALOG")
            _capture_evidence(driver, "UBI_146")
            return False

        print("\n👉 STEP 2: SELECTING 'PRECISA' LOCATION OPTION...")

        precisa_selected = False
        try:
            precisa = driver.find_element(By.XPATH,
                '//*[contains(@text, "Precisa")]'
            )
            if precisa.is_displayed():
                precisa.click()
                precisa_selected = True
                print("   ✅ 'PRECISA' OPTION SELECTED.")
                time.sleep(1)
        except:
            pass

        if not precisa_selected:
            print("   ⚠️ WARNING: COULD NOT SELECT 'PRECISA' — IT MAY BE SELECTED BY DEFAULT.")

        utils.tomar_screenshot(driver, "UBI_146_BEFORE_CLICK")

        print("\n👉 STEP 3: CLICKING 'SOLO ESTA VEZ' BUTTON...")

        try:
            btn_mientras = driver.find_element(By.XPATH,
                '//*[contains(@text, "SOLO ESTA VEZ") or contains(@text, "Solo esta vez")]'
            )
            btn_mientras.click()
            print("   ✅ 'SOLO ESTA VEZ' BUTTON CLICKED.")
            time.sleep(5)
        except Exception as e:
            print(f"   ❌ FAILED TO CLICK 'SOLO ESTA VEZ': {e}")
            utils.tomar_screenshot(driver, "UBI_146_CLICK_FAILED")
            _capture_evidence(driver, "UBI_146")
            return False

        print("\n👉 STEP 4: VERIFYING CALCULATOR / CHARGING SCREEN LOADED...")

        calculator_loaded = False
        elementos_encontrados = []

        
        try:
            cobrar = driver.find_element(By.XPATH, config.XPATH_C_PANTALLA_COBRO)
            if cobrar.is_displayed():
                calculator_loaded = True
                elementos_encontrados.append("BUTTON: 'COBRAR'")
        except:
            pass

        
        try:
            display = driver.find_element(By.XPATH, config.XPATH_C_DISPLAY_MONTO)
            if display.is_displayed():
                calculator_loaded = True
                elementos_encontrados.append("DISPLAY: '\$0.00'")
        except:
            pass

        popup_found = False
        try:
            popup = driver.find_element(By.XPATH,
                '//*[contains(@text, "exitoso") or contains(@text, "éxito") or contains(@text, "correcto")]'
            )
            if popup.is_displayed():
                popup_found = True
                print("   ⚠️ UNEXPECTED GREEN POPUP DETECTED — STILL VALIDATING CALCULATOR...")
        except:
            pass

        print(f"\n   📋 CALCULATOR ELEMENTS FOUND: {len(elementos_encontrados)}")
        for elem in elementos_encontrados:
            print(f"      ✅ {elem}")

        if not popup_found:
            print("   ✅ NO SUCCESS POPUP DETECTED — DIRECT TRANSITION TO CALCULATOR.")

        if calculator_loaded:
            print("\n📸 TAKING SCREENSHOT OF CALCULATOR SCREEN...")
            utils.tomar_screenshot(driver, "UBI_146_SUCCESS")
            _capture_evidence(driver, "UBI_146")
            print("\n✅ UBI-146: SUCCESS — LOCATION PERMISSION GRANTED AND CALCULATOR LOADED CORRECTLY.")
            return True
        else:
            print("\n❌ UBI-146 FAILED — CALCULATOR SCREEN DID NOT LOAD AFTER PERMISSION.")
            utils.tomar_screenshot(driver, "UBI_146_FAILED")
            _capture_evidence(driver, "UBI_146")
            print("\n🔍 SCANNING FOR VISIBLE TEXT ON CURRENT SCREEN FOR DEBUGGING...")
            try:
                todos = driver.find_elements(By.XPATH, "//*")
                for elem in todos:
                    t = elem.get_attribute("text")
                    if t and len(t) > 3:
                        print(f"   📝 VISIBLE TEXT: '{t}'")
            except:
                pass
            return False

    except Exception as e:
        print(f"\n💥 UBI-146 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "UBI_146_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)

# =================================================================================
# UBI-147: SELECT 'PRECISA' + 'NO PERMITIR' → VERIFY 'PERMISO REQUERIDO' POPUP
# =================================================================================
def UBI_147():
    print("\n" + "=" * 60)
    print("🧪 UBI-147: SELECT 'PRECISA' + 'NO PERMITIR' → VERIFY 'PERMISO REQUERIDO' POPUP")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        print("🔐 PRECONDITION: EXECUTING LOGIN + REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)
        time.sleep(3)

        print("\n👉 STEP 1: VERIFYING LOCATION PERMISSION DIALOG IS DISPLAYED...")

        dialog_visible = False
        try:
            btn_no = driver.find_element(By.XPATH,
                '//*[contains(@text, "NO PERMITIR") or contains(@text, "No permitir")]'
            )
            if btn_no.is_displayed():
                dialog_visible = True
                print("   ✅ LOCATION PERMISSION DIALOG DETECTED.")
        except:
            pass

        if not dialog_visible:
            print("   ❌ LOCATION PERMISSION DIALOG NOT FOUND.")
            utils.tomar_screenshot(driver, "UBI_147_NO_DIALOG")
            _capture_evidence(driver, "UBI_147")
            return False

        print("\n👉 STEP 2: SELECTING 'PRECISA' LOCATION OPTION...")

        try:
            precisa = driver.find_element(By.XPATH,
                '//*[contains(@text, "Precisa")]'
            )
            if precisa.is_displayed():
                precisa.click()
                print("   ✅ 'PRECISA' OPTION SELECTED.")
                time.sleep(1)
        except:
            print("   ⚠️ WARNING: COULD NOT SELECT 'PRECISA'.")

        utils.tomar_screenshot(driver, "UBI_147_PRECISA_SELECTED")

        print("\n👉 STEP 3: CLICKING 'NO PERMITIR' BUTTON (FIRST TIME)...")

        try:
            btn_no = driver.find_element(By.XPATH,
                '//*[contains(@text, "NO PERMITIR") or contains(@text, "No permitir")]'
            )
            btn_no.click()
            print("   ✅ 'NO PERMITIR' CLICKED (FIRST TIME).")
            time.sleep(5)
        except Exception as e:
            print(f"   ❌ FAILED TO CLICK 'NO PERMITIR': {e}")
            utils.tomar_screenshot(driver, "UBI_147_FIRST_DENY_FAILED")
            _capture_evidence(driver, "UBI_147")
            return False

        print("\n👉 STEP 4: VERIFYING CALCULATOR SCREEN LOADED...")

        calculator_loaded = False
        try:
            cobrar = driver.find_element(By.XPATH, config.XPATH_C_PANTALLA_COBRO)
            if cobrar.is_displayed():
                calculator_loaded = True
                print("   ✅ CALCULATOR SCREEN LOADED.")
        except:
            pass

        if not calculator_loaded:
            print("   ❌ CALCULATOR SCREEN DID NOT LOAD.")
            utils.tomar_screenshot(driver, "UBI_147_NO_CALCULATOR")
            _capture_evidence(driver, "UBI_147")
            return False

        utils.tomar_screenshot(driver, "UBI_147_CALCULATOR_AFTER_FIRST_DENY")

        print("\n👉 STEP 5: CLICKING 'COBRAR' BUTTON TO TRIGGER LOCATION DIALOG AGAIN...")

        try:
            cobrar = driver.find_element(By.XPATH, config.XPATH_C_PANTALLA_COBRO)
            cobrar.click()
            print("   ✅ 'COBRAR' BUTTON CLICKED.")
            time.sleep(5)
        except Exception as e:
            print(f"   ❌ FAILED TO CLICK 'COBRAR': {e}")
            utils.tomar_screenshot(driver, "UBI_147_COBRAR_FAILED")
            _capture_evidence(driver, "UBI_147")
            return False

        print("\n👉 STEP 6: VERIFYING LOCATION PERMISSION DIALOG APPEARED AGAIN...")

        second_dialog = False
        try:
            btn_no = driver.find_element(By.XPATH,
                '//*[contains(@text, "NO PERMITIR") or contains(@text, "No permitir")]'
            )
            if btn_no.is_displayed():
                second_dialog = True
                print("   ✅ LOCATION PERMISSION DIALOG APPEARED AGAIN.")
        except:
            pass

        if not second_dialog:
            print("   ❌ SECOND LOCATION PERMISSION DIALOG NOT DETECTED.")
            utils.tomar_screenshot(driver, "UBI_147_NO_SECOND_DIALOG")
            _capture_evidence(driver, "UBI_147")
            return False

        print("\n👉 STEP 7: CLICKING 'NO PERMITIR' BUTTON (SECOND TIME)...")

        try:
            btn_no = driver.find_element(By.XPATH,
                '//*[contains(@text, "NO PERMITIR") or contains(@text, "No permitir")]'
            )
            btn_no.click()
            print("   ✅ 'NO PERMITIR' CLICKED (SECOND TIME).")
            time.sleep(5)
        except Exception as e:
            print(f"   ❌ FAILED TO CLICK 'NO PERMITIR' (SECOND TIME): {e}")
            utils.tomar_screenshot(driver, "UBI_147_SECOND_DENY_FAILED")
            _capture_evidence(driver, "UBI_147")
            return False

            print("\n👉 STEP 8: VERIFYING 'PERMISO REQUERIDO' POPUP IS DISPLAYED...")

        time.sleep(8)

        permiso_requerido = False
        elementos_encontrados = []

        
        try:
            titulo = driver.find_element(By.XPATH,
                '//*[@content-desc="Permiso Requerido"]'
            )
            if titulo.is_displayed():
                permiso_requerido = True
                elementos_encontrados.append("TITLE: 'Permiso Requerido'")
        except:
            pass

        try:
            desc = driver.find_element(By.XPATH,
                '//*[contains(@content-desc, "permiso de ubicación") or contains(@content-desc, "necesario para realizar")]'
            )
            if desc.is_displayed():
                permiso_requerido = True
                elementos_encontrados.append(f"DESCRIPTION: '{desc.get_attribute('content-desc')}'")
        except:
            pass

        try:
            btn_config = driver.find_element(By.XPATH,
                '//*[@content-desc="Abrir Configuración"]'
            )
            if btn_config.is_displayed():
                permiso_requerido = True
                elementos_encontrados.append("BUTTON: 'Abrir Configuración'")
        except:
            pass

        print(f"\n   📋 'PERMISO REQUERIDO' ELEMENTS FOUND: {len(elementos_encontrados)}")
        for elem in elementos_encontrados:
            print(f"      ✅ {elem}")

        if permiso_requerido:
            print("\n📸 TAKING SCREENSHOT OF 'PERMISO REQUERIDO' POPUP...")
            utils.tomar_screenshot(driver, "UBI_147_SUCCESS")
            _capture_evidence(driver, "UBI_147")
            print("\n✅ UBI-147: SUCCESS — 'PERMISO REQUERIDO' POPUP DISPLAYED AFTER DENYING LOCATION TWICE.")
            return True
        else:
            print("\n❌ UBI-147 FAILED — 'PERMISO REQUERIDO' POPUP NOT DETECTED.")
            utils.tomar_screenshot(driver, "UBI_147_FAILED")
            _capture_evidence(driver, "UBI_147")
            return False
    finally:
        utils.cerrar_driver(driver)

# =================================================================================
# UBI-148: SELECT 'APROXIMADA' + 'MIENTRAS LA APP EN USO' AND VERIFY CALCULATOR LOADS
# =================================================================================
def UBI_148():
    print("\n" + "=" * 60)
    print("🧪 UBI-148: SELECT 'APROXIMADA' + 'MIENTRAS LA APP EN USO' AND VERIFY CALCULATOR LOADS")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        print("🔐 PRECONDITION: EXECUTING LOGIN + REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)
        time.sleep(3)

        print("\n👉 STEP 1: VERIFYING LOCATION PERMISSION DIALOG IS DISPLAYED...")

        dialog_visible = False
        try:
            btn_mientras = driver.find_element(By.XPATH,
                '//*[contains(@text, "MIENTRAS") or contains(@content-desc, "MIENTRAS") or contains(@text, "Mientras") or contains(@content-desc, "Mientras")]'
            )
            if btn_mientras.is_displayed():
                dialog_visible = True
                print("   ✅ LOCATION PERMISSION DIALOG DETECTED.")
        except:
            pass

        if not dialog_visible:
            print("   ❌ LOCATION PERMISSION DIALOG NOT FOUND.")
            utils.tomar_screenshot(driver, "UBI_148_NO_DIALOG")
            _capture_evidence(driver, "UBI_148")
            return False

        print("\n👉 STEP 2: SELECTING 'APROXIMADA' LOCATION OPTION...")

        aproximada_selected = False
        try:
            aproximada = driver.find_element(By.XPATH,
                '//*[contains(@text, "Aproximada") or contains(@content-desc, "Aproximada")]'
            )
            if aproximada.is_displayed():
                aproximada.click()
                aproximada_selected = True
                print("   ✅ 'APROXIMADA' OPTION SELECTED.")
                time.sleep(2)
        except:
            pass

        if not aproximada_selected:
            print("   ⚠️ WARNING: COULD NOT SELECT 'APROXIMADA'.")

        utils.tomar_screenshot(driver, "UBI_148_APROXIMADA_SELECTED")

        print("\n   🔍 DEBUG: SCANNING BUTTONS AFTER SELECTING 'APROXIMADA'...")
        try:
            todos = driver.find_elements(By.XPATH, "//*")
            for i, elem in enumerate(todos):
                try:
                    text = elem.get_attribute("text") or ""
                    desc = elem.get_attribute("content-desc") or ""
                    if text or desc:
                        print(f"      [{i}] text='{text}' | desc='{desc}'")
                except:
                    pass
        except:
            pass

        print("\n👉 STEP 3: CLICKING 'MIENTRAS LA APP ESTÁ EN USO' BUTTON...")

        btn_clicked = False

        # ATTEMPT 1: BY TEXT (multiple variations)
        text_variations = [
            "MIENTRAS LA APP ESTÁ EN USO",
            "MIENTRAS LA APP ESTA EN USO",
            "Mientras la app está en uso",
            "Mientras la app esta en uso",
            "MIENTRAS LA APP",
            "Mientras la app"
        ]

        for variation in text_variations:
            if btn_clicked:
                break
            try:
                btn = driver.find_element(By.XPATH, f'//*[contains(@text, "{variation}")]')
                btn.click()
                btn_clicked = True
                print(f"   ✅ BUTTON CLICKED VIA @text: '{variation}'")
            except:
                pass

        if not btn_clicked:
            for variation in text_variations:
                if btn_clicked:
                    break
                try:
                    btn = driver.find_element(By.XPATH, f'//*[contains(@content-desc, "{variation}")]')
                    btn.click()
                    btn_clicked = True
                    print(f"   ✅ BUTTON CLICKED VIA @content-desc: '{variation}'")
                except:
                    pass

        if not btn_clicked:
            try:
                btn = driver.find_element(By.ID, "com.android.permissioncontroller:id/permission_allow_foreground_only_button")
                btn.click()
                btn_clicked = True
                print("   ✅ BUTTON CLICKED VIA RESOURCE-ID (permission_allow_foreground_only_button)")
            except:
                pass

        if not btn_clicked:
            print("   ❌ FAILED TO CLICK 'MIENTRAS LA APP ESTÁ EN USO' WITH ALL METHODS.")
            utils.tomar_screenshot(driver, "UBI_148_CLICK_FAILED")
            _capture_evidence(driver, "UBI_148")
            return False

        time.sleep(5)

        print("\n👉 STEP 4: VERIFYING CALCULATOR / CHARGING SCREEN LOADED...")

        calculator_loaded = False
        elementos_encontrados = []

        try:
            cobrar = driver.find_element(By.XPATH, config.XPATH_C_PANTALLA_COBRO)
            if cobrar.is_displayed():
                calculator_loaded = True
                elementos_encontrados.append("BUTTON: 'COBRAR'")
        except:
            pass

        try:
            display = driver.find_element(By.XPATH, config.XPATH_C_DISPLAY_MONTO)
            if display.is_displayed():
                calculator_loaded = True
                elementos_encontrados.append("DISPLAY: '\$0.00'")
        except:
            pass

        popup_found = False
        try:
            popup = driver.find_element(By.XPATH,
                '//*[contains(@text, "exitoso") or contains(@text, "éxito") or contains(@text, "correcto")]'
            )
            if popup.is_displayed():
                popup_found = True
                print("   ⚠️ UNEXPECTED GREEN POPUP DETECTED — STILL VALIDATING CALCULATOR...")
        except:
            pass

        print(f"\n   📋 CALCULATOR ELEMENTS FOUND: {len(elementos_encontrados)}")
        for elem in elementos_encontrados:
            print(f"      ✅ {elem}")

        if not popup_found:
            print("   ✅ NO SUCCESS POPUP DETECTED — DIRECT TRANSITION TO CALCULATOR.")

        if calculator_loaded:
            print("\n📸 TAKING SCREENSHOT OF CALCULATOR SCREEN...")
            utils.tomar_screenshot(driver, "UBI_148_SUCCESS")
            _capture_evidence(driver, "UBI_148")
            print("\n✅ UBI-148: SUCCESS — 'APROXIMADA' + 'MIENTRAS LA APP EN USO' GRANTED AND CALCULATOR LOADED.")
            return True
        else:
            print("\n❌ UBI-148 FAILED — CALCULATOR SCREEN DID NOT LOAD AFTER PERMISSION.")
            utils.tomar_screenshot(driver, "UBI_148_FAILED")
            _capture_evidence(driver, "UBI_148")
            print("\n🔍 SCANNING FOR VISIBLE TEXT ON CURRENT SCREEN FOR DEBUGGING...")
            try:
                todos = driver.find_elements(By.XPATH, "//*")
                for elem in todos:
                    t = elem.get_attribute("text")
                    if t and len(t) > 3:
                        print(f"   📝 VISIBLE TEXT: '{t}'")
            except:
                pass
            return False

    except Exception as e:
        print(f"\n💥 UBI-148 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "UBI_148_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)

# =================================================================================
# INTERNAL HELPER: APROXIMADA + SOLO ESTA VEZ → COBRAR → PRECISION DIALOG
# =================================================================================
def _helper_reach_precision_dialog(driver, wait):
    
    print("\n👉 STEP 1: VERIFYING LOCATION PERMISSION DIALOG IS DISPLAYED...")

    dialog_visible = False
    try:
        btn = driver.find_element(By.XPATH,
            '//*[contains(@text, "MIENTRAS") or contains(@content-desc, "MIENTRAS") or contains(@text, "Mientras") or contains(@content-desc, "Mientras")]'
        )
        if btn.is_displayed():
            dialog_visible = True
            print("   ✅ LOCATION PERMISSION DIALOG DETECTED.")
    except:
        pass

    if not dialog_visible:
        print("   ❌ LOCATION PERMISSION DIALOG NOT FOUND.")
        return False

    print("\n👉 STEP 2: SELECTING 'APROXIMADA' LOCATION OPTION...")

    try:
        aproximada = driver.find_element(By.XPATH,
            '//*[contains(@text, "Aproximada") or contains(@content-desc, "Aproximada")]'
        )
        aproximada.click()
        print("   ✅ 'APROXIMADA' OPTION SELECTED.")
        time.sleep(2)
    except:
        print("   ⚠️ WARNING: COULD NOT SELECT 'APROXIMADA'.")

    print("\n👉 STEP 3: CLICKING 'SOLO ESTA VEZ' BUTTON...")

    btn_clicked = False
    for attr in ['@text', '@content-desc']:
        for variation in ["SOLO ESTA VEZ", "Solo esta vez"]:
            if btn_clicked:
                break
            try:
                btn = driver.find_element(By.XPATH, f'//*[contains({attr}, "{variation}")]')
                btn.click()
                btn_clicked = True
                print(f"   ✅ 'SOLO ESTA VEZ' CLICKED VIA {attr}.")
            except:
                pass

    if not btn_clicked:
        print("   ❌ FAILED TO CLICK 'SOLO ESTA VEZ'.")
        return False

    time.sleep(5)

    print("\n👉 STEP 4: VERIFYING CALCULATOR LOADED...")

    calculator_loaded = False
    try:
        cobrar = driver.find_element(By.XPATH, '//*[@content-desc="Cobrar"]')
        if cobrar.is_displayed():
            calculator_loaded = True
            print("   ✅ CALCULATOR SCREEN LOADED.")
    except:
        pass

    if not calculator_loaded:
        print("   ❌ CALCULATOR DID NOT LOAD.")
        return False

    print("\n👉 STEP 5: CLICKING 'COBRAR' TO TRIGGER PRECISION CHANGE DIALOG...")

    try:
        cobrar = driver.find_element(By.XPATH, '//*[@content-desc="Cobrar"]')
        cobrar.click()
        print("   ✅ 'COBRAR' BUTTON CLICKED.")
        time.sleep(5)
    except Exception as e:
        print(f"   ❌ FAILED TO CLICK 'COBRAR': {e}")
        return False

    print("\n👉 STEP 6: VERIFYING PRECISION CHANGE DIALOG IS DISPLAYED...")

    precision_dialog = False
    elementos = []

    try:
        dialog = driver.find_element(By.XPATH,
            '//*[contains(@text, "aproximada a precisa") or contains(@content-desc, "aproximada a precisa") or contains(@text, "cambiar el acceso") or contains(@content-desc, "cambiar el acceso")]'
        )
        if dialog.is_displayed():
            precision_dialog = True
            elementos.append("TITLE: 'Cambiar acceso de aproximada a precisa'")
    except:
        pass

    try:
        btn_solo = driver.find_element(By.XPATH,
            '//*[contains(@text, "SOLO ESTA VEZ") or contains(@content-desc, "SOLO ESTA VEZ") or contains(@text, "Solo esta vez") or contains(@content-desc, "Solo esta vez")]'
        )
        if btn_solo.is_displayed():
            precision_dialog = True
            elementos.append("BUTTON: 'SOLO ESTA VEZ'")
    except:
        pass

    try:
        btn_seguir = driver.find_element(By.XPATH,
            '//*[contains(@text, "SEGUIR USANDO") or contains(@content-desc, "SEGUIR USANDO") or contains(@text, "Seguir usando") or contains(@content-desc, "Seguir usando")]'
        )
        if btn_seguir.is_displayed():
            precision_dialog = True
            elementos.append("BUTTON: 'SEGUIR USANDO UBICACIÓN APROXIMADA'")
    except:
        pass

    if elementos:
        print(f"   📋 PRECISION DIALOG ELEMENTS FOUND: {len(elementos)}")
        for elem in elementos:
            print(f"      ✅ {elem}")

    return precision_dialog


# =================================================================================
# UBI-149A: APROXIMADA + SOLO ESTA VEZ → COBRAR → PRECISION DIALOG → 'SOLO ESTA VEZ'
# =================================================================================
def UBI_149A():
    print("\n" + "=" * 60)
    print("🧪 UBI-149A: APROXIMADA → SOLO ESTA VEZ → COBRAR → PRECISION DIALOG → 'SOLO ESTA VEZ'")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        print("🔐 PRECONDITION: EXECUTING LOGIN + REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)
        time.sleep(3)

        precision_dialog = _helper_reach_precision_dialog(driver, wait)

        if not precision_dialog:
            utils.tomar_screenshot(driver, "UBI_149A_NO_PRECISION_DIALOG")
            _capture_evidence(driver, "UBI_149A")
            return False

        utils.tomar_screenshot(driver, "UBI_149A_PRECISION_DIALOG_VISIBLE")

        print("\n👉 STEP 7: CLICKING 'SOLO ESTA VEZ' ON PRECISION DIALOG...")

        btn_clicked = False
        for attr in ['@text', '@content-desc']:
            for variation in ["SOLO ESTA VEZ", "Solo esta vez"]:
                if btn_clicked:
                    break
                try:
                    btn = driver.find_element(By.XPATH, f'//*[contains({attr}, "{variation}")]')
                    btn.click()
                    btn_clicked = True
                    print(f"   ✅ 'SOLO ESTA VEZ' CLICKED VIA {attr}.")
                except:
                    pass

        if not btn_clicked:
            print("   ❌ FAILED TO CLICK 'SOLO ESTA VEZ'.")
            utils.tomar_screenshot(driver, "UBI_149A_CLICK_FAILED")
            _capture_evidence(driver, "UBI_149A")
            return False

        time.sleep(5)

        print("\n👉 STEP 8: VERIFYING CALCULATOR RELOADED...")

        calculator_loaded = False
        try:
            cobrar = driver.find_element(By.XPATH, '//*[@content-desc="Cobrar"]')
            if cobrar.is_displayed():
                calculator_loaded = True
        except:
            pass

        if calculator_loaded:
            utils.tomar_screenshot(driver, "UBI_149A_SUCCESS")
            _capture_evidence(driver, "UBI_149A")
            print("\n✅ UBI-149A: SUCCESS — PRECISION CHANGED VIA 'SOLO ESTA VEZ' AND CALCULATOR LOADED.")
            return True
        else:
            utils.tomar_screenshot(driver, "UBI_149A_FAILED")
            _capture_evidence(driver, "UBI_149A")
            print("\n❌ UBI-149A FAILED — CALCULATOR DID NOT LOAD AFTER PRECISION CHANGE.")
            return False

    except Exception as e:
        print(f"\n💥 UBI-149A CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "UBI_149A_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)


# =================================================================================
# UBI-149B: APROXIMADA + SOLO ESTA VEZ → COBRAR → PRECISION DIALOG → 'SEGUIR USANDO APROXIMADA'
# =================================================================================
def UBI_149B():
    print("\n" + "=" * 60)
    print("🧪 UBI-149B: APROXIMADA → SOLO ESTA VEZ → COBRAR → PRECISION DIALOG → 'SEGUIR USANDO APROXIMADA'")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        print("🔐 PRECONDITION: EXECUTING LOGIN + REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)
        time.sleep(3)

        precision_dialog = _helper_reach_precision_dialog(driver, wait)

        if not precision_dialog:
            utils.tomar_screenshot(driver, "UBI_149B_NO_PRECISION_DIALOG")
            _capture_evidence(driver, "UBI_149B")
            return False

        utils.tomar_screenshot(driver, "UBI_149B_PRECISION_DIALOG_VISIBLE")

        print("\n👉 STEP 7: CLICKING 'SEGUIR USANDO UBICACIÓN APROXIMADA'...")

        btn_clicked = False
        for attr in ['@text', '@content-desc']:
            for variation in ["SEGUIR USANDO UBICACIÓN APROXIMADA", "SEGUIR USANDO UBICACION APROXIMADA", "Seguir usando ubicación aproximada", "Seguir usando ubicacion aproximada", "SEGUIR USANDO", "Seguir usando"]:
                if btn_clicked:
                    break
                try:
                    btn = driver.find_element(By.XPATH, f'//*[contains({attr}, "{variation}")]')
                    btn.click()
                    btn_clicked = True
                    print(f"   ✅ 'SEGUIR USANDO UBICACIÓN APROXIMADA' CLICKED VIA {attr}.")
                except:
                    pass

        if not btn_clicked:
            print("   ❌ FAILED TO CLICK 'SEGUIR USANDO UBICACIÓN APROXIMADA'.")
            utils.tomar_screenshot(driver, "UBI_149B_CLICK_FAILED")
            _capture_evidence(driver, "UBI_149B")
            return False

        time.sleep(5)

        print("\n👉 STEP 8: VERIFYING CALCULATOR RELOADED...")

        calculator_loaded = False
        try:
            cobrar = driver.find_element(By.XPATH, '//*[@content-desc="Cobrar"]')
            if cobrar.is_displayed():
                calculator_loaded = True
        except:
            pass

        if calculator_loaded:
            utils.tomar_screenshot(driver, "UBI_149B_SUCCESS")
            _capture_evidence(driver, "UBI_149B")
            print("\n✅ UBI-149B: SUCCESS — KEPT APPROXIMATE LOCATION AND CALCULATOR LOADED.")
            return True
        else:
            utils.tomar_screenshot(driver, "UBI_149B_FAILED")
            _capture_evidence(driver, "UBI_149B")
            print("\n❌ UBI-149B FAILED — CALCULATOR DID NOT LOAD.")
            return False

    except Exception as e:
        print(f"\n💥 UBI-149B CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "UBI_149B_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)

# =================================================================================
# UBI-150: SELECT 'APROXIMADA' + 'NO PERMITIR' AND VERIFY CALCULATOR LOADS
# =================================================================================
def UBI_150():
    print("\n" + "=" * 60)
    print("🧪 UBI-150: SELECT 'APROXIMADA' + 'NO PERMITIR' → VERIFY 'PERMISO REQUERIDO' POPUP")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        print("🔐 PRECONDITION: EXECUTING LOGIN + REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)
        time.sleep(3)

        print("\n👉 STEP 1: VERIFYING LOCATION PERMISSION DIALOG IS DISPLAYED...")

        dialog_visible = False
        try:
            btn_mientras = driver.find_element(By.XPATH,
                '//*[contains(@text, "MIENTRAS") or contains(@content-desc, "MIENTRAS") or contains(@text, "Mientras") or contains(@content-desc, "Mientras")]'
            )
            if btn_mientras.is_displayed():
                dialog_visible = True
                print("   ✅ LOCATION PERMISSION DIALOG DETECTED.")
        except:
            pass

        if not dialog_visible:
            print("   ❌ LOCATION PERMISSION DIALOG NOT FOUND.")
            utils.tomar_screenshot(driver, "UBI_150_NO_DIALOG")
            _capture_evidence(driver, "UBI_150")
            return False

        print("\n👉 STEP 2: SELECTING 'APROXIMADA' LOCATION OPTION...")

        aproximada_selected = False
        try:
            aproximada = driver.find_element(By.XPATH,
                '//*[contains(@text, "Aproximada") or contains(@content-desc, "Aproximada")]'
            )
            if aproximada.is_displayed():
                aproximada.click()
                aproximada_selected = True
                print("   ✅ 'APROXIMADA' OPTION SELECTED.")
                time.sleep(2)
        except:
            pass

        if not aproximada_selected:
            print("   ⚠️ WARNING: COULD NOT SELECT 'APROXIMADA'.")

        utils.tomar_screenshot(driver, "UBI_150_APROXIMADA_SELECTED")

        print("\n   🔍 DEBUG: SCANNING BUTTONS AFTER SELECTING 'APROXIMADA'...")
        try:
            todos = driver.find_elements(By.XPATH, "//*")
            for i, elem in enumerate(todos):
                try:
                    text = elem.get_attribute("text") or ""
                    desc = elem.get_attribute("content-desc") or ""
                    if text or desc:
                        print(f"      [{i}] text='{text}' | desc='{desc}'")
                except:
                    pass
        except:
            pass

        print("\n👉 STEP 3: CLICKING 'NO PERMITIR' BUTTON (FIRST TIME)...")

        btn_clicked = False

        text_variations = [
            "NO PERMITIR",
            "No permitir",
        ]

        for variation in text_variations:
            if btn_clicked:
                break
            try:
                btn = driver.find_element(By.XPATH, f'//*[contains(@text, "{variation}")]')
                btn.click()
                btn_clicked = True
                print(f"   ✅ BUTTON CLICKED VIA @text: '{variation}'")
            except:
                pass

        if not btn_clicked:
            for variation in text_variations:
                if btn_clicked:
                    break
                try:
                    btn = driver.find_element(By.XPATH, f'//*[contains(@content-desc, "{variation}")]')
                    btn.click()
                    btn_clicked = True
                    print(f"   ✅ BUTTON CLICKED VIA @content-desc: '{variation}'")
                except:
                    pass

        if not btn_clicked:
            try:
                btn = driver.find_element(By.ID, "com.android.permissioncontroller:id/permission_deny_button")
                btn.click()
                btn_clicked = True
                print("   ✅ BUTTON CLICKED VIA RESOURCE-ID (permission_deny_button)")
            except:
                pass

        if not btn_clicked:
            print("   ❌ FAILED TO CLICK 'NO PERMITIR' (FIRST TIME) WITH ALL METHODS.")
            utils.tomar_screenshot(driver, "UBI_150_FIRST_DENY_FAILED")
            _capture_evidence(driver, "UBI_150")
            return False

        time.sleep(5)

        print("\n👉 STEP 4: VERIFYING CALCULATOR SCREEN LOADED...")

        calculator_loaded = False
        try:
            cobrar = driver.find_element(By.XPATH, config.XPATH_C_PANTALLA_COBRO)
            if cobrar.is_displayed():
                calculator_loaded = True
                print("   ✅ CALCULATOR SCREEN LOADED.")
        except:
            pass

        if not calculator_loaded:
            print("   ❌ CALCULATOR SCREEN DID NOT LOAD.")
            utils.tomar_screenshot(driver, "UBI_150_NO_CALCULATOR")
            _capture_evidence(driver, "UBI_150")
            return False

        utils.tomar_screenshot(driver, "UBI_150_CALCULATOR_AFTER_FIRST_DENY")

        print("\n👉 STEP 5: CLICKING 'COBRAR' BUTTON TO TRIGGER LOCATION DIALOG AGAIN...")

        try:
            cobrar = driver.find_element(By.XPATH, config.XPATH_C_PANTALLA_COBRO)
            cobrar.click()
            print("   ✅ 'COBRAR' BUTTON CLICKED.")
            time.sleep(5)
        except Exception as e:
            print(f"   ❌ FAILED TO CLICK 'COBRAR': {e}")
            utils.tomar_screenshot(driver, "UBI_150_COBRAR_FAILED")
            _capture_evidence(driver, "UBI_150")
            return False

        print("\n👉 STEP 6: VERIFYING LOCATION PERMISSION DIALOG APPEARED AGAIN...")

        second_dialog = False
        try:
            btn_no = driver.find_element(By.XPATH,
                '//*[contains(@text, "NO PERMITIR") or contains(@text, "No permitir") or contains(@content-desc, "NO PERMITIR") or contains(@content-desc, "No permitir")]'
            )
            if btn_no.is_displayed():
                second_dialog = True
                print("   ✅ LOCATION PERMISSION DIALOG APPEARED AGAIN.")
        except:
            pass

        if not second_dialog:
            print("   ❌ SECOND LOCATION PERMISSION DIALOG NOT DETECTED.")
            utils.tomar_screenshot(driver, "UBI_150_NO_SECOND_DIALOG")
            _capture_evidence(driver, "UBI_150")
            return False

        print("\n👉 STEP 7: CLICKING 'NO PERMITIR' BUTTON (SECOND TIME)...")

        btn_clicked = False

        for variation in text_variations:
            if btn_clicked:
                break
            try:
                btn = driver.find_element(By.XPATH, f'//*[contains(@text, "{variation}")]')
                btn.click()
                btn_clicked = True
                print(f"   ✅ BUTTON CLICKED VIA @text: '{variation}'")
            except:
                pass

        if not btn_clicked:
            for variation in text_variations:
                if btn_clicked:
                    break
                try:
                    btn = driver.find_element(By.XPATH, f'//*[contains(@content-desc, "{variation}")]')
                    btn.click()
                    btn_clicked = True
                    print(f"   ✅ BUTTON CLICKED VIA @content-desc: '{variation}'")
                except:
                    pass

        if not btn_clicked:
            try:
                btn = driver.find_element(By.ID, "com.android.permissioncontroller:id/permission_deny_button")
                btn.click()
                btn_clicked = True
                print("   ✅ BUTTON CLICKED VIA RESOURCE-ID (permission_deny_button)")
            except:
                pass

        if not btn_clicked:
            print("   ❌ FAILED TO CLICK 'NO PERMITIR' (SECOND TIME) WITH ALL METHODS.")
            utils.tomar_screenshot(driver, "UBI_150_SECOND_DENY_FAILED")
            _capture_evidence(driver, "UBI_150")
            return False

        time.sleep(5)

        print("\n👉 STEP 8: VERIFYING 'PERMISO REQUERIDO' POPUP IS DISPLAYED...")

        time.sleep(8)

        permiso_requerido = False
        elementos_encontrados = []

        try:
            titulo = driver.find_element(By.XPATH,
                '//*[@content-desc="Permiso Requerido"]'
            )
            if titulo.is_displayed():
                permiso_requerido = True
                elementos_encontrados.append("TITLE: 'Permiso Requerido'")
        except:
            pass

        try:
            desc = driver.find_element(By.XPATH,
                '//*[contains(@content-desc, "permiso de ubicación") or contains(@content-desc, "necesario para realizar")]'
            )
            if desc.is_displayed():
                permiso_requerido = True
                elementos_encontrados.append(f"DESCRIPTION: '{desc.get_attribute('content-desc')}'")
        except:
            pass

        try:
            btn_config = driver.find_element(By.XPATH,
                '//*[@content-desc="Abrir Configuración"]'
            )
            if btn_config.is_displayed():
                permiso_requerido = True
                elementos_encontrados.append("BUTTON: 'Abrir Configuración'")
        except:
            pass

        print(f"\n   📋 'PERMISO REQUERIDO' ELEMENTS FOUND: {len(elementos_encontrados)}")
        for elem in elementos_encontrados:
            print(f"      ✅ {elem}")

        if permiso_requerido:
            print("\n📸 TAKING SCREENSHOT OF 'PERMISO REQUERIDO' POPUP...")
            utils.tomar_screenshot(driver, "UBI_150_SUCCESS")
            _capture_evidence(driver, "UBI_150")
            print("\n✅ UBI-150: SUCCESS — 'PERMISO REQUERIDO' POPUP DISPLAYED AFTER DENYING 'APROXIMADA' LOCATION TWICE.")
            return True
        else:
            print("\n❌ UBI-150 FAILED — 'PERMISO REQUERIDO' POPUP NOT DETECTED.")
            utils.tomar_screenshot(driver, "UBI_150_FAILED")
            _capture_evidence(driver, "UBI_150")
            print("\n🔍 SCANNING FOR VISIBLE TEXT ON CURRENT SCREEN FOR DEBUGGING...")
            try:
                todos = driver.find_elements(By.XPATH, "//*")
                for elem in todos:
                    try:
                        t = elem.get_attribute("text") or ""
                        d = elem.get_attribute("content-desc") or ""
                        if (t and len(t) > 3) or (d and len(d) > 3):
                            print(f"   📝 text='{t}' | desc='{d}'")
                    except:
                        pass
            except:
                pass
            return False

    except Exception as e:
        print(f"\n💥 UBI-150 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "UBI_150_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)

# === MAIN EXECUTION === #
if __name__ == "__main__":

    logger, log_file, timestamp = utils.iniciar_reporte("OPERATIONALS_UBI")

    try:
        UBI_144()
        UBI_145()
        UBI_146()
        UBI_147()
        UBI_148()
        UBI_149A()
        UBI_149B()
        UBI_150()
        
    finally:
        utils.generar_reporte_html("OPERATIONALS_UBI", log_file, timestamp)
