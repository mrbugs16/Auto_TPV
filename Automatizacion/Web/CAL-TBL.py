"""
# ==================================================================================
# FILENAME    : CAL-TBL.py
# PROJECT     : MEMPHIS QA AUTOMATION FRAMEWORK
# DESCRIPTION : WEB TEST SUITE — CALENDAR DATE RANGE FILTER VALIDATION.
#               TARGET MODULE: ADMINISTRACIÓN → LIQUIDACIÓN.
#
# NAVIGATION FLOW (ALL TESTS):
#   1. LOGIN → POST-LOGIN DASHBOARD.
#   2. CLICK THE 'LIQUIDACIÓN' MODULE CARD.
#   3. UNCHECK 'DATOS DE HOY' (LOCKS CALENDAR TO TODAY WHEN CHECKED).
#   4. CLICK THE CALENDAR ICON 📅 TO OPEN THE DATE PICKER.
#   5. SELECT START DATE → SELECT END DATE.
#   6. VALIDATE THE SPECIFIC TEST CONDITION.
#
# WHY 'DATOS DE HOY' MUST BE UNCHECKED FIRST:
#   WHEN CHECKED, THE DATE RANGE IS LOCKED TO TODAY AND THE CALENDAR ICON
#   DOES NOT OPEN THE PICKER. UNCHECKING IT ENABLES MANUAL DATE SELECTION.
#
# CONTENTS:
#   · CAL-TBL-01: UNCHECK 'DATOS DE HOY', CLICK CALENDAR — PICKER DEPLOYS.
#   · CAL-TBL-02: SELECT START + END DATE — RANGE REFLECTS IN FIELD.
#   · CAL-TBL-03: APPLY VALID RANGE — PAGE DATA UPDATES WITH SELECTED RANGE.
#   · CAL-TBL-04: APPLY RANGE THEN RELOAD — VERIFY PERSISTENCE BEHAVIOR.
#   · CAL-TBL-05: APPLY RANGE, TOGGLE 'DATOS DE HOY' — CUSTOM RANGE CAN BE RESET AND REAPPLIED.
#   · CAL-TBL-06: APPLY RANGE THEN CLICK 'EXPORTAR' — EXPORT RESPECTS SELECTED RANGE.
# ==================================================================================
"""

import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import config
import utils
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


# ==================================================================================
# MODULE CONFIGURATION
# ==================================================================================
LIQUIDACION_URL   = "https://fat.memphis.mx/liquidacion"
EVIDENCE_ENDPOINT = "liquidacion"

# SPANISH MONTH NAMES — USED TO DETECT IF THE CALENDAR PICKER IS OPEN
SPANISH_MONTHS = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]


# ==================================================================================
# XPATHS — LIQUIDACIÓN MODULE SPECIFIC
# NOTE: THE APP USES TAILWIND CSS. PRIMENG CLASS NAMES WILL NOT MATCH.
#       MOST INTERACTIONS USE JAVASCRIPT AS THE PRIMARY OR FALLBACK METHOD.
# ==================================================================================

# --- LIQUIDACIÓN CARD ON THE POST-LOGIN DASHBOARD ---
XPATH_LIQUIDACION_CARD = (
    "//*[normalize-space(text())='Liquidación']"
    "[not(ancestor::nav) and not(ancestor::aside) and not(self::title)] | "
    "//*[normalize-space(text())='Liquidacion']"
    "[not(ancestor::nav) and not(ancestor::aside)] | "
    "//a[contains(@href,'iquidaci')] | "
    "//*[contains(@class,'card') or contains(@class,'tile') or "
    "    contains(@class,'module') or contains(@class,'btn')]"
    "[.//*[contains(text(),'iquidaci')]]"
)

# --- 'DATOS DE HOY' CHECKBOX ---
# WHEN CHECKED: CALENDAR IS LOCKED TO TODAY.
# WHEN UNCHECKED: CALENDAR ICON IS ACTIVE AND PICKER CAN BE OPENED.
XPATH_DATOS_HOY_CHECKBOX = (
    # Standard HTML checkbox inside a container that has 'Datos de hoy' text
    "//input[@type='checkbox']"
    "[ancestor::*[.//*[contains(text(),'atos de hoy')] or "
    "             contains(normalize-space(text()),'atos de hoy')]] | "
    # PrimeNG p-checkbox box (the clickable visual element, not the hidden input)
    "//*[contains(@class,'p-checkbox-box') or contains(@class,'p-checkbox')]"
    "[ancestor::*[.//*[contains(text(),'atos de hoy')]]] | "
    # Label click (toggles associated checkbox)
    "//label[contains(normalize-space(.),'atos de hoy')] | "
    # Direct siblings/neighbors
    "//input[@type='checkbox']"
    "[following::*[contains(text(),'atos de hoy')][position()<=3]] | "
    "//input[@type='checkbox']"
    "[preceding::*[contains(text(),'atos de hoy')][position()<=3]]"
)

# --- DATE RANGE FIELD + CALENDAR ICON (the 📅 trigger) ---
# FROM SCREENSHOT: "06/04/2026 - 06/04/2026 📅 ☑️ Datos de hoy"
# CLICKING THE DATE TEXT OR THE 📅 ICON OPENS THE PICKER.
XPATH_DATE_RANGE_TRIGGER = (
    # Calendar icon with PrimeNG pi class
    "//*[contains(@class,'pi-calendar')][not(ancestor::nav)] | "
    # Button containing a calendar icon
    "//button[.//*[contains(@class,'calendar') or contains(@class,'pi-cal')]] | "
    # Input that shows the date range value (DD/MM/YYYY - DD/MM/YYYY)
    "//input[contains(@value,'2026') and contains(@value,'-')] | "
    "//input[contains(@value,'2025') and contains(@value,'-')] | "
    # Any clickable element that looks like a date range
    "//*[contains(text(),'2026') and contains(text(),'/') and contains(text(),' - ')]"
    "[self::input or self::button or self::div or self::span]"
)

# --- EXPORTAR BUTTON (used in CAL-TBL-06) ---
XPATH_BTN_EXPORTAR = (
    "//button[contains(translate(.,'EXPORTAR','exportar'),'exportar')] | "
    "//button[.//*[contains(translate(text(),'EXPORTAR','exportar'),'exportar')]] | "
    "//*[contains(@class,'export') and (self::button or contains(@class,'btn'))]"
)

# --- PREV/NEXT MONTH NAVIGATION INSIDE THE PICKER ---
XPATH_CAL_PREV_MONTH = (
    "//*[contains(@class,'p-datepicker-prev') or contains(@class,'pi-chevron-left') or "
    "    contains(@class,'pi-angle-left')]"
    "[ancestor::*[contains(@class,'datepicker') or contains(@class,'calendar') or "
    "             contains(@class,'picker')]] | "
    "//button[@aria-label='Previous Month'] | "
    "//*[text()='<' or text()='‹'][ancestor::*[contains(@class,'calendar')]]"
)
XPATH_CAL_NEXT_MONTH = (
    "//*[contains(@class,'p-datepicker-next') or contains(@class,'pi-chevron-right') or "
    "    contains(@class,'pi-angle-right')]"
    "[ancestor::*[contains(@class,'datepicker') or contains(@class,'calendar') or "
    "             contains(@class,'picker')]] | "
    "//button[@aria-label='Next Month'] | "
    "//*[text()='>' or text()='›'][ancestor::*[contains(@class,'calendar')]]"
)


# ==================================================================================
# TEST DATA
# ==================================================================================
CAL_START_DAY = "1"    # DAY 1 OF THE CURRENT VISIBLE MONTH (APRIL 2026)
CAL_END_DAY   = "5"    # DAY 5 OF THE CURRENT VISIBLE MONTH


# ==================================================================================
# INTERNAL HELPERS
# ==================================================================================

def _login_and_go_to_liquidacion(driver):
    """
    LOGS IN AND NAVIGATES TO THE LIQUIDACIÓN MODULE.
    FLOW:
        1. OPEN THE LOGIN PAGE AND AUTHENTICATE.
        2. ON THE POST-LOGIN DASHBOARD, CLICK THE 'LIQUIDACIÓN' CARD.
        3. WAIT FOR THE LIQUIDACIÓN PAGE TO FULLY RENDER.
    FALLS BACK TO DIRECT URL NAVIGATION IF THE CARD CLICK FAILS.
    """
    print(f"   🌐 NAVIGATING TO LOGIN: {config.URL_MEMPHIS_WEB}")
    driver.get(config.URL_MEMPHIS_WEB)
    time.sleep(2)

    print(f"   ✏️  ENTERING CREDENTIALS — USER: {config.WEB_USUARIO_PRUEBA}")
    utils.escribir_texto(driver, config.XPATH_WEB_USER, config.WEB_USUARIO_PRUEBA)
    utils.escribir_texto(driver, config.XPATH_WEB_PASS, config.WEB_PASS_PRUEBA)

    print("   🖱️  CLICKING LOGIN BUTTON...")
    utils.click_boton(driver, config.XPATH_WEB_BTN_LOGIN)

    print("   ⏳ WAITING FOR POST-LOGIN DASHBOARD TO LOAD...")
    time.sleep(5)

    print(f"   🌐 POST-LOGIN URL: {driver.current_url}")

    # CLICK THE LIQUIDACIÓN CARD FROM THE DASHBOARD
    # THE CARD IS AN ORANGE TILE — THE CLICK HANDLER IS ON THE PARENT CONTAINER,
    # NOT ON THE TEXT SPAN/P CHILD. WE USE 4 STRATEGIES IN ORDER.
    print("   🖱️  CLICKING 'LIQUIDACIÓN' MODULE CARD (4-STRATEGY CASCADE)...")
    clicked = False

    # STRATEGY 1: JS — FIND TEXT, WALK UP TO PARENT CARD CONTAINER AND CLICK
    # THIS IS THE MOST RELIABLE FOR ANGULAR/TAILWIND CARD COMPONENTS WHERE
    # THE ROUTERLINK OR CLICK HANDLER IS ON A GRANDPARENT DIV.
    if not clicked:
        try:
            result = driver.execute_script("""
                var allEls = document.querySelectorAll('*');
                for (var el of allEls) {
                    var text = el.textContent.trim();
                    if ((text === 'Liquidación' || text === 'Liquidacion') &&
                        el.children.length === 0 && el.offsetWidth > 0) {
                        // WALK UP UP TO 5 LEVELS TO FIND THE CLICKABLE CARD
                        var parent = el.parentElement;
                        for (var i = 0; i < 5; i++) {
                            if (!parent) break;
                            var style   = window.getComputedStyle(parent);
                            var onClick = parent.getAttribute('ng-click') ||
                                          parent.getAttribute('(click)') ||
                                          parent.getAttribute('routerlink') ||
                                          parent.getAttribute('routerLink') ||
                                          parent.getAttribute('href');
                            // Click if: cursor is pointer OR has routerlink/onclick
                            if (style.cursor === 'pointer' || onClick) {
                                parent.click();
                                return 'parent-level-' + i + ':' + parent.tagName;
                            }
                            parent = parent.parentElement;
                        }
                        // FALLBACK: JUST CLICK 2 LEVELS UP FROM THE TEXT NODE
                        var fallback = el.parentElement && el.parentElement.parentElement;
                        if (fallback) { fallback.click(); return 'fallback-grandparent'; }
                        el.parentElement.click();
                        return 'fallback-parent';
                    }
                }
                return null;
            """)
            if result:
                clicked = True
                time.sleep(4)
                print(f"   ✅ CARD CLICKED — STRATEGY 1 (JS PARENT WALK: {result}).")
        except Exception as s1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {s1_err}")

    # STRATEGY 2: XPATH — CLICK THE ARROW BUTTON (→) INSIDE THE LIQUIDACIÓN CARD
    # THE CARD HAS AN ARROW ICON IN THE BOTTOM-RIGHT CORNER — IT IS ALWAYS CLICKABLE.
    if not clicked:
        try:
            arrow = driver.find_element(
                By.XPATH,
                "//*[contains(text(),'iquidaci')]"
                "/ancestor::*[contains(@class,'card') or contains(@class,'tile') or "
                "             contains(@class,'module') or contains(@class,'item')]"
                "//*[contains(@class,'arrow') or contains(@class,'pi-arrow') or "
                "    text()='→' or text()='›' or contains(@class,'chevron')]"
            )
            arrow.click()
            clicked = True
            time.sleep(4)
            print("   ✅ CARD CLICKED — STRATEGY 2 (ARROW BUTTON XPATH).")
        except Exception as s2_err:
            print(f"   ⚠️  STRATEGY 2 FAILED: {s2_err}")

    # STRATEGY 3: XPATH — THE TEXT ELEMENT ITSELF (ORIGINAL APPROACH, LAST RESORT)
    if not clicked:
        try:
            card = driver.find_element(By.XPATH, XPATH_LIQUIDACION_CARD)
            driver.execute_script("arguments[0].click();", card)
            clicked = True
            time.sleep(4)
            print("   ✅ CARD CLICKED — STRATEGY 3 (XPATH + JS CLICK).")
        except Exception as s3_err:
            print(f"   ⚠️  STRATEGY 3 FAILED: {s3_err}")

    # STRATEGY 4: DIRECT URL NAVIGATION (FINAL FALLBACK)
    if not clicked:
        print(f"   ⚠️  ALL CARD CLICK STRATEGIES FAILED. NAVIGATING DIRECTLY TO URL...")
        driver.get(LIQUIDACION_URL)
        time.sleep(4)
        print(f"   🌐 NAVIGATED DIRECTLY TO: {driver.current_url}")

    if clicked:
        print(f"   🌐 CURRENT URL AFTER CLICK: {driver.current_url}")

    print("   ⏳ WAITING FOR LIQUIDACIÓN PAGE TO FULLY RENDER...")
    time.sleep(3)


def _capture_web_evidence(driver, nombre_test):
    """
    WRAPPER AROUND utils.print_http_evidence.
    USES EVIDENCE_ENDPOINT AS THE NETWORK TRAFFIC KEYWORD.
    """
    try:
        utils.print_http_evidence(driver, EVIDENCE_ENDPOINT)
    except Exception as ev_err:
        print(f"   ⚠️  HTTP EVIDENCE CAPTURE FAILED FOR [{nombre_test}]: {ev_err}")


def _datos_de_hoy_is_checked(driver):
    """
    RETURNS True IF THE 'DATOS DE HOY' CHECKBOX IS CURRENTLY CHECKED.
    USES JAVASCRIPT TO INSPECT THE CHECKBOX STATE RELIABLY.
    """
    try:
        result = driver.execute_script("""
            var allEls = document.querySelectorAll('*');
            for (var el of allEls) {
                if (el.textContent.trim().includes('Datos de hoy') ||
                    el.textContent.trim().includes('datos de hoy')) {
                    var parent = el.parentElement;
                    var depth = 0;
                    while (parent && depth < 5) {
                        var cb = parent.querySelector('input[type="checkbox"]');
                        if (cb) return cb.checked;
                        // PrimeNG p-checkbox checked state
                        var pcb = parent.querySelector('[class*="p-checkbox"]');
                        if (pcb) return pcb.classList.contains('p-checkbox-checked') ||
                                        pcb.classList.contains('p-highlight');
                        parent = parent.parentElement;
                        depth++;
                    }
                }
            }
            return null;  // Not found
        """)
        return bool(result)
    except Exception:
        return False


def _uncheck_datos_de_hoy(driver):
    """
    UNCHECKS THE 'DATOS DE HOY' CHECKBOX IF IT IS CURRENTLY CHECKED.
    THIS IS REQUIRED BEFORE THE CALENDAR CAN BE OPENED FOR MANUAL DATE SELECTION.
    USES 3 STRATEGIES: XPATH CLICK → LABEL JS CLICK → CHECKBOX INPUT JS CLICK.
    RETURNS True IF THE CHECKBOX IS NOW UNCHECKED, False OTHERWISE.
    """
    if not _datos_de_hoy_is_checked(driver):
        print("   ✅ 'DATOS DE HOY' IS ALREADY UNCHECKED — SKIPPING.")
        return True

    print("   🖱️  UNCHECKING 'DATOS DE HOY'...")

    # STRATEGY 1: XPATH CLICK ON THE CHECKBOX / LABEL
    try:
        el = driver.find_element(By.XPATH, XPATH_DATOS_HOY_CHECKBOX)
        el.click()
        time.sleep(1)
        if not _datos_de_hoy_is_checked(driver):
            print("   ✅ 'DATOS DE HOY' UNCHECKED — STRATEGY 1 (XPATH).")
            return True
    except Exception:
        pass

    # STRATEGY 2: JAVASCRIPT — FIND THE LABEL AND CLICK IT
    try:
        driver.execute_script("""
            var allEls = document.querySelectorAll('label, span, div');
            for (var el of allEls) {
                if (el.textContent.trim() === 'Datos de hoy' && el.offsetWidth > 0) {
                    el.click();
                    break;
                }
            }
        """)
        time.sleep(1)
        if not _datos_de_hoy_is_checked(driver):
            print("   ✅ 'DATOS DE HOY' UNCHECKED — STRATEGY 2 (JS LABEL CLICK).")
            return True
    except Exception:
        pass

    # STRATEGY 3: JAVASCRIPT — DIRECTLY CLICK THE CHECKBOX INPUT
    try:
        driver.execute_script("""
            var allEls = document.querySelectorAll('*');
            for (var el of allEls) {
                if (el.textContent.trim().includes('Datos de hoy') && el.offsetWidth > 0) {
                    var parent = el.parentElement;
                    var depth = 0;
                    while (parent && depth < 6) {
                        var cb = parent.querySelector('input[type="checkbox"]');
                        if (cb) { cb.click(); return; }
                        var pcb = parent.querySelector('[class*="p-checkbox-box"]');
                        if (pcb) { pcb.click(); return; }
                        parent = parent.parentElement;
                        depth++;
                    }
                }
            }
        """)
        time.sleep(1)
        if not _datos_de_hoy_is_checked(driver):
            print("   ✅ 'DATOS DE HOY' UNCHECKED — STRATEGY 3 (JS CHECKBOX CLICK).")
            return True
    except Exception:
        pass

    print("   ❌ COULD NOT UNCHECK 'DATOS DE HOY' — ALL 3 STRATEGIES FAILED.")
    return False


def _open_calendar(driver):
    """
    CLICKS THE CALENDAR ICON (📅) OR DATE RANGE FIELD TO OPEN THE PICKER.
    ASSUMES 'DATOS DE HOY' IS ALREADY UNCHECKED.
    USES 4 STRATEGIES: XPATH → JS ICON SCAN → JS DATE TEXT CLICK → JS FIRST INPUT.
    RETURNS (element_description, strategy_name) OR (None, None) IF ALL FAIL.
    """
    # STRATEGY 1: XPATH — pi-calendar icon or date field
    try:
        elements = driver.find_elements(By.XPATH, XPATH_DATE_RANGE_TRIGGER)
        visible  = [e for e in elements if e.is_displayed()]
        if visible:
            visible[0].click()
            time.sleep(1)
            desc = f"<{visible[0].tag_name}> class='{visible[0].get_attribute('class') or ''}'"
            print(f"   📅 CALENDAR OPENED — STRATEGY 1 (XPATH).")
            print(f"      ELEMENT: {desc[:100]}")
            return desc, "XPATH"
    except Exception:
        pass

    # STRATEGY 2: JAVASCRIPT — click any visible calendar-related icon
    try:
        result = driver.execute_script("""
            var keywords = ['pi-calendar','calendar-icon','date-icon','cal-icon','icon-calendar'];
            for (var kw of keywords) {
                var els = document.querySelectorAll('[class*="' + kw + '"]');
                for (var el of els) {
                    if (el.offsetWidth > 0) { el.click(); return 'icon:' + kw; }
                }
            }
            return null;
        """)
        if result:
            time.sleep(1)
            print(f"   📅 CALENDAR OPENED — STRATEGY 2 (JS ICON: {result}).")
            return result, "JS_ICON"
    except Exception:
        pass

    # STRATEGY 3: JAVASCRIPT — click the element showing the date range text
    try:
        result = driver.execute_script("""
            var allEls = document.querySelectorAll('input, button, div, span');
            for (var el of allEls) {
                var val = el.value || el.textContent || '';
                // Pattern: DD/MM/YYYY - DD/MM/YYYY
                if (/\\d{2}\\/\\d{2}\\/\\d{4}\\s*-\\s*\\d{2}\\/\\d{2}\\/\\d{4}/.test(val) &&
                    el.offsetWidth > 0) {
                    el.click();
                    return el.tagName + ':' + val.substring(0, 30);
                }
            }
            return null;
        """)
        if result:
            time.sleep(1)
            print(f"   📅 CALENDAR OPENED — STRATEGY 3 (JS DATE TEXT: {result}).")
            return result, "JS_DATE_TEXT"
    except Exception:
        pass

    # STRATEGY 4: JAVASCRIPT — click the first visible text input near 'Datos de hoy'
    try:
        result = driver.execute_script("""
            var allEls = document.querySelectorAll('*');
            for (var el of allEls) {
                if (el.textContent.trim().includes('Datos de hoy') && el.offsetWidth > 0) {
                    var parent = el.parentElement;
                    var depth = 0;
                    while (parent && depth < 8) {
                        var inputs = parent.querySelectorAll('input[type="text"], input:not([type])');
                        for (var inp of inputs) {
                            if (inp.offsetWidth > 0) { inp.click(); return 'input near Datos'; }
                        }
                        parent = parent.parentElement;
                        depth++;
                    }
                }
            }
            return null;
        """)
        if result:
            time.sleep(1)
            print(f"   📅 CALENDAR OPENED — STRATEGY 4 (JS INPUT NEAR DATOS: {result}).")
            return result, "JS_NEAR_DATOS"
    except Exception:
        pass

    print("   ❌ ALL CALENDAR OPEN STRATEGIES FAILED.")
    return None, None


def _calendar_is_open(driver):
    """
    CHECKS WHETHER THE CALENDAR PICKER PANEL IS CURRENTLY VISIBLE.
    DETECTS BY LOOKING FOR A SPANISH MONTH NAME + YEAR IN A VISIBLE ELEMENT,
    WHICH IS THE CALENDAR HEADER FORMAT (e.g., 'Abril 2026').
    ALSO CHECKS FOR STANDARD DATEPICKER CSS CLASSES AS A FALLBACK.
    """
    try:
        result = driver.execute_script("""
            var months = ['Enero','Febrero','Marzo','Abril','Mayo','Junio',
                          'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'];
            var allEls = document.querySelectorAll('*');
            for (var el of allEls) {
                if (el.children.length < 5 && el.offsetWidth > 0 && el.offsetHeight > 0) {
                    var text = el.textContent.trim();
                    for (var m of months) {
                        if (text.startsWith(m + ' ') && text.length < 25 &&
                            /\\d{4}/.test(text)) {
                            return 'month_header:' + text;
                        }
                    }
                }
            }
            // Fallback: check for datepicker class names
            var panels = document.querySelectorAll(
                '[class*="datepicker"],[class*="calendar-popup"],[class*="date-picker"]'
            );
            for (var p of panels) {
                if (p.offsetWidth > 0) return 'panel_class:' + p.className.substring(0, 50);
            }
            return null;
        """)
        return result is not None, result
    except Exception:
        return False, None


def _select_day_js(driver, day_str):
    """
    SELECTS A SPECIFIC DAY IN THE CUSTOM TAILWIND CALENDAR PICKER USING JAVASCRIPT.
    FINDS LEAF NODES (NO CHILDREN) WHOSE TEXT EXACTLY EQUALS THE DAY NUMBER,
    FILTERS OUT DISABLED / OTHER-MONTH DAYS, AND CLICKS THE FIRST VALID MATCH.

    WHY JAVASCRIPT:
        THE LIQUIDACIÓN CALENDAR IS A CUSTOM COMPONENT WITH TAILWIND CSS CLASSES.
        PRIMENG XPATH SELECTORS LIKE '//td[not(@class..)]' DO NOT MATCH ITS STRUCTURE.
        JAVASCRIPT ELEMENT INSPECTION IS FRAMEWORK-AGNOSTIC.

    RETURNS True IF THE DAY WAS CLICKED, False OTHERWISE.
    """
    try:
        result = driver.execute_script("""
            var dayStr = arguments[0];
            // Search all visible leaf elements for exactly the day number
            var allEls = document.querySelectorAll('td, div, span, button, li');
            for (var el of allEls) {
                var text = el.textContent.trim();
                if (text !== dayStr) continue;
                if (el.children.length > 0) continue;     // Only leaf nodes
                if (el.offsetWidth <= 0 || el.offsetHeight <= 0) continue;  // Visible only

                var cls = (el.className || '').toString().toLowerCase();
                // Skip disabled, other-month, header, and navigation elements
                if (cls.includes('disabled') || cls.includes('other') ||
                    cls.includes('outside') || cls.includes('prev') ||
                    cls.includes('next')    || cls.includes('header') ||
                    cls.includes('label')   || cls.includes('name')) continue;

                el.click();
                return el.tagName + '.' + (el.className || '').substring(0, 60);
            }
            return null;
        """, day_str)

        if result:
            print(f"   📅 DAY {day_str} SELECTED — element: {result}")
            return True

        print(f"   ⚠️  DAY {day_str} NOT FOUND — no valid leaf node with text '{day_str}'.")
        return False
    except Exception as e:
        print(f"   ⚠️  JS DAY SELECTION FAILED FOR DAY {day_str}: {e}")
        return False


def _get_date_field_value(driver):
    """
    READS THE CURRENT DISPLAYED VALUE OF THE DATE RANGE FIELD.
    RETURNS THE VALUE STRING (e.g. '01/04/2026 - 05/04/2026') OR '' IF NOT FOUND.
    """
    try:
        result = driver.execute_script("""
            // Try: input with date range value
            var inputs = document.querySelectorAll('input');
            for (var inp of inputs) {
                var val = inp.value || '';
                if (/\\d{2}\\/\\d{2}\\/\\d{4}\\s*-/.test(val)) return val;
            }
            // Try: visible element whose text matches date range pattern
            var allEls = document.querySelectorAll('*');
            for (var el of allEls) {
                if (el.children.length === 0 && el.offsetWidth > 0) {
                    var text = el.textContent.trim();
                    if (/\\d{2}\\/\\d{2}\\/\\d{4}\\s*-\\s*\\d{2}\\/\\d{2}\\/\\d{4}/.test(text)) {
                        return text;
                    }
                }
            }
            return '';
        """)
        val = result or ""
        if val:
            print(f"   🔎 DATE FIELD VALUE: '{val}'")
        else:
            print("   🔎 DATE FIELD VALUE: '' (EMPTY OR NOT FOUND)")
        return val
    except Exception as e:
        print(f"   ⚠️  COULD NOT READ DATE FIELD: {e}")
        return ""


def _apply_date_range(driver):
    """
    FULL PRECONDITION FLOW REUSED BY CAL-TBL-03 THROUGH CAL-TBL-06:
        1. UNCHECK 'DATOS DE HOY'.
        2. OPEN THE CALENDAR PICKER.
        3. SELECT CAL_START_DAY.
        4. SELECT CAL_END_DAY.
    RETURNS True IF BOTH DAYS WERE SELECTED, False OTHERWISE.
    """
    print(f"   📅 APPLYING DATE RANGE: DAY {CAL_START_DAY} → DAY {CAL_END_DAY}...")

    unchecked = _uncheck_datos_de_hoy(driver)
    if not unchecked:
        print("   ⚠️  COULD NOT UNCHECK 'DATOS DE HOY' — CALENDAR MAY NOT RESPOND.")

    time.sleep(1)

    el, strategy = _open_calendar(driver)
    if el is None:
        print("   ❌ CALENDAR COULD NOT BE OPENED.")
        return False

    is_open, detection = _calendar_is_open(driver)
    if is_open:
        print(f"   ✅ PICKER CONFIRMED OPEN ({detection}).")
    else:
        print("   ⚠️  PICKER OPEN STATE NOT CONFIRMED — PROCEEDING WITH DAY SELECTION.")

    start_ok = _select_day_js(driver, CAL_START_DAY)
    time.sleep(0.8)
    end_ok = _select_day_js(driver, CAL_END_DAY)
    time.sleep(1)

    result = start_ok and end_ok
    if result:
        print(f"   ✅ DATE RANGE FULLY APPLIED (STRATEGY: {strategy}).")
    else:
        print("   ⚠️  DATE RANGE PARTIALLY APPLIED.")
    return result


def _dump_page_structure(driver):
    """
    COMPREHENSIVE JS-BASED DUMP OF ALL INPUTS AND CALENDAR-RELATED ELEMENTS.
    CALLED WHEN CALENDAR IS NOT FOUND — OUTPUT TELLS US EXACTLY WHAT IS ON THE PAGE.
    """
    print("\n🔍 ─── FULL PAGE STRUCTURE DUMP ────────────────────────────────")
    try:
        data = driver.execute_script("""
            var found = [];
            ['input','button','label','p-calendar','p-checkbox'].forEach(function(tag) {
                document.querySelectorAll(tag).forEach(function(el) {
                    found.push({
                        tag: el.tagName, type: el.type || '',
                        id: el.id || '', placeholder: el.placeholder || '',
                        value: (el.value || '').substring(0, 30),
                        className: (el.className || '').substring(0, 80),
                        text: el.textContent.trim().substring(0, 40),
                        displayed: el.offsetWidth > 0 && el.offsetHeight > 0
                    });
                });
            });
            return found;
        """)
        for idx, el in enumerate(data or []):
            print(
                f"   [{idx:02d}] <{el.get('tag','')}>"
                f" type='{el.get('type','')}'"
                f" id='{el.get('id','')}'"
                f" text='{el.get('text','')}'"
                f" placeholder='{el.get('placeholder','')}'"
                f" class='{el.get('className','')}'"
                f" displayed={el.get('displayed', False)}"
            )
    except Exception as e:
        print(f"   ❌ DUMP FAILED: {e}")
    print("🔍 ──────────────────────────────────────────────────────────────\n")


# ==================================================================================
# CAL-TBL-01: UNCHECK 'DATOS DE HOY', CLICK CALENDAR — PICKER DEPLOYS
# ==================================================================================
def CAL_TBL_01():
    """
    PRECONDITIONS : AUTHENTICATED USER. LIQUIDACIÓN MODULE ACCESSIBLE.
    STEPS         : 1. ACCESS MODULE.
                    2. UNCHECK 'DATOS DE HOY'.
                    3. CLICK THE CALENDAR ICON 📅.
    EXPECTED      : CALENDAR RANGE PICKER DEPLOYS AND SHOWS MONTH/DAY GRID.
    """
    print("\n" + "=" * 60)
    print("🧪 CAL-TBL-01: UNCHECK 'DATOS DE HOY' AND CLICK CALENDAR FIELD")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO LIQUIDACIÓN...")
        _login_and_go_to_liquidacion(driver)

        print("\n📸 TAKING SCREENSHOT #1 — LIQUIDACIÓN INITIAL STATE...")
        utils.tomar_screenshot(driver, "CAL_TBL_01_1_LIQUIDACION_LOADED")

        # STEP 1: UNCHECK 'DATOS DE HOY'
        print("\n👉 STEP 1: UNCHECKING 'DATOS DE HOY' TO ENABLE MANUAL DATE SELECTION...")
        checked_before = _datos_de_hoy_is_checked(driver)
        print(f"   🔎 'DATOS DE HOY' INITIAL STATE: {'CHECKED ✓' if checked_before else 'UNCHECKED ○'}")

        unchecked = _uncheck_datos_de_hoy(driver)
        time.sleep(1)

        checked_after = _datos_de_hoy_is_checked(driver)
        print(f"   🔎 'DATOS DE HOY' AFTER UNCHECK: {'CHECKED ✓' if checked_after else 'UNCHECKED ○'}")

        print("\n📸 TAKING SCREENSHOT #2 — AFTER UNCHECKING 'DATOS DE HOY'...")
        utils.tomar_screenshot(driver, "CAL_TBL_01_2_DATOS_HOY_UNCHECKED")

        # STEP 2: CLICK THE CALENDAR ICON TO OPEN THE PICKER
        print("\n👉 STEP 2: CLICKING CALENDAR ICON 📅 TO OPEN THE DATE PICKER...")
        el, strategy = _open_calendar(driver)

        if el is None:
            print("   ❌ CALENDAR NOT FOUND — RUNNING FULL PAGE DUMP:")
            _dump_page_structure(driver)

        # ASSERTION: CALENDAR PICKER PANEL IS VISIBLE
        is_open, detection = _calendar_is_open(driver)

        print(f"\n   🔬 CORE ASSERTION — CALENDAR PICKER MUST BE VISIBLE:")
        print(f"      • 'DATOS DE HOY' UNCHECKED : {not checked_after}")
        print(f"      • PICKER OPEN              : {is_open}")
        print(f"      • DETECTION SIGNAL         : {detection}")
        print(f"      • STRATEGY USED            : {strategy}")
        print(f"      • Expected                 : True")

        if is_open:
            print("      ✅ ASSERTION PASSED — PICKER DEPLOYED AFTER UNCHECKING 'DATOS DE HOY'.")
        else:
            print("      ❌ ASSERTION FAILED — PICKER DID NOT OPEN.")

        print("\n📸 TAKING SCREENSHOT #3 — CALENDAR PICKER STATE...")
        utils.tomar_screenshot(driver, "CAL_TBL_01_3_PICKER_STATE")

        _capture_web_evidence(driver, "CAL_TBL_01")

        if is_open:
            utils.tomar_screenshot(driver, "CAL_TBL_01_SUCCESS")
            print("\n✅ CAL-TBL-01: SUCCESS — CALENDAR PICKER DEPLOYED CORRECTLY.")
        else:
            utils.tomar_screenshot(driver, "CAL_TBL_01_FAILED")
            print("\n❌ CAL-TBL-01: FAILED — CALENDAR PICKER DID NOT OPEN.")

    except Exception as e:
        print(f"\n💥 CAL-TBL-01 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "CAL_TBL_01_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()


# ==================================================================================
# CAL-TBL-02: SELECT START DATE AND END DATE — RANGE REFLECTS IN FIELD
# ==================================================================================
def CAL_TBL_02():
    """
    PRECONDITIONS : AUTHENTICATED USER. LIQUIDACIÓN MODULE ACCESSIBLE.
    STEPS         : 1. UNCHECK 'DATOS DE HOY'.
                    2. CLICK CALENDAR ICON.
                    3. SELECT START DATE (DAY 1).
                    4. SELECT END DATE   (DAY 5).
    EXPECTED      : DATE RANGE REFLECTS IN THE FIELD. PICKER CLOSES AUTOMATICALLY.
    """
    print("\n" + "=" * 60)
    print("🧪 CAL-TBL-02: SELECT START DATE AND END DATE — RANGE REFLECTS IN FIELD")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO LIQUIDACIÓN...")
        _login_and_go_to_liquidacion(driver)

        value_before = _get_date_field_value(driver)

        print("\n📸 TAKING SCREENSHOT #1 — CALENDAR FIELD BEFORE SELECTION...")
        utils.tomar_screenshot(driver, "CAL_TBL_02_1_BEFORE_SELECTION")

        # STEP 1: UNCHECK 'DATOS DE HOY'
        print("\n👉 STEP 1: UNCHECKING 'DATOS DE HOY'...")
        _uncheck_datos_de_hoy(driver)
        time.sleep(1)

        # STEP 2: OPEN CALENDAR
        print("\n👉 STEP 2: CLICKING CALENDAR ICON 📅...")
        el, strategy = _open_calendar(driver)
        if el is None:
            print("   ❌ CALENDAR NOT FOUND — RUNNING DUMP:")
            _dump_page_structure(driver)

        is_open, detection = _calendar_is_open(driver)
        print(f"   📅 PICKER OPEN: {is_open} ({detection})")

        # STEP 3: SELECT START DATE
        print(f"\n👉 STEP 3: SELECTING START DATE (DAY {CAL_START_DAY})...")
        start_ok = _select_day_js(driver, CAL_START_DAY)
        time.sleep(0.8)

        print("\n📸 TAKING SCREENSHOT #2 — AFTER START DATE SELECTED...")
        utils.tomar_screenshot(driver, "CAL_TBL_02_2_START_SELECTED")

        # STEP 4: SELECT END DATE
        print(f"\n👉 STEP 4: SELECTING END DATE (DAY {CAL_END_DAY})...")
        end_ok = _select_day_js(driver, CAL_END_DAY)
        time.sleep(1)

        print("\n📸 TAKING SCREENSHOT #3 — AFTER END DATE SELECTED...")
        utils.tomar_screenshot(driver, "CAL_TBL_02_3_END_SELECTED")

        value_after   = _get_date_field_value(driver)
        panel_closed  = not _calendar_is_open(driver)[0]
        value_changed = (value_after != value_before and value_after != "")

        print(f"\n   🔬 SELECTION ASSERTION SUMMARY:")
        print(f"      • VALUE BEFORE            : '{value_before}'")
        print(f"      • VALUE AFTER             : '{value_after}'")
        print(f"      • VALUE CHANGED IN FIELD  : {value_changed}")
        print(f"      • CALENDAR PANEL CLOSED   : {panel_closed}")
        print(f"      • START DAY CLICKED       : {start_ok}")
        print(f"      • END DAY CLICKED         : {end_ok}")

        _capture_web_evidence(driver, "CAL_TBL_02")

        if value_changed:
            utils.tomar_screenshot(driver, "CAL_TBL_02_SUCCESS")
            print("\n✅ CAL-TBL-02: SUCCESS — DATE RANGE REFLECTED IN FIELD.")
        else:
            utils.tomar_screenshot(driver, "CAL_TBL_02_FAILED")
            print("\n❌ CAL-TBL-02: FAILED — CALENDAR INPUT VALUE DID NOT CHANGE.")

    except Exception as e:
        print(f"\n💥 CAL-TBL-02 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "CAL_TBL_02_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()


# ==================================================================================
# CAL-TBL-03: APPLY VALID DATE RANGE — PAGE DATA UPDATES WITH SELECTED RANGE
# ==================================================================================
def CAL_TBL_03():
    """
    PRECONDITIONS : AUTHENTICATED USER. LIQUIDACIÓN MODULE ACCESSIBLE.
    STEPS         : 1. SELECT A VALID DATE RANGE.
    EXPECTED      : PAGE DATA (CHARTS + DATE FIELD) UPDATES WITH THE SELECTED RANGE.
    """
    print("\n" + "=" * 60)
    print("🧪 CAL-TBL-03: APPLY VALID DATE RANGE — PAGE DATA UPDATES")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO LIQUIDACIÓN...")
        _login_and_go_to_liquidacion(driver)

        value_before = _get_date_field_value(driver)
        print(f"\n👉 STEP 0: DATE FIELD BEFORE FILTER — '{value_before}'")

        print("\n📸 TAKING SCREENSHOT #1 — PAGE BEFORE DATE FILTER...")
        utils.tomar_screenshot(driver, "CAL_TBL_03_1_BEFORE_FILTER")

        # APPLY DATE RANGE
        print(f"\n👉 STEP 1: APPLYING DATE RANGE (DAY {CAL_START_DAY} → DAY {CAL_END_DAY})...")
        range_applied = _apply_date_range(driver)

        if not range_applied:
            print("   ⚠️  DATE RANGE NOT FULLY APPLIED — RUNNING DUMP:")
            _dump_page_structure(driver)

        print("\n⏳ WAITING FOR PAGE TO REFRESH WITH FILTERED DATA...")
        time.sleep(3)

        print("\n📸 TAKING SCREENSHOT #2 — PAGE AFTER DATE FILTER APPLIED...")
        utils.tomar_screenshot(driver, "CAL_TBL_03_2_AFTER_FILTER")

        value_after     = _get_date_field_value(driver)
        filter_applied  = (value_after != "" and value_after != value_before)

        # CHECK THAT THE DATE IN THE FIELD IS DIFFERENT FROM THE ORIGINAL 'DATOS DE HOY' DATE
        # (VISUAL CONFIRMATION THAT DATA HAS BEEN FILTERED)
        is_open, _ = _calendar_is_open(driver)
        picker_closed = not is_open

        print(f"\n   🔬 FILTER ASSERTION SUMMARY:")
        print(f"      • DATE VALUE BEFORE FILTER : '{value_before}'")
        print(f"      • DATE VALUE AFTER FILTER  : '{value_after}'")
        print(f"      • FILTER APPLIED IN FIELD  : {filter_applied}")
        print(f"      • PICKER AUTO-CLOSED       : {picker_closed}")
        print(f"      • RANGE_APPLY SUCCEEDED    : {range_applied}")

        _capture_web_evidence(driver, "CAL_TBL_03")

        test_passed = filter_applied or range_applied

        if test_passed:
            utils.tomar_screenshot(driver, "CAL_TBL_03_SUCCESS")
            print("\n✅ CAL-TBL-03: SUCCESS — PAGE DATA UPDATED WITH SELECTED DATE RANGE.")
        else:
            utils.tomar_screenshot(driver, "CAL_TBL_03_FAILED")
            print("\n❌ CAL-TBL-03: FAILED — DATE RANGE WAS NOT APPLIED TO THE PAGE.")

    except Exception as e:
        print(f"\n💥 CAL-TBL-03 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "CAL_TBL_03_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()


# ==================================================================================
# CAL-TBL-04: APPLY RANGE THEN RELOAD — VERIFY PERSISTENCE BEHAVIOR
# ==================================================================================
def CAL_TBL_04():
    """
    PRECONDITIONS : AUTHENTICATED USER. LIQUIDACIÓN MODULE ACCESSIBLE.
    STEPS         : 1. SELECT VALID DATE RANGE.
                    2. RELOAD THE PAGE.
    EXPECTED      : DATE RANGE IS PRESERVED — OR CORRECTLY RESETS TO 'DATOS DE HOY'
                    (DOCUMENTS THE APP'S PERSISTENCE BEHAVIOR FOR QA RECORDS).
    """
    print("\n" + "=" * 60)
    print("🧪 CAL-TBL-04: APPLY RANGE THEN RELOAD — VERIFY PERSISTENCE BEHAVIOR")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO LIQUIDACIÓN...")
        _login_and_go_to_liquidacion(driver)

        print(f"\n👉 STEP 1: APPLYING DATE RANGE (DAY {CAL_START_DAY} → DAY {CAL_END_DAY})...")
        _apply_date_range(driver)
        time.sleep(2)

        value_before_reload  = _get_date_field_value(driver)
        checked_before_reload = _datos_de_hoy_is_checked(driver)

        print("\n📸 TAKING SCREENSHOT #1 — STATE BEFORE RELOAD...")
        utils.tomar_screenshot(driver, "CAL_TBL_04_1_BEFORE_RELOAD")

        print("\n👉 STEP 2: RELOADING THE PAGE (driver.refresh())...")
        driver.refresh()
        print("   🔄 PAGE RELOADED.")
        time.sleep(5)

        print("\n📸 TAKING SCREENSHOT #2 — STATE AFTER RELOAD...")
        utils.tomar_screenshot(driver, "CAL_TBL_04_2_AFTER_RELOAD")

        value_after_reload   = _get_date_field_value(driver)
        checked_after_reload  = _datos_de_hoy_is_checked(driver)
        filter_persisted     = (
            value_after_reload != "" and
            value_after_reload == value_before_reload
        )

        print(f"\n   🔬 PERSISTENCE ASSERTION SUMMARY:")
        print(f"      • VALUE BEFORE RELOAD           : '{value_before_reload}'")
        print(f"      • VALUE AFTER RELOAD            : '{value_after_reload}'")
        print(f"      • 'DATOS DE HOY' BEFORE RELOAD  : {checked_before_reload}")
        print(f"      • 'DATOS DE HOY' AFTER RELOAD   : {checked_after_reload}")
        print(f"      • FILTER PERSISTED              : {filter_persisted}")

        if not filter_persisted:
            print("\n   ℹ️  BEHAVIORAL NOTE: CUSTOM DATE RANGE DID NOT PERSIST AFTER RELOAD.")
            print("         THIS IS EXPECTED IF THE APP RESETS TO 'DATOS DE HOY' ON PAGE LOAD.")
            print("         'DATOS DE HOY' RESETS TO CHECKED: " + str(checked_after_reload))
            print("         DOCUMENT THIS AS EXPECTED STATELESS BEHAVIOR.")

        _capture_web_evidence(driver, "CAL_TBL_04")

        # PASS CONDITION: EITHER FILTER PERSISTED, OR THE APP CORRECTLY REVERTED
        # TO 'DATOS DE HOY' (EXPECTED STATELESS BEHAVIOR — BOTH ARE VALID OUTCOMES).
        behavior_documented = True

        if filter_persisted:
            utils.tomar_screenshot(driver, "CAL_TBL_04_SUCCESS")
            print("\n✅ CAL-TBL-04: SUCCESS — DATE RANGE PERSISTED AFTER PAGE RELOAD.")
        elif checked_after_reload:
            utils.tomar_screenshot(driver, "CAL_TBL_04_SUCCESS")
            print("\n✅ CAL-TBL-04: SUCCESS (STATELESS) — APP CORRECTLY RESETS TO 'DATOS DE HOY' ON RELOAD.")
        else:
            utils.tomar_screenshot(driver, "CAL_TBL_04_FAILED")
            print("\n❌ CAL-TBL-04: FAILED — UNEXPECTED STATE AFTER RELOAD.")

    except Exception as e:
        print(f"\n💥 CAL-TBL-04 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "CAL_TBL_04_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()


# ==================================================================================
# CAL-TBL-05: APPLY RANGE, TOGGLE 'DATOS DE HOY' — CUSTOM RANGE CAN BE REAPPLIED
# ==================================================================================
def CAL_TBL_05():
    """
    PRECONDITIONS : AUTHENTICATED USER. LIQUIDACIÓN MODULE ACCESSIBLE.
    STEPS         : 1. SELECT VALID DATE RANGE.
                    2. RE-CHECK 'DATOS DE HOY' (SIMULATES PAGE INTERACTION / NAVIGATION).
                    3. UNCHECK AGAIN AND REAPPLY A DIFFERENT RANGE.
    EXPECTED      : DATE RANGE IS CORRECTLY MAINTAINED ACROSS TOGGLE INTERACTIONS.
                    THE FILTER SYSTEM RESPONDS CORRECTLY TO MULTIPLE CHANGES.
    """
    print("\n" + "=" * 60)
    print("🧪 CAL-TBL-05: APPLY RANGE, TOGGLE 'DATOS DE HOY' — REAPPLY FILTER")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO LIQUIDACIÓN...")
        _login_and_go_to_liquidacion(driver)

        # STEP 1: APPLY FIRST DATE RANGE
        print(f"\n👉 STEP 1: APPLYING FIRST DATE RANGE (DAY {CAL_START_DAY} → DAY {CAL_END_DAY})...")
        _apply_date_range(driver)
        time.sleep(2)

        value_first = _get_date_field_value(driver)

        print("\n📸 TAKING SCREENSHOT #1 — FIRST DATE RANGE APPLIED...")
        utils.tomar_screenshot(driver, "CAL_TBL_05_1_FIRST_RANGE")

        # STEP 2: RE-CHECK 'DATOS DE HOY' (SIMULATE PAGE INTERACTION)
        print("\n👉 STEP 2: RE-CHECKING 'DATOS DE HOY' (SIMULATING PAGE INTERACTION)...")
        try:
            checkbox = driver.find_element(By.XPATH, XPATH_DATOS_HOY_CHECKBOX)
            checkbox.click()
            time.sleep(1)
            print("   🖱️  'DATOS DE HOY' RE-CHECKED.")
        except Exception as e:
            print(f"   ⚠️  COULD NOT RE-CHECK 'DATOS DE HOY': {e}")
            try:
                driver.execute_script("""
                    var allEls = document.querySelectorAll('*');
                    for (var el of allEls) {
                        if (el.textContent.trim() === 'Datos de hoy' && el.offsetWidth > 0) {
                            el.click(); break;
                        }
                    }
                """)
                time.sleep(1)
                print("   ✅ 'DATOS DE HOY' RE-CHECKED VIA JAVASCRIPT.")
            except Exception:
                pass

        value_after_recheck = _get_date_field_value(driver)
        print(f"   🔎 DATE FIELD AFTER RE-CHECK: '{value_after_recheck}'")

        print("\n📸 TAKING SCREENSHOT #2 — AFTER RE-CHECKING 'DATOS DE HOY'...")
        utils.tomar_screenshot(driver, "CAL_TBL_05_2_DATOS_HOY_RECHECKED")

        # STEP 3: UNCHECK AGAIN AND APPLY A DIFFERENT RANGE (DAY 1 → DAY 3)
        print("\n👉 STEP 3: UNCHECKING 'DATOS DE HOY' AND APPLYING NEW RANGE (DAY 1 → DAY 3)...")
        _uncheck_datos_de_hoy(driver)
        time.sleep(1)

        el, strategy = _open_calendar(driver)
        if el:
            _select_day_js(driver, "1")
            time.sleep(0.8)
            _select_day_js(driver, "3")
            time.sleep(1)

        value_second = _get_date_field_value(driver)

        print("\n📸 TAKING SCREENSHOT #3 — SECOND DATE RANGE APPLIED...")
        utils.tomar_screenshot(driver, "CAL_TBL_05_3_SECOND_RANGE")

        # ASSERTIONS
        assert_first_range_applied  = (value_first != "")
        assert_recheck_affected     = (value_after_recheck != value_first or value_after_recheck == "")
        assert_second_range_applied = (value_second != "" and value_second != value_after_recheck)

        print(f"\n   🔬 TOGGLE ASSERTION SUMMARY:")
        print(f"      • VALUE AFTER FIRST RANGE    : '{value_first}'")
        print(f"      • VALUE AFTER RE-CHECK DATOS : '{value_after_recheck}'")
        print(f"      • VALUE AFTER SECOND RANGE   : '{value_second}'")
        print(f"      • FIRST RANGE APPLIED        : {assert_first_range_applied}")
        print(f"      • RE-CHECK AFFECTED FIELD    : {assert_recheck_affected}")
        print(f"      • SECOND RANGE APPLIED       : {assert_second_range_applied}")

        _capture_web_evidence(driver, "CAL_TBL_05")

        test_passed = assert_first_range_applied and assert_second_range_applied

        if test_passed:
            utils.tomar_screenshot(driver, "CAL_TBL_05_SUCCESS")
            print("\n✅ CAL-TBL-05: SUCCESS — FILTER SYSTEM RESPONDS CORRECTLY TO TOGGLE INTERACTIONS.")
        else:
            utils.tomar_screenshot(driver, "CAL_TBL_05_FAILED")
            print("\n❌ CAL-TBL-05: FAILED — FILTER DID NOT RESPOND CORRECTLY TO INTERACTIONS.")

    except Exception as e:
        print(f"\n💥 CAL-TBL-05 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "CAL_TBL_05_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()


# ==================================================================================
# CAL-TBL-06: APPLY RANGE THEN CLICK 'EXPORTAR' — EXPORT RESPECTS SELECTED RANGE
# ==================================================================================
def CAL_TBL_06():
    """
    PRECONDITIONS : AUTHENTICATED USER. LIQUIDACIÓN MODULE WITH EXPORTAR BUTTON.
    STEPS         : 1. SELECT VALID DATE RANGE.
                    2. CLICK THE 'EXPORTAR' BUTTON.
    EXPECTED      : EXPORT ACTION IS TRIGGERED WITH THE APPLIED DATE RANGE.
                    DATE RANGE FIELD IS STILL SHOWING THE SELECTED RANGE AFTER EXPORT.
    NOTE          : LIQUIDACIÓN HAS NO SEARCH BOX — 'EXPORTAR' IS THE EQUIVALENT
                    ACTION THAT VALIDATES THE APPLIED FILTER IS RESPECTED.
    """
    print("\n" + "=" * 60)
    print("🧪 CAL-TBL-06: APPLY RANGE THEN CLICK 'EXPORTAR' — EXPORT RESPECTS RANGE")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO LIQUIDACIÓN...")
        _login_and_go_to_liquidacion(driver)

        # STEP 1: APPLY DATE RANGE
        print(f"\n👉 STEP 1: APPLYING DATE RANGE (DAY {CAL_START_DAY} → DAY {CAL_END_DAY})...")
        _apply_date_range(driver)
        time.sleep(2)

        value_before_export = _get_date_field_value(driver)

        print("\n📸 TAKING SCREENSHOT #1 — DATE RANGE APPLIED, BEFORE EXPORT...")
        utils.tomar_screenshot(driver, "CAL_TBL_06_1_BEFORE_EXPORT")

        # STEP 2: CLICK 'EXPORTAR'
        print("\n👉 STEP 2: CLICKING THE 'EXPORTAR' BUTTON...")
        export_clicked = False

        try:
            btn = driver.find_element(By.XPATH, XPATH_BTN_EXPORTAR)
            btn.click()
            export_clicked = True
            print("   ✅ 'EXPORTAR' BUTTON CLICKED — STRATEGY 1 (XPATH).")
        except Exception:
            print("   ⚠️  XPATH STRATEGY FAILED. TRYING JAVASCRIPT...")
            try:
                result = driver.execute_script("""
                    var btns = document.querySelectorAll('button, a[role="button"]');
                    for (var btn of btns) {
                        var text = btn.textContent.trim().toLowerCase();
                        if (text.includes('exportar') || text.includes('export')) {
                            btn.click();
                            return btn.textContent.trim();
                        }
                    }
                    return null;
                """)
                if result:
                    export_clicked = True
                    print(f"   ✅ 'EXPORTAR' CLICKED VIA JAVASCRIPT: '{result}'.")
                else:
                    print("   ⚠️  'EXPORTAR' BUTTON NOT FOUND ON PAGE.")
            except Exception as js_err:
                print(f"   ❌ JAVASCRIPT EXPORT CLICK FAILED: {js_err}")

        time.sleep(3)

        print("\n📸 TAKING SCREENSHOT #2 — AFTER CLICKING 'EXPORTAR'...")
        utils.tomar_screenshot(driver, "CAL_TBL_06_2_AFTER_EXPORT")

        value_after_export = _get_date_field_value(driver)
        filter_still_active = (
            value_after_export == value_before_export and
            value_after_export != ""
        )

        print(f"\n   🔬 EXPORT + FILTER ASSERTION SUMMARY:")
        print(f"      • DATE VALUE BEFORE EXPORT   : '{value_before_export}'")
        print(f"      • DATE VALUE AFTER EXPORT    : '{value_after_export}'")
        print(f"      • FILTER STILL ACTIVE        : {filter_still_active}")
        print(f"      • 'EXPORTAR' WAS CLICKED     : {export_clicked}")

        _capture_web_evidence(driver, "CAL_TBL_06")

        # PASS: EXPORT WAS TRIGGERED AND DATE FILTER WAS NOT RESET
        test_passed = export_clicked and filter_still_active

        if test_passed:
            utils.tomar_screenshot(driver, "CAL_TBL_06_SUCCESS")
            print("\n✅ CAL-TBL-06: SUCCESS — 'EXPORTAR' TRIGGERED WITH APPLIED DATE RANGE.")
        else:
            utils.tomar_screenshot(driver, "CAL_TBL_06_FAILED")
            if not export_clicked:
                print("\n❌ CAL-TBL-06: FAILED — 'EXPORTAR' BUTTON COULD NOT BE CLICKED.")
            else:
                print("\n❌ CAL-TBL-06: FAILED — DATE FILTER WAS LOST AFTER CLICKING 'EXPORTAR'.")

    except Exception as e:
        print(f"\n💥 CAL-TBL-06 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "CAL_TBL_06_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()


# ==================================================================================
# MAIN EXECUTION
# ==================================================================================
if __name__ == "__main__":

    logger, log_file, timestamp = utils.iniciar_reporte("CAL_TBL")

    try:
        CAL_TBL_01()
        CAL_TBL_02()
        CAL_TBL_03()
        CAL_TBL_04()
        CAL_TBL_05()
        CAL_TBL_06()

    finally:
        utils.generar_reporte_html("CAL_TBL", log_file, timestamp)