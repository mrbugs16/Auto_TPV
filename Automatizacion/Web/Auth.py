"""
FILENAME: AUTH.PY
DESCRIPTION: TESTING AUTHENTICATION ON WEB PLATFORM
CONTENTS: 
· AUTH-001: CORRECT USERNAME AND PASSWORD
· AUTH-002: WRONG USERNAME AND PASSWORD
· AUTH-003: CORRECT USERNAME AND WRONG PASSWORD
· AUTH-004: USERNAME ONLY, PASSWORD EMPTY
· AUTH-005: PASSWORD ONLY, USERNAME EMPTY
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time 
import config 
import utils 

# ==============================================
# AUTH-001: ENTER CORRECT USERNAME AND PASSWORD
# ==============================================
def AUTH_001():
    print("\n" + "=" * 60)
    print("AUTH_001: ENTER YOUR CORRECT USERNAME AND PASSWORD")
    print("=" * 60)
    driver, wait = utils.iniciar_driver_web()

    try: 
        print(f"🌐 NAVIGATING TO: {config.URL_MEMPHIS_WEB}")
        driver.get(config.URL_MEMPHIS_WEB)
        time.sleep(3)
        
        print("✍️ WRITING USERNAME & PASSWORD...")
        utils.escribir_texto(driver, config.XPATH_WEB_USER, config.WEB_USUARIO_PRUEBA)
        utils.escribir_texto(driver, config.XPATH_WEB_PASS, config.WEB_PASS_PRUEBA)
        
        print("👉 CLICKING LOGIN BUTTON...")
        utils.click_boton(driver, config.XPATH_WEB_BTN_LOGIN)
        time.sleep(5)
        
        print("📡 CAPTURING HTTP EVIDENCE...")
        utils.print_http_evidence(driver, "auth")
        
        print("📸 TAKING SCREENSHOT EVIDENCE...")
        utils.tomar_screenshot(driver, "AUTH_001_SUCCESS")
        
        print("✅ AUTH-001: SUCCESS")

    except Exception as e:
        print(f"❌ AUTH-001 FAILED: {e}")
        try: utils.tomar_screenshot(driver, "AUTH_001_FAILED")
        except: pass
    finally:
        print("🏁 CLOSING BROWSER...")
        driver.quit()

# ==================================================
# AUTH_002: ENTER AN INCORRECT USERNAME AND PASSWORD
# ==================================================
def AUTH_002():
    print("\n" + "=" * 60)
    print("AUTH-002: ENTER AN INCORRECT USERNAME AND PASSWORD")
    print("=" * 60)
    driver, wait = utils.iniciar_driver_web()

    try: 
        print(f"🌐 NAVIGATING TO: {config.URL_MEMPHIS_WEB}")
        driver.get(config.URL_MEMPHIS_WEB)
        time.sleep(3)
        
        print("✍️ WRITING WRONG USERNAME & WRONG PASSWORD...")
        utils.escribir_texto(driver, config.XPATH_WEB_WRONG_USER, config.WEB_WRONGUSER)
        utils.escribir_texto(driver, config.XPATH_WEB_WRONG_PASS, config.WEB_WRONGPASS)
        
        print("👉 CLICKING LOGIN BUTTON...")
        utils.click_boton(driver, config.XPATH_WEB_BTN_LOGIN)
        time.sleep(1.5)
        
        print("📡 CAPTURING HTTP EVIDENCE...")
        utils.print_http_evidence(driver, "auth")
        
        print("📸 TAKING SCREENSHOT EVIDENCE...")
        utils.tomar_screenshot(driver, "AUTH_002_SUCCESS")
        
        print("✅ AUTH-002: SUCCESS")
        
    except Exception as e:
        print(f"❌ AUTH-002 FAILED: {e}")
        try: utils.tomar_screenshot(driver, "AUTH_002_FAILED")
        except: pass
    finally:
        print("🏁 CLOSING BROWSER...")
        driver.quit()

# ==============================================
# AUTH_003: CORRECT USERNAME AND WRONG PASSWORD
# ==============================================
def AUTH_003():
    print("\n" + "=" * 60)
    print("AUTH-003: CORRECT USERNAME AND WRONG PASSWORD")
    print("=" * 60)
    driver, wait = utils.iniciar_driver_web()

    try:
        print(f"🌐 NAVIGATING TO: {config.URL_MEMPHIS_WEB}")
        driver.get(config.URL_MEMPHIS_WEB)
        time.sleep(3)
        
        print("✍️ WRITING GOOD USERNAME & WRONG PASSWORD...")
        utils.escribir_texto(driver, config.XPATH_WEB_USER, config.WEB_USUARIO_PRUEBA)
        utils.escribir_texto(driver, config.XPATH_WEB_WRONG_PASS, config.WEB_WRONGPASS)
        
        print("👉 CLICKING LOGIN BUTTON...")
        utils.click_boton(driver, config.XPATH_WEB_BTN_LOGIN)
        time.sleep(1.5)
        
        print("📡 CAPTURING HTTP EVIDENCE...")
        utils.print_http_evidence(driver, "auth")
        
        print("📸 TAKING SCREENSHOT EVIDENCE...")
        utils.tomar_screenshot(driver, "AUTH_003_SUCCESS")
        
        print("✅ AUTH-003: SUCCESS")
        
    except Exception as e:
        print(f"❌ AUTH-003 FAILED: {e}")
        try: utils.tomar_screenshot(driver, "AUTH_003_FAILED")
        except: pass
    finally:
        print("🏁 CLOSING BROWSER...")
        driver.quit()


# ========================================================
# AUTH-004: ENTER ONLY USERNAME AND PASSWORD FIELD EMPTY
# ========================================================
def AUTH_004():
    print("\n" + "=" * 60)
    print("AUTH-004: ENTER ONLY USERNAME AND PASSWORD FIELD EMPTY")
    print("=" * 60)
    driver, wait = utils.iniciar_driver_web()

    try: 
        print(f"🌐 NAVIGATING TO: {config.URL_MEMPHIS_WEB}")
        driver.get(config.URL_MEMPHIS_WEB)
        time.sleep(3)
        
        print("✍️ WRITING GOOD USERNAME & LEAVING PASSWORD EMPTY...")
        utils.escribir_texto(driver, config.XPATH_WEB_USER, config.WEB_USUARIO_PRUEBA)
        
        print("👉 CLICKING LOGIN BUTTON...")
        utils.click_boton(driver, config.XPATH_WEB_BTN_LOGIN)
        time.sleep(3)
        
        print("📡 CAPTURING HTTP EVIDENCE...")
        utils.print_http_evidence(driver, "auth")
        utils.verificar_validacion_frontend(driver)
        
        print("📸 TAKING SCREENSHOT EVIDENCE...")
        utils.tomar_screenshot(driver, "AUTH_004_SUCCESS")
        
        print("✅ AUTH-004: SUCCESS")
        
    except Exception as e:
        print(f"❌ AUTH-004 FAILED: {e}")
        try: utils.tomar_screenshot(driver, "AUTH_004_FAILED")
        except: pass
    finally:
        print("🏁 CLOSING BROWSER...")
        driver.quit()


# ======================================================
# AUTH_005: ENTER ONLY PASSWORD AND USERNAME FIELD EMPTY 
# =======================================================
def AUTH_005():
    print("\n" + "=" * 60)
    print("AUTH-005: ENTER ONLY PASSWORD AND USERNAME FIELD EMPTY")
    print("=" * 60)
    driver, wait = utils.iniciar_driver_web()

    try: 
        print(f"🌐 NAVIGATING TO: {config.URL_MEMPHIS_WEB}")
        driver.get(config.URL_MEMPHIS_WEB)
        time.sleep(3)
        
        print("✍️ WRITING PASSWORD & LEAVING USERNAME EMPTY...")
        utils.escribir_texto(driver, config.XPATH_WEB_PASS, config.WEB_PASS_PRUEBA)
        
        print("👉 CLICKING LOGIN BUTTON...")
        utils.click_boton(driver, config.XPATH_WEB_BTN_LOGIN)
        time.sleep(3)
        
        print("📡 CAPTURING HTTP EVIDENCE...")
        utils.print_http_evidence(driver, "auth")
        utils.verificar_validacion_frontend(driver)
        
        print("📸 TAKING SCREENSHOT EVIDENCE...")
        utils.tomar_screenshot(driver, "AUTH_005_SUCCESS")
        
        print("✅ AUTH-005: SUCCESS")
        
    except Exception as e:
        print(f"❌ AUTH-005 FAILED: {e}")
        try: utils.tomar_screenshot(driver, "AUTH_005_FAILED")
        except: pass
    finally:
        print("🏁 CLOSING BROWSER...")
        driver.quit()

# === MAIN EXECUTION ===
if __name__ == "__main__":
    
    # START LOG RECORDER
    logger, log_file, timestamp = utils.iniciar_reporte("AUTH")
    
    try:
        AUTH_001() 
        AUTH_002()
        AUTH_003()
        AUTH_004()
        AUTH_005()
        
    finally:
        # STOP RECORDER AND GENERATE HTML
        logger.close()
        utils.generar_reporte_html("AUTH", log_file, timestamp)
        #utils.generar_zip_evidencias("AUTH", logger, log_file, timestamp)
             
