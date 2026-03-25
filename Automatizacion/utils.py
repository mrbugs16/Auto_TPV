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

# === EMAIL & REGEX IMPORTS === #
import imaplib
import email
import re
import html
import urllib.parse
from email.header import decode_header

import sys
import zipfile
import shutil
from datetime import datetime

# SCREENSHOT FUNCTION FOR T6 TERMINAL AND WEB
def tomar_screenshot(driver, nombre, plataforma="auto"):
    if plataforma == "auto":
        try:
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

# === HTTP EVIDENCE FUNCTION FOR SELENIUM (CAPTURES NETWORK LOGS AND PRINTS REQUESTS TO SPECIFIC ENDPOINTS) === #
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

# === T6 HTTP EVIDENCE FUNCTION WITH APPIUM (FIXED) === #
def print_http_evidence_appium(driver, nombre_test):
    """
    CAPTURES APPIUM SERVER / LOGCAT LOGS AS EVIDENCE.
    Saves to evidencias_zip/{nombre_test}_APPIUM_EVIDENCE_{timestamp}.txt
    and prints a summary.
    """
    os.makedirs("evidencias_zip", exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    evidence_path = f"evidencias_zip/{nombre_test}_APPIUM_EVIDENCE_{ts}.txt"

    lines = []
    def add(msg=""): lines.append(msg); print(msg)

    add(f"\n{'='*60}")
    add(f"📡 HTTP EVIDENCE — {nombre_test} (APPIUM / SERVER LOGS)")
    add(f"{'='*60}")
    add(f"⏰ TIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    add(f"-" * 60)

    raw_logs = []
    source = None

    # ─────────────────────────────────────────────────────────
    # 1) INTENTAR server logs (requiere --allow-insecure o --relaxed-security)
    # ─────────────────────────────────────────────────────────
    try:
        server_logs = driver.get_log('server')
        if server_logs:
            source = "server"
            for entry in server_logs:
                raw_logs.append(entry.get('message', ''))
    except Exception as e:
        err_msg = str(e)[:200]
        add(f"   ⚠️ Server logs: {err_msg}")
        if 'insecure' in err_msg.lower() or 'not been enabled' in err_msg.lower():
            add(f"   💡 Inicia Appium con: appium --relaxed-security")
            add(f"   💡 O bien con:        appium --allow-insecure=get_server_logs")

    # ─────────────────────────────────────────────────────────
    # 2) FALLBACK: logcat (siempre disponible en Android)
    # ─────────────────────────────────────────────────────────
    if not raw_logs:
        try:
            logcat = driver.get_log('logcat')
            if logcat:
                source = "logcat"
                for entry in logcat:
                    raw_logs.append(entry.get('message', ''))
        except Exception as e:
            add(f"   ⚠️ Logcat fallback: {str(e)[:120]}")

    if raw_logs:
        status_count = {}
        total_http = 0
        http_lines = []

        # ═══════════════════════════════════════════════════════
        # PATRONES DE DETECCIÓN SEGÚN FUENTE
        # ═══════════════════════════════════════════════════════
        
        # Patrones para SERVER logs (formato Appium/OkHttp)
        SERVER_PATTERNS = ['<--', 'HTTP/', 'status:']
        
        # Patrones para LOGCAT (formato Android nativo)
        LOGCAT_HTTP_PATTERNS = [
            'http',           # URLs y referencias HTTP
            'HTTP/',          # HTTP/1.1, HTTP/2
            'status',         # status code references
            'response',       # response messages
            'okhttp',         # OkHttp client logs
            'retrofit',       # Retrofit logs
            'NetworkDispatcher',  # Volley logs
            'StatusCode',     # Generic status code
            'Content-Type',   # HTTP headers
            'Authorization',  # Auth headers
            '<--',            # OkHttp interceptor format
            '-->',            # OkHttp request format
        ]
        
        # Códigos HTTP a detectar (ampliado)
        HTTP_STATUS_CODES = {
            '200', '201', '202', '204',          # Success
            '301', '302', '304',                  # Redirects
            '400', '401', '403', '404', '405',    # Client errors
            '409', '422', '429',                  # Client errors
            '500', '501', '502', '503', '504'     # Server errors
        }

        for msg in raw_logs:
            msg_lower = msg.lower()
            is_http_log = False

            if source == "server":
                # Para server logs, usar patrones originales
                is_http_log = any(p in msg for p in SERVER_PATTERNS)
            else:
                # Para logcat, usar patrones más amplios
                is_http_log = any(p in msg_lower for p in LOGCAT_HTTP_PATTERNS)

            if is_http_log:
                total_http += 1
                http_lines.append(msg)
                
                # Extraer código de status
                parts = msg.split()
                for part in parts:
                    # Limpiar el part de caracteres extra
                    clean_part = ''.join(c for c in part if c.isdigit())
                    if clean_part in HTTP_STATUS_CODES:
                        status_count[clean_part] = status_count.get(clean_part, 0) + 1
                        break

        add(f"📋 Source: {source} | Total logs: {len(raw_logs)} | HTTP-related: {total_http}")
        add(f"-" * 60)

        if status_count:
            add(f"   📊 STATUS CODES DETECTED:")
            for code, count in sorted(status_count.items()):
                if code.startswith('2'):
                    emoji = "✅"
                elif code.startswith('3'):
                    emoji = "🔄"
                elif code.startswith('4'):
                    emoji = "⚠️"
                else:
                    emoji = "❌"
                add(f"      {emoji} HTTP {code}: {count} responses")
        else:
            add(f"   ℹ️ No HTTP status codes detected in {source} logs")
            add(f"   📝 Showing last 10 log entries for debugging:")
            for i, log_entry in enumerate(raw_logs[-10:]):
                add(f"      [{i+1}] {log_entry[:150]}")
        add("")

        # ─── Guardar evidencia completa ───
        with open(evidence_path, 'w', encoding='utf-8') as f:
            f.write(f"EVIDENCE: {nombre_test} | Source: {source}\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write(f"Total logs: {len(raw_logs)} | HTTP-related: {total_http}\n")
            f.write("=" * 60 + "\n\n")

            if http_lines:
                f.write("--- HTTP-RELATED LOGS ---\n")
                for ln in http_lines[-200:]:
                    f.write(ln + "\n" if not ln.endswith("\n") else ln)
                f.write("\n\n")

            f.write("--- ALL RAW LOGS (last 500) ---\n")
            for ln in raw_logs[-500:]:
                f.write(ln + "\n" if not ln.endswith("\n") else ln)

        add(f"✔ EVIDENCE SAVED: {evidence_path}")
    else:
        add("   ❌ No logs available from any source (server or logcat)")
        add(f"   💡 Option 1: appium --relaxed-security")
        add(f"   💡 Option 2: appium --allow-insecure=get_server_logs")

    add(f"{'='*60}\n")

# =================================================================================
# FUNCTION: CLICK EYE BUTTON (WITH MULTIPLE FALLBACKS FOR ANGULAR/PRIMENG)
# =================================================================================
def click_eye_button(driver, xpath, descripcion="EYE BUTTON"):
    """
    CLICKS THE EYE BUTTON USING SELENIUM OR JAVASCRIPT AS A FALLBACK.
    USEFUL FOR ICONS LIKE <i class="pi-eye"> THAT OVERLAP WITH INPUT FIELDS.
    """
    print(f"👁️ ATTEMPTING TO CLICK: {descripcion}")
    try:
        # ATTEMPT 1: NORMAL CLICK WITH WEBDRIVERWAIT
        wait = WebDriverWait(driver, 5)
        elemento = wait.until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        elemento.click()
        print(f"✔ CLICKED (NORMAL SELENIUM METHOD): {descripcion}")
        return True

    except Exception as e1:
        print(f"⚠ NORMAL CLICK FAILED — TRYING JAVASCRIPT...")
        try:
            # ATTEMPT 2: JAVASCRIPT CLICK (BYPASSES UI OVERLAPS)
            elemento = driver.find_element(By.XPATH, xpath)
            driver.execute_script("arguments[0].click();", elemento)
            print(f"✔ CLICKED (JAVASCRIPT METHOD): {descripcion}")
            return True

        except Exception as e2:
            print(f"⚠ JAVASCRIPT CLICK FAILED — TRYING PARENT SPAN...")
            try:
                # ATTEMPT 3: CLICK THE PARENT ELEMENT (DYNAMICALLY)
                # INSTEAD OF HARDCODING [1], WE FIND THE PARENT OF THE EXACT XPATH WE PASSED
                parent_xpath = xpath + "/.."
                parent_element = driver.find_element(By.XPATH, parent_xpath)
                driver.execute_script("arguments[0].click();", parent_element)
                print(f"✔ CLICKED (PARENT ELEMENT + JS): {descripcion}")
                return True

            except Exception as e3:
                print(f"❌ ALL CLICK METHODS FAILED FOR {descripcion}")
                return False


# =================================================================================
# FUNCTION: EXTRACT RECOVERY LINK FROM EMAIL VIA IMAP
# =================================================================================
def obtener_link_recuperacion_imap(usuario_email, password_app):
    print(f"\n📧 CONNECTING TO IMAP SERVER FOR: {usuario_email}...")
    
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(usuario_email, password_app)
        
        # 1. DEFINE SEARCH FOLDERS (INBOX AND ALL MAIL AS BACKUP)
        carpetas = ["INBOX", "[Gmail]/All Mail", "[Gmail]/Spam"]
        email_ids = []
        remitente_buscado = 'no-reply@memphis.mx'
        
        # 2. SEARCH BY SENDER
        for carpeta in carpetas:
            try:
                print(f"📂 SCANNING FOLDER: {carpeta}...")
                mail.select(carpeta)
                typ, data = mail.search(None, f'(FROM "{remitente_buscado}")')
                
                if data[0]:
                    ids_encontrados = data[0].split()
                    if ids_encontrados:
                        email_ids = ids_encontrados[-3:] # GET LAST 3 EMAILS
                        break 
            except Exception:
                continue
        
        if not email_ids:
            print("❌ FAILED: NO EMAILS FOUND FROM 'no-reply@memphis.mx'.")
            return None

        # 3. ANALYZE THE LATEST EMAIL
        email_ids.reverse() # NEWEST FIRST
        ultimo_id = email_ids[0] 
        
        print(f"🔎 ANALYZING EMAIL ID: {ultimo_id.decode()}...")
        status, msg_data = mail.fetch(ultimo_id, "(RFC822)")
        
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        
        # EXTRACT BODY
        cuerpo = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    try: cuerpo += part.get_payload(decode=True).decode(errors="ignore")
                    except: pass
        else:
            try: cuerpo = msg.get_payload(decode=True).decode(errors="ignore")
            except: pass

        # 4. SEARCH AND CLEAN THE LINK (REGEX FOR 'FAT' OR 'API')
        patron = r'https?://(?:fat|api)\.memphis\.mx/resetPwd[^\s"\'<>]+'
        urls = re.findall(patron, cuerpo)
        
        if urls:
            link_sucio = urls[0]
            print(f"⚠️ RAW LINK DETECTED: {link_sucio[:60]}...")

            # --- DEEP CLEAN ---
            link_limpio = html.unescape(link_sucio)
            link_limpio = urllib.parse.unquote(link_limpio)
            link_limpio = link_limpio.replace("&amp;", "&").replace("&%23x3D;", "=")
            
            print(f"✅ CLEAN LINK EXTRACTED SUCCESSFULLY: {link_limpio}")
            
            mail.close()
            mail.logout()
            return link_limpio
        else:
            print("❌ EMAIL DOES NOT CONTAIN THE EXPECTED RESET PASSWORD LINK.")
            mail.close()
            mail.logout()
            return None

    except Exception as e:
        print(f"❌ CRITICAL IMAP ERROR: {e}")
        return None
    
# =================================================================================
# REPORTING ENGINE: DUAL LOGGER AND ZIP CREATOR
# =================================================================================
class DualLogger:
    """
    INTERCEPTS TERMINAL OUTPUT TO WRITE TO BOTH THE CONSOLE AND A TEXT FILE SIMULTANEOUSLY.
    """
    def __init__(self, filepath):
        self.terminal = sys.stdout
        self.log_file = open(filepath, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log_file.write(message)
        # 🛑 EL TRUCO DEL ARQUITECTO: Obligamos a Windows a guardar en el disco duro al instante
        self.log_file.flush() 

    def flush(self):
        self.terminal.flush()
        self.log_file.flush()
        
    def close(self):
        if not self.log_file.closed:
            self.log_file.close()
        sys.stdout = self.terminal # RESTORE NORMAL PRINTING

def iniciar_reporte(nombre_modulo):
    """
    STARTS THE RECORDING OF TERMINAL OUTPUT INTO A TEXT FILE.
    """
    os.makedirs("evidencias_zip", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"evidencias_zip/{nombre_modulo}_LOG_{timestamp}.txt"
    
    print(f"\n⏺️ STARTING RECORDING FOR MODULE: {nombre_modulo}...")
    logger = DualLogger(log_filename)
    sys.stdout = logger # REDIRECT ALL PRINTS TO OUR LOGGER
    
    return logger, log_filename, timestamp

def generar_zip_evidencias(nombre_modulo, logger, log_filename, timestamp):
    """
    STOPS RECORDING AND ZIPS THE TEXT LOG ALONG WITH ALL MATCHING SCREENSHOTS.
    """
    # 1. STOP RECORDING AND SAVE THE TEXT FILE
    logger.close()
    
    print("\n📦 PACKAGING EVIDENCE INTO A ZIP FILE...")
    zip_filename = f"evidencias_zip/{nombre_modulo}_FULL_REPORT_{timestamp}.zip"
    
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 2. ADD THE TERMINAL LOG TEXT FILE
            if os.path.exists(log_filename):
                zipf.write(log_filename, os.path.basename(log_filename))
            
            # 3. ADD ALL SCREENSHOTS (WEB AND T6)
            for carpeta in ("evidencias/Web", "evidencias/T6"):
                if os.path.exists(carpeta):
                    for file in os.listdir(carpeta):
                        if file.endswith(".png"):
                            filepath = os.path.join(carpeta, file)
                            zipf.write(filepath, f"screenshots/{file}")

            # 4. ADD APPIUM HTTP EVIDENCE FILES
            if os.path.exists("evidencias_zip"):
                for file in os.listdir("evidencias_zip"):
                    if "APPIUM_EVIDENCE" in file and file.endswith(".txt"):
                        filepath = os.path.join("evidencias_zip", file)
                        zipf.write(filepath, f"appium_evidence/{file}")

        print(f"✅ SUCCESS: ZIP REPORT GENERATED AT -> {zip_filename}")
        print("=" * 70 + "\n")
        return zip_filename
        
    except Exception as e:
        print(f"❌ ERROR GENERATING ZIP: {e}")
        return None
    
import base64
from datetime import datetime

# =================================================================================
# REPORTING ENGINE: PROFESSIONAL HTML DASHBOARD GENERATOR
# =================================================================================
def generar_reporte_html(nombre_modulo, log_filename, timestamp):
    """
    LEE EL ARCHIVO TXT DE LOGS Y GENERA UN REPORTE HTML PROFESIONAL.
    INCLUYE MÉTRICAS AUTOMÁTICAS, ESTILOS MODERNOS Y EVIDENCIAS INCRUSTADAS EN BASE64.
    """
    html_filename = f"evidencias_zip/{nombre_modulo}_REPORT_{timestamp}.html"
    print(f"\n📄 GENERANDO REPORTE HTML PROFESIONAL...")
    
    try:
        with open(log_filename, 'r', encoding='utf-8') as f:
            lineas = f.readlines()

        # 🛑 FIX: Ahora busca que la línea tenga una palomita "✅" Y la palabra "SUCCESS" en cualquier lugar.
        total_pasadas = sum(1 for linea in lineas if "✅" in linea and "SUCCESS" in linea.upper())
        total_fallidas = sum(1 for linea in lineas if "❌" in linea and ("FAILED" in linea.upper() or "ERROR" in linea.upper()))
        
        fecha_formateada = datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")

        # 2. PLANTILLA HTML Y CSS CORPORATIVO
        html_content = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>QA Report | {nombre_modulo}</title>
            <style>
                :root {{
                    --bg-main: #f4f7f9;
                    --bg-card: #ffffff;
                    --primary: #1e293b;
                    --secondary: #64748b;
                    --success: #10b981;
                    --danger: #ef4444;
                    --log-bg: #0f172a;
                    --log-text: #e2e8f0;
                }}
                body {{ font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background-color: var(--bg-main); color: var(--primary); margin: 0; padding: 30px; line-height: 1.5; }}
                
                /* HEADER DASHBOARD */
                .header-dashboard {{ background-color: var(--bg-card); padding: 25px 30px; border-radius: 10px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; border-left: 6px solid var(--primary); }}
                .header-info h1 {{ margin: 0 0 5px 0; font-size: 24px; color: var(--primary); }}
                .header-info p {{ margin: 0; color: var(--secondary); font-size: 14px; font-weight: 500; }}
                
                /* METRICS BADGES */
                .metrics {{ display: flex; gap: 15px; }}
                .badge {{ padding: 12px 20px; border-radius: 8px; font-weight: 600; font-size: 15px; color: white; display: flex; flex-direction: column; align-items: center; min-width: 80px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .badge span {{ font-size: 24px; margin-top: 4px; }}
                .badge-pass {{ background-color: var(--success); }}
                .badge-fail {{ background-color: var(--danger); }}
                
                /* LOG CONSOLE */
                .main-container {{ background-color: var(--bg-card); padding: 25px; border-radius: 10px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }}
                .section-title {{ font-size: 18px; margin-top: 0; margin-bottom: 15px; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }}
                .terminal {{ background-color: var(--log-bg); color: var(--log-text); padding: 20px; border-radius: 8px; font-family: 'Consolas', 'Courier New', monospace; font-size: 13px; overflow-x: auto; }}
                
                /* LOG LINES FORMATTING */
                .log-line {{ margin: 3px 0; white-space: pre-wrap; word-wrap: break-word; }}
                .log-success {{ color: #34d399; font-weight: bold; }}
                .log-error {{ color: #f87171; font-weight: bold; }}
                .log-info {{ color: #38bdf8; }}
                .log-warning {{ color: #facc15; }}
                .log-header {{ color: #cbd5e1; font-weight: bold; padding-top: 15px; border-bottom: 1px dashed #334155; padding-bottom: 5px; margin-bottom: 5px; }}
                
                /* EVIDENCE CARDS */
                .evidence-card {{ background-color: #1e293b; margin: 20px 0; padding: 15px; border-left: 4px solid #38bdf8; border-radius: 6px; box-shadow: inset 0 2px 4px rgba(0,0,0,0.2); }}
                .evidence-title {{ color: #7dd3fc; font-size: 12px; font-weight: bold; margin-bottom: 10px; font-family: 'Segoe UI', sans-serif; letter-spacing: 0.5px; text-transform: uppercase; }}
                .evidence-img {{ max-width: 100%; height: auto; border-radius: 4px; display: block; }}
            </style>
        </head>
        <body>

        <div class="header-dashboard">
            <div class="header-info">
                <h1>📊 Automated Test Execution Report</h1>
                <p>Módulo: <strong>{nombre_modulo}</strong> | Entorno: QA | Ejecución: {fecha_formateada}</p>
            </div>
            <div class="metrics">
                <div class="badge badge-pass">PASSED <span>{total_pasadas}</span></div>
                <div class="badge badge-fail">FAILED <span>{total_fallidas}</span></div>
            </div>
        </div>

        <div class="main-container">
            <h2 class="section-title">Terminal Logs & Evidences</h2>
            <div class="terminal">
        """
        
        # 3. PROCESAR CADA LÍNEA DEL LOG Y APLICAR ESTILOS
        for linea in lineas:
            linea_limpia = linea.replace('<', '&lt;').replace('>', '&gt;').strip('\n')
            
            if not linea_limpia.strip():
                html_content += "<br>\n"
                continue
                
            clase = "log-line"
            if "✅" in linea_limpia or "SUCCESS" in linea_limpia: clase += " log-success"
            elif "❌" in linea_limpia or "ERROR" in linea_limpia or "FAILED" in linea_limpia: clase += " log-error"
            elif "📡" in linea_limpia or "🌐" in linea_limpia or "🚀" in linea_limpia or "👉" in linea_limpia or "✍️" in linea_limpia: clase += " log-info"
            elif "⚠️" in linea_limpia or "WARNING" in linea_limpia: clase += " log-warning"
            elif "===" in linea_limpia: clase += " log-header"

            html_content += f'<div class="{clase}">{linea_limpia}</div>\n'

            # 4. INCRUSTAR IMÁGENES DENTRO DE TARJETAS
            if "✔ SCREENSHOT TAKEN:" in linea_limpia:
                partes = linea_limpia.split("SCREENSHOT TAKEN:")
                if len(partes) > 1:
                    img_path = partes[1].strip()
                    if os.path.exists(img_path):
                        with open(img_path, "rb") as img_file:
                            b64_string = base64.b64encode(img_file.read()).decode()
                            img_name = os.path.basename(img_path)
                            html_content += f"""
                            <div class="evidence-card">
                                <div class="evidence-title">📸 EVIDENCIA VISUAL: {img_name}</div>
                                <img class="evidence-img" src="data:image/png;base64,{b64_string}" alt="QA Evidence">
                            </div>
                            """

        html_content += """
            </div>
        </div>
        </body>
        </html>
        """
        
        # GUARDAR EL ARCHIVO HTML
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"✅ SUCCESS: REPORTE HTML GENERADO EN -> {html_filename}")
        print("=" * 70 + "\n")
        return html_filename

    except Exception as e:
        print(f"❌ ERROR GENERANDO REPORTE HTML: {e}")
        return None