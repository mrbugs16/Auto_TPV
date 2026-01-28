"""
FILENAME: utils.py
DESCRIPTION:
    Utility library and wrapper functions for Appium/Selenium interactions.
    Handles repetitive UI logic, explicit waits, and error management.

KEY FUNCTIONS:
    - iniciar_driver(): Configures and initializes the Appium session.
    - verificar_existencia(): Validates visual elements with wait handling and logs.
    - escribir_texto() / click_boton(): Safe interactions wrapped in try/except blocks.
    - debug_screen(): Scans and prints visible elements (essential for debugging).

USAGE:
    import utils
    utils.click_boton(driver, xpath)
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
import config
import time


def iniciar_driver():
    print("🚀 STARTING AUTOMATION...")
    options = UiAutomator2Options().load_capabilities(config.CAPABILITIES)
    driver = webdriver.Remote(config.URL_APPIUM, options=options)
    wait = WebDriverWait(driver, 15)
    return driver, wait


def escribir_texto(driver, xpath, texto):
    try:
        el = driver.find_element(By.XPATH, xpath)
        el.click()
        el.send_keys(texto)
    except Exception as e:
        print(f"✘ ERROR WRITING TO {xpath}: {e}")


def click_boton(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath).click()
    except Exception as e:
        print(f"✘ ERROR CLICKING {xpath}: {e}")


def verificar_existencia(wait, xpath, descripcion, driver_debug=None):

    """
    CHECK IF AN ELEMENT EXISTS.
    IF IT FAILS AND YOU PASS THE DRIVER, PRINT TEXT AND CONTENT DESCRIPTION
    FOR DEBUGGING.
    """
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        print(f"✔ POPUP / ELEMENT DETECTED : {descripcion}")
        return True
    except:
        print(f"⚠ ALERT : NOT FOUND '{descripcion}'")


        if driver_debug:
            print("\n--- WHAT DOES APPIUM SEE ON THE SCREEN? (DEBUG) ---")
            elementos = driver_debug.find_elements(By.XPATH,
                                                   "//*[string-length(@text) > 0 or string-length(@content-desc) > 0]")
            if not elementos:
                print("   (NO ELEMENTS WITH LEGIBLE TEXT WERE DETECTED)")

            for e in elementos:
                try:
                    txt = e.get_attribute("text")
                    desc = e.get_attribute("content-desc")
                    res_id = e.get_attribute("resource-id")

                    info = []
                    if txt: info.append(f"Text: '{txt}'")
                    if desc: info.append(f"Desc: '{desc}'")
                    if res_id: info.append(f"ID: '{res_id}'")

                    if info:
                        print(f"   -> ELEMENT: {', '.join(info)}")
                except:
                    pass
            print("---------------------------------------------------\n")
        return False


def alternar_wifi(driver, estado=True):

    try:
        if estado:
            driver.execute_script('mobile: shell', {'command': 'svc wifi enable'})
        else:
            driver.execute_script('mobile: shell', {'command': 'svc wifi disable'})
        print(f"📶 WIFI CHANGE ATTEMPT TO: {estado}")
        time.sleep(2)
    except:
        print("⚠ AUTOMATIC WIFI SWITCHING NO SUPPORTED, MANUAL SWITCHING REQUIRED.")


def cerrar_driver(driver):
    print("🏁 CLOSING SESSION...")
    time.sleep(2)
    driver.quit()