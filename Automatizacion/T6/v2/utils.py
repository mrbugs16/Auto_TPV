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

def take_screenshot(driver, name, platform="auto"):
    """
    SAVES A SCREENSHOT TO THE APPROPRIATE EVIDENCE SUBFOLDER.
    AUTO-DETECTS PLATFORM (T6 vs WEB) BASED ON DRIVER CAPABILITIES.
    OUTPUT PATHS:
        T6  → evidence/T6/{name}.png
        WEB → evidence/Web/{name}.png
    """
    if platform == "auto":
        try:
            caps = driver.capabilities
            if (
                "automationName" in caps or
                "deviceName" in caps or
                "appium" in str(caps).lower()
            ):
                platform = "t6"
            else:
                platform = "web"
        except:
            platform = "web"

    folder = os.path.join("evidence", "T6" if platform == "t6" else "Web")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{name}.png")
    driver.save_screenshot(path)
    print(f"✔ SCREENSHOT TAKEN: {path}")


def click_element(driver, xpath):
    """
    CLICKS AN ELEMENT LOCATED BY XPATH.
    PRINTS THE FULL ERROR MESSAGE IF THE ELEMENT IS NOT FOUND OR NOT CLICKABLE.
    WORKS FOR BOTH APPIUM (T6) AND SELENIUM (WEB) DRIVERS.
    """
    try:
        driver.find_element(By.XPATH, xpath).click()
    except Exception as e:
        print(f"✘ ERROR CLICKING {xpath}: {e}")


def type_text(driver, xpath, text):
    """
    LOCATES AN INPUT FIELD BY XPATH, CLICKS IT, AND TYPES THE GIVEN TEXT.
    WORKS FOR BOTH APPIUM (T6) AND SELENIUM (WEB) DRIVERS.
    """
    try:
        el = driver.find_element(By.XPATH, xpath)
        el.click()
        el.send_keys(text)
    except Exception as e:
        print(f"✘ ERROR WRITING TO {xpath}: {e}")


def verify_element(wait, xpath, description, driver_debug=None):
    """
    WAITS UP TO THE DRIVER'S CONFIGURED TIMEOUT FOR AN ELEMENT TO APPEAR IN THE DOM.
    RETURNS True IF FOUND, False OTHERWISE.
    WORKS FOR BOTH APPIUM (T6) AND SELENIUM (WEB) DRIVERS.
    """
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        print(f"✔ POPUP / ELEMENT DETECTED: {description}")
        return True
    except Exception:
        print(f"⚠ ALERT: NOT FOUND '{description}'")
        return False


# ==================================================================================
# [3] T6 MOBILE — APPIUM DRIVER & INTERACTIONS
# ==================================================================================

def start_driver():
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


def close_driver(driver):
    """
    GRACEFULLY TERMINATES THE APPIUM SESSION.
    ALWAYS CALLED IN THE finally BLOCK OF EACH TEST FUNCTION.
    """
    print("🏁 CLOSING T6 SESSION...")
    time.sleep(2)
    driver.quit()


def print_http_evidence_appium(driver, test_name):
    """
    CAPTURES APPIUM SERVER LOGS OR ANDROID LOGCAT AS HTTP TRAFFIC EVIDENCE.
    SAVES A FULL TXT FILE TO zip_evidence/ AND PRINTS A STATUS CODE SUMMARY.

    REQUIREMENTS:
        START APPIUM WITH ONE OF THESE FLAGS TO ENABLE SERVER LOGS:
            appium --relaxed-security
            appium --allow-insecure=get_server_logs
    """
    os.makedirs("zip_evidence", exist_ok=True)
    ts            = datetime.now().strftime("%Y%m%d_%H%M%S")
    evidence_path = f"zip_evidence/{test_name}_APPIUM_EVIDENCE_{ts}.txt"

    lines = []
    def add(msg=""):
        lines.append(msg)
        print(msg)

    add(f"\n{'=' * 60}")
    add(f"📡 HTTP EVIDENCE — {test_name} (APPIUM / SERVER LOGS)")
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
            f.write(f"EVIDENCE: {test_name} | SOURCE: {source}\n")
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

def start_web_driver():
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


def diagnose_traffic(driver):
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


def verify_frontend_validation(driver):
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


def click_eye_button(driver, xpath, description="EYE BUTTON"):
    """
    CLICKS A PASSWORD VISIBILITY TOGGLE (EYE ICON) USING THREE ESCALATING STRATEGIES:
        1. STANDARD WebDriverWait + CLICK (RELIABLE WHEN ELEMENT IS ACCESSIBLE).
        2. JAVASCRIPT CLICK (BYPASSES UI OVERLAPS FROM ANGULAR/PRIMENG OVERLAYS).
        3. JAVASCRIPT CLICK ON THE PARENT ELEMENT (WHEN THE ICON ITSELF IS NOT CLICKABLE).
    RETURNS True IF ANY STRATEGY SUCCEEDS, False IF ALL FAIL.
    """
    print(f"👁️  ATTEMPTING TO CLICK: {description}")
    try:
        wait    = WebDriverWait(driver, 5)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()
        print(f"   ✔ CLICKED (SELENIUM WAIT): {description}")
        return True
    except Exception:
        pass

    try:
        element = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].click();", element)
        print(f"   ✔ CLICKED (JAVASCRIPT): {description}")
        return True
    except Exception:
        pass

    try:
        parent = driver.find_element(By.XPATH, xpath + "/..")
        driver.execute_script("arguments[0].click();", parent)
        print(f"   ✔ CLICKED (PARENT + JAVASCRIPT): {description}")
        return True
    except Exception:
        print(f"   ❌ ALL CLICK STRATEGIES FAILED FOR: {description}")
        return False


def get_recovery_link_imap(usuario_email, password_app):
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

# LINE TIMESTAMPS PER LOG FILE, FILLED BY DualLogger AND READ BY generate_html_report
_LINE_TIMES = {}


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
        # HH:MM:SS OF EVERY LOG LINE (THE HTML REPORT SHOWS THE TIME OF EACH STEP)
        self.times = _LINE_TIMES.setdefault(filepath, [])

    def write(self, message):
        self.times.extend([datetime.now().strftime("%H:%M:%S")] * message.count("\n"))
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


def start_report(module_name):
    """
    STARTS DUAL LOGGING FOR A TEST MODULE EXECUTION.
    CREATES THE OUTPUT DIRECTORY AND RETURNS THE LOGGER, LOG PATH, AND TIMESTAMP.

    ALWAYS USE THIS PATTERN:
        logger, log_file, timestamp = utils.start_report("MODULE_NAME")
        try:
            run_tests()
        finally:
            utils.generate_html_report("MODULE_NAME", log_file, timestamp)
    """
    os.makedirs("zip_evidence", exist_ok=True)
    timestamp    = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"zip_evidence/{module_name}_LOG_{timestamp}.txt"

    print(f"\n⏺️  STARTING LOG RECORDING FOR MODULE: {module_name}...")
    logger     = DualLogger(log_file)
    sys.stdout = logger

    return logger, log_file, timestamp


def generate_zip_report(module_name, logger, log_file, timestamp):
    """
    PACKAGES ALL EVIDENCE (TEXT LOG + SCREENSHOTS + APPIUM FILES) INTO A SINGLE ZIP.
    OUTPUT: zip_evidence/{module_name}_FULL_REPORT_{timestamp}.zip

    NOTE: CALL logger.close() BEFORE THIS FUNCTION SO THE LOG FILE IS FULLY WRITTEN.
    """
    logger.close()
    print("\n📦 PACKAGING EVIDENCE INTO ZIP FILE...")

    zip_path = f"zip_evidence/{module_name}_FULL_REPORT_{timestamp}.zip"
    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            if os.path.exists(log_file):
                zf.write(log_file, os.path.basename(log_file))

            for folder in ("evidence/Web", "evidence/T6"):
                if os.path.exists(folder):
                    for file in os.listdir(folder):
                        if file.endswith(".png"):
                            zf.write(os.path.join(folder, file), f"screenshots/{file}")

            if os.path.exists("zip_evidence"):
                for file in os.listdir("zip_evidence"):
                    if "APPIUM_EVIDENCE" in file and file.endswith(".txt"):
                        zf.write(os.path.join("zip_evidence", file), f"appium_evidence/{file}")

        print(f"✅ ZIP REPORT GENERATED: {zip_path}")
        return zip_path
    except Exception as e:
        print(f"❌ ERROR GENERATING ZIP: {e}")
        return None


def _classify_log_line(line):
    """
    CLASSIFIES A SINGLE LOG LINE AS "pass", "fail" OR "other".
    SHARED BY THE METRIC COUNTERS AND THE PER-LINE data-status ATTRIBUTE
    USED BY THE HTML REPORT'S CLICKABLE PASS/FAIL/ALL FILTER, SO THE
    COUNTERS AND THE FILTERED VIEW ALWAYS AGREE.
    MATCHES BOTH FORMATS:
        FORMAT A (result summary): "📊 LG-005 RESULT: SUCCESS" / "RESULT: FAIL"
        FORMAT B (inline):         "✅ ... : SUCCESS"          / "❌ ... : FAILED"
    """
    upper = line.upper()
    if ("RESULT: SUCCESS" in upper) or ("✅" in line and ": SUCCESS" in upper):
        return "pass"
    if ("RESULT: FAIL" in upper and "RESULT: FAILURE" not in upper) or \
       ("❌" in line and (": FAILED" in upper or "CRITICAL ERROR" in upper)):
        return "fail"
    return "other"


# LOGO SHOWN AT THE TOP OF THE HTML REPORT.
# EXPECTED AT: <PROJECT_ROOT>/assets/memphis_logo.png
# IF THE FILE IS MISSING THE REPORT STILL GENERATES NORMALLY, JUST WITHOUT THE LOGO.
LOGO_PATH = os.path.join("assets", "memphis_logo.png")

# TEST MATRICES (EXCEL) USED TO ENRICH EACH CASE: ID → MODULE, STEPS, EXPECTED RESULT...
MATRICES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Matrices")

# "TC-MSI-008: TITLE" / "TEST TIP-04: TITLE" — ONLY RIGHT AFTER A ===== OR ----- RULE
_CASE_HEADER = re.compile(r"^\s*(?:TEST\s+)?([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+):\s+(.+?)\s*$")
_CASE_RESULT = re.compile(r"📊\s*(\S+)\s+RESULT:\s*(.+?)\s*$")
_RULE        = re.compile(r"^\s*[=\-]{20,}\s*$")


def _norm(text):
    """'Opción de Pago' → 'opcion de pago' (MATRIX HEADER MATCHING)."""
    import unicodedata
    text = unicodedata.normalize("NFKD", str(text or "")).encode("ascii", "ignore").decode()
    return " ".join(text.lower().split())


def _load_matrices():
    """
    READS EVERY Matrices/*.xlsx SHEET WHOSE HEADER ROW STARTS WITH 'ID'.
    RETURNS {CASE_ID: {normalized_header: value}}. EMPTY IF openpyxl OR THE FOLDER IS MISSING.
    """
    rows = {}
    if not os.path.isdir(MATRICES_DIR):
        return rows
    try:
        import openpyxl
    except ImportError:
        print("⚠️ openpyxl NOT INSTALLED — REPORT GENERATED WITHOUT MATRIX DATA")
        return rows
    for file in os.listdir(MATRICES_DIR):
        if not file.lower().endswith(".xlsx") or file.startswith("~$"):
            continue
        try:
            wb = openpyxl.load_workbook(os.path.join(MATRICES_DIR, file), read_only=True, data_only=True)
            for ws in wb.worksheets:
                headers = None
                for row in ws.iter_rows(values_only=True):
                    if headers is None:
                        if row and _norm(row[0]) == "id":
                            headers = [_norm(h) for h in row]
                        continue
                    if row and row[0]:
                        rows[str(row[0]).strip()] = dict(zip(headers, row))
            wb.close()
        except Exception as e:
            print(f"⚠️ COULD NOT READ MATRIX {file}: {e}")
    return rows


def _device_info(log_text):
    """MODEL / ANDROID / APP FOR THE REPORT HEADER (adb IS BEST EFFORT, NEVER BLOCKS THE REPORT)."""
    import subprocess
    caps    = getattr(config, "CAPABILITIES", {})
    package = caps.get("appium:appPackage", "")
    match   = re.search(r"DEVICE:\s*(\S+)", log_text)
    info = {
        "modelo":  match.group(1) if match else caps.get("appium:deviceName", "T6"),
        "android": caps.get("appium:platformVersion", ""),
        "app":     package,
        "serial":  "",
    }

    def adb(*args):
        out = subprocess.run(["adb", *args], capture_output=True, text=True, timeout=4)
        return out.stdout.strip()

    try:
        serials = [l.split()[0] for l in adb("devices").splitlines()[1:] if l.strip().endswith("device")]
        if serials:
            info["serial"]  = serials[0]
            info["android"] = adb("shell", "getprop", "ro.build.version.release") or info["android"]
            version = re.search(r"versionName=(\S+)", adb("shell", "dumpsys", "package", package))
            if version:
                info["app"] = f"{package} {version.group(1)}"
    except Exception:
        pass
    return info


def _image_data_uri(path):
    """SCREENSHOT AS BASE64 SO THE REPORT STAYS A SINGLE SELF-CONTAINED HTML FILE."""
    with open(path, "rb") as img:
        return "data:image/png;base64," + base64.b64encode(img.read()).decode()


def _step_kind(line):
    """
    WHICH LOG LINES BECOME TIMELINE STEPS: ok | fallo | info. None = ONLY IN THE CASE LOG.
    SCREEN DUMPS, COUNTDOWNS AND DECORATION STAY IN THE LOG TO KEEP THE TIMELINE READABLE.
    """
    if _classify_log_line(line) == "fail" or any(m in line for m in ("❌", "✘", "💥")):
        return "fallo"
    if "✅" in line or line.startswith("✔"):
        return "ok"
    if any(m in line for m in ("👉", "⚠️", "⏱️", "ℹ️", "🖐️  ")):
        return "info"
    return None


def _case_status(result_text, note):
    upper = result_text.upper()
    if upper.startswith(("SUCCESS", "PASS")):
        return "Aprobado"
    if "SKIP" in upper or "MANUAL" in upper:
        return "Manual"
    if "CRITICAL ERROR" in note.upper() or "ERROR" in upper:
        return "Error"
    return "Fallido"


def _split_cases(lines, times):
    """
    SPLITS THE RUN LOG INTO CASES:
        - A CASE OPENS ON A "<ID>: <TITLE>" LINE THAT FOLLOWS A ===== / ----- RULE.
        - A CASE CLOSES ON "📊 <ID> RESULT: ...". SUITES WITHOUT A HEADER LINE GET A CASE
          MADE OF THE LINES SINCE THE PREVIOUS RESULT.
        - A CASE THAT NEVER PRINTED ITS RESULT IS REPORTED AS "Error" (RUN INTERRUPTED).
    RETURNS A LIST OF DICTS: id, titulo, lineas [(text, time)], resultado, nota.
    """
    cases, current, pending = [], None, []
    prev = ""
    for idx, raw in enumerate(lines):
        line = raw.rstrip("\n")
        stamp = times[idx] if idx < len(times) else ""
        header = _CASE_HEADER.match(line) if _RULE.match(prev) else None
        result = _CASE_RESULT.search(line)
        if header and not result:
            if current:
                cases.append(current)
            current = {"id": header.group(1), "titulo": header.group(2), "lineas": [],
                       "resultado": None, "nota": ""}
            pending = []
        elif result:
            if current is None:
                current = {"id": result.group(1), "titulo": "", "lineas": pending,
                           "resultado": None, "nota": ""}
            text = result.group(2)
            parts = re.split(r"\s+[—–-]\s+", text, maxsplit=1)
            current["resultado"] = parts[0].strip()
            current["nota"] = parts[1].strip() if len(parts) > 1 else ""
            current["lineas"].append((line, stamp))
            cases.append(current)
            current, pending = None, []
        elif current is not None:
            current["lineas"].append((line, stamp))
        else:
            pending.append((line, stamp))
        if line.strip():
            prev = line
    if current:
        cases.append(current)
    return cases


def _build_case(case, matrix, module_name):
    """TURNS A PARSED LOG CASE INTO THE DATA THE TEMPLATE EXPECTS."""
    row   = matrix.get(case["id"], {})
    steps, log_lines, errors = [], [], []
    context, shot_times = "", []

    for text, stamp in case["lineas"]:
        clean = text.strip()
        log_lines.append(f"[{stamp}] {text}" if stamp and clean else text)
        if not clean or _RULE.match(clean) or set(clean) <= set("🖐️ ️"):
            continue
        if clean.startswith(("Stacktrace:", "at ")) or "📝" in clean:
            errors.append(clean)
            continue
        if "SCREENSHOT TAKEN:" in clean:
            path = clean.split("SCREENSHOT TAKEN:", 1)[1].strip()
            name = os.path.splitext(os.path.basename(path))[0]
            if os.path.exists(path):
                mtime = datetime.fromtimestamp(os.path.getmtime(path))
                shot_times.append(mtime)
                steps.append({
                    "numero": len(steps) + 1,
                    "descripcion": "Captura · " + re.sub(r"^[A-Z0-9]+_(?=\d)", "", name).replace("_", " "),
                    "hora": stamp or mtime.strftime("%H:%M:%S"),
                    "archivo": _image_data_uri(path),
                    "estado": "fallo" if re.search(r"FAIL|ERROR", name, re.I) else "info",
                    "pantalla": context,
                })
            continue
        if "👉" in clean:
            context = clean.replace("👉", "").strip()
        kind = _step_kind(clean)
        if kind == "fallo" and "RESULT:" not in clean:
            errors.append(clean)
        if kind and "RESULT:" not in clean:
            steps.append({"numero": len(steps) + 1, "descripcion": clean, "hora": stamp,
                          "archivo": None, "estado": kind, "pantalla": ""})

    if case["resultado"] is None:
        estado, nota = "Error", "EJECUCIÓN INTERRUMPIDA: EL CASO NO IMPRIMIÓ SU LÍNEA 'RESULT'"
    else:
        nota   = case["nota"]
        estado = _case_status(case["resultado"], nota)
        # AN EXCEPTION INSIDE THE CASE (💥 ... CRITICAL ERROR) IS AN EXECUTION ERROR, NOT A DEFECT
        if estado == "Fallido" and any("CRITICAL ERROR" in e.upper() for e in errors):
            estado = "Error"
        if not nota:
            nota = next((e for e in reversed(errors) if "📝" not in e), "") if estado != "Aprobado" else ""
            nota = nota or f"RESULT: {case['resultado']}"

    stamps = [s for _, s in case["lineas"] if s]
    duracion = None
    if len(stamps) >= 2:
        t0, t1 = (datetime.strptime(s, "%H:%M:%S") for s in (stamps[0], stamps[-1]))
        duracion = (t1 - t0).seconds
    elif len(shot_times) >= 2:
        duracion = int((shot_times[-1] - shot_times[0]).total_seconds())

    monto = None
    raw_monto = row.get("monto")
    if raw_monto not in (None, ""):
        try:
            monto = float(str(raw_monto).replace("$", "").replace(",", ""))
        except ValueError:
            pass
    opcion = str(row.get("opcion de pago") or "")

    return {
        "id": case["id"],
        "caso": str(row.get("caso de prueba") or case["titulo"] or case["id"]),
        "modulo": str(row.get("modulo") or module_name),
        "escenario": opcion,
        "tipo_pago": "6 MSI" if "6 MSI" in opcion.upper() else "",
        "monto": monto,
        "tipo": str(row.get("tipo") or ""),
        "prioridad": str(row.get("prioridad") or ""),
        "automatizacion": str(row.get("ejecucion") or ""),
        "precondiciones": str(row.get("precondiciones") or ""),
        "pasos": str(row.get("pasos a seguir") or ""),
        "datos": str(row.get("datos de prueba") or ""),
        "esperado": str(row.get("resultado esperado") or ""),
        "observaciones": str(row.get("observaciones") or ""),
        "descripcion": case["titulo"] if row else "",
        "estado": estado,
        "obtenido": nota,
        "duracion": duracion,
        "error": "\n".join(errors) if estado in ("Fallido", "Error") else "",
        "pasos_evidencia": steps,
        "log": "\n".join(log_lines).strip("\n"),
    }


def generate_html_report(module_name, log_file, timestamp):
    """
    READS THE DUAL-LOGGER TEXT FILE AND GENERATES THE HTML EVIDENCE REPORT
    (TEMPLATE PORTED FROM Automatization-Rompefilas — SEE reporte_html.py).
    FEATURES:
        - RUN SUMMARY: VERDICT, DEVICE, DURATION, COUNT PER STATUS AND PER MODULE.
        - ONE CARD PER CASE ("📊 <ID> RESULT:" LINES) WITH EXPECTED VS OBTAINED,
          STEP-BY-STEP TIMELINE (TIME + SCREENSHOT) AND THE FULL CASE LOG.
        - MATRIX DATA FROM Matrices/*.xlsx WHEN THE CASE ID IS FOUND THERE.
        - SCREENSHOTS EMBEDDED AS BASE64 (SINGLE FILE, NO EXTERNAL IMAGES NEEDED).
    OUTPUT: zip_evidence/{module_name}_REPORT_{timestamp}.html
    """
    import reporte_html

    html_file = f"zip_evidence/{module_name}_REPORT_{timestamp}.html"
    print(f"\n📄 GENERATING HTML REPORT...")

    try:
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        times    = _LINE_TIMES.get(log_file, [])
        log_text = "".join(lines)
        matrix   = _load_matrices()

        cases = [_build_case(c, matrix, module_name) for c in _split_cases(lines, times)]
        if not cases:
            # SUITE WITHOUT "RESULT:" LINES: THE WHOLE RUN IS ONE CARD
            fails = sum(1 for l in lines if _classify_log_line(l) == "fail")
            whole = {"id": module_name, "titulo": "Ejecución completa", "nota": "",
                     "lineas": [(l.rstrip("\n"), times[i] if i < len(times) else "") for i, l in enumerate(lines)],
                     "resultado": "FAIL" if fails else "SUCCESS"}
            cases = [_build_case(whole, matrix, module_name)]

        inicio = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
        fin    = datetime.now()
        logo   = _image_data_uri(LOGO_PATH) if os.path.exists(LOGO_PATH) else ""

        datos = {
            "modulo": module_name,
            "ejecucion": timestamp,
            "inicio": inicio.strftime("%Y-%m-%d %H:%M:%S"),
            "fin_completo": fin.strftime("%Y-%m-%d %H:%M:%S"),
            "duracion_total": int((fin - inicio).total_seconds()) if times else None,
            "dispositivo": _device_info(log_text),
            "interactivo": "🖐️" in log_text,
            "log_archivo": os.path.basename(log_file),
            "logo": logo,
            "casos": cases,
        }
        reporte_html.generar_reporte(datos, html_file)

        resumen = {}
        for c in cases:
            resumen[c["estado"]] = resumen.get(c["estado"], 0) + 1
        print(f"✅ HTML REPORT GENERATED: {html_file}")
        print(f"   📊 {len(cases)} CASES — " + " · ".join(f"{k}: {v}" for k, v in resumen.items()))
        print("=" * 70 + "\n")
        return html_file

    except Exception as e:
        print(f"❌ ERROR GENERATING HTML REPORT: {e}")
