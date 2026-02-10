"""
FILENAME: AUTH.py
DESCRIPTION: TESTING AUTHENTICATION ON WEB PLATFORM
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time 
import config 
import utils 

"""
AUTOMATION AUTH-001
· ENTER YOUR CORRECT USERNAME AND PASSWORD.
· CLICK ON THE "LOG IN" BUTTON. 
"""
def test_login1():
    print("\n" + "=" * 60)
    print("TESTING WEB LOGIN")
    print("=" * 60)
    
    driver, wait = utils.iniciar_driver_web()

    try: 
        print(f"NAVIGATE TO: {config.URL_MEMPHIS_WEB}")
        driver.get(config.URL_MEMPHIS_WEB)
        time.sleep(3)

        print("WRITING USERNAME...")
        utils.escribir_texto(driver, config.XPATH_WEB_USER, config.WEB_USUARIO_PRUEBA)
        print("WRITING PASSWORD...")
        utils.escribir_texto(driver, config.XPATH_WEB_PASS, config.WEB_PASS_PRUEBA)
        print("CLICKING LOGIN...")
        utils.click_boton(driver, config.XPATH_WEB_BTN_LOGIN)
        time.sleep(5)
        print(f"✅ LOGIN SUCCESSFUL")

    except Exception as e:
        print(f"❌ ERROR IN LOGIN: {e}")
    finally:
        print("CLOSING BROWSER...")
        driver.quit()

"""
AUTOMATION AUTH-002
· ENTER AN INCORRECT USERNAME AND PASSWORD.
· CLICK ON THE "LOG IN" BUTTON. 
""" 
def test_login2():
    print("\n" + "=" * 60)
    print("TESTING WRONG WEB LOGIN")
    print("=" * 60)
    driver, wait = utils.iniciar_driver_web()

    try: 
        print(f"NAVIGATE TO: {config.URL_MEMPHIS_WEB}")
        driver.get(config.URL_MEMPHIS_WEB)
        time.sleep(3)

        print("WRITING WRONG USERNAME...")
        utils.escribir_texto(driver, config.XPATH_WEB_WRONG_USER, config.WEB_WRONGUSER)
        print("WRITING WRONG PASSWORD...")
        utils.escribir_texto(driver, config.XPATH_WEB_WRONG_PASS, config.WEB_WRONGPASS)
        print("CLICKING LOGIN...")
        utils.click_boton(driver, config.XPATH_WEB_BTN_LOGIN)
        time.sleep(5)
        print("✅ WRONG LOGIN SUCCESSFUL")
    except Exception as e:
        print(f"❌ ERROR IN WRONG LOGIN: {e}")
    finally:
        print("CLOSING BROWSER...")
        driver.quit()

"""
AUTOMATION AUTH-003
· ENTER CORRECT USERNAME AND WRONG PASSWORD. 
· CLICK ON THE "LOG IN" BUTTON. 
"""
def test_login3():
    print("\n" + "=" * 60)
    print("TESTING GOOD USERNAME AND WRONG PASSWORD")
    print("=" * 60)
    driver, wait = utils.iniciar_driver_web()

    try:
        print(f"NAVIGATE TO: {config.URL_MEMPHIS_WEB}")
        driver.get(config.URL_MEMPHIS_WEB)
        time.sleep(3)

        print("WRITING GOOD USERNAME...")
        utils.escribir_texto(driver, config.XPATH_WEB_USER, config.WEB_USUARIO_PRUEBA)
        print("WRITING WRONG PASSWORD...")
        utils.escribir_texto(driver, config.XPATH_WEB_WRONG_PASS, config.WEB_WRONGPASS)
        print("CLICKING LOGIN...")
        utils.click_boton(driver, config.XPATH_WEB_BTN_LOGIN)
        time.sleep(5)
        print("✅ GOOD USERNAME AND WRONG PASSWORD SUCCESSFUL")
    except Exception as e:
        print(f"❌ ERROR IN GOOD USERNAME AND WRONG PASSWORD: {e}")
    finally:
        print("CLOSING BROWSER...")
        driver.quit()

"""
AUTOMATION AUTH-004
· ENTER ONLY USERNAME AND PASSWORD FIELD EMPTY. 
· CLICK ON THE "LOG IN" BUTTON. 
"""
def test_login4():
    print("\n" + "=" * 60)
    print("TESTING EMPTY USERNAME AND PASSWORD")
    print("=" * 60)
    driver, wait = utils.iniciar_driver_web()

    try: 
        print(f"NAVIGATE TO: {config.URL_MEMPHIS_WEB}")
        driver.get(config.URL_MEMPHIS_WEB)
        time.sleep(3)

        print("WRITING GOOD USERNAME...")
        utils.escribir_texto(driver, config.XPATH_WEB_USER, config.WEB_USUARIO_PRUEBA)
        print("CLICKING LOGIN...")
        utils.click_boton(driver, config.XPATH_WEB_BTN_LOGIN)
        time.sleep(5)
        print("✅ GOOD USERNAME AND PASSWORD FIELD EMPTY SUCCESSFUL")
    except Exception as e:
        print(f"❌ ERROR IN GOOD USERNAME AND PASSWORD FIELD EMPTY: {e}")
    finally:
        print("CLOSING BROWSER...")
        driver.quit()

"""
AUTOMATION AUTH-005
· ENTER ONLY PASSWORD AND USERNAME FIELD EMPTY. 
· CLICK ON THE "LOG IN" BUTTON. 
"""
def test_login5():
    print("\n" + "=" * 60)
    print("TESTING ONLY PASSWORD AND USERNAME FIELD EMPTY")
    print("=" * 60)
    driver, wait = utils.iniciar_driver_web()

    try: 
        print(f"NAVIGATE TO: {config.URL_MEMPHIS_WEB}")
        driver.get(config.URL_MEMPHIS_WEB)
        time.sleep(3)
        
        print("WRITING PASSWORD...")
        utils.escribir_texto(driver, config.XPATH_WEB_PASS, config.WEB_PASS_PRUEBA)
        print("CLICKING LOGIN...")
        utils.click_boton(driver, config.XPATH_WEB_BTN_LOGIN)
        time.sleep(5)
        print("✅ ONLY PASSWORD AND USERNAME FIELD EMPTY SUCCESSFUL")
    except Exception as e:
        print(f"❌ ERROR IN GOOD USERNAME AND PASSWORD FIELD EMPTY: {e}")
    finally:
        print("CLOSING BROWSER...")
        driver.quit()

if __name__ == "__main__":
    test_login1() 
    test_login2()
    test_login3()
    test_login4()
    test_login5()