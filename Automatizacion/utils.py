"""
FILENAME: utils.py
DESCRIPTION: Utility library for Appium and Selenium Web interactions.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
import config
import time

# === WEB IMPORTS === #
from selenium import webdriver as webdriver_selenium # Renombramos para no confundir con appium
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def iniciar_driver():
    print("🚀 STARTING MOBILE AUTOMATION...")
    options = UiAutomator2Options().load_capabilities(config.CAPABILITIES)
    driver = webdriver.Remote(config.URL_APPIUM, options=options)
    wait = WebDriverWait(driver, 15)
    return driver, wait


def escribir_texto(driver, xpath, texto):
    try:
        # Buscamos el elemento (funciona igual para Web y Mobile)
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
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        print(f"✔ POPUP / ELEMENT DETECTED : {descripcion}")
        return True
    except:
        print(f"⚠ ALERT : NOT FOUND '{descripcion}'")
        return False


def cerrar_driver(driver):
    print("🏁 CLOSING SESSION...")
    time.sleep(2)
    driver.quit()

# === WEB DRIVER === #
def iniciar_driver_web(): # Corregido: Usar ':' y no ';'
    print("🚀 STARTING WEB AUTOMATION...")
    # Esto descarga el driver automáticamente
    service = ChromeService(ChromeDriverManager().install())
    
    options = webdriver_selenium.ChromeOptions()
    options.add_argument("--start-maximized")
    
    driver = webdriver_selenium.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 15)
    
    return driver, wait