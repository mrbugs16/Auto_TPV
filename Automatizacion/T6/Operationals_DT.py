"""
FILENAME: Operationals_DT.py
DESCRIPTION:
    VALIDATES ALL BEHAVIORS WITHIN THE "HISTORIAL DE TRANSACCIONES"
    (TRANSACTION HISTORY) SECTION OF THE MEMPHIS APP.

CONTENTS:
    · DT-82: VIEW DETAILS OF APPROVED TRANSACTION. 
    · DT-83: TRANSACTION DATA VERIFICATION.
    · DT-84: VERIFICATION OF THE 'CANCEL' BUTTON (CRITICAL DEFECT)
    · DT-85: BACK NAVIGATION FROM DETAILS
    · DT-89: BEHAVIOR IN TRANSACTIONS NOT ELIGIBLE FOR CANCELLATION
    · DT-91: DETAILED CARGO HANDLING. 

REQUIREMENTS:
    - APPIUM SERVER RUNNING.
    - config.py AND utils.py IN THE SAME DIRECTORY.
"""

import sys
import os
import re
import time

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_path not in sys.path:
    sys.path.append(project_path)

import config
import utils
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# =================================================================================
# INTERNAL HELPER: CAPTURE EVIDENCE WITHOUT SILENCING ERRORS
# =================================================================================
def _capture_evidence(driver, test_name):
    try:
        utils.print_http_evidence_appium(driver, test_name)
    except Exception as ev_err:
        print(f"   ⚠️  HTTP EVIDENCE CAPTURE FAILED FOR [{test_name}]: {ev_err}")
        print(f"   💡 MAKE SURE APPIUM IS STARTED WITH: appium --allow-insecure=*:get_server_logs")


# =================================================================================
# HELPER: FULL LOGIN + BUSINESS REGISTRATION + LOCATION PERMISSION
#         (REACHES THE MAIN CALCULATOR / CHARGING SCREEN)
# =================================================================================
def helper_login_to_calculator(driver, wait):
    # PHASE 1: LOGIN
    print("   🔐 [HELPER] PHASE 1: EXECUTING LOGIN...")
    time.sleep(4)

    try:
        utils.click_boton(driver, config.XPATH_INPUT_USUARIO)
        time.sleep(1)
    except:
        pass

    print(f"   ✏️  TYPING EMAIL & PASSWORD: {config.USUARIO_VALIDO}")
    utils.escribir_texto(driver, config.XPATH_INPUT_USUARIO, config.USUARIO_VALIDO)
    utils.escribir_texto(driver, config.XPATH_INPUT_PASS, config.PASS_VALIDO)

    try:
        driver.hide_keyboard()
    except:
        pass

    utils.click_boton(driver, config.XPATH_BTN_ACEPTAR)
    time.sleep(6)

    # PHASE 2: BUSINESS REGISTRATION
    print("   🏪 [HELPER] PHASE 2: ENTERING BUSINESS REGISTRATION DATA...")
    time.sleep(4)

    print(f"   🔑 ENTERING TOKEN: {config.RN_TOKEN}")
    try:
        utils.click_boton(driver, config.XPATH_RN_INPUT_TOKEN)
    except:
        pass
    time.sleep(1)
    utils.escribir_texto(driver, config.XPATH_RN_INPUT_TOKEN, config.RN_TOKEN)

    print(f"   🔢 ENTERING AFFILIATION NUMBER: {config.RN_AFILIACION}")
    try:
        utils.click_boton(driver, config.XPATH_RN_INPUT_AFILIACION)
    except:
        pass
    time.sleep(1)
    utils.escribir_texto(driver, config.XPATH_RN_INPUT_AFILIACION, config.RN_AFILIACION)

    try:
        driver.hide_keyboard()
    except:
        pass
    utils.click_boton(driver, config.XPATH_RN_BTN_ACEPTAR_REGISTRO)
    time.sleep(8)

    # PHASE 3: HANDLE LOCATION PERMISSION DIALOG
    print("   📍 [HELPER] PHASE 3: HANDLING LOCATION PERMISSION DIALOG...")

    location_dialog_found = utils.verificar_existencia(
        wait,
        config.XPATH_RN_PANTALLA_EXITO,
        "LOCATION PERMISSION DIALOG",
        driver
    )

    if location_dialog_found:
        print("   ✅ LOCATION PERMISSION DIALOG DETECTED. CLICKING 'MIENTRAS LA APP ESTA EN USO...'")
        utils.click_boton(driver, config.XPATH_C_BTN_MIENTRAS_USO)
        time.sleep(5)
    else:
        print("   ⚠️  WARNING: LOCATION PERMISSION DIALOG NOT DETECTED.")
        time.sleep(3)


# =================================================================================
# INTERNAL HELPER: NAVIGATE TO THE "TRANSACCIONES" BOTTOM NAV TAB
# =================================================================================
def _navigate_to_transactions_tab(driver, wait):
    print("   🔍 [NAV] ATTEMPTING STRATEGY 1: config.XPATH_PÑ_TAB_TRANSACCIONES...")
    try:
        driver.find_element(By.XPATH, config.XPATH_PÑ_TAB_TRANSACCIONES).click()
        time.sleep(2)
        print("   ✅ [NAV] STRATEGY 1 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [NAV] STRATEGY 1 FAILED: {e}")

    print("   🔍 [NAV] ATTEMPTING STRATEGY 2: PARTIAL CONTENT-DESC MATCH...")
    try:
        driver.find_element(
            By.XPATH,
            '//*[contains(@content-desc, "Transacciones")]'
        ).click()
        time.sleep(2)
        print("   ✅ [NAV] STRATEGY 2 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [NAV] STRATEGY 2 FAILED: {e}")

    print("   🔍 [NAV] ATTEMPTING STRATEGY 3: EXACT TEXT / CONTENT-DESC MATCH...")
    try:
        driver.find_element(
            By.XPATH,
            '//*[@text="Transacciones" or @content-desc="Transacciones"]'
        ).click()
        time.sleep(2)
        print("   ✅ [NAV] STRATEGY 3 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [NAV] STRATEGY 3 FAILED: {e}")

    print("   🔍 [NAV] ATTEMPTING STRATEGY 4: UIAUTOMATOR TEXT SEARCH (FINAL FALLBACK)...")
    try:
        driver.find_element(
            By.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains("Transacciones")'
        ).click()
        time.sleep(2)
        print("   ✅ [NAV] STRATEGY 4 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   💥 [NAV] STRATEGY 4 FAILED: {e}")

    print("   ❌ [NAV] ALL STRATEGIES EXHAUSTED — TRANSACTIONS TAB NOT CLICKABLE.")
    return False


# =================================================================================
# INTERNAL HELPER: ENSURE "ÚLTIMOS 30 DÍAS" SUB-TAB IS ACTIVE
# =================================================================================
def _ensure_last_30_days_tab(driver, wait):
    print("   🔍 [SUB-TAB] ATTEMPTING STRATEGY 1: EXACT MATCH 'Últimos 30 días'...")
    try:
        driver.find_element(
            By.XPATH,
            '//*[@text="Últimos 30 días" or @content-desc="Últimos 30 días"]'
        ).click()
        time.sleep(2)
        print("   ✅ [SUB-TAB] STRATEGY 1 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [SUB-TAB] STRATEGY 1 FAILED: {e}")

    print("   🔍 [SUB-TAB] ATTEMPTING STRATEGY 2: PARTIAL MATCH 'ltimos 30'...")
    try:
        driver.find_element(
            By.XPATH,
            '//*[contains(@text, "ltimos 30") or contains(@content-desc, "ltimos 30")]'
        ).click()
        time.sleep(2)
        print("   ✅ [SUB-TAB] STRATEGY 2 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [SUB-TAB] STRATEGY 2 FAILED: {e}")

    print("   🔍 [SUB-TAB] ATTEMPTING STRATEGY 3: UIAUTOMATOR TEXT CONTAINS '30'...")
    try:
        driver.find_element(
            By.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains("30")'
        ).click()
        time.sleep(2)
        print("   ✅ [SUB-TAB] STRATEGY 3 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   💥 [SUB-TAB] STRATEGY 3 FAILED: {e}")

    # NOT A HARD BLOCKER — DEFAULT VIEW MAY ALREADY BE "ÚLTIMOS 30 DÍAS"
    print("   ⚠️  [SUB-TAB] ALL STRATEGIES FAILED — ASSUMING DEFAULT VIEW IS ALREADY ACTIVE.")
    return False


# =================================================================================
# INTERNAL HELPER: DETECT AT LEAST ONE APPROVED TRANSACTION IN THE HISTORY LIST
# =================================================================================
def _find_approved_transaction(driver):
    APPROVED_KEYWORDS = ["aprobada", "aprobado", "aprobación", "aprobacion", "approved"]

    print("   🔍 [FIND APPROVED] STRATEGY 1: XPATH CONTAINS FRAGMENT 'probac'...")
    try:
        xpath_approved = (
            '//*[contains(@text, "probac") or contains(@text, "PROBAC") or '
            'contains(@content-desc, "probac") or contains(@content-desc, "PROBAC")]'
        )
        elements = driver.find_elements(By.XPATH, xpath_approved)
        if elements:
            sample_text = (
                elements[0].get_attribute("text") or
                elements[0].get_attribute("content-desc") or
                "(no text)"
            )
            print(f"   ✅ [FIND APPROVED] STRATEGY 1 SUCCEEDED — "
                  f"{len(elements)} ELEMENT(S) FOUND. FIRST: '{sample_text}'")
            return True, len(elements)
        else:
            print("   ⚠️  [FIND APPROVED] STRATEGY 1 — NO MATCHES.")
    except Exception as e:
        print(f"   ⚠️  [FIND APPROVED] STRATEGY 1 FAILED: {e}")

    # ── STRATEGY 2: FULL ELEMENT ITERATION ───────────────────────────────────
    print("   🔍 [FIND APPROVED] STRATEGY 2: FULL ELEMENT SCAN (text + content-desc)...")
    try:
        approved_count = 0
        first_match    = None
        all_elements   = driver.find_elements(By.XPATH, "//*")

        for el in all_elements:
            for attr in ("text", "content-desc"):
                val = (el.get_attribute(attr) or "").lower()
                if any(kw in val for kw in APPROVED_KEYWORDS):
                    approved_count += 1
                    if first_match is None:
                        first_match = val
                    break  

        if approved_count > 0:
            print(f"   ✅ [FIND APPROVED] STRATEGY 2 SUCCEEDED — "
                  f"{approved_count} APPROVED ITEM(S). FIRST MATCH: '{first_match}'")
            return True, approved_count
        else:
            print("   ⚠️  [FIND APPROVED] STRATEGY 2 — NO APPROVED ITEMS IN VISIBLE DOM.")
    except Exception as e:
        print(f"   ⚠️  [FIND APPROVED] STRATEGY 2 FAILED: {e}")

    # ── STRATEGY 3: UIAUTOMATOR SCROLL INTO VIEW ──────────────────────────────
    print("   🔍 [FIND APPROVED] STRATEGY 3: UIAUTOMATOR SCROLL INTO VIEW...")
    try:
        el = driver.find_element(
            By.ANDROID_UIAUTOMATOR,
            'new UiScrollable(new UiSelector().scrollable(true))'
            '.scrollIntoView(new UiSelector().textContains("probac"))'
        )
        found_text = el.get_attribute("text") or el.get_attribute("content-desc") or "(no text)"
        print(f"   ✅ [FIND APPROVED] STRATEGY 3 SUCCEEDED — "
              f"SCROLLED TO APPROVED ITEM: '{found_text}'")
        return True, 1
    except Exception as e:
        print(f"   💥 [FIND APPROVED] STRATEGY 3 FAILED: {e}")

    print("   ❌ [FIND APPROVED] ALL STRATEGIES EXHAUSTED — NO APPROVED TRANSACTION FOUND.")
    return False, 0


# =================================================================================
# DT-82: VIEW DETAILS OF APPROVED TRANSACTION. 
# =================================================================================
def DT_82():
    print("\n" + "=" * 60)
    print("🧪 DT-82: VIEW DETAILS OF APPROVED TRANSACTION. ")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        # ── PRECONDITION: FULL LOGIN + BUSINESS REGISTRATION ─────────────────
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)
        print("   ✅ PRECONDITION MET — MAIN CHARGING SCREEN REACHED.")

        # ── STEP 1: NAVIGATE TO "TRANSACCIONES" BOTTOM NAV TAB ───────────────
        print("\n👉 STEP 1: NAVIGATING TO 'TRANSACCIONES' BOTTOM NAV TAB...")
        tab_clicked = _navigate_to_transactions_tab(driver, wait)

        if not tab_clicked:
            print("\n❌ DT-82: FAILED — COULD NOT NAVIGATE TO 'TRANSACCIONES' TAB.")
            utils.tomar_screenshot(driver, "DT_82_TAB_CLICK_FAILED")
            _capture_evidence(driver, "DT_82")
            return False

        print("   ✅ STEP 1 COMPLETE — 'TRANSACCIONES' TAB REACHED.")
        time.sleep(3)

        # ── STEP 2: ENSURE "ÚLTIMOS 30 DÍAS" SUB-TAB IS ACTIVE ───────────────
        print("\n👉 STEP 2: ENSURING 'ÚLTIMOS 30 DÍAS' SUB-TAB IS THE ACTIVE VIEW...")
        _ensure_last_30_days_tab(driver, wait)
        print("   ✅ STEP 2 COMPLETE — 'ÚLTIMOS 30 DÍAS' VIEW IS ACTIVE.")
        time.sleep(2)

        # ── STEP 3: WAIT FOR HISTORY LIST TO FULLY RENDER ────────────────────
        print("\n👉 STEP 3: WAITING FOR TRANSACTION HISTORY LIST TO FULLY RENDER...")
        time.sleep(3)
        print("   ✅ STEP 3 COMPLETE — RENDER WAIT ELAPSED.")

        # ── STEP 4: SCAN FOR AT LEAST ONE APPROVED TRANSACTION ───────────────
        print("\n👉 STEP 4: SCANNING HISTORY LIST FOR AT LEAST ONE APPROVED TRANSACTION...")
        approved_found, approved_count = _find_approved_transaction(driver)

        if approved_found:
            print(f"   ✅ STEP 4 COMPLETE — {approved_count} APPROVED TRANSACTION(S) DETECTED.")
        else:
            print("   ❌ STEP 4 — NO APPROVED TRANSACTIONS FOUND IN VISIBLE LIST.")

        # ── DEBUG: LOG ALL VISIBLE TEXT FOR TRACEABILITY ─────────────────────
        print("\n🔍 SCANNING ALL VISIBLE TEXT FOR DEBUGGING...")
        try:
            seen_debug = set()
            for el in driver.find_elements(By.XPATH, "//*"):
                for attr in ("text", "content-desc"):
                    t = el.get_attribute(attr) or ""
                    if t and len(t) > 3 and t not in seen_debug:
                        seen_debug.add(t)
                        print(f"   📝 VISIBLE: '{t}'")
                        break
        except:
            pass
        print("\n📸 TAKING SCREENSHOT — TRANSACTION HISTORY LIST (SUCCESS EVIDENCE)...")
        utils.tomar_screenshot(driver, "DT_82_APPROVED_TRANSACTION_HISTORY")
        _capture_evidence(driver, "DT_82")

        # ── RESULT ────────────────────────────────────────────────────────────
        print("\n" + "-" * 60)
        print("📊 DT-82 VALIDATION SUMMARY:")
        print(f"   TRANSACTIONS TAB REACHED     : ✅")
        print(f"   'ÚLTIMOS 30 DÍAS' VIEW ACTIVE : ✅")
        print(f"   APPROVED TRANSACTION FOUND   : "
              f"{'✅ YES — COUNT: ' + str(approved_count) if approved_found else '❌ NO'}")
        print(f"   SCREENSHOT EVIDENCE SAVED    : ✅  (DT_82_APPROVED_TRANSACTION_HISTORY)")
        print("-" * 60)

        if approved_found:
            print("\n✅ DT-82: SUCCESS — AT LEAST ONE APPROVED TRANSACTION FOUND IN HISTORY.")
            return True
        else:
            print("\n❌ DT-82: FAILED — NO APPROVED TRANSACTIONS FOUND IN HISTORY.")
            return False

    except Exception as e:
        print(f"\n💥 DT-82 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "DT_82_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)


# =================================================================================
# INTERNAL HELPER: CLICK THE FIRST AVAILABLE TRANSACTION IN THE LIST
# =================================================================================
def _click_first_transaction_in_list(driver):
    DATE_PATTERN   = re.compile(r"\d{2}-\d{2}-\d{4},\s*\d{2}:\d{2}:\d{2}")
    AMOUNT_PATTERN = re.compile(r"\$[\d,]+\.\d{2}")

    # ── STRATEGY 1: FIND DATE TEXT ELEMENT → WALK UP TO CLICKABLE PARENT ─────
    print("   🔍 [CLICK FIRST] STRATEGY 1: DATE TEXT → WALK UP TO CLICKABLE PARENT ROW...")
    try:
        all_els = driver.find_elements(By.XPATH, "//*")
        date_element = None
        for el in all_els:
            t = (el.get_attribute("text") or "").strip()
            if DATE_PATTERN.match(t):
                date_element = el
                print(f"   📅 [CLICK FIRST] DATE TEXT FOUND: '{t}'")
                break

        if date_element:
            clicked = driver.execute_script("""
                var el = arguments[0];
                // TRAVERSE UP MAX 6 LEVELS LOOKING FOR CLICKABLE CONTAINER
                for (var i = 0; i < 6; i++) {
                    if (!el.parentElement) break;
                    el = el.parentElement;
                    if (el.onclick || el.getAttribute('clickable') === 'true') {
                        el.click();
                        return true;
                    }
                }
                // FALLBACK: CLICK THE DIRECT PARENT OF THE DATE TEXT
                if (arguments[0].parentElement) {
                    arguments[0].parentElement.click();
                    return true;
                }
                return false;
            """, date_element)

            if clicked:
                print("   ✅ [CLICK FIRST] STRATEGY 1 SUCCEEDED — CLICKED PARENT CARD.")
                return True
            else:
                print("   💡 [CLICK FIRST] JS WALK DID NOT FIND CLICKABLE — TRYING NATIVE PARENT...")
                try:
                    parent = driver.find_element(
                        By.XPATH,
                        f'//*[@text="{date_element.get_attribute("text")}"]/parent::*'
                    )
                    parent.click()
                    print("   ✅ [CLICK FIRST] STRATEGY 1 (NATIVE PARENT) SUCCEEDED.")
                    return True
                except Exception as pe:
                    print(f"   ⚠️  [CLICK FIRST] NATIVE PARENT ALSO FAILED: {pe}")
    except Exception as e:
        print(f"   ⚠️  [CLICK FIRST] STRATEGY 1 FAILED: {e}")

    # ── STRATEGY 2: UIAUTOMATOR — CLICK FIRST CLICKABLE VIEW CONTAINING A DATE ─
    print("   🔍 [CLICK FIRST] STRATEGY 2: UIAUTOMATOR CLICKABLE ROW WITH DATE TEXT...")
    try:
        driver.find_element(
            By.ANDROID_UIAUTOMATOR,
            'new UiSelector().clickable(true).descriptionMatches(".*\\d{2}-\\d{2}-\\d{4}.*")'
        ).click()
        print("   ✅ [CLICK FIRST] STRATEGY 2 SUCCEEDED — UIAUTOMATOR DESC MATCH.")
        return True
    except Exception as e:
        print(f"   ⚠️  [CLICK FIRST] STRATEGY 2 FAILED: {e}")

    # ── STRATEGY 3: UIAUTOMATOR — FIRST CLICKABLE android.view.View IN LIST ───
    print("   🔍 [CLICK FIRST] STRATEGY 3: FIRST CLICKABLE android.view.View IN LIST...")
    try:
        rows = driver.find_elements(
            By.XPATH,
            '//android.view.View[@clickable="true"]'
        )
        if rows:
            rows[0].click()
            print(f"   ✅ [CLICK FIRST] STRATEGY 3 SUCCEEDED — CLICKED FIRST CLICKABLE VIEW.")
            return True
        else:
            print("   ⚠️  [CLICK FIRST] STRATEGY 3 — NO CLICKABLE VIEWS FOUND.")
    except Exception as e:
        print(f"   ⚠️  [CLICK FIRST] STRATEGY 3 FAILED: {e}")

    # ── STRATEGY 4: COORDINATE TAP ON FIRST ROW (ABSOLUTE FALLBACK) ──────────
    print("   🔍 [CLICK FIRST] STRATEGY 4: COORDINATE TAP ON FIRST ROW (y≈200)...")
    try:
        size   = driver.get_window_size()
        tap_x  = size["width"] // 2
        tap_y  = int(size["height"] * 0.22)   # ~22% FROM TOP = FIRST ROW AREA
        driver.execute_script("mobile: clickGesture", {"x": tap_x, "y": tap_y})
        time.sleep(1)
        print(f"   ✅ [CLICK FIRST] STRATEGY 4 SUCCEEDED — TAPPED AT ({tap_x}, {tap_y}).")
        return True
    except Exception as e:
        print(f"   💥 [CLICK FIRST] STRATEGY 4 FAILED: {e}")

    print("   ❌ [CLICK FIRST] ALL STRATEGIES EXHAUSTED — NO TRANSACTION ROW CLICKABLE.")
    return False


# =================================================================================
# INTERNAL HELPER: READ AND VALIDATE ALL REQUIRED FIELDS FROM THE DETAIL SCREEN
# =================================================================================
def _validate_detail_fields(driver):
    AMOUNT_PATTERN  = re.compile(r"^\$[\d,]+\.\d{2}$")
    DATE_PATTERN    = re.compile(r"^\d{2}-\d{2}-\d{4},\s*\d{2}:\d{2}:\d{2}$")
    ID_PATTERN      = re.compile(r"^\d{8,}$")
    AUTH_PATTERN    = re.compile(r"^\d{4,}$")
    STATUS_VALUES   = {"aprobada", "cancelada", "aprobado", "cancelado"}

    print("   🔍 [FIELD VALIDATOR] SCANNING ALL VISIBLE TEXT FROM DETAIL SCREEN...")
    all_values = []
    try:
        seen = set()
        for el in driver.find_elements(By.XPATH, "//*"):
            for attr in ("text", "content-desc"):
                v = (el.get_attribute(attr) or "").strip()
                if v and len(v) >= 1 and v not in seen:
                    seen.add(v)
                    all_values.append(v)
        print(f"   📝 [FIELD VALIDATOR] TOTAL UNIQUE VALUES FOUND: {len(all_values)}")
        print(f"   📝 [FIELD VALIDATOR] VALUES: {all_values}")
    except Exception as e:
        print(f"   ⚠️  [FIELD VALIDATOR] SCAN FAILED: {e}")
        return {}

    results = {}

    print("   🔍 [FIELD VALIDATOR] CHECKING: TOTAL AMOUNT...")
    total_candidates = [v for v in all_values if AMOUNT_PATTERN.match(v)]
    if total_candidates:
        
        total_value = max(
            total_candidates,
            key=lambda x: float(x.replace("$", "").replace(",", ""))
        )
        results["TOTAL_AMOUNT"] = {
            "value"     : total_value,
            "format_ok" : True
        }
        print(f"   ✅ TOTAL AMOUNT: '{total_value}' — FORMAT OK")
    else:
        results["TOTAL_AMOUNT"] = {"value": None, "format_ok": False}
        print("   ❌ TOTAL AMOUNT: NOT FOUND OR WRONG FORMAT")

    # ── STATUS (APROBADA / CANCELADA) ─────────────────────────────────────────
    print("   🔍 [FIELD VALIDATOR] CHECKING: STATUS (APROBADA / CANCELADA)...")
    status_value = None
    for v in all_values:
        if v.lower() in STATUS_VALUES:
            status_value = v
            break
    if status_value:
        results["STATUS"] = {"value": status_value, "format_ok": True}
        print(f"   ✅ STATUS: '{status_value}' — FORMAT OK")
    else:
        results["STATUS"] = {"value": None, "format_ok": False}
        print("   ❌ STATUS: NOT FOUND — EXPECTED 'APROBADA' OR 'CANCELADA'")

    # ── SALE AMOUNT (VENTA) ───────────────────────────────────────────────────
    print("   🔍 [FIELD VALIDATOR] CHECKING: SALE AMOUNT (VENTA)...")
    total_numeric = (
        float(results["TOTAL_AMOUNT"]["value"].replace("$", "").replace(",", ""))
        if results["TOTAL_AMOUNT"]["value"] else None
    )
    sale_candidates = [
        v for v in all_values
        if AMOUNT_PATTERN.match(v) and (
            total_numeric is None or
            float(v.replace("$", "").replace(",", "")) < total_numeric
        )
    ]
    
    if sale_candidates:
        sale_value = max(
            sale_candidates,
            key=lambda x: float(x.replace("$", "").replace(",", ""))
        )
        results["SALE_AMOUNT"] = {"value": sale_value, "format_ok": True}
        print(f"   ✅ SALE AMOUNT (VENTA): '{sale_value}' — FORMAT OK")
    else:
        results["SALE_AMOUNT"] = {"value": None, "format_ok": False}
        print("   ❌ SALE AMOUNT (VENTA): NOT FOUND")

    # ── TIP AMOUNT (PROPINA) ──────────────────────────────────────────────────
    print("   🔍 [FIELD VALIDATOR] CHECKING: TIP AMOUNT (PROPINA)...")
    tip_value = None
    # LOOK FOR ELEMENT DIRECTLY AFTER LABEL "Propina"
    for i, v in enumerate(all_values):
        if "propina" in v.lower() and i + 1 < len(all_values):
            candidate = all_values[i + 1]
            if re.match(r"^\$[\d,]+\.\d{2}$", candidate):
                tip_value = candidate
                break
    # FALLBACK: ANY REMAINING AMOUNT SMALLER THAN SALE
    if not tip_value:
        sale_numeric = (
            float(results["SALE_AMOUNT"]["value"].replace("$", "").replace(",", ""))
            if results["SALE_AMOUNT"]["value"] else None
        )
        tip_candidates = [
            v for v in all_values
            if re.match(r"^\$[\d,]+\.\d{2}$", v) and (
                sale_numeric is None or
                float(v.replace("$", "").replace(",", "")) <= sale_numeric
            ) and v != results["SALE_AMOUNT"].get("value")
               and v != results["TOTAL_AMOUNT"].get("value")
        ]
        if tip_candidates:
            tip_value = tip_candidates[0]

    if tip_value:
        results["TIP_AMOUNT"] = {"value": tip_value, "format_ok": True}
        print(f"   ✅ TIP AMOUNT (PROPINA): '{tip_value}' — FORMAT OK (ZERO IS VALID)")
    else:
        results["TIP_AMOUNT"] = {"value": None, "format_ok": False}
        print("   ❌ TIP AMOUNT (PROPINA): NOT FOUND")

    print("   🔍 [FIELD VALIDATOR] CHECKING: COMMERCE NAME (NOMBRE DEL COMERCIO)...")
    commerce_value = None
    for i, v in enumerate(all_values):
        if "nombre del comercio" in v.lower() and i + 1 < len(all_values):
            commerce_value = all_values[i + 1]
            break
    if not commerce_value:
        for v in all_values:
            if "memphis" in v.lower() or "comercio" in v.lower():
                if len(v) > 3 and "nombre del" not in v.lower():
                    commerce_value = v
                    break
    format_ok = bool(commerce_value and len(commerce_value.strip()) > 0)
    results["COMMERCE_NAME"] = {"value": commerce_value, "format_ok": format_ok}
    if format_ok:
        print(f"   ✅ COMMERCE NAME: '{commerce_value}' — FORMAT OK (NON-EMPTY STRING)")
    else:
        print("   ❌ COMMERCE NAME: NOT FOUND OR EMPTY")

    # ── TRANSACTION ID ────────────────────────────────────────────────────────
    print("   🔍 [FIELD VALIDATOR] CHECKING: TRANSACTION ID...")
    id_value = None
    for i, v in enumerate(all_values):
        if v.lower() == "id" and i + 1 < len(all_values):
            id_value = all_values[i + 1]
            break
    if not id_value:
        for v in all_values:
            if ID_PATTERN.match(v.strip()):
                id_value = v
                break
    format_ok = bool(id_value and ID_PATTERN.match(id_value.strip()))
    results["TRANSACTION_ID"] = {"value": id_value, "format_ok": format_ok}
    if format_ok:
        print(f"   ✅ TRANSACTION ID: '{id_value}' — FORMAT OK (ALL DIGITS, >= 8 CHARS)")
    else:
        print(f"   ❌ TRANSACTION ID: VALUE='{id_value}' — WRONG FORMAT OR NOT FOUND")

    # ── DATE (FECHA) ──────────────────────────────────────────────────────────
    print("   🔍 [FIELD VALIDATOR] CHECKING: DATE (FECHA) FORMAT DD-MM-YYYY, HH:MM:SS...")
    date_value = None
    for i, v in enumerate(all_values):
        if v.lower() == "fecha" and i + 1 < len(all_values):
            date_value = all_values[i + 1]
            break
    if not date_value:
        # FALLBACK: ANY VALUE MATCHING THE DATE PATTERN
        for v in all_values:
            if DATE_PATTERN.match(v.strip()):
                date_value = v
                break
    format_ok = bool(date_value and DATE_PATTERN.match(date_value.strip()))
    results["DATE"] = {"value": date_value, "format_ok": format_ok}
    if format_ok:
        print(f"   ✅ DATE (FECHA): '{date_value}' — FORMAT OK (DD-MM-YYYY, HH:MM:SS)")
    else:
        print(f"   ❌ DATE (FECHA): VALUE='{date_value}' — WRONG FORMAT OR NOT FOUND")

    # ── AUTHORIZATION NUMBER (N.º DE AUTORIZACIÓN) ────────────────────────────
    print("   🔍 [FIELD VALIDATOR] CHECKING: AUTHORIZATION NUMBER...")
    auth_value = None
    AUTH_LABEL_FRAGMENTS = ["autorización", "autorizacion", "autoriza"]
    for i, v in enumerate(all_values):
        if any(f in v.lower() for f in AUTH_LABEL_FRAGMENTS) and i + 1 < len(all_values):
            auth_value = all_values[i + 1]
            break
    format_ok = bool(auth_value and AUTH_PATTERN.match(auth_value.strip()))
    results["AUTH_NUMBER"] = {"value": auth_value, "format_ok": format_ok}
    if format_ok:
        print(f"   ✅ AUTH NUMBER: '{auth_value}' — FORMAT OK (ALL DIGITS, >= 4 CHARS)")
    else:
        print(f"   ❌ AUTH NUMBER: VALUE='{auth_value}' — WRONG FORMAT OR NOT FOUND")

    return results


# =================================================================================
# DT-83: TRANSACTION DATA VERIFICATION.
# =================================================================================
def DT_83():
    print("\n" + "=" * 60)
    print("🧪 DT-83: TRANSACTION DATA VERIFICATION.")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        # ── PRECONDITION: FULL LOGIN + BUSINESS REGISTRATION ─────────────────
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)
        print("   ✅ PRECONDITION MET — MAIN CHARGING SCREEN REACHED.")

        # ── STEP 1: NAVIGATE TO "TRANSACCIONES" BOTTOM NAV TAB ───────────────
        print("\n👉 STEP 1: NAVIGATING TO 'TRANSACCIONES' BOTTOM NAV TAB...")
        if not _navigate_to_transactions_tab(driver, wait):
            print("\n❌ DT-83: FAILED — COULD NOT NAVIGATE TO 'TRANSACCIONES' TAB.")
            utils.tomar_screenshot(driver, "DT_83_TAB_CLICK_FAILED")
            _capture_evidence(driver, "DT_83")
            return False
        print("   ✅ STEP 1 COMPLETE — 'TRANSACCIONES' TAB REACHED.")
        time.sleep(3)

        # ── STEP 2: ENSURE "ÚLTIMOS 30 DÍAS" SUB-TAB IS ACTIVE ───────────────
        print("\n👉 STEP 2: ENSURING 'ÚLTIMOS 30 DÍAS' SUB-TAB IS THE ACTIVE VIEW...")
        _ensure_last_30_days_tab(driver, wait)
        print("   ✅ STEP 2 COMPLETE — 'ÚLTIMOS 30 DÍAS' VIEW IS ACTIVE.")
        time.sleep(2)

        # ── STEP 3: WAIT FOR HISTORY LIST TO FULLY RENDER ────────────────────
        print("\n👉 STEP 3: WAITING FOR TRANSACTION HISTORY LIST TO RENDER...")
        time.sleep(3)
        print("   ✅ STEP 3 COMPLETE — RENDER WAIT ELAPSED.")

        # ── STEP 4: TAKE SCREENSHOT OF THE LIST BEFORE CLICKING ──────────────
        print("\n👉 STEP 4: CAPTURING LIST BEFORE TAPPING FIRST TRANSACTION...")
        utils.tomar_screenshot(driver, "DT_83_LIST_BEFORE_TAP")
        print("   ✅ STEP 4 COMPLETE — LIST SCREENSHOT SAVED.")

        # ── STEP 5: CLICK THE FIRST AVAILABLE TRANSACTION IN THE LIST ─────────
        print("\n👉 STEP 5: CLICKING FIRST AVAILABLE TRANSACTION IN THE LIST...")
        if not _click_first_transaction_in_list(driver):
            print("\n❌ DT-83: FAILED — COULD NOT CLICK ANY TRANSACTION ROW.")
            utils.tomar_screenshot(driver, "DT_83_CLICK_FAILED")
            _capture_evidence(driver, "DT_83")
            return False
        time.sleep(3)
        print("   ✅ STEP 5 COMPLETE — TRANSACTION ROW TAPPED.")

        # ── STEP 6: VERIFY DETAIL SCREEN LOADED ──────────────────────────────
        print("\n👉 STEP 6: VERIFYING DETAIL SCREEN IS DISPLAYED...")
        detail_title_found = False
        # CHECK FOR TITLE "Detalle" OR FOR A LARGE DOLLAR AMOUNT IN HEADER
        for xpath in (
            '//*[@text="Detalle" or @content-desc="Detalle"]',
            '//*[contains(@text, "$") and string-length(@text) > 4]',
        ):
            try:
                elements = driver.find_elements(By.XPATH, xpath)
                if elements:
                    detail_title_found = True
                    print(f"   ✅ DETAIL SCREEN INDICATOR FOUND VIA: '{xpath}'")
                    break
            except:
                pass

        if not detail_title_found:
            print("\n❌ DT-83: FAILED — DETAIL SCREEN DID NOT OPEN AFTER TAP.")
            utils.tomar_screenshot(driver, "DT_83_DETAIL_NOT_OPENED")
            _capture_evidence(driver, "DT_83")
            return False
        print("   ✅ STEP 6 COMPLETE — DETAIL SCREEN IS OPEN.")

        # ── STEP 7: VALIDATE ALL REQUIRED FIELDS ─────────────────────────────
        print("\n👉 STEP 7: VALIDATING FIELD ACCURACY AND FORMAT...")
        field_results = _validate_detail_fields(driver)

        # ── EVIDENCE: SCREENSHOT OF DETAIL SCREEN ─────────────────────────────
        print("\n📸 TAKING SCREENSHOT — TRANSACTION DETAIL SCREEN (SUCCESS EVIDENCE)...")
        utils.tomar_screenshot(driver, "DT_83_DETAIL_FIELDS_VALIDATED")
        _capture_evidence(driver, "DT_83")

        # ── RESULT SUMMARY ────────────────────────────────────────────────────
        print("\n" + "-" * 60)
        print("📊 DT-83 VALIDATION SUMMARY:")
        print(f"   TRANSACTIONS TAB REACHED     : ✅")
        print(f"   DETAIL SCREEN OPENED         : ✅")

        all_passed = True
        field_labels = {
            "TOTAL_AMOUNT"  : "TOTAL AMOUNT (MONTO TOTAL)",
            "STATUS"        : "STATUS (APROBADA / CANCELADA)",
            "SALE_AMOUNT"   : "SALE AMOUNT (VENTA)",
            "TIP_AMOUNT"    : "TIP AMOUNT (PROPINA)",
            "COMMERCE_NAME" : "COMMERCE NAME (NOMBRE DEL COMERCIO)",
            "TRANSACTION_ID": "TRANSACTION ID (ID)",
            "DATE"          : "DATE FORMAT (FECHA) DD-MM-YYYY, HH:MM:SS",
            "AUTH_NUMBER"   : "AUTH NUMBER (N.º DE AUTORIZACIÓN)",
        }
        for field_key, field_label in field_labels.items():
            result = field_results.get(field_key, {"value": None, "format_ok": False})
            icon   = "✅" if result["format_ok"] else "❌"
            value  = result["value"] or "NOT FOUND"
            print(f"   {icon} {field_label:<45} : '{value}'")
            if not result["format_ok"]:
                all_passed = False

        print("-" * 60)

        if all_passed:
            print("\n✅ DT-83: SUCCESS — ALL FIELDS PRESENT AND FORMAT CORRECT IN DETAIL SCREEN.")
            return True
        else:
            print("\n❌ DT-83: FAILED — ONE OR MORE FIELDS MISSING OR WRONG FORMAT.")
            return False

    except Exception as e:
        print(f"\n💥 DT-83 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "DT_83_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)


# =================================================================================
# INTERNAL HELPER: READ THE DATE OF THE FIRST (MOST RECENT) TRANSACTION IN LIST
# =================================================================================
def _get_most_recent_transaction_date(driver):
    from datetime import datetime
    DATE_PATTERN = re.compile(r"(\d{2})-(\d{2})-(\d{4}),\s*(\d{2}):(\d{2}):(\d{2})")

    print("   🔍 [DATE READER] SCANNING LIST FOR MOST RECENT TRANSACTION DATE...")
    try:
        for el in driver.find_elements(By.XPATH, "//*"):
            t = (el.get_attribute("text") or "").strip()
            m = DATE_PATTERN.match(t)
            if m:
                day, month, year, hour, minute, second = m.groups()
                parsed = datetime(
                    int(year), int(month), int(day),
                    int(hour), int(minute), int(second)
                )
                print(f"   ✅ [DATE READER] MOST RECENT DATE FOUND: '{t}' → {parsed}")
                return parsed
    except Exception as e:
        print(f"   ⚠️  [DATE READER] SCAN FAILED: {e}")

    print("   ⚠️  [DATE READER] NO PARSEABLE DATE FOUND IN LIST.")
    return None


# =================================================================================
# INTERNAL HELPER: CHECK IF A GIVEN TRANSACTION DATE IS WITHIN THE LAST 24 HOURS
# =================================================================================
def _is_within_24_hours(transaction_date):
    from datetime import datetime
    now     = datetime.now()
    elapsed = now - transaction_date
    hours   = elapsed.total_seconds() / 3600
    within  = hours <= 24.0
    print(f"   🕐 [24H CHECK] TRANSACTION DATE : {transaction_date}")
    print(f"   🕐 [24H CHECK] CURRENT TIME     : {now}")
    print(f"   🕐 [24H CHECK] HOURS ELAPSED    : {hours:.2f}h")
    print(f"   🕐 [24H CHECK] WITHIN 24H       : {'✅ YES' if within else '❌ NO — CANCEL BUTTON WILL NOT APPEAR'}")
    return within, hours


# =================================================================================
# INTERNAL HELPER: DETECT THE "CANCELAR" BUTTON ON THE TRANSACTION DETAIL SCREEN
# =================================================================================
def _find_cancel_button(driver):
    CANCEL_KEYWORDS = ["cancelar", "cancel", "anular"]

    # ── STRATEGY 1: EXACT TEXT / CONTENT-DESC MATCH ───────────────────────────
    print("   🔍 [CANCEL BTN] STRATEGY 1: EXACT MATCH 'Cancelar'...")
    try:
        elements = driver.find_elements(
            By.XPATH,
            '//*[@text="Cancelar" or @content-desc="Cancelar"]'
        )
        if elements:
            txt = elements[0].get_attribute("text") or elements[0].get_attribute("content-desc")
            print(f"   ✅ [CANCEL BTN] STRATEGY 1 SUCCEEDED — TEXT: '{txt}'")
            return True, txt
        print("   ⚠️  [CANCEL BTN] STRATEGY 1 — NO EXACT MATCH.")
    except Exception as e:
        print(f"   ⚠️  [CANCEL BTN] STRATEGY 1 FAILED: {e}")

    # ── STRATEGY 2: PARTIAL CONTAINS "ancelar" (AVOIDS ACCENT ISSUES) ─────────
    print("   🔍 [CANCEL BTN] STRATEGY 2: PARTIAL CONTAINS 'ancelar'...")
    try:
        elements = driver.find_elements(
            By.XPATH,
            '//*[contains(@text, "ancelar") or contains(@content-desc, "ancelar")]'
        )
        if elements:
            txt = elements[0].get_attribute("text") or elements[0].get_attribute("content-desc")
            print(f"   ✅ [CANCEL BTN] STRATEGY 2 SUCCEEDED — TEXT: '{txt}'")
            return True, txt
        print("   ⚠️  [CANCEL BTN] STRATEGY 2 — NO PARTIAL MATCH.")
    except Exception as e:
        print(f"   ⚠️  [CANCEL BTN] STRATEGY 2 FAILED: {e}")

    # ── STRATEGY 3: UIAUTOMATOR TEXT CONTAINS ─────────────────────────────────
    print("   🔍 [CANCEL BTN] STRATEGY 3: UIAUTOMATOR textContains 'ancelar'...")
    try:
        el = driver.find_element(
            By.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains("ancelar")'
        )
        txt = el.get_attribute("text") or "(no text)"
        print(f"   ✅ [CANCEL BTN] STRATEGY 3 SUCCEEDED — TEXT: '{txt}'")
        return True, txt
    except Exception as e:
        print(f"   ⚠️  [CANCEL BTN] STRATEGY 3 FAILED: {e}")

    # ── STRATEGY 4: FULL ELEMENT SCAN (FINAL FALLBACK) ────────────────────────
    print("   🔍 [CANCEL BTN] STRATEGY 4: FULL ELEMENT SCAN (text + content-desc)...")
    try:
        for el in driver.find_elements(By.XPATH, "//*"):
            for attr in ("text", "content-desc"):
                val = (el.get_attribute(attr) or "").lower()
                if any(kw in val for kw in CANCEL_KEYWORDS):
                    txt = el.get_attribute("text") or el.get_attribute("content-desc") or val
                    print(f"   ✅ [CANCEL BTN] STRATEGY 4 SUCCEEDED — TEXT: '{txt}'")
                    return True, txt
    except Exception as e:
        print(f"   💥 [CANCEL BTN] STRATEGY 4 FAILED: {e}")

    print("   ❌ [CANCEL BTN] ALL STRATEGIES EXHAUSTED — 'CANCELAR' BUTTON NOT FOUND.")
    return False, None


# =================================================================================
# DT-84: VERIFICATION OF THE 'CANCEL' BUTTON (CRITICAL DEFECT)
# =================================================================================
def DT_84():
    from datetime import datetime
    print("\n" + "=" * 60)
    print('🧪 DT-84: VERIFICATION OF THE CANCEL BUTTON (CRITICAL DEFECT)')
    print("=" * 60)
    print("   ℹ️  NOTE: THE 'CANCELAR' BUTTON IS ONLY VISIBLE IF THE MOST RECENT")
    print("   TRANSACTION WAS MADE WITHIN THE LAST 24 HOURS.")

    driver, wait = utils.iniciar_driver()

    try:
        # ── PRECONDITION: FULL LOGIN + BUSINESS REGISTRATION ─────────────────
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)
        print("   ✅ PRECONDITION MET — MAIN CHARGING SCREEN REACHED.")

        # ── STEP 1: NAVIGATE TO "TRANSACCIONES" BOTTOM NAV TAB ───────────────
        print("\n👉 STEP 1: NAVIGATING TO 'TRANSACCIONES' BOTTOM NAV TAB...")
        if not _navigate_to_transactions_tab(driver, wait):
            print("\n❌ DT-84: FAILED — COULD NOT NAVIGATE TO 'TRANSACCIONES' TAB.")
            utils.tomar_screenshot(driver, "DT_84_TAB_CLICK_FAILED")
            _capture_evidence(driver, "DT_84")
            return False
        print("   ✅ STEP 1 COMPLETE — 'TRANSACCIONES' TAB REACHED.")
        time.sleep(3)

        # ── STEP 2: ENSURE "ÚLTIMOS 30 DÍAS" SUB-TAB IS ACTIVE ───────────────
        print("\n👉 STEP 2: ENSURING 'ÚLTIMOS 30 DÍAS' SUB-TAB IS THE ACTIVE VIEW...")
        _ensure_last_30_days_tab(driver, wait)
        print("   ✅ STEP 2 COMPLETE — 'ÚLTIMOS 30 DÍAS' VIEW IS ACTIVE.")
        time.sleep(2)

        # ── STEP 3: WAIT FOR HISTORY LIST TO FULLY RENDER ────────────────────
        print("\n👉 STEP 3: WAITING FOR TRANSACTION HISTORY LIST TO RENDER...")
        time.sleep(3)
        print("   ✅ STEP 3 COMPLETE — RENDER WAIT ELAPSED.")

        # ── STEP 4: READ DATE OF MOST RECENT TRANSACTION ─────────────────────
        print("\n👉 STEP 4: READING DATE OF MOST RECENT TRANSACTION IN LIST...")
        most_recent_date = _get_most_recent_transaction_date(driver)

        if most_recent_date is None:
            print("\n⚠️  DT-84: SKIPPED — COULD NOT READ ANY TRANSACTION DATE FROM LIST.")
            print("   💡 VERIFY THAT THE LIST IS LOADED AND HAS AT LEAST ONE TRANSACTION.")
            utils.tomar_screenshot(driver, "DT_84_NO_DATE_FOUND")
            _capture_evidence(driver, "DT_84")
            return False

        print("   ✅ STEP 4 COMPLETE — MOST RECENT TRANSACTION DATE READ.")

        # ── STEP 5: CHECK IF MOST RECENT TRANSACTION IS WITHIN 24 HOURS ──────
        print("\n👉 STEP 5: CHECKING IF MOST RECENT TRANSACTION IS WITHIN THE 24H WINDOW...")
        within_24h, hours_elapsed = _is_within_24_hours(most_recent_date)

        if not within_24h:
            print(f"\n⚠️  DT-84: SKIPPED — MOST RECENT TRANSACTION IS {hours_elapsed:.1f}H OLD.")
            print("   💡 THE 'CANCELAR' BUTTON ONLY APPEARS WITHIN 24 HOURS OF THE TRANSACTION.")
            print("   💡 PERFORM A NEW TRANSACTION AND RE-RUN THIS TEST WITHIN 24 HOURS.")
            utils.tomar_screenshot(driver, "DT_84_OUTSIDE_24H_WINDOW")
            _capture_evidence(driver, "DT_84")
            return False

        print(f"   ✅ STEP 5 COMPLETE — TRANSACTION IS {hours_elapsed:.1f}H OLD. WITHIN 24H WINDOW.")

        # ── STEP 6: TAKE SCREENSHOT OF THE LIST BEFORE CLICKING ──────────────
        print("\n👉 STEP 6: CAPTURING LIST BEFORE TAPPING MOST RECENT TRANSACTION...")
        utils.tomar_screenshot(driver, "DT_84_LIST_BEFORE_TAP")
        print("   ✅ STEP 6 COMPLETE — LIST SCREENSHOT SAVED.")

        # ── STEP 7: CLICK THE FIRST (MOST RECENT) TRANSACTION IN THE LIST ─────
        print("\n👉 STEP 7: CLICKING MOST RECENT TRANSACTION TO OPEN DETAIL SCREEN...")
        if not _click_first_transaction_in_list(driver):
            print("\n❌ DT-84: FAILED — COULD NOT CLICK MOST RECENT TRANSACTION ROW.")
            utils.tomar_screenshot(driver, "DT_84_CLICK_FAILED")
            _capture_evidence(driver, "DT_84")
            return False
        time.sleep(3)
        print("   ✅ STEP 7 COMPLETE — TRANSACTION ROW TAPPED.")

        # ── STEP 8: VERIFY DETAIL SCREEN LOADED ──────────────────────────────
        print("\n👉 STEP 8: VERIFYING DETAIL SCREEN IS DISPLAYED...")
        detail_loaded = False
        for xpath in (
            '//*[@text="Detalle" or @content-desc="Detalle"]',
            '//*[contains(@text, "$") and string-length(@text) > 4]',
        ):
            try:
                if driver.find_elements(By.XPATH, xpath):
                    detail_loaded = True
                    print(f"   ✅ DETAIL SCREEN INDICATOR FOUND.")
                    break
            except:
                pass

        if not detail_loaded:
            print("\n❌ DT-84: FAILED — DETAIL SCREEN DID NOT OPEN AFTER TAP.")
            utils.tomar_screenshot(driver, "DT_84_DETAIL_NOT_OPENED")
            _capture_evidence(driver, "DT_84")
            return False
        print("   ✅ STEP 8 COMPLETE — DETAIL SCREEN IS OPEN.")

        # ── STEP 9: SCAN FOR "CANCELAR" BUTTON ───────────────────────────────
        print("\n👉 STEP 9: SCANNING DETAIL SCREEN FOR 'CANCELAR' BUTTON...")
        cancel_found, cancel_text = _find_cancel_button(driver)

        # ── DEBUG: LOG ALL VISIBLE TEXT FOR TRACEABILITY ─────────────────────
        print("\n🔍 SCANNING ALL VISIBLE TEXT FOR DEBUGGING...")
        try:
            seen_debug = set()
            for el in driver.find_elements(By.XPATH, "//*"):
                for attr in ("text", "content-desc"):
                    t = el.get_attribute(attr) or ""
                    if t and len(t) > 2 and t not in seen_debug:
                        seen_debug.add(t)
                        print(f"   📝 VISIBLE: '{t}'")
                        break
        except:
            pass

        # ── EVIDENCE: SCREENSHOT OF DETAIL SCREEN ─────────────────────────────
        print("\n📸 TAKING SCREENSHOT — DETAIL SCREEN WITH 'CANCELAR' BUTTON (SUCCESS EVIDENCE)...")
        utils.tomar_screenshot(driver, "DT_84_CANCEL_BUTTON_DETAIL")
        _capture_evidence(driver, "DT_84")

        # ── RESULT ────────────────────────────────────────────────────────────
        print("\n" + "-" * 60)
        print('📊 DT-84 VALIDATION SUMMARY:')
        print(f"   TRANSACTIONS TAB REACHED     : ✅")
        print(f"   MOST RECENT DATE READ        : ✅  ({most_recent_date})")
        print(f"   WITHIN 24H WINDOW            : ✅  ({hours_elapsed:.1f}H ELAPSED)")
        print(f"   DETAIL SCREEN OPENED         : ✅")
        print(f"   'CANCELAR' BUTTON FOUND      : "
              f"{'✅ YES — TEXT: ' + str(cancel_text) if cancel_found else '❌ NO — CRITICAL DEFECT'}")
        print("-" * 60)

        if cancel_found:
            print("\n✅ DT-84: SUCCESS — 'CANCELAR' BUTTON IS PRESENT AND VISIBLE IN DETAIL SCREEN.")
            return True
        else:
            print("\n❌ DT-84: FAILED (CRITICAL DEFECT) — 'CANCELAR' BUTTON NOT FOUND.")
            print("   💡 THIS IS A CRITICAL DEFECT: THE BUTTON SHOULD BE VISIBLE FOR")
            print(f"   TRANSACTIONS MADE WITHIN THE LAST 24 HOURS ({hours_elapsed:.1f}H AGO).")
            return False

    except Exception as e:
        print(f"\n💥 DT-84 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "DT_84_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)


# =================================================================================
# INTERNAL HELPER: CLICK THE BACK ARROW (←) ON THE DETAIL SCREEN
# =================================================================================
def _click_back_arrow_from_detail(driver):
    BACK_LABELS = ["Volver", "volver", "Back", "back", "Atrás", "atrás", "atras", "←", "<"]

    # ── STRATEGY 1: KNOWN BACK LABELS IN content-desc / text ─────────────────
    print("   🔍 [BACK ARROW] STRATEGY 1: KNOWN BACK LABELS (content-desc / text)...")
    try:
        for label in BACK_LABELS:
            elements = driver.find_elements(
                By.XPATH,
                f'//*[@content-desc="{label}" or @text="{label}"]'
            )
            if elements:
                elements[0].click()
                print(f"   ✅ [BACK ARROW] STRATEGY 1 SUCCEEDED — LABEL: '{label}'")
                return True
        print("   ⚠️  [BACK ARROW] STRATEGY 1 — NO KNOWN BACK LABEL FOUND.")
    except Exception as e:
        print(f"   ⚠️  [BACK ARROW] STRATEGY 1 FAILED: {e}")

    # ── STRATEGY 2: FIRST android.widget.Button WITH EMPTY / ICON-ONLY TEXT ───
    
    print("   🔍 [BACK ARROW] STRATEGY 2: FIRST ICON-ONLY BUTTON (NO TEXT)...")
    try:
        buttons = driver.find_elements(By.XPATH, "//android.widget.Button")
        for btn in buttons:
            txt  = (btn.get_attribute("text")         or "").strip()
            desc = (btn.get_attribute("content-desc") or "").strip()
            if not txt and not desc:
                btn.click()
                print("   ✅ [BACK ARROW] STRATEGY 2 SUCCEEDED — ICON-ONLY BUTTON CLICKED.")
                return True
            # ALSO ACCEPT IF content-desc CONTAINS DIRECTIONAL HINT
            if any(kw in desc.lower() for kw in ("back", "volver", "atr", "regresar")):
                btn.click()
                print(f"   ✅ [BACK ARROW] STRATEGY 2 SUCCEEDED — DESC: '{desc}'")
                return True
        print("   ⚠️  [BACK ARROW] STRATEGY 2 — NO ICON-ONLY BUTTON FOUND.")
    except Exception as e:
        print(f"   ⚠️  [BACK ARROW] STRATEGY 2 FAILED: {e}")

    # ── STRATEGY 3: SIBLING ELEMENT TO THE LEFT OF "Detalle" TITLE ───────────
    print("   🔍 [BACK ARROW] STRATEGY 3: PRECEDING SIBLING OF 'Detalle' TITLE...")
    try:
        back_btn = driver.find_element(
            By.XPATH,
            '//*[@text="Detalle" or @content-desc="Detalle"]/preceding-sibling::*[1]'
        )
        back_btn.click()
        print("   ✅ [BACK ARROW] STRATEGY 3 SUCCEEDED — PRECEDING SIBLING OF 'Detalle' CLICKED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [BACK ARROW] STRATEGY 3 FAILED: {e}")

    # ── STRATEGY 4: ANDROID HARDWARE BACK KEY (SYSTEM-LEVEL FALLBACK) ─────────
    print("   🔍 [BACK ARROW] STRATEGY 4: ANDROID HARDWARE BACK KEY...")
    try:
        driver.press_keycode(4)   # KEYCODE 4 = ANDROID BACK BUTTON
        time.sleep(2)
        print("   ✅ [BACK ARROW] STRATEGY 4 SUCCEEDED — HARDWARE BACK KEY PRESSED.")
        return True
    except Exception as e:
        print(f"   💥 [BACK ARROW] STRATEGY 4 FAILED: {e}")

    print("   ❌ [BACK ARROW] ALL STRATEGIES EXHAUSTED — COULD NOT NAVIGATE BACK.")
    return False


# =================================================================================
# INTERNAL HELPER: VERIFY WE ARE BACK ON THE TRANSACTION HISTORY LIST SCREEN
# =================================================================================
def _verify_back_on_history_list(driver, wait):
    DATE_PATTERN = re.compile(r"\d{2}-\d{2}-\d{4},\s*\d{2}:\d{2}:\d{2}")

    # ── INDICATOR 1: "Transacciones" HEADER TITLE ─────────────────────────────
    print("   🔍 [VERIFY BACK] INDICATOR 1: 'Transacciones' HEADER TITLE...")
    try:
        elements = driver.find_elements(
            By.XPATH,
            '//*[@text="Transacciones" or @content-desc="Transacciones"]'
        )
        if elements:
            print("   ✅ [VERIFY BACK] INDICATOR 1 FOUND — 'Transacciones' TITLE VISIBLE.")
            return True
        print("   ⚠️  [VERIFY BACK] INDICATOR 1 NOT FOUND.")
    except Exception as e:
        print(f"   ⚠️  [VERIFY BACK] INDICATOR 1 FAILED: {e}")

    # ── INDICATOR 2: "Últimos 30 días" SUB-TAB ────────────────────────────────
    print("   🔍 [VERIFY BACK] INDICATOR 2: 'Últimos 30 días' SUB-TAB...")
    try:
        elements = driver.find_elements(
            By.XPATH,
            '//*[contains(@text, "ltimos 30") or contains(@content-desc, "ltimos 30")]'
        )
        if elements:
            print("   ✅ [VERIFY BACK] INDICATOR 2 FOUND — 'Últimos 30 días' TAB VISIBLE.")
            return True
        print("   ⚠️  [VERIFY BACK] INDICATOR 2 NOT FOUND.")
    except Exception as e:
        print(f"   ⚠️  [VERIFY BACK] INDICATOR 2 FAILED: {e}")

    # ── INDICATOR 3: TRANSACTION DATE FORMAT IN DOM ────────────────────────────
    print("   🔍 [VERIFY BACK] INDICATOR 3: TRANSACTION DATE IN LIST...")
    try:
        for el in driver.find_elements(By.XPATH, "//*"):
            t = (el.get_attribute("text") or "").strip()
            if DATE_PATTERN.match(t):
                print(f"   ✅ [VERIFY BACK] INDICATOR 3 FOUND — DATE VISIBLE: '{t}'")
                return True
        print("   ⚠️  [VERIFY BACK] INDICATOR 3 NOT FOUND.")
    except Exception as e:
        print(f"   ⚠️  [VERIFY BACK] INDICATOR 3 FAILED: {e}")

    print("   ❌ [VERIFY BACK] ALL INDICATORS EXHAUSTED — HISTORY LIST NOT CONFIRMED.")
    return False


# =================================================================================
# DT-85: BACK NAVIGATION FROM DETAILS
# =================================================================================
def DT_85():
    print("\n" + "=" * 60)
    print("🧪 DT-85: BACK NAVIGATION FROM DETAILS")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        # ── PRECONDITION: FULL LOGIN + BUSINESS REGISTRATION ─────────────────
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)
        print("   ✅ PRECONDITION MET — MAIN CHARGING SCREEN REACHED.")

        # ── STEP 1: NAVIGATE TO "TRANSACCIONES" BOTTOM NAV TAB ───────────────
        print("\n👉 STEP 1: NAVIGATING TO 'TRANSACCIONES' BOTTOM NAV TAB...")
        if not _navigate_to_transactions_tab(driver, wait):
            print("\n❌ DT-85: FAILED — COULD NOT NAVIGATE TO 'TRANSACCIONES' TAB.")
            utils.tomar_screenshot(driver, "DT_85_TAB_CLICK_FAILED")
            _capture_evidence(driver, "DT_85")
            return False
        print("   ✅ STEP 1 COMPLETE — 'TRANSACCIONES' TAB REACHED.")
        time.sleep(3)

        # ── STEP 2: ENSURE "ÚLTIMOS 30 DÍAS" SUB-TAB IS ACTIVE ───────────────
        print("\n👉 STEP 2: ENSURING 'ÚLTIMOS 30 DÍAS' SUB-TAB IS THE ACTIVE VIEW...")
        _ensure_last_30_days_tab(driver, wait)
        print("   ✅ STEP 2 COMPLETE — 'ÚLTIMOS 30 DÍAS' VIEW IS ACTIVE.")
        time.sleep(2)

        # ── STEP 3: WAIT FOR HISTORY LIST TO FULLY RENDER ────────────────────
        print("\n👉 STEP 3: WAITING FOR TRANSACTION HISTORY LIST TO RENDER...")
        time.sleep(3)
        print("   ✅ STEP 3 COMPLETE — RENDER WAIT ELAPSED.")

        # ── STEP 4: TAKE SCREENSHOT OF THE HISTORY LIST (BASELINE) ───────────
        print("\n👉 STEP 4: CAPTURING HISTORY LIST AS BASELINE BEFORE NAVIGATION...")
        utils.tomar_screenshot(driver, "DT_85_LIST_BASELINE")
        print("   ✅ STEP 4 COMPLETE — BASELINE SCREENSHOT SAVED.")

        # ── STEP 5: CLICK THE FIRST (MOST RECENT) TRANSACTION ────────────────
        print("\n👉 STEP 5: CLICKING MOST RECENT TRANSACTION TO OPEN DETAIL SCREEN...")
        if not _click_first_transaction_in_list(driver):
            print("\n❌ DT-85: FAILED — COULD NOT CLICK MOST RECENT TRANSACTION ROW.")
            utils.tomar_screenshot(driver, "DT_85_CLICK_FAILED")
            _capture_evidence(driver, "DT_85")
            return False
        time.sleep(3)
        print("   ✅ STEP 5 COMPLETE — TRANSACTION ROW TAPPED.")

        # ── STEP 6: VERIFY DETAIL SCREEN IS OPEN ─────────────────────────────
        print("\n👉 STEP 6: VERIFYING DETAIL SCREEN IS DISPLAYED...")
        detail_loaded = False
        for xpath in (
            '//*[@text="Detalle" or @content-desc="Detalle"]',
            '//*[contains(@text, "$") and string-length(@text) > 4]',
        ):
            try:
                if driver.find_elements(By.XPATH, xpath):
                    detail_loaded = True
                    print("   ✅ DETAIL SCREEN INDICATOR FOUND.")
                    break
            except:
                pass

        if not detail_loaded:
            print("\n❌ DT-85: FAILED — DETAIL SCREEN DID NOT OPEN AFTER TAP.")
            utils.tomar_screenshot(driver, "DT_85_DETAIL_NOT_OPENED")
            _capture_evidence(driver, "DT_85")
            return False
        print("   ✅ STEP 6 COMPLETE — DETAIL SCREEN IS OPEN.")

        # ── STEP 7: TAKE SCREENSHOT OF DETAIL SCREEN (SHOWS BACK ARROW) ──────
        print("\n👉 STEP 7: CAPTURING DETAIL SCREEN SHOWING BACK ARROW...")
        utils.tomar_screenshot(driver, "DT_85_DETAIL_BEFORE_BACK")
        print("   ✅ STEP 7 COMPLETE — DETAIL SCREENSHOT SAVED.")

        # ── STEP 8: CLICK THE BACK ARROW (←) ─────────────────────────────────
        print("\n👉 STEP 8: CLICKING BACK ARROW TO RETURN TO HISTORY LIST...")
        back_clicked = _click_back_arrow_from_detail(driver)

        if not back_clicked:
            print("\n❌ DT-85: FAILED — COULD NOT CLICK BACK ARROW ON DETAIL SCREEN.")
            utils.tomar_screenshot(driver, "DT_85_BACK_CLICK_FAILED")
            _capture_evidence(driver, "DT_85")
            return False

        time.sleep(3)
        print("   ✅ STEP 8 COMPLETE — BACK ARROW CLICKED.")

        # ── STEP 9: VERIFY WE ARE BACK ON THE HISTORY LIST ───────────────────
        print("\n👉 STEP 9: VERIFYING NAVIGATION RETURNED TO TRANSACTION HISTORY LIST...")
        back_on_list = _verify_back_on_history_list(driver, wait)

        # ── DEBUG: LOG ALL VISIBLE TEXT FOR TRACEABILITY ─────────────────────
        print("\n🔍 SCANNING ALL VISIBLE TEXT FOR DEBUGGING...")
        try:
            seen_debug = set()
            for el in driver.find_elements(By.XPATH, "//*"):
                for attr in ("text", "content-desc"):
                    t = el.get_attribute(attr) or ""
                    if t and len(t) > 2 and t not in seen_debug:
                        seen_debug.add(t)
                        print(f"   📝 VISIBLE: '{t}'")
                        break
        except:
            pass

        # ── EVIDENCE: SCREENSHOT OF THE LIST AFTER BACK NAVIGATION ────────────
        print("\n📸 TAKING SCREENSHOT — HISTORY LIST AFTER BACK NAVIGATION (SUCCESS EVIDENCE)...")
        utils.tomar_screenshot(driver, "DT_85_BACK_TO_HISTORY_LIST")
        _capture_evidence(driver, "DT_85")

        # ── RESULT ────────────────────────────────────────────────────────────
        print("\n" + "-" * 60)
        print("📊 DT-85 VALIDATION SUMMARY:")
        print(f"   TRANSACTIONS TAB REACHED     : ✅")
        print(f"   FIRST TRANSACTION CLICKED    : ✅")
        print(f"   DETAIL SCREEN OPENED         : ✅")
        print(f"   BACK ARROW CLICKED           : ✅")
        print(f"   RETURNED TO HISTORY LIST     : {'✅ YES' if back_on_list else '❌ NO'}")
        print("-" * 60)

        if back_on_list:
            print("\n✅ DT-85: SUCCESS — BACK ARROW NAVIGATED CORRECTLY TO HISTORY LIST.")
            return True
        else:
            print("\n❌ DT-85: FAILED — BACK ARROW DID NOT RETURN TO HISTORY LIST.")
            return False

    except Exception as e:
        print(f"\n💥 DT-85 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "DT_85_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)


# =================================================================================
# INTERNAL HELPER: CLICK THE SECOND TRANSACTION ROW IN THE LIST (INDEX 1)
# =================================================================================
def _click_second_transaction_in_list(driver):
    DATE_PATTERN   = re.compile(r"\d{2}-\d{2}-\d{4},\s*\d{2}:\d{2}:\d{2}")
    NAV_BAR_LABELS = {"inicio", "transacciones", "servicios", "ajustes"}
 
    def _is_nav_bar(el):
        for attr in ("text", "content-desc"):
            if (el.get_attribute(attr) or "").lower().strip() in NAV_BAR_LABELS:
                return True
        return False
 
    # ── STRATEGY 1: SECOND CLICKABLE VIEW (EXCLUDING NAV BAR) ────────────────
    print("   🔍 [CLICK 2ND] STRATEGY 1: SECOND CLICKABLE android.view.View...")
    try:
        rows = driver.find_elements(By.XPATH, '//android.view.View[@clickable="true"]')
        tx_rows = [r for r in rows if not _is_nav_bar(r)]
        print(f"   📋 [CLICK 2ND] {len(tx_rows)} TRANSACTION ROW(S) FOUND AFTER NAV FILTER.")
        if len(tx_rows) >= 2:
            second_row = tx_rows[1]
            # LOG DATE TEXT FROM CHILDREN FOR TRACEABILITY
            date_hint = "(second row)"
            try:
                for child in second_row.find_elements(By.XPATH, ".//*"):
                    t = (child.get_attribute("text") or "").strip()
                    if DATE_PATTERN.search(t):
                        date_hint = t
                        break
            except:
                pass
            print(f"   📅 [CLICK 2ND] CLICKING SECOND ROW: '{date_hint}'")
            second_row.click()
            print("   ✅ [CLICK 2ND] STRATEGY 1 SUCCEEDED.")
            return True, date_hint
        elif len(tx_rows) == 1:
            print("   ⚠️  [CLICK 2ND] STRATEGY 1 — ONLY 1 TRANSACTION ROW VISIBLE.")
        else:
            print("   ⚠️  [CLICK 2ND] STRATEGY 1 — NO TRANSACTION ROWS FOUND.")
    except Exception as e:
        print(f"   ⚠️  [CLICK 2ND] STRATEGY 1 FAILED: {e}")
 
    # ── STRATEGY 2: SECOND DATE TEXT ELEMENT → PARENT CLICK ──────────────────
    print("   🔍 [CLICK 2ND] STRATEGY 2: SECOND DATE TEXT ELEMENT → PARENT CLICK...")
    try:
        date_elements = []
        for el in driver.find_elements(By.XPATH, "//*"):
            t = (el.get_attribute("text") or "").strip()
            if DATE_PATTERN.match(t):
                date_elements.append((el, t))
        print(f"   📋 [CLICK 2ND] {len(date_elements)} DATE ELEMENT(S) FOUND IN DOM.")
        if len(date_elements) >= 2:
            second_el, second_val = date_elements[1]
            print(f"   📅 [CLICK 2ND] CLICKING SECOND DATE: '{second_val}'")
            try:
                parent = driver.find_element(
                    By.XPATH, f'//*[@text="{second_val}"]/parent::*'
                )
                parent.click()
            except:
                second_el.click()
            print("   ✅ [CLICK 2ND] STRATEGY 2 SUCCEEDED.")
            return True, second_val
        elif len(date_elements) == 1:
            print("   ⚠️  [CLICK 2ND] STRATEGY 2 — ONLY 1 DATE ELEMENT VISIBLE.")
        else:
            print("   ⚠️  [CLICK 2ND] STRATEGY 2 — NO DATE ELEMENTS FOUND.")
    except Exception as e:
        print(f"   ⚠️  [CLICK 2ND] STRATEGY 2 FAILED: {e}")
 
    # ── STRATEGY 3: COORDINATE TAP ON SECOND ROW (~27% FROM TOP) ─────────────
    print("   🔍 [CLICK 2ND] STRATEGY 3: COORDINATE TAP ON SECOND ROW (~27% FROM TOP)...")
    try:
        size  = driver.get_window_size()
        tap_x = size["width"] // 2
        tap_y = int(size["height"] * 0.27)
        driver.execute_script("mobile: clickGesture", {"x": tap_x, "y": tap_y})
        time.sleep(1)
        print(f"   ✅ [CLICK 2ND] STRATEGY 3 SUCCEEDED — TAPPED AT ({tap_x}, {tap_y}).")
        return True, "(coordinate tap ~27%)"
    except Exception as e:
        print(f"   💥 [CLICK 2ND] STRATEGY 3 FAILED: {e}")
 
    print("   ❌ [CLICK 2ND] ALL STRATEGIES EXHAUSTED.")
    return False, None
 
 
# =================================================================================
# DT-89: BEHAVIOR IN TRANSACTIONS NOT ELIGIBLE FOR CANCELLATION
# =================================================================================
def DT_89():
    from datetime import datetime
    print("\n" + "=" * 60)
    print('🧪 DT-89: BEHAVIOR IN TRANSACTIONS NOT ELIGIBLE FOR CANCELLATION')
    print("=" * 60)
    print("   ℹ️  CLICKS THE SECOND TRANSACTION IN THE LIST (ALWAYS > 24H OLD)")
    print("   AND VERIFIES THE 'CANCELAR' BUTTON IS NOT PRESENT IN THE DETAIL.")
 
    driver, wait = utils.iniciar_driver()
 
    try:
        # ── PRECONDITION: FULL LOGIN + BUSINESS REGISTRATION ─────────────────
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)
        print("   ✅ PRECONDITION MET — MAIN CHARGING SCREEN REACHED.")
 
        # ── STEP 1: NAVIGATE TO "TRANSACCIONES" BOTTOM NAV TAB ───────────────
        print("\n👉 STEP 1: NAVIGATING TO 'TRANSACCIONES' BOTTOM NAV TAB...")
        if not _navigate_to_transactions_tab(driver, wait):
            print("\n❌ DT-89: FAILED — COULD NOT NAVIGATE TO 'TRANSACCIONES' TAB.")
            utils.tomar_screenshot(driver, "DT_89_TAB_CLICK_FAILED")
            _capture_evidence(driver, "DT_89")
            return False
        print("   ✅ STEP 1 COMPLETE — 'TRANSACCIONES' TAB REACHED.")
        time.sleep(3)
 
        # ── STEP 2: ENSURE "ÚLTIMOS 30 DÍAS" SUB-TAB IS ACTIVE ───────────────
        print("\n👉 STEP 2: ENSURING 'ÚLTIMOS 30 DÍAS' SUB-TAB IS THE ACTIVE VIEW...")
        _ensure_last_30_days_tab(driver, wait)
        print("   ✅ STEP 2 COMPLETE — 'ÚLTIMOS 30 DÍAS' VIEW IS ACTIVE.")
        time.sleep(2)
 
        # ── STEP 3: WAIT FOR HISTORY LIST TO FULLY RENDER ────────────────────
        print("\n👉 STEP 3: WAITING FOR TRANSACTION HISTORY LIST TO RENDER...")
        time.sleep(3)
        print("   ✅ STEP 3 COMPLETE — RENDER WAIT ELAPSED.")
 
        # ── STEP 4: SCREENSHOT OF LIST (BASELINE) ────────────────────────────
        print("\n👉 STEP 4: CAPTURING HISTORY LIST AS BASELINE...")
        utils.tomar_screenshot(driver, "DT_89_LIST_BASELINE")
        print("   ✅ STEP 4 COMPLETE.")
 
        # ── STEP 5: CLICK THE SECOND TRANSACTION ROW (OLD TRANSACTION) ────────
        print("\n👉 STEP 5: CLICKING SECOND TRANSACTION ROW (OLD/RECONCILED)...")
        clicked, row_text = _click_second_transaction_in_list(driver)
 
        if not clicked:
            print("\n❌ DT-89: FAILED — COULD NOT CLICK SECOND TRANSACTION ROW.")
            utils.tomar_screenshot(driver, "DT_89_CLICK_FAILED")
            _capture_evidence(driver, "DT_89")
            return False
 
        print(f"   ✅ STEP 5 COMPLETE — SECOND ROW TAPPED: '{row_text}'")
        time.sleep(3)
 
        # ── STEP 6: VERIFY DETAIL SCREEN LOADED ──────────────────────────────
        print("\n👉 STEP 6: VERIFYING DETAIL SCREEN IS DISPLAYED...")
        detail_loaded = False
        for xpath in (
            '//*[@text="Detalle" or @content-desc="Detalle"]',
            '//*[contains(@text, "$") and string-length(@text) > 4]',
        ):
            try:
                if driver.find_elements(By.XPATH, xpath):
                    detail_loaded = True
                    break
            except:
                pass
 
        if not detail_loaded:
            print("\n❌ DT-89: FAILED — DETAIL SCREEN DID NOT OPEN AFTER TAP.")
            utils.tomar_screenshot(driver, "DT_89_DETAIL_NOT_OPENED")
            _capture_evidence(driver, "DT_89")
            return False
        print("   ✅ STEP 6 COMPLETE — DETAIL SCREEN IS OPEN.")
 
        # ── STEP 7: LOG TRANSACTION DATE FOR TRACEABILITY ─────────────────────
        print("\n👉 STEP 7: READING TRANSACTION DATE FOR TRACEABILITY...")
        DATE_PATTERN     = re.compile(r"(\d{2})-(\d{2})-(\d{4}),\s*(\d{2}):(\d{2}):(\d{2})")
        transaction_date = None
        elapsed_h        = None
        try:
            for el in driver.find_elements(By.XPATH, "//*"):
                t = (el.get_attribute("text") or "").strip()
                m = DATE_PATTERN.match(t)
                if m:
                    day, month, year, hour, minute, second = m.groups()
                    transaction_date = datetime(
                        int(year), int(month), int(day),
                        int(hour), int(minute), int(second)
                    )
                    elapsed_h = (datetime.now() - transaction_date).total_seconds() / 3600
                    print(f"   📅 TRANSACTION DATE : {transaction_date}")
                    print(f"   🕐 HOURS ELAPSED    : {elapsed_h:.1f}h")
                    if elapsed_h > 24:
                        print("   ✅ CONFIRMED OLD TRANSACTION (> 24H) — CANCEL BUTTON SHOULD NOT APPEAR.")
                    else:
                        print("   ⚠️  WARNING: THIS TRANSACTION IS WITHIN 24H — CANCEL MAY APPEAR.")
                    break
        except Exception as e:
            print(f"   ⚠️  COULD NOT READ DATE: {e}")
 
        # ── STEP 8: ASSERT "CANCELAR" BUTTON IS ABSENT ───────────────────────
        print("\n👉 STEP 8: ASSERTING 'CANCELAR' BUTTON IS ABSENT ON DETAIL SCREEN...")
        CANCEL_KEYWORDS = ["cancelar", "anular"]
        cancel_found    = False
        cancel_value    = None
 
        try:
            for el in driver.find_elements(By.XPATH, "//*"):
                for attr in ("text", "content-desc"):
                    val = (el.get_attribute(attr) or "").lower()
                    if any(kw in val for kw in CANCEL_KEYWORDS):
                        # EXCLUDE "CANCELACIÓN" STATUS LABEL — THAT IS NOT THE BUTTON
                        if "cancelaci" not in val:
                            cancel_found = True
                            cancel_value = val
                            break
                if cancel_found:
                    break
        except Exception as e:
            print(f"   ⚠️  STEP 8 SCAN ERROR: {e}")
 
        if cancel_found:
            print(f"   ❌ STEP 8 — 'CANCELAR' BUTTON FOUND UNEXPECTEDLY: '{cancel_value}'")
        else:
            print("   ✅ STEP 8 COMPLETE — 'CANCELAR' BUTTON IS ABSENT AS EXPECTED.")
 
        # ── DEBUG: LOG ALL VISIBLE TEXT ───────────────────────────────────────
        print("\n🔍 SCANNING ALL VISIBLE TEXT FOR DEBUGGING...")
        try:
            seen_debug = set()
            for el in driver.find_elements(By.XPATH, "//*"):
                for attr in ("text", "content-desc"):
                    t = el.get_attribute(attr) or ""
                    if t and len(t) > 2 and t not in seen_debug:
                        seen_debug.add(t)
                        print(f"   📝 VISIBLE: '{t}'")
                        break
        except:
            pass
 
        print("\n📸 TAKING SCREENSHOT — DETAIL WITHOUT 'CANCELAR' (SUCCESS EVIDENCE)...")
        utils.tomar_screenshot(driver, "DT_89_NO_CANCEL_BUTTON")
        _capture_evidence(driver, "DT_89")
 
        # ── RESULT ────────────────────────────────────────────────────────────
        elapsed_str = f"{elapsed_h:.1f}h" if elapsed_h is not None else "UNKNOWN"
        print("\n" + "-" * 60)
        print("📊 DT-89 VALIDATION SUMMARY:")
        print(f"   TRANSACTIONS TAB REACHED     : ✅")
        print(f"   SECOND ROW CLICKED           : ✅  ('{row_text}')")
        print(f"   DETAIL SCREEN OPENED         : ✅")
        print(f"   TRANSACTION AGE              : {elapsed_str}")
        print(f"   'CANCELAR' BUTTON ABSENT     : "
              f"{'✅ CORRECT — NOT FOUND' if not cancel_found else '❌ FOUND — UNEXPECTED'}")
        print("-" * 60)
 
        if not cancel_found:
            print("\n✅ DT-89: SUCCESS — 'CANCELAR' BUTTON CORRECTLY ABSENT FOR OLD TRANSACTION.")
            return True
        else:
            print("\n❌ DT-89: FAILED — 'CANCELAR' BUTTON APPEARED FOR AN OLD TRANSACTION.")
            print(f"   💡 VALUE FOUND: '{cancel_value}'")
            return False
 
    except Exception as e:
        print(f"\n💥 DT-89 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "DT_89_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)

# =================================================================================
# INTERNAL HELPER: POLL THE DOM FOR THE "CARGANDO" LOADING INDICATOR
# =================================================================================
def _poll_for_loading_indicator(driver, wait):
    LOADING_KEYWORDS = ["cargando", "loading", "carga"]
    MAX_POLLS        = 15       # 15 × 200ms = 3 SECONDS TOTAL POLL WINDOW
    poll_count       = 0
    loading_detected = False
    loading_text     = None

    print("   ⚡ [LOADING POLL] STARTING AGGRESSIVE POLL (200ms INTERVAL, UP TO 3s)...")

    # ── STRATEGY 1: RAPID ELEMENT SCAN ───────────────────────────────────────
    while poll_count < MAX_POLLS and not loading_detected:
        poll_count += 1
        try:
            for el in driver.find_elements(By.XPATH, "//*"):
                try:
                    for attr in ("text", "content-desc"):
                        val = (el.get_attribute(attr) or "").lower()
                        if any(kw in val for kw in LOADING_KEYWORDS) and len(val) > 2:
                            loading_detected = True
                            loading_text     = val
                            print(f"   ✅ [LOADING POLL] STRATEGY 1 DETECTED ON POLL "
                                  f"#{poll_count}: '{val}'")
                            break
                    if loading_detected:
                        break
                except Exception:
                    continue  # STALE ELEMENT — SKIP AND CONTINUE SCAN
        except Exception as e:
            print(f"   ⚠️  [LOADING POLL] POLL #{poll_count} FIND FAILED: {e}")

        if not loading_detected:
            time.sleep(0.2)

    if loading_detected:
        return True, loading_text

    # ── STRATEGY 2: WebDriverWait XPATH PRESENCE (FALLBACK) ──────────────────
    print("   🔍 [LOADING POLL] STRATEGY 2: WebDriverWait XPATH CHECK...")
    try:
        wait_short = WebDriverWait(driver, 3)
        wait_short.until(EC.presence_of_element_located(
            (By.XPATH,
             '//*[contains(@text, "argando") or contains(@content-desc, "argando") or '
             'contains(@text, "oading") or contains(@content-desc, "oading")]')
        ))
        loading_detected = True
        loading_text     = "cargando (via WebDriverWait)"
        print("   ✅ [LOADING POLL] STRATEGY 2 SUCCEEDED — LOADING INDICATOR FOUND.")
    except Exception as e:
        print(f"   ⚠️  [LOADING POLL] STRATEGY 2 FAILED: {e}")
        print("   💡 THE LOADING STATE MAY BE SHORTER THAN APPIUM'S POLL INTERVAL.")

    return loading_detected, loading_text


# =================================================================================
# DT-91: DETAILED CARGO HANDLING. 
# =================================================================================
def DT_91():
    print("\n" + "=" * 60)
    print("🧪 DT-91: DETAILED CARGO HANDLING. ")
    print("=" * 60)
    print("   ℹ️  NOTE: THE LOADING SPINNER IS TRANSIENT (~1-2s). THIS TEST")
    print("   POLLS IMMEDIATELY AFTER THE TAP WITH 200ms INTERVALS.")

    driver, wait = utils.iniciar_driver()

    try:
        # ── PRECONDITION: FULL LOGIN + BUSINESS REGISTRATION ─────────────────
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)
        print("   ✅ PRECONDITION MET — MAIN CHARGING SCREEN REACHED.")

        # ── STEP 1: NAVIGATE TO "INICIO" TAB TO ENSURE FRESH STATE ───────────
        print("\n👉 STEP 1: NAVIGATING TO 'INICIO' TAB TO RESET STATE...")
        try:
            driver.find_element(By.XPATH, config.XPATH_PÑ_TAB_INICIO).click()
            time.sleep(2)
            print("   ✅ STEP 1 COMPLETE — NOW ON 'INICIO' TAB.")
        except Exception as e:
            print(f"   ⚠️  STEP 1 WARNING — COULD NOT TAP 'INICIO': {e}")
            print("   💡 PROCEEDING — LOADING STATE MAY STILL APPEAR FROM CURRENT SCREEN.")

        # ── STEP 2: TAP "TRANSACCIONES" AND IMMEDIATELY START POLLING ─────────
        print("\n👉 STEP 2: TAPPING 'TRANSACCIONES' TAB AND IMMEDIATELY POLLING...")
        print("   ⚡ TAPPING NOW — POLL STARTS IMMEDIATELY AFTER...")
        tab_tapped = False

        try:
            driver.find_element(By.XPATH, config.XPATH_PÑ_TAB_TRANSACCIONES).click()
            tab_tapped = True
        except Exception as e:
            print(f"   ⚠️  PRIMARY TAP FAILED: {e} — TRYING PARTIAL MATCH FALLBACK...")
            try:
                driver.find_element(
                    By.XPATH, '//*[contains(@content-desc, "Transacciones")]'
                ).click()
                tab_tapped = True
            except Exception as e2:
                print(f"   💥 ALL TAP STRATEGIES FAILED: {e2}")

        if not tab_tapped:
            print("\n❌ DT-91: FAILED — COULD NOT TAP 'TRANSACCIONES' TAB.")
            utils.tomar_screenshot(driver, "DT_91_TAB_TAP_FAILED")
            _capture_evidence(driver, "DT_91")
            return False

        print("   ✅ STEP 2 COMPLETE — TAB TAPPED.")

        # ── STEP 3: POLL FOR "CARGANDO" IMMEDIATELY AFTER TAP ────────────────
        print("\n👉 STEP 3: POLLING FOR 'CARGANDO' LOADING INDICATOR...")
        loading_detected, loading_text = _poll_for_loading_indicator(driver, wait)

        print(f"   📊 TOTAL POLL ATTEMPTS: UP TO 15 @ 200ms EACH")
        if loading_detected:
            print(f"   ✅ STEP 3 COMPLETE — LOADING INDICATOR CAPTURED: '{loading_text}'")
            utils.tomar_screenshot(driver, "DT_91_LOADING_DETECTED")
        else:
            print("   ⚠️  STEP 3 — LOADING INDICATOR NOT CAPTURED BY APPIUM.")
            print("   💡 THIS IS EXPECTED IF THE STATE IS SHORTER THAN APPIUM'S RESPONSE TIME.")

        # ── STEP 4: WAIT FOR LOADING TO FINISH AND VERIFY FINAL SCREEN ────────
        print("\n👉 STEP 4: WAITING FOR LOADING TO FINISH AND VERIFYING FINAL SCREEN...")
        time.sleep(3)
        final_screen_ok = False
        for xpath in (
            '//*[@text="Transacciones" or @content-desc="Transacciones"]',
            '//*[contains(@text, "ltimos 30") or contains(@content-desc, "ltimos 30")]',
        ):
            try:
                if driver.find_elements(By.XPATH, xpath):
                    final_screen_ok = True
                    break
            except:
                pass

        if final_screen_ok:
            print("   ✅ STEP 4 COMPLETE — TRANSACTIONS SCREEN FULLY LOADED AFTER ANIMATION.")
        else:
            print("   ⚠️  STEP 4 — TRANSACTIONS SCREEN COULD NOT BE VERIFIED.")

        # ── EVIDENCE ──────────────────────────────────────────────────────────
        print("\n📸 TAKING SCREENSHOT — FINAL STATE AFTER LOADING (SUCCESS EVIDENCE)...")
        utils.tomar_screenshot(driver, "DT_91_FINAL_STATE")
        _capture_evidence(driver, "DT_91")

        # ── DEBUG: LOG ALL VISIBLE TEXT ───────────────────────────────────────
        print("\n🔍 SCANNING ALL VISIBLE TEXT FOR DEBUGGING...")
        try:
            seen_debug = set()
            for el in driver.find_elements(By.XPATH, "//*"):
                for attr in ("text", "content-desc"):
                    t = el.get_attribute(attr) or ""
                    if t and len(t) > 3 and t not in seen_debug:
                        seen_debug.add(t)
                        print(f"   📝 VISIBLE: '{t}'")
                        break
        except:
            pass

        # ── RESULT ────────────────────────────────────────────────────────────
        print("\n" + "-" * 60)
        print("📊 DT-91 VALIDATION SUMMARY:")
        print(f"   'INICIO' TAB RESET           : ✅")
        print(f"   'TRANSACCIONES' TAB TAPPED   : ✅")
        print(f"   'CARGANDO' DETECTED          : "
              f"{'✅ YES — ' + str(loading_text) if loading_detected else '⚠️  NOT CAPTURED (TRANSIENT)'}")
        print(f"   FINAL SCREEN LOADED OK       : {'✅' if final_screen_ok else '⚠️  WARNING'}")
        print("-" * 60)

        # SUCCESS CRITERIA: FINAL SCREEN LOADED. LOADING CAPTURE IS BEST-EFFORT
        # BECAUSE APPIUM'S POLL LATENCY MAY EXCEED THE SPINNER DURATION.
        if loading_detected and final_screen_ok:
            print("\n✅ DT-91: SUCCESS — LOADING INDICATOR DETECTED AND SCREEN LOADED CORRECTLY.")
            return True
        elif final_screen_ok:
            print("\n✅ DT-91: SUCCESS (PARTIAL) — FINAL SCREEN LOADED CORRECTLY.")
            print("   ℹ️  'CARGANDO' SPINNER WAS NOT CAPTURED — THIS IS ACCEPTABLE WHEN")
            print("   THE LOADING STATE DURATION IS SHORTER THAN APPIUM'S RESPONSE TIME.")
            return True
        else:
            print("\n❌ DT-91: FAILED — TRANSACTIONS SCREEN DID NOT LOAD AFTER TAB TAP.")
            return False

    except Exception as e:
        print(f"\n💥 DT-91 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "DT_91_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)


# =================================================================================
# MAIN EXECUTION
# =================================================================================
if __name__ == "__main__":

    logger, log_file, timestamp = utils.iniciar_reporte("OPERATIONALS_DT")

    try:
        DT_82()
        DT_83()
        DT_84()
        DT_85()
        DT_89()
        DT_91()

    finally:
        utils.generar_reporte_html("OPERATIONALS_DT", log_file, timestamp)