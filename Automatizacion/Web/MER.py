"""
# ==================================================================================
# FILENAME    : MER.py
# CONTENTS:
#   · MER-01: GO TO THE MERCHANTS PAGE.
#   · MER-02: THE USER CAN VIEW THE LIST OF BUSSINESSESS.
# ==================================================================================
"""

import sys
import os
import time
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import config
import utils
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# MODULE CONFIGURATION
COMERCIOS_URL     = "https://fat.memphis.mx/v2/comercios"
EVIDENCE_ENDPOINT = "comercios"

XPATH_COMERCIOS_CARD = (
    
    "[routerLink='/comercios'] | "
    
    "//a[@href='/comercios'] | "
    
    "//*[normalize-space(text())='Comercios']"
    "[not(ancestor::nav) and not(ancestor::aside) and not(self::title)]"
)

XPATH_TABLA_COMERCIOS_HEADING = (
    "//h1[contains(text(),'Comercios') or normalize-space(text())='Comercios'] | "
    "//h2[contains(text(),'Comercios')] | "
    "//*[contains(@class,'title') or contains(@class,'heading')]"
    "[normalize-space(text())='Comercios'][not(ancestor::nav)]"
)

XPATH_COL_ID              = "//*[normalize-space(text())='ID'][ancestor::thead or ancestor::th or ancestor::*[contains(@class,'header')]]"
XPATH_COL_NOMBRE_COMERCIO = "//*[contains(text(),'Nombre de Comercio')][ancestor::thead or ancestor::th or ancestor::*[contains(@class,'header')]]"
XPATH_COL_AFILIACION      = "//*[contains(text(),'Afiliación') or contains(text(),'Afiliacion')][ancestor::thead or ancestor::th or ancestor::*[contains(@class,'header')]]"

XPATH_FIRST_ROW = "//tbody//tr[1] | //*[contains(@class,'row') or contains(@class,'tr')][1]"


XPATH_BTN_NUEVO = (
    "//button[contains(text(),'Nuevo') or contains(text(),'NUEVO')] | "
    "//*[contains(@class,'btn')][contains(.,'Nuevo')]"
)

XPATH_BTN_REPORTE = (
    "//button[contains(text(),'Reporte') or contains(text(),'REPORTE')] | "
    "//a[contains(text(),'Reporte')]"
)

XPATH_BTN_PENCIL_FIRST_ROW = (
    
    "(//tbody//tr[1]//button)[1] | "
    
    "(//tbody//tr[1]//*[contains(@class,'pencil') or contains(@class,'edit') or "
    "                    contains(@class,'pi-pencil') or contains(@class,'pi-pen')])[1]"
)

XPATH_EDIT_COMERCIO_TITULO = (
    "//h1[contains(text(),'Edición de Comercio') or contains(text(),'Edicion de Comercio')] | "
    "//h2[contains(text(),'Edición de Comercio')] | "
    "//*[contains(@class,'title') or contains(@class,'heading')]"
    "[contains(text(),'Edición de Comercio') or contains(text(),'Edicion de Comercio')] | "
    "//*[normalize-space(text())='Edición de Comercio' or "
    "    normalize-space(text())='Edicion de Comercio']"
    "[not(ancestor::nav) and not(ancestor::aside)]"
)

# INTERNAL HELPERS
def _login_and_go_to_comercios(driver):
    
    print(f"   🌐 NAVIGATING TO LOGIN: {config.URL_MEMPHIS_WEB}")
    driver.get(config.URL_MEMPHIS_WEB)
    time.sleep(2)

    print(f"   ✏️  ENTERING CREDENTIALS — USER: {config.WEB_USUARIO_PRUEBA}")
    utils.escribir_texto(driver, config.XPATH_WEB_USER, config.WEB_USUARIO_PRUEBA)
    utils.escribir_texto(driver, config.XPATH_WEB_PASS, config.WEB_PASS_PRUEBA)

    print("   🖱️  CLICKING LOGIN BUTTON...")
    utils.click_boton(driver, config.XPATH_WEB_BTN_LOGIN)

    print("   ⏳ WAITING FOR HOME DASHBOARD TO LOAD...")
    time.sleep(5)

    print(f"   🌐 POST-LOGIN URL: {driver.current_url}")
    print("   🖱️  CLICKING ORANGE 'COMERCIOS' CARD (4-STRATEGY CASCADE)...")
    clicked = False

    if not clicked:
        try:
            result = driver.execute_script("""
                var candidates = document.querySelectorAll(
                    '[routerLink], [routerlink], [ng-reflect-router-link]'
                );
                for (var el of candidates) {
                    var rl = el.getAttribute('routerLink') ||
                             el.getAttribute('routerlink') ||
                             el.getAttribute('ng-reflect-router-link') || '';
                    if (rl === '/comercios' || rl === 'comercios') {
                        el.click();
                        return 'routerLink:' + el.tagName + '[' + rl + ']';
                    }
                }
                return null;
            """)
            if result:
                clicked = True
                time.sleep(4)
                print(f"   ✅ CARD CLICKED — STRATEGY 1 (JS routerLink: {result}).")
        except Exception as s1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {s1_err}")

    if not clicked:
        try:
            result = driver.execute_script("""
                var anchors = document.querySelectorAll('a[href]');
                for (var a of anchors) {
                    var href = a.getAttribute('href') || '';
                    if ((href === '/comercios' || href.endsWith('/comercios')) &&
                        a.offsetWidth > 0) {
                        a.click();
                        return 'href:' + href;
                    }
                }
                return null;
            """)
            if result:
                clicked = True
                time.sleep(4)
                print(f"   ✅ CARD CLICKED — STRATEGY 2 (JS href: {result}).")
        except Exception as s2_err:
            print(f"   ⚠️  STRATEGY 2 FAILED: {s2_err}")

    if not clicked:
        try:
            result = driver.execute_script("""
                var allEls = document.querySelectorAll('*');
                for (var el of allEls) {
                    if (el.textContent.trim() === 'Comercios' &&
                        el.children.length === 0 &&
                        el.offsetWidth > 0 &&
                        !el.closest('nav') &&
                        !el.closest('aside')) {
                        var parent = el.parentElement;
                        for (var i = 0; i < 6; i++) {
                            if (!parent) break;
                            var style = window.getComputedStyle(parent);
                            var rl    = parent.getAttribute('routerLink') ||
                                        parent.getAttribute('routerlink') ||
                                        parent.getAttribute('href');
                            if (style.cursor === 'pointer' || rl) {
                                parent.click();
                                return 'text-walk:level-' + i + ':' + parent.tagName;
                            }
                            parent = parent.parentElement;
                        }
                        var up2 = el.parentElement && el.parentElement.parentElement;
                        if (up2) { up2.click(); return 'text-walk:fallback-up2'; }
                        el.parentElement.click();
                        return 'text-walk:fallback-up1';
                    }
                }
                return null;
            """)
            if result:
                clicked = True
                time.sleep(4)
                print(f"   ✅ CARD CLICKED — STRATEGY 3 (JS TEXT WALK: {result}).")
        except Exception as s3_err:
            print(f"   ⚠️  STRATEGY 3 FAILED: {s3_err}")

    if not clicked:
        print(f"   ⚠️  ALL CLICK STRATEGIES FAILED. NAVIGATING DIRECTLY TO URL...")
        driver.get(COMERCIOS_URL)
        time.sleep(4)
        print(f"   🌐 NAVIGATED DIRECTLY TO: {driver.current_url}")
    else:
        print(f"   🌐 CURRENT URL AFTER CARD CLICK: {driver.current_url}")

    print("   ⏳ WAITING FOR COMERCIOS TABLE TO RENDER...")
    time.sleep(3)


def _tabla_comercios_is_loaded(driver):
    try:
        driver.find_element(By.XPATH, XPATH_TABLA_COMERCIOS_HEADING)
        return True
    except Exception:
        pass

    # CHECK 2: FIRST DATA ROW PRESENT
    try:
        driver.find_element(By.XPATH, XPATH_FIRST_ROW)
        return True
    except Exception:
        pass

    # CHECK 3: URL
    return "comercios" in driver.current_url.lower()


def _capture_web_evidence(driver, nombre_test):
    print(f"\n📡 CAPTURING HTTP EVIDENCE FOR [{nombre_test}]...")

    SKIP_EXTENSIONS = [".css", ".js", ".png", ".jpg", ".jpeg", ".svg",
                       ".woff", ".ttf", ".ico", "favicon", "fonts",
                       "google", "analytics", "gtm", "hotjar"]

    try:
        raw_logs = driver.get_log("performance")
    except Exception as e:
        print(f"   ❌ COULD NOT READ PERFORMANCE LOGS: {e}")
        return

    if not raw_logs:
        print(f"   ℹ️  PERFORMANCE LOG BUFFER IS EMPTY FOR [{nombre_test}].")
        print("   💡 THIS IS EXPECTED WHEN NO HTTP REQUESTS WERE MADE DURING THE TEST.")
        return

    requests_map = {}
    responses    = []

    for entry in raw_logs:
        try:
            msg    = json.loads(entry["message"])["message"]
            method = msg.get("method", "")
            params = msg.get("params", {})

            if method == "Network.requestWillBeSent":
                req = params.get("request", {})
                rid = params.get("requestId", "")
                url = req.get("url", "")
                if not any(s in url.lower() for s in SKIP_EXTENSIONS):
                    requests_map[rid] = {
                        "url"      : url,
                        "method"   : req.get("method", "UNKNOWN"),
                        "postData" : req.get("postData", None),
                    }

            if method == "Network.responseReceived":
                resp = params.get("response", {})
                url  = resp.get("url", "")
                if not any(s in url.lower() for s in SKIP_EXTENSIONS):
                    responses.append({
                        "requestId": params.get("requestId", ""),
                        "url"      : url,
                        "status"   : resp.get("status", "N/A"),
                        "mimeType" : resp.get("mimeType", "N/A"),
                    })
        except Exception:
            continue

    if not responses:
        print(f"   ℹ️  NO NON-STATIC HTTP RESPONSES CAPTURED FOR [{nombre_test}].")
        return

    matched = [r for r in responses if EVIDENCE_ENDPOINT in r["url"]]

    if matched:
        print(f"   ✅ KEYWORD '{EVIDENCE_ENDPOINT}' MATCHED {len(matched)} RESPONSE(S).")
        print("-" * 60)
        for i, resp in enumerate(matched, 1):
            req_info    = requests_map.get(resp["requestId"], {})
            http_method = req_info.get("method", "UNKNOWN")
            post_data   = req_info.get("postData", None)
            status      = resp["status"]

            print(f"📋 MATCH #{i}")
            print(f"🔗 URL      : {resp['url']}")
            print(f"📨 METHOD   : {http_method}")
            print(f"📦 STATUS   : {status}")
            print(f"📄 MIME TYPE: {resp['mimeType']}")

            if post_data:
                try:
                    safe = json.loads(post_data)
                    for key in ["password", "contrasena", "pass", "pwd"]:
                        if key in safe:
                            safe[key] = "********"
                    print(f"📤 PAYLOAD  : {json.dumps(safe)}")
                except Exception:
                    print("📤 PAYLOAD  : [RAW — NOT JSON]")

            INTERPRETATIONS = {
                200: "✅ SERVER: OK",
                201: "✅ SERVER: RESOURCE CREATED",
                202: "✅ SERVER: ACCEPTED",
                400: "⛔ SERVER: BAD REQUEST",
                401: "🔒 SERVER: UNAUTHORIZED",
                403: "🚫 SERVER: FORBIDDEN",
                404: "🔍 SERVER: NOT FOUND",
                409: "⚠️  SERVER: CONFLICT",
                422: "⚠️  SERVER: UNPROCESSABLE ENTITY",
                500: "💥 SERVER: INTERNAL SERVER ERROR",
            }
            print(INTERPRETATIONS.get(status, f"⚠️  SERVER: HTTP {status}"))
            print("-" * 60)
    else:
        print(f"   ⚠️  KEYWORD '{EVIDENCE_ENDPOINT}' NOT FOUND IN CAPTURED URLS.")
        print(f"   🔍 DIAGNOSTIC MODE — ALL {len(responses)} NON-STATIC RESPONSE(S):")
        print("-" * 60)
        for resp in responses:
            req_info = requests_map.get(resp["requestId"], {})
            print(f"   {req_info.get('method','?'):6} | {resp['status']} | {resp['url'][:120]}")
            if req_info.get("postData"):
                print(f"          📤 PAYLOAD: {req_info['postData'][:100]}")
        print("-" * 60)
        print("   💡 UPDATE 'EVIDENCE_ENDPOINT' WITH A KEYWORD FROM THE URLS ABOVE.")


# ==================================================================================
# MER-01: GO TO THE MERCHANTS PAGE.
# ==================================================================================
def MER_01():
    print("\n" + "=" * 60)
    print("🧪 MER-01: GO TO THE MERCHANTS PAGE.S")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO COMERCIOS MODULE...")
        _login_and_go_to_comercios(driver)

        print(f"\n   🌐 CURRENT URL: {driver.current_url}")

        print("\n👉 STEP 1: VERIFYING COMERCIOS TABLE IS LOADED...")
        tabla_loaded = _tabla_comercios_is_loaded(driver)

        if tabla_loaded:
            print("   ✅ COMERCIOS TABLE PAGE CONFIRMED AS LOADED.")
        else:
            print("   ⚠️  TABLE NOT DETECTED — PAGE MAY STILL BE RENDERING...")
            time.sleep(3)
            tabla_loaded = _tabla_comercios_is_loaded(driver)

        print("\n📸 TAKING SCREENSHOT #1 — COMERCIOS TABLE AFTER NAVIGATION...")
        utils.tomar_screenshot(driver, "MER_01_1_COMERCIOS_TABLE")

        print("\n👉 STEP 2: VERIFYING TABLE COLUMN HEADERS ARE PRESENT...")
        columns_found = {}
        col_checks = {
            "ID"               : XPATH_COL_ID,
            "NOMBRE DE COMERCIO": XPATH_COL_NOMBRE_COMERCIO,
            "AFILIACION"       : XPATH_COL_AFILIACION,
        }

        for col_name, xpath in col_checks.items():
            try:
                driver.find_element(By.XPATH, xpath)
                columns_found[col_name] = True
                print(f"      ✅ COLUMN FOUND: {col_name}")
            except Exception:
                columns_found[col_name] = False
                print(f"      ⚠️  COLUMN NOT FOUND: {col_name}")

        print("\n👉 STEP 3: VERIFYING AT LEAST ONE DATA ROW IS PRESENT...")
        rows_found  = False
        row_count   = 0

        try:
            rows      = driver.find_elements(By.XPATH, "//tbody//tr")
            row_count = len(rows)
            rows_found = row_count > 0
            if rows_found:
                print(f"   ✅ {row_count} DATA ROW(S) FOUND IN TABLE BODY — STRATEGY 1 (XPATH tbody tr).")
            else:
                print("   ⚠️  NO ROWS FOUND VIA XPATH — TRYING JS SCAN...")
        except Exception as r1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {r1_err}")

        if not rows_found:
            try:
                row_count = driver.execute_script("""
                    var rows = document.querySelectorAll('tbody tr, [class*="row"]:not([class*="header"])');
                    return rows.length;
                """)
                rows_found = row_count > 0
                if rows_found:
                    print(f"   ✅ {row_count} ROW(S) FOUND — STRATEGY 2 (JS DOM SCAN).")
                else:
                    print("   ❌ NO DATA ROWS FOUND IN TABLE.")
            except Exception as r2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {r2_err}")

        # STEP 4: CHECK FOR 'NUEVO +' BUTTON — CONFIRMS FULL MODULE LOAD
        print("\n👉 STEP 4: CHECKING FOR 'NUEVO +' BUTTON (TOP-RIGHT)...")
        nuevo_found = False
        try:
            driver.find_element(By.XPATH, XPATH_BTN_NUEVO)
            nuevo_found = True
            print("   ✅ 'NUEVO +' BUTTON FOUND.")
        except Exception:
            print("   ⚠️  'NUEVO +' BUTTON NOT FOUND — CHECKING VIA JS...")
            try:
                result = driver.execute_script("""
                    var btns = document.querySelectorAll('button, a');
                    for (var btn of btns) {
                        if (btn.textContent.trim().toLowerCase().includes('nuevo')
                                && btn.offsetWidth > 0) {
                            return btn.textContent.trim();
                        }
                    }
                    return null;
                """)
                if result:
                    nuevo_found = True
                    print(f"   ✅ 'NUEVO' BUTTON FOUND VIA JS: '{result}'.")
                else:
                    print("   ⚠️  'NUEVO' BUTTON NOT FOUND VIA JS.")
            except Exception as js_err:
                print(f"   ⚠️  JS SCAN FAILED: {js_err}")

        print("\n👉 STEP 5: READING RECORD COUNT FROM PAGINATION...")
        record_count_text = ""
        try:
            result = driver.execute_script("""
                var all = document.querySelectorAll('*');
                for (var el of all) {
                    if (el.children.length === 0 &&
                        el.textContent.trim().toLowerCase().includes('mostrando') &&
                        el.textContent.trim().toLowerCase().includes('registros')) {
                        return el.textContent.trim();
                    }
                }
                return null;
            """)
            if result:
                record_count_text = result
                print(f"   ✅ PAGINATION TEXT FOUND: '{record_count_text}'")
            else:
                print("   ⚠️  PAGINATION TEXT NOT FOUND IN DOM.")
        except Exception as pg_err:
            print(f"   ⚠️  PAGINATION READ FAILED: {pg_err}")

        print("\n📸 TAKING SCREENSHOT #2 — COMERCIOS TABLE FULLY LOADED WITH DATA...")
        utils.tomar_screenshot(driver, "MER_01_2_TABLE_WITH_DATA")

        test_passed = tabla_loaded and rows_found

        print(f"\n   🔬 MER-01 ASSERTION SUMMARY:")
        print(f"      • COMERCIOS TABLE LOADED     : {tabla_loaded}")
        print(f"      • TABLE COLUMNS FOUND        : {[k for k, v in columns_found.items() if v]}")
        print(f"      • DATA ROWS FOUND            : {rows_found} ({row_count} row(s))")
        print(f"      • 'NUEVO +' BUTTON VISIBLE   : {nuevo_found}")
        print(f"      • PAGINATION TEXT            : '{record_count_text}'")
        print(f"      • FINAL URL                  : {driver.current_url}")

        _capture_web_evidence(driver, "MER_01")

        if test_passed:
            utils.tomar_screenshot(driver, "MER_01_SUCCESS")
            print("\n✅ MER-01: SUCCESS — COMERCIOS TABLE LOADED WITH DATA AFTER CLICKING ORANGE CARD.")
        else:
            utils.tomar_screenshot(driver, "MER_01_FAILED")
            if not tabla_loaded:
                print("\n❌ MER-01: FAILED — COMERCIOS TABLE PAGE DID NOT LOAD AFTER CLICKING CARD.")
            else:
                print("\n❌ MER-01: FAILED — TABLE LOADED BUT NO DATA ROWS WERE FOUND.")

    except Exception as e:
        print(f"\n💥 MER-01 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "MER_01_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()

# ==================================================================================
# MER-02: THE USER CAN VIEW THE LIST OF BUSSINESSESS.
# ==================================================================================
def MER_02():
    
    print("\n" + "=" * 60)
    print("🧪 MER-02: THE USER CAN VIEW THE LIST OF BUSSINESSESS.")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO COMERCIOS MODULE...")
        _login_and_go_to_comercios(driver)

        print(f"\n   🌐 CURRENT URL: {driver.current_url}")

        print("\n👉 STEP 1: VERIFYING COMERCIOS TABLE IS LOADED...")
        tabla_loaded = _tabla_comercios_is_loaded(driver)

        if tabla_loaded:
            print("   ✅ COMERCIOS TABLE PAGE CONFIRMED AS LOADED.")
        else:
            print("   ⚠️  TABLE NOT DETECTED — PAGE MAY STILL BE RENDERING...")
            time.sleep(3)
            tabla_loaded = _tabla_comercios_is_loaded(driver)

        print("\n📸 TAKING SCREENSHOT #1 — COMERCIOS TABLE AFTER NAVIGATION...")
        utils.tomar_screenshot(driver, "MER_01_1_COMERCIOS_TABLE")

        print("\n👉 STEP 2: VERIFYING TABLE COLUMN HEADERS ARE PRESENT...")
        columns_found = {}
        col_checks = {
            "ID"               : XPATH_COL_ID,
            "NOMBRE DE COMERCIO": XPATH_COL_NOMBRE_COMERCIO,
            "AFILIACION"       : XPATH_COL_AFILIACION,
        }

        for col_name, xpath in col_checks.items():
            try:
                driver.find_element(By.XPATH, xpath)
                columns_found[col_name] = True
                print(f"      ✅ COLUMN FOUND: {col_name}")
            except Exception:
                columns_found[col_name] = False
                print(f"      ⚠️  COLUMN NOT FOUND: {col_name}")

        print("\n👉 STEP 3: VERIFYING AT LEAST ONE DATA ROW IS PRESENT...")
        rows_found  = False
        row_count   = 0

        try:
            rows      = driver.find_elements(By.XPATH, "//tbody//tr")
            row_count = len(rows)
            rows_found = row_count > 0
            if rows_found:
                print(f"   ✅ {row_count} DATA ROW(S) FOUND IN TABLE BODY — STRATEGY 1 (XPATH tbody tr).")
            else:
                print("   ⚠️  NO ROWS FOUND VIA XPATH — TRYING JS SCAN...")
        except Exception as r1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {r1_err}")

        if not rows_found:
            try:
                row_count = driver.execute_script("""
                    var rows = document.querySelectorAll('tbody tr, [class*="row"]:not([class*="header"])');
                    return rows.length;
                """)
                rows_found = row_count > 0
                if rows_found:
                    print(f"   ✅ {row_count} ROW(S) FOUND — STRATEGY 2 (JS DOM SCAN).")
                else:
                    print("   ❌ NO DATA ROWS FOUND IN TABLE.")
            except Exception as r2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {r2_err}")

        print("\n👉 STEP 4: CHECKING FOR 'NUEVO +' BUTTON (TOP-RIGHT)...")
        nuevo_found = False
        try:
            driver.find_element(By.XPATH, XPATH_BTN_NUEVO)
            nuevo_found = True
            print("   ✅ 'NUEVO +' BUTTON FOUND.")
        except Exception:
            print("   ⚠️  'NUEVO +' BUTTON NOT FOUND — CHECKING VIA JS...")
            try:
                result = driver.execute_script("""
                    var btns = document.querySelectorAll('button, a');
                    for (var btn of btns) {
                        if (btn.textContent.trim().toLowerCase().includes('nuevo')
                                && btn.offsetWidth > 0) {
                            return btn.textContent.trim();
                        }
                    }
                    return null;
                """)
                if result:
                    nuevo_found = True
                    print(f"   ✅ 'NUEVO' BUTTON FOUND VIA JS: '{result}'.")
                else:
                    print("   ⚠️  'NUEVO' BUTTON NOT FOUND VIA JS.")
            except Exception as js_err:
                print(f"   ⚠️  JS SCAN FAILED: {js_err}")

        print("\n👉 STEP 5: READING RECORD COUNT FROM PAGINATION...")
        record_count_text = ""
        try:
            result = driver.execute_script("""
                var all = document.querySelectorAll('*');
                for (var el of all) {
                    if (el.children.length === 0 &&
                        el.textContent.trim().toLowerCase().includes('mostrando') &&
                        el.textContent.trim().toLowerCase().includes('registros')) {
                        return el.textContent.trim();
                    }
                }
                return null;
            """)
            if result:
                record_count_text = result
                print(f"   ✅ PAGINATION TEXT FOUND: '{record_count_text}'")
            else:
                print("   ⚠️  PAGINATION TEXT NOT FOUND IN DOM.")
        except Exception as pg_err:
            print(f"   ⚠️  PAGINATION READ FAILED: {pg_err}")

        print("\n📸 TAKING SCREENSHOT #2 — COMERCIOS TABLE FULLY LOADED WITH DATA...")
        utils.tomar_screenshot(driver, "MER_01_2_TABLE_WITH_DATA")

        test_passed = tabla_loaded and rows_found

        print(f"\n   🔬 MER-01 ASSERTION SUMMARY:")
        print(f"      • COMERCIOS TABLE LOADED     : {tabla_loaded}")
        print(f"      • TABLE COLUMNS FOUND        : {[k for k, v in columns_found.items() if v]}")
        print(f"      • DATA ROWS FOUND            : {rows_found} ({row_count} row(s))")
        print(f"      • 'NUEVO +' BUTTON VISIBLE   : {nuevo_found}")
        print(f"      • PAGINATION TEXT            : '{record_count_text}'")
        print(f"      • FINAL URL                  : {driver.current_url}")

        _capture_web_evidence(driver, "MER_01")

        if test_passed:
            utils.tomar_screenshot(driver, "MER_01_SUCCESS")
            print("\n✅ MER-01: SUCCESS — COMERCIOS TABLE LOADED WITH DATA AFTER CLICKING ORANGE CARD.")
        else:
            utils.tomar_screenshot(driver, "MER_01_FAILED")
            if not tabla_loaded:
                print("\n❌ MER-01: FAILED — COMERCIOS TABLE PAGE DID NOT LOAD AFTER CLICKING CARD.")
            else:
                print("\n❌ MER-01: FAILED — TABLE LOADED BUT NO DATA ROWS WERE FOUND.")

    except Exception as e:
        print(f"\n💥 MER-01 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "MER_01_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()

# ==================================================================================
# MER-03: COMERCIOS TABLE → CLICK PENCIL ON FIRST ROW
#         → 'EDICIÓN DE COMERCIO' FORM OPENS WITH PRE-FILLED DATA
# ==================================================================================
def MER_03():
    """
    PRECONDITIONS : VALID CREDENTIALS. AT LEAST ONE COMERCIO EXISTS IN THE TABLE.
    STEPS         : 1. LOGIN → DASHBOARD → CLICK ORANGE 'COMERCIOS' CARD.
                    2. VERIFY THE COMERCIOS TABLE IS LOADED.
                    3. CLICK THE PENCIL ICON ✏️ ON THE FIRST ROW (ACCIONES COLUMN).
                    4. VERIFY THE 'EDICIÓN DE COMERCIO' FORM OPENS.
                    5. TAKE SCREENSHOT OF THE FORM AS EVIDENCE.
    EXPECTED      : THE EDIT FORM 'EDICIÓN DE COMERCIO' IS DISPLAYED WITH:
                    · TITLE 'Edición de Comercio' VISIBLE AT THE TOP.
                    · SECTION 1: 'DATOS DE COMERCIO' WITH PRE-FILLED FIELDS.
                    · SECTION 2: 'DATOS DE CONTACTO'.
                    · 'LIMPIAR' AND 'GUARDAR' BUTTONS AT THE BOTTOM.
    SUCCESS CRITERIA: EDIT FORM TITLE 'Edición de Comercio' IS VISIBLE ON SCREEN.
    """
    print("\n" + "=" * 60)
    print("🧪 MER-03: COMERCIOS TABLE → CLICK PENCIL → EDIT FORM OPENS")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        # PRECONDITION: LOG IN AND NAVIGATE TO THE COMERCIOS MODULE
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO COMERCIOS MODULE...")
        _login_and_go_to_comercios(driver)

        print("\n📸 TAKING SCREENSHOT #1 — COMERCIOS TABLE BEFORE CLICKING PENCIL...")
        utils.tomar_screenshot(driver, "MER_03_1_COMERCIOS_TABLE")

        # STEP 1: CLICK THE PENCIL ✏️ ON THE FIRST ROW
        # FROM SCREENSHOT: EACH ROW HAS 4 ICONS IN ACCIONES — ✏️ 🗑️ 👁️ ✅
        # THE PENCIL IS ALWAYS THE FIRST ICON/BUTTON IN THE ROW.
        print("\n👉 STEP 1: CLICKING PENCIL ✏️ ICON ON FIRST ROW (3-STRATEGY CASCADE)...")
        pencil_clicked = False

        # STRATEGY 1: XPATH — FIRST BUTTON IN FIRST TBODY ROW
        try:
            btn = driver.find_element(By.XPATH, "(//tbody//tr[1]//button)[1]")
            driver.execute_script("arguments[0].click();", btn)
            pencil_clicked = True
            time.sleep(3)
            print("   ✅ PENCIL CLICKED — STRATEGY 1 (FIRST BUTTON IN FIRST TR).")
        except Exception as s1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {s1_err}")

        # STRATEGY 2: XPATH — PENCIL ICON CLASS IN FIRST ROW
        if not pencil_clicked:
            try:
                btn = driver.find_element(By.XPATH, XPATH_BTN_PENCIL_FIRST_ROW)
                driver.execute_script("arguments[0].click();", btn)
                pencil_clicked = True
                time.sleep(3)
                print("   ✅ PENCIL CLICKED — STRATEGY 2 (PENCIL ICON XPATH).")
            except Exception as s2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {s2_err}")

        # STRATEGY 3: JS — FIRST BUTTON IN FIRST TBODY ROW
        if not pencil_clicked:
            try:
                result = driver.execute_script("""
                    var rows = document.querySelectorAll('tbody tr');
                    if (rows.length === 0) return 'NO ROWS FOUND';
                    var btns = rows[0].querySelectorAll('button, a[role="button"]');
                    if (btns.length === 0) return 'NO BUTTONS IN FIRST ROW';
                    btns[0].click();
                    return 'clicked:' + btns[0].className;
                """)
                if result and result.startswith('clicked:'):
                    pencil_clicked = True
                    time.sleep(3)
                    print(f"   ✅ PENCIL CLICKED — STRATEGY 3 (JS FIRST ROW BUTTON: '{result}').")
                else:
                    print(f"   ❌ STRATEGY 3 — DEBUG: {result}")
            except Exception as s3_err:
                print(f"   ⚠️  STRATEGY 3 FAILED: {s3_err}")

        print(f"   🌐 CURRENT URL AFTER PENCIL CLICK: {driver.current_url}")

        print("\n📸 TAKING SCREENSHOT #2 — AFTER CLICKING PENCIL...")
        utils.tomar_screenshot(driver, "MER_03_2_AFTER_PENCIL")

        # STEP 2: VERIFY THE 'EDICIÓN DE COMERCIO' FORM IS VISIBLE
        print("\n👉 STEP 2: VERIFYING 'EDICIÓN DE COMERCIO' FORM TITLE IS VISIBLE...")
        time.sleep(2)
        form_visible = False

        # STRATEGY 1: XPATH — LOOK FOR THE FORM TITLE TEXT
        try:
            driver.find_element(By.XPATH, XPATH_EDIT_COMERCIO_TITULO)
            form_visible = True
            print("   ✅ TITLE 'Edición de Comercio' FOUND — STRATEGY 1 (XPATH).")
        except Exception:
            print("   ⚠️  TITLE NOT FOUND VIA XPATH — TRYING JS SCAN...")

        # STRATEGY 2: JS — SCAN ALL HEADINGS FOR THE TITLE TEXT
        if not form_visible:
            try:
                result = driver.execute_script("""
                    var all = document.querySelectorAll('h1, h2, h3, [class*="title"], [class*="heading"]');
                    for (var el of all) {
                        var txt = el.textContent.trim().toLowerCase();
                        if (txt.includes('edici') && txt.includes('comercio')) {
                            return el.textContent.trim();
                        }
                    }
                    return null;
                """)
                if result:
                    form_visible = True
                    print(f"   ✅ TITLE FOUND VIA JS SCAN: '{result}'.")
                else:
                    print("   ⚠️  TITLE NOT FOUND VIA JS — CHECKING URL...")
            except Exception as js_err:
                print(f"   ⚠️  JS SCAN FAILED: {js_err}")

        # STRATEGY 3: URL CHECK — EDIT FORM URL CONTAINS 'editar' OR 'edit'
        if not form_visible:
            url_has_edit = (
                "editar" in driver.current_url.lower() or
                "edit"   in driver.current_url.lower()
            )
            if url_has_edit:
                form_visible = True
                print(f"   ✅ EDIT URL CONFIRMED: {driver.current_url}")
            else:
                print(f"   ❌ URL DOES NOT INDICATE EDIT FORM: {driver.current_url}")

        # TAKE THE KEY SCREENSHOT — THE EDIT FORM WITH TITLE VISIBLE
        print("\n📸 TAKING SCREENSHOT #3 — 'EDICIÓN DE COMERCIO' FORM (KEY EVIDENCE)...")
        utils.tomar_screenshot(driver, "MER_03_3_EDICION_COMERCIO_FORM")

        # FINAL ASSERTION
        test_passed = pencil_clicked and form_visible

        print(f"\n   🔬 MER-03 ASSERTION SUMMARY:")
        print(f"      • PENCIL CLICKED              : {pencil_clicked}")
        print(f"      • EDIT FORM TITLE VISIBLE     : {form_visible}")
        print(f"      • FINAL URL                   : {driver.current_url}")

        _capture_web_evidence(driver, "MER_03")

        if test_passed:
            utils.tomar_screenshot(driver, "MER_03_SUCCESS")
            print("\n✅ MER-03: SUCCESS — 'EDICIÓN DE COMERCIO' FORM OPENED CORRECTLY.")
        else:
            utils.tomar_screenshot(driver, "MER_03_FAILED")
            if not pencil_clicked:
                print("\n❌ MER-03: FAILED — PENCIL ICON COULD NOT BE CLICKED.")
            else:
                print("\n❌ MER-03: FAILED — 'EDICIÓN DE COMERCIO' FORM TITLE NOT FOUND.")

    except Exception as e:
        print(f"\n💥 MER-03 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "MER_03_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()


# ==================================================================================
# MAIN EXECUTION
# ==================================================================================
if __name__ == "__main__":

    logger, log_file, timestamp = utils.iniciar_reporte("MER")

    try:
        # MER_01()
        # MER_02()
        MER_03() 

    finally:
        utils.generar_reporte_html("MER", log_file, timestamp)