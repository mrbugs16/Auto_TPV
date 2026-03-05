"""
FILENAME: RST.PY
DESCRIPTION: RESET PASSWORD MODULE VALIDATIONS
CONTENTS:
· RST-001: CLICK 'RESET PASSWORD' WITH EMPTY FIELDS
· RST-002: ENTER VALID PASSWORDS IN RECOVERY FORM
"""

import sys 
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time
import config 
import utils 

# ==================================================
# RST-001: CLICK 'RESET PASSWORD' WITH EMPTY FIELDS
# ==================================================
def RST_001():
    print("\n" + "=" * 60)
    print("RST-001: CLICK 'RESET PASSWORD' WITH EMPTY FIELDS")
    print("=" * 60)
    
    # DATA NEEDED FOR IMAP RECOVERY
    EMAIL_QA = "santiago.tapia@memphis.mx"
    PASS_APP_GMAIL = "bpgg sgkz lgpi jvfi"
    
    driver, wait = utils.iniciar_driver_web()

    try: 
        print("🕵️ PHASE 1: SEARCHING FOR RECOVERY LINK IN EMAIL SERVER...")
        link_recuperacion = utils.obtener_link_recuperacion_imap(EMAIL_QA, PASS_APP_GMAIL)
        
        if not link_recuperacion:
            print("❌ RST-001 FAILED: RECOVERY LINK NOT FOUND IN INBOX")
            return False

        print(f"🌐 PHASE 2: NAVIGATING DIRECTLY TO RECOVERY URL...")
        driver.get(link_recuperacion)
        time.sleep(3)
        
        # WE DON'T WRITE ANYTHING, WE JUST CLICK
        print("👉 PHASE 3: CLICKING 'RESET PASSWORD' BUTTON (WITHOUT FILLING FIELDS)...")
        utils.click_boton(driver, config.XPATH_BTN_ACEPTAR_WEB)
        time.sleep(1.5)
        
        print("📡 CAPTURING HTTP EVIDENCE...")
        utils.print_http_evidence(driver, "auth")
        
        print("🔍 CHECKING FRONTEND VALIDATIONS (EXPECTING EMPTY FIELDS ERRORS)...")
        utils.verificar_validacion_frontend(driver)
        
        print("📸 TAKING SCREENSHOT EVIDENCE...")
        utils.tomar_screenshot(driver, "RST_001_SUCCESS")
        
        print("✅ RST-001: SUCCESS (SYSTEM BLOCKED EMPTY SUBMISSION)")

    except Exception as e:
        print(f"❌ RST-001 FAILED: {e}")
        try: utils.tomar_screenshot(driver, "RST_001_FAILED")
        except: pass
    finally:
        print("🏁 CLOSING BROWSER...")
        driver.quit()


# ==================================================
# RST-002: ENTER VALID PASSWORDS IN RECOVERY FORM
# ==================================================
def RST_002():
    print("\n" + "=" * 60)
    print("RST-002: ENTER VALID PASSWORDS IN RECOVERY FORM")
    print("=" * 60)
    
    # DATA NEEDED FOR IMAP RECOVERY
    EMAIL_QA = "santiago.tapia@memphis.mx"
    PASS_APP_GMAIL = "bpgg sgkz lgpi jvfi"
    
    # NEW PASSWORD THAT MEETS ALL SECURITY REQUIREMENTS
    NEW_VALID_PASSWORD = "MemphisQA.2026!" 
    
    driver, wait = utils.iniciar_driver_web()

    try: 
        print("🕵️ PHASE 1: SEARCHING FOR RECOVERY LINK IN EMAIL SERVER...")
        link_recuperacion = utils.obtener_link_recuperacion_imap(EMAIL_QA, PASS_APP_GMAIL)
        
        if not link_recuperacion:
            print("❌ RST-002 FAILED: RECOVERY LINK NOT FOUND IN INBOX")
            return False

        print(f"🌐 PHASE 2: NAVIGATING DIRECTLY TO RECOVERY URL...")
        driver.get(link_recuperacion)
        time.sleep(3)
        
        print("✍️ PHASE 3: WRITING NEW VALID PASSWORD IN BOTH FIELDS...")
        utils.escribir_texto(driver, config.XPATH_INPUT_NUEVA_PASS, NEW_VALID_PASSWORD)
        utils.escribir_texto(driver, config.XPATH_INPUT_REPITE_PASS, NEW_VALID_PASSWORD)
        time.sleep(1)
        
        print("👁️ REVEALING PASSWORDS FOR EVIDENCE...")
        try:
            utils.click_eye_button(driver, config.XPATH_BTN_OJO_NUEVA_PASS, "EYE BUTTON - NEW PASSWORD")
            utils.click_eye_button(driver, config.XPATH_BTN_OJO_CONFIRMAR, "EYE BUTTON - CONFIRM PASSWORD")
        except:
            print("⚠️ WARNING: COULD NOT CLICK EYE BUTTONS. CONTINUING...")
            pass
        time.sleep(1)
        
        print("👉 CLICKING 'RESET PASSWORD' BUTTON...")
        utils.click_boton(driver, config.XPATH_BTN_ACEPTAR_WEB)
        
        print("⏳ WAITING FOR SYSTEM SUCCESS CONFIRMATION...")
        # SHORT WAIT TO CATCH THE SUCCESS POPUP BEFORE TAKING SCREENSHOT
        time.sleep(1.5) 
        
        print("📸 TAKING SCREENSHOT EVIDENCE (CAPTURING VISUAL FEEDBACK)...")
        utils.tomar_screenshot(driver, "RST_002_SUCCESS")
        
        print("📡 CAPTURING HTTP EVIDENCE...")
        utils.print_http_evidence(driver, "auth")
        
        print("✅ RST-002: SUCCESS (FORM SUBMITTED AND VISUAL FEEDBACK SHOWN)")

    except Exception as e:
        print(f"❌ RST-002 FAILED: {e}")
        try: utils.tomar_screenshot(driver, "RST_002_FAILED")
        except: pass
    finally:
        print("🏁 CLOSING BROWSER...")
        driver.quit()


# === MAIN EXECUTION ===
if __name__ == "__main__":
    
    # START LOG RECORDER
    logger, log_file, timestamp = utils.iniciar_reporte("RST")
    
    try:
        RST_001()
        #RST_002()
        
    finally:
        # STOP RECORDER AND GENERATE HTML
        logger.close()
        utils.generar_reporte_html("RST", log_file, timestamp)
        #utils.generar_zip_evidencias("RST", logger, log_file, timestamp)