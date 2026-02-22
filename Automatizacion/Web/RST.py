"""
FILENAME: RST.py
DESCRIPTION: TESTING PASSWORD RESET ON WEB PLATFORM
CONTENTS:
· RST_001: PASSWORD RECOVERY LINK 
· RST_002: PASSWORD RECOVERY PROCESS (VALID USER)
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time
import config
import utils 

# ================================
# RST_001: PASSWORD RECOVERY LINK 
# ================================
def RST_001():
    print("\n" + "=" * 60)
    print("RST-001: PASSWORD RECOVERY LINK")
    print("=" * 60)
    driver, wait = utils.iniciar_driver_web()

    try: 
        print(f"👉 NAVIGATE TO: {config.URL_MEMPHIS_WEB}")
        driver.get(config.URL_MEMPHIS_WEB)
        print("👉 CLICKING 'ENTER HERE' & VALIDATING CHANGING SCREEN...")
        utils.click_boton(driver, config.XPATH_WEB_TXT_INGRESA_AQUI)
        time.sleep(2) 
        titulo_esperado = "Olvidaste tu contraseña"
        es_visible = utils.verificar_existencia(wait, config.XPATH_WEB_TITULO_OLVIDASTE, "Título Recuperación", driver)
        time.sleep(4)
        utils.print_http_evidence(driver, "gateway/api/v2/auth")
        if es_visible:
            print("\n✅ SUCCESS")
            utils.tomar_screenshot(driver, "RST_001_SUCCESS")
        else:
            print("\n❌ FAILED")
            utils.tomar_screenshot(driver, "RST_001_FAIL")
            raise Exception("No cambiamos de pantalla correctamente.")

    except Exception as e:
        print(f"❌ CRITICAL ERROR IN RST_001: {e}")
        try: utils.tomar_screenshot(driver, "RST_001_TECHNICAL_ERROR")
        except: pass
            
    finally:
        print("🏁 CLOSING BROWSER...")
        driver.quit()

# ===============================================
# RST_002: PASSWORD RECOVERY PROCESS (VALID USER)
# ===============================================
def RST_002():
    print("\n" + "=" * 60)
    print("RST-002: PASSWORD RECOVERY PROCESS (VALID USER) ")
    print("=" * 60)
    driver, wait = utils.iniciar_driver_web()

    try:
        print(f"👉 NAVIGATE TO: {config.URL_MEMPHIS_WEB}")
        driver.get(config.URL_MEMPHIS_WEB)
        print("👉 CLICKING 'INGRESA AQUI'...")
        utils.click_boton(driver, config.XPATH_WEB_TXT_INGRESA_AQUI)
        time.sleep(2) 
        print(f"✍️ ENTER USERNAME: {config.WEB_USUARIO_PRUEBA}...")
        utils.escribir_texto(driver, config.XPATH_WEB_USER, config.WEB_USUARIO_PRUEBA)
        print("👉 CLICKING 'ENVIAR' BUTTON...")
        utils.click_boton(driver, config.XPATH_WEB_BTN_ENVIAR)
        print("⏳ WAITING FOR SUCCESS POPUP...")
        mensaje_detectado = utils.verificar_existencia(wait, config.XPATH_MSJ_EXITO_RCV, "SUCCESS GREEN POPUP", driver)
        utils.print_http_evidence(driver, "gateway/api/v2/auth")
        
        if mensaje_detectado:
            print("\n✅ SUCCESS")
            utils.tomar_screenshot(driver, "RST_002_SUCCESS")
        else:
            print("\n❌ FAILED: POPUP NOT DETECTED")
            utils.tomar_screenshot(driver, "RST_002_FAILED")
            raise Exception("No se detectó confirmación del sistema.")

    except Exception as e:
        print(f"❌ CRITICAL ERROR IN RST-002: {e}")
        try: 
            utils.tomar_screenshot(driver, "RST_002_TECHNICAL_ERROR")
        except: 
            pass
        
    finally:
        print("🏁 CLOSING BROWSER...")
        driver.quit()
        
# === EXECUTION ===
if __name__ == "__main__":
    RST_001()
    RST_002()