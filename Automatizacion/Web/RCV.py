"""
FILENAME: RCV.PY
DESCRIPTION: RECOVERY PASSWORD ON WEB PLATFORM
CONTENTS:
· RCV-001: HOME PAGE, CLICK ON RECOVERY LINK
· RCV-002: PASSWORD RECOVERY PAGE (SEND EMAIL)
"""

import sys 
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time
import config 
import utils 

# ==================================================
# RCV-001: HOME PAGE, CLICK ON RECOVERY LINK
# ==================================================
def RCV_001():
    print("\n" + "=" * 60)
    print("RCV-001: HOME PAGE, CLICK ON RECOVERY LINK")
    print("=" * 60)
    driver, wait = utils.iniciar_driver_web()

    try: 
        print(f"🌐 NAVIGATING TO: {config.URL_MEMPHIS_WEB}")
        driver.get(config.URL_MEMPHIS_WEB)
        time.sleep(3)
        
        print("👉 CLICKING 'FORGOT PASSWORD' (INGRESA AQUI) LINK...")
        utils.click_boton(driver, config.XPATH_WEB_TXT_INGRESA_AQUI)
        time.sleep(3)
        
        print("📡 CAPTURING HTTP EVIDENCE...")
        utils.print_http_evidence(driver, "auth")
        
        print("📸 TAKING SCREENSHOT EVIDENCE...")
        utils.tomar_screenshot(driver, "RCV_001_SUCCESS")
        
        print("✅ RCV-001: SUCCESS")

    except Exception as e:
        print(f"❌ RCV-001 FAILED: {e}")
        try: utils.tomar_screenshot(driver, "RCV_001_FAILED")
        except: pass
    finally:
        print("🏁 CLOSING BROWSER...")
        driver.quit()

# ==================================================
# RCV-002: PASSWORD RECOVERY PAGE (SEND EMAIL)
# ==================================================
def RCV_002():
    print("\n" + "=" * 60)
    print("RCV-002: PASSWORD RECOVERY PAGE (SEND EMAIL)")
    print("=" * 60)
    driver, wait = utils.iniciar_driver_web()

    try:
        print(f"🌐 NAVIGATING TO: {config.URL_MEMPHIS_WEB}")
        driver.get(config.URL_MEMPHIS_WEB)
        time.sleep(3)
        
        print("👉 CLICKING 'FORGOT PASSWORD' (INGRESA AQUI) LINK...")
        utils.click_boton(driver, config.XPATH_WEB_TXT_INGRESA_AQUI)
        time.sleep(2)
        
        print("✍️ ENTERING USERNAME & CLICKING SEND BUTTON...")
        utils.escribir_texto(driver, config.XPATH_WEB_USER, config.WEB_USUARIO_PRUEBA)
        utils.click_boton(driver, config.XPATH_WEB_BTN_ENVIAR)
        
        print("⏳ WAITING FOR SYSTEM CONFIRMATION...")
        # SHORT WAIT TO CATCH THE GREEN TOAST NOTIFICATION BEFORE IT VANISHES
        time.sleep(1.5)
        
        print("📸 TAKING SCREENSHOT EVIDENCE (CAPTURING SUCCESS POPUP)...")
        utils.tomar_screenshot(driver, "RCV_002_SUCCESS")
        
        print("📡 CAPTURING HTTP EVIDENCE...")
        utils.print_http_evidence(driver, "auth")
        
        # VERIFY IF THE ELEMENT ACTUALLY EXISTS IN THE DOM
        mensaje_detectado = utils.verificar_existencia(wait, config.XPATH_MSJ_EXITO_RCV, "SUCCESS MESSAGE: EMAIL SENT", driver)
        
        if mensaje_detectado:
            print("✅ RCV-002: SUCCESS")
        else:
            print("❌ RCV-002 FAILED: THE GREEN CONFIRMATION MESSAGE DID NOT APPEAR.")
            utils.tomar_screenshot(driver, "RCV_002_FAILED")

    except Exception as e:
        print(f"❌ RCV-002 CRITICAL ERROR: {e}")
        try: utils.tomar_screenshot(driver, "RCV_002_TECHNICAL_ERROR")
        except: pass
        
    finally:
        print("🏁 CLOSING BROWSER...")
        driver.quit()

# === MAIN EXECUTION ===
if __name__ == "__main__":
    
    # START LOG RECORDER
    logger, log_file, timestamp = utils.iniciar_reporte("RCV")
    
    try:
        RCV_001()
        RCV_002()
        
    finally:
        # STOP RECORDER AND GENERATE HTML
        logger.close()
        utils.generar_reporte_html("RCV", log_file, timestamp)
        #utils.generar_zip_evidencias("RCV", logger, log_file, timestamp)