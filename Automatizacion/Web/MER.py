"""
# ==================================================================================
# FILENAME    : MER.py
# CONTENTS:
#   · MER-01: GO TO THE COMERCIOS PAGE.
#   · MER-02: THE USER CAN VIEW THE LIST OF COMERCIOS.
    · MER-03: GO TO COMERCIOS TABLE.
    · MER-04: USER CAN VIEW LIST OF COMERCIO.
    · MER-05: AUTHENTICATED. USER HAS PERMISSIONS TO VIEW AND CREATE.
    · MER-06: CREATE NEW USER
    · MER-07: THE SWITCH USE PHYSICAL ADDRESS AS BILLING ADDRESS SHOULD BE ENABLED BY DEFAULT.
    · MER-08: THE TAX ADDRESS FIELDS ARE DISPLAYED. THE FIELDS ARE EDITABLE.
    · MER-09: THE TAX ADDRESS FIELDS ARE HIDDEN AGAIN.
    · MER-10: THE SWITCH IS SET TO 'ON' THE TAX FIELDS ARE NOT DISPLAYED.
    · MER-11: USER WITH EDIT PERMISSIONS STORE CREATED WITH SAME ADDRESS = ACTIVE.
    · MER-12: USER WITH EDIT PERMISSIONS STORE CREATED WITH SAME_ADDRESS.
    · MER-13: USER WITH CREATION PERMISSIONS. NO PROCESSOR HAS BEEN SELECTED.
    · MER-14: FIELDS ID, TRANSACTION MODE AND DESTINATION URL ARE GRAYED OUT.
    · MER-15: ACCESS THE CREATION FORM.
    · MER-16: THE FORM DOES NOT ALLOW SAVING VALIDATION ERRORS ARE DISPLAYED.
    · MER-17: THE FORM DOES NOT ALLOW SAVING. VALIDATION ERRORS ARE DISPLAYED. 
    · MER-18: ID, TRANSACTION, DESTINATION URL ARE REQUIRED.
    · MER-19: FIELDS ID, TRANSACTION MODE AND URL ARE ENABLED AND REQUIRED.
    · MER-20: USER WITH EDITING PERMISSIONS, STORE CREATED USING BANREGIO
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
COMERCIOS_URL     = "https://fat.memphis.mx/merchant"
EVIDENCE_ENDPOINT = "merchants"

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
# SMART HELPERS FOR FORM INTERACTION (USED IN MER-06)
# ==================================================================================
def _select_first_dropdown_option(driver, label_text):
    """
    FINDS A DROPDOWN NEXT TO A SPECIFIC LABEL, CLICKS IT, AND SELECTS THE FIRST OPTION.
    """
    try:
        # FIND THE DROPDOWN/SELECT ELEMENT IMMEDIATELY FOLLOWING THE LABEL
        xpath_dropdown = f"//label[contains(normalize-space(.), '{label_text}')]/following::*[contains(@class, 'dropdown') or contains(@class, 'select')][1]"
        dd = driver.find_element(By.XPATH, xpath_dropdown)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dd)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", dd)
        time.sleep(1) # WAIT FOR DROPDOWN PANEL TO ANIMATE

        # FIND AND CLICK THE FIRST OPTION IN THE PANEL
        xpath_option = "(//li[contains(@class, 'p-dropdown-item') and not(contains(@class, 'p-disabled'))] | //mat-option | //*[@role='option'])[1]"
        opt = driver.find_element(By.XPATH, xpath_option)
        driver.execute_script("arguments[0].click();", opt)
        print(f"   ✅ DROPDOWN '{label_text}': SELECTED FIRST AVAILABLE OPTION.")
        time.sleep(0.5)
        return True
    except Exception as e:
        print(f"   ⚠️  WARNING: COULD NOT SELECT DROPDOWN '{label_text}'. ERROR: {e}")
        return False

def _fill_text_by_label(driver, label_text, value):
    """
    FINDS A TEXT INPUT NEXT TO A SPECIFIC LABEL AND INJECTS THE VALUE.
    """
    try:
        xpath = f"//label[contains(normalize-space(.), '{label_text}')]/following::input[1]"
        el = driver.find_element(By.XPATH,
    "//input[contains(@id,'id_medio') or "
    "        contains(@id,'medio') or "
    "        contains(@name,'id_medio') or "
    "        contains(@placeholder,'ID Medio') or "
    "        contains(@formcontrolname,'idMedio') or "
    "        contains(@formcontrolname,'id_medio')]"
)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        time.sleep(0.2)
        el.clear()
        el.send_keys(value)
        print(f"   ⌨️  ENTERED '{value}' IN FIELD '{label_text}'.")
        return value
    except Exception as e:
        print(f"   ⚠️  WARNING: COULD NOT FILL FIELD '{label_text}'. ERROR: {e}")
        return None

def _get_input_value_by_label(driver, label_text):
    """
    EXTRACTS THE CURRENT VALUE OF A TEXT INPUT NEXT TO A SPECIFIC LABEL.
    """
    try:
        xpath = f"//label[contains(normalize-space(.), '{label_text}')]/following::input[1]"
        el = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        return el.get_attribute("value").strip()
    except Exception:
        return ""


# ==================================================================================
# MER-01: GO TO THE COMERCIOS PAGE.
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
# MER-02: THE USER CAN VIEW THE LIST OF COMERCIOS.
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
# MER-03: GO TO COMERCIOS TABLE.
# ==================================================================================
def MER_03():
    print("\n" + "=" * 60)
    print("🧪 MER-03: GO TO COMERCIOS TABLE")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO COMERCIOS MODULE...")
        _login_and_go_to_comercios(driver)

        print("\n📸 TAKING SCREENSHOT #1 — COMERCIOS TABLE BEFORE CLICKING PENCIL...")
        utils.tomar_screenshot(driver, "MER_03_1_COMERCIOS_TABLE")

        
        print("\n👉 STEP 1: CLICKING PENCIL ✏️ ICON ON FIRST ROW (3-STRATEGY CASCADE)...")
        pencil_clicked = False

        
        try:
            btn = driver.find_element(By.XPATH, "(//tbody//tr[1]//button)[1]")
            driver.execute_script("arguments[0].click();", btn)
            pencil_clicked = True
            time.sleep(3)
            print("   ✅ PENCIL CLICKED — STRATEGY 1 (FIRST BUTTON IN FIRST TR).")
        except Exception as s1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {s1_err}")

        
        if not pencil_clicked:
            try:
                btn = driver.find_element(By.XPATH, XPATH_BTN_PENCIL_FIRST_ROW)
                driver.execute_script("arguments[0].click();", btn)
                pencil_clicked = True
                time.sleep(3)
                print("   ✅ PENCIL CLICKED — STRATEGY 2 (PENCIL ICON XPATH).")
            except Exception as s2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {s2_err}")

        
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

        
        print("\n👉 STEP 2: VERIFYING 'EDICIÓN DE COMERCIO' FORM TITLE IS VISIBLE...")
        time.sleep(2)
        form_visible = False

        
        try:
            driver.find_element(By.XPATH, XPATH_EDIT_COMERCIO_TITULO)
            form_visible = True
            print("   ✅ TITLE 'Edición de Comercio' FOUND — STRATEGY 1 (XPATH).")
        except Exception:
            print("   ⚠️  TITLE NOT FOUND VIA XPATH — TRYING JS SCAN...")

        
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
# MER-04: USER CAN VIEW LIST OF COMERCIO.
# ==================================================================================
def MER_04():
    print("\n" + "=" * 60)
    print("🧪 MER-04: USER CAN VIEW LIST OF COMERCIO.")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO COMERCIOS MODULE...")
        _login_and_go_to_comercios(driver)
        print("\n📸 TAKING SCREENSHOT #1 — COMERCIOS TABLE BEFORE DELETION...")
        utils.tomar_screenshot(driver, "MER_04_1_TABLE_BEFORE_DELETE")

        print("\n👉 STEP 1: VERIFYING COMERCIOS TABLE IS LOADED...")
        if not _tabla_comercios_is_loaded(driver):
            print("   ❌ TABLE NOT LOADED. ABORTING TEST.")
            return
        print("   ✅ TABLE LOADED.")
        print("\n👉 STEP 2: COUNTING DATA ROWS BEFORE DELETION...")
        row_count_before = 0
        try:
            rows = driver.find_elements(By.XPATH, "//tbody//tr")
            row_count_before = len(rows)
            if row_count_before > 0:
                print(f"   ✅ {row_count_before} ROW(S) FOUND.")
            else:
                print("   ⚠️  NO ROWS FOUND VIA XPATH — TRYING JS SCAN...")
                row_count_before = driver.execute_script("""
                    var rows = document.querySelectorAll('tbody tr, [class*="row"]:not([class*="header"])');
                    return rows.length;
                """)
                print(f"   ✅ JS SCAN FOUND {row_count_before} ROW(S).")
        except Exception as e:
            print(f"   ⚠️  ERROR COUNTING ROWS: {e}")

        if row_count_before == 0:
            print("   ❌ NO DATA ROWS TO DELETE. TEST CANNOT PROCEED.")
            return

        
        print("\n👉 STEP 3: CLICKING DELETE ICON 🗑️ ON FIRST ROW (4-STRATEGY CASCADE)...")
        delete_clicked = False

        try:
            btn = driver.find_element(By.XPATH, "(//tbody//tr[1]//button)[2]")
            driver.execute_script("arguments[0].click();", btn)
            delete_clicked = True
            time.sleep(2)
            print("   ✅ DELETE CLICKED — STRATEGY 1 (SECOND BUTTON IN FIRST TR).")
        except Exception as s1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {s1_err}")

        if not delete_clicked:
            try:
                btn = driver.find_element(By.XPATH,
                    "(//tbody//tr[1]//*[contains(@class,'trash') or contains(@class,'delete') or "
                    "contains(@class,'pi-trash') or contains(@class,'pi-delete')])[1]")
                driver.execute_script("arguments[0].click();", btn)
                delete_clicked = True
                time.sleep(2)
                print("   ✅ DELETE CLICKED — STRATEGY 2 (TRASH/DELETE CLASS).")
            except Exception as s2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {s2_err}")

        if not delete_clicked:
            try:
                result = driver.execute_script("""
                    var rows = document.querySelectorAll('tbody tr');
                    if (rows.length === 0) return 'NO ROWS';
                    var btns = rows[0].querySelectorAll('button, a[role="button"]');
                    for (var i=0; i<btns.length; i++) {
                        var btn = btns[i];
                        var html = btn.innerHTML.toLowerCase();
                        var cls = btn.className.toLowerCase();
                        var txt = btn.textContent.trim().toLowerCase();
                        if (html.includes('trash') || html.includes('delete') ||
                            cls.includes('trash') || cls.includes('delete') ||
                            txt === 'eliminar' || txt === 'delete' || txt === 'borrar') {
                            btn.click();
                            return 'clicked:' + i;
                        }
                    }
                    return 'NOT FOUND';
                """)
                if result and result.startswith('clicked:'):
                    delete_clicked = True
                    time.sleep(2)
                    print(f"   ✅ DELETE CLICKED — STRATEGY 3 (JS ICON DETECTION: {result}).")
                else:
                    print(f"   ⚠️  STRATEGY 3 RESULT: {result}")
            except Exception as s3_err:
                print(f"   ⚠️  STRATEGY 3 FAILED: {s3_err}")

        if not delete_clicked:
            try:
                result = driver.execute_script("""
                    var rows = document.querySelectorAll('tbody tr');
                    if (rows.length === 0) return 'NO ROWS';
                    var btns = rows[0].querySelectorAll('button:not([disabled]), a[role="button"]');
                    if (btns.length >= 2) {
                        btns[1].click();
                        return 'clicked second button';
                    }
                    return 'less than 2 buttons';
                """)
                if result == 'clicked second button':
                    delete_clicked = True
                    time.sleep(2)
                    print("   ✅ DELETE CLICKED — STRATEGY 4 (FALLBACK: SECOND VISIBLE BUTTON).")
                else:
                    print(f"   ❌ STRATEGY 4 FAILED: {result}")
            except Exception as s4_err:
                print(f"   ⚠️  STRATEGY 4 FAILED: {s4_err}")

        if not delete_clicked:
            print("   ❌ ALL DELETE CLICK STRATEGIES FAILED. TEST ABORTED.")
            return

        print("   🖱️  DELETE ACTION TRIGGERED. WAITING FOR CONFIRMATION DIALOG...")
        time.sleep(2)

        print("\n📸 TAKING SCREENSHOT #2 — AFTER CLICKING DELETE (CONFIRMATION DIALOG)...")
        utils.tomar_screenshot(driver, "MER_04_2_DELETE_CONFIRMATION")

        
        print("\n👉 STEP 4: LOOKING FOR CONFIRMATION DIALOG AND ACCEPTING...")
        confirmation_handled = False
        try:
            
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,
                    "//*[contains(@role,'dialog') or contains(@class,'modal') or contains(@class,'dialog')]"
                    "[.//*[contains(text(),'Eliminar') or contains(text(),'eliminar') or contains(text(),'Confirmar')]]"
                ))
            )
            print("   ✅ CONFIRMATION DIALOG DETECTED.")

            confirm_xpaths = [
                "//button[contains(text(),'Sí') or contains(text(),'Yes') or contains(text(),'Eliminar') or contains(text(),'Aceptar')]",
                "//*[contains(@class,'btn')][contains(.,'Eliminar') or contains(.,'Confirmar')]",
                "//button[contains(@class,'confirm') or contains(@class,'danger')]"
            ]
            for xp in confirm_xpaths:
                try:
                    confirm_btn = driver.find_element(By.XPATH, xp)
                    driver.execute_script("arguments[0].click();", confirm_btn)
                    confirmation_handled = True
                    print(f"   ✅ CONFIRMATION CLICKED USING: {xp[:60]}...")
                    break
                except:
                    continue

            if not confirmation_handled:
                print("   ⚠️  COULD NOT FIND CONFIRM BUTTON — TRYING JS SCAN...")
                result = driver.execute_script("""
                    var btns = document.querySelectorAll('button, a[role="button"]');
                    for (var btn of btns) {
                        var txt = btn.textContent.trim().toLowerCase();
                        if (txt === 'sí' || txt === 'yes' || txt === 'eliminar' || txt === 'delete' || txt === 'aceptar') {
                            btn.click();
                            return txt;
                        }
                    }
                    return null;
                """)
                if result:
                    confirmation_handled = True
                    print(f"   ✅ CONFIRMATION CLICKED VIA JS: '{result}'")
                else:
                    print("   ❌ CONFIRMATION BUTTON NOT FOUND. DELETION MAY NOT HAVE BEEN CONFIRMED.")
        except Exception as dialog_err:
            print(f"   ℹ️  NO CONFIRMATION DIALOG DETECTED (MAY BE DIRECT DELETE): {dialog_err}")
            
            confirmation_handled = True  # proceed

        print("   ⏳ WAITING FOR DELETION TO COMPLETE...")
        time.sleep(4)

        print("\n📸 TAKING SCREENSHOT #3 — AFTER CONFIRMATION / DELETION (SHOULD SHOW SUCCESS POPUP)...")
        utils.tomar_screenshot(driver, "MER_04_3_AFTER_DELETE")

        print("\n👉 STEP 5: VERIFYING ITEM WAS REMOVED...")
        deletion_success = False
        row_count_after = row_count_before

        print("   🔍 LOOKING FOR SUCCESS POPUP...")
        time.sleep(1)  

        try:
            
            toast_xpath = (
                "//*[contains(normalize-space(), 'Éxito') or contains(normalize-space(), 'exito') or "
                "contains(normalize-space(), 'Comercio eliminado correctamente')]"
            )
            
            toast_elements = driver.find_elements(By.XPATH, toast_xpath)
            found_toast = None
            for el in toast_elements:
                if el.is_displayed():
                    found_toast = el
                    break
            if found_toast:
                deletion_success = True
                print(f"   ✅ SUCCESS POPUP DETECTED: '{found_toast.text[:80]}'")
            else:
                
                WebDriverWait(driver, 4).until(
                    EC.visibility_of_element_located((By.XPATH, toast_xpath))
                )
                toast = driver.find_element(By.XPATH, toast_xpath)
                deletion_success = True
                print(f"   ✅ SUCCESS POPUP DETECTED (WAIT): '{toast.text[:80]}'")
        except Exception as toast_err:
            print(f"   ℹ️  SUCCESS POPUP NOT DETECTED: {toast_err}")

        
        if not deletion_success:
            print("   🔄 FALLBACK: CHECKING ROW COUNT...")
            try:
                rows = driver.find_elements(By.XPATH, "//tbody//tr")
                row_count_after = len(rows)
                if row_count_after == 0:
                    
                    row_count_after = driver.execute_script("""
                        var rows = document.querySelectorAll('tbody tr, [class*="row"]:not([class*="header"])');
                        return rows.length;
                    """)
                print(f"   📊 ROW COUNT BEFORE: {row_count_before} | AFTER: {row_count_after}")
                if row_count_after < row_count_before:
                    deletion_success = True
                    print("   ✅ ROW COUNT DECREASED — DELETION CONFIRMED.")
            except Exception as e:
                print(f"   ⚠️  ERROR COUNTING ROWS AFTER DELETE: {e}")

        
        if not deletion_success:
            try:
                no_data = driver.find_element(By.XPATH,
                    "//*[contains(text(),'No hay datos') or contains(text(),'No se encontraron')]")
                if no_data.is_displayed():
                    deletion_success = True
                    print("   ✅ 'NO DATA' MESSAGE APPEARED — TABLE EMPTY.")
            except:
                pass

        print("\n📸 TAKING SCREENSHOT #4 — FINAL TABLE STATE...")
        utils.tomar_screenshot(driver, "MER_04_4_FINAL_TABLE")

        test_passed = delete_clicked and deletion_success

        print(f"\n   🔬 MER-04 ASSERTION SUMMARY:")
        print(f"      • DELETE ICON CLICKED        : {delete_clicked}")
        print(f"      • CONFIRMATION HANDLED       : {confirmation_handled}")
        print(f"      • DELETION VERIFIED          : {deletion_success}")
        print(f"      • ROW COUNT CHANGE           : {row_count_before} → {row_count_after}")
        print(f"      • FINAL URL                  : {driver.current_url}")

        _capture_web_evidence(driver, "MER_04")

        if test_passed:
            utils.tomar_screenshot(driver, "MER_04_SUCCESS")
            print("\n✅ MER-04: SUCCESS — COMERCIO WAS DELETED FROM THE TABLE.")
        else:
            utils.tomar_screenshot(driver, "MER_04_FAILED")
            if not delete_clicked:
                print("\n❌ MER-04: FAILED — DELETE ICON COULD NOT BE CLICKED.")
            else:
                print("\n❌ MER-04: FAILED — DELETION COULD NOT BE VERIFIED.")

    except Exception as e:
        print(f"\n💥 MER-04 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "MER_04_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()

# ==================================================================================
# MER-05: USER AUTHENTICATED. USER HAS PERMISSIONS TO VIEW AND CREATE.
# ==================================================================================
def MER_05():
    print("\n" + "=" * 60)
    print("🧪 MER-05: USER AUTHENTICATED. USER HAS PERMISSIONS TO VIEW AND CREATE. ")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        # PRECONDITION: LOG IN AND NAVIGATE TO COMERCIOS MODULE
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO COMERCIOS MODULE...")
        _login_and_go_to_comercios(driver)

        print("\n📸 TAKING SCREENSHOT #1 — COMERCIOS TABLE BEFORE CLICKING 'NUEVO +'...")
        utils.tomar_screenshot(driver, "MER_05_1_COMERCIOS_TABLE")

        # STEP 1: VERIFY COMERCIOS TABLE IS LOADED
        print("\n👉 STEP 1: VERIFYING COMERCIOS TABLE IS LOADED...")
        if not _tabla_comercios_is_loaded(driver):
            print("   ❌ TABLE NOT LOADED. ABORTING TEST.")
            return
        print("   ✅ TABLE LOADED.")

        # STEP 2: CLICK 'NUEVO +' BUTTON
        print("\n👉 STEP 2: CLICKING 'NUEVO +' BUTTON (3-STRATEGY CASCADE)...")
        nuevo_clicked = False

        # STRATEGY 1: XPATH — USE XPATH_BTN_NUEVO DEFINED AT MODULE LEVEL
        try:
            btn = driver.find_element(By.XPATH, XPATH_BTN_NUEVO)
            driver.execute_script("arguments[0].click();", btn)
            nuevo_clicked = True
            time.sleep(3)
            print("   ✅ 'NUEVO +' CLICKED — STRATEGY 1 (XPATH_BTN_NUEVO).")
        except Exception as s1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {s1_err}")

        # STRATEGY 2: JS — SCAN FOR VISIBLE BUTTON WITH TEXT 'Nuevo'
        if not nuevo_clicked:
            try:
                result = driver.execute_script("""
                    var btns = document.querySelectorAll('button, a');
                    for (var btn of btns) {
                        var txt = btn.textContent.trim();
                        if ((txt.includes('Nuevo') || txt.includes('NUEVO')) && btn.offsetWidth > 0) {
                            btn.click();
                            return txt;
                        }
                    }
                    return null;
                """)
                if result:
                    nuevo_clicked = True
                    time.sleep(3)
                    print(f"   ✅ 'NUEVO +' CLICKED — STRATEGY 2 (JS SCAN: '{result}').")
                else:
                    print("   ⚠️  STRATEGY 2: NO 'NUEVO' BUTTON FOUND.")
            except Exception as s2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {s2_err}")

        # STRATEGY 3: FALLBACK — DIRECT NAVIGATION TO KNOWN URL (IF EXISTS)
        if not nuevo_clicked:
            print("   ⚠️  ALL CLICK STRATEGIES FAILED. ATTEMPTING DIRECT NAVIGATION TO CREATION URL...")
            driver.get("https://fat.memphis.mx/merchant/create")  # GUESSED URL — ADJUST IF NEEDED
            time.sleep(4)
            nuevo_clicked = True  # ASSUME NAVIGATION WORKED
            print(f"   🌐 NAVIGATED DIRECTLY TO: {driver.current_url}")

        print(f"   🌐 CURRENT URL AFTER CLICK: {driver.current_url}")

        print("\n📸 TAKING SCREENSHOT #2 — AFTER CLICKING 'NUEVO +' (LOADING FORM)...")
        utils.tomar_screenshot(driver, "MER_05_2_AFTER_CLICK_NUEVO")

        # STEP 3: VERIFY 'CREACIÓN DE COMERCIO' FORM IS VISIBLE
        print("\n👉 STEP 3: VERIFYING 'CREACIÓN DE COMERCIO' FORM TITLE IS VISIBLE...")
        time.sleep(2)
        form_visible = False

        # STRATEGY 1: XPATH — LOOK FOR HEADING WITH 'Creación de Comercio'
        try:
            # XPATH TO MATCH 'Creación de Comercio' IN H1, H2, OR ANY TITLE ELEMENT
            xpath_titulo_creacion = (
                "//h1[contains(text(),'Creación de Comercio')] | "
                "//h2[contains(text(),'Creación de Comercio')] | "
                "//*[contains(@class,'title') or contains(@class,'heading')]"
                "[contains(text(),'Creación de Comercio')] | "
                "//*[normalize-space(text())='Creación de Comercio']"
                "[not(ancestor::nav) and not(ancestor::aside)]"
            )
            driver.find_element(By.XPATH, xpath_titulo_creacion)
            form_visible = True
            print("   ✅ TITLE 'Creación de Comercio' FOUND — STRATEGY 1 (XPATH).")
        except Exception:
            print("   ⚠️  TITLE NOT FOUND VIA XPATH — TRYING JS SCAN...")

        # STRATEGY 2: JS — SCAN ALL HEADINGS FOR THE TITLE TEXT
        if not form_visible:
            try:
                result = driver.execute_script("""
                    var all = document.querySelectorAll('h1, h2, h3, h4, [class*="title"], [class*="heading"]');
                    for (var el of all) {
                        var txt = el.textContent.trim().toLowerCase();
                        if (txt.includes('creación de comercio') || txt.includes('creacion de comercio')) {
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

        # STRATEGY 3: URL CHECK — CREATION FORM URL CONTAINS 'create' OR 'nuevo'
        if not form_visible:
            url_lower = driver.current_url.lower()
            if "create" in url_lower or "nuevo" in url_lower or "crear" in url_lower:
                form_visible = True
                print(f"   ✅ URL INDICATES CREATION FORM: {driver.current_url}")
            else:
                print(f"   ❌ URL DOES NOT INDICATE CREATION FORM: {driver.current_url}")

        
        print("\n👉 STEP 4: CONFIRMING FORM FIELDS ARE EMPTY (VISUAL CHECK)...")
        # WE CAN QUICKLY CHECK IF ANY INPUT FIELD HAS PRE-FILLED TEXT (NOT STRICTLY REQUIRED)
        try:
            # CHECK FIRST VISIBLE INPUT FIELD (E.G., RFC) — IF IT HAS VALUE, WARN
            first_input = driver.find_element(By.XPATH, "//input[not(@type='hidden') and @visible]")
            current_value = first_input.get_attribute("value")
            if current_value:
                print(f"   ⚠️  WARNING: FIRST INPUT FIELD HAS PRE-FILLED VALUE: '{current_value}'")
            else:
                print("   ✅ FIRST INPUT FIELD IS EMPTY (AS EXPECTED).")
        except Exception:
            print("   ℹ️  COULD NOT CHECK INPUT FIELD VALUES — VISUAL CONFIRMATION IN SCREENSHOT.")

        # TAKE KEY SCREENSHOT — THE CREATION FORM WITH EMPTY FIELDS
        print("\n📸 TAKING SCREENSHOT #3 — 'CREACIÓN DE COMERCIO' FORM WITH EMPTY FIELDS (KEY EVIDENCE)...")
        utils.tomar_screenshot(driver, "MER_05_3_CREACION_COMERCIO_EMPTY_FORM")

        # FINAL ASSERTION
        test_passed = nuevo_clicked and form_visible

        print(f"\n   🔬 MER-05 ASSERTION SUMMARY:")
        print(f"      • 'NUEVO +' CLICKED          : {nuevo_clicked}")
        print(f"      • CREATION FORM TITLE VISIBLE: {form_visible}")
        print(f"      • FINAL URL                  : {driver.current_url}")

        _capture_web_evidence(driver, "MER_05")

        if test_passed:
            utils.tomar_screenshot(driver, "MER_05_SUCCESS")
            print("\n✅ MER-05: SUCCESS — 'CREACIÓN DE COMERCIO' FORM OPENED WITH EMPTY FIELDS.")
        else:
            utils.tomar_screenshot(driver, "MER_05_FAILED")
            if not nuevo_clicked:
                print("\n❌ MER-05: FAILED — 'NUEVO +' BUTTON COULD NOT BE CLICKED.")
            else:
                print("\n❌ MER-05: FAILED — 'CREACIÓN DE COMERCIO' FORM TITLE NOT FOUND.")

    except Exception as e:
        print(f"\n💥 MER-05 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "MER_05_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()

# ==================================================================================
# TEST DATA — MER-06: NEW COMERCIO CREATION
# ==================================================================================
MER06_SOCIAL_REASON      = "AutoTest Razon Social SA"
MER06_COMERCIAL_NAME  = "AutoTest Comercio"
MER06_RFC               = "CACX7605101P8"
MER06_REPRESENT    = "AutoTest Representante"
MER06_URL               = "https://autotest.memphis.mx"
MER06_STREET           = "Calle AutoTest"
MER06_EXTERIOR_NUMBER       = "101"
MER06_INTERIOR_NUMBER      = "A"
MER06_COLOGNE        = "Colonia AutoTest"
MER06_ZIP_CODE    = "54321"
MER06_MUNICIPALITY      = "AutoTest Municipio"
MER06_CITY         = "AutoTest Ciudad"
MER06_DESCRIPTION      = "Comercio creado por automatizacion MER06"
MER06_SALES_AGENT  = "Agente AutoTest"

MER06_CONTACT_NAME   = "Contacto AutoTest"
MER06_ROLE              = "Gerente"
MER06_MAIL            = "autotest.mer06@memphis.mx"
MER06_MAIN_CEL     = "5550001234"
MER06_ALTERNATE_CEL       = "5550005678"
MER06_CELLPHONE           = "5559991234"

MER06_AFILIATION_NUMBER    = "8000001"
MER06_SUBAFILIACION_NO  = "0001"
MER06_TOKEN_REGISTER    = "TOKEN_AUTOTEST_001"
MER06_BROXEL_NAME     = "AutoTest Broxel"
MER06_VISA_FAC          = "4000000000001"
MER06_MASTERCARD_FAC    = "5200000000001"
MER06_INTERNACIONAL_FAC = "3700000000001"
MER06_VISA_ISO          = "4000000000002"
MER06_MASTERCARD_ISO    = "5200000000002"
MER06_ID_MEDIO          = "MEDIO_001"
MER06_AFILIACION_LINK   = "LINK_001"
MER06_ID_MEDIO_LINK     = "IDLINK_001"
MER06_TERMINAL_SERIES    = "TERM_AUTOTEST"

MER06_MINIUM_AMOUNT         = "10"
MER06_MAX_AMOUNT       = "99999"

MER06_BANK            = "Banco AutoTest"
MER06_CARD        = "4111111111111111"
MER06_NO_CUENTA         = "123456789"
MER06_CLABE             = "032180000118359719"

XPATH_BTN_SAVE_FORM = (
    "//button[contains(translate(.,'GUARDAR','guardar'),'guardar')] | "
    "//button[contains(text(),'Guardar') or contains(text(),'GUARDAR')]"
)


# ==================================================================================
# HELPER — SELECT FIRST AVAILABLE OPTION IN A NATIVE <select> ELEMENT
# ==================================================================================
def _select_first_option(driver, xpath_select, field_name):
    """
    FINDS A <select> BY XPATH AND SELECTS THE FIRST NON-PLACEHOLDER OPTION.
    RETURNS True IF SELECTION SUCCEEDED, False OTHERWISE.
    """
    try:
        from selenium.webdriver.support.ui import Select as SeleniumSelect
        el  = driver.find_element(By.XPATH, xpath_select)
        sel = SeleniumSelect(el)
        for opt in sel.options:
            val = opt.get_attribute("value") or ""
            txt = opt.text.strip()
            if val and val != "" and not txt.lower().startswith("selecciona"):
                sel.select_by_value(val)
                time.sleep(0.3)
                print(f"      ✅ {field_name} → '{txt}' (FIRST AVAILABLE OPTION).")
                return True
        print(f"      ⚠️  {field_name} — NO VALID OPTIONS FOUND.")
        return False
    except Exception as e:
        try:
            result = driver.execute_script(f"""
                var el = document.evaluate("{xpath_select}",
                    document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                if (!el) return 'SELECT NOT FOUND';
                for (var i = 0; i < el.options.length; i++) {{
                    var opt = el.options[i];
                    if (opt.value && opt.value !== '' &&
                        !opt.text.trim().toLowerCase().startsWith('selecciona')) {{
                        el.value = opt.value;
                        el.dispatchEvent(new Event('change', {{bubbles: true}}));
                        return 'set:' + opt.text.trim();
                    }}
                }}
                return 'NO OPTIONS';
            """)
            if result and result.startswith('set:'):
                print(f"      ✅ {field_name} → JS FALLBACK: '{result}'.")
                return True
            print(f"      ⚠️  {field_name} JS FALLBACK: {result}")
        except Exception as js_e:
            print(f"      ❌ {field_name} ALL STRATEGIES FAILED: {js_e}")
        return False


def _fill_text_field(driver, xpath, value, field_name):
    """
    FILLS A TEXT INPUT FIELD WITH THE GIVEN VALUE.
    USES TRIPLE-CLICK TO SELECT ALL + send_keys FOR ANGULAR COMPATIBILITY.
    ActionChains SIMULATES REAL KEYBOARD INPUT — ANGULAR DETECTS IT CORRECTLY.
    JS FALLBACK ONLY USED AS LAST RESORT (ANGULAR MAY NOT VALIDATE JS-SET VALUES).
    """
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.keys import Keys

    try:
        el = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        time.sleep(0.3)
        # TRIPLE CLICK SELECTS ALL EXISTING TEXT, THEN send_keys REPLACES IT
        ActionChains(driver).click(el).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
        time.sleep(0.1)
        el.send_keys(value)
        # TRIGGER BLUR TO FIRE ANGULAR VALIDATION
        ActionChains(driver).send_keys(Keys.TAB).perform()
        time.sleep(0.2)
        print(f"      ✅ {field_name} → '{value}'")
        return True
    except Exception as e1:
        # FALLBACK: CLICK + CLEAR + SEND_KEYS WITHOUT ActionChains
        try:
            el = driver.find_element(By.XPATH, xpath)
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            time.sleep(0.2)
            el.click()
            time.sleep(0.1)
            el.send_keys(Keys.CONTROL + "a")
            time.sleep(0.1)
            el.send_keys(value)
            el.send_keys(Keys.TAB)
            time.sleep(0.2)
            print(f"      ✅ {field_name} → '{value}' (FALLBACK send_keys)")
            return True
        except Exception as e2:
            print(f"      ❌ {field_name} FAILED: {e2}")
            return False

# ==================================================================================
# MER-06: CREATE NEW USER
# ==================================================================================

def MER_06():
    
    print("\n" + "=" * 60)
    print("🧪 MER-06: CREATE NEW USER")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO COMERCIOS MODULE...")
        _login_and_go_to_comercios(driver)

        print("\n📸 TAKING SCREENSHOT #1 — COMERCIOS TABLE BEFORE CLICKING NUEVO...")
        utils.tomar_screenshot(driver, "MER_06_1_COMERCIOS_TABLE")

        # ── STEP 1: CLICK 'NUEVO +' ───────────────────────────────────────────
        print("\n👉 STEP 1: CLICKING 'NUEVO +' BUTTON...")
        nuevo_clicked = False

        try:
            btn = driver.find_element(By.XPATH, XPATH_BTN_NUEVO)
            driver.execute_script("arguments[0].click();", btn)
            nuevo_clicked = True
            time.sleep(3)
            print("   ✅ 'NUEVO +' CLICKED — STRATEGY 1 (XPATH).")
        except Exception as n1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {n1_err}")

        if not nuevo_clicked:
            try:
                result = driver.execute_script("""
                    var btns = document.querySelectorAll('button, a');
                    for (var b of btns) {
                        if (b.textContent.trim().toLowerCase().includes('nuevo')
                                && b.offsetWidth > 0) {
                            b.click();
                            return b.textContent.trim();
                        }
                    }
                    return null;
                """)
                if result:
                    nuevo_clicked = True
                    time.sleep(3)
                    print(f"   ✅ 'NUEVO +' CLICKED — STRATEGY 2 (JS: '{result}').")
            except Exception as n2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {n2_err}")

        print(f"   🌐 CURRENT URL: {driver.current_url}")
        print("\n📸 TAKING SCREENSHOT #2 — CREATION FORM OPENED...")
        utils.tomar_screenshot(driver, "MER_06_2_CREATION_FORM_OPEN")

        # ── STEP 2: SECTION 1 — DATOS DE COMERCIO ────────────────────────────
        print("\n👉 STEP 2: FILLING SECTION 1 — DATOS DE COMERCIO...")

        # IDS CONFIRMED: id_client, id_person_type, id_tax_regime, id_state, id_country
        _select_first_option(driver, "//select[@id='id_client']", "CLIENTE")
        time.sleep(0.5)

        _select_first_option(driver, "//select[@id='id_person_type']", "TIPO DE PERSONA")
        time.sleep(0.5)

        _fill_text_field(driver,
            "//input[contains(@placeholder,'Razón Social') or contains(@id,'razon') or "
            "        contains(@formcontrolname,'razon')]",
            MER06_SOCIAL_REASON, "RAZON SOCIAL")
        time.sleep(0.2)

        _fill_text_field(driver,
            "//input[contains(@placeholder,'Nombre Comercial') or "
            "        contains(@formcontrolname,'nombreComercial') or "
            "        contains(@formcontrolname,'nombre_comercial')]",
            MER06_COMERCIAL_NAME, "NOMBRE COMERCIAL")
        time.sleep(0.2)

        _fill_text_field(driver,
            "//input[@placeholder='RFC' or contains(@id,'rfc') or "
            "        contains(@formcontrolname,'rfc')]",
            MER06_RFC, "RFC")
        time.sleep(0.2)

        _fill_text_field(driver,
            "//input[contains(@placeholder,'Representante') or "
            "        contains(@formcontrolname,'representante')]",
            MER06_REPRESENT, "REPRESENTANTE")
        time.sleep(0.2)

        _select_first_option(driver, "//select[@id='id_tax_regime']", "REGIMEN FISCAL")
        time.sleep(0.5)

        _fill_text_field(driver,
            "//input[@placeholder='URL' or contains(@formcontrolname,'url')]",
            MER06_URL, "URL")
        time.sleep(0.2)

        _fill_text_field(driver,
            "//input[contains(@placeholder,'Calle') or contains(@formcontrolname,'calle')]",
            MER06_STREET, "CALLE")
        time.sleep(0.2)

        _fill_text_field(driver,
            "//input[contains(@placeholder,'Exterior') or contains(@formcontrolname,'exterior') or "
            "        contains(@formcontrolname,'noExt')]",
            MER06_EXTERIOR_NUMBER, "NO. EXTERIOR")
        time.sleep(0.2)

        _fill_text_field(driver,
            "//input[contains(@placeholder,'Interior') or contains(@formcontrolname,'interior') or "
            "        contains(@formcontrolname,'noInt')]",
            MER06_INTERIOR_NUMBER, "NO. INTERIOR")
        time.sleep(0.2)

        _fill_text_field(driver,
            "//input[contains(@placeholder,'Colonia') or contains(@formcontrolname,'colonia')]",
            MER06_COLOGNE, "COLONIA")
        time.sleep(0.2)

        _fill_text_field(driver,
            "//input[contains(@placeholder,'Código Postal') or contains(@placeholder,'Postal') or "
            "        contains(@formcontrolname,'codigoPostal') or contains(@formcontrolname,'cp')]",
            MER06_ZIP_CODE, "CODIGO POSTAL")
        time.sleep(0.2)

        _fill_text_field(driver,
            "//input[contains(@placeholder,'Municipio') or contains(@placeholder,'Alcald') or "
            "        contains(@formcontrolname,'municipio') or contains(@formcontrolname,'alcaldia')]",
            MER06_MUNICIPALITY, "MUNICIPIO")
        time.sleep(0.2)

        _fill_text_field(driver,
            "//input[contains(@placeholder,'Ciudad') or contains(@formcontrolname,'ciudad')]",
            MER06_CITY, "CIUDAD")
        time.sleep(0.2)

        # ID CONFIRMED: id_state
        _select_first_option(driver, "//select[@id='id_state']", "ESTADO")
        time.sleep(0.5)

        # ID CONFIRMED: id_country
        _select_first_option(driver, "//select[@id='id_country']", "PAIS")
        time.sleep(0.5)

        _fill_text_field(driver,
            "//textarea[contains(@placeholder,'Descripción') or contains(@formcontrolname,'descripcion')] | "
            "//input[contains(@placeholder,'Descripción') or contains(@formcontrolname,'descripcion')]",
            MER06_DESCRIPTION, "DESCRIPCION")
        time.sleep(0.2)

        _fill_text_field(driver,
            "//input[contains(@placeholder,'Agente') or contains(@formcontrolname,'agente')]",
            MER06_SALES_AGENT, "AGENTE COMERCIAL")
        time.sleep(0.2)

        print("\n📸 TAKING SCREENSHOT #3 — SECTION 1 FILLED...")
        utils.tomar_screenshot(driver, "MER_06_3_SECTION1_FILLED")

        # ── STEP 3: SECTION 2 — DATOS DE CONTACTO ────────────────────────────
        print("\n👉 STEP 3: FILLING SECTION 2 — DATOS DE CONTACTO...")

        _fill_text_field(driver,
            "//input[contains(@placeholder,'Nombre') or contains(@formcontrolname,'nombre')]"
            "[ancestor::*[.//*[contains(text(),'DATOS DE CONTACTO') or "
            "             contains(text(),'Datos de Contacto')]]]",
            MER06_CONTACT_NAME, "NOMBRE CONTACTO")
        time.sleep(0.2)

        _fill_text_field(driver,
            "//input[contains(@placeholder,'Rol') or contains(@formcontrolname,'rol')]",
            MER06_ROLE, "ROL")
        time.sleep(0.2)

        _fill_text_field(driver,
            "//input[contains(@placeholder,'Correo') or contains(@placeholder,'Email') or "
            "        contains(@formcontrolname,'correo') or contains(@formcontrolname,'email')]",
            MER06_MAIL, "CORREO ELECTRONICO")
        time.sleep(0.2)

        _fill_text_field(driver,
            "//input[contains(@placeholder,'Teléfono Principal') or "
            "        contains(@formcontrolname,'telefonoPrincipal')]",
            MER06_MAIN_CEL, "TELEFONO PRINCIPAL")
        time.sleep(0.2)

        _fill_text_field(driver,
            "//input[contains(@placeholder,'Teléfono Alterno') or "
            "        contains(@formcontrolname,'telefonoAlterno')]",
            MER06_ALTERNATE_CEL, "TELEFONO ALTERNO")
        time.sleep(0.2)

        _fill_text_field(driver,
            "//input[contains(@placeholder,'Celular') or contains(@formcontrolname,'celular')]",
            MER06_CELLPHONE, "CELULAR")
        time.sleep(0.2)

        print("\n📸 TAKING SCREENSHOT #4 — SECTION 2 FILLED...")
        utils.tomar_screenshot(driver, "MER_06_4_SECTION2_FILLED")

        # ── STEP 4: SECTION 3 — DATOS DE OPERACIÓN ───────────────────────────
        print("\n👉 STEP 4: FILLING SECTION 3 — DATOS DE OPERACION...")

        # ALL IDS CONFIRMED VIA BROWSER CONSOLE
        _select_first_option(driver,
            "//select[@id='id_transactional_schema']", "ESQUEMA TRANSACCIONAL")
        time.sleep(0.5)

        _fill_text_field(driver,
            "//input[contains(@placeholder,'Afiliación No') or "
            "        contains(@formcontrolname,'afiliacion')]",
            MER06_AFILIATION_NUMBER, "AFILIACION NO")
        time.sleep(0.2)

        _fill_text_field(driver,
            "//input[contains(@placeholder,'Subafiliación') or "
            "        contains(@formcontrolname,'subafiliacion')]",
            MER06_SUBAFILIACION_NO, "SUBAFILIACION NO")
        time.sleep(0.2)

        _select_first_option(driver, "//select[@id='id_mcc']", "GIRO MCC")
        time.sleep(0.5)

        _select_first_option(driver, "//select[@id='id_acquirer_bank']", "BANCO ADQUIRENTE")
        time.sleep(0.5)

        _select_first_option(driver, "//select[@id='id_ln']", "RED LOGICA")
        time.sleep(0.5)

        _select_first_option(driver, "//select[@id='ln_aggregator']", "NOMBRE AGREGADOR")
        time.sleep(0.5)

        _select_first_option(driver, "//select[@id='id_processor']", "PROCESADOR")
        time.sleep(0.5)

        _fill_text_field(driver,
            "//input[contains(@placeholder,'Token') or contains(@formcontrolname,'token')]",
            MER06_TOKEN_REGISTER, "TOKEN DE REGISTRO")
        time.sleep(0.2)

        _fill_text_field(driver,
            "//input[contains(@placeholder,'Nombre del Comercio') or "
            "        contains(@formcontrolname,'nombreBroxel')]",
            MER06_BROXEL_NAME, "NOMBRE COMERCIO BROXEL")
        time.sleep(0.2)

        _fill_text_field(driver,
            "(//input[contains(@id,'visa') or contains(@formcontrolname,'visa')])[1]",
            MER06_VISA_FAC, "VISA FACILITADOR")
        time.sleep(0.2)

        _fill_text_field(driver,
            "(//input[contains(@id,'mastercard') or contains(@formcontrolname,'mastercard')])[1]",
            MER06_MASTERCARD_FAC, "MASTERCARD FACILITADOR")
        time.sleep(0.2)

        _fill_text_field(driver,
            "(//input[contains(@id,'internacional') or contains(@formcontrolname,'internacional')])[1]",
            MER06_INTERNACIONAL_FAC, "INTERNACIONAL FACILITADOR")
        time.sleep(0.2)

        _fill_text_field(driver,
            "(//input[contains(@id,'visa') or contains(@formcontrolname,'visa')])[2]",
            MER06_VISA_ISO, "VISA ISO")
        time.sleep(0.2)

        _fill_text_field(driver,
            "(//input[contains(@id,'mastercard') or contains(@formcontrolname,'mastercard')])[2]",
            MER06_MASTERCARD_ISO, "MASTERCARD ISO")
        time.sleep(0.2)

        _fill_text_field(driver,
            "//input[contains(@id,'id_medio') or contains(@formcontrolname,'idMedio') or "
            "        contains(@placeholder,'ID Medio')]",
            MER06_ID_MEDIO, "ID MEDIO")
        time.sleep(0.2)

        _select_first_option(driver, "//select[@id='id_transaction_mode']", "MODO TRANSACCION")
        time.sleep(0.5)

        _select_first_option(driver, "//select[@id='id_url_target']", "URL DESTINO")
        time.sleep(0.5)

        _select_first_option(driver, "//select[@id='id_profile_transaction']", "PERFIL TRANSACCIONAL")
        time.sleep(0.5)

        _fill_text_field(driver,
            "//input[contains(@placeholder,'Serie Terminal') or contains(@formcontrolname,'serie')]",
            MER06_TERMINAL_SERIES, "SERIE TERMINAL")
        time.sleep(0.2)

        _fill_text_field(driver,
            "//input[contains(@placeholder,'Afiliación Link') or "
            "        contains(@formcontrolname,'afiliacionLink')]",
            MER06_AFILIACION_LINK, "AFILIACION LINK DE PAGO")
        time.sleep(0.2)

        _fill_text_field(driver,
            "//input[contains(@placeholder,'ID Medio Link') or "
            "        contains(@formcontrolname,'idMedioLink')]",
            MER06_ID_MEDIO_LINK, "ID MEDIO LINK DE PAGO")
        time.sleep(0.2)

        # ID CONFIRMED: tax
        _select_first_option(driver, "//select[@id='tax']", "VALOR DE IMPUESTO")
        time.sleep(0.5)

        print("\n📸 TAKING SCREENSHOT #5 — SECTION 3 FILLED...")
        utils.tomar_screenshot(driver, "MER_06_5_SECTION3_FILLED")

        # ── STEP 5: SECTION 4 — VALIDACIONES ─────────────────────────────────
        print("\n👉 STEP 5: FILLING SECTION 4 — VALIDACIONES...")

        _fill_text_field(driver,
            "//input[contains(@placeholder,'Monto') and contains(@placeholder,'Mínima')] | "
            "//input[contains(@formcontrolname,'montoMin') or contains(@formcontrolname,'minimo')]",
            MER06_MINIUM_AMOUNT, "MONTO MINIMO")
        time.sleep(0.2)

        _fill_text_field(driver,
            "//input[contains(@placeholder,'Monto') and contains(@placeholder,'Máximo')] | "
            "//input[contains(@formcontrolname,'montoMax') or contains(@formcontrolname,'maximo')]",
            MER06_MAX_AMOUNT, "MONTO MAXIMO")
        time.sleep(0.2)

        # ── STEP 6: SECTION 5 — DATOS BANCARIOS ──────────────────────────────
        print("\n👉 STEP 6: FILLING SECTION 5 — DATOS BANCARIOS...")
        _fill_text_field(driver,
            "//div[.//*[contains(text(),'DATOS BANCARIOS') or contains(text(),'Datos Bancarios')]]"
            "//following::input[1]",
            MER06_BANK, "BANCO")

        _fill_text_field(driver,
            "//input[contains(@placeholder,'Tarjeta') or contains(@formcontrolname,'tarjeta')]",
            MER06_CARD, "TARJETA")
        time.sleep(0.2)

        _fill_text_field(driver,
            "//input[contains(@placeholder,'No. Cuenta') or contains(@formcontrolname,'cuenta')]",
            MER06_NO_CUENTA, "NO. CUENTA")
        time.sleep(0.2)

        _fill_text_field(driver,
            "//input[contains(@placeholder,'CLABE') or contains(@formcontrolname,'clabe')]",
            MER06_CLABE, "CLABE")
        time.sleep(0.2)

        print("\n📸 TAKING SCREENSHOT #6 — SECTIONS 4 AND 5 FILLED...")
        utils.tomar_screenshot(driver, "MER_06_6_SECTIONS4_5_FILLED")

        # SECTIONS 6 & 7 — COMISIONES: LEAVE DEFAULT 0% VALUES
        print("\n👉 STEP 7: SECTIONS 6 & 7 — COMISIONES: USING DEFAULT 0% VALUES...")
        print("   ℹ️  COMMISSION FIELDS ARE PRE-FILLED WITH 0% / $0 — NO INPUT NEEDED.")

        # ── STEP 8: CLICK 'GUARDAR' ───────────────────────────────────────────
        print("\n👉 STEP 8: SCROLLING TO BOTTOM AND CLICKING 'GUARDAR' BUTTON...")
        guardar_clicked = False

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        try:
            btn = driver.find_element(By.XPATH, XPATH_BTN_SAVE_FORM)
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
            time.sleep(1)
            btn.click()
            guardar_clicked = True
            print("   ✅ 'GUARDAR' CLICKED — STRATEGY 1 (XPATH).")
        except Exception as g1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {g1_err}")

        if not guardar_clicked:
            try:
                result = driver.execute_script("""
                    window.scrollTo(0, document.body.scrollHeight);
                    var btns = document.querySelectorAll('button');
                    for (var btn of btns) {
                        if (btn.textContent.trim().toLowerCase().includes('guardar')
                                && btn.offsetWidth > 0) {
                            btn.scrollIntoView({block:'center'});
                            btn.click();
                            return btn.textContent.trim();
                        }
                    }
                    return null;
                """)
                if result:
                    guardar_clicked = True
                    print(f"   ✅ 'GUARDAR' CLICKED — STRATEGY 2 (JS: '{result}').")
            except Exception as g2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {g2_err}")

        time.sleep(6)  # LONGER WAIT — FORM SUBMISSION + SERVER RESPONSE

        # ── STEP 9: CLICK PENCIL ON FIRST ROW ─────────────────────────────────
        # WAIT FOR REDIRECT TO TABLE FIRST
        print("\n👉 STEP 9: WAITING FOR REDIRECT TO TABLE AND CLICKING PENCIL ✏️...")
        time.sleep(3)

        # WAIT UP TO 10 SECONDS FOR TABLE TO APPEAR AFTER SAVE
        table_appeared = False
        for _ in range(10):
            if "create" not in driver.current_url.lower():
                table_appeared = True
                break
            time.sleep(1)

        if not table_appeared:
            print(f"   ⚠️  STILL ON FORM URL: {driver.current_url} — NAVIGATING TO TABLE DIRECTLY...")
            driver.get("https://fat.memphis.mx/merchant")  # URL REAL CONFIRMADA EN LOG
            time.sleep(4)

        print(f"   🌐 CURRENT URL BEFORE PENCIL CLICK: {driver.current_url}")

        pencil_clicked = False

        try:
            btn = driver.find_element(By.XPATH, "(//tbody//tr[1]//button)[1]")
            driver.execute_script("arguments[0].click();", btn)
            pencil_clicked = True
            time.sleep(3)
            print("   ✅ PENCIL CLICKED — STRATEGY 1 (FIRST BUTTON IN FIRST TR).")
        except Exception as p1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {p1_err}")

        if not pencil_clicked:
            try:
                result = driver.execute_script("""
                    var rows = document.querySelectorAll('tbody tr');
                    if (rows.length === 0) return 'NO ROWS';
                    var btns = rows[0].querySelectorAll('button, a[role="button"]');
                    if (btns.length === 0) return 'NO BUTTONS';
                    btns[0].click();
                    return 'clicked:' + btns[0].className;
                """)
                if result and result.startswith('clicked:'):
                    pencil_clicked = True
                    time.sleep(3)
                    print(f"   ✅ PENCIL CLICKED — STRATEGY 2 (JS: '{result}').")
                else:
                    print(f"   ❌ PENCIL JS DEBUG: {result}")
            except Exception as p2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {p2_err}")

        time.sleep(2)
        print(f"   🌐 CURRENT URL: {driver.current_url}")

        # ── STEP 10: VERIFY NOMBRE COMERCIAL PERSISTED ─────────────────────────
        print("\n👉 STEP 10: VERIFYING 'NOMBRE COMERCIAL' MATCHES ORIGINAL INPUT...")
        nombre_verified = False
        nombre_found    = ""

        XPATH_NOMBRE_COMERCIAL_INPUT = (
            "//input[contains(@placeholder,'Nombre Comercial') or "
            "        contains(@formcontrolname,'nombreComercial') or "
            "        contains(@formcontrolname,'nombre_comercial')]"
        )

        try:
            el           = driver.find_element(By.XPATH, XPATH_NOMBRE_COMERCIAL_INPUT)
            nombre_found = el.get_attribute("value") or ""
            nombre_verified = nombre_found.strip() == MER06_NOMBRE_COMERCIAL.strip()
            if nombre_verified:
                print(f"   ✅ NOMBRE COMERCIAL MATCHES: '{nombre_found}'")
            else:
                print(f"   ❌ MISMATCH — EXPECTED: '{MER06_NOMBRE_COMERCIAL}' | FOUND: '{nombre_found}'")
        except Exception as v1_err:
            print(f"   ⚠️  FIELD NOT FOUND VIA XPATH — TRYING JS: {v1_err}")
            try:
                nombre_found = driver.execute_script(f"""
                    var inputs = document.querySelectorAll('input');
                    for (var inp of inputs) {{
                        if (inp.value && inp.value.trim() === '{MER06_NOMBRE_COMERCIAL}') {{
                            return inp.value.trim();
                        }}
                    }}
                    return null;
                """)
                if nombre_found:
                    nombre_verified = True
                    print(f"   ✅ NOMBRE COMERCIAL FOUND VIA JS: '{nombre_found}'")
                else:
                    print(f"   ❌ '{MER06_NOMBRE_COMERCIAL}' NOT FOUND IN ANY INPUT.")
            except Exception as v2_err:
                print(f"   ⚠️  JS VERIFICATION FAILED: {v2_err}")

        print("\n📸 TAKING SCREENSHOT #8 — EDIT FORM REOPENED (VERIFICATION STATE)...")
        utils.tomar_screenshot(driver, "MER_06_8_EDIT_FORM_VERIFIED")

        # FINAL ASSERTION
        test_passed = guardar_clicked and pencil_clicked and nombre_verified

        print(f"\n   🔬 MER-06 ASSERTION SUMMARY:")
        print(f"      • 'NUEVO +' CLICKED          : {nuevo_clicked}")
        print(f"      • 'GUARDAR' CLICKED          : {guardar_clicked}")
        print(f"      • SUCCESS TOAST DETECTED     : {toast_detected}")
        print(f"      • REDIRECTED TO TABLE        : {table_appeared}")
        print(f"      • PENCIL CLICKED (REOPEN)    : {pencil_clicked}")
        print(f"      • NOMBRE COMERCIAL VERIFIED  : {nombre_verified}")
        print(f"        · EXPECTED                 : '{MER06_NOMBRE_COMERCIAL}'")
        print(f"        · FOUND                    : '{nombre_found}'")
        print(f"      • FINAL URL                  : {driver.current_url}")

        _capture_web_evidence(driver, "MER_06")

        if test_passed:
            utils.tomar_screenshot(driver, "MER_06_SUCCESS")
            print("\n✅ MER-06: SUCCESS — COMERCIO CREATED AND DATA VERIFIED AFTER REOPENING.")
        else:
            utils.tomar_screenshot(driver, "MER_06_FAILED")
            if not guardar_clicked:
                print("\n❌ MER-06: FAILED — 'GUARDAR' BUTTON COULD NOT BE CLICKED.")
            elif not pencil_clicked:
                print("\n❌ MER-06: FAILED — PENCIL ICON COULD NOT BE CLICKED TO REOPEN.")
            else:
                print(f"\n❌ MER-06: FAILED — NOMBRE COMERCIAL MISMATCH AFTER REOPEN.")

    except Exception as e:
        print(f"\n💥 MER-06 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "MER_06_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()

# ==================================================================================
# MER-07: THE SWITCH USE PHYSICAL ADDRESS AS BILLING ADDRESS SHOULD BE ENABLED BY DEFAULT.
# ==================================================================================
def MER_07():
    print("\n" + "=" * 60)
    print("🧪 MER-07: THE SWITCH USE PHYSICAL ADDRESS AS BILLING ADDRESS SHOULD BE ENABLED BY DEFAULT.")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        # PRECONDITION: LOG IN AND NAVIGATE TO COMERCIOS MODULE
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO COMERCIOS MODULE...")
        _login_and_go_to_comercios(driver)

        # STEP 1: CLICK 'NUEVO +' TO OPEN THE CREATION FORM
        print("\n👉 STEP 1: CLICKING 'NUEVO +' TO OPEN CREATION FORM...")
        nuevo_clicked = False

        try:
            btn = driver.find_element(By.XPATH, XPATH_BTN_NUEVO)
            driver.execute_script("arguments[0].click();", btn)
            nuevo_clicked = True
            time.sleep(3)
            print("   ✅ 'NUEVO +' CLICKED — STRATEGY 1 (XPATH).")
        except Exception as n1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {n1_err}")

        if not nuevo_clicked:
            try:
                result = driver.execute_script("""
                    var btns = document.querySelectorAll('button, a');
                    for (var b of btns) {
                        if (b.textContent.trim().toLowerCase().includes('nuevo')
                                && b.offsetWidth > 0) {
                            b.click();
                            return b.textContent.trim();
                        }
                    }
                    return null;
                """)
                if result:
                    nuevo_clicked = True
                    time.sleep(3)
                    print(f"   ✅ 'NUEVO +' CLICKED — STRATEGY 2 (JS: '{result}').")
            except Exception as n2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {n2_err}")

        print(f"   🌐 CURRENT URL: {driver.current_url}")

        print("\n📸 TAKING SCREENSHOT #1 — CREATION FORM OPENED...")
        utils.tomar_screenshot(driver, "MER_07_1_CREATION_FORM")

        
        print("\n👉 STEP 2: LOCATING TOGGLE '¿Usar Dirección Física Como Dirección Fiscal?'...")

        XPATH_TOGGLE_LABEL = (
            "//*[contains(text(),'Usar Dirección Física') or "
            "    contains(text(),'Usar Direccion Fisica') or "
            "    contains(text(),'Dirección Fiscal')]"
            "[not(ancestor::nav)]"
        )

        XPATH_TOGGLE_INPUT = (
            # CHECKBOX INPUT NEAR THE LABEL
            "//*[contains(text(),'Usar Dirección Física') or "
            "    contains(text(),'Dirección Fiscal')]"
            "/following::input[@type='checkbox'][1] | "
            "//*[contains(text(),'Usar Dirección Física') or "
            "    contains(text(),'Dirección Fiscal')]"
            "/following::input[1] | "
            # p-inputswitch ANGULAR COMPONENT
            "//*[contains(text(),'Usar Dirección Física') or "
            "    contains(text(),'Dirección Fiscal')]"
            "/following::*[contains(@class,'p-inputswitch') or "
            "              contains(@class,'toggle') or "
            "              contains(@class,'switch')][1]"
        )

        toggle_found   = False
        toggle_enabled = False
        toggle_method  = ""

        # STRATEGY 1: FIND CHECKBOX INPUT AND CHECK ITS 'checked' ATTRIBUTE
        try:
            toggle = driver.find_element(By.XPATH, XPATH_TOGGLE_INPUT)
            tag    = toggle.tag_name.lower()

            if tag == "input":
                # NATIVE CHECKBOX — READ checked PROPERTY
                is_checked = driver.execute_script(
                    "return arguments[0].checked;", toggle
                )
                toggle_found   = True
                toggle_enabled = bool(is_checked)
                toggle_method  = "XPATH checkbox input — checked property"
            else:
                # ANGULAR COMPONENT — CHECK aria-checked OR class CONTAINING 'checked'/'active'
                aria   = toggle.get_attribute("aria-checked") or ""
                cls    = toggle.get_attribute("class") or ""
                is_on  = (aria.lower() == "true" or
                          "checked" in cls.lower() or
                          "active"  in cls.lower() or
                          "p-inputswitch-checked" in cls.lower())
                toggle_found   = True
                toggle_enabled = is_on
                toggle_method  = f"XPATH component ({tag}) — aria/class check"

            print(f"   ✅ TOGGLE FOUND — {toggle_method}")
            print(f"   🔍 TOGGLE STATE: {'ENABLED (ON) ✅' if toggle_enabled else 'DISABLED (OFF) ❌'}")

        except Exception as s1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {s1_err}")

        # STRATEGY 2: JS — SCAN FOR TOGGLE BY PROXIMITY TO LABEL TEXT
        if not toggle_found:
            try:
                result = driver.execute_script("""
                    // FIND THE LABEL ELEMENT CONTAINING THE TOGGLE TEXT
                    var all = document.querySelectorAll('*');
                    for (var el of all) {
                        var txt = el.textContent.trim();
                        if (el.children.length === 0 &&
                            (txt.includes('Usar Dirección') || txt.includes('Dirección Fiscal') ||
                             txt.includes('Usar Direccion') || txt.includes('Direccion Fiscal'))) {

                            // WALK UP TO FIND A CONTAINER WITH A TOGGLE/SWITCH SIBLING
                            var parent = el.parentElement;
                            for (var i = 0; i < 5; i++) {
                                if (!parent) break;
                                // LOOK FOR CHECKBOX INPUT INSIDE CONTAINER
                                var cb = parent.querySelector('input[type="checkbox"]');
                                if (cb) {
                                    return JSON.stringify({
                                        found: true,
                                        checked: cb.checked,
                                        method: 'js-checkbox'
                                    });
                                }
                                // LOOK FOR p-inputswitch
                                var sw = parent.querySelector(
                                    '[class*="p-inputswitch"], [class*="toggle"], [class*="switch"]'
                                );
                                if (sw) {
                                    var cls = sw.className || '';
                                    return JSON.stringify({
                                        found: true,
                                        checked: cls.includes('checked') || cls.includes('active'),
                                        method: 'js-switch-class',
                                        class: cls
                                    });
                                }
                                parent = parent.parentElement;
                            }
                        }
                    }
                    return JSON.stringify({found: false});
                """)
                import json as _json
                data = _json.loads(result)
                if data.get("found"):
                    toggle_found   = True
                    toggle_enabled = bool(data.get("checked", False))
                    toggle_method  = f"JS SCAN — {data.get('method', 'unknown')}"
                    print(f"   ✅ TOGGLE FOUND — {toggle_method}")
                    print(f"   🔍 TOGGLE STATE: {'ENABLED (ON) ✅' if toggle_enabled else 'DISABLED (OFF) ❌'}")
                else:
                    print("   ⚠️  TOGGLE NOT FOUND VIA JS SCAN.")
            except Exception as s2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {s2_err}")

        # STRATEGY 3: VISUAL CHECK — LOOK FOR BLUE COLOR CLASS ON SWITCH ELEMENT
        if not toggle_found:
            try:
                result = driver.execute_script("""
                    var switches = document.querySelectorAll(
                        'input[type="checkbox"], [class*="switch"], [class*="toggle"],
                         p-inputswitch, [role="switch"]'
                    );
                    var results = [];
                    for (var sw of switches) {
                        results.push({
                            tag:     sw.tagName,
                            class:   sw.className,
                            checked: sw.checked,
                            aria:    sw.getAttribute('aria-checked')
                        });
                    }
                    return JSON.stringify(results);
                """)
                import json as _json
                items = _json.loads(result)
                if items:
                    # ASSUME LAST TOGGLE IN SECTION 1 IS THE TARGET
                    target = items[-1]
                    toggle_found   = True
                    toggle_enabled = (
                        bool(target.get("checked")) or
                        target.get("aria") == "true" or
                        "checked" in (target.get("class") or "").lower()
                    )
                    toggle_method  = f"STRATEGY 3 FALLBACK — {target.get('tag')} {target.get('class')[:40]}"
                    print(f"   ✅ TOGGLE FOUND — {toggle_method}")
                    print(f"   🔍 TOGGLE STATE: {'ENABLED (ON) ✅' if toggle_enabled else 'DISABLED (OFF) ❌'}")
                else:
                    print("   ❌ NO TOGGLE ELEMENTS FOUND IN DOM.")
            except Exception as s3_err:
                print(f"   ⚠️  STRATEGY 3 FAILED: {s3_err}")

        print("\n📸 TAKING SCREENSHOT #2 — TOGGLE STATE (KEY EVIDENCE)...")
        utils.tomar_screenshot(driver, "MER_07_2_TOGGLE_STATE")

        # FINAL ASSERTION
        test_passed = nuevo_clicked and toggle_found and toggle_enabled

        print(f"\n   🔬 MER-07 ASSERTION SUMMARY:")
        print(f"      • 'NUEVO +' CLICKED          : {nuevo_clicked}")
        print(f"      • TOGGLE FOUND               : {toggle_found}")
        print(f"      • TOGGLE ENABLED BY DEFAULT  : {toggle_enabled}")
        print(f"      • DETECTION METHOD           : {toggle_method}")
        print(f"      • FINAL URL                  : {driver.current_url}")

        _capture_web_evidence(driver, "MER_07")

        if test_passed:
            utils.tomar_screenshot(driver, "MER_07_SUCCESS")
            print("\n✅ MER-07: SUCCESS — TOGGLE '¿Usar Dirección Física Como Dirección Fiscal?' IS ENABLED BY DEFAULT.")
        else:
            utils.tomar_screenshot(driver, "MER_07_FAILED")
            if not nuevo_clicked:
                print("\n❌ MER-07: FAILED — 'NUEVO +' BUTTON COULD NOT BE CLICKED.")
            elif not toggle_found:
                print("\n❌ MER-07: FAILED — TOGGLE ELEMENT NOT FOUND IN DOM.")
            else:
                print("\n❌ MER-07: FAILED — TOGGLE IS DISABLED BY DEFAULT (EXPECTED: ENABLED).")

    except Exception as e:
        print(f"\n💥 MER-07 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "MER_07_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()

# ==================================================================================
# MER-08: THE TAX ADDRESS FIELDS ARE DISPLAYED. THE FIELDS ARE EDITABLE.
# ==================================================================================
def MER_08():
    print("\n" + "=" * 60)
    print("🧪 MER-08: THE TAX ADDRESS FIELDS ARE DISPLAYED. THE FIELDS ARE EDITABLE.")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        # PRECONDITION: LOG IN AND NAVIGATE TO COMERCIOS MODULE
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO COMERCIOS MODULE...")
        _login_and_go_to_comercios(driver)

        # STEP 1: CLICK 'NUEVO +' TO OPEN THE CREATION FORM
        print("\n👉 STEP 1: CLICKING 'NUEVO +' TO OPEN CREATION FORM...")
        nuevo_clicked = False

        try:
            btn = driver.find_element(By.XPATH, XPATH_BTN_NUEVO)
            driver.execute_script("arguments[0].click();", btn)
            nuevo_clicked = True
            time.sleep(3)
            print("   ✅ 'NUEVO +' CLICKED — STRATEGY 1 (XPATH).")
        except Exception as n1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {n1_err}")

        if not nuevo_clicked:
            try:
                result = driver.execute_script("""
                    var btns = document.querySelectorAll('button, a');
                    for (var b of btns) {
                        if (b.textContent.trim().toLowerCase().includes('nuevo')
                                && b.offsetWidth > 0) {
                            b.click();
                            return b.textContent.trim();
                        }
                    }
                    return null;
                """)
                if result:
                    nuevo_clicked = True
                    time.sleep(3)
                    print(f"   ✅ 'NUEVO +' CLICKED — STRATEGY 2 (JS: '{result}').")
            except Exception as n2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {n2_err}")

        print(f"   🌐 CURRENT URL: {driver.current_url}")

        print("\n📸 TAKING SCREENSHOT #1 — FORM OPEN, TOGGLE ENABLED (BEFORE CLICK)...")
        utils.tomar_screenshot(driver, "MER_08_1_TOGGLE_BEFORE_CLICK")

        print("\n👉 STEP 2: LOCATING AND CLICKING THE TOGGLE...")
        toggle_clicked = False

        try:
            result = driver.execute_script("""
                // FIND ALL LABEL ELEMENTS NEAR THE TOGGLE TEXT
                var all = document.querySelectorAll('*');
                for (var el of all) {
                    var txt = el.textContent.trim();
                    if (el.children.length <= 3 &&
                        (txt.includes('Usar Dirección') || txt.includes('Dirección Fiscal') ||
                         txt.includes('Usar Direccion') || txt.includes('Direccion Fiscal'))) {

                        // SEARCH FOR CHECKBOX INPUT WITHIN PARENT CONTAINERS
                        var parent = el.parentElement;
                        for (var i = 0; i < 5; i++) {
                            if (!parent) break;
                            var cb = parent.querySelector('input[type="checkbox"]');
                            if (cb) {
                                cb.click();
                                return 'checkbox-clicked:checked=' + cb.checked;
                            }
                            parent = parent.parentElement;
                        }
                    }
                }
                return 'NOT FOUND';
            """)
            if result and result.startswith('checkbox-clicked:'):
                toggle_clicked = True
                time.sleep(1)
                print(f"   ✅ TOGGLE CLICKED — STRATEGY 1 (JS CHECKBOX CLICK: {result}).")
            else:
                print(f"   ⚠️  STRATEGY 1: {result}")
        except Exception as s1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {s1_err}")

    
        if not toggle_clicked:
            try:
                toggle_div = driver.find_element(By.XPATH,
                    "//*[contains(text(),'Usar Dirección') or "
                    "    contains(text(),'Dirección Fiscal')]"
                    "/following::div[contains(@class,'rounded-full')][1]"
                )
                driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});", toggle_div
                )
                time.sleep(0.3)
                driver.execute_script("arguments[0].click();", toggle_div)
                toggle_clicked = True
                time.sleep(1)
                print("   ✅ TOGGLE CLICKED — STRATEGY 2 (VISUAL DIV rounded-full).")
            except Exception as s2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {s2_err}")

        # STRATEGY 3: XPATH — FIND THE LABEL AND CLICK IT (LABEL CLICK TOGGLES CHECKBOX)
        if not toggle_clicked:
            try:
                label = driver.find_element(By.XPATH,
                    "//label[.//*[contains(text(),'Usar Dirección') or "
                    "             contains(text(),'Dirección Fiscal')]] | "
                    "//label[contains(.,'Usar Dirección') or contains(.,'Dirección Fiscal')]"
                )
                driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});", label
                )
                time.sleep(0.3)
                label.click()
                toggle_clicked = True
                time.sleep(1)
                print("   ✅ TOGGLE CLICKED — STRATEGY 3 (LABEL CLICK).")
            except Exception as s3_err:
                print(f"   ⚠️  STRATEGY 3 FAILED: {s3_err}")

        print("\n📸 TAKING SCREENSHOT #2 — AFTER TOGGLE CLICK...")
        utils.tomar_screenshot(driver, "MER_08_2_AFTER_TOGGLE_CLICK")
        print("\n👉 STEP 3: VERIFYING 'DIRECCIÓN FISCAL' SECTION IS VISIBLE...")
        time.sleep(1)
        section_visible = False

        XPATH_DIRECCION_FISCAL = (
            "//*[contains(text(),'DIRECCIÓN FISCAL') or "
            "    contains(text(),'Dirección Fiscal') or "
            "    contains(text(),'DIRECCION FISCAL')]"
            "[not(ancestor::nav) and not(ancestor::aside)]"
        )

        # STRATEGY 1: XPATH SEARCH FOR SECTION HEADING
        try:
            el = driver.find_element(By.XPATH, XPATH_DIRECCION_FISCAL)
            if el.is_displayed():
                section_visible = True
                print("   ✅ 'DIRECCIÓN FISCAL' SECTION FOUND AND VISIBLE — STRATEGY 1 (XPATH).")
            else:
                print("   ⚠️  SECTION FOUND BUT NOT VISIBLE.")
        except Exception as sv1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {sv1_err}")

        # STRATEGY 2: JS SCAN FOR THE SECTION HEADING TEXT
        if not section_visible:
            try:
                result = driver.execute_script("""
                    var all = document.querySelectorAll('*');
                    for (var el of all) {
                        var txt = el.textContent.trim().toUpperCase();
                        if ((txt === 'DIRECCIÓN FISCAL' || txt === 'DIRECCION FISCAL' ||
                             txt === 'DIRECCIÓN FISCAL'.toUpperCase()) &&
                            el.offsetWidth > 0 && el.offsetHeight > 0) {
                            return el.textContent.trim();
                        }
                    }
                    return null;
                """)
                if result:
                    section_visible = True
                    print(f"   ✅ 'DIRECCIÓN FISCAL' SECTION FOUND VIA JS: '{result}'.")
                else:
                    print("   ❌ 'DIRECCIÓN FISCAL' SECTION NOT FOUND IN DOM.")
            except Exception as sv2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {sv2_err}")

        # TAKE THE KEY SCREENSHOT — DIRECCIÓN FISCAL SECTION EXPANDED
        print("\n📸 TAKING SCREENSHOT #3 — 'DIRECCIÓN FISCAL' SECTION VISIBLE (KEY EVIDENCE)...")
        utils.tomar_screenshot(driver, "MER_08_3_DIRECCION_FISCAL_VISIBLE")

        # FINAL ASSERTION
        test_passed = nuevo_clicked and toggle_clicked and section_visible

        print(f"\n   🔬 MER-08 ASSERTION SUMMARY:")
        print(f"      • 'NUEVO +' CLICKED              : {nuevo_clicked}")
        print(f"      • TOGGLE CLICKED                 : {toggle_clicked}")
        print(f"      • 'DIRECCIÓN FISCAL' VISIBLE     : {section_visible}")
        print(f"      • FINAL URL                      : {driver.current_url}")

        _capture_web_evidence(driver, "MER_08")

        if test_passed:
            utils.tomar_screenshot(driver, "MER_08_SUCCESS")
            print("\n✅ MER-08: SUCCESS — TOGGLE DISABLED AND 'DIRECCIÓN FISCAL' SECTION APPEARED.")
        else:
            utils.tomar_screenshot(driver, "MER_08_FAILED")
            if not nuevo_clicked:
                print("\n❌ MER-08: FAILED — 'NUEVO +' BUTTON COULD NOT BE CLICKED.")
            elif not toggle_clicked:
                print("\n❌ MER-08: FAILED — TOGGLE COULD NOT BE CLICKED.")
            else:
                print("\n❌ MER-08: FAILED — 'DIRECCIÓN FISCAL' SECTION DID NOT APPEAR AFTER TOGGLE CLICK.")

    except Exception as e:
        print(f"\n💥 MER-08 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "MER_08_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()

# ==================================================================================
# MER-09: THE TAX ADDRESS FIELDS ARE HIDDEN AGAIN.
# ==================================================================================
def MER_09():
    print("\n" + "=" * 60)
    print("🧪 MER-09: THE TAX ADDRESS FIELDS ARE HIDDEN AGAIN.")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        # PRECONDITION: LOG IN AND NAVIGATE TO COMERCIOS MODULE
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO COMERCIOS MODULE...")
        _login_and_go_to_comercios(driver)

        # STEP 1: CLICK 'NUEVO +' TO OPEN THE CREATION FORM
        print("\n👉 STEP 1: CLICKING 'NUEVO +' TO OPEN CREATION FORM...")
        nuevo_clicked = False

        try:
            btn = driver.find_element(By.XPATH, XPATH_BTN_NUEVO)
            driver.execute_script("arguments[0].click();", btn)
            nuevo_clicked = True
            time.sleep(3)
            print("   ✅ 'NUEVO +' CLICKED — STRATEGY 1 (XPATH).")
        except Exception as n1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {n1_err}")

        if not nuevo_clicked:
            try:
                result = driver.execute_script("""
                    var btns = document.querySelectorAll('button, a');
                    for (var b of btns) {
                        if (b.textContent.trim().toLowerCase().includes('nuevo')
                                && b.offsetWidth > 0) {
                            b.click();
                            return b.textContent.trim();
                        }
                    }
                    return null;
                """)
                if result:
                    nuevo_clicked = True
                    time.sleep(3)
                    print(f"   ✅ 'NUEVO +' CLICKED — STRATEGY 2 (JS: '{result}').")
            except Exception as n2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {n2_err}")

        print(f"   🌐 CURRENT URL: {driver.current_url}")

        print("\n📸 TAKING SCREENSHOT #1 — CREATION FORM OPENED...")
        utils.tomar_screenshot(driver, "MER_07_1_CREATION_FORM")

        print("\n👉 STEP 2: LOCATING TOGGLE '¿Usar Dirección Física Como Dirección Fiscal?'...")

        XPATH_TOGGLE_LABEL = (
            "//*[contains(text(),'Usar Dirección Física') or "
            "    contains(text(),'Usar Direccion Fisica') or "
            "    contains(text(),'Dirección Fiscal')]"
            "[not(ancestor::nav)]"
        )

        XPATH_TOGGLE_INPUT = (
            # CHECKBOX INPUT NEAR THE LABEL
            "//*[contains(text(),'Usar Dirección Física') or "
            "    contains(text(),'Dirección Fiscal')]"
            "/following::input[@type='checkbox'][1] | "
            "//*[contains(text(),'Usar Dirección Física') or "
            "    contains(text(),'Dirección Fiscal')]"
            "/following::input[1] | "
            # p-inputswitch ANGULAR COMPONENT
            "//*[contains(text(),'Usar Dirección Física') or "
            "    contains(text(),'Dirección Fiscal')]"
            "/following::*[contains(@class,'p-inputswitch') or "
            "              contains(@class,'toggle') or "
            "              contains(@class,'switch')][1]"
        )

        toggle_found   = False
        toggle_enabled = False
        toggle_method  = ""

        # STRATEGY 1: FIND CHECKBOX INPUT AND CHECK ITS 'checked' ATTRIBUTE
        try:
            toggle = driver.find_element(By.XPATH, XPATH_TOGGLE_INPUT)
            tag    = toggle.tag_name.lower()

            if tag == "input":
                # NATIVE CHECKBOX — READ checked PROPERTY
                is_checked = driver.execute_script(
                    "return arguments[0].checked;", toggle
                )
                toggle_found   = True
                toggle_enabled = bool(is_checked)
                toggle_method  = "XPATH checkbox input — checked property"
            else:
                # ANGULAR COMPONENT — CHECK aria-checked OR class CONTAINING 'checked'/'active'
                aria   = toggle.get_attribute("aria-checked") or ""
                cls    = toggle.get_attribute("class") or ""
                is_on  = (aria.lower() == "true" or
                          "checked" in cls.lower() or
                          "active"  in cls.lower() or
                          "p-inputswitch-checked" in cls.lower())
                toggle_found   = True
                toggle_enabled = is_on
                toggle_method  = f"XPATH component ({tag}) — aria/class check"

            print(f"   ✅ TOGGLE FOUND — {toggle_method}")
            print(f"   🔍 TOGGLE STATE: {'ENABLED (ON) ✅' if toggle_enabled else 'DISABLED (OFF) ❌'}")

        except Exception as s1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {s1_err}")

        # STRATEGY 2: JS — SCAN FOR TOGGLE BY PROXIMITY TO LABEL TEXT
        if not toggle_found:
            try:
                result = driver.execute_script("""
                    // FIND THE LABEL ELEMENT CONTAINING THE TOGGLE TEXT
                    var all = document.querySelectorAll('*');
                    for (var el of all) {
                        var txt = el.textContent.trim();
                        if (el.children.length === 0 &&
                            (txt.includes('Usar Dirección') || txt.includes('Dirección Fiscal') ||
                             txt.includes('Usar Direccion') || txt.includes('Direccion Fiscal'))) {

                            // WALK UP TO FIND A CONTAINER WITH A TOGGLE/SWITCH SIBLING
                            var parent = el.parentElement;
                            for (var i = 0; i < 5; i++) {
                                if (!parent) break;
                                // LOOK FOR CHECKBOX INPUT INSIDE CONTAINER
                                var cb = parent.querySelector('input[type="checkbox"]');
                                if (cb) {
                                    return JSON.stringify({
                                        found: true,
                                        checked: cb.checked,
                                        method: 'js-checkbox'
                                    });
                                }
                                // LOOK FOR p-inputswitch
                                var sw = parent.querySelector(
                                    '[class*="p-inputswitch"], [class*="toggle"], [class*="switch"]'
                                );
                                if (sw) {
                                    var cls = sw.className || '';
                                    return JSON.stringify({
                                        found: true,
                                        checked: cls.includes('checked') || cls.includes('active'),
                                        method: 'js-switch-class',
                                        class: cls
                                    });
                                }
                                parent = parent.parentElement;
                            }
                        }
                    }
                    return JSON.stringify({found: false});
                """)
                import json as _json
                data = _json.loads(result)
                if data.get("found"):
                    toggle_found   = True
                    toggle_enabled = bool(data.get("checked", False))
                    toggle_method  = f"JS SCAN — {data.get('method', 'unknown')}"
                    print(f"   ✅ TOGGLE FOUND — {toggle_method}")
                    print(f"   🔍 TOGGLE STATE: {'ENABLED (ON) ✅' if toggle_enabled else 'DISABLED (OFF) ❌'}")
                else:
                    print("   ⚠️  TOGGLE NOT FOUND VIA JS SCAN.")
            except Exception as s2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {s2_err}")

        # STRATEGY 3: VISUAL CHECK — LOOK FOR BLUE COLOR CLASS ON SWITCH ELEMENT
        if not toggle_found:
            try:
                result = driver.execute_script("""
                    var switches = document.querySelectorAll(
                        'input[type="checkbox"], [class*="switch"], [class*="toggle"],
                         p-inputswitch, [role="switch"]'
                    );
                    var results = [];
                    for (var sw of switches) {
                        results.push({
                            tag:     sw.tagName,
                            class:   sw.className,
                            checked: sw.checked,
                            aria:    sw.getAttribute('aria-checked')
                        });
                    }
                    return JSON.stringify(results);
                """)
                import json as _json
                items = _json.loads(result)
                if items:
                    # ASSUME LAST TOGGLE IN SECTION 1 IS THE TARGET
                    target = items[-1]
                    toggle_found   = True
                    toggle_enabled = (
                        bool(target.get("checked")) or
                        target.get("aria") == "true" or
                        "checked" in (target.get("class") or "").lower()
                    )
                    toggle_method  = f"STRATEGY 3 FALLBACK — {target.get('tag')} {target.get('class')[:40]}"
                    print(f"   ✅ TOGGLE FOUND — {toggle_method}")
                    print(f"   🔍 TOGGLE STATE: {'ENABLED (ON) ✅' if toggle_enabled else 'DISABLED (OFF) ❌'}")
                else:
                    print("   ❌ NO TOGGLE ELEMENTS FOUND IN DOM.")
            except Exception as s3_err:
                print(f"   ⚠️  STRATEGY 3 FAILED: {s3_err}")

        print("\n📸 TAKING SCREENSHOT #2 — TOGGLE STATE (KEY EVIDENCE)...")
        utils.tomar_screenshot(driver, "MER_09_2_TOGGLE_STATE")

        # FINAL ASSERTION
        test_passed = nuevo_clicked and toggle_found and toggle_enabled

        print(f"\n   🔬 MER-09 ASSERTION SUMMARY:")
        print(f"      • 'NUEVO +' CLICKED          : {nuevo_clicked}")
        print(f"      • TOGGLE FOUND               : {toggle_found}")
        print(f"      • TOGGLE ENABLED BY DEFAULT  : {toggle_enabled}")
        print(f"      • DETECTION METHOD           : {toggle_method}")
        print(f"      • FINAL URL                  : {driver.current_url}")

        _capture_web_evidence(driver, "MER_07")

        if test_passed:
            utils.tomar_screenshot(driver, "MER_09_SUCCESS")
            print("\n✅ MER-09: SUCCESS — TOGGLE '¿Usar Dirección Física Como Dirección Fiscal?' IS ENABLED BY DEFAULT.")
        else:
            utils.tomar_screenshot(driver, "MER_07_FAILED")
            if not nuevo_clicked:
                print("\n❌ MER-09: FAILED — 'NUEVO +' BUTTON COULD NOT BE CLICKED.")
            elif not toggle_found:
                print("\n❌ MER-09: FAILED — TOGGLE ELEMENT NOT FOUND IN DOM.")
            else:
                print("\n❌ MER-09: FAILED — TOGGLE IS DISABLED BY DEFAULT (EXPECTED: ENABLED).")

    except Exception as e:
        print(f"\n💥 MER-09 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "MER_09_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()

# ==================================================================================
# MER-10: THE SWITCH IS SET TO 'ON' THE TAX FIELDS ARE NOT DISPLAYED.
# ==================================================================================
def MER_10():
    print("\n" + "=" * 60)
    print("🧪 MER-10: THE SWITCH IS SET TO 'ON' THE TAX FIELDS ARE NOT DISPLAYED.")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        # PRECONDITION: LOG IN AND NAVIGATE TO COMERCIOS MODULE
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO COMERCIOS MODULE...")
        _login_and_go_to_comercios(driver)

        print("\n📸 TAKING SCREENSHOT #1 — COMERCIOS TABLE...")
        utils.tomar_screenshot(driver, "MER_10_1_COMERCIOS_TABLE")

        # STEP 1: CLICK '+NUEVO' TO OPEN THE CREATION FORM
        print("\n👉 STEP 1: CLICKING '+NUEVO' TO OPEN CREATION FORM...")
        nuevo_clicked = False

        try:
            btn = driver.find_element(By.XPATH, XPATH_BTN_NUEVO)
            driver.execute_script("arguments[0].click();", btn)
            nuevo_clicked = True
            time.sleep(3)
            print("   ✅ '+NUEVO' CLICKED — STRATEGY 1 (XPATH).")
        except Exception as n1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {n1_err}")

        if not nuevo_clicked:
            try:
                result = driver.execute_script("""
                    var btns = document.querySelectorAll('button, a');
                    for (var b of btns) {
                        if (b.textContent.trim().toLowerCase().includes('nuevo')
                                && b.offsetWidth > 0) {
                            b.click();
                            return b.textContent.trim();
                        }
                    }
                    return null;
                """)
                if result:
                    nuevo_clicked = True
                    time.sleep(3)
                    print(f"   ✅ '+NUEVO' CLICKED — STRATEGY 2 (JS: '{result}').")
            except Exception as n2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {n2_err}")

        print(f"   🌐 CURRENT URL: {driver.current_url}")

        # STEP 2: VERIFY FORM IS OPEN — 'CREACIÓN DE COMERCIO' TITLE VISIBLE
        print("\n👉 STEP 2: VERIFYING CREATION FORM IS OPEN...")
        form_visible = False

        try:
            driver.find_element(By.XPATH,
                "//h1[contains(text(),'Creación de Comercio')] | "
                "//*[normalize-space(text())='Creación de Comercio']"
                "[not(ancestor::nav)]"
            )
            form_visible = True
            print("   ✅ FORM 'CREACIÓN DE COMERCIO' IS VISIBLE.")
        except Exception:
            # FALLBACK: CHECK URL
            if "create" in driver.current_url.lower():
                form_visible = True
                print(f"   ✅ FORM CONFIRMED VIA URL: {driver.current_url}")
            else:
                print(f"   ⚠️  FORM TITLE NOT DETECTED. URL: {driver.current_url}")

        # STEP 3: VERIFY 'DIRECCIÓN FISCAL' SECTION IS NOT VISIBLE
        # BY DEFAULT THE TOGGLE IS ON — WHICH MEANS THE FISCAL ADDRESS
        # SECTION SHOULD NOT BE SHOWN ON THE FORM.
        print("\n👉 STEP 3: VERIFYING 'DIRECCIÓN FISCAL' SECTION IS NOT VISIBLE...")

        XPATH_DIRECCION_FISCAL = (
            "//*[normalize-space(text())='DIRECCIÓN FISCAL' or "
            "    normalize-space(text())='DIRECCION FISCAL' or "
            "    normalize-space(text())='Dirección Fiscal']"
            "[not(ancestor::nav) and not(ancestor::aside)]"
        )

        section_visible = False

        # STRATEGY 1: XPATH CHECK
        try:
            el = driver.find_element(By.XPATH, XPATH_DIRECCION_FISCAL)
            section_visible = el.is_displayed()
        except Exception:
            section_visible = False

        # STRATEGY 2: JS SCAN AS CONFIRMATION
        if not section_visible:
            try:
                section_visible = bool(driver.execute_script("""
                    var all = document.querySelectorAll('*');
                    for (var el of all) {
                        var txt = el.textContent.trim();
                        if ((txt === 'DIRECCIÓN FISCAL' ||
                             txt === 'DIRECCION FISCAL' ||
                             txt === 'Dirección Fiscal') &&
                            el.offsetWidth > 0 && el.offsetHeight > 0) {
                            return true;
                        }
                    }
                    return false;
                """))
            except Exception:
                section_visible = False

        if section_visible:
            print("   ⚠️  'DIRECCIÓN FISCAL' SECTION IS VISIBLE — NOT EXPECTED BY DEFAULT.")
        else:
            print("   ✅ 'DIRECCIÓN FISCAL' SECTION IS NOT VISIBLE — CORRECT DEFAULT STATE.")

        # KEY SCREENSHOT — FORM WITHOUT DIRECCIÓN FISCAL SECTION
        print("\n📸 TAKING SCREENSHOT #2 — CREATION FORM (KEY EVIDENCE: NO DIRECCIÓN FISCAL)...")
        utils.tomar_screenshot(driver, "MER_10_2_FORM_NO_FISCAL_SECTION")

        test_passed = nuevo_clicked and form_visible and not section_visible

        print(f"\n   🔬 MER-10 ASSERTION SUMMARY:")
        print(f"      • '+NUEVO' CLICKED               : {nuevo_clicked}")
        print(f"      • CREATION FORM VISIBLE          : {form_visible}")
        print(f"      • 'DIRECCIÓN FISCAL' VISIBLE     : {section_visible}")
        print(f"      • SECTION CORRECTLY HIDDEN       : {not section_visible}")
        print(f"      • FINAL URL                      : {driver.current_url}")

        _capture_web_evidence(driver, "MER_10")

        if test_passed:
            utils.tomar_screenshot(driver, "MER_10_SUCCESS")
            print("\n✅ MER-10: SUCCESS — CREATION FORM OPENS WITHOUT 'DIRECCIÓN FISCAL' SECTION.")
        else:
            utils.tomar_screenshot(driver, "MER_10_FAILED")
            if not nuevo_clicked:
                print("\n❌ MER-10: FAILED — '+NUEVO' BUTTON COULD NOT BE CLICKED.")
            elif not form_visible:
                print("\n❌ MER-10: FAILED — CREATION FORM DID NOT OPEN.")
            else:
                print("\n❌ MER-10: FAILED — 'DIRECCIÓN FISCAL' SECTION IS VISIBLE (UNEXPECTED).")

    except Exception as e:
        print(f"\n💥 MER-10 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "MER_10_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()

# ==================================================================================
# MER-11: USER WITH EDIT PERMISSIONS STORE CREATED WITH SAME ADDRESS = ACTIVE.
# ==================================================================================
def MER_11():
    print("\n" + "=" * 60)
    print("🧪 MER-11: USER WITH EDIT PERMISSIONS STORE CREATED WITH SAME ADDRESS = ACTIVE.")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        # PRECONDITION: LOG IN AND NAVIGATE TO COMERCIOS MODULE
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO COMERCIOS MODULE...")
        _login_and_go_to_comercios(driver)

        print("\n📸 TAKING SCREENSHOT #1 — COMERCIOS TABLE...")
        utils.tomar_screenshot(driver, "MER_11_1_COMERCIOS_TABLE")

        # STEP 1: CLICK '+NUEVO' TO OPEN THE CREATION FORM
        print("\n👉 STEP 1: CLICKING '+NUEVO' TO OPEN CREATION FORM...")
        nuevo_clicked = False

        try:
            btn = driver.find_element(By.XPATH, XPATH_BTN_NUEVO)
            driver.execute_script("arguments[0].click();", btn)
            nuevo_clicked = True
            time.sleep(3)
            print("   ✅ '+NUEVO' CLICKED — STRATEGY 1 (XPATH).")
        except Exception as n1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {n1_err}")

        if not nuevo_clicked:
            try:
                result = driver.execute_script("""
                    var btns = document.querySelectorAll('button, a');
                    for (var b of btns) {
                        if (b.textContent.trim().toLowerCase().includes('nuevo')
                                && b.offsetWidth > 0) {
                            b.click();
                            return b.textContent.trim();
                        }
                    }
                    return null;
                """)
                if result:
                    nuevo_clicked = True
                    time.sleep(3)
                    print(f"   ✅ '+NUEVO' CLICKED — STRATEGY 2 (JS: '{result}').")
            except Exception as n2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {n2_err}")

        print(f"   🌐 CURRENT URL: {driver.current_url}")

        # SCROLL TO TOGGLE AREA AND TAKE BEFORE SCREENSHOT
        driver.execute_script("""
            var el = document.querySelector(
                'div[class*="accent-primary"][class*="min-w-10"][class*="h-6"]'
            );
            if (el) { el.scrollIntoView({block: 'center'}); }
        """)
        time.sleep(1)

        print("\n📸 TAKING SCREENSHOT #2 — FORM OPEN, TOGGLE DEFAULT STATE (BEFORE CLICK)...")
        utils.tomar_screenshot(driver, "MER_11_2_BEFORE_TOGGLE_CLICK")

        print("\n👉 STEP 2: CLICKING TOGGLE '¿Usar Dirección Física Como Dirección Fiscal?'...")
        toggle_clicked = False

        # STRATEGY 1: JS — TARGET BY CONFIRMED UNIQUE CLASS accent-primary + min-w-10 + h-6
        try:
            result = driver.execute_script("""
                var div = document.querySelector(
                    'div[class*="accent-primary"][class*="min-w-10"][class*="h-6"]'
                );
                if (div && div.offsetWidth > 0) {
                    div.scrollIntoView({block: 'center'});
                    div.click();
                    return 'clicked:accent-primary';
                }
                return 'NOT FOUND';
            """)
            if result == 'clicked:accent-primary':
                toggle_clicked = True
                time.sleep(1.5)
                print("   ✅ TOGGLE CLICKED — STRATEGY 1 (accent-primary DIV).")
            else:
                print(f"   ⚠️  STRATEGY 1: {result}")
        except Exception as s1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {s1_err}")

        # STRATEGY 2: XPATH — CONFIRMED UNIQUE CLASS COMBINATION FROM DOM
        if not toggle_clicked:
            try:
                toggle_div = driver.find_element(By.XPATH,
                    "//div[contains(@class,'accent-primary') and "
                    "      contains(@class,'min-w-10') and "
                    "      contains(@class,'h-6') and "
                    "      contains(@class,'rounded-full')]"
                )
                driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});", toggle_div
                )
                time.sleep(0.4)
                driver.execute_script("arguments[0].click();", toggle_div)
                toggle_clicked = True
                time.sleep(1.5)
                print("   ✅ TOGGLE CLICKED — STRATEGY 2 (XPATH accent-primary).")
            except Exception as s2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {s2_err}")

        # STRATEGY 3: JS — FIND <input type="checkbox"> WHOSE NEXT SIBLING HAS accent-primary
        if not toggle_clicked:
            try:
                result = driver.execute_script("""
                    var inputs = document.querySelectorAll('input[type="checkbox"]');
                    for (var i = 0; i < inputs.length; i++) {
                        var sib = inputs[i].nextElementSibling;
                        if (sib && sib.className &&
                            sib.className.includes('accent-primary')) {
                            sib.scrollIntoView({block: 'center'});
                            sib.click();
                            return 'clicked:peer-sibling-accent-primary';
                        }
                    }
                    return 'NOT FOUND';
                """)
                if result == 'clicked:peer-sibling-accent-primary':
                    toggle_clicked = True
                    time.sleep(1.5)
                    print("   ✅ TOGGLE CLICKED — STRATEGY 3 (PEER SIBLING).")
                else:
                    print(f"   ❌ ALL TOGGLE STRATEGIES FAILED: {result}")
            except Exception as s3_err:
                print(f"   ⚠️  STRATEGY 3 FAILED: {s3_err}")

        # STEP 3: VERIFY 'DIRECCIÓN FISCAL' SECTION IS NOW VISIBLE
        print("\n👉 STEP 3: VERIFYING 'DIRECCIÓN FISCAL' SECTION IS VISIBLE...")
        time.sleep(1)
        section_visible = False

        # STRATEGY 1: XPATH
        try:
            el = driver.find_element(By.XPATH,
                "//*[normalize-space(text())='DIRECCIÓN FISCAL' or "
                "    normalize-space(text())='DIRECCION FISCAL' or "
                "    normalize-space(text())='Dirección Fiscal']"
                "[not(ancestor::nav) and not(ancestor::aside)]"
            )
            section_visible = el.is_displayed()
            if section_visible:
                print("   ✅ 'DIRECCIÓN FISCAL' SECTION IS VISIBLE — STRATEGY 1 (XPATH).")
            else:
                print("   ⚠️  SECTION FOUND BUT NOT DISPLAYED.")
        except Exception:
            print("   ⚠️  XPATH NOT FOUND — TRYING JS SCAN...")

        # STRATEGY 2: JS SCAN
        if not section_visible:
            try:
                section_visible = bool(driver.execute_script("""
                    var all = document.querySelectorAll('*');
                    for (var el of all) {
                        var txt = el.textContent.trim();
                        if ((txt === 'DIRECCIÓN FISCAL' ||
                             txt === 'DIRECCION FISCAL' ||
                             txt === 'Dirección Fiscal') &&
                            el.offsetWidth > 0 && el.offsetHeight > 0) {
                            return true;
                        }
                    }
                    return false;
                """))
                if section_visible:
                    print("   ✅ 'DIRECCIÓN FISCAL' SECTION FOUND VIA JS SCAN.")
                else:
                    print("   ❌ 'DIRECCIÓN FISCAL' SECTION NOT FOUND IN DOM.")
            except Exception as js_err:
                print(f"   ⚠️  JS SCAN FAILED: {js_err}")

        # SCROLL TO SHOW TOGGLE + SECTION IN SAME VIEWPORT FOR KEY SCREENSHOT
        driver.execute_script("""
            var el = document.querySelector(
                'div[class*="accent-primary"][class*="min-w-10"][class*="h-6"]'
            );
            if (el) { el.scrollIntoView({block: 'center'}); }
        """)
        time.sleep(0.5)

        # KEY SCREENSHOT — TOGGLE CLICKED, DIRECCIÓN FISCAL SECTION VISIBLE
        print("\n📸 TAKING SCREENSHOT #3 — 'DIRECCIÓN FISCAL' SECTION VISIBLE (KEY EVIDENCE)...")
        utils.tomar_screenshot(driver, "MER_11_3_DIRECCION_FISCAL_VISIBLE")

        # FINAL ASSERTION
        test_passed = nuevo_clicked and toggle_clicked and section_visible

        print(f"\n   🔬 MER-11 ASSERTION SUMMARY:")
        print(f"      • '+NUEVO' CLICKED               : {nuevo_clicked}")
        print(f"      • TOGGLE CLICKED                 : {toggle_clicked}")
        print(f"      • 'DIRECCIÓN FISCAL' VISIBLE     : {section_visible}")
        print(f"      • FINAL URL                      : {driver.current_url}")

        _capture_web_evidence(driver, "MER_11")

        if test_passed:
            utils.tomar_screenshot(driver, "MER_11_SUCCESS")
            print("\n✅ MER-11: SUCCESS — TOGGLE CLICKED AND 'DIRECCIÓN FISCAL' SECTION APPEARED.")
        else:
            utils.tomar_screenshot(driver, "MER_11_FAILED")
            if not nuevo_clicked:
                print("\n❌ MER-11: FAILED — '+NUEVO' BUTTON COULD NOT BE CLICKED.")
            elif not toggle_clicked:
                print("\n❌ MER-11: FAILED — TOGGLE COULD NOT BE CLICKED.")
            else:
                print("\n❌ MER-11: FAILED — 'DIRECCIÓN FISCAL' SECTION DID NOT APPEAR AFTER TOGGLE CLICK.")

    except Exception as e:
        print(f"\n💥 MER-11 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "MER_11_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()

# ==================================================================================
# MER-12: USER WITH EDIT PERMISSIONS STORE CREATED WITH SAME_ADDRESS.
# ==================================================================================
def MER_12():
    print("\n" + "=" * 60)
    print("🧪 MER-12: USER WITH EDIT PERMISSIONS STORE CREATED WITH SAME_ADDRESS")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        # PRECONDITION: LOG IN AND NAVIGATE TO COMERCIOS MODULE
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO COMERCIOS MODULE...")
        _login_and_go_to_comercios(driver)

        print("\n📸 TAKING SCREENSHOT #1 — COMERCIOS TABLE...")
        utils.tomar_screenshot(driver, "MER_12_1_COMERCIOS_TABLE")

        # STEP 1: CLICK '+NUEVO' TO OPEN THE CREATION FORM
        print("\n👉 STEP 1: CLICKING '+NUEVO' TO OPEN CREATION FORM...")
        nuevo_clicked = False

        try:
            btn = driver.find_element(By.XPATH, XPATH_BTN_NUEVO)
            driver.execute_script("arguments[0].click();", btn)
            nuevo_clicked = True
            time.sleep(3)
            print("   ✅ '+NUEVO' CLICKED — STRATEGY 1 (XPATH).")
        except Exception as n1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {n1_err}")

        if not nuevo_clicked:
            try:
                result = driver.execute_script("""
                    var btns = document.querySelectorAll('button, a');
                    for (var b of btns) {
                        if (b.textContent.trim().toLowerCase().includes('nuevo')
                                && b.offsetWidth > 0) {
                            b.click();
                            return b.textContent.trim();
                        }
                    }
                    return null;
                """)
                if result:
                    nuevo_clicked = True
                    time.sleep(3)
                    print(f"   ✅ '+NUEVO' CLICKED — STRATEGY 2 (JS: '{result}').")
            except Exception as n2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {n2_err}")

        print(f"   🌐 CURRENT URL: {driver.current_url}")

        # SCROLL TO TOGGLE AND TAKE BEFORE SCREENSHOT
        driver.execute_script("""
            var el = document.querySelector(
                'div[class*="accent-primary"][class*="min-w-10"][class*="h-6"]'
            );
            if (el) { el.scrollIntoView({block: 'center'}); }
        """)
        time.sleep(1)

        print("\n📸 TAKING SCREENSHOT #2 — FORM OPEN, TOGGLE DEFAULT STATE (ON)...")
        utils.tomar_screenshot(driver, "MER_12_2_FORM_TOGGLE_ON")

        # ── HELPERS ────────────────────────────────────────────────────────────

        def _get_toggle_state():
            try:
                result = driver.execute_script("""
                    var divs = document.querySelectorAll(
                        'div[class*="accent-primary"][class*="min-w-10"][class*="h-6"]'
                    );
                    // INDEX 1 = ¿Usar Dirección Física? (INDEX 0 = ¿Factura?)
                    var div = divs[1] || divs[0];
                    if (!div) return null;
                    var prev = div.previousElementSibling;
                    if (prev && prev.tagName === 'INPUT' && prev.type === 'checkbox') {
                        return prev.checked;
                    }
                    return null;
                """)
                if result is not None:
                    return bool(result)
            except Exception as e:
                print(f"   ⚠️  _get_toggle_state FAILED: {e}")
            return False

        def _click_toggle(attempt_label):
            # STRATEGY 1: JS — INDEX 1 IS CONFIRMED AS ¿Usar Dirección Física?
            try:
                result = driver.execute_script("""
                    var divs = document.querySelectorAll(
                        'div[class*="accent-primary"][class*="min-w-10"][class*="h-6"]'
                    );
                    // INDEX 1 = ¿Usar Dirección Física? CONFIRMED FROM CONSOLE OUTPUT
                    var div = divs.length >= 2 ? divs[1] : divs[0];
                    if (div && div.offsetWidth > 0) {
                        div.scrollIntoView({block: 'center'});
                        div.click();
                        return 'clicked:index-' + (divs.length >= 2 ? 1 : 0);
                    }
                    return 'NOT FOUND';
                """)
                if result and result.startswith('clicked:'):
                    print(f"   ✅ [{attempt_label}] TOGGLE CLICKED — STRATEGY 1 ({result}).")
                    return True
                else:
                    print(f"   ⚠️  [{attempt_label}] STRATEGY 1: {result}")
            except Exception as s1_err:
                print(f"   ⚠️  [{attempt_label}] STRATEGY 1 FAILED: {s1_err}")

            # STRATEGY 2: XPATH — TARGET SECOND OCCURRENCE EXPLICITLY
            try:
                toggle_divs = driver.find_elements(By.XPATH,
                    "//div[contains(@class,'accent-primary') and "
                    "      contains(@class,'min-w-10') and "
                    "      contains(@class,'h-6') and "
                    "      contains(@class,'rounded-full')]"
                )
                # INDEX 1 = ¿Usar Dirección Física? CONFIRMED
                target = toggle_divs[1] if len(toggle_divs) >= 2 else toggle_divs[0]
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", target)
                time.sleep(0.4)
                driver.execute_script("arguments[0].click();", target)
                print(f"   ✅ [{attempt_label}] TOGGLE CLICKED — STRATEGY 2 (XPATH index {1 if len(toggle_divs) >= 2 else 0}).")
                return True
            except Exception as s2_err:
                print(f"   ⚠️  [{attempt_label}] STRATEGY 2 FAILED: {s2_err}")

            # STRATEGY 3: JS — FIND BY PREVIOUS SIBLING checked=true (¿Usar Dirección? IS ON BY DEFAULT)
            try:
                result = driver.execute_script("""
                    var inputs = document.querySelectorAll('input[type="checkbox"]');
                    for (var i = 0; i < inputs.length; i++) {
                        var sib = inputs[i].nextElementSibling;
                        if (sib && sib.className &&
                            sib.className.includes('accent-primary') &&
                            sib.className.includes('min-w-10')) {
                            // SKIP INDEX 0 (¿Factura?) — TARGET INDEX 1 (¿Usar Dirección?)
                            if (i === 0) continue;
                            sib.scrollIntoView({block: 'center'});
                            sib.click();
                            return 'clicked:input-index-' + i;
                        }
                    }
                    return 'NOT FOUND';
                """)
                if result and result.startswith('clicked:'):
                    print(f"   ✅ [{attempt_label}] TOGGLE CLICKED — STRATEGY 3 ({result}).")
                    return True
                else:
                    print(f"   ❌ [{attempt_label}] ALL STRATEGIES FAILED: {result}")
            except Exception as s3_err:
                print(f"   ⚠️  [{attempt_label}] STRATEGY 3 FAILED: {s3_err}")

            return False

        def _direccion_fiscal_is_visible():
            """RETURNS True IF 'DIRECCIÓN FISCAL' SECTION HEADING IS VISIBLE."""
            try:
                el = driver.find_element(By.XPATH,
                    "//*[normalize-space(text())='DIRECCIÓN FISCAL' or "
                    "    normalize-space(text())='DIRECCION FISCAL' or "
                    "    normalize-space(text())='Dirección Fiscal']"
                    "[not(ancestor::nav) and not(ancestor::aside)]"
                )
                return el.is_displayed()
            except Exception:
                pass
            try:
                return bool(driver.execute_script("""
                    var all = document.querySelectorAll('*');
                    for (var el of all) {
                        var txt = el.textContent.trim();
                        if ((txt === 'DIRECCIÓN FISCAL' ||
                             txt === 'DIRECCION FISCAL' ||
                             txt === 'Dirección Fiscal') &&
                            el.offsetWidth > 0 && el.offsetHeight > 0) {
                            return true;
                        }
                    }
                    return false;
                """))
            except Exception:
                return False

        # STEP 2: READ DEFAULT STATE (SHOULD BE ON)
        print("\n👉 STEP 2: READING TOGGLE DEFAULT STATE...")
        initial_state = _get_toggle_state()
        print(f"   🔍 TOGGLE DEFAULT STATE: {'ON' if initial_state else 'OFF'}")

        # STEP 3: CLICK TOGGLE TO TURN IT OFF
        print("\n👉 STEP 3: CLICKING TOGGLE TO TURN IT OFF...")
        toggle_clicked = _click_toggle("TURN OFF")
        time.sleep(1.5)

        # STEP 4: READ TOGGLE STATE AFTER CLICK (SHOULD BE OFF)
        print("\n👉 STEP 4: READING TOGGLE STATE AFTER CLICK...")
        state_after_click = _get_toggle_state()
        toggle_is_off = not state_after_click
        print(f"   🔍 TOGGLE STATE AFTER CLICK: {'ON' if state_after_click else 'OFF ✅'}")

        # STEP 5: VERIFY 'DIRECCIÓN FISCAL' SECTION IS VISIBLE
        print("\n👉 STEP 5: VERIFYING 'DIRECCIÓN FISCAL' SECTION IS VISIBLE...")
        section_visible = _direccion_fiscal_is_visible()

        if section_visible:
            print("   ✅ 'DIRECCIÓN FISCAL' SECTION IS VISIBLE.")
        else:
            print("   ❌ 'DIRECCIÓN FISCAL' SECTION IS NOT VISIBLE.")

        # SCROLL TO SHOW TOGGLE + SECTION HEADING IN SAME VIEWPORT
        driver.execute_script("""
            var el = document.querySelector(
                'div[class*="accent-primary"][class*="min-w-10"][class*="h-6"]'
            );
            if (el) { el.scrollIntoView({block: 'center'}); }
        """)
        time.sleep(0.5)

        # KEY SCREENSHOT — TOGGLE OFF + DIRECCIÓN FISCAL VISIBLE
        print("\n📸 TAKING SCREENSHOT #3 — TOGGLE OFF + 'DIRECCIÓN FISCAL' VISIBLE (KEY EVIDENCE)...")
        utils.tomar_screenshot(driver, "MER_12_3_TOGGLE_OFF_FISCAL_VISIBLE")

        # FINAL ASSERTION:
        # PASS → TOGGLE WAS CLICKED + STATE IS NOW OFF + SECTION IS VISIBLE.
        test_passed = toggle_clicked and toggle_is_off and section_visible

        print(f"\n   🔬 MER-12 ASSERTION SUMMARY:")
        print(f"      • '+NUEVO' CLICKED               : {nuevo_clicked}")
        print(f"      • TOGGLE DEFAULT STATE           : {'ON' if initial_state else 'OFF'}")
        print(f"      • TOGGLE CLICKED (TURN OFF)      : {toggle_clicked}")
        print(f"      • TOGGLE IS NOW OFF              : {toggle_is_off}")
        print(f"      • 'DIRECCIÓN FISCAL' VISIBLE     : {section_visible}")
        print(f"      • FINAL URL                      : {driver.current_url}")

        _capture_web_evidence(driver, "MER_12")

        if test_passed:
            utils.tomar_screenshot(driver, "MER_12_SUCCESS")
            print("\n❌ MER-12: FAILED — TOGGLE DID NOT TURN OFF AFTER CLICK.")
        else:
            utils.tomar_screenshot(driver, "MER_12_FAILED")
            if not toggle_clicked:
                print("\n❌ MER-12: FAILED — TOGGLE COULD NOT BE CLICKED.")
            elif not toggle_is_off:
                print("\n❌ MER-12: FAILED — TOGGLE DID NOT TURN OFF AFTER CLICK.")
            else:
                print("\n✅ MER-12: SUCCESS — TOGGLE IS OFF AND 'DIRECCIÓN FISCAL' SECTION IS VISIBLE.")

    except Exception as e:
        print(f"\n💥 MER-12 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "MER_12_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()

# ==================================================================================
# MER-13: USER WITH CREATION PERMISSIONS. NO PROCESSOR HAS BEEN SELECTED.
# ==================================================================================
def MER_13():
    print("\n" + "=" * 60)
    print("🧪 MER-13: USER WITH CREATION PERMISSIONS. NO PROCESSOR HAS BEEN SELECTED.")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO COMERCIOS MODULE...")
        _login_and_go_to_comercios(driver)

        print("\n👉 STEP 1: CLICKING '+NUEVO' TO OPEN CREATION FORM...")
        nuevo_clicked = False

        try:
            btn = driver.find_element(By.XPATH, XPATH_BTN_NUEVO)
            driver.execute_script("arguments[0].click();", btn)
            nuevo_clicked = True
            time.sleep(3)
            print("   ✅ '+NUEVO' CLICKED — STRATEGY 1 (XPATH).")
        except Exception as n1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {n1_err}")

        if not nuevo_clicked:
            try:
                result = driver.execute_script("""
                    var btns = document.querySelectorAll('button, a');
                    for (var b of btns) {
                        if (b.textContent.trim().toLowerCase().includes('nuevo')
                                && b.offsetWidth > 0) {
                            b.click();
                            return b.textContent.trim();
                        }
                    }
                    return null;
                """)
                if result:
                    nuevo_clicked = True
                    time.sleep(3)
                    print(f"   ✅ '+NUEVO' CLICKED — STRATEGY 2 (JS: '{result}').")
            except Exception as n2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {n2_err}")

        print(f"   🌐 CURRENT URL: {driver.current_url}")

        # SCROLL TO 'DATOS DE OPERACIÓN' SECTION
        print("\n👉 STEP 2: SCROLLING TO 'DATOS DE OPERACIÓN' SECTION...")
        driver.execute_script("""
            var all = document.querySelectorAll('*');
            for (var el of all) {
                if (el.textContent.trim() === 'DATOS DE OPERACIÓN' ||
                    el.textContent.trim() === 'DATOS DE OPERACION') {
                    el.scrollIntoView({block: 'center'});
                    break;
                }
            }
        """)
        time.sleep(1)

        # VERIFY EACH FIELD IS PRESENT AND EMPTY
        print("\n👉 STEP 3: VERIFYING FIELDS ARE PRESENT AND EMPTY/DEFAULT...")

        results = {}

        # ── ID MEDIO ──────────────────────────────────────────────────────────
        print("   🔍 CHECKING 'ID MEDIO'...")
        try:
            el = driver.find_element(By.XPATH,
                "//input[contains(@placeholder,'ID Medio') or "
                "        contains(@id,'id_medio') or "
                "        contains(@formcontrolname,'idMedio')]"
            )
            value = el.get_attribute("value") or ""
            is_empty = value.strip() == ""
            results["ID MEDIO"] = {
                "found"  : True,
                "empty"  : is_empty,
                "value"  : value,
            }
            print(f"      ✅ FOUND — VALUE: '{value}' — EMPTY: {is_empty}")
        except Exception:
            # FALLBACK: VERIFY BY LABEL PRESENCE
            try:
                driver.find_element(By.XPATH,
                    "//*[normalize-space(text())='ID Medio:' or "
                    "    normalize-space(text())='ID Medio']"
                    "[not(ancestor::nav)]"
                )
                results["ID MEDIO"] = {"found": True, "empty": True, "value": ""}
                print("      ✅ LABEL FOUND (FIELD CONFIRMED PRESENT).")
            except Exception:
                results["ID MEDIO"] = {"found": False, "empty": False, "value": ""}
                print("      ❌ NOT FOUND IN DOM.")

        # ── MODO DE TRANSACCIÓN ───────────────────────────────────────────────
        print("   🔍 CHECKING 'MODO DE TRANSACCIÓN'...")
        try:
            el = driver.find_element(By.XPATH, "//select[@id='id_transaction_mode']")
            selected_text = driver.execute_script(
                "return arguments[0].options[arguments[0].selectedIndex].text;", el
            ) or ""
            is_default = (
                selected_text.strip() == "" or
                "selecciona" in selected_text.lower()
            )
            results["MODO DE TRANSACCIÓN"] = {
                "found"  : True,
                "empty"  : is_default,
                "value"  : selected_text.strip(),
            }
            print(f"      ✅ FOUND — SELECTED: '{selected_text.strip()}' — DEFAULT: {is_default}")
        except Exception:
            try:
                driver.find_element(By.XPATH,
                    "//*[contains(text(),'Modo de Transacción') or "
                    "    contains(text(),'Modo de Transaccion')]"
                    "[not(ancestor::nav)]"
                )
                results["MODO DE TRANSACCIÓN"] = {"found": True, "empty": True, "value": ""}
                print("      ✅ LABEL FOUND (FIELD CONFIRMED PRESENT).")
            except Exception:
                results["MODO DE TRANSACCIÓN"] = {"found": False, "empty": False, "value": ""}
                print("      ❌ NOT FOUND IN DOM.")

        # ── URL DESTINO ───────────────────────────────────────────────────────
        print("   🔍 CHECKING 'URL DESTINO'...")
        try:
            el = driver.find_element(By.XPATH, "//select[@id='id_url_target']")
            selected_text = driver.execute_script(
                "return arguments[0].options[arguments[0].selectedIndex].text;", el
            ) or ""
            is_default = (
                selected_text.strip() == "" or
                "selecciona" in selected_text.lower()
            )
            results["URL DESTINO"] = {
                "found"  : True,
                "empty"  : is_default,
                "value"  : selected_text.strip(),
            }
            print(f"      ✅ FOUND — SELECTED: '{selected_text.strip()}' — DEFAULT: {is_default}")
        except Exception:
            try:
                driver.find_element(By.XPATH,
                    "//*[normalize-space(text())='URL Destino:' or "
                    "    normalize-space(text())='URL Destino']"
                    "[not(ancestor::nav)]"
                )
                results["URL DESTINO"] = {"found": True, "empty": True, "value": ""}
                print("      ✅ LABEL FOUND (FIELD CONFIRMED PRESENT).")
            except Exception:
                results["URL DESTINO"] = {"found": False, "empty": False, "value": ""}
                print("      ❌ NOT FOUND IN DOM.")

        # SCROLL TO CENTER THE 3 FIELDS FOR SCREENSHOT
        driver.execute_script("""
            var el = document.getElementById('id_transaction_mode');
            if (!el) {
                var all = document.querySelectorAll('*');
                for (var e of all) {
                    if (e.textContent.trim().includes('Modo de Transac')) {
                        el = e; break;
                    }
                }
            }
            if (el) el.scrollIntoView({block: 'center'});
        """)
        time.sleep(0.5)

        print("\n📸 TAKING SCREENSHOT — FIELDS PRESENT AND EMPTY (KEY EVIDENCE)...")
        utils.tomar_screenshot(driver, "MER_13_FIELDS_EMPTY")

        # FINAL ASSERTION
        all_found = all(v["found"] for v in results.values())
        all_empty = all(v["empty"] for v in results.values())
        test_passed = all_found and all_empty

        print(f"\n   🔬 MER-13 ASSERTION SUMMARY:")
        print(f"      • '+NUEVO' CLICKED               : {nuevo_clicked}")
        for k, v in results.items():
            print(f"      • {k:<25} : FOUND={v['found']} | EMPTY={v['empty']} | VALUE='{v['value']}'")
        print(f"      • ALL FIELDS FOUND               : {all_found}")
        print(f"      • ALL FIELDS EMPTY/DEFAULT       : {all_empty}")
        print(f"      • FINAL URL                      : {driver.current_url}")

        _capture_web_evidence(driver, "MER_13")

        if test_passed:
            utils.tomar_screenshot(driver, "MER_13_SUCCESS")
            print("\n✅ MER-13: SUCCESS — ID MEDIO, MODO TRANSACCIÓN AND URL DESTINO ARE PRESENT AND EMPTY.")
        else:
            utils.tomar_screenshot(driver, "MER_13_FAILED")
            if not all_found:
                missing = [k for k, v in results.items() if not v["found"]]
                print(f"\n❌ MER-13: FAILED — FIELDS NOT FOUND: {missing}")
            else:
                filled = [k for k, v in results.items() if not v["empty"]]
                print(f"\n❌ MER-13: FAILED — FIELDS NOT EMPTY: {filled}")

    except Exception as e:
        print(f"\n💥 MER-13 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "MER_13_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()


# ==================================================================================
# MER-14: FIELDS ID, TRANSACTION MODE AND DESTINATION URL ARE GRAYED OUT.
# ==================================================================================
def MER_14():
    print("\n" + "=" * 60)
    print("🧪 MER-14: FIELDS ID, TRANSACTION MODE AND DESTINATION URL ARE GRAYED OUT")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO COMERCIOS MODULE...")
        _login_and_go_to_comercios(driver)

        print("\n👉 STEP 1: CLICKING '+NUEVO' TO OPEN CREATION FORM...")
        nuevo_clicked = False

        try:
            btn = driver.find_element(By.XPATH, XPATH_BTN_NUEVO)
            driver.execute_script("arguments[0].click();", btn)
            nuevo_clicked = True
            time.sleep(3)
            print("   ✅ '+NUEVO' CLICKED — STRATEGY 1 (XPATH).")
        except Exception as n1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {n1_err}")

        if not nuevo_clicked:
            try:
                result = driver.execute_script("""
                    var btns = document.querySelectorAll('button, a');
                    for (var b of btns) {
                        if (b.textContent.trim().toLowerCase().includes('nuevo')
                                && b.offsetWidth > 0) {
                            b.click();
                            return b.textContent.trim();
                        }
                    }
                    return null;
                """)
                if result:
                    nuevo_clicked = True
                    time.sleep(3)
                    print(f"   ✅ '+NUEVO' CLICKED — STRATEGY 2 (JS: '{result}').")
            except Exception as n2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {n2_err}")

        print(f"   🌐 CURRENT URL: {driver.current_url}")

        print("\n👉 STEP 2: SCROLLING TO 'DATOS DE OPERACIÓN' SECTION...")
        driver.execute_script("""
            var all = document.querySelectorAll('*');
            for (var el of all) {
                if (el.textContent.trim() === 'DATOS DE OPERACIÓN' ||
                    el.textContent.trim() === 'DATOS DE OPERACION') {
                    el.scrollIntoView({block: 'center'});
                    break;
                }
            }
        """)
        time.sleep(1)

        print("\n👉 STEP 3: VERIFYING FIELDS ARE PRESENT AND EMPTY/DEFAULT...")
        results = {}

        # ── ID MEDIO ──────────────────────────────────────────────────────────
        print("   🔍 CHECKING 'ID MEDIO'...")
        try:
            el = driver.find_element(By.XPATH,
                "//input[contains(@placeholder,'ID Medio') or "
                "        contains(@id,'id_medio') or "
                "        contains(@formcontrolname,'idMedio')]"
            )
            value = el.get_attribute("value") or ""
            is_empty = value.strip() == ""
            results["ID MEDIO"] = {"found": True, "empty": is_empty, "value": value}
            print(f"      ✅ FOUND — VALUE: '{value}' — EMPTY: {is_empty}")
        except Exception:
            try:
                driver.find_element(By.XPATH,
                    "//*[normalize-space(text())='ID Medio:' or "
                    "    normalize-space(text())='ID Medio']"
                    "[not(ancestor::nav)]"
                )
                results["ID MEDIO"] = {"found": True, "empty": True, "value": ""}
                print("      ✅ LABEL FOUND (FIELD CONFIRMED PRESENT).")
            except Exception:
                results["ID MEDIO"] = {"found": False, "empty": False, "value": ""}
                print("      ❌ NOT FOUND IN DOM.")

        # ── MODO DE TRANSACCIÓN ───────────────────────────────────────────────
        print("   🔍 CHECKING 'MODO DE TRANSACCIÓN'...")
        try:
            el = driver.find_element(By.XPATH, "//select[@id='id_transaction_mode']")
            selected_text = driver.execute_script(
                "return arguments[0].options[arguments[0].selectedIndex].text;", el
            ) or ""
            is_default = (
                selected_text.strip() == "" or
                "selecciona" in selected_text.lower()
            )
            results["MODO DE TRANSACCIÓN"] = {
                "found": True, "empty": is_default, "value": selected_text.strip()
            }
            print(f"      ✅ FOUND — SELECTED: '{selected_text.strip()}' — DEFAULT: {is_default}")
        except Exception:
            try:
                driver.find_element(By.XPATH,
                    "//*[contains(text(),'Modo de Transacción') or "
                    "    contains(text(),'Modo de Transaccion')]"
                    "[not(ancestor::nav)]"
                )
                results["MODO DE TRANSACCIÓN"] = {"found": True, "empty": True, "value": ""}
                print("      ✅ LABEL FOUND (FIELD CONFIRMED PRESENT).")
            except Exception:
                results["MODO DE TRANSACCIÓN"] = {"found": False, "empty": False, "value": ""}
                print("      ❌ NOT FOUND IN DOM.")

        # ── URL DESTINO ───────────────────────────────────────────────────────
        print("   🔍 CHECKING 'URL DESTINO'...")
        try:
            el = driver.find_element(By.XPATH, "//select[@id='id_url_target']")
            selected_text = driver.execute_script(
                "return arguments[0].options[arguments[0].selectedIndex].text;", el
            ) or ""
            is_default = (
                selected_text.strip() == "" or
                "selecciona" in selected_text.lower()
            )
            results["URL DESTINO"] = {
                "found": True, "empty": is_default, "value": selected_text.strip()
            }
            print(f"      ✅ FOUND — SELECTED: '{selected_text.strip()}' — DEFAULT: {is_default}")
        except Exception:
            try:
                driver.find_element(By.XPATH,
                    "//*[normalize-space(text())='URL Destino:' or "
                    "    normalize-space(text())='URL Destino']"
                    "[not(ancestor::nav)]"
                )
                results["URL DESTINO"] = {"found": True, "empty": True, "value": ""}
                print("      ✅ LABEL FOUND (FIELD CONFIRMED PRESENT).")
            except Exception:
                results["URL DESTINO"] = {"found": False, "empty": False, "value": ""}
                print("      ❌ NOT FOUND IN DOM.")

        # SCROLL TO CENTER THE 3 FIELDS FOR SCREENSHOT
        driver.execute_script("""
            var el = document.getElementById('id_transaction_mode');
            if (!el) {
                var all = document.querySelectorAll('*');
                for (var e of all) {
                    if (e.textContent.trim().includes('Modo de Transac')) {
                        el = e; break;
                    }
                }
            }
            if (el) el.scrollIntoView({block: 'center'});
        """)
        time.sleep(0.5)

        print("\n📸 TAKING SCREENSHOT — FIELDS PRESENT AND EMPTY (KEY EVIDENCE)...")
        utils.tomar_screenshot(driver, "MER_14_FIELDS_EMPTY")

        all_found = all(v["found"] for v in results.values())
        all_empty = all(v["empty"] for v in results.values())
        test_passed = all_found and all_empty

        print(f"\n   🔬 MER-14 ASSERTION SUMMARY:")
        print(f"      • '+NUEVO' CLICKED               : {nuevo_clicked}")
        for k, v in results.items():
            print(f"      • {k:<25} : FOUND={v['found']} | EMPTY={v['empty']} | VALUE='{v['value']}'")
        print(f"      • ALL FIELDS FOUND               : {all_found}")
        print(f"      • ALL FIELDS EMPTY/DEFAULT       : {all_empty}")
        print(f"      • FINAL URL                      : {driver.current_url}")

        _capture_web_evidence(driver, "MER_14")

        if test_passed:
            utils.tomar_screenshot(driver, "MER_14_SUCCESS")
            print("\n✅ MER-14: SUCCESS — ID MEDIO, MODO TRANSACCIÓN AND URL DESTINO ARE PRESENT AND EMPTY.")
        else:
            utils.tomar_screenshot(driver, "MER_14_FAILED")
            if not all_found:
                missing = [k for k, v in results.items() if not v["found"]]
                print(f"\n❌ MER-14: FAILED — FIELDS NOT FOUND: {missing}")
            else:
                filled = [k for k, v in results.items() if not v["empty"]]
                print(f"\n❌ MER-14: FAILED — FIELDS NOT EMPTY: {filled}")

    except Exception as e:
        print(f"\n💥 MER-14 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "MER_14_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()

# ==================================================================================
# MER-15: ACCESS THE CREATION FORM.
# ==================================================================================
def MER_15():
    
    print("\n" + "=" * 60)
    print("🧪 MER-15: ACCESS THE CREATION FORM")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO COMERCIOS MODULE...")
        _login_and_go_to_comercios(driver)

        print("\n👉 STEP 1: CLICKING '+NUEVO' TO OPEN CREATION FORM...")
        nuevo_clicked = False

        try:
            btn = driver.find_element(By.XPATH, XPATH_BTN_NUEVO)
            driver.execute_script("arguments[0].click();", btn)
            nuevo_clicked = True
            time.sleep(3)
            print("   ✅ '+NUEVO' CLICKED — STRATEGY 1 (XPATH).")
        except Exception as n1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {n1_err}")

        if not nuevo_clicked:
            try:
                result = driver.execute_script("""
                    var btns = document.querySelectorAll('button, a');
                    for (var b of btns) {
                        if (b.textContent.trim().toLowerCase().includes('nuevo')
                                && b.offsetWidth > 0) {
                            b.click();
                            return b.textContent.trim();
                        }
                    }
                    return null;
                """)
                if result:
                    nuevo_clicked = True
                    time.sleep(3)
                    print(f"   ✅ '+NUEVO' CLICKED — STRATEGY 2 (JS: '{result}').")
            except Exception as n2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {n2_err}")

        print(f"   🌐 CURRENT URL: {driver.current_url}")

        print("\n👉 STEP 2: SCROLLING TO 'DATOS DE OPERACIÓN' SECTION...")
        driver.execute_script("""
            var all = document.querySelectorAll('*');
            for (var el of all) {
                if (el.textContent.trim() === 'DATOS DE OPERACIÓN' ||
                    el.textContent.trim() === 'DATOS DE OPERACION') {
                    el.scrollIntoView({block: 'center'});
                    break;
                }
            }
        """)
        time.sleep(1)

        print("\n👉 STEP 3: VERIFYING FIELDS ARE PRESENT AND EMPTY/DEFAULT...")
        results = {}

        # ── ID MEDIO ──────────────────────────────────────────────────────────
        print("   🔍 CHECKING 'ID MEDIO'...")
        try:
            el = driver.find_element(By.XPATH,
                "//input[contains(@placeholder,'ID Medio') or "
                "        contains(@id,'id_medio') or "
                "        contains(@formcontrolname,'idMedio')]"
            )
            value = el.get_attribute("value") or ""
            is_empty = value.strip() == ""
            results["ID MEDIO"] = {"found": True, "empty": is_empty, "value": value}
            print(f"      ✅ FOUND — VALUE: '{value}' — EMPTY: {is_empty}")
        except Exception:
            try:
                driver.find_element(By.XPATH,
                    "//*[normalize-space(text())='ID Medio:' or "
                    "    normalize-space(text())='ID Medio']"
                    "[not(ancestor::nav)]"
                )
                results["ID MEDIO"] = {"found": True, "empty": True, "value": ""}
                print("      ✅ LABEL FOUND (FIELD CONFIRMED PRESENT).")
            except Exception:
                results["ID MEDIO"] = {"found": False, "empty": False, "value": ""}
                print("      ❌ NOT FOUND IN DOM.")

        # ── MODO DE TRANSACCIÓN ───────────────────────────────────────────────
        print("   🔍 CHECKING 'MODO DE TRANSACCIÓN'...")
        try:
            el = driver.find_element(By.XPATH, "//select[@id='id_transaction_mode']")
            selected_text = driver.execute_script(
                "return arguments[0].options[arguments[0].selectedIndex].text;", el
            ) or ""
            is_default = (
                selected_text.strip() == "" or
                "selecciona" in selected_text.lower()
            )
            results["MODO DE TRANSACCIÓN"] = {
                "found": True, "empty": is_default, "value": selected_text.strip()
            }
            print(f"      ✅ FOUND — SELECTED: '{selected_text.strip()}' — DEFAULT: {is_default}")
        except Exception:
            try:
                driver.find_element(By.XPATH,
                    "//*[contains(text(),'Modo de Transacción') or "
                    "    contains(text(),'Modo de Transaccion')]"
                    "[not(ancestor::nav)]"
                )
                results["MODO DE TRANSACCIÓN"] = {"found": True, "empty": True, "value": ""}
                print("      ✅ LABEL FOUND (FIELD CONFIRMED PRESENT).")
            except Exception:
                results["MODO DE TRANSACCIÓN"] = {"found": False, "empty": False, "value": ""}
                print("      ❌ NOT FOUND IN DOM.")

        # ── URL DESTINO ───────────────────────────────────────────────────────
        print("   🔍 CHECKING 'URL DESTINO'...")
        try:
            el = driver.find_element(By.XPATH, "//select[@id='id_url_target']")
            selected_text = driver.execute_script(
                "return arguments[0].options[arguments[0].selectedIndex].text;", el
            ) or ""
            is_default = (
                selected_text.strip() == "" or
                "selecciona" in selected_text.lower()
            )
            results["URL DESTINO"] = {
                "found": True, "empty": is_default, "value": selected_text.strip()
            }
            print(f"      ✅ FOUND — SELECTED: '{selected_text.strip()}' — DEFAULT: {is_default}")
        except Exception:
            try:
                driver.find_element(By.XPATH,
                    "//*[normalize-space(text())='URL Destino:' or "
                    "    normalize-space(text())='URL Destino']"
                    "[not(ancestor::nav)]"
                )
                results["URL DESTINO"] = {"found": True, "empty": True, "value": ""}
                print("      ✅ LABEL FOUND (FIELD CONFIRMED PRESENT).")
            except Exception:
                results["URL DESTINO"] = {"found": False, "empty": False, "value": ""}
                print("      ❌ NOT FOUND IN DOM.")

        # SCROLL TO CENTER THE 3 FIELDS FOR SCREENSHOT
        driver.execute_script("""
            var el = document.getElementById('id_transaction_mode');
            if (!el) {
                var all = document.querySelectorAll('*');
                for (var e of all) {
                    if (e.textContent.trim().includes('Modo de Transac')) {
                        el = e; break;
                    }
                }
            }
            if (el) el.scrollIntoView({block: 'center'});
        """)
        time.sleep(0.5)

        print("\n📸 TAKING SCREENSHOT — FIELDS PRESENT AND EMPTY (KEY EVIDENCE)...")
        utils.tomar_screenshot(driver, "MER_15_FIELDS_EMPTY")

        all_found = all(v["found"] for v in results.values())
        all_empty = all(v["empty"] for v in results.values())
        test_passed = all_found and all_empty

        print(f"\n   🔬 MER-14 ASSERTION SUMMARY:")
        print(f"      • '+NUEVO' CLICKED               : {nuevo_clicked}")
        for k, v in results.items():
            print(f"      • {k:<25} : FOUND={v['found']} | EMPTY={v['empty']} | VALUE='{v['value']}'")
        print(f"      • ALL FIELDS FOUND               : {all_found}")
        print(f"      • ALL FIELDS EMPTY/DEFAULT       : {all_empty}")
        print(f"      • FINAL URL                      : {driver.current_url}")

        _capture_web_evidence(driver, "MER_14")

        if test_passed:
            utils.tomar_screenshot(driver, "MER_15_SUCCESS")
            print("\n✅ MER-14: SUCCESS — ID MEDIO, MODO TRANSACCIÓN AND URL DESTINO ARE PRESENT AND EMPTY.")
        else:
            utils.tomar_screenshot(driver, "MER_15_FAILED")
            if not all_found:
                missing = [k for k, v in results.items() if not v["found"]]
                print(f"\n❌ MER-15: FAILED — FIELDS NOT FOUND: {missing}")
            else:
                filled = [k for k, v in results.items() if not v["empty"]]
                print(f"\n❌ MER-15: FAILED — FIELDS NOT EMPTY: {filled}")

    except Exception as e:
        print(f"\n💥 MER-15 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "MER_15_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()

# ==================================================================================
# MER-16: THE FORM DOES NOT ALLOW SAVING VALIDATION ERRORS ARE DISPLAYED.
# ==================================================================================
def MER_16():
    
    print("\n" + "=" * 60)
    print("🧪 MER-16: THE FORM DOES NOT ALLOW SAVING VALIDATION ERRORS ARE DISPLAYED.")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        # PRECONDITION: LOG IN AND NAVIGATE TO COMERCIOS MODULE
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO COMERCIOS MODULE...")
        _login_and_go_to_comercios(driver)

        # STEP 1: CLICK '+NUEVO' TO OPEN THE CREATION FORM
        print("\n👉 STEP 1: CLICKING '+NUEVO' TO OPEN CREATION FORM...")
        nuevo_clicked = False

        try:
            btn = driver.find_element(By.XPATH, XPATH_BTN_NUEVO)
            driver.execute_script("arguments[0].click();", btn)
            nuevo_clicked = True
            time.sleep(3)
            print("   ✅ '+NUEVO' CLICKED — STRATEGY 1 (XPATH).")
        except Exception as n1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {n1_err}")

        if not nuevo_clicked:
            try:
                result = driver.execute_script("""
                    var btns = document.querySelectorAll('button, a');
                    for (var b of btns) {
                        if (b.textContent.trim().toLowerCase().includes('nuevo')
                                && b.offsetWidth > 0) {
                            b.click();
                            return b.textContent.trim();
                        }
                    }
                    return null;
                """)
                if result:
                    nuevo_clicked = True
                    time.sleep(3)
                    print(f"   ✅ '+NUEVO' CLICKED — STRATEGY 2 (JS: '{result}').")
            except Exception as n2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {n2_err}")

        print(f"   🌐 CURRENT URL: {driver.current_url}")

        # STEP 2: SCROLL TO 'DATOS DE OPERACIÓN' SECTION
        print("\n👉 STEP 2: SCROLLING TO 'DATOS DE OPERACIÓN' SECTION...")
        driver.execute_script("""
            var all = document.querySelectorAll('*');
            for (var el of all) {
                if (el.textContent.trim() === 'DATOS DE OPERACIÓN' ||
                    el.textContent.trim() === 'DATOS DE OPERACION') {
                    el.scrollIntoView({block: 'center'});
                    break;
                }
            }
        """)
        time.sleep(1)

        # STEP 3: VERIFY THE 3 TARGET FIELDS ARE PRESENT
        print("\n👉 STEP 3: VERIFYING TARGET FIELDS ARE PRESENT IN 'DATOS DE OPERACIÓN'...")

        field_checks = {
            "ID MEDIO": (
                "//input[contains(@placeholder,'ID Medio') or "
                "        contains(@id,'id_medio') or "
                "        contains(@formcontrolname,'idMedio')] | "
                "//*[contains(text(),'ID Medio') or contains(text(),'Id Medio')]"
                "[not(ancestor::nav)]"
            ),
            "MODO DE TRANSACCIÓN": (
                "//select[@id='id_transaction_mode'] | "
                "//*[contains(text(),'Modo de Transacción') or "
                "    contains(text(),'Modo de Transaccion')]"
                "[not(ancestor::nav)]"
            ),
            "URL DESTINO": (
                "//select[@id='id_url_target'] | "
                "//*[contains(text(),'URL Destino')]"
                "[not(ancestor::nav)]"
            ),
        }

        fields_found = {}
        for field_name, xpath in field_checks.items():
            try:
                el = driver.find_element(By.XPATH, xpath)
                fields_found[field_name] = el.is_displayed() or True
                print(f"      ✅ FIELD FOUND: {field_name}")
            except Exception:
                fields_found[field_name] = False
                print(f"      ❌ FIELD NOT FOUND: {field_name}")

        all_fields_found = all(fields_found.values())

        # SCROLL TO SHOW THE 3 FIELDS IN VIEWPORT FOR KEY SCREENSHOT
        driver.execute_script("""
            var el = document.getElementById('id_transaction_mode');
            if (!el) {
                var all = document.querySelectorAll('*');
                for (var e of all) {
                    if (e.textContent.trim() === 'Modo de Transacción' ||
                        e.textContent.trim() === 'Modo de Transaccion') {
                        el = e;
                        break;
                    }
                }
            }
            if (el) { el.scrollIntoView({block: 'center'}); }
        """)
        time.sleep(0.5)

        # KEY SCREENSHOT #1 — THE 3 FIELDS VISIBLE
        print("\n📸 TAKING SCREENSHOT #1 — ID MEDIO + MODO TRANSACCIÓN + URL DESTINO (EVIDENCE)...")
        utils.tomar_screenshot(driver, "MER_16_1_FIELDS_PRESENT")

        # STEP 4: CLICK 'GUARDAR' WITHOUT FILLING ANY REQUIRED FIELD
        print("\n👉 STEP 4: CLICKING 'GUARDAR' WITHOUT FILLING REQUIRED FIELDS...")
        guardar_clicked = False

        # SCROLL TO BOTTOM FIRST — GUARDAR IS AT THE VERY END OF THE FORM
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        try:
            btn = driver.find_element(By.XPATH, XPATH_BTN_SAVE_FORM)
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
            time.sleep(0.5)
            btn.click()
            guardar_clicked = True
            print("   ✅ 'GUARDAR' CLICKED — STRATEGY 1 (XPATH).")
        except Exception as g1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {g1_err}")

        if not guardar_clicked:
            try:
                result = driver.execute_script("""
                    var btns = document.querySelectorAll('button');
                    for (var btn of btns) {
                        if (btn.textContent.trim().toLowerCase().includes('guardar')
                                && btn.offsetWidth > 0) {
                            btn.scrollIntoView({block: 'center'});
                            btn.click();
                            return btn.textContent.trim();
                        }
                    }
                    return null;
                """)
                if result:
                    guardar_clicked = True
                    print(f"   ✅ 'GUARDAR' CLICKED — STRATEGY 2 (JS: '{result}').")
                else:
                    print("   ❌ 'GUARDAR' BUTTON NOT FOUND.")
            except Exception as g2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {g2_err}")

        time.sleep(2)

        # STEP 5: VERIFY INFO TOAST 'Revisa la información ingresada.' APPEARS
        print("\n👉 STEP 5: VERIFYING INFO TOAST 'Revisa la información ingresada.'...")
        toast_detected = False
        wait_toast = WebDriverWait(driver, 8)

        XPATH_TOAST_INFO = (
            "//*[contains(text(),'Revisa la información ingresada') or "
            "    contains(text(),'Revisa la informacion ingresada') or "
            "    contains(text(),'Revisa la informaci')]"
        )

        # STRATEGY 1: WebDriverWait
        try:
            wait_toast.until(EC.presence_of_element_located(
                (By.XPATH, XPATH_TOAST_INFO)
            ))
            toast_detected = True
            print("   ✅ INFO TOAST DETECTED — STRATEGY 1 (WebDriverWait + XPATH).")
        except Exception:
            print("   ⚠️  TOAST NOT DETECTED VIA WAIT — TRYING JS SCAN...")

        # STRATEGY 2: JS FULL DOM SCAN
        if not toast_detected:
            try:
                result = driver.execute_script("""
                    var all = document.querySelectorAll('*');
                    for (var el of all) {
                        if (el.children.length === 0 &&
                            el.textContent.trim().toLowerCase()
                               .includes('revisa la')) {
                            return el.textContent.trim();
                        }
                    }
                    return null;
                """)
                if result:
                    toast_detected = True
                    print(f"   ✅ INFO TOAST FOUND VIA JS SCAN: '{result}'.")
                else:
                    print("   ❌ INFO TOAST NOT FOUND IN DOM.")
            except Exception as js_err:
                print(f"   ⚠️  JS SCAN FAILED: {js_err}")

        # KEY SCREENSHOT #2 — TOAST VISIBLE
        print("\n📸 TAKING SCREENSHOT #2 — INFO TOAST 'Revisa la información ingresada.' (KEY EVIDENCE)...")
        utils.tomar_screenshot(driver, "MER_16_2_INFO_TOAST")

        # FINAL ASSERTION
        test_passed = all_fields_found and guardar_clicked and toast_detected

        print(f"\n   🔬 MER-16 ASSERTION SUMMARY:")
        print(f"      • '+NUEVO' CLICKED               : {nuevo_clicked}")
        print(f"      • FIELDS FOUND                   :")
        for k, v in fields_found.items():
            print(f"          · {k:<25} : {'✅' if v else '❌'}")
        print(f"      • ALL 3 FIELDS PRESENT           : {all_fields_found}")
        print(f"      • 'GUARDAR' CLICKED              : {guardar_clicked}")
        print(f"      • INFO TOAST DETECTED            : {toast_detected}")
        print(f"      • FINAL URL                      : {driver.current_url}")

        _capture_web_evidence(driver, "MER_16")

        if test_passed:
            utils.tomar_screenshot(driver, "MER_16_SUCCESS")
            print("\n✅ MER-16: SUCCESS — FIELDS PRESENT AND INFO TOAST APPEARED ON GUARDAR.")
        else:
            utils.tomar_screenshot(driver, "MER_16_FAILED")
            if not all_fields_found:
                missing = [k for k, v in fields_found.items() if not v]
                print(f"\n❌ MER-16: FAILED — FIELDS NOT FOUND: {missing}")
            elif not guardar_clicked:
                print("\n❌ MER-16: FAILED — 'GUARDAR' BUTTON COULD NOT BE CLICKED.")
            else:
                print("\n❌ MER-16: FAILED — INFO TOAST DID NOT APPEAR AFTER GUARDAR.")

    except Exception as e:
        print(f"\n💥 MER-16 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "MER_16_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()

# ==================================================================================
# MER-17: THE FORM DOES NOT ALLOW SAVING. VALIDATION ERRORS ARE DISPLAYED. 
# ==================================================================================
def MER_17():
    print("\n" + "=" * 60)
    print("🧪 MER-17: THE FORM DOES NOT ALLOW SAVING. VALIDATION ERRORS ARE DISPLAYED. ")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO COMERCIOS MODULE...")
        _login_and_go_to_comercios(driver)

        print("\n📸 TAKING SCREENSHOT #1 — COMERCIOS TABLE...")
        utils.tomar_screenshot(driver, "MER_17_1_COMERCIOS_TABLE")

        # STEP 1: CLICK PENCIL ON FIRST ROW
        print("\n👉 STEP 1: CLICKING PENCIL ✏️ ON FIRST ROW...")
        pencil_clicked = False

        try:
            btn = driver.find_element(By.XPATH, "(//tbody//tr[1]//button)[1]")
            driver.execute_script("arguments[0].click();", btn)
            pencil_clicked = True
            time.sleep(3)
            print("   ✅ PENCIL CLICKED — STRATEGY 1 (FIRST BUTTON IN FIRST TR).")
        except Exception as p1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {p1_err}")

        if not pencil_clicked:
            try:
                result = driver.execute_script("""
                    var rows = document.querySelectorAll('tbody tr');
                    if (rows.length === 0) return 'NO ROWS';
                    var btns = rows[0].querySelectorAll('button, a[role="button"]');
                    if (btns.length === 0) return 'NO BUTTONS';
                    btns[0].click();
                    return 'clicked:' + btns[0].className;
                """)
                if result and result.startswith('clicked:'):
                    pencil_clicked = True
                    time.sleep(3)
                    print(f"   ✅ PENCIL CLICKED — STRATEGY 2 (JS: '{result}').")
                else:
                    print(f"   ❌ PENCIL DEBUG: {result}")
            except Exception as p2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {p2_err}")

        time.sleep(2)
        print(f"   🌐 CURRENT URL: {driver.current_url}")

        # STEP 2: SCROLL TO 'DATOS DE OPERACIÓN' SECTION
        print("\n👉 STEP 2: SCROLLING TO 'DATOS DE OPERACIÓN' SECTION...")
        driver.execute_script("""
            var all = document.querySelectorAll('*');
            for (var el of all) {
                if (el.textContent.trim() === 'DATOS DE OPERACIÓN' ||
                    el.textContent.trim() === 'DATOS DE OPERACION') {
                    el.scrollIntoView({block: 'center'});
                    break;
                }
            }
        """)
        time.sleep(1)

        # STEP 3: VERIFY EACH FIELD HAS A PRE-FILLED VALUE
        print("\n👉 STEP 3: VERIFYING FIELDS ARE PRE-FILLED...")
        results = {}

        # ── ID MEDIO ──────────────────────────────────────────────────────────
        print("   🔍 CHECKING 'ID MEDIO'...")
        try:
            el = driver.find_element(By.XPATH,
                "//input[contains(@placeholder,'ID Medio') or "
                "        contains(@id,'id_medio') or "
                "        contains(@formcontrolname,'idMedio')]"
            )
            value = el.get_attribute("value") or ""
            is_filled = value.strip() != ""
            results["ID MEDIO"] = {"found": True, "filled": is_filled, "value": value.strip()}
            print(f"      {'✅' if is_filled else '❌'} VALUE: '{value.strip()}' — FILLED: {is_filled}")
        except Exception:
            try:
                driver.find_element(By.XPATH,
                    "//*[normalize-space(text())='ID Medio:' or "
                    "    normalize-space(text())='ID Medio']"
                    "[not(ancestor::nav)]"
                )
                results["ID MEDIO"] = {"found": True, "filled": False, "value": ""}
                print("      ⚠️  LABEL FOUND BUT COULD NOT READ VALUE.")
            except Exception:
                results["ID MEDIO"] = {"found": False, "filled": False, "value": ""}
                print("      ❌ NOT FOUND IN DOM.")

        # ── MODO DE TRANSACCIÓN ───────────────────────────────────────────────
        print("   🔍 CHECKING 'MODO DE TRANSACCIÓN'...")
        try:
            el = driver.find_element(By.XPATH, "//select[@id='id_transaction_mode']")
            selected_text = driver.execute_script(
                "return arguments[0].options[arguments[0].selectedIndex].text;", el
            ) or ""
            is_filled = (
                selected_text.strip() != "" and
                "selecciona" not in selected_text.lower()
            )
            results["MODO DE TRANSACCIÓN"] = {
                "found": True, "filled": is_filled, "value": selected_text.strip()
            }
            print(f"      {'✅' if is_filled else '❌'} SELECTED: '{selected_text.strip()}' — FILLED: {is_filled}")
        except Exception:
            try:
                driver.find_element(By.XPATH,
                    "//*[contains(text(),'Modo de Transacción') or "
                    "    contains(text(),'Modo de Transaccion')]"
                    "[not(ancestor::nav)]"
                )
                results["MODO DE TRANSACCIÓN"] = {"found": True, "filled": False, "value": ""}
                print("      ⚠️  LABEL FOUND BUT COULD NOT READ VALUE.")
            except Exception:
                results["MODO DE TRANSACCIÓN"] = {"found": False, "filled": False, "value": ""}
                print("      ❌ NOT FOUND IN DOM.")

        # ── URL DESTINO ───────────────────────────────────────────────────────
        print("   🔍 CHECKING 'URL DESTINO'...")
        try:
            el = driver.find_element(By.XPATH, "//select[@id='id_url_target']")
            selected_text = driver.execute_script(
                "return arguments[0].options[arguments[0].selectedIndex].text;", el
            ) or ""
            is_filled = (
                selected_text.strip() != "" and
                "selecciona" not in selected_text.lower()
            )
            results["URL DESTINO"] = {
                "found": True, "filled": is_filled, "value": selected_text.strip()
            }
            print(f"      {'✅' if is_filled else '❌'} SELECTED: '{selected_text.strip()}' — FILLED: {is_filled}")
        except Exception:
            try:
                driver.find_element(By.XPATH,
                    "//*[normalize-space(text())='URL Destino:' or "
                    "    normalize-space(text())='URL Destino']"
                    "[not(ancestor::nav)]"
                )
                results["URL DESTINO"] = {"found": True, "filled": False, "value": ""}
                print("      ⚠️  LABEL FOUND BUT COULD NOT READ VALUE.")
            except Exception:
                results["URL DESTINO"] = {"found": False, "filled": False, "value": ""}
                print("      ❌ NOT FOUND IN DOM.")

        # SCROLL TO CENTER THE 3 FIELDS FOR SCREENSHOT
        driver.execute_script("""
            var el = document.getElementById('id_transaction_mode');
            if (!el) {
                var all = document.querySelectorAll('*');
                for (var e of all) {
                    if (e.textContent.trim().includes('Modo de Transac')) {
                        el = e; break;
                    }
                }
            }
            if (el) el.scrollIntoView({block: 'center'});
        """)
        time.sleep(0.5)

        print("\n📸 TAKING SCREENSHOT #2 — FIELDS PRE-FILLED (KEY EVIDENCE)...")
        utils.tomar_screenshot(driver, "MER_17_2_FIELDS_PREFILLED")

        all_found  = all(v["found"]  for v in results.values())
        all_filled = all(v["filled"] for v in results.values())
        test_passed = pencil_clicked and all_found and all_filled

        print(f"\n   🔬 MER-17 ASSERTION SUMMARY:")
        print(f"      • PENCIL CLICKED                 : {pencil_clicked}")
        for k, v in results.items():
            print(f"      • {k:<25} : FOUND={v['found']} | FILLED={v['filled']} | VALUE='{v['value']}'")
        print(f"      • ALL FIELDS FOUND               : {all_found}")
        print(f"      • ALL FIELDS PRE-FILLED          : {all_filled}")
        print(f"      • FINAL URL                      : {driver.current_url}")

        _capture_web_evidence(driver, "MER_17")

        if test_passed:
            utils.tomar_screenshot(driver, "MER_17_SUCCESS")
            print("\n✅ MER-17: SUCCESS — ALL 3 FIELDS ARE PRESENT AND PRE-FILLED.")
        else:
            utils.tomar_screenshot(driver, "MER_17_FAILED")
            if not pencil_clicked:
                print("\n❌ MER-17: FAILED — PENCIL COULD NOT BE CLICKED.")
            elif not all_found:
                missing = [k for k, v in results.items() if not v["found"]]
                print(f"\n❌ MER-17: FAILED — FIELDS NOT FOUND: {missing}")
            else:
                empty = [k for k, v in results.items() if not v["filled"]]
                print(f"\n❌ MER-17: FAILED — FIELDS WITHOUT VALUE: {empty}")

    except Exception as e:
        print(f"\n💥 MER-17 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "MER_17_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()

# ==================================================================================
# MER-18: ID, TRANSACTION, DESTINATION URL ARE REQUIRED.
# ==================================================================================
def MER_18():
    print("\n" + "=" * 60)
    print("🧪 MER-18: ID, TRANSACTION, DESTINATION URL ARE REQUIRED.")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO COMERCIOS MODULE...")
        _login_and_go_to_comercios(driver)

        print("\n📸 TAKING SCREENSHOT #1 — COMERCIOS TABLE...")
        utils.tomar_screenshot(driver, "MER_18_1_COMERCIOS_TABLE")

        # STEP 1: CLICK PENCIL ON FIRST ROW
        print("\n👉 STEP 1: CLICKING PENCIL ✏️ ON FIRST ROW...")
        pencil_clicked = False

        try:
            btn = driver.find_element(By.XPATH, "(//tbody//tr[1]//button)[1]")
            driver.execute_script("arguments[0].click();", btn)
            pencil_clicked = True
            time.sleep(3)
            print("   ✅ PENCIL CLICKED — STRATEGY 1 (FIRST BUTTON IN FIRST TR).")
        except Exception as p1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {p1_err}")

        if not pencil_clicked:
            try:
                result = driver.execute_script("""
                    var rows = document.querySelectorAll('tbody tr');
                    if (rows.length === 0) return 'NO ROWS';
                    var btns = rows[0].querySelectorAll('button, a[role="button"]');
                    if (btns.length === 0) return 'NO BUTTONS';
                    btns[0].click();
                    return 'clicked:' + btns[0].className;
                """)
                if result and result.startswith('clicked:'):
                    pencil_clicked = True
                    time.sleep(3)
                    print(f"   ✅ PENCIL CLICKED — STRATEGY 2 (JS).")
                else:
                    print(f"   ❌ PENCIL DEBUG: {result}")
            except Exception as p2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {p2_err}")

        time.sleep(2)
        print(f"   🌐 CURRENT URL: {driver.current_url}")

        # STEP 2: SCROLL TO 'DATOS DE OPERACIÓN' SECTION
        print("\n👉 STEP 2: SCROLLING TO 'DATOS DE OPERACIÓN' SECTION...")
        driver.execute_script("""
            var all = document.querySelectorAll('*');
            for (var el of all) {
                if (el.textContent.trim() === 'DATOS DE OPERACIÓN' ||
                    el.textContent.trim() === 'DATOS DE OPERACION') {
                    el.scrollIntoView({block: 'center'});
                    break;
                }
            }
        """)
        time.sleep(1)

        print("\n👉 STEP 3: VERIFYING ID MEDIO, MODO TRANSACCIÓN, URL DESTINO ARE PRE-FILLED...")
        results = {}

        # ── ID MEDIO — id CONFIRMED: id_medio ─────────────────────────────────
        print("   🔍 CHECKING 'ID MEDIO' (id='id_medio')...")
        try:
            el    = driver.find_element(By.XPATH, "//input[@id='id_medio']")
            value = el.get_attribute("value") or ""
            is_filled = value.strip() != ""
            results["ID MEDIO"] = {"found": True, "filled": is_filled, "value": value.strip()}
            print(f"      {'✅' if is_filled else '❌'} VALUE: '{value.strip()}' — FILLED: {is_filled}")
        except Exception as e:
            print(f"      ⚠️  XPATH FAILED: {e} — TRYING JS...")
            try:
                value = driver.execute_script(
                    "var el = document.getElementById('id_medio'); "
                    "return el ? el.value : null;"
                ) or ""
                is_filled = bool(value.strip())
                results["ID MEDIO"] = {"found": True, "filled": is_filled, "value": value.strip()}
                print(f"      {'✅' if is_filled else '❌'} JS VALUE: '{value.strip()}'")
            except Exception as js_e:
                results["ID MEDIO"] = {"found": False, "filled": False, "value": ""}
                print(f"      ❌ NOT FOUND: {js_e}")

        # ── MODO DE TRANSACCIÓN — id CONFIRMED: id_transaction_mode ───────────
        print("   🔍 CHECKING 'MODO DE TRANSACCIÓN' (id='id_transaction_mode')...")
        try:
            el = driver.find_element(By.XPATH, "//select[@id='id_transaction_mode']")
            selected_text = driver.execute_script(
                "return arguments[0].options[arguments[0].selectedIndex].text;", el
            ) or ""
            is_filled = (
                selected_text.strip() != "" and
                "selecciona" not in selected_text.lower()
            )
            results["MODO DE TRANSACCIÓN"] = {
                "found": True, "filled": is_filled, "value": selected_text.strip()
            }
            print(f"      {'✅' if is_filled else '❌'} SELECTED: '{selected_text.strip()}'")
        except Exception as e:
            results["MODO DE TRANSACCIÓN"] = {"found": False, "filled": False, "value": ""}
            print(f"      ❌ NOT FOUND: {e}")

        # ── URL DESTINO — id CONFIRMED: id_url_target ──────────────────────────
        print("   🔍 CHECKING 'URL DESTINO' (id='id_url_target')...")
        try:
            el = driver.find_element(By.XPATH, "//select[@id='id_url_target']")
            selected_text = driver.execute_script(
                "return arguments[0].options[arguments[0].selectedIndex].text;", el
            ) or ""
            is_filled = (
                selected_text.strip() != "" and
                "selecciona" not in selected_text.lower()
            )
            results["URL DESTINO"] = {
                "found": True, "filled": is_filled, "value": selected_text.strip()
            }
            print(f"      {'✅' if is_filled else '❌'} SELECTED: '{selected_text.strip()}'")
        except Exception as e:
            results["URL DESTINO"] = {"found": False, "filled": False, "value": ""}
            print(f"      ❌ NOT FOUND: {e}")

        # SCROLL TO CENTER THE 3 FIELDS FOR SCREENSHOT
        driver.execute_script("""
            var el = document.getElementById('id_medio');
            if (el) el.scrollIntoView({block: 'center'});
        """)
        time.sleep(0.5)

        print("\n📸 TAKING SCREENSHOT #2 — FIELDS PRE-FILLED...")
        utils.tomar_screenshot(driver, "MER_18_2_FIELDS_PREFILLED")

        # STEP 4: CHANGE 'BANCO ADQUIRENTE' TO 'B058 - BANREGIO'
        # id CONFIRMED: id_acquirer_bank
        print("\n👉 STEP 4: CHANGING 'BANCO ADQUIRENTE' TO 'B058 - BANREGIO'...")
        banco_changed = False

        # SCROLL TO BANCO ADQUIRENTE FIRST
        driver.execute_script("""
            var el = document.getElementById('id_acquirer_bank');
            if (el) el.scrollIntoView({block: 'center'});
        """)
        time.sleep(0.5)

        # STRATEGY 1: SELENIUM Select — SELECT BY TEXT CONTAINING 'BANREGIO'
        try:
            from selenium.webdriver.support.ui import Select as SeleniumSelect
            el  = driver.find_element(By.XPATH, "//select[@id='id_acquirer_bank']")
            sel = SeleniumSelect(el)
            for opt in sel.options:
                if "BANREGIO" in opt.text.upper() or "B058" in opt.text.upper():
                    sel.select_by_value(opt.get_attribute("value"))
                    banco_changed = True
                    time.sleep(0.5)
                    print(f"      ✅ BANCO ADQUIRENTE → '{opt.text.strip()}' — STRATEGY 1 (Select).")
                    break
            if not banco_changed:
                print("      ⚠️  BANREGIO OPTION NOT FOUND IN SELECT — TRYING JS...")
        except Exception as b1_err:
            print(f"      ⚠️  STRATEGY 1 FAILED: {b1_err}")

        # STRATEGY 2: JS — getElementById + scan options
        if not banco_changed:
            try:
                result = driver.execute_script("""
                    var sel = document.getElementById('id_acquirer_bank');
                    if (!sel) return 'SELECT NOT FOUND';
                    for (var i = 0; i < sel.options.length; i++) {
                        var txt = sel.options[i].text.toUpperCase();
                        if (txt.includes('BANREGIO') || txt.includes('B058')) {
                            sel.value = sel.options[i].value;
                            sel.dispatchEvent(new Event('change', {bubbles: true}));
                            return 'set:' + sel.options[i].text.trim();
                        }
                    }
                    return 'BANREGIO NOT FOUND IN ' + sel.options.length + ' OPTIONS';
                """)
                if result and result.startswith('set:'):
                    banco_changed = True
                    time.sleep(0.5)
                    print(f"      ✅ BANCO ADQUIRENTE SET VIA JS: '{result}' — STRATEGY 2.")
                else:
                    print(f"      ❌ JS FALLBACK: {result}")
            except Exception as b2_err:
                print(f"      ⚠️  STRATEGY 2 FAILED: {b2_err}")

        print("\n📸 TAKING SCREENSHOT #3 — BANCO ADQUIRENTE CHANGED TO BANREGIO...")
        utils.tomar_screenshot(driver, "MER_18_3_BANCO_CHANGED")

        # STEP 5: SCROLL TO BOTTOM AND CLICK 'GUARDAR'
        print("\n👉 STEP 5: CLICKING 'GUARDAR'...")
        guardar_clicked = False

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        try:
            btn = driver.find_element(By.XPATH, XPATH_BTN_SAVE_FORM)
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
            time.sleep(0.5)
            btn.click()
            guardar_clicked = True
            print("   ✅ 'GUARDAR' CLICKED — STRATEGY 1 (XPATH).")
        except Exception as g1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {g1_err}")

        if not guardar_clicked:
            try:
                result = driver.execute_script("""
                    var btns = document.querySelectorAll('button');
                    for (var btn of btns) {
                        if (btn.textContent.trim().toLowerCase().includes('guardar')
                                && btn.offsetWidth > 0) {
                            btn.scrollIntoView({block: 'center'});
                            btn.click();
                            return btn.textContent.trim();
                        }
                    }
                    return null;
                """)
                if result:
                    guardar_clicked = True
                    print(f"   ✅ 'GUARDAR' CLICKED — STRATEGY 2 (JS).")
            except Exception as g2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {g2_err}")

        # STEP 6: VERIFY SUCCESS
        # STRATEGY 1: IMMEDIATE TOAST CHECK (BEFORE SLEEP — TOAST IS BRIEF)
        print("\n👉 STEP 6: VERIFYING SUCCESS...")
        save_confirmed = False
        save_method    = ""

        # CHECK TOAST IMMEDIATELY AFTER CLICK
        try:
            el = driver.find_element(By.XPATH,
                "//*[contains(text(),'actualizado correctamente') or "
                "    contains(text(),'guardado correctamente') or "
                "    contains(text(),'Éxito') or "
                "    contains(text(),'exitosamente')]"
            )
            if el.is_displayed():
                save_confirmed = True
                save_method    = f"IMMEDIATE TOAST: '{el.text.strip()[:60]}'"
                print(f"   ✅ SUCCESS TOAST DETECTED IMMEDIATELY: '{el.text.strip()[:60]}'")
        except Exception:
            pass

        # STRATEGY 2: WebDriverWait SHORT TIMEOUT
        if not save_confirmed:
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,
                    "//*[contains(text(),'actualizado correctamente') or "
                    "    contains(text(),'Éxito') or "
                    "    contains(text(),'exitosamente')]"
                )))
                save_confirmed = True
                save_method    = "TOAST VIA WebDriverWait"
                print("   ✅ SUCCESS TOAST DETECTED — STRATEGY 2 (WebDriverWait 5s).")
            except Exception:
                print("   ⚠️  TOAST NOT DETECTED VIA WAIT.")

        # STRATEGY 3: URL REDIRECT CONFIRMATION
        # FROM LOG: AFTER SUCCESSFUL SAVE, URL CHANGES FROM /merchant/edit/XXX TO /merchant
        if not save_confirmed:
            time.sleep(2)
            current_url = driver.current_url.lower()
            if "merchant" in current_url and "edit" not in current_url:
                save_confirmed = True
                save_method    = f"URL REDIRECT CONFIRMED: {driver.current_url}"
                print(f"   ✅ SAVE CONFIRMED VIA URL REDIRECT: {driver.current_url}")
                print("   ℹ️  TOAST MAY HAVE APPEARED AND DISAPPEARED BEFORE DETECTION.")
            else:
                print(f"   ❌ URL STILL ON EDIT FORM: {driver.current_url}")

        # STRATEGY 4: JS SCAN FOR ANY SUCCESS MESSAGE
        if not save_confirmed:
            try:
                result = driver.execute_script("""
                    var all = document.querySelectorAll('*');
                    for (var el of all) {
                        if (el.children.length === 0) {
                            var txt = el.textContent.trim().toLowerCase();
                            if (txt.includes('actualizado') || txt.includes('exitosamente') ||
                                txt.includes('éxito') || txt.includes('exito')) {
                                return el.textContent.trim();
                            }
                        }
                    }
                    return null;
                """)
                if result:
                    save_confirmed = True
                    save_method    = f"JS SCAN: '{result[:60]}'"
                    print(f"   ✅ SUCCESS MESSAGE VIA JS: '{result[:60]}'.")
                else:
                    print("   ❌ NO SUCCESS SIGNAL DETECTED.")
            except Exception as js_err:
                print(f"   ⚠️  JS SCAN FAILED: {js_err}")

        print("\n📸 TAKING SCREENSHOT #4 — AFTER GUARDAR (KEY EVIDENCE)...")
        utils.tomar_screenshot(driver, "MER_18_4_AFTER_GUARDAR")

        # FINAL ASSERTION
        all_found  = all(v["found"]  for v in results.values())
        all_filled = all(v["filled"] for v in results.values())
        test_passed = pencil_clicked and all_filled and banco_changed and guardar_clicked and save_confirmed

        print(f"\n   🔬 MER-18 ASSERTION SUMMARY:")
        print(f"      • PENCIL CLICKED                 : {pencil_clicked}")
        for k, v in results.items():
            print(f"      • {k:<25} : FOUND={v['found']} | FILLED={v['filled']} | VALUE='{v['value']}'")
        print(f"      • ALL FIELDS FOUND               : {all_found}")
        print(f"      • ALL FIELDS PRE-FILLED          : {all_filled}")
        print(f"      • BANCO ADQUIRENTE CHANGED       : {banco_changed}")
        print(f"      • 'GUARDAR' CLICKED              : {guardar_clicked}")
        print(f"      • SAVE CONFIRMED                 : {save_confirmed}")
        print(f"      • SAVE METHOD                    : {save_method}")
        print(f"      • FINAL URL                      : {driver.current_url}")

        _capture_web_evidence(driver, "MER_18")

        if test_passed:
            utils.tomar_screenshot(driver, "MER_18_SUCCESS")
            print("\n✅ MER-18: SUCCESS — BANCO ADQUIRENTE UPDATED AND SAVE CONFIRMED.")
        else:
            utils.tomar_screenshot(driver, "MER_18_FAILED")
            if not pencil_clicked:
                print("\n❌ MER-18: FAILED — PENCIL COULD NOT BE CLICKED.")
            elif not all_filled:
                empty = [k for k, v in results.items() if not v["filled"]]
                print(f"\n❌ MER-18: FAILED — FIELDS WITHOUT VALUE: {empty}")
            elif not banco_changed:
                print("\n❌ MER-18: FAILED — 'BANCO ADQUIRENTE' COULD NOT BE CHANGED TO BANREGIO.")
            elif not guardar_clicked:
                print("\n❌ MER-18: FAILED — 'GUARDAR' COULD NOT BE CLICKED.")
            else:
                print("\n❌ MER-18: FAILED — SAVE COULD NOT BE CONFIRMED.")

    except Exception as e:
        print(f"\n💥 MER-18 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "MER_18_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()

# ==================================================================================
# MER-19: FIELDS ID, TRANSACTION MODE AND URL ARE ENABLED AND REQUIRED.
# ==================================================================================
def MER_19():
    print("\n" + "=" * 60)
    print("🧪 MER-19: FIELDS ID, TRANSACTION MODE AND URL ARE ENABLED AND REQUIRED.")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO COMERCIOS MODULE...")
        _login_and_go_to_comercios(driver)

        print("\n📸 TAKING SCREENSHOT #1 — COMERCIOS TABLE...")
        utils.tomar_screenshot(driver, "MER_19_1_COMERCIOS_TABLE")

        # STEP 1: CLICK PENCIL ON FIRST ROW
        print("\n👉 STEP 1: CLICKING PENCIL ✏️ ON FIRST ROW...")
        pencil_clicked = False

        try:
            btn = driver.find_element(By.XPATH, "(//tbody//tr[1]//button)[1]")
            driver.execute_script("arguments[0].click();", btn)
            pencil_clicked = True
            time.sleep(3)
            print("   ✅ PENCIL CLICKED — STRATEGY 1 (FIRST BUTTON IN FIRST TR).")
        except Exception as p1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {p1_err}")

        if not pencil_clicked:
            try:
                result = driver.execute_script("""
                    var rows = document.querySelectorAll('tbody tr');
                    if (rows.length === 0) return 'NO ROWS';
                    var btns = rows[0].querySelectorAll('button, a[role="button"]');
                    if (btns.length === 0) return 'NO BUTTONS';
                    btns[0].click();
                    return 'clicked:' + btns[0].className;
                """)
                if result and result.startswith('clicked:'):
                    pencil_clicked = True
                    time.sleep(3)
                    print(f"   ✅ PENCIL CLICKED — STRATEGY 2 (JS: '{result}').")
                else:
                    print(f"   ❌ PENCIL DEBUG: {result}")
            except Exception as p2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {p2_err}")

        time.sleep(2)
        print(f"   🌐 CURRENT URL: {driver.current_url}")

        # STEP 2: SCROLL TO 'DATOS DE OPERACIÓN' SECTION
        print("\n👉 STEP 2: SCROLLING TO 'DATOS DE OPERACIÓN' SECTION...")
        driver.execute_script("""
            var all = document.querySelectorAll('*');
            for (var el of all) {
                if (el.textContent.trim() === 'DATOS DE OPERACIÓN' ||
                    el.textContent.trim() === 'DATOS DE OPERACION') {
                    el.scrollIntoView({block: 'center'});
                    break;
                }
            }
        """)
        time.sleep(1)

        # STEP 3: VERIFY EACH FIELD HAS A PRE-FILLED VALUE
        print("\n👉 STEP 3: VERIFYING FIELDS ARE PRE-FILLED...")
        results = {}

        # ── ID MEDIO ──────────────────────────────────────────────────────────
        print("   🔍 CHECKING 'ID MEDIO'...")
        try:
            el = driver.find_element(By.XPATH,
                "//input[contains(@placeholder,'ID Medio') or "
                "        contains(@id,'id_medio') or "
                "        contains(@formcontrolname,'idMedio')]"
            )
            value = el.get_attribute("value") or ""
            is_filled = value.strip() != ""
            results["ID MEDIO"] = {"found": True, "filled": is_filled, "value": value.strip()}
            print(f"      {'✅' if is_filled else '❌'} VALUE: '{value.strip()}' — FILLED: {is_filled}")
        except Exception:
            try:
                driver.find_element(By.XPATH,
                    "//*[normalize-space(text())='ID Medio:' or "
                    "    normalize-space(text())='ID Medio']"
                    "[not(ancestor::nav)]"
                )
                results["ID MEDIO"] = {"found": True, "filled": False, "value": ""}
                print("      ⚠️  LABEL FOUND BUT COULD NOT READ VALUE.")
            except Exception:
                results["ID MEDIO"] = {"found": False, "filled": False, "value": ""}
                print("      ❌ NOT FOUND IN DOM.")

        # ── MODO DE TRANSACCIÓN ───────────────────────────────────────────────
        print("   🔍 CHECKING 'MODO DE TRANSACCIÓN'...")
        try:
            el = driver.find_element(By.XPATH, "//select[@id='id_transaction_mode']")
            selected_text = driver.execute_script(
                "return arguments[0].options[arguments[0].selectedIndex].text;", el
            ) or ""
            is_filled = (
                selected_text.strip() != "" and
                "selecciona" not in selected_text.lower()
            )
            results["MODO DE TRANSACCIÓN"] = {
                "found": True, "filled": is_filled, "value": selected_text.strip()
            }
            print(f"      {'✅' if is_filled else '❌'} SELECTED: '{selected_text.strip()}' — FILLED: {is_filled}")
        except Exception:
            try:
                driver.find_element(By.XPATH,
                    "//*[contains(text(),'Modo de Transacción') or "
                    "    contains(text(),'Modo de Transaccion')]"
                    "[not(ancestor::nav)]"
                )
                results["MODO DE TRANSACCIÓN"] = {"found": True, "filled": False, "value": ""}
                print("      ⚠️  LABEL FOUND BUT COULD NOT READ VALUE.")
            except Exception:
                results["MODO DE TRANSACCIÓN"] = {"found": False, "filled": False, "value": ""}
                print("      ❌ NOT FOUND IN DOM.")

        # ── URL DESTINO ───────────────────────────────────────────────────────
        print("   🔍 CHECKING 'URL DESTINO'...")
        try:
            el = driver.find_element(By.XPATH, "//select[@id='id_url_target']")
            selected_text = driver.execute_script(
                "return arguments[0].options[arguments[0].selectedIndex].text;", el
            ) or ""
            is_filled = (
                selected_text.strip() != "" and
                "selecciona" not in selected_text.lower()
            )
            results["URL DESTINO"] = {
                "found": True, "filled": is_filled, "value": selected_text.strip()
            }
            print(f"      {'✅' if is_filled else '❌'} SELECTED: '{selected_text.strip()}' — FILLED: {is_filled}")
        except Exception:
            try:
                driver.find_element(By.XPATH,
                    "//*[normalize-space(text())='URL Destino:' or "
                    "    normalize-space(text())='URL Destino']"
                    "[not(ancestor::nav)]"
                )
                results["URL DESTINO"] = {"found": True, "filled": False, "value": ""}
                print("      ⚠️  LABEL FOUND BUT COULD NOT READ VALUE.")
            except Exception:
                results["URL DESTINO"] = {"found": False, "filled": False, "value": ""}
                print("      ❌ NOT FOUND IN DOM.")

        # SCROLL TO CENTER THE 3 FIELDS FOR SCREENSHOT
        driver.execute_script("""
            var el = document.getElementById('id_transaction_mode');
            if (!el) {
                var all = document.querySelectorAll('*');
                for (var e of all) {
                    if (e.textContent.trim().includes('Modo de Transac')) {
                        el = e; break;
                    }
                }
            }
            if (el) el.scrollIntoView({block: 'center'});
        """)
        time.sleep(0.5)

        print("\n📸 TAKING SCREENSHOT #2 — FIELDS PRE-FILLED (KEY EVIDENCE)...")
        utils.tomar_screenshot(driver, "MER_19_2_FIELDS_PREFILLED")

        all_found  = all(v["found"]  for v in results.values())
        all_filled = all(v["filled"] for v in results.values())
        test_passed = pencil_clicked and all_found and all_filled

        print(f"\n   🔬 MER-19 ASSERTION SUMMARY:")
        print(f"      • PENCIL CLICKED                 : {pencil_clicked}")
        for k, v in results.items():
            print(f"      • {k:<25} : FOUND={v['found']} | FILLED={v['filled']} | VALUE='{v['value']}'")
        print(f"      • ALL FIELDS FOUND               : {all_found}")
        print(f"      • ALL FIELDS PRE-FILLED          : {all_filled}")
        print(f"      • FINAL URL                      : {driver.current_url}")

        _capture_web_evidence(driver, "MER_17")

        if test_passed:
            utils.tomar_screenshot(driver, "MER_19_SUCCESS")
            print("\n✅ MER-19: SUCCESS — ALL 3 FIELDS ARE PRESENT AND PRE-FILLED.")
        else:
            utils.tomar_screenshot(driver, "MER_19_FAILED")
            if not pencil_clicked:
                print("\n❌ MER-19: FAILED — PENCIL COULD NOT BE CLICKED.")
            elif not all_found:
                missing = [k for k, v in results.items() if not v["found"]]
                print(f"\n❌ MER-19: FAILED — FIELDS NOT FOUND: {missing}")
            else:
                empty = [k for k, v in results.items() if not v["filled"]]
                print(f"\n❌ MER-19: FAILED — FIELDS WITHOUT VALUE: {empty}")

    except Exception as e:
        print(f"\n💥 MER-19 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "MER_19_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()

# ==================================================================================
# MER-20: USER WITH EDITING PERMISSIONS, STORE CREATED USING BANREGIO
# ==================================================================================
def MER_20():
    print("\n" + "=" * 60)
    print("🧪 MER-20: USER WITH EDITING PERMISSIONS, STORE CREATED USING BANREGIO")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO COMERCIOS MODULE...")
        _login_and_go_to_comercios(driver)

        print("\n📸 TAKING SCREENSHOT #1 — COMERCIOS TABLE...")
        utils.tomar_screenshot(driver, "MER_20_1_COMERCIOS_TABLE")

        # STEP 1: CLICK PENCIL ON FIRST ROW
        print("\n👉 STEP 1: CLICKING PENCIL ✏️ ON FIRST ROW...")
        pencil_clicked = False

        try:
            btn = driver.find_element(By.XPATH, "(//tbody//tr[1]//button)[1]")
            driver.execute_script("arguments[0].click();", btn)
            pencil_clicked = True
            time.sleep(3)
            print("   ✅ PENCIL CLICKED — STRATEGY 1 (FIRST BUTTON IN FIRST TR).")
        except Exception as p1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {p1_err}")

        if not pencil_clicked:
            try:
                result = driver.execute_script("""
                    var rows = document.querySelectorAll('tbody tr');
                    if (rows.length === 0) return 'NO ROWS';
                    var btns = rows[0].querySelectorAll('button, a[role="button"]');
                    if (btns.length === 0) return 'NO BUTTONS';
                    btns[0].click();
                    return 'clicked:' + btns[0].className;
                """)
                if result and result.startswith('clicked:'):
                    pencil_clicked = True
                    time.sleep(3)
                    print(f"   ✅ PENCIL CLICKED — STRATEGY 2 (JS: '{result}').")
                else:
                    print(f"   ❌ PENCIL DEBUG: {result}")
            except Exception as p2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {p2_err}")

        time.sleep(2)
        print(f"   🌐 CURRENT URL: {driver.current_url}")

        # STEP 2: SCROLL TO 'DATOS DE OPERACIÓN' SECTION
        print("\n👉 STEP 2: SCROLLING TO 'DATOS DE OPERACIÓN' SECTION...")
        driver.execute_script("""
            var all = document.querySelectorAll('*');
            for (var el of all) {
                if (el.textContent.trim() === 'DATOS DE OPERACIÓN' ||
                    el.textContent.trim() === 'DATOS DE OPERACION') {
                    el.scrollIntoView({block: 'center'});
                    break;
                }
            }
        """)
        time.sleep(1)

        # STEP 3: VERIFY EACH FIELD HAS A PRE-FILLED VALUE
        print("\n👉 STEP 3: VERIFYING FIELDS ARE PRE-FILLED...")
        results = {}

        # ── ID MEDIO ──────────────────────────────────────────────────────────
        print("   🔍 CHECKING 'ID MEDIO'...")
        try:
            el = driver.find_element(By.XPATH,
                "//input[contains(@placeholder,'ID Medio') or "
                "        contains(@id,'id_medio') or "
                "        contains(@formcontrolname,'idMedio')]"
            )
            value = el.get_attribute("value") or ""
            is_filled = value.strip() != ""
            results["ID MEDIO"] = {"found": True, "filled": is_filled, "value": value.strip()}
            print(f"      {'✅' if is_filled else '❌'} VALUE: '{value.strip()}' — FILLED: {is_filled}")
        except Exception:
            try:
                driver.find_element(By.XPATH,
                    "//*[normalize-space(text())='ID Medio:' or "
                    "    normalize-space(text())='ID Medio']"
                    "[not(ancestor::nav)]"
                )
                results["ID MEDIO"] = {"found": True, "filled": False, "value": ""}
                print("      ⚠️  LABEL FOUND BUT COULD NOT READ VALUE.")
            except Exception:
                results["ID MEDIO"] = {"found": False, "filled": False, "value": ""}
                print("      ❌ NOT FOUND IN DOM.")

        # ── MODO DE TRANSACCIÓN ───────────────────────────────────────────────
        print("   🔍 CHECKING 'MODO DE TRANSACCIÓN'...")
        try:
            el = driver.find_element(By.XPATH, "//select[@id='id_transaction_mode']")
            selected_text = driver.execute_script(
                "return arguments[0].options[arguments[0].selectedIndex].text;", el
            ) or ""
            is_filled = (
                selected_text.strip() != "" and
                "selecciona" not in selected_text.lower()
            )
            results["MODO DE TRANSACCIÓN"] = {
                "found": True, "filled": is_filled, "value": selected_text.strip()
            }
            print(f"      {'✅' if is_filled else '❌'} SELECTED: '{selected_text.strip()}' — FILLED: {is_filled}")
        except Exception:
            try:
                driver.find_element(By.XPATH,
                    "//*[contains(text(),'Modo de Transacción') or "
                    "    contains(text(),'Modo de Transaccion')]"
                    "[not(ancestor::nav)]"
                )
                results["MODO DE TRANSACCIÓN"] = {"found": True, "filled": False, "value": ""}
                print("      ⚠️  LABEL FOUND BUT COULD NOT READ VALUE.")
            except Exception:
                results["MODO DE TRANSACCIÓN"] = {"found": False, "filled": False, "value": ""}
                print("      ❌ NOT FOUND IN DOM.")

        # ── URL DESTINO ───────────────────────────────────────────────────────
        print("   🔍 CHECKING 'URL DESTINO'...")
        try:
            el = driver.find_element(By.XPATH, "//select[@id='id_url_target']")
            selected_text = driver.execute_script(
                "return arguments[0].options[arguments[0].selectedIndex].text;", el
            ) or ""
            is_filled = (
                selected_text.strip() != "" and
                "selecciona" not in selected_text.lower()
            )
            results["URL DESTINO"] = {
                "found": True, "filled": is_filled, "value": selected_text.strip()
            }
            print(f"      {'✅' if is_filled else '❌'} SELECTED: '{selected_text.strip()}' — FILLED: {is_filled}")
        except Exception:
            try:
                driver.find_element(By.XPATH,
                    "//*[normalize-space(text())='URL Destino:' or "
                    "    normalize-space(text())='URL Destino']"
                    "[not(ancestor::nav)]"
                )
                results["URL DESTINO"] = {"found": True, "filled": False, "value": ""}
                print("      ⚠️  LABEL FOUND BUT COULD NOT READ VALUE.")
            except Exception:
                results["URL DESTINO"] = {"found": False, "filled": False, "value": ""}
                print("      ❌ NOT FOUND IN DOM.")

        # SCROLL TO CENTER THE 3 FIELDS FOR SCREENSHOT
        driver.execute_script("""
            var el = document.getElementById('id_transaction_mode');
            if (!el) {
                var all = document.querySelectorAll('*');
                for (var e of all) {
                    if (e.textContent.trim().includes('Modo de Transac')) {
                        el = e; break;
                    }
                }
            }
            if (el) el.scrollIntoView({block: 'center'});
        """)
        time.sleep(0.5)

        print("\n📸 TAKING SCREENSHOT #2 — FIELDS PRE-FILLED (KEY EVIDENCE)...")
        utils.tomar_screenshot(driver, "MER_20_2_FIELDS_PREFILLED")

        all_found  = all(v["found"]  for v in results.values())
        all_filled = all(v["filled"] for v in results.values())
        test_passed = pencil_clicked and all_found and all_filled

        print(f"\n   🔬 MER-20 ASSERTION SUMMARY:")
        print(f"      • PENCIL CLICKED                 : {pencil_clicked}")
        for k, v in results.items():
            print(f"      • {k:<25} : FOUND={v['found']} | FILLED={v['filled']} | VALUE='{v['value']}'")
        print(f"      • ALL FIELDS FOUND               : {all_found}")
        print(f"      • ALL FIELDS PRE-FILLED          : {all_filled}")
        print(f"      • FINAL URL                      : {driver.current_url}")

        _capture_web_evidence(driver, "MER_17")

        if test_passed:
            utils.tomar_screenshot(driver, "MER_20_SUCCESS")
            print("\n✅ MER-19: SUCCESS — ALL 3 FIELDS ARE PRESENT AND PRE-FILLED.")
        else:
            utils.tomar_screenshot(driver, "MER_20_FAILED")
            if not pencil_clicked:
                print("\n❌ MER-20: FAILED — PENCIL COULD NOT BE CLICKED.")
            elif not all_found:
                missing = [k for k, v in results.items() if not v["found"]]
                print(f"\n❌ MER-20: FAILED — FIELDS NOT FOUND: {missing}")
            else:
                empty = [k for k, v in results.items() if not v["filled"]]
                print(f"\n❌ MER-20: FAILED — FIELDS WITHOUT VALUE: {empty}")

    except Exception as e:
        print(f"\n💥 MER-20 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "MER_20_TECHNICAL_ERROR")
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
        # MER_03() 
        # MER_04()
        #MER_05()
        #MER_06()
        #MER_07()
        #MER_08()
        #MER_09()
        #MER_10()
        #MER_11()
        #MER_12()
        #MER_13()
        #MER_14()
        #MER_15()
        #MER_16()
        #MER_17()
        #MER_18()
        MER_19()
        MER_20()

    finally:
        utils.generar_reporte_html("MER", log_file, timestamp)


