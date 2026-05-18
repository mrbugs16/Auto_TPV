"""
FILENAME: Operationals_CT.py
DESCRIPTION:
    VALIDATES THE "COMPARTIR COMPROBANTE" (SHARE RECEIPT) FUNCTIONALITY
    FROM THE TRANSACTION DETAIL SCREEN OF THE MEMPHIS APP.
    NAVIGATES TO THE MOST RECENT TRANSACTION AND TESTS EACH SHARING CHANNEL.

CONTENTS:
    · CT-86: SHARE RECEIPT FEATURE (EMAIL)
    · CT-87: SHARE RECEIPT FEATURE (WHATSAPP)
    · CT-88: SHARE RECEIPT FEATURE (SMS)

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
try:
    from appium.webdriver.common.appiumby import AppiumBy
except ImportError:
    
    class AppiumBy:
        ANDROID_UIAUTOMATOR = "android uiAutomator"


# =================================================================================
# TEST DATA — SHARE RECEIPT DESTINATIONS
# =================================================================================
CT_EMAIL_ADDRESS    = "santiago.tapia@memphis.mx"   # EMAIL RECIPIENT FOR CT-86
CT_WHATSAPP_NUMBER  = "5580049837"                  # WHATSAPP NUMBER FOR CT-87
CT_SMS_NUMBER       = "5580049837"                  # SMS NUMBER FOR CT-88

# SUCCESS / FAILURE MESSAGE FRAGMENTS USED FOR VALIDATION
CT_SUCCESS_FRAGMENT = "sido enviado"                # FRAGMENT OF SUCCESS MESSAGE
CT_FAILURE_FRAGMENT = "no fue posible"              # FRAGMENT OF FAILURE MESSAGE


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
            By.XPATH, '//*[contains(@content-desc, "Transacciones")]'
        ).click()
        time.sleep(2)
        print("   ✅ [NAV] STRATEGY 2 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [NAV] STRATEGY 2 FAILED: {e}")

    print("   🔍 [NAV] ATTEMPTING STRATEGY 3: EXACT TEXT / CONTENT-DESC MATCH...")
    try:
        driver.find_element(
            By.XPATH, '//*[@text="Transacciones" or @content-desc="Transacciones"]'
        ).click()
        time.sleep(2)
        print("   ✅ [NAV] STRATEGY 3 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [NAV] STRATEGY 3 FAILED: {e}")

    print("   🔍 [NAV] ATTEMPTING STRATEGY 4: UIAUTOMATOR TEXT SEARCH (FINAL FALLBACK)...")
    try:
        driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
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
def _last_30_days_tab_(driver, wait):
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
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains("30")'
        ).click()
        time.sleep(2)
        print("   ✅ [SUB-TAB] STRATEGY 3 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   💥 [SUB-TAB] STRATEGY 3 FAILED: {e}")

    print("   ⚠️  [SUB-TAB] ALL STRATEGIES FAILED — ASSUMING DEFAULT VIEW IS ALREADY ACTIVE.")
    return False


# =================================================================================
# INTERNAL HELPER: CLICK THE FIRST (MOST RECENT) TRANSACTION IN THE LIST

# =================================================================================
def _click_first_transaction_in_list(driver):
    DATE_PATTERN = re.compile(r"\d{2}-\d{2}-\d{4},\s*\d{2}:\d{2}:\d{2}")

    print("   🔍 [CLICK FIRST] STRATEGY 1: DATE TEXT → WALK UP TO CLICKABLE PARENT ROW...")
    try:
        date_element = None
        for el in driver.find_elements(By.XPATH, "//*"):
            t = (el.get_attribute("text") or "").strip()
            if DATE_PATTERN.match(t):
                date_element = el
                print(f"   📅 [CLICK FIRST] DATE TEXT FOUND: '{t}'")
                break

        if date_element:
            clicked = driver.execute_script("""
                var el = arguments[0];
                for (var i = 0; i < 6; i++) {
                    if (!el.parentElement) break;
                    el = el.parentElement;
                    if (el.onclick || el.getAttribute('clickable') === 'true') {
                        el.click();
                        return true;
                    }
                }
                if (arguments[0].parentElement) {
                    arguments[0].parentElement.click();
                    return true;
                }
                return false;
            """, date_element)

            if clicked:
                print("   ✅ [CLICK FIRST] STRATEGY 1 SUCCEEDED — CLICKED PARENT CARD.")
                return True

            # NATIVE PARENT FALLBACK
            try:
                parent = driver.find_element(
                    By.XPATH,
                    f'//*[@text="{date_element.get_attribute("text")}"]/parent::*'
                )
                parent.click()
                print("   ✅ [CLICK FIRST] STRATEGY 1 (NATIVE PARENT) SUCCEEDED.")
                return True
            except Exception as pe:
                print(f"   ⚠️  [CLICK FIRST] NATIVE PARENT FAILED: {pe}")
    except Exception as e:
        print(f"   ⚠️  [CLICK FIRST] STRATEGY 1 FAILED: {e}")

    print("   🔍 [CLICK FIRST] STRATEGY 2: UIAUTOMATOR CLICKABLE ROW WITH DATE...")
    try:
        driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().clickable(true).descriptionMatches(".*\\d{2}-\\d{2}-\\d{4}.*")'
        ).click()
        print("   ✅ [CLICK FIRST] STRATEGY 2 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [CLICK FIRST] STRATEGY 2 FAILED: {e}")

    print("   🔍 [CLICK FIRST] STRATEGY 3: FIRST CLICKABLE android.view.View IN LIST...")
    try:
        rows = driver.find_elements(By.XPATH, '//android.view.View[@clickable="true"]')
        if rows:
            rows[0].click()
            print("   ✅ [CLICK FIRST] STRATEGY 3 SUCCEEDED.")
            return True
        print("   ⚠️  [CLICK FIRST] STRATEGY 3 — NO CLICKABLE VIEWS FOUND.")
    except Exception as e:
        print(f"   ⚠️  [CLICK FIRST] STRATEGY 3 FAILED: {e}")

    print("   🔍 [CLICK FIRST] STRATEGY 4: COORDINATE TAP ON FIRST ROW (y≈22%)...")
    try:
        size  = driver.get_window_size()
        tap_x = size["width"] // 2
        tap_y = int(size["height"] * 0.22)
        driver.execute_script("mobile: clickGesture", {"x": tap_x, "y": tap_y})
        time.sleep(1)
        print(f"   ✅ [CLICK FIRST] STRATEGY 4 SUCCEEDED — TAPPED AT ({tap_x}, {tap_y}).")
        return True
    except Exception as e:
        print(f"   💥 [CLICK FIRST] STRATEGY 4 FAILED: {e}")

    print("   ❌ [CLICK FIRST] ALL STRATEGIES EXHAUSTED — NO TRANSACTION ROW CLICKABLE.")
    return False


# =================================================================================
# INTERNAL HELPER: CLICK A SHARE BUTTON BY CHANNEL NAME
# =================================================================================
def _click_share_button(driver, channel_name):
    print(f"   🔍 [SHARE BTN] STRATEGY 1: EXACT MATCH '{channel_name}'...")
    try:
        elements = driver.find_elements(
            By.XPATH,
            f'//*[@text="{channel_name}" or @content-desc="{channel_name}"]'
        )
        if elements:
            elements[0].click()
            print(f"   ✅ [SHARE BTN] STRATEGY 1 SUCCEEDED — CLICKED '{channel_name}'.")
            return True
        print(f"   ⚠️  [SHARE BTN] STRATEGY 1 — NO EXACT MATCH FOR '{channel_name}'.")
    except Exception as e:
        print(f"   ⚠️  [SHARE BTN] STRATEGY 1 FAILED: {e}")

    # USE A PARTIAL FRAGMENT TO AVOID CASE / ENCODING ISSUES
    fragment = channel_name[:4]
    print(f"   🔍 [SHARE BTN] STRATEGY 2: PARTIAL CONTAINS MATCH '{fragment}'...")
    try:
        elements = driver.find_elements(
            By.XPATH,
            f'//*[contains(@text, "{fragment}") or contains(@content-desc, "{fragment}")]'
        )
        if elements:
            elements[0].click()
            print(f"   ✅ [SHARE BTN] STRATEGY 2 SUCCEEDED — FRAGMENT: '{fragment}'.")
            return True
        print(f"   ⚠️  [SHARE BTN] STRATEGY 2 — NO PARTIAL MATCH FOR '{fragment}'.")
    except Exception as e:
        print(f"   ⚠️  [SHARE BTN] STRATEGY 2 FAILED: {e}")

    print(f"   🔍 [SHARE BTN] STRATEGY 3: UIAUTOMATOR textContains '{fragment}'...")
    try:
        driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().textContains("{fragment}")'
        ).click()
        print(f"   ✅ [SHARE BTN] STRATEGY 3 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   💥 [SHARE BTN] STRATEGY 3 FAILED: {e}")

    print(f"   ❌ [SHARE BTN] ALL STRATEGIES EXHAUSTED — '{channel_name}' BUTTON NOT FOUND.")
    return False


# =================================================================================
# INTERNAL HELPER: ENTER DESTINATION AND TAP "ENVIAR" IN THE SHARE MODAL
# =================================================================================
def _enter_destination_and_send(driver, destination):
    print(f"   🔍 [SEND MODAL] WAITING FOR MODAL INPUT TO APPEAR...")
    time.sleep(2)

    # LOCATE THE INPUT FIELD — TRY EditText FIRST, THEN ANY FOCUSABLE ELEMENT
    def _find_input_field():
        fields = driver.find_elements(By.XPATH, "//android.widget.EditText")
        if fields:
            return fields[0]
        fields = driver.find_elements(By.XPATH, '//*[@focusable="true" and @clickable="true"]')
        if fields:
            return fields[0]
        return None
    print(f"   🔍 [SEND MODAL] STRATEGY 1: TRIPLE TAP SELECT ALL → SEND_KEYS...")
    try:
        field = _find_input_field()
        if field:
            # FIRST CLICK TO FOCUS
            field.click()
            time.sleep(0.5)
            # CLEAR ANY EXISTING VALUE WITH clear() FIRST
            try:
                field.clear()
                time.sleep(0.3)
            except:
                pass
            # TRIPLE TAP TO ENSURE CURSOR IS AT END AND ANY REMNANT IS SELECTED
            field.click()
            time.sleep(0.2)
            field.click()
            time.sleep(0.2)
            field.click()
            time.sleep(0.3)
            # NOW TYPE THE DESTINATION — FIELD SHOULD BE EMPTY AFTER clear()
            field.send_keys(destination)
            time.sleep(0.5)
            actual = (field.get_attribute("text") or "").strip()
            print(f"   ✏️  [SEND MODAL] STRATEGY 1 TYPED. FIELD VALUE: '{actual}'")
            if destination.strip() in actual or actual == destination.strip():
                try:
                    driver.hide_keyboard()
                except:
                    pass
                time.sleep(1)
                send_btn = driver.find_elements(
                    By.XPATH, '//*[@text="Enviar" or @content-desc="Enviar"]'
                )
                if send_btn:
                    send_btn[0].click()
                    print("   ✅ [SEND MODAL] STRATEGY 1 SUCCEEDED — 'Enviar' TAPPED.")
                    return True
                print("   ⚠️  [SEND MODAL] STRATEGY 1 — 'Enviar' NOT FOUND AFTER TYPING.")
            else:
                print(f"   ⚠️  [SEND MODAL] STRATEGY 1 — FIELD VALUE MISMATCH: '{actual}'")
        else:
            print("   ⚠️  [SEND MODAL] STRATEGY 1 — NO INPUT FIELD FOUND.")
    except Exception as e:
        print(f"   ⚠️  [SEND MODAL] STRATEGY 1 FAILED: {e}")

    # ── STRATEGY 2: CLICK → CLEAR VIA KEYCODE 67 LOOP → send_keys ────────────
    print(f"   🔍 [SEND MODAL] STRATEGY 2: CLEAR VIA KEYCODE 67 LOOP → SEND_KEYS...")
    try:
        field = _find_input_field()
        if field:
            field.click()
            time.sleep(1)
            # PRESS BACKSPACE UP TO 30 TIMES TO CLEAR ANY PRE-FILLED VALUE
            for _ in range(30):
                driver.press_keycode(67)
            time.sleep(0.5)
            field.send_keys(destination)
            time.sleep(0.5)
            actual = field.get_attribute("text") or ""
            print(f"   ✏️  [SEND MODAL] STRATEGY 2 TYPED. FIELD VALUE: '{actual}'")
            if destination in actual or actual.strip() == destination.strip():
                try:
                    driver.hide_keyboard()
                except:
                    pass
                time.sleep(1)
                send_btn = driver.find_elements(
                    By.XPATH, '//*[@text="Enviar" or @content-desc="Enviar"]'
                )
                if send_btn:
                    send_btn[0].click()
                    print("   ✅ [SEND MODAL] STRATEGY 2 SUCCEEDED — 'Enviar' TAPPED.")
                    return True
                print("   ⚠️  [SEND MODAL] STRATEGY 2 — 'Enviar' NOT FOUND AFTER TYPING.")
            else:
                print(f"   ⚠️  [SEND MODAL] STRATEGY 2 — FIELD VALUE MISMATCH: '{actual}'")
        else:
            print("   ⚠️  [SEND MODAL] STRATEGY 2 — NO INPUT FIELD FOUND.")
    except Exception as e:
        print(f"   ⚠️  [SEND MODAL] STRATEGY 2 FAILED: {e}")

    # ── STRATEGY 3: set_value VIA APPIUM EXECUTE_SCRIPT ──────────────────────
    print(f"   🔍 [SEND MODAL] STRATEGY 3: set_value VIA execute_script...")
    try:
        field = _find_input_field()
        if field:
            field.click()
            time.sleep(1)
            driver.execute_script(
                "mobile: replaceElementValue",
                {"elementId": field.id, "value": destination}
            )
            time.sleep(0.5)
            actual = field.get_attribute("text") or ""
            print(f"   ✏️  [SEND MODAL] STRATEGY 3 SET VALUE. FIELD: '{actual}'")
            try:
                driver.hide_keyboard()
            except:
                pass
            time.sleep(1)
            send_btn = driver.find_elements(
                By.XPATH, '//*[@text="Enviar" or @content-desc="Enviar"]'
            )
            if send_btn:
                send_btn[0].click()
                print("   ✅ [SEND MODAL] STRATEGY 3 SUCCEEDED — 'Enviar' TAPPED.")
                return True
            print("   ⚠️  [SEND MODAL] STRATEGY 3 — 'Enviar' NOT FOUND AFTER SET_VALUE.")
        else:
            print("   ⚠️  [SEND MODAL] STRATEGY 3 — NO INPUT FIELD FOUND.")
    except Exception as e:
        print(f"   ⚠️  [SEND MODAL] STRATEGY 3 FAILED: {e}")

    # ── STRATEGY 4: AppiumBy UIAUTOMATOR FIND + replaceText ACTION ───────────
    print(f"   🔍 [SEND MODAL] STRATEGY 4: AppiumBy UIAUTOMATOR replaceText...")
    try:
        input_el = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().className("android.widget.EditText").instance(0)'
        )
        input_el.click()
        time.sleep(0.5)
        # UIAUTOMATOR replaceText DIRECTLY SETS THE FIELD VALUE
        driver.execute_script(
            "mobile: replaceElementValue",
            {"elementId": input_el.id, "value": destination}
        )
        time.sleep(0.5)
        print(f"   ✏️  [SEND MODAL] STRATEGY 4 APPLIED replaceElementValue: '{destination}'")
        try:
            driver.hide_keyboard()
        except:
            pass
        time.sleep(1)
        send_btn = driver.find_elements(
            By.XPATH, '//*[@text="Enviar" or @content-desc="Enviar"]'
        )
        if send_btn:
            send_btn[0].click()
            print("   ✅ [SEND MODAL] STRATEGY 4 SUCCEEDED — 'Enviar' TAPPED.")
            return True
        # UIAUTOMATOR FIND "Enviar" AS FINAL FALLBACK
        driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Enviar")'
        ).click()
        print("   ✅ [SEND MODAL] STRATEGY 4 SUCCEEDED — 'Enviar' VIA UIAUTOMATOR.")
        return True
    except Exception as e:
        print(f"   💥 [SEND MODAL] STRATEGY 4 FAILED: {e}")

    print("   ❌ [SEND MODAL] ALL STRATEGIES EXHAUSTED — COULD NOT FILL AND SEND MODAL.")
    return False


# =================================================================================
# INTERNAL HELPER: DETECT SEND RESULT — SUCCESS OR FAILURE POPUP
# =================================================================================
def _detect_send_result(driver, test_name):
    print("   🔍 [RESULT DETECTOR] POLLING FOR SEND RESULT POPUP (UP TO 10s)...")
    max_polls    = 20
    poll_count   = 0
    result_found = "unknown"

    while poll_count < max_polls and result_found == "unknown":
        poll_count += 1
        try:
            combined = ""
            fresh_elements = driver.find_elements(By.XPATH, "//*")
            for el in fresh_elements:
                try:
                    for attr in ("text", "content-desc"):
                        v = (el.get_attribute(attr) or "").lower()
                        if v and len(v) > 2:
                            combined += " " + v
                except Exception:
                    # ELEMENT WENT STALE MID-ITERATION — SKIP IT AND CONTINUE
                    continue

            if CT_SUCCESS_FRAGMENT in combined:
                result_found = "success"
                print(f"   ✅ [RESULT DETECTOR] SUCCESS POPUP DETECTED ON POLL #{poll_count}.")
                break
            elif CT_FAILURE_FRAGMENT in combined:
                result_found = "failure"
                print(f"   ❌ [RESULT DETECTOR] FAILURE POPUP DETECTED ON POLL #{poll_count}.")
                break

        except Exception as e:
            # FULL FIND_ELEMENTS CALL FAILED — WAIT AND RETRY
            print(f"   ⚠️  [RESULT DETECTOR] POLL #{poll_count} FIND FAILED: {e}")

        time.sleep(0.5)

    if result_found == "unknown":
        print(f"   ⚠️  [RESULT DETECTOR] NO RESULT POPUP DETECTED AFTER {poll_count} POLLS.")

    return result_found


# =================================================================================
# INTERNAL HELPER: DISMISS RESULT POPUP BY TAPPING "Continuar"
# =================================================================================
def _dismiss_result_popup(driver):
    print("   🔍 [DISMISS] STRATEGY 1: EXACT MATCH 'Continuar'...")
    try:
        elements = driver.find_elements(
            By.XPATH, '//*[@text="Continuar" or @content-desc="Continuar"]'
        )
        if elements:
            elements[0].click()
            print("   ✅ [DISMISS] STRATEGY 1 SUCCEEDED — 'Continuar' TAPPED.")
            time.sleep(2)
            return True
        print("   ⚠️  [DISMISS] STRATEGY 1 — 'Continuar' NOT FOUND.")
    except Exception as e:
        print(f"   ⚠️  [DISMISS] STRATEGY 1 FAILED: {e}")

    print("   🔍 [DISMISS] STRATEGY 2: UIAUTOMATOR textContains 'ontinuar'...")
    try:
        driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains("ontinuar")'
        ).click()
        print("   ✅ [DISMISS] STRATEGY 2 SUCCEEDED.")
        time.sleep(2)
        return True
    except Exception as e:
        print(f"   💥 [DISMISS] STRATEGY 2 FAILED: {e}")

    print("   ⚠️  [DISMISS] COULD NOT DISMISS POPUP — CONTINUING ANYWAY.")
    return False


# =================================================================================
# INTERNAL HELPER: FULL NAVIGATION FLOW TO THE TRANSACTION DETAIL SCREEN
# =================================================================================
def _navigate_to_transaction_detail(driver, wait, test_name):
    # PHASE A: TRANSACTIONS TAB
    print(f"\n👉 [PRECONDITION] NAVIGATING TO 'TRANSACCIONES' TAB...")
    if not _navigate_to_transactions_tab(driver, wait):
        raise RuntimeError(f"{test_name}: FAILED — COULD NOT REACH 'TRANSACCIONES' TAB.")
    print("   ✅ 'TRANSACCIONES' TAB REACHED.")
    time.sleep(3)

    # PHASE B: ÚLTIMOS 30 DÍAS SUB-TAB
    print(f"\n👉 [PRECONDITION] ENSURING 'ÚLTIMOS 30 DÍAS' SUB-TAB IS ACTIVE...")
    _last_30_days_tab_(driver, wait)
    print("   ✅ 'ÚLTIMOS 30 DÍAS' VIEW IS ACTIVE.")
    time.sleep(2)

    # PHASE C: WAIT FOR LIST TO RENDER
    print(f"\n👉 [PRECONDITION] WAITING FOR HISTORY LIST TO RENDER...")
    time.sleep(3)

    # PHASE D: CLICK FIRST TRANSACTION
    print(f"\n👉 [PRECONDITION] CLICKING MOST RECENT TRANSACTION...")
    if not _click_first_transaction_in_list(driver):
        raise RuntimeError(f"{test_name}: FAILED — COULD NOT CLICK MOST RECENT TRANSACTION.")
    time.sleep(3)

    # PHASE E: VERIFY DETAIL SCREEN LOADED
    print(f"\n👉 [PRECONDITION] VERIFYING DETAIL SCREEN IS DISPLAYED...")
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
        raise RuntimeError(f"{test_name}: FAILED — DETAIL SCREEN DID NOT OPEN.")

    print("   ✅ DETAIL SCREEN IS OPEN AND READY.")


# =================================================================================
# CT-86: SHARE RECEIPT FEATURE (EMAIL)
# =================================================================================
def CT_86():
    print("\n" + "=" * 60)
    print("🧪 CT-86: SHARE RECEIPT FEATURE (EMAIL)")
    print("=" * 60)
    print(f"   📧 EMAIL DESTINATION: {CT_EMAIL_ADDRESS}")

    driver, wait = utils.iniciar_driver()

    try:
        # ── PRECONDITION: LOGIN + NAVIGATE TO DETAIL SCREEN ──────────────────
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)
        print("   ✅ PRECONDITION MET — MAIN CHARGING SCREEN REACHED.")

        _navigate_to_transaction_detail(driver, wait, "CT-86")
        print("   ✅ PRECONDITION COMPLETE — DETAIL SCREEN REACHED.")

        # ── STEP 1: SCREENSHOT OF DETAIL SCREEN (SHOWS SHARE SECTION) ─────────
        print("\n👉 STEP 1: CAPTURING DETAIL SCREEN SHOWING 'COMPARTIR COMPROBANTE'...")
        utils.tomar_screenshot(driver, "CT_86_DETAIL_SCREEN")
        print("   ✅ STEP 1 COMPLETE.")

        # ── STEP 2: CLICK THE "Email" SHARE BUTTON ────────────────────────────
        print("\n👉 STEP 2: CLICKING 'Email' SHARE BUTTON...")
        if not _click_share_button(driver, "Email"):
            print("\n❌ CT-86: FAILED — COULD NOT CLICK 'Email' SHARE BUTTON.")
            utils.tomar_screenshot(driver, "CT_86_EMAIL_BTN_FAILED")
            _capture_evidence(driver, "CT_86")
            return False
        print("   ✅ STEP 2 COMPLETE — 'Email' BUTTON TAPPED.")

        # ── STEP 3: FILL EMAIL AND TAP "Enviar" ───────────────────────────────
        print(f"\n👉 STEP 3: FILLING EMAIL '{CT_EMAIL_ADDRESS}' AND TAPPING 'Enviar'...")
        if not _enter_destination_and_send(driver, CT_EMAIL_ADDRESS):
            print("\n❌ CT-86: FAILED — COULD NOT FILL EMAIL OR TAP 'Enviar'.")
            utils.tomar_screenshot(driver, "CT_86_SEND_MODAL_FAILED")
            _capture_evidence(driver, "CT_86")
            return False
        print("   ✅ STEP 3 COMPLETE — 'Enviar' TAPPED.")

        # ── STEP 4: DETECT RESULT POPUP ───────────────────────────────────────
        print("\n👉 STEP 4: DETECTING SEND RESULT POPUP...")
        result = _detect_send_result(driver, "CT_86")

        # ── EVIDENCE: SCREENSHOT OF RESULT POPUP (SUCCESS OR FAILURE) ─────────
        print("\n📸 TAKING SCREENSHOT — SEND RESULT POPUP (PRIMARY EVIDENCE)...")
        utils.tomar_screenshot(driver, "CT_86_SEND_RESULT")
        _capture_evidence(driver, "CT_86")

        # ── DISMISS POPUP ─────────────────────────────────────────────────────
        if result != "unknown":
            _dismiss_result_popup(driver)

        # ── RESULT ────────────────────────────────────────────────────────────
        print("\n" + "-" * 60)
        print("📊 CT-86 VALIDATION SUMMARY:")
        print(f"   DETAIL SCREEN REACHED        : ✅")
        print(f"   'Email' BUTTON CLICKED       : ✅")
        print(f"   DESTINATION ENTERED          : ✅  ({CT_EMAIL_ADDRESS})")
        print(f"   RESULT POPUP DETECTED        : "
              f"{'✅ SUCCESS — TICKET SENT' if result == 'success' else '❌ FAILURE POPUP' if result == 'failure' else '⚠️  UNKNOWN'}")
        print("-" * 60)

        if result == "success":
            print("\n✅ CT-86: SUCCESS — RECEIPT SENT VIA EMAIL AND CONFIRMATION RECEIVED.")
            return True
        elif result == "failure":
            print("\n❌ CT-86: FAILED — 'Aviso: No fue posible enviar el ticket' POPUP APPEARED.")
            return False
        else:
            print("\n⚠️  CT-86: INCONCLUSIVE — NO RESULT POPUP WAS DETECTED.")
            return False

    except RuntimeError as nav_err:
        print(f"\n❌ {nav_err}")
        utils.tomar_screenshot(driver, "CT_86_NAV_FAILED")
        _capture_evidence(driver, "CT_86")
        return False
    except Exception as e:
        print(f"\n💥 CT-86 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "CT_86_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)


# =================================================================================
# CT-87: SHARE RECEIPT FEATURE (WHATSAPP)
# =================================================================================
def CT_87():
    print("\n" + "=" * 60)
    print("🧪 CT-87: SHARE RECEIPT FEATURE (WHATSAPP)")
    print("=" * 60)
    print(f"   📱 WHATSAPP DESTINATION: {CT_WHATSAPP_NUMBER}")

    driver, wait = utils.iniciar_driver()

    try:
        # ── PRECONDITION: LOGIN + NAVIGATE TO DETAIL SCREEN ──────────────────
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)
        print("   ✅ PRECONDITION MET — MAIN CHARGING SCREEN REACHED.")

        _navigate_to_transaction_detail(driver, wait, "CT-87")
        print("   ✅ PRECONDITION COMPLETE — DETAIL SCREEN REACHED.")

        # ── STEP 1: SCREENSHOT OF DETAIL SCREEN ───────────────────────────────
        print("\n👉 STEP 1: CAPTURING DETAIL SCREEN SHOWING 'COMPARTIR COMPROBANTE'...")
        utils.tomar_screenshot(driver, "CT_87_DETAIL_SCREEN")
        print("   ✅ STEP 1 COMPLETE.")

        # ── STEP 2: CLICK THE "WhatsApp" SHARE BUTTON ─────────────────────────
        print("\n👉 STEP 2: CLICKING 'WhatsApp' SHARE BUTTON...")
        if not _click_share_button(driver, "WhatsApp"):
            print("\n❌ CT-87: FAILED — COULD NOT CLICK 'WhatsApp' SHARE BUTTON.")
            utils.tomar_screenshot(driver, "CT_87_WHATSAPP_BTN_FAILED")
            _capture_evidence(driver, "CT_87")
            return False
        print("   ✅ STEP 2 COMPLETE — 'WhatsApp' BUTTON TAPPED.")

        # ── STEP 3: FILL PHONE NUMBER AND TAP "Enviar" ────────────────────────
        print(f"\n👉 STEP 3: FILLING NUMBER '{CT_WHATSAPP_NUMBER}' AND TAPPING 'Enviar'...")
        if not _enter_destination_and_send(driver, CT_WHATSAPP_NUMBER):
            print("\n❌ CT-87: FAILED — COULD NOT FILL NUMBER OR TAP 'Enviar'.")
            utils.tomar_screenshot(driver, "CT_87_SEND_MODAL_FAILED")
            _capture_evidence(driver, "CT_87")
            return False
        print("   ✅ STEP 3 COMPLETE — 'Enviar' TAPPED.")

        # ── STEP 4: DETECT RESULT POPUP ───────────────────────────────────────
        print("\n👉 STEP 4: DETECTING SEND RESULT POPUP...")
        result = _detect_send_result(driver, "CT_87")

        # ── EVIDENCE: SCREENSHOT OF RESULT POPUP ──────────────────────────────
        print("\n📸 TAKING SCREENSHOT — SEND RESULT POPUP (PRIMARY EVIDENCE)...")
        utils.tomar_screenshot(driver, "CT_87_SEND_RESULT")
        _capture_evidence(driver, "CT_87")

        if result != "unknown":
            _dismiss_result_popup(driver)

        # ── RESULT ────────────────────────────────────────────────────────────
        print("\n" + "-" * 60)
        print("📊 CT-87 VALIDATION SUMMARY:")
        print(f"   DETAIL SCREEN REACHED        : ✅")
        print(f"   'WhatsApp' BUTTON CLICKED    : ✅")
        print(f"   DESTINATION ENTERED          : ✅  ({CT_WHATSAPP_NUMBER})")
        print(f"   RESULT POPUP DETECTED        : "
              f"{'✅ SUCCESS — TICKET SENT' if result == 'success' else '❌ FAILURE POPUP' if result == 'failure' else '⚠️  UNKNOWN'}")
        print("-" * 60)

        if result == "success":
            print("\n✅ CT-87: SUCCESS — RECEIPT SENT VIA WHATSAPP AND CONFIRMATION RECEIVED.")
            return True
        elif result == "failure":
            print("\n❌ CT-87: FAILED — 'Aviso: No fue posible enviar el ticket' POPUP APPEARED.")
            return False
        else:
            print("\n⚠️  CT-87: INCONCLUSIVE — NO RESULT POPUP WAS DETECTED.")
            return False

    except RuntimeError as nav_err:
        print(f"\n❌ {nav_err}")
        utils.tomar_screenshot(driver, "CT_87_NAV_FAILED")
        _capture_evidence(driver, "CT_87")
        return False
    except Exception as e:
        print(f"\n💥 CT-87 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "CT_87_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)


# =================================================================================
# CT-88: SHARE RECEIPT FEATURE (SMS)
# =================================================================================
def CT_88():
    print("\n" + "=" * 60)
    print("🧪 CT-88: SHARE RECEIPT FEATURE (SMS)")
    print("=" * 60)
    print(f"   💬 SMS DESTINATION: {CT_SMS_NUMBER}")

    driver, wait = utils.iniciar_driver()

    try:
        # ── PRECONDITION: LOGIN + NAVIGATE TO DETAIL SCREEN ──────────────────
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)
        print("   ✅ PRECONDITION MET — MAIN CHARGING SCREEN REACHED.")

        _navigate_to_transaction_detail(driver, wait, "CT-88")
        print("   ✅ PRECONDITION COMPLETE — DETAIL SCREEN REACHED.")

        # ── STEP 1: SCREENSHOT OF DETAIL SCREEN ───────────────────────────────
        print("\n👉 STEP 1: CAPTURING DETAIL SCREEN SHOWING 'COMPARTIR COMPROBANTE'...")
        utils.tomar_screenshot(driver, "CT_88_DETAIL_SCREEN")
        print("   ✅ STEP 1 COMPLETE.")

        # ── STEP 2: CLICK THE "SMS" SHARE BUTTON ──────────────────────────────
        print("\n👉 STEP 2: CLICKING 'SMS' SHARE BUTTON...")
        if not _click_share_button(driver, "SMS"):
            print("\n❌ CT-88: FAILED — COULD NOT CLICK 'SMS' SHARE BUTTON.")
            utils.tomar_screenshot(driver, "CT_88_SMS_BTN_FAILED")
            _capture_evidence(driver, "CT_88")
            return False
        print("   ✅ STEP 2 COMPLETE — 'SMS' BUTTON TAPPED.")

        # ── STEP 3: FILL PHONE NUMBER AND TAP "Enviar" ────────────────────────
        print(f"\n👉 STEP 3: FILLING NUMBER '{CT_SMS_NUMBER}' AND TAPPING 'Enviar'...")
        if not _enter_destination_and_send(driver, CT_SMS_NUMBER):
            print("\n❌ CT-88: FAILED — COULD NOT FILL NUMBER OR TAP 'Enviar'.")
            utils.tomar_screenshot(driver, "CT_88_SEND_MODAL_FAILED")
            _capture_evidence(driver, "CT_88")
            return False
        print("   ✅ STEP 3 COMPLETE — 'Enviar' TAPPED.")

        # ── STEP 4: DETECT RESULT POPUP ───────────────────────────────────────
        print("\n👉 STEP 4: DETECTING SEND RESULT POPUP...")
        result = _detect_send_result(driver, "CT_88")

        # ── EVIDENCE: SCREENSHOT OF RESULT POPUP ──────────────────────────────
        print("\n📸 TAKING SCREENSHOT — SEND RESULT POPUP (PRIMARY EVIDENCE)...")
        utils.tomar_screenshot(driver, "CT_88_SEND_RESULT")
        _capture_evidence(driver, "CT_88")

        if result != "unknown":
            _dismiss_result_popup(driver)

        # ── RESULT ────────────────────────────────────────────────────────────
        print("\n" + "-" * 60)
        print("📊 CT-88 VALIDATION SUMMARY:")
        print(f"   DETAIL SCREEN REACHED        : ✅")
        print(f"   'SMS' BUTTON CLICKED         : ✅")
        print(f"   DESTINATION ENTERED          : ✅  ({CT_SMS_NUMBER})")
        print(f"   RESULT POPUP DETECTED        : "
              f"{'✅ SUCCESS — TICKET SENT' if result == 'success' else '❌ FAILURE POPUP' if result == 'failure' else '⚠️  UNKNOWN'}")
        print("-" * 60)

        if result == "success":
            print("\n✅ CT-88: SUCCESS — RECEIPT SENT VIA SMS AND CONFIRMATION RECEIVED.")
            return True
        elif result == "failure":
            print("\n❌ CT-88: FAILED — 'Aviso: No fue posible enviar el ticket' POPUP APPEARED.")
            return False
        else:
            print("\n⚠️  CT-88: INCONCLUSIVE — NO RESULT POPUP WAS DETECTED.")
            return False

    except RuntimeError as nav_err:
        print(f"\n❌ {nav_err}")
        utils.tomar_screenshot(driver, "CT_88_NAV_FAILED")
        _capture_evidence(driver, "CT_88")
        return False
    except Exception as e:
        print(f"\n💥 CT-88 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "CT_88_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)


# =================================================================================
# MAIN EXECUTION
# =================================================================================
if __name__ == "__main__":

    logger, log_file, timestamp = utils.iniciar_reporte("OPERATIONALS_CT")

    try:
        CT_86()
        CT_87()
        CT_88()

    finally:
        utils.generar_reporte_html("OPERATIONALS_CT", log_file, timestamp)
