"""
FILENAME: RCV.py
DESCRIPTION: RECOVERY PASSWORD ON WEB PLATFORM
CONTENTS:
· RCV_001: HOME PAGE, USER NOT LOGGED IN.
· RCV_002: PASSWORD RECOVERY PAGE
"""

import sys 
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time
import config 
import utils 


# =======================================
# RCV_001: HOME PAGE, USER NOT LOGGED IN
# ======================================
def RCV_001():
    print("\n" + "=" * 60)
    print("RCV-001: HOME PAGE, USER NOT LOGGED IN")
    print("=" * 60)
    driver, wait = utils.iniciar_driver_web()

    try: 
        print(f"NAVIGATE TO: {config.URL_MEMPHIS_WEB}")
        driver.get(config.URL_MEMPHIS_WEB)
        url_antes = driver.current_url
        time.sleep(3)
        print("✍️ WRITING USER AND PASSWORD...")
        utils.escribir_texto(driver, config.XPATH_WEB_USER, config.WEB_USUARIO_PRUEBA)
        utils.escribir_texto(driver, config.XPATH_WEB_PASS, config.WEB_PASS_PRUEBA)
        print("👉 CLICKING 'LOGIN BUTTON'...")
        utils.click_boton(driver, config.XPATH_WEB_BTN_LOGIN)
        print("⏳ WAITING SCREEN TRANSITION...")
        time.sleep(4) 
        utils.print_http_evidence(driver, "gateway/api/v2/auth")
        
        url_despues = driver.current_url
        print(f"   🔹 URL Antes:   {url_antes}")
        print(f"   🔹 URL Después: {url_despues}")

        if url_antes != url_despues: 
            print("\n✅ SUCCESS")
            utils.tomar_screenshot(driver, "RCV_001_SUCCESS")
        else:
            print("⚠ La URL DOES NOT CHANGE.")
           
            try:
                driver.implicitly_wait(2) 
                driver.find_element("xpath", config.XPATH_WEB_BTN_LOGIN)
                print("❌ FAILED.")
                utils.tomar_screenshot(driver, "RCV_001_FALLO_URL_IGUAL")
                raise Exception("ASSERTION FAILED")
            except:
                print("✅ SUCCESS")
                utils.tomar_screenshot(driver, "RCV_001_SUCCESS_B")

    except Exception as e:
        print(f"❌ ERROR : {e}")
        try: utils.tomar_screenshot(driver, "RCV_001_TECHNICAL_ERROR")
        except: pass
        
    finally:
        print("🏁 CLOSING BROWSER...")
        driver.quit()

# ================================
# RCV_002: PASSWORD RECOVERY PAGE
# ================================
def RCV_002():
    print("\n" + "=" * 60)
    print("RCV-002: PASSWORD RECOVERY PAGE")
    print("=" * 60)
    driver, wait = utils.iniciar_driver_web()

    try:
        driver.get(config.URL_MEMPHIS_WEB)
        time.sleep(2)
        print("👉 CLICKING 'INGRESA AQUI'...")
        utils.click_boton(driver, config.XPATH_WEB_TXT_INGRESA_AQUI)
        print("✍️ ENTER USERNAME & CLICKING 'SEND BUTTON'...")
        utils.escribir_texto(driver, config.XPATH_WEB_USER, config.WEB_USUARIO_PRUEBA)
        utils.click_boton(driver, config.XPATH_WEB_BTN_ENVIAR)
        print("⏳ WAITING FOR SYSTEM CONFIRMATION...")
        mensaje_detectado = utils.verificar_existencia(wait, config.XPATH_MSJ_EXITO_RCV, "Mensaje: Se ha enviado un mail")
        utils.print_http_evidence(driver, "gateway/api/v2/auth")
        
        if mensaje_detectado:
            print("\n✅ SUCCESS")
            utils.tomar_screenshot(driver, "RCV_002_SUCCESS")
        else:
            error_msg = "ASSERTION FAILED: THE CONFIRMATION GREEN MESSAGE DID NOT APPEAR."
            utils.tomar_screenshot(driver, "RCV_002_FAILED")
            raise Exception(error_msg)

    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        
    finally:
        print("🏁 CLOSING BROWSER...")
        driver.quit()



if __name__ == "__main__":
    RCV_001()
    RCV_002()