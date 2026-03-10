"""
FILENAME: CRUD-TBL.py
DESCRIPTION: STANDARD TABLE COMPONENT DEEP VALIDATIONS
CONTENTS:
· CRUD-TBL-01: ACCESS MODULE WITH STANDARD TABLE LAYOUT
· CRUD-TBL-02: ACCESS TABLE AND CLICK EDIT ACTION
"""

import sys 
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time
import config 
import utils 

# ==========================================================
# CRUD-TBL-01: ACCESS MODULE WITH STANDARD TABLE LAYOUT
# ==========================================================
def CRUD_TBL_01():
    print("\n" + "=" * 60)
    print("CRUD-TBL-01: ACCESS MODULE WITH STANDARD TABLE LAYOUT")
    print("=" * 60)
    driver, wait = utils.iniciar_driver_web()

    try: 
        print("🔐 PRECONDITION: AUTHENTICATING USER...")
        driver.get(config.URL_MEMPHIS_WEB)
        time.sleep(2)
        utils.escribir_texto(driver, config.XPATH_WEB_USER, config.WEB_USUARIO_PRUEBA)
        utils.escribir_texto(driver, config.XPATH_WEB_PASS, config.WEB_PASS_PRUEBA)
        utils.click_boton(driver, config.XPATH_WEB_BTN_LOGIN)
        time.sleep(5) 
        
        MODULE_URL = "https://fat.memphis.mx/cat/bancoAdq" 
        print(f"🌐 NAVIGATING TO TABLE MODULE: {MODULE_URL}")
        driver.get(MODULE_URL)
        time.sleep(5)
        
        # STEP 1: CLICK THE 'NEW' / 'AGREGAR' BUTTON
        print("👉 STEP 1: CLICKING THE 'NUEVO' (ADD NEW) BUTTON...")
        try:
            XPATH_BTN_NUEVO = "//button[contains(translate(., 'NUEVO', 'nuevo'), 'nuevo') or contains(translate(., 'AGREGAR', 'agregar'), 'agregar')]"
            utils.click_boton(driver, XPATH_BTN_NUEVO)
        except:
            print("   ⚠️ TEXT BUTTON NOT FOUND. TRYING PRIME-NG 'PLUS' ICON...")
            XPATH_BTN_NUEVO_ICON = "//button[.//i[contains(@class, 'pi-plus')]]"
            utils.click_boton(driver, XPATH_BTN_NUEVO_ICON)
            
        print("⏳ WAITING FOR CREATION MODAL/FORM TO OPEN...")
        time.sleep(3)
        
        # DEEP VERIFICATION: DID THE FORM OPEN?
        print("🔍 VERIFYING THAT THE NEW RECORD FORM APPEARED...")
        form_opened = False
        
        try:
            driver.implicitly_wait(2)
            driver.find_element("xpath", "//p-dialog | //form | //div[contains(@class, 'modal')]")
            form_opened = True
            print("   🔹 CREATION MODAL/FORM DETECTED IN THE DOM.")
        except:
            print("   ⚠️ CREATION MODAL NOT DETECTED. CHECKING IF URL CHANGED INSTEAD...")
            if driver.current_url != MODULE_URL:
                form_opened = True
                print(f"   🔹 NAVIGATED TO NEW PAGE: {driver.current_url}")
        driver.implicitly_wait(10) 
        
        # FINAL VALIDATION
        print("📡 CAPTURING HTTP EVIDENCE...")
        utils.print_http_evidence(driver, "bancoAdq")
        if form_opened:
            print("📸 TAKING SCREENSHOT EVIDENCE...")
            utils.tomar_screenshot(driver, "CRUD_TBL_01_SUCCESS")
            print("✅ CRUD-TBL-01: SUCCESS")
        else:
            print("❌ CRUD-TBL-01: FAILED")
            utils.tomar_screenshot(driver, "CRUD_TBL_01_FAILED")

    except Exception as e:
        print(f"❌ CRUD-TBL-01 CRITICAL ERROR: {e}")
        try: utils.tomar_screenshot(driver, "CRUD_TBL_01_TECHNICAL_ERROR")
        except: pass
    finally:
        print("🏁 CLOSING BROWSER...")
        driver.quit()

# ================================================
# CRUD_TBL_02: ACCESS TABLE AND CLICK EDIT ACTION
# ================================================
def CRUD_TBL_02():
    print("\n" + "=" * 60)
    print("CRUD_TBL_02: ACCESS TABLE AND CLICK EDIT ACTION")
    print("=" * 60)
    driver, wait = utils.iniciar_driver_web()

    try: 
        print("🔐 PRECONDITION: AUTHENTICATING USER...")
        driver.get(config.URL_MEMPHIS_WEB)
        time.sleep(2)
        utils.escribir_texto(driver, config.XPATH_WEB_USER, config.WEB_USUARIO_PRUEBA)
        utils.escribir_texto(driver, config.XPATH_WEB_PASS, config.WEB_PASS_PRUEBA)
        utils.click_boton(driver, config.XPATH_WEB_BTN_LOGIN)
        time.sleep(5) 
        
        # NAVIGATE TO THE SPECIFIC MODULE YOU REQUESTED
        MODULE_URL = "https://fat.memphis.mx/cat/bancoAdq" 
        print(f"🌐 NAVIGATING TO TABLE MODULE: {MODULE_URL}")
        driver.get(MODULE_URL)
        time.sleep(5)
        
        # STEP 1: CLICK THE 'EDIT' (PENCIL) BUTTON IN THE FIRST ROW
        print("👉 STEP 1: CLICKING THE 'EDIT' (PENCIL) BUTTON IN THE FIRST ROW...")
        XPATH_BTN_EDIT = "//p-table//tbody/tr[1]//button[.//span[contains(@class, 'pi-pencil')]]"
        utils.click_boton(driver, XPATH_BTN_EDIT)
        print("⏳ WAITING FOR EDIT MODAL/FORM TO OPEN...")
        time.sleep(3)
        
        # VALIDATION: DID THE FORM OR MODAL OPEN?
        print("🔍 VERIFYING THAT THE EDIT FORM APPEARED...")
        form_opened = False
        
        try:
            driver.implicitly_wait(2)
            driver.find_element("xpath", "//p-dialog | //form | //div[contains(@class, 'modal')]")
            form_opened = True
            print("   🔹 EDIT MODAL/FORM DETECTED IN THE DOM.")
        except:
            print("   ⚠️ EDIT MODAL NOT DETECTED. CHECKING IF URL CHANGED INSTEAD...")
            if driver.current_url != MODULE_URL:
                form_opened = True
                print(f"   🔹 NAVIGATED TO EDIT PAGE: {driver.current_url}")
        
        driver.implicitly_wait(10)
        
        # FINAL EVIDENCE
        print("📡 CAPTURING HTTP EVIDENCE...")
        
        utils.print_http_evidence(driver, "bancoAdq")
        if form_opened:
            print("📸 TAKING SCREENSHOT EVIDENCE...")
            utils.tomar_screenshot(driver, "CRUD_TBL_02_SUCCESS")
            print("✅ CRUD-TBL-02: SUCCESS")
        else:
            print("❌ CRUD-TBL-02: FAILED")
            utils.tomar_screenshot(driver, "CRUD_TBL_02_FAILED")

    except Exception as e:
        print(f"❌ CRUD-TBL-02 CRITICAL ERROR: {e}")
        try: utils.tomar_screenshot(driver, "CRUD_TBL_02_TECHNICAL_ERROR")
        except: pass
    finally:
        print("🏁 CLOSING BROWSER...")
        driver.quit()


# === MAIN EXECUTION ===
if __name__ == "__main__":
    
    logger, log_file, timestamp = utils.iniciar_reporte("CRUD_TBL")
    
    try:
        #CRUD_TBL_01()
        CRUD_TBL_02()
        
    finally:
        logger.close()
        #utils.generar_reporte_html("CRUD_TBL", log_file, timestamp)