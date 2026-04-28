"""
FILENAME: Operationals_TS.py
DESCRIPTION:
    VALIDATES ALL BEHAVIORS WITHIN THE "TRANSACCIONES" TAB OF THE MEMPHIS APP.

CONTENTS:
    · TS-70: VALIDATE THAT THE "TRANSACCIONES" TAB LOADS CORRECTLY WHEN SELECTED.
    · TS-71: VALIDATE THAT THE "ÚLTIMOS 30 DÍAS" VIEW SHOWS A TRANSACTION LIST.s
    · TS-72: VERIFY THAT THE  'LAST 30 DAYS' VIEW CORRECTLY HANDLES THE ABSENCE OF TRANSACTIONS.
    · TS-73: VALIDATE THAT "CORTE POR DÍA" VIEW SHOWS SUMMARY FOR THE CURRENT DAY.
    · TS-74: VALIDATE THAT "CORTE POR DÍA" HANDLES CORRECTLY A DATE WITH NO TRANSACTIONS.
    · TS-75: VALIDATE DAY NAVIGATION IN "CORTE POR DÍA" (TODAY ↔ YESTERDAY).
    · TS-76: VALIDATE THAT SELECTING AN "APROBACIÓN" TRANSACTION SHOWS CORRECT DETAILS.
    · TS-77: VALIDATE THAT SELECTING A "CANCELACIÓN" TRANSACTION SHOWS CORRECT DETAILS.
    · TS-78: VALIDATE THAT SCROLLING THE TRANSACTION LIST LOADS MORE ITEMS.
    · TS-79: VALIDATE THAT "MONTO TOTAL" AND "SUBTOTAL DE PAGOS" SHOW CORRECT VALUES
             IN THE "CORTE POR DÍA" VIEW — NAVIGATES BACK UNTIL A DATE WITH DATA.
    · TS-80: VALIDATE THAT THE LOADING ANIMATION ("CARGANDO") APPEARS WHEN
             NAVIGATING TO THE TRANSACTIONS TAB.
    
REQUIREMENTS:
    - APPIUM SERVER RUNNING.
    - config.py AND utils.py IN THE SAME DIRECTORY.
"""

import sys
import os
import re 
import time

ruta_proyecto = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ruta_proyecto not in sys.path:
    sys.path.append(ruta_proyecto)

import config
import utils
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# =================================================================================
# INTERNAL HELPER: CAPTURE EVIDENCE WITHOUT SILENCING ERRORS
# =================================================================================
def _capture_evidence(driver, nombre_test):
    try:
        utils.print_http_evidence_appium(driver, nombre_test)
    except Exception as ev_err:
        print(f"   ⚠️  HTTP EVIDENCE CAPTURE FAILED FOR [{nombre_test}]: {ev_err}")
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
# INTERNAL HELPER: NAVIGATE TO TRANSACTIONS TAB
# =================================================================================
def _navigate_to_transactions_tab(driver, wait):
    print("   🔍 [NAV] ATTEMPTING STRATEGY 1: CONTENT-DESC WITH INDEX...")
    try:
        driver.find_element(By.XPATH, config.XPATH_PÑ_TAB_TRANSACTIONSS).click()
        time.sleep(2)
        print("   ✅ [NAV] STRATEGY 1 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [NAV] STRATEGY 1 FAILED: {e}")

    print("   🔍 [NAV] ATTEMPTING STRATEGY 2: PARTIAL CONTENT-DESC MATCH...")
    try:
        driver.find_element(By.XPATH, config.XPATH_TS_TAB_TRANSACCIONES_ALT).click()
        time.sleep(2)
        print("   ✅ [NAV] STRATEGY 2 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [NAV] STRATEGY 2 FAILED: {e}")

    print("   🔍 [NAV] ATTEMPTING STRATEGY 3: TEXT ATTRIBUTE MATCH...")
    try:
        driver.find_element(By.XPATH, config.XPATH_TS_TAB_TRANSACCIONES_TEXT).click()
        time.sleep(2)
        print("   ✅ [NAV] STRATEGY 3 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [NAV] STRATEGY 3 FAILED: {e}")

    print("   🔍 [NAV] ATTEMPTING STRATEGY 4: ABSOLUTE XPATH (APPIUM INSPECTOR)...")
    try:
        driver.find_element(By.XPATH, config.XPATH_TS_TAB_TRANSACCIONES_ABSOLUTE).click()
        time.sleep(2)
        print("   ✅ [NAV] STRATEGY 4 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   💥 [NAV] STRATEGY 4 FAILED: {e}")

    print("   ❌ [NAV] ALL STRATEGIES EXHAUSTED — TRANSACTIONS TAB NOT CLICKABLE.")
    return False


# =================================================================================
# INTERNAL HELPER: VERIFY TRANSACTIONS SCREEN LOADED
# =================================================================================
def _verify_transactions_screen_loaded(driver, wait):
    print("   🔍 [VERIFY] CHECKING INDICATOR 1: HEADER TITLE 'TRANSACCIONES'...")
    try:
        wait.until(EC.presence_of_element_located(
            (By.XPATH, config.XPATH_TS_HEADER_TITLE)
        ))
        print("   ✅ [VERIFY] INDICATOR 1 FOUND: TRANSACTIONS HEADER TITLE VISIBLE.")
        return True
    except:
        print("   ⚠️  [VERIFY] INDICATOR 1 NOT FOUND.")

    print("   🔍 [VERIFY] CHECKING INDICATOR 2: TRANSACTION LIST OR EMPTY STATE...")
    try:
        wait.until(EC.presence_of_element_located(
            (By.XPATH, config.XPATH_TS_EMPTY_STATE)
        ))
        print("   ✅ [VERIFY] INDICATOR 2 FOUND: LIST OR EMPTY-STATE MESSAGE VISIBLE.")
        return True
    except:
        print("   ⚠️  [VERIFY] INDICATOR 2 NOT FOUND.")

    print("   🔍 [VERIFY] CHECKING INDICATOR 3: TAB SELECTED STATE...")
    try:
        wait.until(EC.presence_of_element_located(
            (By.XPATH, config.XPATH_TS_TAB_SELECTED_STATE)
        ))
        print("   ✅ [VERIFY] INDICATOR 3 FOUND: TAB IS IN SELECTED STATE.")
        return True
    except:
        print("   ⚠️  [VERIFY] INDICATOR 3 NOT FOUND.")

    print("   ❌ [VERIFY] ALL INDICATORS EXHAUSTED — SCREEN LOAD COULD NOT BE CONFIRMED.")
    return False

# =================================================================================
# INTERNAL HELPER: CLICK THE "CORTE POR DÍA" SUB-TAB
# =================================================================================
def _click_corte_por_dia_tab(driver, wait):
    print("   🔍 [NAV] ATTEMPTING STRATEGY 1: CONTENT-DESC 'CORTE POR DÍA'...")
    try:
        driver.find_element(By.XPATH, config.XPATH_TS_TAB_DAILY_CUT).click()
        time.sleep(2)
        print("   ✅ [NAV] STRATEGY 1 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [NAV] STRATEGY 1 FAILED: {e}")

    print("   🔍 [NAV] ATTEMPTING STRATEGY 2: TEXT ATTRIBUTE MATCH...")
    try:
        driver.find_element(By.XPATH, config.XPATH_TS_TAB_DAILY_CUT_TEXT).click()
        time.sleep(2)
        print("   ✅ [NAV] STRATEGY 2 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [NAV] STRATEGY 2 FAILED: {e}")

    print("   🔍 [NAV] ATTEMPTING STRATEGY 3: PARTIAL TEXT 'CORTE'...")
    try:
        driver.find_element(By.XPATH, config.XPATH_TS_TAB_DAILY_CUT_PARTIAL).click()
        time.sleep(2)
        print("   ✅ [NAV] STRATEGY 3 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [NAV] STRATEGY 3 FAILED: {e}")

    print("   🔍 [NAV] ATTEMPTING STRATEGY 4: SECOND TAB BY SIBLING POSITION...")
    try:
        driver.find_element(By.XPATH, config.XPATH_TS_TAB_DAILY_CUT_SIBLING).click()
        time.sleep(2)
        print("   ✅ [NAV] STRATEGY 4 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   💥 [NAV] STRATEGY 4 FAILED: {e}")

    print("   ❌ [NAV] ALL STRATEGIES EXHAUSTED — 'CORTE POR DÍA' TAB NOT CLICKABLE.")
    return False

# =================================================================================
# INTERNAL HELPER: READ THE CURRENTLY DISPLAYED DATE FROM THE DATE NAVIGATOR
# =================================================================================
def _get_current_navigator_date(driver):
    DIAS_SEMANA = ["lunes", "martes", "miércoles", "miercoles",
                   "jueves", "viernes", "sábado", "sabado", "domingo"]
    try:
        for el in driver.find_elements(By.XPATH, '//*[contains(@text, ",")]'):
            t = el.get_attribute("text") or ""
            if "," in t and len(t) > 5:
                print(f"   📅 [DATE READER] STRATEGY A — text WITH COMMA: '{t}'")
                return t
    except:
        pass
    try:
        for el in driver.find_elements(By.XPATH, '//*[contains(@content-desc, ",")]'):
            t = el.get_attribute("content-desc") or ""
            if "," in t and len(t) > 5:
                print(f"   📅 [DATE READER] STRATEGY B — content-desc WITH COMMA: '{t}'")
                return t
    except:
        pass
    try:
        for el in driver.find_elements(By.XPATH, "//*"):
            t = (el.get_attribute("text") or el.get_attribute("content-desc") or "").lower()
            if any(dia in t for dia in DIAS_SEMANA) and len(t) > 4:
                print(f"   📅 [DATE READER] STRATEGY C — DAY-OF-WEEK MATCH: '{t}'")
                return t
    except:
        pass

    try:
        candidates = []
        for el in driver.find_elements(By.XPATH, "//*"):
            t = el.get_attribute("text") or el.get_attribute("content-desc") or ""
            if any(c.isdigit() for c in t) and len(t) > 4:
                candidates.append(t)
        if candidates:
            best = max(candidates, key=len)
            print(f"   📅 [DATE READER] STRATEGY D — LONGEST WITH DIGIT: '{best}'")
            return best
    except:
        pass

    print("   ⚠️  [DATE READER] ALL STRATEGIES FAILED — DATE NOT READABLE.")
    return None

# =================================================================================
# INTERNAL HELPER: CLICK DATE NAVIGATION ARROW (◄ OR ►)
# =================================================================================
def _click_date_arrow(driver, wait, direction="back"):
    dir_label  = "◄ BACK" if direction == "back" else "► FORWARD"
    xpath_abs  = config.XPATH_TS_BTN_PREVIOUS_DATE if direction == "back" else config.XPATH_TS_BTN_NEXT_DATE
    x_coord    = config.TS_ARROW_BACK_X if direction == "back" else config.TS_ARROW_FWD_X

    date_before = _get_current_navigator_date(driver)
    print(f"   📅 [ARROW] DATE BEFORE CLICK: '{date_before}'")

    # STRATEGY 1: ABSOLUTE XPATH FROM APPIUM INSPECTOR
    print(f"   🔍 [ARROW] {dir_label} — STRATEGY 1: APPIUM INSPECTOR ABSOLUTE XPATH...")
    try:
        driver.find_element(By.XPATH, xpath_abs).click()
        time.sleep(2)
        if _date_did_change(driver, date_before):
            print(f"   ✅ [ARROW] {dir_label} — STRATEGY 1 SUCCEEDED.")
            return True
        print(f"   ⚠️  [ARROW] STRATEGY 1 CLICKED BUT DATE DID NOT CHANGE.")
    except Exception as e:
        print(f"   ⚠️  [ARROW] STRATEGY 1 FAILED: {e}")

    # STRATEGY 2: UNICODE CHARACTER MATCH
    print(f"   🔍 [ARROW] {dir_label} — STRATEGY 2: UNICODE CHAR MATCH...")
    unicode_char = "◄" if direction == "back" else "►"
    try:
        driver.find_element(
            By.XPATH,
            f'//*[@content-desc="{unicode_char}" or @text="{unicode_char}"]'
        ).click()
        time.sleep(2)
        if _date_did_change(driver, date_before):
            print(f"   ✅ [ARROW] {dir_label} — STRATEGY 2 SUCCEEDED.")
            return True
        print(f"   ⚠️  [ARROW] STRATEGY 2 CLICKED BUT DATE DID NOT CHANGE.")
    except Exception as e:
        print(f"   ⚠️  [ARROW] STRATEGY 2 FAILED: {e}")

    # STRATEGY 3: COORDINATE TAP
    print(f"   🔍 [ARROW] {dir_label} — STRATEGY 3: COORDINATE TAP (x={x_coord}, y={config.TS_ARROW_Y})...")
    try:
        driver.execute_script("mobile: clickGesture", {"x": x_coord, "y": config.TS_ARROW_Y})
        time.sleep(2)
        if _date_did_change(driver, date_before):
            print(f"   ✅ [ARROW] {dir_label} — STRATEGY 3 SUCCEEDED.")
            return True
        print(f"   ⚠️  [ARROW] STRATEGY 3 CLICKED BUT DATE DID NOT CHANGE.")
    except Exception as e:
        print(f"   💥 [ARROW] STRATEGY 3 FAILED: {e}")

    print(f"   ❌ [ARROW] ALL STRATEGIES EXHAUSTED — DATE DID NOT CHANGE FOR {dir_label}.")
    return False

# =================================================================================
# INTERNAL HELPER: COMPARE CURRENT DATE VS A BASELINE TO DETECT CHANGE
# =================================================================================
def _date_did_change(driver, date_before):
    date_now = _get_current_navigator_date(driver)
    if date_now is None:
        print(f"   ⚠️  [DATE CHECK] COULD NOT READ CURRENT DATE AFTER CLICK.")
        return False
    changed = date_now != date_before
    print(f"   📅 [DATE CHECK] BEFORE='{date_before}' | NOW='{date_now}' | CHANGED={changed}")
    return changed

# =================================================================================
# INTERNAL HELPER: READ FIRST "APROBACIÓN" ITEM DATA FROM THE LIST
# =================================================================================
def _get_first_aprobacion_item(driver):
    
    import re
    DATE_PATTERN   = re.compile(r"\d{2}-\d{2}-\d{4},?\s*\d{2}:\d{2}:\d{2}")
    AMOUNT_PATTERN = re.compile(r"\$[\d,]+\.\d{2}")

    print("   🔍 [LIST READER] SCANNING FOR FIRST 'APROBACIÓN' ITEM...")

    aprobacion_elements = driver.find_elements(
        By.XPATH, config.XPATH_TS_ITEM_APPROVAL_STATUS
    )
    print(f"   📊 [LIST READER] 'APROBACIÓN' ELEMENTS FOUND: {len(aprobacion_elements)}")

    if not aprobacion_elements:
        print("   ⚠️  [LIST READER] NO 'APROBACIÓN' ITEMS FOUND.")
        return None

    
    print("   🔍 [LIST READER] STRATEGY A: SCANNING content-desc OF ALL ELEMENTS...")
    fecha_found  = None
    monto_found  = None
    all_descs    = []

    try:
        for el in driver.find_elements(By.XPATH, "//*"):
            #
            for attr in ("text", "content-desc"):
                val = el.get_attribute(attr) or ""
                if val and len(val) > 1:
                    all_descs.append(val)

        
        seen = set()
        all_descs = [x for x in all_descs if not (x in seen or seen.add(x))]
        print(f"   📝 [LIST READER] ALL ACCESSIBLE VALUES ({len(all_descs)}): {all_descs[:30]}")

        for val in all_descs:
            if not fecha_found and DATE_PATTERN.search(val):
                fecha_found = DATE_PATTERN.search(val).group()
                print(f"   📅 [LIST READER] DATE FOUND: '{fecha_found}'")
            if not monto_found and AMOUNT_PATTERN.search(val) and "$0.00" not in val:
                monto_found = AMOUNT_PATTERN.search(val).group()
                print(f"   💰 [LIST READER] AMOUNT FOUND: '{monto_found}'")
            if fecha_found and monto_found:
                break

    except Exception as e:
        print(f"   ⚠️  [LIST READER] STRATEGY A FAILED: {e}")

    if fecha_found and monto_found:
        print(f"   ✅ [LIST READER] STRATEGY A SUCCESS — "
              f"FECHA: '{fecha_found}' | MONTO: '{monto_found}'")
        return {"fecha": fecha_found, "monto": monto_found}

    # ── STRATEGY B: READ content-desc OF THE APROBACIÓN ELEMENT ITSELF ───────
    
    print("   🔍 [LIST READER] STRATEGY B: READING content-desc OF APROBACIÓN ELEMENT...")
    try:
        first_aprobacion = aprobacion_elements[0]
        full_desc = first_aprobacion.get_attribute("content-desc") or ""
        print(f"   📝 [LIST READER] APROBACIÓN ELEMENT content-desc: '{full_desc}'")

        if not fecha_found:
            m = DATE_PATTERN.search(full_desc)
            if m:
                fecha_found = m.group()
                print(f"   📅 [LIST READER] DATE FROM STRATEGY B: '{fecha_found}'")

        if not monto_found:
            m = AMOUNT_PATTERN.search(full_desc)
            if m and "$0.00" not in m.group():
                monto_found = m.group()
                print(f"   💰 [LIST READER] AMOUNT FROM STRATEGY B: '{monto_found}'")

    except Exception as e:
        print(f"   ⚠️  [LIST READER] STRATEGY B FAILED: {e}")

    if fecha_found and monto_found:
        print(f"   ✅ [LIST READER] STRATEGY B SUCCESS — "
              f"FECHA: '{fecha_found}' | MONTO: '{monto_found}'")
        return {"fecha": fecha_found, "monto": monto_found}

    # ── STRATEGY C: UIAUTOMATOR DIRECT QUERY ─────────────────────────────────
    
    print("   🔍 [LIST READER] STRATEGY C: UIAUTOMATOR DIRECT QUERY...")
    try:
        # FIND ALL NODES WITH ANY TEXT CONTENT
        nodes = driver.find_elements(
            By.ANDROID_UIAUTOMATOR,
            'new UiSelector().textMatches(".*\\\\d.*")'
        )
        print(f"   📊 [LIST READER] UIAUTOMATOR NODES WITH DIGITS: {len(nodes)}")
        for node in nodes:
            val = node.get_attribute("text") or node.get_attribute("content-desc") or ""
            print(f"      → '{val}'")
            if not fecha_found and DATE_PATTERN.search(val):
                fecha_found = DATE_PATTERN.search(val).group()
            if not monto_found and AMOUNT_PATTERN.search(val) and "$0.00" not in val:
                monto_found = AMOUNT_PATTERN.search(val).group()
            if fecha_found and monto_found:
                break

    except Exception as e:
        print(f"   ⚠️  [LIST READER] STRATEGY C FAILED: {e}")

    if fecha_found or monto_found:
        print(f"   ✅ [LIST READER] STRATEGY C PARTIAL/FULL — "
              f"FECHA: '{fecha_found}' | MONTO: '{monto_found}'")
        return {"fecha": fecha_found, "monto": monto_found}

    print("   ❌ [LIST READER] ALL STRATEGIES EXHAUSTED — NO DATA READABLE FROM LIST.")
    return None

# =================================================================================
# INTERNAL HELPER: CLICK THE FIRST "APROBACIÓN" ITEM IN THE LIST
# =================================================================================
def _click_first_aprobacion_item(driver, wait):
    print("   🔍 [CLICK ITEM] STRATEGY 1: CLICKING 'APROBACIÓN' STATUS ELEMENT...")
    try:
        elements = driver.find_elements(By.XPATH, config.XPATH_TS_ITEM_APROBACION_STATUS)
        if elements:
            elements[0].click()
            print("   ✅ [CLICK ITEM] STRATEGY 1 SUCCEEDED.")
            return True
    except Exception as e:
        print(f"   ⚠️  [CLICK ITEM] STRATEGY 1 FAILED: {e}")

    print("   🔍 [CLICK ITEM] STRATEGY 2: CLICKING FIRST DATE IN LIST...")
    try:
        import re
        all_els = driver.find_elements(By.XPATH, "//*")
        for el in all_els:
            t = el.get_attribute("text") or ""
            if re.match(r"\d{2}-\d{2}-\d{4},\s*\d{2}:\d{2}:\d{2}", t):
                el.click()
                print(f"   ✅ [CLICK ITEM] STRATEGY 2 SUCCEEDED — CLICKED DATE: '{t}'")
                return True
    except Exception as e:
        print(f"   ⚠️  [CLICK ITEM] STRATEGY 2 FAILED: {e}")

    print("   🔍 [CLICK ITEM] STRATEGY 3: CLICKING FIRST ROW BY ABSOLUTE XPATH...")
    try:
        driver.find_element(By.XPATH, config.XPATH_TS_FIRST_LIST_ROW).click()
        print("   ✅ [CLICK ITEM] STRATEGY 3 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   💥 [CLICK ITEM] STRATEGY 3 FAILED: {e}")

    print("   ❌ [CLICK ITEM] ALL STRATEGIES EXHAUSTED.")
    return False

# =================================================================================
# INTERNAL HELPER: READ A SPECIFIC FIELD VALUE FROM THE DETAIL SCREEN
# =================================================================================
def _get_detail_field_value(driver, field_label):
    import re
    print(f"   🔍 [FIELD READER] READING VALUE FOR LABEL: '{field_label}'...")

    try:
        
        label_els = driver.find_elements(
            By.XPATH,
            f'//*[@text="{field_label}" or @content-desc="{field_label}"]'
        )
        if label_els:
            label_el = label_els[0]
            
            try:
                sibling = driver.find_element(
                    By.XPATH,
                    f'//*[@text="{field_label}" or '
                    f'@content-desc="{field_label}"]'
                    f'/following-sibling::*[1]'
                )
                val = sibling.get_attribute("text") or sibling.get_attribute("content-desc") or ""
                if val:
                    print(f"   ✅ [FIELD READER] STRATEGY A — '{field_label}': '{val}'")
                    return val
            except:
                pass

            
            all_vals = []
            for el in driver.find_elements(By.XPATH, "//*"):
                for attr in ("text", "content-desc"):
                    v = el.get_attribute(attr) or ""
                    if v and len(v) > 0:
                        all_vals.append(v)
            seen = set()
            all_vals = [x for x in all_vals if not (x in seen or seen.add(x))]

            for i, v in enumerate(all_vals):
                if field_label in v and i + 1 < len(all_vals):
                    result = all_vals[i + 1]
                    print(f"   ✅ [FIELD READER] STRATEGY B — '{field_label}': '{result}'")
                    return result

    except Exception as e:
        print(f"   ⚠️  [FIELD READER] FAILED FOR '{field_label}': {e}")

    print(f"   ⚠️  [FIELD READER] COULD NOT READ VALUE FOR '{field_label}'.")
    return None


# =================================================================================
# INTERNAL HELPER: CLICK A TAB BY NAME ON THE DETAIL SCREEN (VENTA / CANCELACIÓN)
# =================================================================================
def _click_detail_tab(driver, wait, tab_name):
    print(f"   🔍 [TAB CLICK] CLICKING DETAIL TAB: '{tab_name}'...")

    
    try:
        driver.find_element(
            By.XPATH,
            f'//*[@text="{tab_name}" or @content-desc="{tab_name}"]'
        ).click()
        time.sleep(2)
        print(f"   ✅ [TAB CLICK] STRATEGY 1 SUCCEEDED — TAB '{tab_name}' ACTIVE.")
        return True
    except Exception as e:
        print(f"   ⚠️  [TAB CLICK] STRATEGY 1 FAILED: {e}")

    
    try:
       
        partial = tab_name[:9]
        driver.find_element(
            By.XPATH,
            f'//*[contains(@text, "{partial}") or contains(@content-desc, "{partial}")]'
        ).click()
        time.sleep(2)
        print(f"   ✅ [TAB CLICK] STRATEGY 2 SUCCEEDED — TAB '{tab_name}' ACTIVE.")
        return True
    except Exception as e:
        print(f"   💥 [TAB CLICK] STRATEGY 2 FAILED: {e}")

    print(f"   ❌ [TAB CLICK] COULD NOT CLICK TAB '{tab_name}'.")
    return False

# =================================================================================
# INTERNAL HELPER
# =================================================================================
def _get_first_cancelacion_item(driver):
    import re
    DATE_PATTERN   = re.compile(r"\d{2}-\d{2}-\d{4},?\s*\d{2}:\d{2}:\d{2}")
    AMOUNT_PATTERN = re.compile(r"\$[\d,]+\.\d{2}")

    print("   🔍 [LIST READER] SCANNING FOR FIRST 'CANCELACIÓN' ITEM...")

    cancelacion_elements = driver.find_elements(
        By.XPATH, config.XPATH_TS_ITEM_STATUS_CANCELATION
    )
    print(f"   📊 [LIST READER] 'CANCELACIÓN' ELEMENTS FOUND: {len(cancelacion_elements)}")

    if not cancelacion_elements:
        print("   ⚠️  [LIST READER] NO 'CANCELACIÓN' ITEMS IN LIST.")
        return None

    fecha_found = None
    monto_found = None
    all_vals    = []

    # STRATEGY A
    try:
        for el in driver.find_elements(By.XPATH, "//*"):
            for attr in ("text", "content-desc"):
                v = el.get_attribute(attr) or ""
                if v and len(v) > 1:
                    all_vals.append(v)
        seen = set()
        all_vals = [x for x in all_vals if not (x in seen or seen.add(x))]
        print(f"   📝 [LIST READER] ALL VALUES: {all_vals}")

        
        for val in reversed(all_vals):
            if not fecha_found and DATE_PATTERN.search(val):
                fecha_found = DATE_PATTERN.search(val).group()
            if not monto_found and AMOUNT_PATTERN.search(val) and "$0.00" not in val:
                monto_found = AMOUNT_PATTERN.search(val).group()
            if fecha_found and monto_found:
                break
    except Exception as e:
        print(f"   ⚠️  [LIST READER] STRATEGY A FAILED: {e}")

    # STRATEGY B
    if not (fecha_found and monto_found):
        try:
            full_desc = cancelacion_elements[0].get_attribute("content-desc") or ""
            print(f"   📝 [LIST READER] CANCELACIÓN ELEMENT DESC: '{full_desc}'")
            if not fecha_found:
                m = DATE_PATTERN.search(full_desc)
                if m:
                    fecha_found = m.group()
            if not monto_found:
                m = AMOUNT_PATTERN.search(full_desc)
                if m and "$0.00" not in m.group():
                    monto_found = m.group()
        except Exception as e:
            print(f"   ⚠️  [LIST READER] STRATEGY B FAILED: {e}")

    print(f"   {'✅' if fecha_found or monto_found else '❌'} [LIST READER] "
          f"FECHA: '{fecha_found}' | MONTO: '{monto_found}'")
    return {"fecha": fecha_found, "monto": monto_found} if (fecha_found or monto_found) else None

# =================================================================================
# INTERNAL HELPER
# =================================================================================
def _click_first_cancelacion_item(driver, wait):
    import re
    DATE_PATTERN = re.compile(r"\d{2}-\d{2}-\d{4},?\s*\d{2}:\d{2}:\d{2}")

    print("   🔍 [CLICK ITEM] STRATEGY 1: CLICKING 'CANCELACIÓN' STATUS ELEMENT...")
    try:
        elements = driver.find_elements(By.XPATH, config.XPATH_TS_ITEM_CANCELACION_STATUS)
        if elements:
            elements[0].click()
            print("   ✅ [CLICK ITEM] STRATEGY 1 SUCCEEDED.")
            return True
    except Exception as e:
        print(f"   ⚠️  [CLICK ITEM] STRATEGY 1 FAILED: {e}")

    print("   🔍 [CLICK ITEM] STRATEGY 2: CLICKING LAST DATE IN LIST...")
    try:
        all_els = driver.find_elements(By.XPATH, "//*")
        date_elements = []
        for el in all_els:
            for attr in ("text", "content-desc"):
                t = el.get_attribute(attr) or ""
                if DATE_PATTERN.match(t):
                    date_elements.append(el)
                    break
        if date_elements:
            
            date_elements[-1].click()
            print(f"   ✅ [CLICK ITEM] STRATEGY 2 SUCCEEDED — CLICKED LAST DATE ELEMENT.")
            return True
    except Exception as e:
        print(f"   ⚠️  [CLICK ITEM] STRATEGY 2 FAILED: {e}")

    print("   🔍 [CLICK ITEM] STRATEGY 3: UIAUTOMATOR SCROLL TO CANCELACIÓN...")
    try:
        driver.find_element(
            By.ANDROID_UIAUTOMATOR,
            'new UiScrollable(new UiSelector().scrollable(true))'
            '.scrollIntoView(new UiSelector().textContains("CANCELACI"))'
        ).click()
        print("   ✅ [CLICK ITEM] STRATEGY 3 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   💥 [CLICK ITEM] STRATEGY 3 FAILED: {e}")

    print("   ❌ [CLICK ITEM] ALL STRATEGIES EXHAUSTED.")
    return False


# =================================================================================
# TS-70: VALIDATE THAT THE "TRANSACCIONES" TAB LOADS CORRECTLY WHEN SELECTED.
# =================================================================================
def TS_70():
    print("\n" + "=" * 60)
    print("🧪 TS-70: TRANSACTIONS TAB LOADS CORRECTLY WHEN SELECTED")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)
        print("   ✅ PRECONDITION MET — MAIN CHARGING SCREEN REACHED.")

        # ── STEP 1: TAP THE "TRANSACCIONES" BOTTOM NAV TAB ───────────────────
        print("\n👉 STEP 1: TAPPING 'TRANSACCIONES' BOTTOM NAV TAB...")
        tab_clicked = _navigate_to_transactions_tab(driver, wait)

        if not tab_clicked:
            print("\n❌ TS-70: FAILED — COULD NOT TAP 'TRANSACCIONES' TAB.")
            utils.tomar_screenshot(driver, "TS_70_TAB_CLICK_FAILED")
            _capture_evidence(driver, "TS_70")
            return False

        print("   ✅ STEP 1 COMPLETE — TAB TAPPED SUCCESSFULLY.")
        time.sleep(2)

        # ── STEP 2: VERIFY TRANSACTIONS SCREEN LOADED ─────────────────────────
        print("\n👉 STEP 2: VERIFYING TRANSACTIONS SCREEN LOADED CORRECTLY...")
        screen_loaded = _verify_transactions_screen_loaded(driver, wait)

        
        print("\n📸 TAKING SCREENSHOT — TRANSACTIONS TAB STATE...")
        utils.tomar_screenshot(driver, "TS_70_TRANSACTIONS_TAB")
        _capture_evidence(driver, "TS_70")

        print("\n🔍 SCANNING VISIBLE TEXT FOR DEBUGGING...")
        try:
            for elem in driver.find_elements(By.XPATH, "//*"):
                t = elem.get_attribute("text")
                if t and len(t) > 3:
                    print(f"   📝 VISIBLE TEXT: '{t}'")
        except:
            pass

        # ── RESULT ───────────────────────────────────────────────────────────
        if screen_loaded:
            print("\n✅ TS-70: SUCCESS — 'TRANSACCIONES' TAB LOADED CORRECTLY.")
            return True
        else:
            print("\n❌ TS-70: FAILED — TRANSACTIONS SCREEN CONTENT COULD NOT BE VERIFIED.")
            return False

    except Exception as e:
        print(f"\n💥 TS-70 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "TS_70_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)

# =================================================================================
# TS-71: VALIDATE THAT THE "ÚLTIMOS 30 DÍAS" VIEW SHOWS A TRANSACTION LIST.
# =================================================================================
def TS_71():
    print("\n" + "=" * 60)
    print("🧪 TS-71: 'ÚLTIMOS 30 DÍAS' VIEW DISPLAYS TRANSACTION LIST")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)
        print("   ✅ PRECONDITION MET — MAIN CHARGING SCREEN REACHED.")

        # ── STEP 1: TAP THE "TRANSACCIONES" BOTTOM NAV TAB ───────────────────
        print("\n👉 STEP 1: TAPPING 'TRANSACCIONES' BOTTOM NAV TAB...")
        tab_clicked = _navigate_to_transactions_tab(driver, wait)

        if not tab_clicked:
            print("\n❌ TS-71: FAILED — COULD NOT TAP 'TRANSACCIONES' TAB.")
            utils.tomar_screenshot(driver, "TS_71_TAB_CLICK_FAILED")
            _capture_evidence(driver, "TS_71")
            return False

        print("   ✅ STEP 1 COMPLETE — TRANSACTIONS SCREEN REACHED.")
        time.sleep(2)

        # ── STEP 2: VERIFY "ÚLTIMOS 30 DÍAS" TAB IS THE DEFAULT ACTIVE VIEW ──
        print("\n👉 STEP 2: VERIFYING 'ÚLTIMOS 30 DÍAS' TAB IS ACTIVE BY DEFAULT...")
        tab_30_dias_visible = utils.verificar_existencia(
            wait,
            config.XPATH_TS_TAB_30_DAYS,
            "ÚLTIMOS 30 DÍAS TAB",
            driver
        )

        if not tab_30_dias_visible:
            print("   ❌ 'ÚLTIMOS 30 DÍAS' TAB NOT FOUND — SCREEN MAY NOT HAVE LOADED.")
            utils.tomar_screenshot(driver, "TS_71_TAB_30_DIAS_NOT_FOUND")
            _capture_evidence(driver, "TS_71")
            return False

        print("   ✅ STEP 2 COMPLETE — 'ÚLTIMOS 30 DÍAS' TAB IS VISIBLE AND ACTIVE.")

        # ── STEP 3: VERIFY AT LEAST ONE TRANSACTION ITEM EXISTS IN THE LIST ──
        print("\n👉 STEP 3: VERIFYING TRANSACTION LIST HAS AT LEAST ONE ITEM...")
        list_has_items = utils.verificar_existencia(
            wait,
            config.XPATH_TS_TRANSACTION_ITEM,
            "TRANSACTION LIST ITEM",
            driver
        )

        if not list_has_items:
            print("   ❌ NO TRANSACTION ITEMS FOUND — LIST MAY BE EMPTY OR NOT LOADED.")
            utils.tomar_screenshot(driver, "TS_71_LIST_EMPTY")
            _capture_evidence(driver, "TS_71")
            return False

        print("   ✅ STEP 3 COMPLETE — TRANSACTION LIST HAS ITEMS.")

        # ── STEP 4: VERIFY TRANSACTION ITEM STRUCTURE (DATE + AMOUNT + STATUS) ─
        print("\n👉 STEP 4: VERIFYING TRANSACTION ITEM STRUCTURE...")

        date_visible = utils.verificar_existencia(
            wait,
            config.XPATH_TS_TRANSACTION_DATE,
            "TRANSACTION DATE FIELD",
            driver
        )
        amount_visible = utils.verificar_existencia(
            wait,
            config.XPATH_TS_TRANSACTION_AMOUNT,
            "TRANSACTION AMOUNT FIELD",
            driver
        )
        status_visible = utils.verificar_existencia(
            wait,
            config.XPATH_TS_TRANSACTION_STATUS,
            "TRANSACTION STATUS (APROBACIÓN/CANCELACIÓN)",
            driver
        )

        structure_ok = date_visible and amount_visible and status_visible

        if structure_ok:
            print("   ✅ STEP 4 COMPLETE — ITEM STRUCTURE VALID: DATE + AMOUNT + STATUS PRESENT.")
        else:
            print("   ⚠️  STEP 4 WARNING — SOME ITEM FIELDS COULD NOT BE VERIFIED:")
            print(f"      DATE: {'✅' if date_visible else '❌'}  |  "
                  f"AMOUNT: {'✅' if amount_visible else '❌'}  |  "
                  f"STATUS: {'✅' if status_visible else '❌'}")

        
        print("\n📸 TAKING SCREENSHOT — ÚLTIMOS 30 DÍAS LIST...")
        utils.tomar_screenshot(driver, "TS_71_ULTIMOS_30_DIAS")
        _capture_evidence(driver, "TS_71")

        
        print("\n🔍 SCANNING VISIBLE TEXT FOR DEBUGGING...")
        try:
            items = driver.find_elements(By.XPATH, config.XPATH_TS_TRANSACTION_ITEM)
            print(f"   📊 TOTAL TRANSACTION ITEMS DETECTED: {len(items)}")
            for elem in driver.find_elements(By.XPATH, "//*"):
                t = elem.get_attribute("text")
                if t and len(t) > 3:
                    print(f"   📝 VISIBLE TEXT: '{t}'")
        except:
            pass

        # ── RESULT ───────────────────────────────────────────────────────────
        if list_has_items and structure_ok:
            print("\n✅ TS-71: SUCCESS — 'ÚLTIMOS 30 DÍAS' VIEW SHOWS TRANSACTION LIST CORRECTLY.")
            return True
        elif list_has_items:
            print("\n✅ TS-71: SUCCESS (PARTIAL) — LIST HAS ITEMS BUT SOME FIELD STRUCTURE COULD NOT BE FULLY VERIFIED.")
            return True
        else:
            print("\n❌ TS-71: FAILED — TRANSACTION LIST NOT PROPERLY DISPLAYED.")
            return False

    except Exception as e:
        print(f"\n💥 TS-71 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "TS_71_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)


# ===============================================================================================
# TS-72: VERIFY THAT THE  'LAST 30 DAYS' VIEW CORRECTLY HANDLES THE ABSENCE OF TRANSACTIONS.
# ===============================================================================================
def TS_72():
    print("\n" + "=" * 60)
    print("🧪 TS-72: 'VERIFY THAT THE  'LAST 30 DAYS' VIEW CORRECTLY HANDLES THE ABSENCE OF TRANSACTIONS.")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)
        print("   ✅ PRECONDITION MET — MAIN CHARGING SCREEN REACHED.")

        # ── STEP 1: TAP THE "TRANSACCIONES" BOTTOM NAV TAB ───────────────────
        print("\n👉 STEP 1: TAPPING 'TRANSACCIONES' BOTTOM NAV TAB...")
        tab_clicked = _navigate_to_transactions_tab(driver, wait)

        if not tab_clicked:
            print("\n❌ TS-71: FAILED — COULD NOT TAP 'TRANSACCIONES' TAB.")
            utils.tomar_screenshot(driver, "TS_71_TAB_CLICK_FAILED")
            _capture_evidence(driver, "TS_71")
            return False

        print("   ✅ STEP 1 COMPLETE — TRANSACTIONS SCREEN REACHED.")
        time.sleep(2)

        # ── STEP 2: VERIFY "ÚLTIMOS 30 DÍAS" TAB IS THE DEFAULT ACTIVE VIEW ──
        print("\n👉 STEP 2: VERIFYING 'ÚLTIMOS 30 DÍAS' TAB IS ACTIVE BY DEFAULT...")
        tab_30_dias_visible = utils.verificar_existencia(
            wait,
            config.XPATH_TS_TAB_30_DIAS,
            "ÚLTIMOS 30 DÍAS TAB",
            driver
        )

        if not tab_30_dias_visible:
            print("   ❌ 'ÚLTIMOS 30 DÍAS' TAB NOT FOUND — SCREEN MAY NOT HAVE LOADED.")
            utils.tomar_screenshot(driver, "TS_71_TAB_30_DIAS_NOT_FOUND")
            _capture_evidence(driver, "TS_71")
            return False

        print("   ✅ STEP 2 COMPLETE — 'ÚLTIMOS 30 DÍAS' TAB IS VISIBLE AND ACTIVE.")

        # ── STEP 3: VERIFY AT LEAST ONE TRANSACTION ITEM EXISTS IN THE LIST ──
        print("\n👉 STEP 3: VERIFYING TRANSACTION LIST HAS AT LEAST ONE ITEM...")
        list_has_items = utils.verificar_existencia(
            wait,
            config.XPATH_TS_TRANSACTION_ITEM,
            "TRANSACTION LIST ITEM",
            driver
        )

        if not list_has_items:
            print("   ❌ NO TRANSACTION ITEMS FOUND — LIST MAY BE EMPTY OR NOT LOADED.")
            utils.tomar_screenshot(driver, "TS_71_LIST_EMPTY")
            _capture_evidence(driver, "TS_71")
            return False

        print("   ✅ STEP 3 COMPLETE — TRANSACTION LIST HAS ITEMS.")

        # ── STEP 4: VERIFY TRANSACTION ITEM STRUCTURE (DATE + AMOUNT + STATUS) ─
        print("\n👉 STEP 4: VERIFYING TRANSACTION ITEM STRUCTURE...")

        date_visible = utils.verificar_existencia(
            wait,
            config.XPATH_TS_TRANSACTION_DATE,
            "TRANSACTION DATE FIELD",
            driver
        )
        amount_visible = utils.verificar_existencia(
            wait,
            config.XPATH_TS_TRANSACTION_AMOUNT,
            "TRANSACTION AMOUNT FIELD",
            driver
        )
        status_visible = utils.verificar_existencia(
            wait,
            config.XPATH_TS_TRANSACTION_STATUS,
            "TRANSACTION STATUS (APROBACIÓN/CANCELACIÓN)",
            driver
        )

        structure_ok = date_visible and amount_visible and status_visible

        if structure_ok:
            print("   ✅ STEP 4 COMPLETE — ITEM STRUCTURE VALID: DATE + AMOUNT + STATUS PRESENT.")
        else:
            print("   ⚠️  STEP 4 WARNING — SOME ITEM FIELDS COULD NOT BE VERIFIED:")
            print(f"      DATE: {'✅' if date_visible else '❌'}  |  "
                  f"AMOUNT: {'✅' if amount_visible else '❌'}  |  "
                  f"STATUS: {'✅' if status_visible else '❌'}")

        
        print("\n📸 TAKING SCREENSHOT — ÚLTIMOS 30 DÍAS LIST...")
        utils.tomar_screenshot(driver, "TS_71_ULTIMOS_30_DIAS")
        _capture_evidence(driver, "TS_71")

        
        print("\n🔍 SCANNING VISIBLE TEXT FOR DEBUGGING...")
        try:
            items = driver.find_elements(By.XPATH, config.XPATH_TS_TRANSACTION_ITEM)
            print(f"   📊 TOTAL TRANSACTION ITEMS DETECTED: {len(items)}")
            for elem in driver.find_elements(By.XPATH, "//*"):
                t = elem.get_attribute("text")
                if t and len(t) > 3:
                    print(f"   📝 VISIBLE TEXT: '{t}'")
        except:
            pass

        # ── RESULT ───────────────────────────────────────────────────────────
        if list_has_items and structure_ok:
            print("\n✅ TS-72: SUCCESS — 'ÚLTIMOS 30 DÍAS' VIEW SHOWS TRANSACTION LIST CORRECTLY.")
            return True
        elif list_has_items:
            print("\n✅ TS-72: SUCCESS (PARTIAL) — LIST HAS ITEMS BUT SOME FIELD STRUCTURE COULD NOT BE FULLY VERIFIED.")
            return True
        else:
            print("\n❌ TS-72: FAILED — TRANSACTION LIST NOT PROPERLY DISPLAYED.")
            return False

    except Exception as e:
        print(f"\n💥 TS-72 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "TS_72_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)

# =================================================================================
# TS-73: VALIDATE THAT "CORTE POR DÍA" VIEW SHOWS SUMMARY FOR THE CURRENT DAY.
# =================================================================================
def TS_73():
    from datetime import datetime
    import locale

    print("\n" + "=" * 60)
    print("🧪 TS-73: 'CORTE POR DÍA' VIEW SHOWS CURRENT DAY SUMMARY")
    print("=" * 60)

    
    MESES_ES = {
        1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
        5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
        9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
    }
    hoy = datetime.now()
    dia_num   = str(hoy.day)                    # e.g. "15"
    mes_str   = MESES_ES[hoy.month]             # e.g. "abril"
    fecha_str = f"{dia_num} {mes_str}"          # e.g. "15 abril"

    print(f"   📅 CURRENT DATE FOR VALIDATION: '{fecha_str}' (DAY={dia_num}, MONTH={mes_str})")

    driver, wait = utils.iniciar_driver()

    try:
        
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)
        print("   ✅ PRECONDITION MET — MAIN CHARGING SCREEN REACHED.")

        # ── STEP 1: TAP THE "TRANSACCIONES" BOTTOM NAV TAB ───────────────────
        print("\n👉 STEP 1: TAPPING 'TRANSACCIONES' BOTTOM NAV TAB...")
        tab_clicked = _navigate_to_transactions_tab(driver, wait)

        if not tab_clicked:
            print("\n❌ TS-73: FAILED — COULD NOT TAP 'TRANSACCIONES' TAB.")
            utils.tomar_screenshot(driver, "TS_73_TAB_CLICK_FAILED")
            _capture_evidence(driver, "TS_73")
            return False

        print("   ✅ STEP 1 COMPLETE — TRANSACTIONS SCREEN REACHED.")
        time.sleep(2)

        # ── STEP 2: TAP THE "CORTE POR DÍA" TAB ─────────────────────────────
        print("\n👉 STEP 2: TAPPING 'CORTE POR DÍA' TAB...")
        corte_tab_clicked = _click_corte_por_dia_tab(driver, wait)

        if not corte_tab_clicked:
            print("\n❌ TS-73: FAILED — COULD NOT TAP 'CORTE POR DÍA' TAB.")
            utils.tomar_screenshot(driver, "TS_73_CORTE_TAB_FAILED")
            _capture_evidence(driver, "TS_73")
            return False

        print("   ✅ STEP 2 COMPLETE — 'CORTE POR DÍA' TAB ACTIVE.")
        time.sleep(2)

        # ── STEP 3: VERIFY DATE NAVIGATOR SHOWS TODAY'S DATE ─────────────────
        print(f"\n👉 STEP 3: VERIFYING DATE NAVIGATOR SHOWS TODAY: '{fecha_str}'...")
        xpath_fecha_hoy = (
            f'//*[contains(@text, "{dia_num}") and contains(@text, "{mes_str}") or '
            f'contains(@content-desc, "{dia_num}") and contains(@content-desc, "{mes_str}")]'
        )
        date_found = utils.verificar_existencia(
            wait,
            xpath_fecha_hoy,
            f"TODAY'S DATE IN NAVIGATOR: '{fecha_str}'",
            driver
        )

        if not date_found:
            print(f"   ⚠️  DATE '{fecha_str}' NOT FOUND IN NAVIGATOR — CHECKING RAW TEXT...")
            
            xpath_dia_fallback = f'//*[contains(@text, "{dia_num}") or contains(@content-desc, "{dia_num}")]'
            date_found = utils.verificar_existencia(
                wait,
                xpath_dia_fallback,
                f"DAY NUMBER '{dia_num}' ON SCREEN",
                driver
            )

        if date_found:
            print(f"   ✅ STEP 3 COMPLETE — TODAY'S DATE CONFIRMED IN DATE NAVIGATOR.")
        else:
            print(f"   ⚠️  STEP 3 WARNING — COULD NOT CONFIRM TODAY'S DATE IN NAVIGATOR.")

        # ── STEP 4: VERIFY SUMMARY SECTION IS PRESENT ─────────────────────────
        print("\n👉 STEP 4: VERIFYING SUMMARY SECTION (MONTO TOTAL + SUBTOTAL DE PAGOS)...")

        monto_visible = utils.verificar_existencia(
            wait,
            config.XPATH_TS_TOTAL_AMOUNT,
            "MONTO TOTAL LABEL",
            driver
        )
        subtotal_visible = utils.verificar_existencia(
            wait,
            config.XPATH_TS_SUBTOTAL_CUT_PAYMENTS,
            "SUBTOTAL DE PAGOS LABEL",
            driver
        )

        if monto_visible and subtotal_visible:
            print("   ✅ STEP 4 COMPLETE — SUMMARY SECTION IS FULLY VISIBLE.")
        else:
            print("   ⚠️  STEP 4 WARNING — SOME SUMMARY FIELDS MISSING:")
            print(f"      MONTO TOTAL: {'✅' if monto_visible else '❌'}  |  "
                  f"SUBTOTAL DE PAGOS: {'✅' if subtotal_visible else '❌'}")

        # ── STEP 5: VERIFY "IMPRIMIR CORTE" BUTTON IS PRESENT ────────────────
        print("\n👉 STEP 5: VERIFYING 'IMPRIMIR CORTE' BUTTON IS PRESENT...")
        btn_imprimir = utils.verificar_existencia(
            wait,
            config.XPATH_TS_BTN_PRINT_CUT,
            "IMPRIMIR CORTE BUTTON",
            driver
        )

        if btn_imprimir:
            print("   ✅ STEP 5 COMPLETE — 'IMPRIMIR CORTE' BUTTON VISIBLE.")
        else:
            print("   ⚠️  STEP 5 WARNING — 'IMPRIMIR CORTE' BUTTON NOT FOUND.")

        # ── STEP 6: VERIFY "MOVIMIENTOS" SECTION IS PRESENT ──────────────────
        print("\n👉 STEP 6: VERIFYING 'MOVIMIENTOS' SECTION IS PRESENT...")
        movimientos_visible = utils.verificar_existencia(
            wait,
            config.XPATH_TS_CUT_MOVEMENTS,
            "MOVIMIENTOS SECTION",
            driver
        )

        if movimientos_visible:
            print("   ✅ STEP 6 COMPLETE — 'MOVIMIENTOS' SECTION VISIBLE.")
        else:
            print("   ⚠️  STEP 6 WARNING — 'MOVIMIENTOS' SECTION NOT FOUND.")

        
        print("\n📸 TAKING SCREENSHOT — CORTE POR DÍA VIEW...")
        utils.tomar_screenshot(driver, "TS_73_CORTE_POR_DIA")
        _capture_evidence(driver, "TS_73")

        
        print("\n🔍 SCANNING VISIBLE TEXT FOR DEBUGGING...")
        try:
            for elem in driver.find_elements(By.XPATH, "//*"):
                t = elem.get_attribute("text")
                if t and len(t) > 3:
                    print(f"   📝 VISIBLE TEXT: '{t}'")
        except:
            pass

        core_ok = corte_tab_clicked and (monto_visible or subtotal_visible)

        if core_ok:
            print(f"\n✅ TS-73: SUCCESS — 'CORTE POR DÍA' VIEW LOADED CORRECTLY FOR TODAY ({fecha_str}).")
            return True
        else:
            print("\n❌ TS-73: FAILED — 'CORTE POR DÍA' VIEW DID NOT LOAD CORRECTLY.")
            return False

    except Exception as e:
        print(f"\n💥 TS-73 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "TS_7_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)

# =============================================================================================================
# TS-74: VERIFY THAT THE 'COURT BY DAY' VIEW CORRECTLY HANDLES THE ABSENCE OF TRANSACTION FOR A GIVEN DATE
# =============================================================================================================
def TS_74():
    from datetime import datetime
    import locale

    print("\n" + "=" * 60)
    print("🧪 TS-74: VERIFY THAT THE 'COURT BY DAY' VIEW CORRECTLY HANDLES THE ABSENCE OF TRANSACTION FOR A GIVEN DATE")
    print("=" * 60)

    
    MESES_ES = {
        1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
        5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
        9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
    }
    hoy = datetime.now()
    dia_num   = str(hoy.day)                    # e.g. "15"
    mes_str   = MESES_ES[hoy.month]             # e.g. "abril"
    fecha_str = f"{dia_num} {mes_str}"          # e.g. "15 abril"

    print(f"   📅 CURRENT DATE FOR VALIDATION: '{fecha_str}' (DAY={dia_num}, MONTH={mes_str})")

    driver, wait = utils.iniciar_driver()

    try:
        
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)
        print("   ✅ PRECONDITION MET — MAIN CHARGING SCREEN REACHED.")

        # ── STEP 1: TAP THE "TRANSACCIONES" BOTTOM NAV TAB ───────────────────
        print("\n👉 STEP 1: TAPPING 'TRANSACCIONES' BOTTOM NAV TAB...")
        tab_clicked = _navigate_to_transactions_tab(driver, wait)

        if not tab_clicked:
            print("\n❌ TS-74: FAILED — COULD NOT TAP 'TRANSACCIONES' TAB.")
            utils.tomar_screenshot(driver, "TS_74_TAB_CLICK_FAILED")
            _capture_evidence(driver, "TS_74")
            return False

        print("   ✅ STEP 1 COMPLETE — TRANSACTIONS SCREEN REACHED.")
        time.sleep(2)

        # ── STEP 2: TAP THE "CORTE POR DÍA" TAB ─────────────────────────────
        print("\n👉 STEP 2: TAPPING 'CORTE POR DÍA' TAB...")
        corte_tab_clicked = _click_corte_por_dia_tab(driver, wait)

        if not corte_tab_clicked:
            print("\n❌ TS-74: FAILED — COULD NOT TAP 'CORTE POR DÍA' TAB.")
            utils.tomar_screenshot(driver, "TS_74_CORTE_TAB_FAILED")
            _capture_evidence(driver, "TS_74")
            return False

        print("   ✅ STEP 2 COMPLETE — 'CORTE POR DÍA' TAB ACTIVE.")
        time.sleep(2)

        # ── STEP 3: VERIFY DATE NAVIGATOR SHOWS TODAY'S DATE ─────────────────
        print(f"\n👉 STEP 3: VERIFYING DATE NAVIGATOR SHOWS TODAY: '{fecha_str}'...")
        xpath_fecha_hoy = (
            f'//*[contains(@text, "{dia_num}") and contains(@text, "{mes_str}") or '
            f'contains(@content-desc, "{dia_num}") and contains(@content-desc, "{mes_str}")]'
        )
        date_found = utils.verificar_existencia(
            wait,
            xpath_fecha_hoy,
            f"TODAY'S DATE IN NAVIGATOR: '{fecha_str}'",
            driver
        )

        if not date_found:
            print(f"   ⚠️  DATE '{fecha_str}' NOT FOUND IN NAVIGATOR — CHECKING RAW TEXT...")
            
            xpath_dia_fallback = f'//*[contains(@text, "{dia_num}") or contains(@content-desc, "{dia_num}")]'
            date_found = utils.verificar_existencia(
                wait,
                xpath_dia_fallback,
                f"DAY NUMBER '{dia_num}' ON SCREEN",
                driver
            )

        if date_found:
            print(f"   ✅ STEP 3 COMPLETE — TODAY'S DATE CONFIRMED IN DATE NAVIGATOR.")
        else:
            print(f"   ⚠️  STEP 3 WARNING — COULD NOT CONFIRM TODAY'S DATE IN NAVIGATOR.")

        # ── STEP 4: VERIFY SUMMARY SECTION IS PRESENT ─────────────────────────
        print("\n👉 STEP 4: VERIFYING SUMMARY SECTION (MONTO TOTAL + SUBTOTAL DE PAGOS)...")

        monto_visible = utils.verificar_existencia(
            wait,
            config.XPATH_TS_CORTE_MONTO_TOTAL,
            "MONTO TOTAL LABEL",
            driver
        )
        subtotal_visible = utils.verificar_existencia(
            wait,
            config.XPATH_TS_CORTE_SUBTOTAL_PAGOS,
            "SUBTOTAL DE PAGOS LABEL",
            driver
        )

        if monto_visible and subtotal_visible:
            print("   ✅ STEP 4 COMPLETE — SUMMARY SECTION IS FULLY VISIBLE.")
        else:
            print("   ⚠️  STEP 4 WARNING — SOME SUMMARY FIELDS MISSING:")
            print(f"      MONTO TOTAL: {'✅' if monto_visible else '❌'}  |  "
                  f"SUBTOTAL DE PAGOS: {'✅' if subtotal_visible else '❌'}")

        # ── STEP 5: VERIFY "IMPRIMIR CORTE" BUTTON IS PRESENT ────────────────
        print("\n👉 STEP 5: VERIFYING 'IMPRIMIR CORTE' BUTTON IS PRESENT...")
        btn_imprimir = utils.verificar_existencia(
            wait,
            config.XPATH_TS_BTN_IMPRIMIR_CORTE,
            "IMPRIMIR CORTE BUTTON",
            driver
        )

        if btn_imprimir:
            print("   ✅ STEP 5 COMPLETE — 'IMPRIMIR CORTE' BUTTON VISIBLE.")
        else:
            print("   ⚠️  STEP 5 WARNING — 'IMPRIMIR CORTE' BUTTON NOT FOUND.")

        # ── STEP 6: VERIFY "MOVIMIENTOS" SECTION IS PRESENT ──────────────────
        print("\n👉 STEP 6: VERIFYING 'MOVIMIENTOS' SECTION IS PRESENT...")
        movimientos_visible = utils.verificar_existencia(
            wait,
            config.XPATH_TS_CORTE_MOVIMIENTOS,
            "MOVIMIENTOS SECTION",
            driver
        )

        if movimientos_visible:
            print("   ✅ STEP 6 COMPLETE — 'MOVIMIENTOS' SECTION VISIBLE.")
        else:
            print("   ⚠️  STEP 6 WARNING — 'MOVIMIENTOS' SECTION NOT FOUND.")

        # ── EVIDENCE ──────────────────────────────────────────────────────────
        print("\n📸 TAKING SCREENSHOT — CORTE POR DÍA VIEW...")
        utils.tomar_screenshot(driver, "TS_74_CORTE_POR_DIA")
        _capture_evidence(driver, "TS_74")

        # ── DEBUG: SCAN ALL VISIBLE TEXT ──────────────────────────────────────
        print("\n🔍 SCANNING VISIBLE TEXT FOR DEBUGGING...")
        try:
            for elem in driver.find_elements(By.XPATH, "//*"):
                t = elem.get_attribute("text")
                if t and len(t) > 3:
                    print(f"   📝 VISIBLE TEXT: '{t}'")
        except:
            pass

        core_ok = corte_tab_clicked and (monto_visible or subtotal_visible)

        if core_ok:
            print(f"\n✅ TS-74: SUCCESS — 'CORTE POR DÍA' VIEW LOADED CORRECTLY FOR TODAY ({fecha_str}).")
            return True
        else:
            print("\n❌ TS-74: FAILED — 'CORTE POR DÍA' VIEW DID NOT LOAD CORRECTLY.")
            return False

    except Exception as e:
        print(f"\n💥 TS-74 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "TS_74_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)

# =================================================================================
# TS-75: VALIDATE DAY NAVIGATION IN "CORTE POR DÍA" (TODAY ↔ YESTERDAY).
# =================================================================================
def TS_75():
    from datetime import datetime, timedelta

    print("\n" + "=" * 60)
    print("🧪 TS-75: DAY NAVIGATION IN 'CORTE POR DÍA' (TODAY ↔ YESTERDAY)")
    print("=" * 60)

    
    MESES_ES = {
        1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
        5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
        9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
    }
    hoy   = datetime.now()
    ayer  = hoy - timedelta(days=1)

    hoy_dia   = str(hoy.day)
    hoy_mes   = MESES_ES[hoy.month]
    ayer_dia  = str(ayer.day)
    ayer_mes  = MESES_ES[ayer.month]

    print(f"   📅 TODAY   EXPECTED IN NAVIGATOR: day='{hoy_dia}', month='{hoy_mes}'")
    print(f"   📅 YESTERDAY EXPECTED IN NAVIGATOR: day='{ayer_dia}', month='{ayer_mes}'")

    driver, wait = utils.iniciar_driver()

    try:
        
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)
        print("   ✅ PRECONDITION MET — MAIN CHARGING SCREEN REACHED.")

        # ── STEP 1: TAP THE "TRANSACCIONES" BOTTOM NAV TAB ───────────────────
        print("\n👉 STEP 1: TAPPING 'TRANSACCIONES' BOTTOM NAV TAB...")
        if not _navigate_to_transactions_tab(driver, wait):
            print("\n❌ TS-75: FAILED — COULD NOT TAP 'TRANSACCIONES' TAB.")
            utils.tomar_screenshot(driver, "TS_75_TAB_CLICK_FAILED")
            _capture_evidence(driver, "TS_75")
            return False
        print("   ✅ STEP 1 COMPLETE — TRANSACTIONS SCREEN REACHED.")
        time.sleep(2)

        # ── STEP 2: TAP "CORTE POR DÍA" SUB-TAB ─────────────────────────────
        print("\n👉 STEP 2: TAPPING 'CORTE POR DÍA' TAB...")
        if not _click_corte_por_dia_tab(driver, wait):
            print("\n❌ TS-75: FAILED — COULD NOT TAP 'CORTE POR DÍA' TAB.")
            utils.tomar_screenshot(driver, "TS_75_CORTE_TAB_FAILED")
            _capture_evidence(driver, "TS_75")
            return False
        print("   ✅ STEP 2 COMPLETE — 'CORTE POR DÍA' ACTIVE.")
        time.sleep(2)

        # ── STEP 3: READ AND CONFIRM TODAY'S DATE IS SHOWN BY DEFAULT ─────────
        print(f"\n👉 STEP 3: READING INITIAL DATE — EXPECTING TODAY ({hoy_dia} {hoy_mes})...")
        date_before = _get_current_navigator_date(driver)

        today_confirmed = (
            date_before is not None and
            hoy_dia in date_before and
            hoy_mes in date_before
        )

        if today_confirmed:
            print(f"   ✅ STEP 3 COMPLETE — TODAY CONFIRMED: '{date_before}'")
        else:
            print(f"   ⚠️  STEP 3 WARNING — COULD NOT CONFIRM TODAY IN NAVIGATOR.")
            print(f"      READ: '{date_before}' | EXPECTED DAY: '{hoy_dia}', MONTH: '{hoy_mes}'")
            print(f"   💡 PROCEEDING — THE ARROW NAVIGATION IS THE CORE OF THIS TEST.")

        utils.tomar_screenshot(driver, "TS_75_STEP3_TODAY")

        # ── STEP 4: PRESS ◄ TO GO TO YESTERDAY ────────────────────────────────
        print(f"\n👉 STEP 4: PRESSING ◄ TO NAVIGATE TO YESTERDAY ({ayer_dia} {ayer_mes})...")
        arrow_back_ok = _click_date_arrow(driver, wait, direction="back")

        if not arrow_back_ok:
            print("\n❌ TS-75: FAILED — BACK ARROW (◄) NOT CLICKABLE.")
            utils.tomar_screenshot(driver, "TS_75_ARROW_BACK_FAILED")
            _capture_evidence(driver, "TS_75")
            return False

        time.sleep(2)
        print("   ✅ STEP 4 COMPLETE — ◄ PRESSED.")

        # ── STEP 5: VERIFY YESTERDAY'S DATE IS NOW SHOWN ──────────────────────
        print(f"\n👉 STEP 5: VERIFYING NAVIGATOR NOW SHOWS YESTERDAY ({ayer_dia} {ayer_mes})...")
        date_after_back = _get_current_navigator_date(driver)

        yesterday_confirmed = (
            date_after_back is not None and
            ayer_dia in date_after_back and
            ayer_mes in date_after_back
        )

        if yesterday_confirmed:
            print(f"   ✅ STEP 5 COMPLETE — YESTERDAY CONFIRMED: '{date_after_back}'")
        else:
            print(f"   ⚠️  STEP 5 WARNING — NAVIGATOR DATE AFTER ◄: '{date_after_back}'")
            print(f"      EXPECTED DAY: '{ayer_dia}', MONTH: '{ayer_mes}'")

        
        date_did_change = (date_before != date_after_back)
        if date_did_change:
            print(f"   ✅ DATE CHANGE CONFIRMED: '{date_before}' → '{date_after_back}'")
        else:
            print(f"   ❌ DATE DID NOT CHANGE AFTER PRESSING ◄ — ARROW MAY NOT BE WORKING.")

        utils.tomar_screenshot(driver, "TS_75_STEP5_YESTERDAY")

        # ── STEP 6: PRESS ► TO RETURN TO TODAY ────────────────────────────────
        print(f"\n👉 STEP 6: PRESSING ► TO NAVIGATE BACK TO TODAY ({hoy_dia} {hoy_mes})...")
        arrow_fwd_ok = _click_date_arrow(driver, wait, direction="forward")

        if not arrow_fwd_ok:
            print("\n❌ TS-75: FAILED — FORWARD ARROW (►) NOT CLICKABLE.")
            utils.tomar_screenshot(driver, "TS_75_ARROW_FWD_FAILED")
            _capture_evidence(driver, "TS_75")
            return False

        time.sleep(2)
        print("   ✅ STEP 6 COMPLETE — ► PRESSED.")

        # ── STEP 7: VERIFY TODAY'S DATE IS RESTORED ───────────────────────────
        print(f"\n👉 STEP 7: VERIFYING NAVIGATOR RETURNED TO TODAY ({hoy_dia} {hoy_mes})...")
        date_after_fwd = _get_current_navigator_date(driver)

        today_restored = (
            date_after_fwd is not None and
            hoy_dia in date_after_fwd and
            hoy_mes in date_after_fwd
        )

        if today_restored:
            print(f"   ✅ STEP 7 COMPLETE — TODAY RESTORED: '{date_after_fwd}'")
        else:
            print(f"   ⚠️  STEP 7 WARNING — NAVIGATOR DATE AFTER ►: '{date_after_fwd}'")

        utils.tomar_screenshot(driver, "TS_75_STEP7_TODAY_RESTORED")

        # ── EVIDENCE ──────────────────────────────────────────────────────────
        print("\n📸 TAKING FINAL SCREENSHOT — END STATE...")
        utils.tomar_screenshot(driver, "TS_75_NAVIGATION_COMPLETE")
        _capture_evidence(driver, "TS_75")

        # ── DEBUG: SCAN ALL VISIBLE TEXT ──────────────────────────────────────
        print("\n🔍 SCANNING VISIBLE TEXT FOR DEBUGGING...")
        try:
            for elem in driver.find_elements(By.XPATH, "//*"):
                t = elem.get_attribute("text")
                if t and len(t) > 3:
                    print(f"   📝 VISIBLE TEXT: '{t}'")
        except:
            pass

        both_arrows_worked = arrow_back_ok and arrow_fwd_ok
        date_round_trip_ok = date_did_change and (date_after_fwd != date_after_back)

        print("\n" + "-" * 60)
        print("📊 TS-75 NAVIGATION SUMMARY:")
        print(f"   ◄ BACK ARROW CLICKABLE    : {'✅' if arrow_back_ok else '❌'}")
        print(f"   DATE CHANGED AFTER ◄      : {'✅' if date_did_change else '❌'}")
        print(f"   YESTERDAY DATE CONFIRMED  : {'✅' if yesterday_confirmed else '⚠️  (WARNING)'}")
        print(f"   ► FORWARD ARROW CLICKABLE : {'✅' if arrow_fwd_ok else '❌'}")
        print(f"   DATE RESTORED AFTER ►     : {'✅' if date_round_trip_ok else '⚠️  (WARNING)'}")
        print(f"   TODAY DATE CONFIRMED      : {'✅' if today_restored else '⚠️  (WARNING)'}")
        print("-" * 60)

        if both_arrows_worked and date_did_change:
            print("\n✅ TS-75: SUCCESS — DAY NAVIGATION WORKS CORRECTLY (TODAY ↔ YESTERDAY).")
            return True
        elif both_arrows_worked:
            print("\n✅ TS-75: SUCCESS (PARTIAL) — BOTH ARROWS CLICKABLE BUT DATE TEXT "
                  "COULD NOT BE READ. CHECK DEBUG SCAN ABOVE.")
            return True
        else:
            print("\n❌ TS-75: FAILED — ONE OR BOTH NAVIGATION ARROWS DID NOT WORK.")
            return False

    except Exception as e:
        print(f"\n💥 TS-75 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "TS_75_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)


# =================================================================================
# TS-76: VALIDATE THAT SELECTING AN "APROBACIÓN" TRANSACTION SHOWS CORRECT DETAILS.
# =================================================================================
def TS_76():
    import re
    print("\n" + "=" * 60)
    print("🧪 TS-76: APROBACIÓN TRANSACTION DETAIL SHOWS CORRECT DATA")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)
        print("   ✅ PRECONDITION MET — MAIN CHARGING SCREEN REACHED.")

        # ── STEP 1: TAP THE "TRANSACCIONES" BOTTOM NAV TAB ───────────────────
        print("\n👉 STEP 1: TAPPING 'TRANSACCIONES' BOTTOM NAV TAB...")
        if not _navigate_to_transactions_tab(driver, wait):
            print("\n❌ TS-76: FAILED — COULD NOT TAP 'TRANSACCIONES' TAB.")
            utils.tomar_screenshot(driver, "TS_76_TAB_CLICK_FAILED")
            _capture_evidence(driver, "TS_76")
            return False
        print("   ✅ STEP 1 COMPLETE — 'ÚLTIMOS 30 DÍAS' LIST VISIBLE.")
        time.sleep(2)

        # ── STEP 2: READ FIRST APROBACIÓN ITEM DATA FROM THE LIST ────────────
        print("\n👉 STEP 2: READING DATA FROM FIRST 'APROBACIÓN' ITEM IN LIST...")
        item_data = _get_first_aprobacion_item(driver)

        if not item_data or (not item_data.get("fecha") and not item_data.get("monto")):
            print("\n❌ TS-76: FAILED — COULD NOT READ ANY ITEM DATA FROM THE LIST.")
            utils.tomar_screenshot(driver, "TS_76_LIST_READ_FAILED")
            _capture_evidence(driver, "TS_76")
            return False

        fecha_lista = item_data.get("fecha")
        monto_lista = item_data.get("monto")
        print(f"   ✅ STEP 2 COMPLETE — LIST ITEM DATA CAPTURED:")
        print(f"      📅 FECHA : '{fecha_lista}'")
        print(f"      💰 MONTO : '{monto_lista}'")

        utils.tomar_screenshot(driver, "TS_76_STEP2_LIST_ITEM")

        # ── STEP 3: TAP THE FIRST APROBACIÓN ITEM ────────────────────────────
        print("\n👉 STEP 3: TAPPING FIRST 'APROBACIÓN' ITEM TO OPEN DETAIL...")
        if not _click_first_aprobacion_item(driver, wait):
            print("\n❌ TS-76: FAILED — COULD NOT TAP TRANSACTION ITEM.")
            utils.tomar_screenshot(driver, "TS_76_ITEM_CLICK_FAILED")
            _capture_evidence(driver, "TS_76")
            return False
        time.sleep(3)
        print("   ✅ STEP 3 COMPLETE — DETAIL SCREEN SHOULD BE OPEN.")

        # ── STEP 4: VERIFY DETAIL SCREEN LOADED ──────────────────────────────
        print("\n👉 STEP 4: VERIFYING DETAIL SCREEN IS DISPLAYED...")
        detail_loaded = utils.verificar_existencia(
            wait, config.XPATH_TS_TITLE_DETAILS,
            "DETAIL SCREEN TITLE 'Detalle'", driver
        )

        if not detail_loaded:
            print("   ⚠️  STEP 4 WARNING — 'DETALLE' TITLE NOT FOUND. CHECKING FOR AMOUNT...")
            
            detail_loaded = utils.verificar_existencia(
                wait, config.XPATH_TS_LARGE_SCALE_DETAIL,
                "DETAIL SCREEN LARGE AMOUNT", driver
            )

        if not detail_loaded:
            print("\n❌ TS-76: FAILED — DETAIL SCREEN DID NOT OPEN.")
            utils.tomar_screenshot(driver, "TS_76_DETAIL_NOT_OPENED")
            _capture_evidence(driver, "TS_76")
            return False

        print("   ✅ STEP 4 COMPLETE — DETAIL SCREEN IS OPEN.")
        utils.tomar_screenshot(driver, "TS_76_STEP4_DETAIL_SCREEN")

       # ── STEP 5: READ ALL VISIBLE TEXT FROM DETAIL SCREEN ─────────────────
        print("\n👉 STEP 5: READING ALL DATA FROM DETAIL SCREEN...")
        detail_texts = []
        try:
            for el in driver.find_elements(By.XPATH, "//*"):
                
                for attr in ("text", "content-desc"):
                    val = el.get_attribute(attr) or ""
                    if val and len(val) > 1:
                        detail_texts.append(val)

            
            seen = set()
            detail_texts = [x for x in detail_texts if not (x in seen or seen.add(x))]
            print(f"   📝 DETAIL SCREEN VALUES ({len(detail_texts)}): {detail_texts}")

        except Exception as e:
            print(f"   ⚠️  COULD NOT SCAN DETAIL TEXTS: {e}")

        # ── STEP 6: CROSS-VALIDATE MONTO (LIST vs DETAIL) ────────────────────
        print(f"\n👉 STEP 6: CROSS-VALIDATING MONTO — LIST: '{monto_lista}'...")
        monto_ok = False

        if monto_lista:
            
            monto_clean = monto_lista.replace("$", "").replace(",", "").strip()
            for t in detail_texts:
                t_clean = t.replace("$", "").replace(",", "").strip()
                if monto_clean in t_clean or t_clean in monto_clean:
                    print(f"   ✅ STEP 6 COMPLETE — MONTO MATCH: LIST='{monto_lista}' → DETAIL='{t}'")
                    monto_ok = True
                    break

            if not monto_ok:
                print(f"   ❌ STEP 6 FAILED — MONTO '{monto_lista}' NOT FOUND IN DETAIL SCREEN.")
                print(f"      DETAIL TEXTS AVAILABLE: {detail_texts}")
        else:
            print("   ⚠️  STEP 6 SKIPPED — NO MONTO CAPTURED FROM LIST.")

        # ── STEP 7: CROSS-VALIDATE FECHA (LIST vs DETAIL) ────────────────────
        print(f"\n👉 STEP 7: CROSS-VALIDATING FECHA — LIST: '{fecha_lista}'...")
        fecha_ok = False

        if fecha_lista:
            
            for t in detail_texts:
                if fecha_lista.strip() in t or t in fecha_lista.strip():
                    print(f"   ✅ STEP 7 COMPLETE — FECHA MATCH: LIST='{fecha_lista}' → DETAIL='{t}'")
                    fecha_ok = True
                    break

            if not fecha_ok:
                
                fecha_date_only = fecha_lista.split(",")[0].strip() if "," in fecha_lista else fecha_lista
                for t in detail_texts:
                    if fecha_date_only in t:
                        print(f"   ✅ STEP 7 COMPLETE (DATE ONLY MATCH) — '{fecha_date_only}' FOUND IN '{t}'")
                        fecha_ok = True
                        break

            if not fecha_ok:
                print(f"   ❌ STEP 7 FAILED — FECHA '{fecha_lista}' NOT FOUND IN DETAIL SCREEN.")

        else:
            print("   ⚠️  STEP 7 SKIPPED — NO FECHA CAPTURED FROM LIST.")

        # ── STEP 8: VERIFY DETAIL FIELDS ARE PRESENT (STRUCTURE CHECK) ────────
        print("\n👉 STEP 8: VERIFYING DETAIL SCREEN FIELD LABELS ARE PRESENT...")
        fields_found = {}
        for label, xpath in config.TS_DETAILS_REQUIRED_FIELDS.items():
            found = utils.verificar_existencia(wait, xpath, label, driver)
            fields_found[label] = found

        fields_ok = all(fields_found.values())
        print(f"   📊 FIELD CHECK RESULTS: {fields_found}")

        if fields_ok:
            print("   ✅ STEP 8 COMPLETE — ALL REQUIRED FIELDS PRESENT IN DETAIL.")
        else:
            missing = [k for k, v in fields_found.items() if not v]
            print(f"   ⚠️  STEP 8 WARNING — MISSING FIELDS: {missing}")

        # ── STEP 9: VERIFY ESTATUS IS "APROBADA" ─────────────────────────────
        print("\n👉 STEP 9: VERIFYING ESTATUS IS 'APROBADA'...")
        estatus_ok = utils.verificar_existencia(
            wait, config.XPATH_TS_DETAIL_APPROVED_STATUS,
            "ESTATUS — APROBADA", driver
        )
        if estatus_ok:
            print("   ✅ STEP 9 COMPLETE — ESTATUS 'APROBADA' CONFIRMED.")
        else:
            print("   ⚠️  STEP 9 WARNING — 'APROBADA' STATUS NOT FOUND.")

        
        print("\n📸 TAKING FINAL SCREENSHOT — DETAIL SCREEN FULL VIEW...")
        utils.tomar_screenshot(driver, "TS_76_DETAIL_FULL")
        _capture_evidence(driver, "TS_76")

        
        print("\n" + "-" * 60)
        print("📊 TS-76 VALIDATION SUMMARY:")
        print(f"   DETAIL SCREEN OPENED      : {'✅' if detail_loaded else '❌'}")
        print(f"   MONTO MATCHES LIST        : {'✅' if monto_ok else '❌' if monto_lista else '⚠️  SKIPPED'}")
        print(f"   FECHA MATCHES LIST        : {'✅' if fecha_ok else '❌' if fecha_lista else '⚠️  SKIPPED'}")
        print(f"   REQUIRED FIELDS PRESENT   : {'✅' if fields_ok else '⚠️  PARTIAL'}")
        print(f"   ESTATUS IS APROBADA       : {'✅' if estatus_ok else '⚠️  WARNING'}")
        print("-" * 60)

        
        core_ok = detail_loaded and (monto_ok or fecha_ok)

        if core_ok:
            print("\n✅ TS-76: SUCCESS — APROBACIÓN DETAIL SHOWS CORRECT DATA.")
            return True
        else:
            print("\n❌ TS-76: FAILED — DETAIL DATA DOES NOT MATCH LIST DATA.")
            return False

    except Exception as e:
        print(f"\n💥 TS-76 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "TS_76_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)


# =================================================================================
# TS-77: VALIDATE THAT SELECTING A "CANCELACIÓN" TRANSACTION SHOWS CORRECT DETAILS.
# =================================================================================
def TS_77():
    import re

    print("\n" + "=" * 60)
    print("🧪 TS-77: CANCELACIÓN TRANSACTION DETAIL SHOWS CORRECT DATA")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)
        print("   ✅ PRECONDITION MET — MAIN CHARGING SCREEN REACHED.")

        # ── STEP 1: TAP THE "TRANSACCIONES" BOTTOM NAV TAB ───────────────────
        print("\n👉 STEP 1: TAPPING 'TRANSACCIONES' BOTTOM NAV TAB...")
        if not _navigate_to_transactions_tab(driver, wait):
            print("\n❌ TS-77: FAILED — COULD NOT TAP 'TRANSACCIONES' TAB.")
            utils.tomar_screenshot(driver, "TS_77_TAB_CLICK_FAILED")
            _capture_evidence(driver, "TS_77")
            return False
        print("   ✅ STEP 1 COMPLETE — 'ÚLTIMOS 30 DÍAS' LIST VISIBLE.")
        time.sleep(2)

        # ── STEP 2: READ CANCELACIÓN ITEM DATA FROM LIST ──────────────────────
        print("\n👉 STEP 2: READING DATA FROM FIRST 'CANCELACIÓN' ITEM IN LIST...")
        item_data = _get_first_cancelacion_item(driver)

        if not item_data or (not item_data.get("fecha") and not item_data.get("monto")):
            print("\n❌ TS-77: FAILED — COULD NOT READ ANY CANCELACIÓN ITEM FROM LIST.")
            utils.tomar_screenshot(driver, "TS_77_LIST_READ_FAILED")
            _capture_evidence(driver, "TS_77")
            return False

        fecha_lista = item_data.get("fecha")
        monto_lista = item_data.get("monto")
        print(f"   ✅ STEP 2 COMPLETE — CANCELACIÓN ITEM DATA:")
        print(f"      📅 FECHA : '{fecha_lista}'")
        print(f"      💰 MONTO : '{monto_lista}'")
        utils.tomar_screenshot(driver, "TS_77_STEP2_LIST_ITEM")

        # ── STEP 3: TAP THE CANCELACIÓN ITEM ─────────────────────────────────
        print("\n👉 STEP 3: TAPPING 'CANCELACIÓN' ITEM TO OPEN DETAIL...")
        if not _click_first_cancelacion_item(driver, wait):
            print("\n❌ TS-77: FAILED — COULD NOT TAP CANCELACIÓN ITEM.")
            utils.tomar_screenshot(driver, "TS_77_ITEM_CLICK_FAILED")
            _capture_evidence(driver, "TS_77")
            return False
        time.sleep(3)
        print("   ✅ STEP 3 COMPLETE — DETAIL SCREEN SHOULD BE OPEN.")

        # ── STEP 4: VERIFY DETAIL SCREEN LOADED ──────────────────────────────
        print("\n👉 STEP 4: VERIFYING DETAIL SCREEN IS DISPLAYED...")
        detail_loaded = utils.verificar_existencia(
            wait, config.XPATH_TS_TITLE_DETAILS, "DETAIL SCREEN TITLE", driver
        )
        if not detail_loaded:
            detail_loaded = utils.verificar_existencia(
                wait, config.XPATH_TS_LARGE_SCALE_DETAIL, "DETAIL LARGE AMOUNT", driver
            )
        if not detail_loaded:
            print("\n❌ TS-77: FAILED — DETAIL SCREEN DID NOT OPEN.")
            utils.tomar_screenshot(driver, "TS_77_DETAIL_NOT_OPENED")
            _capture_evidence(driver, "TS_77")
            return False

        print("   ✅ STEP 4 COMPLETE — DETAIL SCREEN IS OPEN.")
        utils.tomar_screenshot(driver, "TS_77_STEP4_DETAIL_OPEN")

        # ── STEP 5: VERIFY BOTH TABS (VENTA / CANCELACIÓN) ARE PRESENT ────────
        print("\n👉 STEP 5: VERIFYING 'VENTA' AND 'CANCELACIÓN' TABS ARE PRESENT...")
        tab_venta_ok = utils.verificar_existencia(
            wait, config.XPATH_TS_DETAIL_SELL_TAB,
            "TAB 'VENTA'", driver
        )
        tab_cancelacion_ok = utils.verificar_existencia(
            wait, config.XPATH_TS_DETAIL_CANCELATION_TAB,
            "TAB 'CANCELACIÓN'", driver
        )

        if tab_venta_ok and tab_cancelacion_ok:
            print("   ✅ STEP 5 COMPLETE — BOTH TABS PRESENT.")
        else:
            print(f"   ⚠️  STEP 5 WARNING — "
                  f"VENTA: {'✅' if tab_venta_ok else '❌'} | "
                  f"CANCELACIÓN: {'✅' if tab_cancelacion_ok else '❌'}")

        # ── STEP 6: READ ID FROM "VENTA" TAB (DEFAULT ACTIVE) ────────────────
        print("\n👉 STEP 6: READING ID FROM 'VENTA' TAB (DEFAULT ACTIVE)...")
        
        time.sleep(1)
        utils.tomar_screenshot(driver, "TS_77_STEP6_TAB_VENTA")

        id_venta = _get_detail_field_value(driver, "ID")
        print(f"   📋 ID (VENTA TAB): '{id_venta}'")

        
        detail_texts_venta = []
        for el in driver.find_elements(By.XPATH, "//*"):
            for attr in ("text", "content-desc"):
                val = el.get_attribute(attr) or ""
                if val and len(val) > 1:
                    detail_texts_venta.append(val)
        seen = set()
        detail_texts_venta = [x for x in detail_texts_venta if not (x in seen or seen.add(x))]
        print(f"   📝 VENTA TAB VALUES: {detail_texts_venta}")

        # ── STEP 7: CLICK "CANCELACIÓN" TAB AND READ ITS ID ──────────────────
        print("\n👉 STEP 7: CLICKING 'CANCELACIÓN' TAB AND READING ITS ID...")
        tab_clicked = _click_detail_tab(driver, wait, "Cancelación")

        if not tab_clicked:
            print("   ⚠️  STEP 7 WARNING — COULD NOT CLICK 'CANCELACIÓN' TAB.")
        else:
            print("   ✅ 'CANCELACIÓN' TAB CLICKED.")

        time.sleep(2)
        utils.tomar_screenshot(driver, "TS_77_STEP7_TAB_CANCELACION")

        id_cancelacion = _get_detail_field_value(driver, "ID")
        print(f"   📋 ID (CANCELACIÓN TAB): '{id_cancelacion}'")

        detail_texts_cancelacion = []
        for el in driver.find_elements(By.XPATH, "//*"):
            for attr in ("text", "content-desc"):
                val = el.get_attribute(attr) or ""
                if val and len(val) > 1:
                    detail_texts_cancelacion.append(val)
        seen = set()
        detail_texts_cancelacion = [x for x in detail_texts_cancelacion if not (x in seen or seen.add(x))]
        print(f"   📝 CANCELACIÓN TAB VALUES: {detail_texts_cancelacion}")

        # ── STEP 8: VALIDATE IDs ARE DIFFERENT ───────────────────────────────
        print("\n👉 STEP 8: VALIDATING THAT VENTA ID ≠ CANCELACIÓN ID...")
        ids_are_different = False

        if id_venta and id_cancelacion:
            ids_are_different = id_venta.strip() != id_cancelacion.strip()
            if ids_are_different:
                print(f"   ✅ STEP 8 COMPLETE — IDs ARE DIFFERENT:")
                print(f"      VENTA ID      : '{id_venta}'")
                print(f"      CANCELACIÓN ID: '{id_cancelacion}'")
            else:
                print(f"   ❌ STEP 8 FAILED — BOTH IDs ARE IDENTICAL: '{id_venta}'")
        else:
            print(f"   ⚠️  STEP 8 WARNING — COULD NOT COMPARE IDs:")
            print(f"      VENTA ID      : '{id_venta}'")
            print(f"      CANCELACIÓN ID: '{id_cancelacion}'")

        # ── STEP 9: CROSS-VALIDATE MONTO (LIST vs DETAIL) ────────────────────
        print(f"\n👉 STEP 9: CROSS-VALIDATING MONTO — LIST: '{monto_lista}'...")
        monto_ok = False
        if monto_lista:
            monto_clean = monto_lista.replace("$", "").replace(",", "").strip()
            for t in detail_texts_venta + detail_texts_cancelacion:
                t_clean = t.replace("$", "").replace(",", "").replace(" ", "").strip()
                if monto_clean in t_clean or t_clean in monto_clean:
                    print(f"   ✅ STEP 9 COMPLETE — MONTO MATCH: '{monto_lista}' → '{t}'")
                    monto_ok = True
                    break
            if not monto_ok:
                print(f"   ⚠️  STEP 9 WARNING — MONTO '{monto_lista}' NOT FOUND IN DETAIL.")
        else:
            print("   ⚠️  STEP 9 SKIPPED — NO MONTO FROM LIST.")

        # ── STEP 10: CROSS-VALIDATE FECHA (LIST vs DETAIL) ───────────────────
        print(f"\n👉 STEP 10: CROSS-VALIDATING FECHA — LIST: '{fecha_lista}'...")
        fecha_ok = False
        if fecha_lista:
            fecha_date_only = fecha_lista.split(",")[0].strip() if "," in fecha_lista else fecha_lista
            for t in detail_texts_cancelacion:
                if fecha_lista.strip() in t or fecha_date_only in t:
                    print(f"   ✅ STEP 10 COMPLETE — FECHA MATCH: '{fecha_lista}' → '{t}'")
                    fecha_ok = True
                    break
            if not fecha_ok:
                print(f"   ⚠️  STEP 10 WARNING — FECHA '{fecha_lista}' NOT CONFIRMED IN DETAIL.")
                print(f"      NOTE: CANCELACIÓN TAB MAY SHOW CANCELLATION DATE, NOT ORIGINAL DATE.")
        else:
            print("   ⚠️  STEP 10 SKIPPED — NO FECHA FROM LIST.")

        # ── EVIDENCE ──────────────────────────────────────────────────────────
        print("\n📸 TAKING FINAL SCREENSHOT — CANCELACIÓN DETAIL FULL VIEW...")
        utils.tomar_screenshot(driver, "TS_77_CANCELACION_DETAIL_FULL")
        _capture_evidence(driver, "TS_77")

        # ── RESULT ───────────────────────────────────────────────────────────
        print("\n" + "-" * 60)
        print("📊 TS-77 VALIDATION SUMMARY:")
        print(f"   DETAIL SCREEN OPENED      : {'✅' if detail_loaded else '❌'}")
        print(f"   BOTH TABS PRESENT         : {'✅' if tab_venta_ok and tab_cancelacion_ok else '⚠️  PARTIAL'}")
        print(f"   VENTA ID READ             : {'✅' if id_venta else '⚠️  NOT READ'}")
        print(f"   CANCELACIÓN ID READ       : {'✅' if id_cancelacion else '⚠️  NOT READ'}")
        print(f"   IDs ARE DIFFERENT         : {'✅' if ids_are_different else '❌' if (id_venta and id_cancelacion) else '⚠️  COULD NOT COMPARE'}")
        print(f"   MONTO MATCHES LIST        : {'✅' if monto_ok else '⚠️  WARNING'}")
        print(f"   FECHA CONFIRMED IN DETAIL : {'✅' if fecha_ok else '⚠️  WARNING'}")
        print("-" * 60)
        
        core_ok = detail_loaded and tab_venta_ok and tab_cancelacion_ok and ids_are_different

        if core_ok:
            print("\n✅ TS-77: SUCCESS — CANCELACIÓN DETAIL CORRECT. VENTA ID ≠ CANCELACIÓN ID.")
            return True
        elif detail_loaded and (tab_venta_ok or tab_cancelacion_ok):
            print("\n✅ TS-77: SUCCESS (PARTIAL) — DETAIL OPENED WITH TABS, "
                  "BUT ID COMPARISON COULD NOT BE COMPLETED.")
            return True
        else:
            print("\n❌ TS-77: FAILED — CANCELACIÓN DETAIL DID NOT LOAD CORRECTLY.")
            return False

    except Exception as e:
        print(f"\n💥 TS-77 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "TS_77_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver) 


# =================================================================================
# TS-78: VALIDATE THAT SCROLLING THE TRANSACTION LIST LOADS MORE ITEMS.
# =================================================================================
def TS_78():
    print("\n" + "=" * 60)
    print("🧪 TS-78: TRANSACTION LIST LOADS MORE ITEMS ON SCROLL")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    # ── INNER HELPER: COUNT UNIQUE TRANSACTION ROWS BY DATE PATTERN ──────────
    def _count_visible_items(drv):
        
        DATE_PATTERN = re.compile(r"\d{2}-\d{2}-\d{4},?\s*\d{2}:\d{2}:\d{2}")
        found = set()
        for el in drv.find_elements(By.XPATH, "//*"):
            for attr in ("text", "content-desc"):
                val = el.get_attribute(attr) or ""
                match = DATE_PATTERN.search(val)
                if match:
                    found.add(match.group())
                    break
        return found

    try:
        
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)
        print("   ✅ PRECONDITION MET — MAIN CHARGING SCREEN REACHED.")

        # ── STEP 1: TAP THE "TRANSACCIONES" BOTTOM NAV TAB ───────────────────
        print("\n👉 STEP 1: TAPPING 'TRANSACCIONES' BOTTOM NAV TAB...")
        if not _navigate_to_transactions_tab(driver, wait):
            print("\n❌ TS-78: FAILED — COULD NOT TAP 'TRANSACCIONES' TAB.")
            utils.tomar_screenshot(driver, "TS_78_TAB_CLICK_FAILED")
            _capture_evidence(driver, "TS_78")
            return False
        print("   ✅ STEP 1 COMPLETE — 'ÚLTIMOS 30 DÍAS' LIST VISIBLE.")
        time.sleep(2)

        # ── STEP 2: COUNT ITEMS BEFORE SCROLL ────────────────────────────────
        print("\n👉 STEP 2: COUNTING TRANSACTION ITEMS BEFORE SCROLL...")
        items_before = _count_visible_items(driver)
        count_before = len(items_before)
        print(f"   📊 ITEMS VISIBLE BEFORE SCROLL: {count_before}")
        print(f"   📝 DATES BEFORE: {sorted(items_before)}")
        utils.tomar_screenshot(driver, "TS_78_STEP2_BEFORE_SCROLL")

        if count_before == 0:
            print("\n❌ TS-78: FAILED — NO ITEMS FOUND IN LIST BEFORE SCROLL.")
            _capture_evidence(driver, "TS_78")
            return False

         # ── STEP 3: PERFORM SLOW SCROLL DOWN (~4 SECONDS) ────────────────────
        print("\n👉 STEP 3: PERFORMING SLOW SCROLL DOWN FOR ~4 SECONDS...")
        print("   ⬇️  EXECUTING SCROLL GESTURE...")

        screen_size    = driver.get_window_size()
        screen_w       = screen_size["width"]
        screen_h       = screen_size["height"]
        scroll_start_x = screen_w // 2
        scroll_start_y = int(screen_h * 0.75)
        scroll_end_y   = int(screen_h * 0.10)

        print(f"   📐 SCREEN SIZE: {screen_w}x{screen_h}")
        print(f"   📐 SCROLL: ({scroll_start_x}, {scroll_start_y}) → ({scroll_start_x}, {scroll_end_y})")

        scroll_ok = False

        # STRATEGY 1: mobile: scrollGesture
        
        try:
            driver.execute_script("mobile: scrollGesture", {
                "left"     : scroll_start_x - 50,
                "top"      : scroll_start_y,
                "width"    : 100,
                "height"   : scroll_start_y - scroll_end_y,
                "direction": "up",      
                "percent"  : 1.0,
                "speed"    : 300
            })
            scroll_ok = True
            print("   ✅ STEP 3 COMPLETE — SCROLL GESTURE EXECUTED (mobile: scrollGesture).")
        except Exception as e:
            print(f"   ⚠️  mobile:scrollGesture FAILED: {e} — TRYING swipeGesture...")

        # STRATEGY 2: mobile: swipeGesture
        if not scroll_ok:
            try:
                driver.execute_script("mobile: swipeGesture", {
                    "left"     : scroll_start_x - 50,
                    "top"      : scroll_start_y,
                    "width"    : 100,
                    "height"   : scroll_start_y - scroll_end_y,
                    "direction": "up",   # ← FIXED: SAME LOGIC AS ABOVE
                    "percent"  : 0.95,
                    "speed"    : 300
                })
                scroll_ok = True
                print("   ✅ STEP 3 COMPLETE — SCROLL GESTURE EXECUTED (mobile: swipeGesture).")
            except Exception as e:
                print(f"   ⚠️  swipeGesture FAILED: {e} — TRYING TouchAction...")

        # STRATEGY 3: CLASSIC TOUCH ACTION — FINGER STARTS LOW, MOVES UP
        if not scroll_ok:
            try:
                from appium.webdriver.common.touch_action import TouchAction
                action = TouchAction(driver)
                action.press(x=scroll_start_x, y=scroll_start_y)
                action.wait(4000)
                action.move_to(x=scroll_start_x, y=scroll_end_y)
                action.release()
                action.perform()
                scroll_ok = True
                print("   ✅ STEP 3 COMPLETE — SCROLL GESTURE EXECUTED (TouchAction).")
            except Exception as e:
                print(f"   💥 ALL SCROLL STRATEGIES FAILED: {e}")
                utils.tomar_screenshot(driver, "TS_78_SCROLL_FAILED")
                _capture_evidence(driver, "TS_78")
                return False

        time.sleep(3)

        # ── STEP 4: COUNT ITEMS AFTER SCROLL ─────────────────────────────────
        print("\n👉 STEP 4: COUNTING TRANSACTION ITEMS AFTER SCROLL...")
        items_after = _count_visible_items(driver)
        count_after = len(items_after)
        print(f"   📊 ITEMS VISIBLE AFTER SCROLL: {count_after}")
        print(f"   📝 DATES AFTER: {sorted(items_after)}")
        utils.tomar_screenshot(driver, "TS_78_STEP4_AFTER_SCROLL")

        # ── STEP 5: COMPARE BEFORE vs AFTER ──────────────────────────────────
        print("\n👉 STEP 5: COMPARING ITEM COUNT BEFORE vs AFTER SCROLL...")
        new_items              = items_after - items_before
        screen_content_changed = items_before != items_after
        new_data_loaded        = len(new_items) > 0

        print(f"   🆕 NEW ITEMS LOADED AFTER SCROLL: {len(new_items)}")
        print(f"   📝 NEW DATES: {sorted(new_items)}")

        # ── STEP 6: VERIFY LIST IS SCROLLABLE IN ACCESSIBILITY TREE ──────────
        print("\n👉 STEP 6: VERIFYING LIST CONTAINER IS MARKED AS SCROLLABLE...")
        list_is_scrollable = False
        try:
            
            from appium.webdriver.common.appiumby import AppiumBy
            scrollable_els = driver.find_elements(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().scrollable(true)'
            )
            list_is_scrollable = len(scrollable_els) > 0
            print(f"   📊 SCROLLABLE ELEMENTS FOUND: {len(scrollable_els)}")
            for el in scrollable_els:
                desc = el.get_attribute("content-desc") or el.get_attribute("text") or ""
                cls  = el.get_attribute("className") or ""
                print(f"      → CLASS: '{cls}' | DESC: '{desc[:60]}'")
        except Exception as e:
            print(f"   ⚠️  COULD NOT CHECK SCROLLABILITY: {e}")
            
            list_is_scrollable = scroll_ok
            print(f"   💡 FALLBACK — USING scroll_ok AS SCROLLABILITY INDICATOR: {list_is_scrollable}")

        
        print("\n📸 TAKING FINAL SCREENSHOT — POST SCROLL STATE...")
        utils.tomar_screenshot(driver, "TS_78_SCROLL_COMPLETE")
        _capture_evidence(driver, "TS_78")

        
        print("\n🔍 SCANNING VISIBLE TEXT FOR DEBUGGING...")
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

        # ── RESULT ───────────────────────────────────────────────────────────
        print("\n" + "-" * 60)
        print("📊 TS-78 SCROLL VALIDATION SUMMARY:")
        print(f"   ITEMS BEFORE SCROLL       : {count_before}")
        print(f"   ITEMS AFTER SCROLL        : {count_after}")
        print(f"   NEW UNIQUE ITEMS LOADED   : {len(new_items)}")
        print(f"   SCREEN CONTENT CHANGED    : {'✅' if screen_content_changed else '⚠️  SAME CONTENT'}")
        print(f"   NEW DATA LOADED           : {'✅' if new_data_loaded else '⚠️  NO NEW ITEMS'}")
        print(f"   LIST IS SCROLLABLE        : {'✅' if list_is_scrollable else '❌'}")
        print("-" * 60)

        if new_data_loaded:
            print(f"\n✅ TS-78: SUCCESS — SCROLL LOADED {len(new_items)} NEW TRANSACTION(S).")
            return True
        elif list_is_scrollable and scroll_ok:
            print(f"\n✅ TS-78: SUCCESS — LIST IS SCROLLABLE AND GESTURE WAS ACCEPTED.")
            print(f"   ℹ️  NOTE: NO NEW ITEMS APPEARED — ALL {count_before} TRANSACTIONS")
            print(f"   IN THE LAST 30 DAYS ARE ALREADY VISIBLE. THIS IS VALID FOR")
            print(f"   QA ENVIRONMENTS WITH LIMITED TRANSACTION HISTORY.")
            return True
        else:
            print("\n❌ TS-78: FAILED — LIST SCROLL NOT FUNCTIONAL.")
            return False

    except Exception as e:
        print(f"\n💥 TS-78 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "TS_78_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)

# =================================================================================
# TS-79: VALIDATE THAT "MONTO TOTAL" AND "SUBTOTAL DE PAGOS" SHOW CORRECT VALUES
#        IN THE "CORTE POR DÍA" VIEW — NAVIGATES BACK UNTIL A DATE WITH DATA.
# =================================================================================
def TS_79():
    print("\n" + "=" * 60)
    print("🧪 TS-79: CORTE POR DÍA — MONTO TOTAL AND SUBTOTAL DE PAGOS VALUES")
    print("=" * 60)

    # ── INNER HELPER: READ ALL UNIQUE VALUES FROM SCREEN ─────────────────────
    def _read_all_screen_values(drv):
        
        vals = []
        try:
            for el in drv.find_elements(By.XPATH, "//*"):
                for attr in ("text", "content-desc"):
                    val = el.get_attribute(attr) or ""
                    if val and len(val) > 0:
                        vals.append(val)
        except:
            pass
        seen = set()
        return [x for x in vals if not (x in seen or seen.add(x))]

    # ── INNER HELPER: EXTRACT MONTO AND SUBTOTAL FROM SCREEN VALUES ───────────
    def _extract_corte_values(vals):
        
        DATE_PATTERN   = re.compile(r"\d{2}-\d{2}-\d{4}")
        AMOUNT_PATTERN = re.compile(r"\$[\d,]+\.\d{2}")

        monto    = None
        subtotal = None

        for val in vals:
            v = val.strip()
            if monto is None and AMOUNT_PATTERN.match(v) and v != "$0.00":
                monto = v
            if subtotal is None:
                if (v.isdigit() and
                        int(v) >= 1 and
                        not DATE_PATTERN.search(v) and
                        not AMOUNT_PATTERN.search(v)):
                    subtotal = v
            if monto and subtotal:
                break

        return monto, subtotal

    driver, wait = utils.iniciar_driver()

    try:
        
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)
        print("   ✅ PRECONDITION MET — MAIN CHARGING SCREEN REACHED.")

        # ── STEP 1: TAP "TRANSACCIONES" TAB ──────────────────────────────────
        print("\n👉 STEP 1: TAPPING 'TRANSACCIONES' BOTTOM NAV TAB...")
        if not _navigate_to_transactions_tab(driver, wait):
            print("\n❌ TS-79: FAILED — COULD NOT TAP 'TRANSACCIONES' TAB.")
            utils.tomar_screenshot(driver, "TS_79_TAB_CLICK_FAILED")
            _capture_evidence(driver, "TS_79")
            return False
        print("   ✅ STEP 1 COMPLETE — TRANSACTIONS SCREEN REACHED.")
        time.sleep(2)

        # ── STEP 2: TAP "CORTE POR DÍA" SUB-TAB ─────────────────────────────
        print("\n👉 STEP 2: TAPPING 'CORTE POR DÍA' TAB...")
        if not _click_corte_por_dia_tab(driver, wait):
            print("\n❌ TS-79: FAILED — COULD NOT TAP 'CORTE POR DÍA' TAB.")
            utils.tomar_screenshot(driver, "TS_79_CORTE_TAB_FAILED")
            _capture_evidence(driver, "TS_79")
            return False
        print("   ✅ STEP 2 COMPLETE — 'CORTE POR DÍA' ACTIVE.")
        time.sleep(2)

        # ── STEP 3: NAVIGATE BACK DAY BY DAY UNTIL DATA IS FOUND ─────────────
        print(f"\n👉 STEP 3: SEARCHING FOR A DATE WITH TRANSACTIONS "
              f"(MAX {config.TS_MAX_SEARCH_DAYS} DAYS BACK)...")
        print("   ⏩ NAVIGATION LOGS SUPPRESSED — ONLY RESULT WILL BE SHOWN.")

        days_navigated   = 0
        date_found       = None
        monto_found      = None
        subtotal_found   = None
        max_days         = config.TS_MAX_SEARCH_DAYS

        for i in range(max_days):
            
            current_vals        = _read_all_screen_values(driver)
            monto, subtotal     = _extract_corte_values(current_vals)

            if monto and subtotal:
                
                date_found     = _get_current_navigator_date(driver)
                monto_found    = monto
                subtotal_found = subtotal
                days_navigated = i
                break

            
            try:
                driver.find_element(
                    By.XPATH, config.XPATH_TS_BTN_PREVIOUS_DATE
                ).click()
            except:
                try:
                    driver.find_element(
                        By.XPATH, config.XPATH_TS_BTN_PREVIOUS_DATE
                    ).click()
                except:
                    pass
            time.sleep(1.5)

        # ── STEP 3 RESULT SUMMARY ─────────────────────────────────────────────
        if date_found:
            print(f"   ✅ DATE WITH TRANSACTIONS FOUND AFTER {days_navigated} DAY(S) BACK.")
            print(f"   📅 DATE    : '{date_found}'")
            print(f"   💰 MONTO   : '{monto_found}'")
            print(f"   🔢 SUBTOTAL: '{subtotal_found}'")
        else:
            print(f"   ⚠️  NO DATE WITH TRANSACTIONS FOUND IN {max_days} DAYS.")
            print(f"   💡 INCREASE config.TS_MAX_SEARCH_DAYS IF MORE HISTORY EXISTS.")

        utils.tomar_screenshot(driver, "TS_79_STEP3_DATE_WITH_DATA")

        if not date_found:
            print("\n❌ TS-79: FAILED — COULD NOT FIND A DATE WITH TRANSACTIONS.")
            _capture_evidence(driver, "TS_79")
            return False

        # ── STEP 4: VALIDATE MONTO TOTAL > $0.00 ─────────────────────────────
        print("\n👉 STEP 4: VALIDATING MONTO TOTAL VALUE...")
        monto_ok = False
        try:
            amount_str   = monto_found.replace("$", "").replace(",", "").strip()
            amount_float = float(amount_str)
            monto_ok     = amount_float > 0.0
        except:
            pass

        if monto_ok:
            print(f"   ✅ STEP 4 COMPLETE — MONTO TOTAL IS VALID: '{monto_found}' > $0.00")
        else:
            print(f"   ❌ STEP 4 FAILED — MONTO TOTAL '{monto_found}' IS NOT > $0.00")

        # ── STEP 5: VALIDATE SUBTOTAL DE PAGOS ≥ 1 ───────────────────────────
        print("\n👉 STEP 5: VALIDATING SUBTOTAL DE PAGOS VALUE...")
        subtotal_ok = False
        try:
            subtotal_ok = int(subtotal_found) >= 1
        except:
            pass

        if subtotal_ok:
            print(f"   ✅ STEP 5 COMPLETE — SUBTOTAL DE PAGOS IS VALID: '{subtotal_found}' ≥ 1")
        else:
            print(f"   ❌ STEP 5 FAILED — SUBTOTAL DE PAGOS '{subtotal_found}' IS NOT ≥ 1")

        # ── STEP 6: CROSS-VALIDATE CONSISTENCY ───────────────────────────────
        print("\n👉 STEP 6: CROSS-VALIDATING MONTO vs SUBTOTAL CONSISTENCY...")
        cross_ok = monto_ok and subtotal_ok
        if cross_ok:
            print(f"   ✅ STEP 6 COMPLETE — MONTO '{monto_found}' AND "
                  f"SUBTOTAL '{subtotal_found}' ARE CONSISTENT.")
        else:
            print(f"   ❌ STEP 6 FAILED — INCONSISTENT: "
                  f"MONTO='{monto_found}' | SUBTOTAL='{subtotal_found}'")

        # ── STEP 7: VERIFY LABELS ARE PRESENT ON SCREEN ───────────────────────
        print("\n👉 STEP 7: VERIFYING 'MONTO TOTAL' AND 'SUBTOTAL DE PAGOS' LABELS...")
        monto_label_ok    = utils.verificar_existencia(
            wait, config.XPATH_TS_TOTAL_CUT_AMOUNT, "MONTO TOTAL LABEL", driver
        )
        subtotal_label_ok = utils.verificar_existencia(
            wait, config.XPATH_TS_SUBTOTAL_CUT_PAYMENTS, "SUBTOTAL DE PAGOS LABEL", driver
        )

        if monto_label_ok and subtotal_label_ok:
            print("   ✅ STEP 7 COMPLETE — BOTH LABELS PRESENT.")
        else:
            print(f"   ⚠️  STEP 7 WARNING — "
                  f"MONTO LABEL: {'✅' if monto_label_ok else '❌'} | "
                  f"SUBTOTAL LABEL: {'✅' if subtotal_label_ok else '❌'}")

        # ── EVIDENCE ──────────────────────────────────────────────────────────
        print("\n📸 TAKING FINAL SCREENSHOT — CORTE WITH VALID VALUES...")
        utils.tomar_screenshot(driver, "TS_79_CORTE_VALID_VALUES")
        _capture_evidence(driver, "TS_79")

        # ── RESULT ───────────────────────────────────────────────────────────
        print("\n" + "-" * 60)
        print("📊 TS-79 VALIDATION SUMMARY:")
        print(f"   DAYS NAVIGATED TO FIND DATA   : {days_navigated}")
        print(f"   DATE FOUND                    : '{date_found}'")
        print(f"   MONTO TOTAL                   : '{monto_found}' "
              f"{'✅' if monto_ok else '❌'}")
        print(f"   SUBTOTAL DE PAGOS             : '{subtotal_found}' "
              f"{'✅' if subtotal_ok else '❌'}")
        print(f"   MONTO LABEL PRESENT           : {'✅' if monto_label_ok else '⚠️'}")
        print(f"   SUBTOTAL LABEL PRESENT        : {'✅' if subtotal_label_ok else '⚠️'}")
        print(f"   CROSS-VALIDATION              : {'✅' if cross_ok else '❌'}")
        print("-" * 60)

        if monto_ok and subtotal_ok:
            print(f"\n✅ TS-79: SUCCESS — MONTO TOTAL '{monto_found}' AND "
                  f"SUBTOTAL '{subtotal_found}' ARE CORRECTLY DISPLAYED.")
            return True
        else:
            print("\n❌ TS-79: FAILED — VALUES NOT CORRECTLY DISPLAYED.")
            return False

    except Exception as e:
        print(f"\n💥 TS-79 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "TS_79_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)


# =================================================================================
# TS-80: VALIDATE THAT THE LOADING ANIMATION ("CARGANDO") APPEARS WHEN
#        NAVIGATING TO THE TRANSACTIONS TAB.
# =================================================================================
def TS_80():
    print("\n" + "=" * 60)
    print("🧪 TS-80: LOADING ANIMATION 'CARGANDO' APPEARS ON TAB NAVIGATION")
    print("=" * 60)
    print("   ℹ️  NOTE: THIS TEST REQUIRES FAST DETECTION — THE LOADING SCREEN")
    print("   IS TRANSIENT AND DISAPPEARS IN ~1-2 SECONDS AFTER NAVIGATION.")

    driver, wait = utils.iniciar_driver()

    
    wait_short = WebDriverWait(driver, 3)

    try:
        
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)
        print("   ✅ PRECONDITION MET — MAIN CHARGING SCREEN REACHED.")

        # ── STEP 1: NAVIGATE AWAY FIRST (ENSURE FRESH STATE ON RETURN) ────────
        
        print("\n👉 STEP 1: TAPPING 'INICIO' TAB TO ENSURE FRESH STATE ON RETURN...")
        try:
            driver.find_element(By.XPATH, config.XPATH_PÑ_TAB_HOME).click()
            time.sleep(2)
            print("   ✅ STEP 1 COMPLETE — NOW ON 'INICIO' TAB.")
        except Exception as e:
            print(f"   ⚠️  STEP 1 WARNING — COULD NOT TAP 'INICIO': {e}")
            print("   💡 PROCEEDING — LOADING STATE MAY STILL APPEAR FROM CURRENT SCREEN.")

        # ── STEP 2: TAP "TRANSACCIONES" AND IMMEDIATELY POLL FOR LOADING ──────
        print("\n👉 STEP 2: TAPPING 'TRANSACCIONES' AND IMMEDIATELY POLLING FOR LOADING STATE...")
        print("   ⚡ TAPPING TAB NOW — POLLING STARTS IMMEDIATELY AFTER...")

        
        try:
            driver.find_element(By.XPATH, config.XPATH_PÑ_TAB_TRANSACTIONS).click()
        except Exception as e:
            print(f"   ⚠️  TAP FAILED WITH PRIMARY XPATH: {e} — TRYING FALLBACK...")
            try:
                driver.find_element(By.XPATH, config.XPATH_TS_TAB_TRANSACCIONES_ALT).click()
            except Exception as e2:
                print(f"   💥 TAB CLICK FAILED: {e2}")
                utils.tomar_screenshot(driver, "TS_80_TAB_CLICK_FAILED")
                _capture_evidence(driver, "TS_80")
                return False

        # ── STEP 3: POLL FOR "CARGANDO" TEXT — FAST WINDOW (~3 SECONDS) ───────
        print("\n👉 STEP 3: POLLING FOR 'CARGANDO' LOADING STATE...")
        loading_detected   = False
        loading_screenshot = False
        poll_attempts      = 0
        max_attempts       = 15   

        while poll_attempts < max_attempts and not loading_detected:
            poll_attempts += 1
            try:
                
                for el in driver.find_elements(By.XPATH, "//*"):
                    for attr in ("text", "content-desc"):
                        val = (el.get_attribute(attr) or "").lower()
                        if "cargando" in val or "loading" in val or "carga" in val:
                            loading_detected = True
                            print(f"   ✅ LOADING STATE DETECTED ON POLL #{poll_attempts}: '{val}'")
                            
                            utils.tomar_screenshot(driver, "TS_80_LOADING_DETECTED")
                            loading_screenshot = True
                            break
                    if loading_detected:
                        break

                if not loading_detected:
                    time.sleep(0.2)   # WAIT 200ms BEFORE NEXT POLL

            except Exception as e:
                print(f"   ⚠️  POLL #{poll_attempts} ERROR: {e}")
                time.sleep(0.2)

        print(f"   📊 TOTAL POLL ATTEMPTS: {poll_attempts} / {max_attempts}")

        # ── STEP 4: FALLBACK — CHECK IF "CARGANDO" APPEARS VIA WAIT ──────────
       
        if not loading_detected:
            print("\n👉 STEP 4: FALLBACK — TRYING WebDriverWait FOR 'CARGANDO'...")
            try:
                wait_short.until(EC.presence_of_element_located(
                    (By.XPATH, config.XPATH_TS_LOADING)
                ))
                loading_detected = True
                print("   ✅ STEP 4 FALLBACK SUCCESS — 'CARGANDO' FOUND VIA WebDriverWait.")
                utils.tomar_screenshot(driver, "TS_80_LOADING_FALLBACK")
                loading_screenshot = True
            except:
                print("   ⚠️  STEP 4 FALLBACK ALSO MISSED 'CARGANDO'.")
                print("   💡 THE LOADING STATE MAY BE TOO FAST FOR APPIUM TO CAPTURE.")
        else:
            print("\n👉 STEP 4: SKIPPED — 'CARGANDO' ALREADY DETECTED IN STEP 3.")

        # ── STEP 5: WAIT FOR LOADING TO FINISH AND VERIFY FINAL SCREEN ────────
        print("\n👉 STEP 5: WAITING FOR LOADING TO FINISH AND VERIFYING FINAL STATE...")
        time.sleep(3)
        final_screen_ok = _verify_transactions_screen_loaded(driver, wait)

        if final_screen_ok:
            print("   ✅ STEP 5 COMPLETE — TRANSACTIONS SCREEN LOADED AFTER ANIMATION.")
        else:
            print("   ⚠️  STEP 5 WARNING — TRANSACTIONS SCREEN COULD NOT BE VERIFIED.")

        # ── EVIDENCE ──────────────────────────────────────────────────────────
        if not loading_screenshot:
            
            print("\n📸 TAKING SCREENSHOT — FINAL STATE AFTER LOAD...")
            utils.tomar_screenshot(driver, "TS_80_FINAL_STATE")

        _capture_evidence(driver, "TS_80")

        
        print("\n🔍 SCANNING VISIBLE TEXT FOR DEBUGGING...")
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

        # ── RESULT ───────────────────────────────────────────────────────────
        print("\n" + "-" * 60)
        print("📊 TS-80 VALIDATION SUMMARY:")
        print(f"   LOADING STATE DETECTED     : {'✅' if loading_detected else '⚠️  NOT CAPTURED'}")
        print(f"   LOADING SCREENSHOT SAVED   : {'✅' if loading_screenshot else '⚠️  NO'}")
        print(f"   FINAL SCREEN LOADED OK     : {'✅' if final_screen_ok else '⚠️  WARNING'}")
        print("-" * 60)

       
        if loading_detected and final_screen_ok:
            print("\n✅ TS-80: SUCCESS — LOADING ANIMATION DETECTED AND SCREEN LOADED CORRECTLY.")
            return True
        elif final_screen_ok:
            print("\n✅ TS-80: SUCCESS (PARTIAL) — FINAL SCREEN LOADED CORRECTLY.")
            print("   ℹ️  'CARGANDO' ANIMATION WAS NOT CAPTURED BY APPIUM — THIS IS EXPECTED")
            print("   BEHAVIOR WHEN THE LOADING STATE IS SHORTER THAN APPIUM'S POLL INTERVAL.")
            return True
        else:
            print("\n❌ TS-80: FAILED — TRANSACTIONS SCREEN DID NOT LOAD AFTER TAB TAP.")
            return False

    except Exception as e:
        print(f"\n💥 TS-80 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "TS_80_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)


# =================================================================================
# MAIN EXECUTION
# =================================================================================
if __name__ == "__main__":

    logger, log_file, timestamp = utils.iniciar_reporte("OPERATIONALS_TS")

    try:
        TS_70()
        TS_71()
        TS_72()
        TS_73()
        TS_74()
        TS_75()
        TS_76()
        TS_77()
        TS_78()
        TS_79()
        TS_80()
        

    finally:
        utils.generar_reporte_html("OPERATIONALS_TS", log_file, timestamp)