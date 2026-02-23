"""
FILENAME: AUTH.py
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
# AUTH_001: ENTER CORRECT USERNAME AND PASSWORD.
# ==============================================
def auth_001():
    print("\n" + "=" * 60)
    print("AUTH_001: ENTER YOUR CORRECT USERNAME AND PASSWORD.")
    print("=" * 60)
    driver, wait = utils.iniciar_driver_web()

    try: 
        print(f"NAVIGATE TO: {config.URL_MEMPHIS_WEB}")
        driver.get(config.URL_MEMPHIS_WEB)
        time.sleep(3)
        print("WRITING USERNAME & PASSWORD...")
        utils.escribir_texto(driver, config.XPATH_WEB_USER, config.WEB_USUARIO_PRUEBA)
        utils.escribir_texto(driver, config.XPATH_WEB_PASS, config.WEB_PASS_PRUEBA)
        print("CLICKING LOGIN...")
        utils.click_boton(driver, config.XPATH_WEB_BTN_LOGIN)
        time.sleep(5)
        utils.print_http_evidence(driver, "gateway/api/v2/auth")
        print("📸 SCREENSHOT EVIDENCE TAKEN...")
        utils.tomar_screenshot(driver, "AUTH_001_SUCCESS")
        print(f"✅ SUCCESS")

    except Exception as e:
        print(f"❌ FAILED: {e}")
        try: utils.tomar_screenshot(driver, "AUTH_001_FAILED")
        except: pass
    finally:
        print("CLOSING BROWSER...")
        driver.quit()

# ==================================================
# AUTH_002: ENTER AN INCORRECT USERNAME AND PASSWORD.
# ==================================================
def auth_002():
    print("\n" + "=" * 60)
    print("AUTH_002: ENTER AN INCORRECT USERNAME AND PASSWORD.")
    print("=" * 60)
    driver, wait = utils.iniciar_driver_web()

    try: 
        print(f"NAVIGATE TO: {config.URL_MEMPHIS_WEB}")
        driver.get(config.URL_MEMPHIS_WEB)
        time.sleep(3)
        print("WRITING WRONG USERNAME & PASSWORD...")
        utils.escribir_texto(driver, config.XPATH_WEB_WRONG_USER, config.WEB_WRONGUSER)
        utils.escribir_texto(driver, config.XPATH_WEB_WRONG_PASS, config.WEB_WRONGPASS)
        print("CLICKING LOGIN...")
        utils.click_boton(driver, config.XPATH_WEB_BTN_LOGIN)
        time.sleep(5)
        utils.print_http_evidence(driver, "gateway/api/v2/auth")
        print("📸 SCREENSHOT EVIDENCE TAKEN...")
        utils.tomar_screenshot(driver, "AUTH_002_SUCCESS")
        print("✅ SUCCESS")
        
    except Exception as e:
        print(f"❌ FAILED {e}")
        try: utils.tomar_screenshot(driver, "AUTH_002_FAILED")
        except: pass
    finally:
        print("CLOSING BROWSER...")
        driver.quit()

# ==============================================
# AUTH_003: CORRECT USERNAME AND WRONG PASSWORD
# ==============================================
def auth_003():
    print("\n" + "=" * 60)
    print("AUTH_003: CORRECT USERNAME AND WRONG PASSWORD")
    print("=" * 60)
    driver, wait = utils.iniciar_driver_web()

    try:
        print(f"NAVIGATE TO: {config.URL_MEMPHIS_WEB}")
        driver.get(config.URL_MEMPHIS_WEB)
        time.sleep(3)
        print("WRITING GOOD USERNAME & WRONG PASSWORD...")
        utils.escribir_texto(driver, config.XPATH_WEB_USER, config.WEB_USUARIO_PRUEBA)
        utils.escribir_texto(driver, config.XPATH_WEB_WRONG_PASS, config.WEB_WRONGPASS)
        utils.click_boton(driver, config.XPATH_WEB_BTN_LOGIN)
        time.sleep(4)
        utils.print_http_evidence(driver, "gateway/api/v2/auth")
        print("📸 SCREENSHOT EVIDENCE TAKEN...")
        utils.tomar_screenshot(driver, "AUTH_003_SUCCESS")
        print("✅ SUCCESS")
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        try: utils.tomar_screenshot(driver, "AUTH_003_FAILED")
        except: pass
    finally:
        print("CLOSING BROWSER...")
        driver.quit()


# ========================================================
# AUTH_003: ENTRER ONLY USERNAME AND PASSWORD FIELD EMPTY.
# ========================================================
def auth_004():
    print("\n" + "=" * 60)
    print("AUTH_004: ENTER ONLY USERNAME AND PASSWORD FIELD EMPTY")
    print("=" * 60)
    driver, wait = utils.iniciar_driver_web()

    try: 
        print(f"NAVIGATE TO: {config.URL_MEMPHIS_WEB}")
        driver.get(config.URL_MEMPHIS_WEB)
        time.sleep(3)
        print("WRITING GOOD USERNAME & CLICKING LOGIN...")
        utils.escribir_texto(driver, config.XPATH_WEB_USER, config.WEB_USUARIO_PRUEBA)
        utils.click_boton(driver, config.XPATH_WEB_BTN_LOGIN)
        time.sleep(3)
        utils.print_http_evidence(driver, "gateway/api/v2/auth")
        utils.verificar_validacion_frontend(driver)
        print("📸 SCREEENSHOT EVIDENCE TAKEN...")
        utils.tomar_screenshot(driver, "AUTH_004_SUCCESS")
        print("✅ SUCCESS")
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        try: utils.tomar_screenshot(driver, "AUTH_004_FAILED")
        except: pass
    finally:
        print("CLOSING BROWSER...")
        driver.quit()


# ======================================================
# AUTH_005: ENTER ONLY PASSWORD AND USERNAME FIELD EMPTY. 
# =======================================================
def auth_005():
    print("\n" + "=" * 60)
    print("AUTH_005: ENTER ONLY PASSWORD AND USERNAME FIELD EMPTY")
    print("=" * 60)
    driver, wait = utils.iniciar_driver_web()

    try: 
        print(f"NAVIGATE TO: {config.URL_MEMPHIS_WEB}")
        driver.get(config.URL_MEMPHIS_WEB)
        time.sleep(3)
        print("WRITING PASSWORD & CLICKING LOGIN...")
        utils.escribir_texto(driver, config.XPATH_WEB_PASS, config.WEB_PASS_PRUEBA)
        utils.click_boton(driver, config.XPATH_WEB_BTN_LOGIN)
        time.sleep(5)
        utils.print_http_evidence(driver, "gateway/api/v2/auth")
        utils.verificar_validacion_frontend(driver)
        print("📸 SCREEENSHOT EVIDENCE TAKEN...")
        utils.tomar_screenshot(driver, "AUTH_005_SUCCESS")
        print("✅ SUCCESS")
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        try: utils.tomar_screenshot(driver, "AUTH_005_FAILED")
        except: pass
    finally:
        print("CLOSING BROWSER...")
        driver.quit()

if __name__ == "__main__":
    auth_001() 
    auth_002()
    auth_003()
    auth_004()
    auth_005()