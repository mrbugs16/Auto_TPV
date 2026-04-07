"""
# ==================================================================================
# FILENAME    : utils.py
# PROJECT     : MEMPHIS QA AUTOMATION FRAMEWORK
# DESCRIPTION : SHARED UTILITY LIBRARY — ABSTRACTION LAYER OVER APPIUM AND SELENIUM
#               INTERACTIONS. ALL TEST SCRIPTS IMPORT FROM HERE; NOTHING IS EVER
#               HARDCODED AT THE TEST LEVEL.
#
# STRUCTURE:
#   [1] IMPORTS
#   [2] COMMON UTILITIES   — screenshot, shared click/write helpers
#   [3] T6 MOBILE          — driver init, mobile interactions, Appium HTTP evidence
#   [4] WEB PLATFORM       — driver init, web interactions, network evidence, IMAP
#   [5] REPORTING ENGINE   — DualLogger, HTML report, ZIP packager
#
# CONVENTIONS:
#   - FUNCTIONS PREFIXED WITH _ ARE INTERNAL HELPERS (NOT CALLED FROM TEST FILES).
#   - ALL PRINT STATEMENTS USE EMOJIS CONSISTENT WITH THE REST OF THE FRAMEWORK.
#   - NO BARE except: CLAUSES — ALWAYS LOG THE ERROR MESSAGE.
# ==================================================================================
"""

# ==================================================================================
# [1] IMPORTS
# ==================================================================================

# --- STANDARD LIBRARY ---
import sys
import os
import re
import html
import json
import time
import base64
import zipfile
import shutil
import imaplib
import email
import urllib.parse
from datetime import datetime
from email.header import decode_header

# --- SELENIUM / APPIUM ---
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

# T6 — APPIUM CLIENT
from appium import webdriver as appium_webdriver
from appium.options.android import UiAutomator2Options

# WEB — SELENIUM CHROME
from selenium import webdriver as selenium_webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import config


# ==================================================================================
# [2] COMMON UTILITIES
# ==================================================================================

def tomar_screenshot(driver, nombre, plataforma="auto"):
    """
    SAVES A SCREENSHOT TO THE APPROPRIATE EVIDENCE SUBFOLDER.
    AUTO-DETECTS PLATFORM (T6 vs WEB) BASED ON DRIVER CAPABILITIES.
    OUTPUT PATHS:
        T6  → evidencias/T6/{nombre}.png
        WEB → evidencias/Web/{nombre}.png
    """
    if plataforma == "auto":
        try:
            caps = driver.capabilities
            if (
                "automationName" in caps or
                "deviceName" in caps or
                "appium" in str(caps).lower()
            ):
                plataforma = "t6"
            else:
                plataforma = "web"
        except:
            plataforma = "web"

    carpeta = os.path.join("evidencias", "T6" if plataforma == "t6" else "Web")
    os.makedirs(carpeta, exist_ok=True)
    path = os.path.join(carpeta, f"{nombre}.png")
    driver.save_screenshot(path)
    print(f"✔ SCREENSHOT TAKEN: {path}")


def click_boton(driver, xpath):
    """
    CLICKS AN ELEMENT LOCATED BY XPATH.
    PRINTS THE FULL ERROR MESSAGE IF THE ELEMENT IS NOT FOUND OR NOT CLICKABLE.
    WORKS FOR BOTH APPIUM (T6) AND SELENIUM (WEB) DRIVERS.
    """
    try:
        driver.find_element(By.XPATH, xpath).click()
    except Exception as e:
        print(f"✘ ERROR CLICKING {xpath}: {e}")


def escribir_texto(driver, xpath, texto):
    """
    LOCATES AN INPUT FIELD BY XPATH, CLICKS IT, AND TYPES THE GIVEN TEXT.
    WORKS FOR BOTH APPIUM (T6) AND SELENIUM (WEB) DRIVERS.
    """
    try:
        el = driver.find_element(By.XPATH, xpath)
        el.click()
        el.send_keys(texto)
    except Exception as e:
        print(f"✘ ERROR WRITING TO {xpath}: {e}")


def verificar_existencia(wait, xpath, descripcion, driver_debug=None):
    """
    WAITS UP TO THE DRIVER'S CONFIGURED TIMEOUT FOR AN ELEMENT TO APPEAR IN THE DOM.
    RETURNS True IF FOUND, False OTHERWISE.
    WORKS FOR BOTH APPIUM (T6) AND SELENIUM (WEB) DRIVERS.
    """
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        print(f"✔ POPUP / ELEMENT DETECTED: {descripcion}")
        return True
    except Exception:
        print(f"⚠ ALERT: NOT FOUND '{descripcion}'")
        return False


# ==================================================================================
# [3] T6 MOBILE — APPIUM DRIVER & INTERACTIONS
# ==================================================================================

def iniciar_driver():
    """
    STARTS AN APPIUM SESSION AGAINST THE T6 ANDROID DEVICE DEFINED IN config.py.
    ENABLES PERFORMANCE LOGGING (REQUIRED FOR print_http_evidence_appium).
    RETURNS (driver, wait) TUPLE.
    """
    print("🚀 STARTING T6 MOBILE AUTOMATION SESSION...")
    options = UiAutomator2Options().load_capabilities(config.CAPABILITIES)
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    driver = appium_webdriver.Remote(config.URL_APPIUM, options=options)
    wait   = WebDriverWait(driver, 15)
    print(f"   ✅ APPIUM SESSION STARTED — DEVICE: {config.CAPABILITIES.get('appium:deviceName', 'UNKNOWN')}")
    return driver, wait


def cerrar_driver(driver):
    """
    GRACEFULLY TERMINATES THE APPIUM SESSION.
    ALWAYS CALLED IN THE finally BLOCK OF EACH TEST FUNCTION.
    """
    print("🏁 CLOSING T6 SESSION...")
    time.sleep(2)
    driver.quit()


def print_http_evidence_appium(driver, nombre_test):
    """
    CAPTURES APPIUM SERVER LOGS OR ANDROID LOGCAT AS HTTP TRAFFIC EVIDENCE.
    SAVES A FULL TXT FILE TO evidencias_zip/ AND PRINTS A STATUS CODE SUMMARY.

    REQUIREMENTS:
        START APPIUM WITH ONE OF THESE FLAGS TO ENABLE SERVER LOGS:
            appium --relaxed-security
            appium --allow-insecure=get_server_logs
    """
    os.makedirs("evidencias_zip", exist_ok=True)
    ts            = datetime.now().strftime("%Y%m%d_%H%M%S")
    evidence_path = f"evidencias_zip/{nombre_test}_APPIUM_EVIDENCE_{ts}.txt"

    lines = []
    def add(msg=""):
        lines.append(msg)
        print(msg)

    add(f"\n{'=' * 60}")
    add(f"📡 HTTP EVIDENCE — {nombre_test} (APPIUM / SERVER LOGS)")
    add(f"{'=' * 60}")
    add(f"⏰ TIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    add("-" * 60)

    raw_logs = []
    source   = None

    # ── ATTEMPT 1: SERVER LOGS (REQUIRES --relaxed-security OR --allow-insecure) ──
    try:
        server_logs = driver.get_log("server")
        if server_logs:
            source = "server"
            for entry in server_logs:
                raw_logs.append(entry.get("message", ""))
    except Exception as e:
        err_msg = str(e)[:200]
        add(f"   ⚠️  SERVER LOGS UNAVAILABLE: {err_msg}")
        if "insecure" in err_msg.lower() or "not been enabled" in err_msg.lower():
            add("   💡 START APPIUM WITH: appium --relaxed-security")
            add("   💡 OR WITH:           appium --allow-insecure=get_server_logs")

    # ── ATTEMPT 2: LOGCAT FALLBACK (ALWAYS AVAILABLE ON ANDROID) ──────────────────
    if not raw_logs:
        try:
            logcat = driver.get_log("logcat")
            if logcat:
                source = "logcat"
                for entry in logcat:
                    raw_logs.append(entry.get("message", ""))
        except Exception as e:
            add(f"   ⚠️  LOGCAT FALLBACK FAILED: {str(e)[:120]}")

    HTTP_STATUS_CODES = {
        "200", "201", "202", "204",
        "301", "302", "304",
        "400", "401", "403", "404", "405", "409", "422", "429",
        "500", "501", "502", "503", "504",
    }
    SERVER_PATTERNS = ["<--", "HTTP/", "status:"]
    LOGCAT_PATTERNS = [
        "http", "HTTP/", "status", "response", "okhttp",
        "retrofit", "NetworkDispatcher", "StatusCode",
        "Content-Type", "Authorization", "<--", "-->",
    ]

    if raw_logs:
        status_count = {}
        http_lines   = []
        total_http   = 0

        for msg in raw_logs:
            patterns = SERVER_PATTERNS if source == "server" else LOGCAT_PATTERNS
            is_http  = any(p in (msg if source == "server" else msg.lower()) for p in patterns)
            if is_http:
                total_http += 1
                http_lines.append(msg)
                for part in msg.split():
                    clean = "".join(c for c in part if c.isdigit())
                    if clean in HTTP_STATUS_CODES:
                        status_count[clean] = status_count.get(clean, 0) + 1
                        break

        add(f"📋 SOURCE: {source} | TOTAL LOGS: {len(raw_logs)} | HTTP-RELATED: {total_http}")
        add("-" * 60)

        if status_count:
            add("   📊 STATUS CODES DETECTED:")
            for code, count in sorted(status_count.items()):
                emoji = "✅" if code.startswith("2") else ("🔄" if code.startswith("3") else ("⚠️" if code.startswith("4") else "❌"))
                add(f"      {emoji} HTTP {code}: {count} RESPONSE(S)")
        else:
            add(f"   ℹ️  NO HTTP STATUS CODES DETECTED IN {source} LOGS.")
            add("   📝 LAST 10 LOG ENTRIES FOR DEBUGGING:")
            for i, entry in enumerate(raw_logs[-10:]):
                add(f"      [{i + 1}] {entry[:150]}")

        # SAVE FULL EVIDENCE TO FILE
        with open(evidence_path, "w", encoding="utf-8") as f:
            f.write(f"EVIDENCE: {nombre_test} | SOURCE: {source}\n")
            f.write(f"TIMESTAMP: {datetime.now().isoformat()}\n")
            f.write(f"TOTAL LOGS: {len(raw_logs)} | HTTP-RELATED: {total_http}\n")
            f.write("=" * 60 + "\n\n")
            if http_lines:
                f.write("--- HTTP-RELATED LOGS ---\n")
                for ln in http_lines[-200:]:
                    f.write(ln + ("\n" if not ln.endswith("\n") else ""))
                f.write("\n\n")
            f.write("--- ALL RAW LOGS (LAST 500) ---\n")
            for ln in raw_logs[-500:]:
                f.write(ln + ("\n" if not ln.endswith("\n") else ""))

        add(f"✔ EVIDENCE SAVED: {evidence_path}")
    else:
        add("   ❌ NO LOGS AVAILABLE FROM ANY SOURCE (SERVER OR LOGCAT).")
        add("   💡 OPTION 1: appium --relaxed-security")
        add("   💡 OPTION 2: appium --allow-insecure=get_server_logs")

    add(f"{'=' * 60}\n")


# ==================================================================================
# [4] WEB PLATFORM — SELENIUM DRIVER & INTERACTIONS
# ==================================================================================

def iniciar_driver_web():
    """
    STARTS A CHROME SESSION MANAGED BY WEBDRIVER MANAGER.
    ENABLES PERFORMANCE LOGGING (REQUIRED FOR print_http_evidence).
    RETURNS (driver, wait) TUPLE.
    """
    print("🚀 STARTING WEB AUTOMATION SESSION...")
    options = selenium_webdriver.ChromeOptions()
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    options.add_argument("--start-maximized")
    service = ChromeService(ChromeDriverManager().install())
    driver  = selenium_webdriver.Chrome(service=service, options=options)
    wait    = WebDriverWait(driver, config.WEB_EXPLICIT_WAIT)
    print("   ✅ CHROME SESSION STARTED.")
    return driver, wait


def print_http_evidence(driver, endpoint_clave):
    """
    SCANS CHROME PERFORMANCE LOGS FOR NETWORK TRAFFIC MATCHING endpoint_clave.
    PRINTS A FORMATTED SUMMARY OF ALL MATCHED REQUEST/RESPONSE PAIRS.
    PASSWORDS IN PAYLOADS ARE AUTOMATICALLY MASKED.

    REQUIREMENT: DRIVER MUST BE STARTED WITH goog:loggingPrefs performance: ALL.
    """
    print(f"\n📡 SCANNING NETWORK TRAFFIC FOR ENDPOINT: '{endpoint_clave}'...")
    try:
        logs         = driver.get_log("performance")
        requests_map = {}
        responses    = []

        for entry in logs:
            log_json = json.loads(entry["message"])["message"]
            method   = log_json["method"]
            params   = log_json.get("params", {})

            if method == "Network.requestWillBeSent":
                req = params.get("request", {})
                url = req.get("url", "")
                if endpoint_clave in url:
                    rid = params.get("requestId", "")
                    requests_map[rid] = {
                        "url"      : url,
                        "method"   : req.get("method", "UNKNOWN"),
                        "postData" : req.get("postData", None),
                    }

            if method == "Network.responseReceived":
                resp = params.get("response", {})
                url  = resp.get("url", "")
                if endpoint_clave in url:
                    responses.append({
                        "requestId": params.get("requestId", ""),
                        "url"      : url,
                        "status"   : resp.get("status", "N/A"),
                        "mimeType" : resp.get("mimeType", "N/A"),
                    })

        if not responses:
            print(f"   ⚠️  NO HTTP TRAFFIC FOUND FOR: '{endpoint_clave}'")
            return

        for i, resp in enumerate(responses, 1):
            req_info    = requests_map.get(resp["requestId"], {})
            http_method = req_info.get("method", "UNKNOWN")
            post_data   = req_info.get("postData", None)
            status      = resp["status"]

            print("-" * 60)
            print(f"📋 MATCH #{i}")
            print(f"🔗 URL      : {resp['url']}")
            print(f"📨 METHOD   : {http_method}")
            print(f"📦 STATUS   : {status} (HTTP CODE)")
            print(f"📄 MIME TYPE: {resp['mimeType']}")

            if post_data:
                try:
                    safe = json.loads(post_data)
                    if "password" in safe:
                        safe["password"] = "********"
                    print(f"📤 PAYLOAD  : {json.dumps(safe)}")
                except Exception:
                    print("📤 PAYLOAD  : [RAW DATA PRESENT — NOT JSON]")

            print("-" * 60)

            # STATUS INTERPRETATION
            if http_method == "POST":
                interpretations = {
                    200: "✅ SERVER: REQUEST SUCCESSFUL",
                    201: "✅ SERVER: RESOURCE CREATED",
                    400: "⛔ SERVER: BAD REQUEST",
                    401: "🔒 SERVER: UNAUTHORIZED",
                    403: "🚫 SERVER: FORBIDDEN",
                    404: "🔍 SERVER: NOT FOUND",
                    500: "💥 SERVER: INTERNAL SERVER ERROR",
                }
                print(interpretations.get(status, f"⚠️ SERVER: UNEXPECTED CODE {status}"))

    except Exception as e:
        print(f"❌ ERROR READING HTTP LOGS: {e}")


def diagnosticar_trafico(driver):
    """
    PRINTS A FULL DUMP OF ALL NON-STATIC NETWORK TRAFFIC CAPTURED BY CHROME.
    USEFUL DURING EXPLORATORY DEBUG SESSIONS TO DISCOVER REAL ENDPOINT NAMES.
    STATIC ASSETS (CSS, JS, FONTS, IMAGES) ARE FILTERED OUT AUTOMATICALLY.
    """
    print("\n🔬 FULL NETWORK TRAFFIC DIAGNOSTIC")
    print("=" * 70)
    try:
        logs         = driver.get_log("performance")
        requests_map = {}
        SKIP_EXTENSIONS = [".css", ".js", ".png", ".jpg", ".svg", ".woff", ".ttf",
                           "favicon", "fonts", "google", "analytics"]

        for entry in logs:
            log_json = json.loads(entry["message"])["message"]
            method   = log_json["method"]
            params   = log_json.get("params", {})

            if method == "Network.requestWillBeSent":
                req = params.get("request", {})
                rid = params.get("requestId", "")
                requests_map[rid] = {
                    "method"   : req.get("method", ""),
                    "url"      : req.get("url", ""),
                    "postData" : req.get("postData", None),
                }

            if method == "Network.responseReceived":
                resp     = params.get("response", {})
                rid      = params.get("requestId", "")
                url      = resp.get("url", "")
                status   = resp.get("status", "")
                mime     = resp.get("mimeType", "")
                req_info = requests_map.get(rid, {})

                if any(s in url.lower() for s in SKIP_EXTENSIONS):
                    continue

                print(f"  {req_info.get('method', '?'):6} | {status} | {mime:30} | {url[:100]}")
                if req_info.get("postData"):
                    print(f"         📤 PAYLOAD: {req_info['postData'][:150]}")

        print("=" * 70)
    except Exception as e:
        print(f"❌ DIAGNOSTIC ERROR: {e}")


def verificar_validacion_frontend(driver):
    """
    CHECKS IF ANY VISIBLE ERROR/ALERT/WARNING ELEMENTS ARE PRESENT IN THE DOM.
    USEFUL FOR DETECTING FRONT-END ONLY VALIDATION (NO HTTP REQUEST SENT).
    RETURNS True IF VALIDATION MESSAGES ARE FOUND, False OTHERWISE.
    """
    try:
        error_msgs = driver.find_elements(
            By.XPATH,
            "//*[contains(@class, 'error') or contains(@class, 'alert') or contains(@class, 'warning')]"
        )
        if error_msgs:
            for msg in error_msgs:
                text = msg.text.strip()
                if text:
                    print(f"🔸 FRONTEND VALIDATION MESSAGE: '{text}'")
            return True
        else:
            print("🔸 FRONTEND VALIDATION: NO MESSAGES FOUND — SUBMISSION MAY NOT HAVE BEEN BLOCKED.")
            return False
    except Exception as e:
        print(f"⚠️  COULD NOT READ FRONTEND VALIDATION: {e}")
        return False


def click_eye_button(driver, xpath, descripcion="EYE BUTTON"):
    """
    CLICKS A PASSWORD VISIBILITY TOGGLE (EYE ICON) USING THREE ESCALATING STRATEGIES:
        1. STANDARD WebDriverWait + CLICK (RELIABLE WHEN ELEMENT IS ACCESSIBLE).
        2. JAVASCRIPT CLICK (BYPASSES UI OVERLAPS FROM ANGULAR/PRIMENG OVERLAYS).
        3. JAVASCRIPT CLICK ON THE PARENT ELEMENT (WHEN THE ICON ITSELF IS NOT CLICKABLE).
    RETURNS True IF ANY STRATEGY SUCCEEDS, False IF ALL FAIL.
    """
    print(f"👁️  ATTEMPTING TO CLICK: {descripcion}")
    try:
        wait    = WebDriverWait(driver, 5)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()
        print(f"   ✔ CLICKED (SELENIUM WAIT): {descripcion}")
        return True
    except Exception:
        pass

    try:
        element = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].click();", element)
        print(f"   ✔ CLICKED (JAVASCRIPT): {descripcion}")
        return True
    except Exception:
        pass

    try:
        parent = driver.find_element(By.XPATH, xpath + "/..")
        driver.execute_script("arguments[0].click();", parent)
        print(f"   ✔ CLICKED (PARENT + JAVASCRIPT): {descripcion}")
        return True
    except Exception:
        print(f"   ❌ ALL CLICK STRATEGIES FAILED FOR: {descripcion}")
        return False


def obtener_link_recuperacion_imap(usuario_email, password_app):
    """
    CONNECTS TO GMAIL VIA IMAP, FINDS THE LATEST PASSWORD RESET EMAIL FROM
    no-reply@memphis.mx, AND EXTRACTS THE CLEAN RECOVERY LINK.

    REQUIREMENTS:
        - GMAIL IMAP ACCESS MUST BE ENABLED IN THE ACCOUNT SETTINGS.
        - USE AN APP PASSWORD, NOT THE ACCOUNT'S MAIN PASSWORD.

    RETURNS:
        str  — THE CLEAN RECOVERY URL IF FOUND.
        None — IF NO EMAIL OR LINK WAS FOUND.
    """
    print(f"\n📧 CONNECTING TO IMAP SERVER FOR: {usuario_email}...")
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(usuario_email, password_app)

        folders      = ["INBOX", "[Gmail]/All Mail", "[Gmail]/Spam"]
        email_ids    = []
        sender       = "no-reply@memphis.mx"

        for folder in folders:
            try:
                print(f"   📂 SCANNING FOLDER: {folder}...")
                mail.select(folder)
                _, data = mail.search(None, f'(FROM "{sender}")')
                if data[0]:
                    ids = data[0].split()
                    if ids:
                        email_ids = ids[-3:]
                        break
            except Exception:
                continue

        if not email_ids:
            print(f"   ❌ NO EMAILS FOUND FROM '{sender}'.")
            return None

        email_ids.reverse()
        latest_id = email_ids[0]
        print(f"   🔎 ANALYZING EMAIL ID: {latest_id.decode()}...")
        _, msg_data = mail.fetch(latest_id, "(RFC822)")

        raw = msg_data[0][1]
        msg = email.message_from_bytes(raw)

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    try:
                        body += part.get_payload(decode=True).decode(errors="ignore")
                    except Exception:
                        pass
        else:
            try:
                body = msg.get_payload(decode=True).decode(errors="ignore")
            except Exception:
                pass

        pattern = r"https?://(?:fat|api)\.memphis\.mx/resetPwd[^\s\"'<>]+"
        urls    = re.findall(pattern, body)

        if urls:
            raw_link   = urls[0]
            clean_link = html.unescape(raw_link)
            clean_link = urllib.parse.unquote(clean_link)
            clean_link = clean_link.replace("&amp;", "&").replace("&%23x3D;", "=")
            print(f"   ✅ RECOVERY LINK EXTRACTED: {clean_link}")
            mail.close()
            mail.logout()
            return clean_link
        else:
            print("   ❌ EMAIL FOUND BUT CONTAINS NO RECOVERY LINK.")
            mail.close()
            mail.logout()
            return None

    except Exception as e:
        print(f"   ❌ CRITICAL IMAP ERROR: {e}")
        return None


# ==================================================================================
# [5] REPORTING ENGINE — DUAL LOGGER, HTML REPORT, ZIP PACKAGER
# ==================================================================================

class DualLogger:
    """
    INTERCEPTS sys.stdout TO WRITE EVERY PRINT STATEMENT TO BOTH:
        - THE TERMINAL (LIVE OUTPUT DURING TEST EXECUTION).
        - A TEXT FILE  (PERSISTENT LOG FOR REPORT GENERATION).

    USAGE:
        logger = DualLogger("path/to/log.txt")
        sys.stdout = logger
        ...run tests...
        logger.close()  # ALWAYS CALL IN A finally BLOCK
    """
    def __init__(self, filepath):
        self.terminal = sys.stdout
        self.log_file = open(filepath, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log_file.write(message)
        self.log_file.flush()  # FORCE DISK WRITE ON EVERY LINE (SAFE ON CRASH)

    def flush(self):
        self.terminal.flush()
        self.log_file.flush()

    def close(self):
        if not self.log_file.closed:
            self.log_file.close()
        sys.stdout = self.terminal  # RESTORE NORMAL TERMINAL OUTPUT


def iniciar_reporte(nombre_modulo):
    """
    STARTS DUAL LOGGING FOR A TEST MODULE EXECUTION.
    CREATES THE OUTPUT DIRECTORY AND RETURNS THE LOGGER, LOG PATH, AND TIMESTAMP.

    ALWAYS USE THIS PATTERN:
        logger, log_file, timestamp = utils.iniciar_reporte("MODULE_NAME")
        try:
            run_tests()
        finally:
            utils.generar_reporte_html("MODULE_NAME", log_file, timestamp)
    """
    os.makedirs("evidencias_zip", exist_ok=True)
    timestamp    = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"evidencias_zip/{nombre_modulo}_LOG_{timestamp}.txt"

    print(f"\n⏺️  STARTING LOG RECORDING FOR MODULE: {nombre_modulo}...")
    logger     = DualLogger(log_filename)
    sys.stdout = logger

    return logger, log_filename, timestamp


def generar_zip_evidencias(nombre_modulo, logger, log_filename, timestamp):
    """
    PACKAGES ALL EVIDENCE (TEXT LOG + SCREENSHOTS + APPIUM FILES) INTO A SINGLE ZIP.
    OUTPUT: evidencias_zip/{nombre_modulo}_FULL_REPORT_{timestamp}.zip

    NOTE: CALL logger.close() BEFORE THIS FUNCTION SO THE LOG FILE IS FULLY WRITTEN.
    """
    logger.close()
    print("\n📦 PACKAGING EVIDENCE INTO ZIP FILE...")

    zip_path = f"evidencias_zip/{nombre_modulo}_FULL_REPORT_{timestamp}.zip"
    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            if os.path.exists(log_filename):
                zf.write(log_filename, os.path.basename(log_filename))

            for folder in ("evidencias/Web", "evidencias/T6"):
                if os.path.exists(folder):
                    for file in os.listdir(folder):
                        if file.endswith(".png"):
                            zf.write(os.path.join(folder, file), f"screenshots/{file}")

            if os.path.exists("evidencias_zip"):
                for file in os.listdir("evidencias_zip"):
                    if "APPIUM_EVIDENCE" in file and file.endswith(".txt"):
                        zf.write(os.path.join("evidencias_zip", file), f"appium_evidence/{file}")

        print(f"✅ ZIP REPORT GENERATED: {zip_path}")
        return zip_path
    except Exception as e:
        print(f"❌ ERROR GENERATING ZIP: {e}")
        return None


def generar_reporte_html(nombre_modulo, log_filename, timestamp):
    """
    READS THE DUAL-LOGGER TEXT FILE AND GENERATES A PROFESSIONAL HTML REPORT.
    FEATURES:
        - AUTOMATIC PASS/FAIL METRIC BADGES.
        - COLOR-CODED LOG LINES (SUCCESS / ERROR / WARNING / INFO / HEADER).
        - SCREENSHOTS EMBEDDED AS BASE64 DIRECTLY IN THE HTML (NO EXTERNAL FILES NEEDED).
    OUTPUT: evidencias_zip/{nombre_modulo}_REPORT_{timestamp}.html
    """
    html_filename = f"evidencias_zip/{nombre_modulo}_REPORT_{timestamp}.html"
    print(f"\n📄 GENERATING HTML REPORT...")

    try:
        with open(log_filename, "r", encoding="utf-8") as f:
            lines = f.readlines()

        total_pass = sum(1 for l in lines if "✅" in l and ": SUCCESS" in l.upper())
        total_fail = sum(1 for l in lines if "❌" in l and (": FAILED" in l.upper() or "CRITICAL ERROR" in l.upper()))
        fecha      = datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>QA Report | {nombre_modulo}</title>
    <style>
        :root {{
            --bg-main: #f4f7f9; --bg-card: #ffffff;
            --primary: #1e293b; --secondary: #64748b;
            --success: #10b981; --danger: #ef4444;
            --log-bg: #0f172a;  --log-text: #e2e8f0;
        }}
        body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: var(--bg-main); color: var(--primary); margin: 0; padding: 30px; line-height: 1.5; }}
        .header {{ background: var(--bg-card); padding: 25px 30px; border-radius: 10px; box-shadow: 0 4px 6px -1px rgba(0,0,0,.05); display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; border-left: 6px solid var(--primary); }}
        .header h1 {{ margin: 0 0 5px; font-size: 24px; }}
        .header p  {{ margin: 0; color: var(--secondary); font-size: 14px; font-weight: 500; }}
        .metrics   {{ display: flex; gap: 15px; }}
        .badge     {{ padding: 12px 20px; border-radius: 8px; font-weight: 600; font-size: 15px; color: #fff; display: flex; flex-direction: column; align-items: center; min-width: 80px; box-shadow: 0 2px 4px rgba(0,0,0,.1); }}
        .badge span {{ font-size: 24px; margin-top: 4px; }}
        .badge-pass {{ background: var(--success); }}
        .badge-fail {{ background: var(--danger); }}
        .container  {{ background: var(--bg-card); padding: 25px; border-radius: 10px; box-shadow: 0 4px 6px -1px rgba(0,0,0,.05); }}
        .section-title {{ font-size: 18px; margin: 0 0 15px; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }}
        .terminal  {{ background: var(--log-bg); color: var(--log-text); padding: 20px; border-radius: 8px; font-family: 'Consolas','Courier New',monospace; font-size: 13px; overflow-x: auto; }}
        .log-line    {{ margin: 3px 0; white-space: pre-wrap; word-wrap: break-word; }}
        .log-success {{ color: #34d399; font-weight: bold; }}
        .log-error   {{ color: #f87171; font-weight: bold; }}
        .log-info    {{ color: #38bdf8; }}
        .log-warning {{ color: #facc15; }}
        .log-header  {{ color: #cbd5e1; font-weight: bold; padding-top: 15px; border-bottom: 1px dashed #334155; padding-bottom: 5px; margin-bottom: 5px; }}
        .evidence-card  {{ background: #1e293b; margin: 20px 0; padding: 15px; border-left: 4px solid #38bdf8; border-radius: 6px; }}
        .evidence-title {{ color: #7dd3fc; font-size: 12px; font-weight: bold; margin-bottom: 10px; text-transform: uppercase; letter-spacing: .5px; }}
        .evidence-img   {{ max-width: 100%; height: auto; border-radius: 4px; display: block; }}
    </style>
</head>
<body>
<div class="header">
    <div>
        <h1>📊 Automated Test Execution Report</h1>
        <p>Module: <strong>{nombre_modulo}</strong> &nbsp;|&nbsp; Environment: QA &nbsp;|&nbsp; Executed: {fecha}</p>
    </div>
    <div class="metrics">
        <div class="badge badge-pass">PASSED <span>{total_pass}</span></div>
        <div class="badge badge-fail">FAILED <span>{total_fail}</span></div>
    </div>
</div>
<div class="container">
    <h2 class="section-title">Terminal Logs &amp; Evidence</h2>
    <div class="terminal">
"""
        for line in lines:
            clean = line.replace("<", "&lt;").replace(">", "&gt;").strip("\n")
            if not clean.strip():
                html_content += "<br>\n"
                continue

            css = "log-line"
            if "✅" in clean or "SUCCESS" in clean:            css += " log-success"
            elif "❌" in clean or "FAILED" in clean or "ERROR" in clean: css += " log-error"
            elif any(e in clean for e in ["📡","🌐","🚀","👉","✍️"]): css += " log-info"
            elif "⚠️" in clean or "WARNING" in clean:          css += " log-warning"
            elif "===" in clean:                               css += " log-header"

            html_content += f'<div class="{css}">{clean}</div>\n'

            if "✔ SCREENSHOT TAKEN:" in clean:
                parts = clean.split("SCREENSHOT TAKEN:")
                if len(parts) > 1:
                    img_path = parts[1].strip()
                    if os.path.exists(img_path):
                        with open(img_path, "rb") as img:
                            b64 = base64.b64encode(img.read()).decode()
                        img_name = os.path.basename(img_path)
                        html_content += f"""
<div class="evidence-card">
    <div class="evidence-title">📸 VISUAL EVIDENCE: {img_name}</div>
    <img class="evidence-img" src="data:image/png;base64,{b64}" alt="QA Evidence">
</div>
"""
        html_content += """
    </div>
</div>
</body>
</html>
"""
        with open(html_filename, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"✅ HTML REPORT GENERATED: {html_filename}")
        print("=" * 70 + "\n")
        return html_filename

    except Exception as e:
        print(f"❌ ERROR GENERATING HTML REPORT: {e}")
        return None