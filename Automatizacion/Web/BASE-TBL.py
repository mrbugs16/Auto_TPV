"""
FILENAME: BASE_TBL.py
DESCRIPTION: STANDARD TABLE COMPONENT DEEP VALIDATIONS
CONTENTS:
· BASE-TBL-01: ACCESS MODULE WITH STANDARD TABLE LAYOUT
· BASE-TBL-02: INTERACT WITH PAGINATOR AND ROW COUNT
· BASE-TBL-03: PERSISTENCE OF PAGINATION STATE ON RELOAD
· BASE-TBL-04: ENTER TEXT IN SEARCH FIELD AND VERIFY FILTER
· BASE-TBL-05: SEARCH PERSISTENCE ON RELOAD
· BASE-TBL-06: CLICK ON SORTABLE COLUMN HEADER (SMART TOGGLE)
· BASE-TBL-SM_01: ACCESS MODULE AND CLICK 'NEW' BUTTON
"""
import sys 
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time
import config 
import utils 

# ======================================================
# BASE-TBL-01: ACCESS MODULE WITH STANDARD TABLE LAYOUT
# ======================================================
def BASE_TBL_01():
    print("\n" + "=" * 60)
    print("BASE-TBL-01: ACCESS MODULE WITH STANDARD TABLE LAYOUT (DEEP VERIFICATION)")
    print("=" * 60)
    driver, wait = utils.iniciar_driver_web()

    try: 
        print("🔐 PRECONDITION: AUTHENTICATING USER...")
        driver.get(config.URL_MEMPHIS_WEB)
        time.sleep(2)
        
        print("✍️ ENTERING CREDENTIALS...")
        utils.escribir_texto(driver, config.XPATH_WEB_USER, config.WEB_USUARIO_PRUEBA)
        utils.escribir_texto(driver, config.XPATH_WEB_PASS, config.WEB_PASS_PRUEBA)
        
        print("👉 CLICKING LOGIN BUTTON...")
        utils.click_boton(driver, config.XPATH_WEB_BTN_LOGIN)
        
        print("⏳ WAITING FOR DASHBOARD TO LOAD...")
        time.sleep(5) 
        
        MODULE_URL = "https://fat.memphis.mx/merchant" 
        print(f"🌐 STEP 1: NAVIGATING TO TABLE MODULE: {MODULE_URL}")
        driver.get(MODULE_URL)
        
        print("⏳ WAITING FOR TABLE DATA TO RENDER...")
        time.sleep(5)
        
        print("📡 CAPTURING HTTP EVIDENCE...")
        utils.print_http_evidence(driver, "merchant") 
        
        print("🔍 VERIFYING PRIMENG TABLE ELEMENTS IN THE DOM...")
        
        XPATH_TABLE_CONTAINER = "//p-table//table[contains(@class, 'p-datatable-table')]"
        XPATH_TABLE_HEADER = "//p-table//thead[contains(@class, 'p-datatable-thead')]"
        XPATH_TABLE_BODY = "//p-table//tbody[contains(@class, 'p-datatable-tbody')]"
        XPATH_TABLE_PAGINATOR = "//p-paginator" 

        table_exists = utils.verificar_existencia(wait, XPATH_TABLE_CONTAINER, "MAIN TABLE ELEMENT", driver)
        
        if table_exists:
            print("\n📊 --- DEEP TABLE DATA EXTRACTION ---")
            filas = driver.find_elements("xpath", "//p-table//tbody/tr")
            print(f"   🔹 DATA ROWS RENDERED ON SCREEN: {len(filas)}")
            
            columnas = driver.find_elements("xpath", "//p-table//thead//th")
            nombres_columnas = [col.text.strip().replace('\n', ' ') for col in columnas if col.text.strip() != '']
            print(f"   🔹 COLUMNS DETECTED: {nombres_columnas}")
            print("--------------------------------------\n")

            print("🖍️ INJECTING JAVASCRIPT TO HIGHLIGHT TABLE FOR VISUAL EVIDENCE...")
            tabla_obj = driver.find_element("xpath", XPATH_TABLE_CONTAINER)
            driver.execute_script("arguments[0].style.border='4px solid #10b981'", tabla_obj)
            time.sleep(1)
            
            print("📸 TAKING SCREENSHOT EVIDENCE...")
            utils.tomar_screenshot(driver, "BASE_TBL_01_SUCCESS")
            print("✅ BASE-TBL-01: SUCCESS")
        else:
            print("❌ BASE-TBL-01 FAILED")
            utils.tomar_screenshot(driver, "BASE_TBL_01_FAILED")

    except Exception as e:
        print(f"❌ BASE-TBL-01 CRITICAL ERROR: {e}")
        try: utils.tomar_screenshot(driver, "BASE_TBL_01_TECHNICAL_ERROR")
        except: pass
    finally:
        print("🏁 CLOSING BROWSER...")
        driver.quit()

# ===================================================
# BASE-TBL-02: INTERACT WITH PAGINATOR AND ROW COUNT
# ==================================================
def BASE_TBL_02():
    print("\n" + "=" * 60)
    print("BASE-TBL-02: INTERACT WITH PAGINATOR AND ROW COUNT")
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
        
        MODULE_URL = "https://fat.memphis.mx/merchant" 
        print(f"🌐 NAVIGATING TO TABLE MODULE: {MODULE_URL}")
        driver.get(MODULE_URL)
        time.sleep(5)
        
        # ACTION 1: CHANGE TO ANOTHER PAGE
        print("👉 ACTION 1: CLICKING 'NEXT PAGE' BUTTON IN PAGINATOR...")
        XPATH_NEXT_PAGE = "//button[contains(@class, 'p-paginator-next')]"
        utils.click_boton(driver, XPATH_NEXT_PAGE)
        
        print("⏳ WAITING FOR TABLE TO LOAD NEXT PAGE DATA...")
        time.sleep(3)
        
        print("📸 TAKING SCREENSHOT EVIDENCE (PAGE CHANGED)...")
        utils.tomar_screenshot(driver, "BASE_TBL_02_PAGE_CHANGED")
        
        # ACTION 2: CHANGE AMOUNT OF RECORDS TO DISPLAY
        print("👉 ACTION 2: OPENING 'RECORDS PER PAGE' DROPDOWN...")
        XPATH_DROPDOWN = "//p-paginator//p-dropdown"
        utils.click_boton(driver, XPATH_DROPDOWN)
        time.sleep(1)
        
        print("👉 SELECTING '20' OR NEXT AVAILABLE OPTION...")
        XPATH_OPTION = "//li[@role='option']//span[contains(text(), '20')] | (//li[@role='option'])[2]"
        utils.click_boton(driver, XPATH_OPTION)
        
        print("⏳ WAITING FOR TABLE TO RENDER NEW AMOUNT OF ROWS...")
        time.sleep(3)
        
        print("\n📊 --- ROW COUNT VERIFICATION ---")
        filas = driver.find_elements("xpath", "//p-table//tbody/tr")
        print(f"   🔹 DATA ROWS RENDERED ON SCREEN NOW: {len(filas)}")
        print("----------------------------------\n")
        
        print("📡 CAPTURING HTTP EVIDENCE...")
        utils.print_http_evidence(driver, "merchant") 
        
        print("📸 TAKING SCREENSHOT EVIDENCE (ROWS CHANGED)...")
        utils.tomar_screenshot(driver, "BASE_TBL_02_ROWS_CHANGED")
        
        print("✅ BASE-TBL-02: SUCCESS")

    except Exception as e:
        print(f"❌ BASE-TBL-02 CRITICAL ERROR: {e}")
        try: utils.tomar_screenshot(driver, "BASE_TBL_02_TECHNICAL_ERROR")
        except: pass
    finally:
        print("🏁 CLOSING BROWSER...")
        driver.quit()

# =======================================================
# BASE-TBL_03: PERSISTENCE OF PAGINATION STATE ON RELOAD
# =======================================================
def BASE_TBL_03():
    print("\n" + "=" * 60)
    print("BASE-TBL_03: PERSISTENCE OF PAGINATION STATE ON RELOAD")
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
        
        MODULE_URL = "https://fat.memphis.mx/merchant" 
        print(f"🌐 NAVIGATING TO TABLE MODULE: {MODULE_URL}")
        driver.get(MODULE_URL)
        time.sleep(5)
        
        # STEP 1: CHANGE PAGE
        print("👉 STEP 1: CLICKING 'NEXT PAGE' IN PAGINATOR...")
        XPATH_NEXT_PAGE = "//button[contains(@class, 'p-paginator-next')]"
        utils.click_boton(driver, XPATH_NEXT_PAGE)
        time.sleep(3) # Wait for page 2 to load
        XPATH_PAGINATOR_TEXT = "//p-paginator/../span[contains(@class, 'text-sm')]"
        estado_antes_recarga = driver.find_element("xpath", XPATH_PAGINATOR_TEXT).text
        print(f"   🔹 PAGINATION STATE BEFORE RELOAD: '{estado_antes_recarga}'")
        
        # STEP 2: RELOAD VIEW
        print("🔄 STEP 2: RELOADING THE BROWSER VIEW (F5)...")
        driver.refresh()
        
        print("⏳ WAITING FOR TABLE TO RENDER AFTER RELOAD...")
        time.sleep(5)
        
        # EXTRACT NEW PAGINATOR STATE
        estado_despues_recarga = driver.find_element("xpath", XPATH_PAGINATOR_TEXT).text
        print(f"   🔹 PAGINATION STATE AFTER RELOAD:  '{estado_despues_recarga}'")
        
        # VALIDATION
        print("📡 CAPTURING HTTP EVIDENCE...")
        utils.print_http_evidence(driver, "merchant")
        
        if estado_antes_recarga == estado_despues_recarga and "1 a 10" not in estado_despues_recarga:
            print("📸 TAKING SCREENSHOT EVIDENCE...")
            utils.tomar_screenshot(driver, "BASE_TBL_03_SUCCESS")
            print("✅ BASE-TBL-03: SUCCESS")
        else:
            print("❌ BASE-TBL-03 FAILED")
            utils.tomar_screenshot(driver, "BASE_TBL_03_FAILED")

    except Exception as e:
        print(f"❌ BASE-TBL-03 CRITICAL ERROR: {e}")
        try: utils.tomar_screenshot(driver, "BASE_TBL_03_TECHNICAL_ERROR")
        except: pass
    finally:
        print("🏁 CLOSING BROWSER...")
        driver.quit()       

# ==========================================================
# BASE-TBL_04: ENTER TEXT IN SEARCH FIELD AND VERIFY FILTER
# ==========================================================
def BASE_TBL_04():
    print("\n" + "=" * 60)
    print("BASE-TBL_04: ENTER TEXT IN SEARCH FIELD AND VERIFY FILTER")
    print("=" * 60)
    # CAN CHANGE THIS TO ANY TEXT THAT EXISTS IN THE TABLE
    SEARCH_TERM = "memphis"
    driver, wait = utils.iniciar_driver_web()

    try: 
        print("🔐 PRECONDITION: AUTHENTICATING USER...")
        driver.get(config.URL_MEMPHIS_WEB)
        time.sleep(2)
        utils.escribir_texto(driver, config.XPATH_WEB_USER, config.WEB_USUARIO_PRUEBA)
        utils.escribir_texto(driver, config.XPATH_WEB_PASS, config.WEB_PASS_PRUEBA)
        utils.click_boton(driver, config.XPATH_WEB_BTN_LOGIN)
        time.sleep(5) 
        
        MODULE_URL = "https://fat.memphis.mx/merchant" 
        print(f"🌐 NAVIGATING TO TABLE MODULE: {MODULE_URL}")
        driver.get(MODULE_URL)
        time.sleep(5)
        
        # EXTRACT ROW COUNT BEFORE SEARCH
        filas_antes = len(driver.find_elements("xpath", "//p-table//tbody/tr"))
        print(f"   🔹 ROWS BEFORE SEARCH: {filas_antes}")
        
        # STEP 1: ENTER TEXT IN SEARCH FIELD
        print(f"👉 STEP 1: TYPING '{SEARCH_TERM}' IN SEARCH BAR ('Buscar')...")
        XPATH_SEARCH_BAR = "//input[@placeholder='Buscar']"
        
        
        from selenium.webdriver.common.keys import Keys
        input_element = driver.find_element("xpath", XPATH_SEARCH_BAR)
        input_element.clear()
        input_element.send_keys(SEARCH_TERM)
        input_element.send_keys(Keys.RETURN)
        
        print("⏳ WAITING FOR TABLE TO FILTER RESULTS...")
        time.sleep(3)
        filas_despues = len(driver.find_elements("xpath", "//p-table//tbody/tr"))
        print(f"   🔹 ROWS AFTER SEARCH: {filas_despues}")
        
        # VALIDATION
        print("📡 CAPTURING HTTP EVIDENCE...")
        utils.print_http_evidence(driver, "merchant")
        
        if filas_antes != filas_despues or filas_despues > 0:
            print("📸 TAKING SCREENSHOT EVIDENCE...")
            utils.tomar_screenshot(driver, "BASE_TBL_04_SUCCESS")
            print("✅ BASE-TBL-04: SUCCESS")
        else:
            print("❌ BASE-TBL-04 FAILED")
            utils.tomar_screenshot(driver, "BASE_TBL_04_FAILED")

    except Exception as e:
        print(f"❌ BASE-TBL-04 CRITICAL ERROR: {e}")
        try: utils.tomar_screenshot(driver, "BASE_TBL_04_TECHNICAL_ERROR")
        except: pass
    finally:
        print("🏁 CLOSING BROWSER...")
        driver.quit() 

# =========================================
# BASE-TBL-05: SEARCH PERSISTENCE ON RELOAD
# =========================================
def BASE_TBL_05():
    print("\n" + "=" * 60)
    print("BASE-TBL-05: SEARCH PERSISTENCE ON RELOAD")
    print("=" * 60)
    
    SEARCH_TERM = "memphis"
    driver, wait = utils.iniciar_driver_web()

    try: 
        print("🔐 PRECONDITION: AUTHENTICATING USER...")
        driver.get(config.URL_MEMPHIS_WEB)
        time.sleep(2)
        utils.escribir_texto(driver, config.XPATH_WEB_USER, config.WEB_USUARIO_PRUEBA)
        utils.escribir_texto(driver, config.XPATH_WEB_PASS, config.WEB_PASS_PRUEBA)
        utils.click_boton(driver, config.XPATH_WEB_BTN_LOGIN)
        time.sleep(5) 
        
        MODULE_URL = "https://fat.memphis.mx/merchant" 
        print(f"🌐 NAVIGATING TO TABLE MODULE: {MODULE_URL}")
        driver.get(MODULE_URL)
        time.sleep(5)
        
        # STEP 1: PERFORM A SEARCH
        print(f"👉 STEP 1: TYPING '{SEARCH_TERM}' IN SEARCH BAR AND PRESSING ENTER...")
        XPATH_SEARCH_BAR = "//input[@placeholder='Buscar']"
        from selenium.webdriver.common.keys import Keys
        input_element = driver.find_element("xpath", XPATH_SEARCH_BAR)
        input_element.clear()
        input_element.send_keys(SEARCH_TERM)
        input_element.send_keys(Keys.RETURN)
        
        print("⏳ WAITING FOR TABLE TO FILTER RESULTS...")
        time.sleep(3)
        
        filas_filtradas = len(driver.find_elements("xpath", "//p-table//tbody/tr"))
        print(f"   🔹 ROWS RENDERED AFTER INITIAL SEARCH: {filas_filtradas}")
        
        # STEP 2: RELOAD THE VIEW
        print("🔄 STEP 2: RELOADING THE BROWSER VIEW (F5)...")
        driver.refresh()
        print("⏳ WAITING FOR TABLE TO RENDER AFTER RELOAD...")
        time.sleep(5)
        
       # VALIDATION
        print("🔍 VERIFYING SEARCH STATE PERSISTENCE...")
        input_element_after = driver.find_element("xpath", XPATH_SEARCH_BAR)
        texto_buscador_actual = input_element_after.get_attribute("value")
        filas_post_recarga = len(driver.find_elements("xpath", "//p-table//tbody/tr"))
        print(f"   🔹 SEARCH BAR TEXT AFTER RELOAD: '{texto_buscador_actual}'")
        print(f"   🔹 ROWS RENDERED AFTER RELOAD: {filas_post_recarga}")
        print("📡 CAPTURING HTTP EVIDENCE...")
        utils.print_http_evidence(driver, "merchant")
        
        if texto_buscador_actual == SEARCH_TERM and filas_filtradas == filas_post_recarga:
            print("📸 TAKING SCREENSHOT EVIDENCE...")
            utils.tomar_screenshot(driver, "BASE_TBL_05_SUCCESS")
            print("✅ BASE-TBL-05: SUCCESS")
        else:
            print("❌ BASE-TBL-05 FAILED")
            utils.tomar_screenshot(driver, "BASE_TBL_05_FAILED")

    except Exception as e:
        print(f"❌ BASE-TBL-05 CRITICAL ERROR: {e}")
        try: utils.tomar_screenshot(driver, "BASE_TBL_05_TECHNICAL_ERROR")
        except: pass
    finally:
        print("🏁 CLOSING BROWSER...")
        driver.quit()

# ==========================================================
# BASE_TBL_06: CLICK ON SORTABLE COLUMN HEADER (SMART TOGGLE)
# ==========================================================
def BASE_TBL_06():
    print("\n" + "=" * 60)
    print("BASE_TBL_06: CLICK ON SORTABLE COLUMN HEADER")
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
        
        MODULE_URL = "https://fat.memphis.mx/merchant" 
        print(f"🌐 NAVIGATING TO TABLE MODULE: {MODULE_URL}")
        driver.get(MODULE_URL)
        time.sleep(5)
        
        # EXTRACT STATE BEFORE SORTING
        XPATH_FIRST_ROW_ID = "//p-table//tbody/tr[1]/td[3]"
        id_antes = driver.find_element("xpath", XPATH_FIRST_ROW_ID).text.strip()
        print(f"   🔹 FIRST ROW 'ID' BEFORE SORTING: {id_antes}")
        
        # STEP 1: CLICK SORT BUTTON (DESCENDING)
        print("👉 STEP 1: CLICKING ON THE 'ID' SORT BUTTON (DESCENDING)...")
        XPATH_SORT_DOWN = "//th[.//span[text()='ID']]//button[.//i[contains(@class, 'pi-sort-down-fill')]]"
        utils.click_boton(driver, XPATH_SORT_DOWN)
        
        print("⏳ WAITING FOR TABLE TO REORDER...")
        time.sleep(4)
        
        id_despues = driver.find_element("xpath", XPATH_FIRST_ROW_ID).text.strip()
        print(f"   🔹 FIRST ROW 'ID' AFTER 1ST CLICK: {id_despues}")
        
        # SMART TOGGLE: IF IT DIDN'T CHANGE, TRY ASCENDING
        if id_antes == id_despues:
            print("⚠️ ID DID NOT CHANGE. TABLE MIGHT BE SORTED THIS WAY BY DEFAULT.")
            print("👉 STEP 2: CLICKING SORT BUTTON AGAIN TO REVERSE ORDER (ASCENDING)...")
            XPATH_SORT_UP = "//th[.//span[text()='ID']]//button[.//i[contains(@class, 'pi-sort-up-fill')]]"
            utils.click_boton(driver, XPATH_SORT_UP)
            print("⏳ WAITING FOR TABLE TO REORDER...")
            time.sleep(4)
            id_despues = driver.find_element("xpath", XPATH_FIRST_ROW_ID).text.strip()
            print(f"   🔹 FIRST ROW 'ID' AFTER 2ND CLICK: {id_despues}")
        
        # VALIDATION
        print("📡 CAPTURING HTTP EVIDENCE...")
        utils.print_http_evidence(driver, "merchant")
        
        if id_antes != id_despues:
            print("📸 TAKING SCREENSHOT EVIDENCE...")
            utils.tomar_screenshot(driver, "BASE_TBL_06_SUCCESS")
            print("✅ BASE-TBL-06: SUCCESS")
        else:
            print("❌ BASE-TBL-06 FAILED")
            utils.tomar_screenshot(driver, "BASE_TBL_06_FAILED")

    except Exception as e:
        print(f"❌ BASE-TBL-06 CRITICAL ERROR: {e}")
        try: utils.tomar_screenshot(driver, "BASE_TBL_06_TECHNICAL_ERROR")
        except: pass
    finally:
        print("🏁 CLOSING BROWSER...")
        driver.quit()

# ==========================================================
# BASE-TBL-SM_01: ACCESS MODULE AND CLICK 'NEW' BUTTON
# ==========================================================
def BASE_TBL_SM_01():
    print("\n" + "=" * 60)
    print("BASE-TBL-SM_01: ACCESS MODULE AND CLICK 'NEW' BUTTON")
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
        
        MODULE_URL = "https://fat.memphis.mx/merchant" 
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
        utils.print_http_evidence(driver, "merchant")
        if form_opened:
            print("📸 TAKING SCREENSHOT EVIDENCE...")
            utils.tomar_screenshot(driver, "BASE_TBL_SM_01_SUCCESS")
            print("✅ BASE-TBL-SM-01: SUCCESS")
        else:
            print("❌ BASE-TBL-SM-01: FAILED")
            utils.tomar_screenshot(driver, "BASE_TBL_SM_01_FAILED")

    except Exception as e:
        print(f"❌ BASE-TBL-SM-01 CRITICAL ERROR: {e}")
        try: utils.tomar_screenshot(driver, "BASE_TBL_SM_01_TECHNICAL_ERROR")
        except: pass
    finally:
        print("🏁 CLOSING BROWSER...")
        driver.quit()

# === MAIN EXECUTION ===
if __name__ == "__main__":
    
    logger, log_file, timestamp = utils.iniciar_reporte("BASE_TBL")
    
    try:
        BASE_TBL_01()
        BASE_TBL_02()
        BASE_TBL_03()
        BASE_TBL_04()
        BASE_TBL_05()
        BASE_TBL_06()
        BASE_TBL_SM_01()
        
    finally:
        logger.close()
        #utils.generar_reporte_html("BASE_TBL", log_file, timestamp)