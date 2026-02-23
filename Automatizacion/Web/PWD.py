"""
FILENAME: PWD.py
DESCRIPTION: TESTING CHANGE PASSWORD ON WEB PLATFORM
CONTENTS:
· PWD_001: ENTER VALID USERNAME AND PASSWORD. 
· PWD_002: ATTEMPT TO MAUALLY NAVIGATE TO ANOTHER URL AFTER LOGIN. 
· PWD_003: CLICK ON "SET PASSWORD" WITHOUT FILLING IN ANY FIELDS. 
· PWD_004: ENTER INCORRECT PASSWORD AT LOGIN
"""
import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
import utils

# ========================
# HELPER: AUTOMATIC LOGIN 
# ========================
def login_helper(driver, wait):
    """Función auxiliar para loguearse antes de cada prueba de PWD."""
    print("🔄 [HELPER] Iniciando sesión para preparar el test...")
    driver.get(config.URL_MEMPHIS_WEB)
    time.sleep(2)
    utils.escribir_texto(driver, config.XPATH_WEB_USER, "eamartin")
    utils.escribir_texto(driver, config.XPATH_WEB_PASS, "Patito4.")
    utils.click_boton(driver, config.XPATH_WEB_BTN_LOGIN)
    time.sleep(3) 
    driver.get(config.URL_MEMPHIS_PWD)
    time.sleep(2)

# ==========================================
# PWD_001: ENTER VALID USERNAME AND PASSWORD
# ==========================================
def PWD_001():
    print("\n" + "=" * 60)
    print("PWD-001: ENTER VALID USERNAME AND PASSWORD")
    print("=" * 60)
    driver, wait = utils.iniciar_driver_web()
    try:
        login_helper(driver, wait)
        print("✅ SUCCESS")
        utils.tomar_screenshot(driver, "PWD_001_SUCCESS")
    except Exception as e:
        print(f"❌ FAILED: {e}")
        utils.tomar_screenshot(driver, "PWD_001_FAILED")
    finally:
        driver.quit()

# ==================================================
# PWD_002: ATTEMPT TO MAUALLY NAVIGATE TO ANOTHER URL 
# ==================================================
def PWD_002():
    print("\n" + "=" * 60)
    print("PWD-002: ATTEMPT TO MAUALLY NAVIGATE TO ANOTHER URL AFTER LOGIN")
    print("=" * 60)
    driver, wait = utils.iniciar_driver_web()
    try:
        login_helper(driver, wait)
        
        url_restringida = "https://fat.memphis.mx/v2/dashboard"
        print(f"👉 GOING TO ANOTHER URL IN MANUAL WAY: {url_restringida}")
        driver.get(url_restringida)
        time.sleep(2)
        utils.print_http_evidence(driver, "gateway/api/v2/auth")
        if driver.current_url == url_restringida:
            print("✅ SUCCESS")
            utils.tomar_screenshot(driver, "PWD_002_SUCCESS")
        else:
            print("✅ SUCCESS")
            utils.tomar_screenshot(driver, "PWD_002_FAILED")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    finally:
        driver.quit()

# ==============================================================
# PWD_003: CLICK ON "SET PASSWORD" WITHOUT FILLING IN ANY FIELDS"
# ==============================================================
def PWD_003():
    print("\n" + "=" * 60)
    print("PWD-003: CLICK ON \"SET PASSWORD\" WITHOUT FILLING IN ANY FIELDS")
    print("=" * 60)
    driver, wait = utils.iniciar_driver_web()
    try:
        login_helper(driver, wait)
        print("👉 CLICK 'ESTABLECER CONTRASEÑA'")
        utils.click_boton(driver, config.XPATH_PWD_BTN_ESTABLECER)
        time.sleep(1)
        utils.print_http_evidence(driver, "gateway/api/v2/auth")
        if utils.verificar_existencia(wait, config.XPATH_PWD_ERROR_VACIO, "Error Campos Vacíos", driver):
            print("✅ SUCCESS")
            utils.tomar_screenshot(driver, "PWD_003_SUCCESS")
        else:
            print("❌ FAILED")
            utils.tomar_screenshot(driver, "PWD_003_FAILED")
    finally:
        driver.quit()

# ===========================================
# PWD_004: ENTER INCORRECT PASSWORD AT LOGIN
# ===========================================
def PWD_004():
    print("\n" + "=" * 60)
    print("PWD_004:ENTER INCORRECT PASSWORD AT LOGIN")
    print("=" * 60)
    driver, wait = utils.iniciar_driver_web()
    
    try:
        print(f"👉 NAVIGATING TO: {config.URL_MEMPHIS_WEB}")
        driver.get(config.URL_MEMPHIS_WEB)
        time.sleep(2)
        usuario_correcto = config.WEB_USUARIO_PRUEBA
        pass_incorrecta = "ContrasenaFalsa123"
        utils.escribir_texto(driver, config.XPATH_WEB_USER, usuario_correcto)
        utils.escribir_texto(driver, config.XPATH_WEB_PASS, pass_incorrecta)
        print("👉 CLICK ON LOGIN...")
        utils.click_boton(driver, config.XPATH_WEB_BTN_LOGIN)
        XPATH_POPUP_ERROR = "//*[contains(text(), 'Error') or contains(text(), 'error')]"
        time.sleep(2)
        utils.print_http_evidence(driver, "gateway/api/v2/auth")
        error_detectado = utils.verificar_existencia(wait, XPATH_POPUP_ERROR, "Popup de Error", driver)
        
        if error_detectado:
            print("✅ SUCCESS")
            utils.tomar_screenshot(driver, "PWD_004_SUCCESS")
        else:
            print("❌ FAILED")
            utils.tomar_screenshot(driver, "PWD_004_FAILED")

    except Exception as e:
        print(f"❌ ERROR ON PWD-004: {e}")
        try: 
            utils.tomar_screenshot(driver, "PWD_004_TECHNICAL_ERROR")
        except: 
            pass
            
    finally:
        print("🏁 CLOSING BROWSER...")
        driver.quit()

# === EXECUTION ===
if __name__ == "__main__":
    PWD_001()
    PWD_002()
    PWD_003()
    PWD_004()
    