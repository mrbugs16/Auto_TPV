"""
FILENAME: utils.py
DESCRIPTION: Utility library for Appium and Selenium Web interactions.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.chrome.options import Options 

import config
import time
import os 
import json

# === WEB IMPORTS === #
from selenium import webdriver as webdriver_selenium 
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def tomar_screenshot(driver, nombre_archivo):
    carpeta = "evidencias"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    ruta = os.path.join(carpeta, f"{nombre_archivo}.png")
    driver.save_screenshot(ruta)
    print(f"✔ SCREENSHOT TAKEN: {ruta}")

def iniciar_driver():
    options = Options()
    print("🚀 STARTING MOBILE AUTOMATION...")
    options = UiAutomator2Options().load_capabilities(config.CAPABILITIES)
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
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
def iniciar_driver_web(): 
    print("🚀 STARTING WEB AUTOMATION...")
    options = webdriver_selenium.ChromeOptions()
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    options.add_argument("--start-maximized")
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver_selenium.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 15)
    return driver, wait


def print_http_evidence(driver, endpoint_clave):
    print(f"\n📡 SCANNING NETWORK TRAFFIC: '{endpoint_clave}'...")
    try:
        logs = driver.get_log('performance')
        requests_map = {}
        responses = []

        for entry in logs:
            log_json = json.loads(entry['message'])['message']
            method = log_json['method']
            params = log_json.get('params', {})

            if method == 'Network.requestWillBeSent':
                req = params.get('request', {})
                url = req.get('url', '')
                if endpoint_clave in url:
                    request_id = params.get('requestId', '')
                    requests_map[request_id] = {
                        'url': url,
                        'method': req.get('method', 'UNKNOWN'),
                        'postData': req.get('postData', None)
                    }

            if method == 'Network.responseReceived':
                resp = params.get('response', {})
                url = resp.get('url', '')
                if endpoint_clave in url:
                    request_id = params.get('requestId', '')
                    responses.append({
                        'requestId': request_id,
                        'url': url,
                        'status': resp.get('status', 'N/A'),
                        'mimeType': resp.get('mimeType', 'N/A')
                    })

        if not responses:
            print(f"⚠️ NO HTTP TRAFFIC FOUND FOR: '{endpoint_clave}'")
            return

        for i, resp in enumerate(responses, 1):
            req_info = requests_map.get(resp['requestId'], {})
            http_method = req_info.get('method', 'UNKNOWN')
            post_data = req_info.get('postData', None)

            print("-" * 60)
            print(f"📋 MATCH #{i}")
            print(f"🔗 URL      : {resp['url']}")
            print(f"📨 METHOD   : {http_method}")
            print(f"📦 STATUS   : {resp['status']} (HTTP CODE)")
            print(f"📄 MIME TYPE: {resp['mimeType']}")

            
            if post_data:
                try:
                    safe_data = json.loads(post_data)
                    if 'password' in safe_data:
                        safe_data['password'] = '********'
                    print(f"📤 PAYLOAD  : {json.dumps(safe_data)}")
                except:
                    print(f"📤 PAYLOAD  : [RAW DATA PRESENT]")
            print("-" * 60)

            
            status = resp['status']
            if http_method == 'POST':
                if status == 200:
                    print("✅ SERVER: AUTHENTICATION SUCCESSFUL")
                elif status == 401:
                    print("🔒 SERVER: UNAUTHORIZED")
                elif status == 403:
                    print("🚫 SERVER: FORBIDDEN")
                elif status == 400:
                    print("⛔ SERVER: BAD REQUEST")
                else:
                    print(f"⚠️ SERVER: UNEXPECTED CODE {status}")

    except Exception as e:
        print(f"❌ ERROR READING HTTP LOGS: {e}")

def diagnosticar_trafico(driver):
    print("\n🔬 FULL NETWORK TRAFFIC DIAGNOSTIC")
    print("=" * 70)
    try:
        logs = driver.get_log('performance')
        requests_map = {}
        for entry in logs:
            log_json = json.loads(entry['message'])['message']
            method = log_json['method']
            params = log_json.get('params', {})

            # REQUEST CAPTURE
            if method == 'Network.requestWillBeSent':
                req = params.get('request', {})
                request_id = params.get('requestId', '')
                requests_map[request_id] = {
                    'method': req.get('method', ''),
                    'url': req.get('url', ''),
                    'postData': req.get('postData', None)
                }

            # RESPONSE CAPTURE
            if method == 'Network.responseReceived':
                resp = params.get('response', {})
                request_id = params.get('requestId', '')
                url = resp.get('url', '')
                status = resp.get('status', '')
                mime = resp.get('mimeType', '')
                req_info = requests_map.get(request_id, {})
                http_method = req_info.get('method', '?')
                post_data = req_info.get('postData', None)

                # FILTER OUT STATIC ASSETS
                skip = ['.css', '.js', '.png', '.jpg', '.svg', '.woff', 
                        '.ttf', 'favicon', 'fonts', 'google', 'analytics']
                if any(s in url.lower() for s in skip):
                    continue

                print(f"  {http_method:6} | {status} | {mime:30} | {url[:100]}")
                if post_data:
                    print(f"         📤 PAYLOAD: {post_data[:150]}")

        print("=" * 70)
    except Exception as e:
        print(f"❌ ERROR: {e}")


def verificar_validacion_frontend(driver):
    try:
        error_msgs = driver.find_elements(By.XPATH, 
            "//*[contains(@class, 'error') or contains(@class, 'alert') or contains(@class, 'warning')]")
        if error_msgs:
            for msg in error_msgs:
                if msg.text.strip():
                    print(f"🔸 FRONTEND VALIDATION: '{msg.text.strip()}'")
            return True
        else:
            print("🔸 FRONTEND VALIDATION: No POST sent (client-side validation blocked submission)")
            return False
    except Exception as e:
        print(f"⚠️ Could not read frontend validation: {e}")
        return False

