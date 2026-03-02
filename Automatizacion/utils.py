"""
FILENAME: utils.py
DESCRIPTION: UTILITY LIBRARY FOR APPIUM AND SELENIUM WEB INTERACTIONS. 
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.chrome.options import Options 
# === WEB IMPORTS === #
from selenium import webdriver as webdriver_selenium 
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import config
import time
import os 
import json
import requests
from datetime import datetime

def tomar_screenshot(driver, nombre, plataforma="auto"):
    """
    Guarda screenshot en la carpeta correspondiente.
    plataforma: "t6", "web", o "auto" (detecta automáticamente)
    """
    if plataforma == "auto":
        try:
            # Si tiene capability 'automationName' es móvil (T6)
            caps = driver.capabilities
            if 'automationName' in caps or 'deviceName' in caps or 'appium' in str(caps).lower():
                plataforma = "t6"
            else:
                plataforma = "web"
        except:
            plataforma = "web"
    
    if plataforma == "t6":
        carpeta = os.path.join("evidencias", "T6")
    else:
        carpeta = os.path.join("evidencias", "Web")
    
    os.makedirs(carpeta, exist_ok=True)
    path = os.path.join(carpeta, f"{nombre}.png")
    driver.save_screenshot(path)
    print(f"✔ SCREENSHOT TAKEN: {path}")

# === T6 DRIVER === #
def iniciar_driver():
    options = Options()
    print("🚀 STARTING MOBILE AUTOMATION...")
    options = UiAutomator2Options().load_capabilities(config.CAPABILITIES)
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    driver = webdriver.Remote(config.URL_APPIUM, options=options)
    wait = WebDriverWait(driver, 15)
    return driver, wait

# === UTILITY FUNCTIONS === #
def escribir_texto(driver, xpath, texto):
    try:
        el = driver.find_element(By.XPATH, xpath)
        el.click()
        el.send_keys(texto)
    except Exception as e:
        print(f"✘ ERROR WRITING TO {xpath}: {e}")

# === CLICK FUNCTION WITH ERROR HANDLING === #
def click_boton(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath).click()
    except Exception as e:
        print(f"✘ ERROR CLICKING {xpath}: {e}")

# === WAIT FOR ELEMENT FUNCTION === #
def verificar_existencia(wait, xpath, descripcion, driver_debug=None):
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        print(f"✔ POPUP / ELEMENT DETECTED : {descripcion}")
        return True
    except:
        print(f"⚠ ALERT : NOT FOUND '{descripcion}'")
        return False

# === CLOSE DRIVER # === #
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

# === FRONTEND VALIDATION CHECK === #
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

# === T6 HTTP EVIDENCE FUNCTION WITH APPPIUM === #
def print_http_evidence_appium(driver, nombre_test):
    print(f"\n{'='*60}")
    print(f"📡 HTTP EVIDENCE — {nombre_test} (APPIUM SERVER)")
    print(f"{'='*60}")
    print(f"⏰ TIMESTAMP : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"-" * 60)
    
    try:
        server_logs = driver.get_log('server')
        
        if server_logs:
            status_count = {}
            total_http = 0
            
            for entry in server_logs:
                msg = entry.get('message', '')
                
                if '<--' in msg:
                    total_http += 1
                    
                    parts = msg.split()
                    for part in parts:
                        if part in ['200', '201', '400', '401', '403', '404', '500']:
                            status_count[part] = status_count.get(part, 0) + 1
                            break
            
            print(f"📋 {total_http} HTTP responses captured")
            print(f"-" * 60)
            print(f"   📊 STATUS CODES:")
            for code, count in sorted(status_count.items()):
                emoji = "✅" if code in ['200', '201'] else "❌"
                print(f"      {emoji} HTTP {code}: {count} responses")
        else:
            print("   ⚠️ No server logs available")
            
    except Exception as e:
        err_msg = str(e)[:80]
        if 'insecure' in err_msg.lower():
            print(f"   ⚠️ Server logs disabled")
            print(f"   💡 Run: appium --allow-insecure=*:get_server_logs")
        else:
            print(f"   ⚠️ Server logs error: {err_msg}")

def print_test_results(nombre_test, resultados):
    print("\n" + "=" * 60)
    print(f"📊 {nombre_test} RESULTS:")
    print("=" * 60)
    for fase, status, descripcion in resultados:
        emoji = "✅" if status else "❌"
        print(f"   {fase} : {emoji} {descripcion}")
    print("=" * 60)

# utils.py

def click_eye_button(driver, xpath, descripcion="Eye Button"):
    """
    Hace click en el botón del ojo usando JavaScript como fallback.
    Necesario cuando el elemento es un <i> con ::before pseudo-element.
    """
    try:
        # Intento 1 — click normal con WebDriverWait
        wait = WebDriverWait(driver, 10)
        elemento = wait.until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        elemento.click()
        print(f"✔ CLICKED (normal): {descripcion}")
        return True

    except Exception as e1:
        print(f"⚠ Normal click failed: {e1.__class__.__name__} — trying JavaScript...")
        try:
            # Intento 2 — JavaScript click (bypasa pseudo-elementos)
            elemento = driver.find_element(By.XPATH, xpath)
            driver.execute_script("arguments[0].click();", elemento)
            print(f"✔ CLICKED (JavaScript): {descripcion}")
            return True

        except Exception as e2:
            print(f"⚠ JavaScript click failed: {e2.__class__.__name__} — trying parent span...")
            try:
                # Intento 3 — click en el <span> padre del <i>
                elemento = driver.find_element(
                    By.XPATH,
                    "(//span[.//i[contains(@class,'pi-eye')]])[1]"
                )
                driver.execute_script("arguments[0].click();", elemento)
                print(f"✔ CLICKED (parent span + JS): {descripcion}")
                return True

            except Exception as e3:
                print(f"❌ ALL CLICK METHODS FAILED: {e3}")
                return False