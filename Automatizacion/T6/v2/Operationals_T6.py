"""
FILENAME: Operationals_T6.py
DESCRIPTION:
    AUTOMATED TEST SUITE — PINPAD (PP) MODULE.
    COVERS THE "SERVIDOR PINPAD" SECTION INSIDE AJUSTES OF THE NEW MEMPHIS APP v2
    (com.memphis.app.dev).
    FLOW: Ajustes → PinPad → Servidor PinPad → PinPad screen.

TEST CASES COVERED:
    · PP-01 : AJUSTES SHOWS "PINPAD" SECTION WITH "SERVIDOR PINPAD" STATUS
    · PP-02 : NAVIGATE TO "SERVIDOR PINPAD" AND VERIFY PINPAD SCREEN ELEMENTS
    · PP-03 : TOGGLE "SERVIDOR ACTIVO" OFF / ON
    · PP-04 : "CONFIGURACIÓN" SCREEN LOADS WITH ALL OPTIONS
    · PP-05 : TOGGLE "IMPRESIÓN AUTOMÁTICA" OFF / ON
    · PP-06 : TOGGLE "CANCELACIONES Y DEVOLUCIONES" OFF / ON
    · PP-07 : TOGGLE "COMPARTIR TICKET" OFF / ON
    · PP-08 : "OBTENER INTERNET POR CABLE USB" OPENS ITS SUB-SCREEN
    · PP-09 : "PROTECTOR PINPAD" OPENS PROTECTOR SCREEN AND CAN BE EXITED
    · PP-10 : "COMANDOS RECIBIDOS" SHOWS PINPAD_STARTED (PORT + ADDRESS)
    · PP-11 : "LIMPIAR" CLEARS THE RECEIVED COMMANDS LIST
    · PP-12 : SERVER RESTART REGISTERS A NEW PINPAD_STARTED COMMAND
    · PP-13 : "HORARIOS DE ACTUALIZACIONES" SCREEN LOADS WITH DEFAULT VALUES
    · PP-14 : "HORA DE INICIO" PICKER OPENS — CANCELAR KEEPS THE VALUE
    · PP-15 : "HORA DE FIN" PICKER OPENS — CANCELAR KEEPS THE VALUE
    · PP-16 : CHANGE "HORA DE INICIO" + CONFIRMAR PERSISTS THE NEW VALUE
    · PP-17 : CHANGE "HORA DE FIN" + CANCELAR (SCREEN) DISCARDS THE CHANGE
    · PP-18 : BACK ARROW FROM EVERY PINPAD SUB-SCREEN RETURNS TO PINPAD

REQUIREMENTS:
    - APPIUM SERVER RUNNING.
    - config.py AND utils.py IN THE SAME DIRECTORY.
"""

import sys
import os
import re

# ── PATH SETUP ──────────────────────────────────────────────────
v2_path = os.path.abspath(os.path.dirname(__file__))
t6_path = os.path.abspath(os.path.join(v2_path, '..'))
for p in [v2_path, t6_path]:
    if p not in sys.path:
        sys.path.insert(0, p)
# ────────────────────────────────────────────────────────────────

import time
import config
import utils
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


# REGEX FOR "HH:MM AM/PM" VALUES SHOWN IN "HORARIOS DE ACTUALIZACIONES"
TIME_REGEX = re.compile(r'\d{1,2}:\d{2}\s?[AP]M', re.IGNORECASE)

# REGEX FOR "Escuchando en 192.168.x.x:8080"
LISTEN_REGEX = re.compile(r'(\d{1,3}(?:\.\d{1,3}){3}):(\d+)')

# KEYWORDS OF THE "SERVIDOR PINPAD" ROW ON THE PINPAD SCREEN (ON AND OFF STATES)
SERVER_KEYS = ["Servidor activo", "Servidor inactivo", "Escuchando", "Enciéndelo"]


# ==================================================================================
# HELPER: FULL LOGIN FLOW v2
#         ONBOARDING → LOGIN → CONFIGURA TU COMERCIO → LECTOR POPUP → HOME
# ==================================================================================

def helper_login_to_calculator(driver, wait):

    from selenium.webdriver.support.ui import WebDriverWait as _WDW

    print("   📱 [HELPER] PHASE 1: NAVIGATING ONBOARDING SLIDES...")
    time.sleep(3)

    for slide_num, btn_xpath in enumerate(
        [config.XPATH_OB_BTN_SIGUIENTE,
         config.XPATH_OB_BTN_SIGUIENTE,
         config.XPATH_OB_BTN_COMENZAR], start=1
    ):
        label = "Siguiente" if slide_num < 3 else "Comenzar"
        try:
            utils.click_element(driver, btn_xpath)
            time.sleep(1.5 if slide_num < 3 else 2)
            print(f"   ✅ [HELPER] SLIDE {slide_num} PASSED — '{label}'")
        except Exception as e:
            print(f"   ⚠️  [HELPER] SLIDE {slide_num} SKIP: {e}")
            if slide_num == 1:
                try:
                    utils.click_element(driver, config.XPATH_OB_BTN_SALTAR)
                    time.sleep(1)
                except:
                    pass

    print("   🔐 [HELPER] PHASE 2: EXECUTING LOGIN...")
    utils.type_text(driver, config.XPATH_INPUT_USUARIO, config.USUARIO_VALIDO)
    time.sleep(0.5)
    utils.type_text(driver, config.XPATH_INPUT_PASS, config.PASS_VALIDO)
    time.sleep(0.5)
    try:
        driver.hide_keyboard()
    except:
        pass
    utils.click_element(driver, config.XPATH_LG_BTN_INICIAR)
    time.sleep(4)

    print("   🏪 [HELPER] PHASE 3: CHECKING 'CONFIGURA TU COMERCIO' SCREEN...")
    screen_present = utils.verify_element(
        wait, config.XPATH_CC_SCREEN, "CONFIGURA TU COMERCIO SCREEN"
    )
    if screen_present:
        try:
            utils.type_text(driver, config.XPATH_CC_INPUT_AFILIACION, config.CC_AFILIACION)
            time.sleep(0.5)
            utils.type_text(driver, config.XPATH_CC_INPUT_TOKEN, config.CC_TOKEN)
            time.sleep(0.5)
            try: driver.hide_keyboard()
            except: pass
            utils.click_element(driver, config.XPATH_CC_BTN_CONFIRMAR)
            time.sleep(3)
        except Exception as e:
            print(f"   ⚠️  [HELPER] COMERCIO FORM ERROR: {e}")
    else:
        print("   ℹ️  [HELPER] COMMERCE ALREADY LINKED")

    print("   ⚙️  [HELPER] PHASE 4: CHECKING 'LECTOR NO CONFIGURADO' POPUP...")
    time.sleep(2)
    popup_present = utils.verify_element(
        wait, config.XPATH_LG_POPUP_LECTOR_NC, "LECTOR NO CONFIGURADO POPUP"
    )
    if popup_present:
        try:
            utils.click_element(driver, config.XPATH_LG_BTN_CONFIGURAR_AHORA)
            time.sleep(3)
            _WDW(driver, 8).until(
                lambda d: d.find_element(By.XPATH, config.XPATH_LG_LECTOR_CONFIGURADO)
            )
            utils.click_element(driver, config.XPATH_LG_BTN_ACEPTAR_LECTOR)
            time.sleep(2)
            print("   ✅ [HELPER] LECTOR CONFIGURED — HEADING TO HOME")
        except Exception as e:
            print(f"   ⚠️  [HELPER] LECTOR POPUP HANDLING: {e}")
    else:
        print("   ℹ️  [HELPER] NO POPUP — HEADING TO HOME")
        time.sleep(2)


# ==================================================================================
# INTERNAL HELPER — GENERIC ELEMENT UTILITIES
# ==================================================================================

def _is_visible(driver, xpath):
    """RETURNS True IF THE FIRST ELEMENT MATCHING xpath IS DISPLAYED."""
    try:
        return driver.find_element(By.XPATH, xpath).is_displayed()
    except:
        return False


def _element_label(el):
    """RETURNS THE VISIBLE LABEL OF AN ELEMENT (text OR content-desc)."""
    try:
        return (el.get_attribute("text") or "") + " " + (el.get_attribute("content-desc") or "")
    except:
        return ""


def _click_first(driver, xpaths, label, keyword=None, pause=2):
    """
    TRIES EACH XPATH IN ORDER AND CLICKS THE FIRST MATCH.
    IF keyword IS GIVEN, FALLS BACK TO UIAUTOMATOR scrollIntoView + click.
    """
    for xpath in xpaths:
        try:
            driver.find_element(By.XPATH, xpath).click()
            time.sleep(pause)
            print(f"   ✅ '{label}' CLICKED")
            return True
        except:
            pass

    if keyword:
        for selector in [
            f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView('
            f'new UiSelector().descriptionContains("{keyword}"))',
            f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView('
            f'new UiSelector().textContains("{keyword}"))',
            f'new UiSelector().descriptionContains("{keyword}")',
            f'new UiSelector().textContains("{keyword}")',
        ]:
            try:
                driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, selector).click()
                time.sleep(pause)
                print(f"   ✅ '{label}' CLICKED VIA UIAUTOMATOR")
                return True
            except:
                pass

    print(f"   ❌ '{label}' — ALL STRATEGIES FAILED")
    return False


def _click_back_arrow(driver):
    """
    CLICKS THE TOP-LEFT BACK ARROW (←) OF THE CURRENT SCREEN.
    FALLS BACK TO THE ANDROID SYSTEM BACK KEY.
    """
    try:
        btns = driver.find_elements(By.XPATH, "//android.widget.Button")
        if btns:
            loc  = btns[0].location
            size = driver.get_window_size()
            if loc['y'] < size['height'] * 0.20 and loc['x'] < size['width'] * 0.25:
                btns[0].click()
                time.sleep(2)
                print("   ✅ [NAV] BACK ARROW CLICKED (android.widget.Button[0])")
                return True, "android.widget.Button[0]"
    except:
        pass

    try:
        driver.back()
        time.sleep(2)
        print("   ✅ [NAV] ANDROID SYSTEM BACK KEY")
        return True, "Android BACK key"
    except Exception as e:
        return False, f"ALL STRATEGIES FAILED: {e}"


def _dump_screen(driver, limit=40):
    """PRINTS VISIBLE text/content-desc VALUES FOR DIAGNOSIS."""
    try:
        count = 0
        for elem in driver.find_elements(By.XPATH, "//*"):
            try:
                d = (elem.get_attribute("content-desc") or "")[:80].replace("\n", " | ")
                t = (elem.get_attribute("text") or "")[:40]
                if (d and d != "null" and len(d) > 1) or (t and len(t) > 1):
                    print(f"      📝 desc='{d}' | text='{t}'")
                    count += 1
                    if count >= limit:
                        break
            except:
                continue
    except:
        pass


# ==================================================================================
# INTERNAL HELPER — TOGGLE (SWITCH) UTILITIES
# ==================================================================================

def _find_toggle(driver, keywords, fallback_index=None):
    """
    LOCATES THE SWITCH THAT BELONGS TO A ROW IDENTIFIED BY ANY OF THE keywords.
    FLUTTER MAY EXPOSE THE ROW ITSELF AS CHECKABLE OR A CHILD/SIBLING SWITCH,
    SO SEVERAL STRATEGIES ARE ATTEMPTED.
    """
    for kw in keywords:
        for xpath in [
            f'//*[@checkable="true" and (contains(@content-desc,"{kw}") or contains(@text,"{kw}"))]',
            f'//*[contains(@content-desc,"{kw}") or contains(@text,"{kw}")]//*[@checkable="true"]',
            f'//*[contains(@content-desc,"{kw}") or contains(@text,"{kw}")]'
            f'/following-sibling::*[@checkable="true"][1]',
            f'//*[contains(@content-desc,"{kw}") or contains(@text,"{kw}")]'
            f'/..//*[@checkable="true"]',
        ]:
            try:
                return driver.find_element(By.XPATH, xpath)
            except:
                continue

    if fallback_index is not None:
        try:
            switches = driver.find_elements(
                By.XPATH, '//android.widget.Switch | //*[@checkable="true"]'
            )
            if len(switches) > fallback_index:
                print(f"   ℹ️  TOGGLE LOCATED BY INDEX FALLBACK [{fallback_index}]")
                return switches[fallback_index]
        except:
            pass
    return None


def _get_toggle_state(driver, keywords, fallback_index=None):
    """RETURNS True (ON), False (OFF) OR None (NOT FOUND)."""
    el = _find_toggle(driver, keywords, fallback_index)
    if el is None:
        return None
    try:
        return (el.get_attribute("checked") or "").lower() == "true"
    except:
        return None


def _tap_toggle(driver, keywords, fallback_index=None):
    el = _find_toggle(driver, keywords, fallback_index)
    if el is None:
        # FALLBACK: TAPPING THE WHOLE ROW ALSO FLIPS A FLUTTER SWITCH TILE
        for kw in keywords:
            try:
                driver.find_element(
                    By.XPATH, f'//*[contains(@content-desc,"{kw}") or contains(@text,"{kw}")]'
                ).click()
                time.sleep(2)
                print(f"   ℹ️  TOGGLE TAPPED VIA ROW '{kw}'")
                return True
            except:
                continue
        print("   ❌ TOGGLE NOT FOUND")
        return False
    try:
        el.click()
        time.sleep(2)
        return True
    except Exception as e:
        print(f"   ❌ TOGGLE CLICK FAILED: {e}")
        return False


def _state_label(state):
    return "ON" if state else ("OFF" if state is False else "UNKNOWN")


def _server_state(driver):
    """
    READS THE PINPAD SERVER STATE FROM THE SCREEN TEXT (MORE RELIABLE THAN THE SWITCH):
    "Servidor activo" / "Escuchando en" → ON | "Servidor inactivo" → OFF.
    FALLS BACK TO THE SWITCH "checked" ATTRIBUTE.
    """
    if _is_visible(driver, config.XPATH_PP_SERVIDOR_ACTIVO) or _is_visible(driver, config.XPATH_PP_ESCUCHANDO):
        return True
    if _is_visible(driver, config.XPATH_PP_SERVIDOR_INACTIVO):
        return False
    return _get_toggle_state(driver, SERVER_KEYS, 0)


def _set_server(driver, on, timeout=12):
    """TURNS THE PINPAD SERVER ON/OFF AND WAITS UNTIL THE SCREEN REFLECTS IT."""
    if _server_state(driver) == on:
        return True
    _tap_toggle(driver, SERVER_KEYS, 0)
    end = time.time() + timeout
    while time.time() < end:
        if _server_state(driver) == on:
            time.sleep(1)  # LET THE OPTIONS LIST RENDER
            return True
        time.sleep(1)
    print(f"   ❌ SERVER DID NOT TURN {'ON' if on else 'OFF'} IN {timeout}s")
    return False


# ==================================================================================
# INTERNAL HELPER — NAVIGATION
# ==================================================================================

def _navigate_to_settings(driver, wait):
    print("\n   📍 [NAV] NAVIGATING TO SETTINGS TAB...")
    # WAIT FOR THE BOTTOM NAV — LOGIN CAN TAKE A FEW EXTRA SECONDS ON THE T6
    try:
        WebDriverWait(driver, 15).until(
            lambda d: d.find_element(By.XPATH, '//*[@content-desc="Ajustes"]')
        )
    except TimeoutException:
        print("   ⚠️  [NAV] BOTTOM NAV NOT VISIBLE AFTER 15s — TRYING ANYWAY")
    for xpath in [
        '//android.widget.ImageView[@content-desc="Ajustes"]',
        '//android.view.View[@content-desc="Ajustes"]',
        '//*[@content-desc="Ajustes"]',
        config.XPATH_AJ_TAB_SETTINGS,
        config.XPATH_PÑ_TAB_AJUSTES,
        '//*[contains(@content-desc,"Ajustes")]',
    ]:
        try:
            driver.find_element(By.XPATH, xpath).click()
            time.sleep(2)
            print("   ✅ [NAV] SETTINGS TAB REACHED")
            return True
        except:
            pass

    for selector in [
        'new UiSelector().description("Ajustes")',
        'new UiSelector().descriptionContains("Ajustes")',
        'new UiSelector().textContains("Ajustes")',
    ]:
        try:
            driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, selector).click()
            time.sleep(2)
            print(f"   ✅ [NAV] SETTINGS TAB VIA UIAUTOMATOR: {selector[:40]}")
            return True
        except:
            pass

    print("   ❌ [NAV] SETTINGS TAB FAILED — ALL STRATEGIES EXHAUSTED")
    return False


def _scroll_to_pinpad_section(driver):
    """SCROLLS THE AJUSTES LIST UNTIL "SERVIDOR PINPAD" IS VISIBLE."""
    for selector in [
        'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView('
        'new UiSelector().descriptionContains("Servidor PinPad"))',
        'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView('
        'new UiSelector().textContains("Servidor PinPad"))',
    ]:
        try:
            driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, selector)
            time.sleep(1)
            print("   ✅ [NAV] SCROLLED TO 'Servidor PinPad'")
            return True
        except:
            pass

    # FALLBACK: MANUAL SWIPE UP (MAX 3 ATTEMPTS)
    size = driver.get_window_size()
    x = int(size['width'] * 0.5)
    for _ in range(3):
        if _is_visible(driver, config.XPATH_PP_BTN_SERVIDOR_PINPAD):
            print("   ✅ [NAV] 'Servidor PinPad' VISIBLE")
            return True
        driver.swipe(x, int(size['height'] * 0.75), x, int(size['height'] * 0.35), 600)
        time.sleep(1)
    return _is_visible(driver, config.XPATH_PP_BTN_SERVIDOR_PINPAD)


def _is_on_pinpad_screen(driver):
    # "Servidor activo/inactivo" ONLY EXIST ON THE PINPAD SCREEN (NOT ON AJUSTES)
    for xpath in [
        config.XPATH_PP_SERVIDOR_ACTIVO,
        config.XPATH_PP_SERVIDOR_INACTIVO,
        config.XPATH_PP_ESCUCHANDO,
        config.XPATH_PP_BTN_PROTECTOR,
        config.XPATH_PP_BTN_HORARIOS,
    ]:
        if _is_visible(driver, xpath):
            return True
    return False


def _navigate_to_pinpad(driver, wait):
    """AJUSTES → SCROLL → "SERVIDOR PINPAD" → PINPAD SCREEN."""
    if not _navigate_to_settings(driver, wait):
        return False
    _scroll_to_pinpad_section(driver)

    print("   📍 [NAV] OPENING 'Servidor PinPad'...")
    if not _click_first(
        driver,
        [config.XPATH_PP_BTN_SERVIDOR_PINPAD, config.XPATH_PP_STATUS_RECIBIENDO],
        "Servidor PinPad", keyword="Servidor PinPad",
    ):
        return False

    if _is_on_pinpad_screen(driver):
        print("   ✅ [NAV] PINPAD SCREEN REACHED")
        return True
    print("   ❌ [NAV] PINPAD SCREEN NOT DETECTED")
    _dump_screen(driver)
    return False


def _open_pinpad_option(driver, xpath, label):
    """CLICKS ONE OF THE OPTIONS LISTED IN THE PINPAD SCREEN."""
    print(f"\n   📍 [NAV] OPENING '{label}'...")
    return _click_first(driver, [xpath], label, keyword=label)


def _setup_until_pinpad(driver, wait, test_id, server_on=True):
    """
    PRECONDITION SHARED BY EVERY CASE: LOGIN + NAVIGATE TO PINPAD SCREEN.
    AFTER A FRESH INSTALL THE SERVER IS OFF AND THE OPTIONS ARE HIDDEN,
    SO BY DEFAULT THE SERVER IS TURNED ON TO EXPOSE THEM.
    """
    print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN FLOW...")
    helper_login_to_calculator(driver, wait)
    tag = test_id.replace('-', '')
    if not _navigate_to_pinpad(driver, wait):
        print(f"\n💥 {test_id} FAILED — COULD NOT REACH PINPAD SCREEN")
        utils.take_screenshot(driver, f"{tag}_NAV_FAILED", "t6")
        return False

    print(f"   ℹ️  SERVER STATE ON ARRIVAL: {_state_label(_server_state(driver))}")
    if server_on and not _set_server(driver, True):
        print(f"\n💥 {test_id} FAILED — COULD NOT TURN THE PINPAD SERVER ON")
        utils.take_screenshot(driver, f"{tag}_SERVER_ON_FAILED", "t6")
        _dump_screen(driver)
        return False
    if server_on:
        print("   ✅ PINPAD SERVER ON — OPTIONS AVAILABLE")
    return True


# ==================================================================================
# INTERNAL HELPER — HORARIOS DE ACTUALIZACIONES
# ==================================================================================

def _read_time_value(driver, row_xpath):
    """
    READS THE "HH:MM AM/PM" VALUE DISPLAYED UNDER A ROW (HORA DE INICIO / HORA DE FIN).
    THE VALUE MAY BE MERGED INTO THE ROW content-desc OR LIVE IN A SIBLING NODE.
    """
    try:
        row = driver.find_element(By.XPATH, row_xpath)
        match = TIME_REGEX.search(_element_label(row))
        if match:
            return match.group(0).upper()
        # SIBLING / PARENT LOOKUP
        for rel in ['./following-sibling::*[1]', './..']:
            try:
                match = TIME_REGEX.search(_element_label(row.find_element(By.XPATH, rel)))
                if match:
                    return match.group(0).upper()
            except:
                continue
    except:
        pass
    return None


def _open_time_picker(driver, row_xpath, label):
    if not _click_first(driver, [row_xpath], label, keyword=label):
        return False
    try:
        WebDriverWait(driver, 5).until(
            lambda d: d.find_element(By.XPATH, config.XPATH_PP_PICKER_SHEET)
        )
        print(f"   ✅ PICKER '{label}' OPENED")
        return True
    except TimeoutException:
        print(f"   ❌ PICKER '{label}' DID NOT OPEN")
        return False


def _click_sheet_button(driver, xpath, label):
    """
    CLICKS A BOTTOM-SHEET BUTTON. THE SHEET AND THE SCREEN BOTH HAVE
    "CONFIRMAR" / "CANCELAR", SO THE LAST MATCH (TOP-MOST LAYER) IS USED.
    """
    try:
        elems = driver.find_elements(By.XPATH, xpath)
        if elems:
            elems[-1].click()
            time.sleep(2)
            print(f"   ✅ SHEET '{label}' CLICKED")
            return True
    except Exception as e:
        print(f"   ❌ SHEET '{label}' FAILED: {e}")
    return False


def _scroll_hour_wheel(driver, current_hour, steps=1):
    """
    MOVES THE HOUR WHEEL OF THE PICKER BY `steps` POSITIONS.
    POSITIVE = NEXT HOUR (SWIPE UP), NEGATIVE = PREVIOUS HOUR (SWIPE DOWN).
    ITEM HEIGHT IS MEASURED FROM THE SELECTED HOUR AND ITS NEIGHBOUR WHEN POSSIBLE.
    """
    size = driver.get_window_size()
    selected = None
    for xpath in [
        f'//*[@text="{current_hour}" or @content-desc="{current_hour}"]',
        f'//*[contains(@content-desc,"{current_hour}")]',
    ]:
        try:
            # THE SELECTED HOUR IS THE LEFT-MOST MATCH INSIDE THE BOTTOM SHEET
            candidates = [
                e for e in driver.find_elements(By.XPATH, xpath)
                if e.location['y'] > size['height'] * 0.55
            ]
            if candidates:
                selected = min(candidates, key=lambda e: e.location['x'])
                break
        except:
            continue

    if selected is not None:
        loc, dim = selected.location, selected.size
        x = loc['x'] + dim['width'] // 2
        y = loc['y'] + dim['height'] // 2
        item_h = max(dim['height'], int(size['height'] * 0.025))
    else:
        print("   ⚠️  SELECTED HOUR NOT LOCATED — USING RELATIVE COORDINATES")
        x = int(size['width'] * 0.20)
        y = int(size['height'] * 0.74)
        item_h = int(size['height'] * 0.025)

    for _ in range(abs(steps)):
        end_y = y - item_h if steps > 0 else y + item_h
        driver.swipe(x, y, x, end_y, 700)
        time.sleep(1)
    print(f"   ✅ HOUR WHEEL MOVED {steps:+d} POSITION(S) (x={x}, y={y}, item_h={item_h})")


def _hour_of(value):
    """'02:00 AM' → '02'"""
    return value.split(":")[0].zfill(2) if value else "12"


# ==================================================================================
# PP-01: AJUSTES SHOWS "PINPAD" SECTION WITH "SERVIDOR PINPAD" STATUS
# ==================================================================================

def PP_01():
    print("\n" + "=" * 60)
    print("PP-01: AJUSTES SHOWS 'PINPAD' SECTION WITH SERVER STATUS")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN FLOW...")
        helper_login_to_calculator(driver, wait)

        # ── STEP 1: GO TO AJUSTES ────────────────────────────────────────────
        print("\n👉 STEP 1: CLICKING 'Ajustes' TAB...")
        if not _navigate_to_settings(driver, wait):
            utils.take_screenshot(driver, "PP01_01_NAV_FAILED", "t6")
            return False

        # ── STEP 2: SCROLL TO PINPAD SECTION ─────────────────────────────────
        print("\n👉 STEP 2: SCROLLING TO 'PinPad' SECTION...")
        _scroll_to_pinpad_section(driver)
        utils.take_screenshot(driver, "PP01_02_PINPAD_SECTION", "t6")

        # ── STEP 3: VERIFY SECTION ELEMENTS ──────────────────────────────────
        print("\n👉 STEP 3: VERIFYING SECTION ELEMENTS...")
        # STATUS DEPENDS ON THE SERVER: ON → "Recibiendo comandos..." | OFF → "Enciéndelo para..."
        status_on  = _is_visible(driver, config.XPATH_PP_STATUS_RECIBIENDO)
        status_off = _is_visible(driver, config.XPATH_PP_STATUS_ENCIENDELO)
        checks = {
            "SECTION 'PinPad'"     : _is_visible(driver, config.XPATH_PP_SECTION_PINPAD),
            "ROW 'Servidor PinPad'": _is_visible(driver, config.XPATH_PP_BTN_SERVIDOR_PINPAD),
            "SERVER STATUS TEXT"   : status_on or status_off,
        }
        for label, ok in checks.items():
            print(f"   {'✅' if ok else '❌'} {label}")
        print(f"   ℹ️  STATUS: {'ON — Recibiendo comandos' if status_on else 'OFF — Enciéndelo para recibir comandos' if status_off else 'UNKNOWN'}")

        if all(checks.values()):
            result = "SUCCESS"
            print("\n✅ PP-01 RESULT: SUCCESS — PINPAD SECTION VISIBLE WITH SERVER STATUS")
        else:
            print(f"\n❌ PP-01 RESULT: FAIL — {checks}")
            _dump_screen(driver)

    except Exception as e:
        print(f"\n💥 PP-01 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "PP01_CRITICAL_ERROR", "t6")
        except: pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 PP-01 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# PP-02: NAVIGATE TO "SERVIDOR PINPAD" AND VERIFY PINPAD SCREEN ELEMENTS
# ==================================================================================

def PP_02():
    print("\n" + "=" * 60)
    print("PP-02: PINPAD SCREEN LOADS WITH ALL ELEMENTS")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    options = {
        "Configuración"              : config.XPATH_PP_BTN_CONFIGURACION,
        "Protector PinPad"           : config.XPATH_PP_BTN_PROTECTOR,
        "Comandos recibidos"         : config.XPATH_PP_BTN_COMANDOS,
        "Horarios de actualizaciones": config.XPATH_PP_BTN_HORARIOS,
    }

    try:
        if not _setup_until_pinpad(driver, wait, "PP-02", server_on=False):
            return False

        # ── STEP 1: SERVER OFF — ONLY THE SERVER ROW, NO OPTIONS ─────────────
        print("\n👉 STEP 1: VERIFYING SCREEN WITH SERVER OFF...")
        _set_server(driver, False)
        utils.take_screenshot(driver, "PP02_01_SERVER_OFF", "t6")
        off_label = _is_visible(driver, config.XPATH_PP_SERVIDOR_INACTIVO)
        off_hidden = not any(_is_visible(driver, x) for x in options.values())
        print(f"   {'✅' if off_label else '❌'} 'Servidor inactivo'")
        print(f"   {'✅' if off_hidden else '❌'} OPTIONS HIDDEN WHILE SERVER IS OFF")

        # ── STEP 2: TURN SERVER ON ───────────────────────────────────────────
        print("\n👉 STEP 2: TURNING SERVER ON...")
        _set_server(driver, True)
        utils.take_screenshot(driver, "PP02_02_SERVER_ON", "t6")

        print("\n👉 STEP 3: VERIFYING 'Servidor activo' ROW...")
        server_ok = _is_visible(driver, config.XPATH_PP_SERVIDOR_ACTIVO)
        print(f"   {'✅' if server_ok else '❌'} 'Servidor activo'")

        listen_ok = False
        try:
            text = _element_label(driver.find_element(By.XPATH, config.XPATH_PP_ESCUCHANDO))
            match = LISTEN_REGEX.search(text)
            if match:
                ip, port = match.groups()
                print(f"   ✅ LISTENING ON {ip}:{port}")
                listen_ok = port == config.PP_EXPECTED_PORT
                if not listen_ok:
                    print(f"   ❌ UNEXPECTED PORT — EXPECTED {config.PP_EXPECTED_PORT}")
            else:
                print(f"   ❌ 'Escuchando en' WITHOUT IP:PORT — '{text.strip()}'")
        except:
            print("   ❌ 'Escuchando en' NOT FOUND")

        # ── STEP 4: VERIFY OPTIONS ───────────────────────────────────────────
        print("\n👉 STEP 4: VERIFYING PINPAD OPTIONS...")
        missing = []
        for label, xpath in options.items():
            ok = _is_visible(driver, xpath)
            print(f"   {'✅' if ok else '❌'} {label}")
            if not ok:
                missing.append(label)
        if missing:
            _dump_screen(driver)

        if off_label and off_hidden and server_ok and listen_ok and not missing:
            result = "SUCCESS"
            print("\n✅ PP-02 RESULT: SUCCESS — PINPAD SCREEN CORRECT IN BOTH SERVER STATES")
        else:
            print(f"\n❌ PP-02 RESULT: FAIL — off_label={off_label} | off_hidden={off_hidden} | "
                  f"server_on={server_ok} | listen={listen_ok} | missing={missing}")

    except Exception as e:
        print(f"\n💥 PP-02 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "PP02_CRITICAL_ERROR", "t6")
        except: pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 PP-02 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# PP-03: TOGGLE "SERVIDOR ACTIVO" OFF / ON
# ==================================================================================

def PP_03():
    print("\n" + "=" * 60)
    print("PP-03: TOGGLE 'SERVIDOR ACTIVO' OFF / ON")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"
    initial = None

    try:
        if not _setup_until_pinpad(driver, wait, "PP-03"):
            return False

        initial = _server_state(driver)
        print(f"\n   ℹ️  INITIAL STATE: {_state_label(initial)}")
        utils.take_screenshot(driver, "PP03_01_INITIAL", "t6")

        # ── STEP 1: TURN SERVER OFF ──────────────────────────────────────────
        print("\n👉 STEP 1: TURNING SERVER OFF...")
        _set_server(driver, False)
        off_state   = _server_state(driver)
        listen_gone = not _is_visible(driver, config.XPATH_PP_ESCUCHANDO)
        print(f"   ℹ️  STATE AFTER TAP: {_state_label(off_state)} | 'Escuchando en' HIDDEN: {listen_gone}")
        utils.take_screenshot(driver, "PP03_02_SERVER_OFF", "t6")

        # ── STEP 2: TURN SERVER BACK ON ──────────────────────────────────────
        print("\n👉 STEP 2: TURNING SERVER ON AGAIN...")
        _set_server(driver, True)
        on_state      = _server_state(driver)
        listen_back   = _is_visible(driver, config.XPATH_PP_ESCUCHANDO)
        print(f"   ℹ️  STATE AFTER TAP: {_state_label(on_state)} | 'Escuchando en' VISIBLE: {listen_back}")
        utils.take_screenshot(driver, "PP03_03_SERVER_ON", "t6")

        if off_state is False and on_state is True and listen_back:
            result = "SUCCESS"
            print("\n✅ PP-03 RESULT: SUCCESS — SERVER TOGGLES OFF AND ON CORRECTLY")
        else:
            print(f"\n❌ PP-03 RESULT: FAIL — off={_state_label(off_state)} | "
                  f"on={_state_label(on_state)} | listening={listen_back}")

    except Exception as e:
        print(f"\n💥 PP-03 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "PP03_CRITICAL_ERROR", "t6")
        except: pass
    finally:
        # POSTCONDITION: LEAVE THE SERVER ACTIVE
        try:
            if _server_state(driver) is False:
                print("\n🔧 POSTCONDITION: RESTORING SERVER TO ON...")
                _set_server(driver, True)
        except:
            pass
        print("\n" + "-" * 60)
        print(f"📊 PP-03 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# PP-04: "CONFIGURACIÓN" SCREEN LOADS WITH ALL OPTIONS
# ==================================================================================

def PP_04():
    print("\n" + "=" * 60)
    print("PP-04: 'CONFIGURACIÓN' SCREEN LOADS WITH ALL OPTIONS")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        if not _setup_until_pinpad(driver, wait, "PP-04"):
            return False

        # ── STEP 1: OPEN CONFIGURACIÓN ───────────────────────────────────────
        print("\n👉 STEP 1: OPENING 'Configuración'...")
        if not _open_pinpad_option(driver, config.XPATH_PP_BTN_CONFIGURACION, "Configuración"):
            utils.take_screenshot(driver, "PP04_01_CLICK_FAILED", "t6")
            return False
        utils.take_screenshot(driver, "PP04_01_CONFIGURACION", "t6")

        # ── STEP 2: VERIFY OPTIONS AND TOGGLES ───────────────────────────────
        print("\n👉 STEP 2: VERIFYING OPTIONS...")
        rows = {
            "Impresión automática"          : config.XPATH_PP_CFG_IMPRESION,
            "Cancelaciones y devoluciones"  : config.XPATH_PP_CFG_CANCELACIONES,
            "Compartir ticket"              : config.XPATH_PP_CFG_COMPARTIR,
            "Obtener internet por cable USB": config.XPATH_PP_CFG_INTERNET_USB,
        }
        missing = []
        for label, xpath in rows.items():
            ok = _is_visible(driver, xpath)
            print(f"   {'✅' if ok else '❌'} {label}")
            if not ok:
                missing.append(label)

        for idx, label in enumerate(["Impresión automática", "Cancelaciones y devoluciones",
                                     "Compartir ticket"]):
            state = _get_toggle_state(driver, [label], idx)
            print(f"   ℹ️  TOGGLE '{label}': {_state_label(state)}")

        if not missing:
            result = "SUCCESS"
            print("\n✅ PP-04 RESULT: SUCCESS — CONFIGURACIÓN SCREEN COMPLETE")
        else:
            print(f"\n❌ PP-04 RESULT: FAIL — missing={missing}")
            _dump_screen(driver)

    except Exception as e:
        print(f"\n💥 PP-04 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "PP04_CRITICAL_ERROR", "t6")
        except: pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 PP-04 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# PP-05 / PP-06 / PP-07: CONFIGURACIÓN TOGGLES (SHARED FLOW)
# ==================================================================================

def _run_config_toggle_case(test_id, label, fallback_index):
    """
    SHARED FLOW FOR THE CONFIGURACIÓN TOGGLES:
      1. OPEN CONFIGURACIÓN
      2. READ INITIAL STATE
      3. TAP → STATE MUST INVERT
      4. TAP AGAIN → STATE MUST RETURN TO INITIAL
      5. LEAVE AND RE-ENTER → STATE MUST PERSIST
    """
    tag = test_id.replace("-", "")
    print("\n" + "=" * 60)
    print(f"{test_id}: TOGGLE '{label.upper()}' OFF / ON")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"
    initial = None

    try:
        if not _setup_until_pinpad(driver, wait, test_id):
            return False

        print("\n👉 STEP 1: OPENING 'Configuración'...")
        if not _open_pinpad_option(driver, config.XPATH_PP_BTN_CONFIGURACION, "Configuración"):
            utils.take_screenshot(driver, f"{tag}_01_CLICK_FAILED", "t6")
            return False

        initial = _get_toggle_state(driver, [label], fallback_index)
        print(f"   ℹ️  INITIAL STATE '{label}': {_state_label(initial)}")
        utils.take_screenshot(driver, f"{tag}_01_INITIAL", "t6")
        if initial is None:
            print(f"\n❌ {test_id} RESULT: FAIL — TOGGLE NOT FOUND")
            _dump_screen(driver)
            return False

        # ── STEP 2: FIRST TAP — STATE MUST INVERT ────────────────────────────
        print(f"\n👉 STEP 2: TAPPING '{label}' (EXPECTED {_state_label(not initial)})...")
        _tap_toggle(driver, [label], fallback_index)
        after_first = _get_toggle_state(driver, [label], fallback_index)
        print(f"   {'✅' if after_first == (not initial) else '❌'} STATE: {_state_label(after_first)}")
        utils.take_screenshot(driver, f"{tag}_02_TOGGLED", "t6")

        # ── STEP 3: SECOND TAP — STATE MUST RETURN ───────────────────────────
        print(f"\n👉 STEP 3: TAPPING '{label}' AGAIN (EXPECTED {_state_label(initial)})...")
        _tap_toggle(driver, [label], fallback_index)
        after_second = _get_toggle_state(driver, [label], fallback_index)
        print(f"   {'✅' if after_second == initial else '❌'} STATE: {_state_label(after_second)}")
        utils.take_screenshot(driver, f"{tag}_03_RESTORED", "t6")

        # ── STEP 4: PERSISTENCE — LEAVE AND RE-ENTER ─────────────────────────
        print("\n👉 STEP 4: VERIFYING PERSISTENCE (BACK → RE-ENTER)...")
        _click_back_arrow(driver)
        _open_pinpad_option(driver, config.XPATH_PP_BTN_CONFIGURACION, "Configuración")
        persisted = _get_toggle_state(driver, [label], fallback_index)
        print(f"   {'✅' if persisted == initial else '❌'} STATE AFTER RE-ENTER: {_state_label(persisted)}")
        utils.take_screenshot(driver, f"{tag}_04_PERSISTED", "t6")

        if after_first == (not initial) and after_second == initial and persisted == initial:
            result = "SUCCESS"
            print(f"\n✅ {test_id} RESULT: SUCCESS — '{label}' TOGGLES AND PERSISTS CORRECTLY")
        else:
            print(f"\n❌ {test_id} RESULT: FAIL — initial={_state_label(initial)} | "
                  f"first={_state_label(after_first)} | second={_state_label(after_second)} | "
                  f"persisted={_state_label(persisted)}")

    except Exception as e:
        print(f"\n💥 {test_id} CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, f"{tag}_CRITICAL_ERROR", "t6")
        except: pass
    finally:
        # POSTCONDITION: LEAVE THE TOGGLE IN ITS ORIGINAL STATE
        try:
            if initial is not None:
                current = _get_toggle_state(driver, [label], fallback_index)
                if current is not None and current != initial:
                    print(f"\n🔧 POSTCONDITION: RESTORING '{label}' TO {_state_label(initial)}...")
                    _tap_toggle(driver, [label], fallback_index)
        except:
            pass
        print("\n" + "-" * 60)
        print(f"📊 {test_id} RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


def PP_05():
    _run_config_toggle_case("PP-05", "Impresión automática", 0)


def PP_06():
    _run_config_toggle_case("PP-06", "Cancelaciones y devoluciones", 1)


def PP_07():
    _run_config_toggle_case("PP-07", "Compartir ticket", 2)


# ==================================================================================
# PP-08: "OBTENER INTERNET POR CABLE USB" OPENS ITS SUB-SCREEN
# ==================================================================================

def PP_08():
    print("\n" + "=" * 60)
    print("PP-08: 'OBTENER INTERNET POR CABLE USB' OPENS SUB-SCREEN")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        if not _setup_until_pinpad(driver, wait, "PP-08"):
            return False

        print("\n👉 STEP 1: OPENING 'Configuración'...")
        if not _open_pinpad_option(driver, config.XPATH_PP_BTN_CONFIGURACION, "Configuración"):
            utils.take_screenshot(driver, "PP08_01_CLICK_FAILED", "t6")
            return False

        # ── STEP 2: OPEN USB OPTION ──────────────────────────────────────────
        print("\n👉 STEP 2: CLICKING 'Obtener internet por cable USB'...")
        if not _click_first(driver, [config.XPATH_PP_CFG_INTERNET_USB],
                            "Obtener internet por cable USB", keyword="cable USB"):
            utils.take_screenshot(driver, "PP08_02_CLICK_FAILED", "t6")
            return False
        utils.take_screenshot(driver, "PP08_02_USB_SCREEN", "t6")

        # ── STEP 3: VERIFY WE LEFT CONFIGURACIÓN ─────────────────────────────
        print("\n👉 STEP 3: VERIFYING SUB-SCREEN OPENED...")
        still_on_config = _is_visible(driver, config.XPATH_PP_CFG_IMPRESION)
        print("   📝 SUB-SCREEN CONTENT:")
        _dump_screen(driver, limit=15)

        # ── STEP 4: BACK RETURNS TO CONFIGURACIÓN ────────────────────────────
        print("\n👉 STEP 4: GOING BACK...")
        _click_back_arrow(driver)
        back_ok = _is_visible(driver, config.XPATH_PP_CFG_IMPRESION)
        print(f"   {'✅' if back_ok else '❌'} BACK ON 'Configuración'")
        utils.take_screenshot(driver, "PP08_03_BACK", "t6")

        if not still_on_config and back_ok:
            result = "SUCCESS"
            print("\n✅ PP-08 RESULT: SUCCESS — USB SUB-SCREEN OPENS AND RETURNS")
        else:
            print(f"\n❌ PP-08 RESULT: FAIL — opened={not still_on_config} | back={back_ok}")

    except Exception as e:
        print(f"\n💥 PP-08 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "PP08_CRITICAL_ERROR", "t6")
        except: pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 PP-08 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# PP-09: "PROTECTOR PINPAD" OPENS PROTECTOR SCREEN AND CAN BE EXITED
# ==================================================================================

def PP_09():
    print("\n" + "=" * 60)
    print("PP-09: 'PROTECTOR PINPAD' SCREEN")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        if not _setup_until_pinpad(driver, wait, "PP-09"):
            return False

        # ── STEP 1: OPEN PROTECTOR ───────────────────────────────────────────
        print("\n👉 STEP 1: OPENING 'Protector PinPad'...")
        if not _open_pinpad_option(driver, config.XPATH_PP_BTN_PROTECTOR, "Protector PinPad"):
            utils.take_screenshot(driver, "PP09_01_CLICK_FAILED", "t6")
            return False
        time.sleep(2)
        utils.take_screenshot(driver, "PP09_01_PROTECTOR_SCREEN", "t6")

        # ── STEP 2: VERIFY PROTECTOR (FULL-SCREEN LOGO, NO MENU) ─────────────
        print("\n👉 STEP 2: VERIFYING PROTECTOR SCREEN IS DISPLAYED...")
        menu_hidden = not _is_on_pinpad_screen(driver)
        tabs_hidden = not _is_visible(driver, '//*[@content-desc="Ajustes"]')
        print(f"   {'✅' if menu_hidden else '❌'} PINPAD MENU HIDDEN")
        print(f"   {'✅' if tabs_hidden else '⚠️ '} BOTTOM NAV HIDDEN")

        # ── STEP 3: EXIT PROTECTOR ───────────────────────────────────────────
        print("\n👉 STEP 3: EXITING PROTECTOR...")
        driver.back()
        time.sleep(2)
        exited = _is_on_pinpad_screen(driver)
        if not exited:
            print("   ℹ️  BACK KEY DID NOT EXIT — TAPPING SCREEN CENTER...")
            size = driver.get_window_size()
            driver.tap([(size['width'] // 2, size['height'] // 2)])
            time.sleep(2)
            if not _is_on_pinpad_screen(driver):
                driver.back()
                time.sleep(2)
            exited = _is_on_pinpad_screen(driver)
        print(f"   {'✅' if exited else '❌'} BACK ON PINPAD SCREEN")
        utils.take_screenshot(driver, "PP09_02_EXITED", "t6")

        if menu_hidden and exited:
            result = "SUCCESS"
            print("\n✅ PP-09 RESULT: SUCCESS — PROTECTOR SHOWN AND EXITED")
        else:
            print(f"\n❌ PP-09 RESULT: FAIL — shown={menu_hidden} | exited={exited}")

    except Exception as e:
        print(f"\n💥 PP-09 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "PP09_CRITICAL_ERROR", "t6")
        except: pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 PP-09 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# PP-10: "COMANDOS RECIBIDOS" SHOWS PINPAD_STARTED (PORT + ADDRESS)
# ==================================================================================

def PP_10():
    print("\n" + "=" * 60)
    print("PP-10: 'COMANDOS RECIBIDOS' SHOWS PINPAD_STARTED")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        if not _setup_until_pinpad(driver, wait, "PP-10"):
            return False

        # ── STEP 1: OPEN COMANDOS RECIBIDOS ──────────────────────────────────
        print("\n👉 STEP 1: OPENING 'Comandos recibidos'...")
        if not _open_pinpad_option(driver, config.XPATH_PP_BTN_COMANDOS, "Comandos recibidos"):
            utils.take_screenshot(driver, "PP10_01_CLICK_FAILED", "t6")
            return False
        utils.take_screenshot(driver, "PP10_01_COMANDOS", "t6")

        # ── STEP 2: VERIFY PINPAD_STARTED ENTRY ──────────────────────────────
        print("\n👉 STEP 2: VERIFYING 'PINPAD_STARTED' ENTRY...")
        entry_ok = port_ok = address_ok = False
        try:
            entry = driver.find_element(By.XPATH, config.XPATH_PP_CMD_PINPAD_STARTED)
            entry_ok = True
            # PORT / ADDRESS MAY BE MERGED IN THE ENTRY OR LIVE IN SIBLING NODES
            text = _element_label(entry)
            try:
                text += " " + _element_label(entry.find_element(By.XPATH, './..'))
            except:
                pass
            for el in driver.find_elements(
                By.XPATH, '//*[contains(@text,"port") or contains(@content-desc,"port") or '
                          'contains(@text,"address") or contains(@content-desc,"address")]'
            ):
                text += " " + _element_label(el)
            port_ok    = f"port: {config.PP_EXPECTED_PORT}" in text
            address_ok = re.search(r'address:\s*\d{1,3}(?:\.\d{1,3}){3}', text) is not None
            time_match = re.search(r'\d{2}:\d{2}:\d{2}', text)
            print(f"   ✅ PINPAD_STARTED FOUND")
            print(f"   {'✅' if port_ok else '❌'} port: {config.PP_EXPECTED_PORT}")
            print(f"   {'✅' if address_ok else '❌'} address: <IP>")
            print(f"   ℹ️  TIMESTAMP: {time_match.group(0) if time_match else 'NOT FOUND'}")
        except:
            print("   ❌ PINPAD_STARTED NOT FOUND")
            _dump_screen(driver)

        limpiar_ok = _is_visible(driver, config.XPATH_PP_CMD_BTN_LIMPIAR)
        print(f"   {'✅' if limpiar_ok else '❌'} 'Limpiar' BUTTON")

        if entry_ok and port_ok and address_ok and limpiar_ok:
            result = "SUCCESS"
            print("\n✅ PP-10 RESULT: SUCCESS — PINPAD_STARTED LOGGED WITH PORT AND ADDRESS")
        else:
            print(f"\n❌ PP-10 RESULT: FAIL — entry={entry_ok} | port={port_ok} | "
                  f"address={address_ok} | limpiar={limpiar_ok}")

    except Exception as e:
        print(f"\n💥 PP-10 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "PP10_CRITICAL_ERROR", "t6")
        except: pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 PP-10 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# PP-11: "LIMPIAR" CLEARS THE RECEIVED COMMANDS LIST
# ==================================================================================

def PP_11():
    print("\n" + "=" * 60)
    print("PP-11: 'LIMPIAR' CLEARS RECEIVED COMMANDS")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        if not _setup_until_pinpad(driver, wait, "PP-11"):
            return False

        print("\n👉 STEP 1: OPENING 'Comandos recibidos'...")
        if not _open_pinpad_option(driver, config.XPATH_PP_BTN_COMANDOS, "Comandos recibidos"):
            utils.take_screenshot(driver, "PP11_01_CLICK_FAILED", "t6")
            return False

        before = len(driver.find_elements(By.XPATH, config.XPATH_PP_CMD_PINPAD_STARTED))
        print(f"   ℹ️  PINPAD_STARTED ENTRIES BEFORE: {before}")
        utils.take_screenshot(driver, "PP11_01_BEFORE_CLEAN", "t6")

        # ── STEP 2: CLICK LIMPIAR ────────────────────────────────────────────
        print("\n👉 STEP 2: CLICKING 'Limpiar'...")
        if not _click_first(driver, [config.XPATH_PP_CMD_BTN_LIMPIAR], "Limpiar", keyword="Limpiar"):
            utils.take_screenshot(driver, "PP11_02_CLICK_FAILED", "t6")
            return False

        # ── STEP 3: VERIFY LIST IS EMPTY ─────────────────────────────────────
        print("\n👉 STEP 3: VERIFYING LIST IS EMPTY...")
        after = len(driver.find_elements(By.XPATH, config.XPATH_PP_CMD_PINPAD_STARTED))
        print(f"   {'✅' if after == 0 else '❌'} PINPAD_STARTED ENTRIES AFTER: {after}")
        utils.take_screenshot(driver, "PP11_02_AFTER_CLEAN", "t6")

        if after == 0:
            result = "SUCCESS"
            print("\n✅ PP-11 RESULT: SUCCESS — COMMANDS LIST CLEARED")
        else:
            print("\n❌ PP-11 RESULT: FAIL — ENTRIES STILL PRESENT AFTER 'Limpiar'")

    except Exception as e:
        print(f"\n💥 PP-11 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "PP11_CRITICAL_ERROR", "t6")
        except: pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 PP-11 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# PP-12: SERVER RESTART REGISTERS A NEW PINPAD_STARTED COMMAND
# ==================================================================================

def PP_12():
    print("\n" + "=" * 60)
    print("PP-12: SERVER RESTART LOGS A NEW PINPAD_STARTED")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        if not _setup_until_pinpad(driver, wait, "PP-12"):
            return False

        # ── STEP 1: CLEAN THE LIST ───────────────────────────────────────────
        print("\n👉 STEP 1: CLEANING 'Comandos recibidos'...")
        _open_pinpad_option(driver, config.XPATH_PP_BTN_COMANDOS, "Comandos recibidos")
        _click_first(driver, [config.XPATH_PP_CMD_BTN_LIMPIAR], "Limpiar", keyword="Limpiar")
        cleaned = len(driver.find_elements(By.XPATH, config.XPATH_PP_CMD_PINPAD_STARTED)) == 0
        print(f"   {'✅' if cleaned else '⚠️ '} LIST EMPTY: {cleaned}")
        _click_back_arrow(driver)

        # ── STEP 2: RESTART SERVER (OFF → ON) ────────────────────────────────
        print("\n👉 STEP 2: RESTARTING SERVER (OFF → ON)...")
        _set_server(driver, False)
        _set_server(driver, True)
        server_on = _server_state(driver)
        print(f"   ℹ️  SERVER STATE: {_state_label(server_on)}")
        utils.take_screenshot(driver, "PP12_01_SERVER_RESTARTED", "t6")

        # ── STEP 3: VERIFY NEW ENTRY ─────────────────────────────────────────
        print("\n👉 STEP 3: VERIFYING NEW 'PINPAD_STARTED' ENTRY...")
        _open_pinpad_option(driver, config.XPATH_PP_BTN_COMANDOS, "Comandos recibidos")
        count = len(driver.find_elements(By.XPATH, config.XPATH_PP_CMD_PINPAD_STARTED))
        print(f"   {'✅' if count >= 1 else '❌'} PINPAD_STARTED ENTRIES: {count}")
        utils.take_screenshot(driver, "PP12_02_NEW_ENTRY", "t6")

        if server_on and count >= 1:
            result = "SUCCESS"
            print("\n✅ PP-12 RESULT: SUCCESS — RESTART LOGGED A NEW PINPAD_STARTED")
        else:
            print(f"\n❌ PP-12 RESULT: FAIL — server={_state_label(server_on)} | entries={count}")

    except Exception as e:
        print(f"\n💥 PP-12 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "PP12_CRITICAL_ERROR", "t6")
        except: pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 PP-12 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# PP-13: "HORARIOS DE ACTUALIZACIONES" SCREEN LOADS WITH DEFAULT VALUES
# ==================================================================================

def PP_13():
    print("\n" + "=" * 60)
    print("PP-13: 'HORARIOS DE ACTUALIZACIONES' SCREEN")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        if not _setup_until_pinpad(driver, wait, "PP-13"):
            return False

        print("\n👉 STEP 1: OPENING 'Horarios de actualizaciones'...")
        if not _open_pinpad_option(driver, config.XPATH_PP_BTN_HORARIOS, "Horarios de actualizaciones"):
            utils.take_screenshot(driver, "PP13_01_CLICK_FAILED", "t6")
            return False
        utils.take_screenshot(driver, "PP13_01_HORARIOS", "t6")

        # ── STEP 2: VERIFY ELEMENTS ──────────────────────────────────────────
        print("\n👉 STEP 2: VERIFYING SCREEN ELEMENTS...")
        checks = {
            "TITLE 'Actualizaciones'" : _is_visible(driver, config.XPATH_PP_UPD_SCREEN_TITLE),
            "DESCRIPTION"             : _is_visible(driver, config.XPATH_PP_UPD_DESCRIPCION),
            "ROW 'Hora de inicio'"    : _is_visible(driver, config.XPATH_PP_UPD_HORA_INICIO),
            "ROW 'Hora de fin'"       : _is_visible(driver, config.XPATH_PP_UPD_HORA_FIN),
            "BUTTON 'Confirmar'"      : _is_visible(driver, config.XPATH_PP_UPD_BTN_CONFIRMAR),
            "BUTTON 'Cancelar'"       : _is_visible(driver, config.XPATH_PP_UPD_BTN_CANCELAR),
        }
        for label, ok in checks.items():
            print(f"   {'✅' if ok else '❌'} {label}")

        # ── STEP 3: VERIFY VALUES ────────────────────────────────────────────
        print("\n👉 STEP 3: READING CURRENT VALUES...")
        inicio = _read_time_value(driver, config.XPATH_PP_UPD_HORA_INICIO)
        fin    = _read_time_value(driver, config.XPATH_PP_UPD_HORA_FIN)
        print(f"   ℹ️  HORA DE INICIO: {inicio} (DEFAULT {config.PP_DEFAULT_HORA_INICIO})")
        print(f"   ℹ️  HORA DE FIN   : {fin} (DEFAULT {config.PP_DEFAULT_HORA_FIN})")

        if all(checks.values()) and inicio and fin:
            result = "SUCCESS"
            print("\n✅ PP-13 RESULT: SUCCESS — HORARIOS SCREEN COMPLETE")
        else:
            print(f"\n❌ PP-13 RESULT: FAIL — {checks} | inicio={inicio} | fin={fin}")
            _dump_screen(driver)

    except Exception as e:
        print(f"\n💥 PP-13 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "PP13_CRITICAL_ERROR", "t6")
        except: pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 PP-13 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# PP-14 / PP-15: TIME PICKER OPENS — CANCELAR KEEPS THE VALUE (SHARED FLOW)
# ==================================================================================

def _run_picker_cancel_case(test_id, label, row_xpath):
    tag = test_id.replace("-", "")
    print("\n" + "=" * 60)
    print(f"{test_id}: '{label.upper()}' PICKER — CANCELAR KEEPS VALUE")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        if not _setup_until_pinpad(driver, wait, test_id):
            return False

        print("\n👉 STEP 1: OPENING 'Horarios de actualizaciones'...")
        if not _open_pinpad_option(driver, config.XPATH_PP_BTN_HORARIOS, "Horarios de actualizaciones"):
            utils.take_screenshot(driver, f"{tag}_01_CLICK_FAILED", "t6")
            return False
        before = _read_time_value(driver, row_xpath)
        print(f"   ℹ️  VALUE BEFORE: {before}")

        # ── STEP 2: OPEN PICKER ──────────────────────────────────────────────
        print(f"\n👉 STEP 2: OPENING '{label}' PICKER...")
        if not _open_time_picker(driver, row_xpath, label):
            utils.take_screenshot(driver, f"{tag}_02_PICKER_FAILED", "t6")
            return False
        utils.take_screenshot(driver, f"{tag}_02_PICKER_OPEN", "t6")

        sheet_title_ok = len(driver.find_elements(By.XPATH, row_xpath)) >= 2  # ROW + SHEET TITLE
        am_pm_ok = _is_visible(driver, '//*[@text="AM" or @content-desc="AM"]')
        print(f"   {'✅' if sheet_title_ok else '❌'} SHEET TITLE '{label}'")
        print(f"   {'✅' if am_pm_ok else '❌'} AM/PM COLUMN")

        # ── STEP 3: MOVE WHEEL AND CANCEL ────────────────────────────────────
        print("\n👉 STEP 3: MOVING HOUR WHEEL AND CLICKING 'Cancelar'...")
        _scroll_hour_wheel(driver, _hour_of(before), steps=1)
        _click_sheet_button(driver, config.XPATH_PP_UPD_BTN_CANCELAR, "Cancelar")

        sheet_closed = not _is_visible(driver, config.XPATH_PP_PICKER_SHEET)
        after = _read_time_value(driver, row_xpath)
        print(f"   {'✅' if sheet_closed else '❌'} PICKER CLOSED")
        print(f"   {'✅' if after == before else '❌'} VALUE AFTER: {after} (EXPECTED {before})")
        utils.take_screenshot(driver, f"{tag}_03_AFTER_CANCEL", "t6")

        if sheet_closed and before and after == before:
            result = "SUCCESS"
            print(f"\n✅ {test_id} RESULT: SUCCESS — PICKER CANCELLED WITHOUT CHANGES")
        else:
            print(f"\n❌ {test_id} RESULT: FAIL — closed={sheet_closed} | before={before} | after={after}")

    except Exception as e:
        print(f"\n💥 {test_id} CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, f"{tag}_CRITICAL_ERROR", "t6")
        except: pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 {test_id} RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


def PP_14():
    _run_picker_cancel_case("PP-14", "Hora de inicio", config.XPATH_PP_UPD_HORA_INICIO)


def PP_15():
    _run_picker_cancel_case("PP-15", "Hora de fin", config.XPATH_PP_UPD_HORA_FIN)


# ==================================================================================
# PP-16: CHANGE "HORA DE INICIO" + CONFIRMAR PERSISTS THE NEW VALUE
# ==================================================================================

def PP_16():
    print("\n" + "=" * 60)
    print("PP-16: CHANGE 'HORA DE INICIO' + CONFIRMAR PERSISTS")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"
    before = None
    changed = False

    def _set_start_hour(steps):
        """OPENS PICKER → MOVES WHEEL → CONFIRMS SHEET → CONFIRMS SCREEN."""
        current = _read_time_value(driver, config.XPATH_PP_UPD_HORA_INICIO)
        if not _open_time_picker(driver, config.XPATH_PP_UPD_HORA_INICIO, "Hora de inicio"):
            return None, None
        _scroll_hour_wheel(driver, _hour_of(current), steps=steps)
        _click_sheet_button(driver, config.XPATH_PP_UPD_BTN_CONFIRMAR, "Confirmar")
        on_screen = _read_time_value(driver, config.XPATH_PP_UPD_HORA_INICIO)
        print(f"   ℹ️  VALUE ON SCREEN BEFORE SAVING: {on_screen}")
        _click_first(driver, [config.XPATH_PP_UPD_BTN_CONFIRMAR], "Confirmar (screen)")
        return current, on_screen

    try:
        if not _setup_until_pinpad(driver, wait, "PP-16"):
            return False

        print("\n👉 STEP 1: OPENING 'Horarios de actualizaciones'...")
        if not _open_pinpad_option(driver, config.XPATH_PP_BTN_HORARIOS, "Horarios de actualizaciones"):
            utils.take_screenshot(driver, "PP16_01_CLICK_FAILED", "t6")
            return False
        utils.take_screenshot(driver, "PP16_01_BEFORE", "t6")

        # ── STEP 2: CHANGE HOUR (+1) AND CONFIRM ─────────────────────────────
        print("\n👉 STEP 2: MOVING 'Hora de inicio' +1 HOUR AND CONFIRMING...")
        before, on_screen = _set_start_hour(+1)
        changed = on_screen is not None and on_screen != before
        print(f"   {'✅' if changed else '❌'} VALUE CHANGED: {before} → {on_screen}")
        utils.take_screenshot(driver, "PP16_02_CONFIRMED", "t6")

        # ── STEP 3: RE-ENTER AND VERIFY PERSISTENCE ──────────────────────────
        print("\n👉 STEP 3: RE-ENTERING TO VERIFY PERSISTENCE...")
        if not _is_on_pinpad_screen(driver):
            _click_back_arrow(driver)
        _open_pinpad_option(driver, config.XPATH_PP_BTN_HORARIOS, "Horarios de actualizaciones")
        persisted = _read_time_value(driver, config.XPATH_PP_UPD_HORA_INICIO)
        print(f"   {'✅' if persisted == on_screen else '❌'} PERSISTED VALUE: {persisted} (EXPECTED {on_screen})")
        utils.take_screenshot(driver, "PP16_03_PERSISTED", "t6")

        if changed and persisted == on_screen:
            result = "SUCCESS"
            print("\n✅ PP-16 RESULT: SUCCESS — NEW START HOUR SAVED AND PERSISTED")
        else:
            print(f"\n❌ PP-16 RESULT: FAIL — before={before} | confirmed={on_screen} | persisted={persisted}")

    except Exception as e:
        print(f"\n💥 PP-16 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "PP16_CRITICAL_ERROR", "t6")
        except: pass
    finally:
        # POSTCONDITION: RESTORE ORIGINAL START HOUR (-1)
        if changed:
            try:
                print(f"\n🔧 POSTCONDITION: RESTORING 'Hora de inicio' TO {before}...")
                if not _is_visible(driver, config.XPATH_PP_UPD_HORA_INICIO):
                    _open_pinpad_option(driver, config.XPATH_PP_BTN_HORARIOS, "Horarios de actualizaciones")
                _set_start_hour(-1)
                if not _is_on_pinpad_screen(driver):
                    _click_back_arrow(driver)
                _open_pinpad_option(driver, config.XPATH_PP_BTN_HORARIOS, "Horarios de actualizaciones")
                restored = _read_time_value(driver, config.XPATH_PP_UPD_HORA_INICIO)
                print(f"   {'✅' if restored == before else '⚠️ '} RESTORED VALUE: {restored}")
            except Exception as e:
                print(f"   ⚠️  RESTORE FAILED: {e}")
        print("\n" + "-" * 60)
        print(f"📊 PP-16 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# PP-17: CHANGE "HORA DE FIN" + CANCELAR (SCREEN) DISCARDS THE CHANGE
# ==================================================================================

def PP_17():
    print("\n" + "=" * 60)
    print("PP-17: CHANGE 'HORA DE FIN' + CANCELAR DISCARDS")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        if not _setup_until_pinpad(driver, wait, "PP-17"):
            return False

        print("\n👉 STEP 1: OPENING 'Horarios de actualizaciones'...")
        if not _open_pinpad_option(driver, config.XPATH_PP_BTN_HORARIOS, "Horarios de actualizaciones"):
            utils.take_screenshot(driver, "PP17_01_CLICK_FAILED", "t6")
            return False
        before = _read_time_value(driver, config.XPATH_PP_UPD_HORA_FIN)
        print(f"   ℹ️  VALUE BEFORE: {before}")

        # ── STEP 2: CHANGE HOUR IN PICKER AND CONFIRM THE SHEET ──────────────
        print("\n👉 STEP 2: MOVING 'Hora de fin' +1 HOUR (SHEET CONFIRMAR)...")
        if not _open_time_picker(driver, config.XPATH_PP_UPD_HORA_FIN, "Hora de fin"):
            utils.take_screenshot(driver, "PP17_02_PICKER_FAILED", "t6")
            return False
        _scroll_hour_wheel(driver, _hour_of(before), steps=1)
        _click_sheet_button(driver, config.XPATH_PP_UPD_BTN_CONFIRMAR, "Confirmar")
        draft = _read_time_value(driver, config.XPATH_PP_UPD_HORA_FIN)
        print(f"   ℹ️  DRAFT VALUE ON SCREEN: {draft}")
        utils.take_screenshot(driver, "PP17_02_DRAFT", "t6")

        # ── STEP 3: CANCEL THE SCREEN ────────────────────────────────────────
        print("\n👉 STEP 3: CLICKING SCREEN 'Cancelar'...")
        _click_first(driver, [config.XPATH_PP_UPD_BTN_CANCELAR], "Cancelar (screen)")

        # ── STEP 4: RE-ENTER AND VERIFY ORIGINAL VALUE ───────────────────────
        print("\n👉 STEP 4: RE-ENTERING TO VERIFY ORIGINAL VALUE...")
        if not _is_on_pinpad_screen(driver):
            _click_back_arrow(driver)
        _open_pinpad_option(driver, config.XPATH_PP_BTN_HORARIOS, "Horarios de actualizaciones")
        after = _read_time_value(driver, config.XPATH_PP_UPD_HORA_FIN)
        print(f"   {'✅' if after == before else '❌'} VALUE AFTER: {after} (EXPECTED {before})")
        utils.take_screenshot(driver, "PP17_03_AFTER_CANCEL", "t6")

        if draft and draft != before and after == before:
            result = "SUCCESS"
            print("\n✅ PP-17 RESULT: SUCCESS — CANCELAR DISCARDED THE CHANGE")
        elif draft == before:
            print("\n❌ PP-17 RESULT: FAIL — HOUR WHEEL DID NOT CHANGE THE VALUE (CHECK SWIPE)")
        else:
            print(f"\n❌ PP-17 RESULT: FAIL — before={before} | draft={draft} | after={after}")

    except Exception as e:
        print(f"\n💥 PP-17 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "PP17_CRITICAL_ERROR", "t6")
        except: pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 PP-17 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# PP-18: BACK ARROW FROM EVERY PINPAD SUB-SCREEN RETURNS TO PINPAD
# ==================================================================================

def PP_18():
    print("\n" + "=" * 60)
    print("🧪 PP-18: BACK ARROW VALIDATION — ALL PINPAD SUB-SCREENS")
    print("=" * 60)

    driver, wait = utils.start_driver()
    results = {}

    SUB_SCREENS = [
        ("Configuración",               config.XPATH_PP_BTN_CONFIGURACION),
        ("Comandos recibidos",          config.XPATH_PP_BTN_COMANDOS),
        ("Horarios de actualizaciones", config.XPATH_PP_BTN_HORARIOS),
    ]

    try:
        if not _setup_until_pinpad(driver, wait, "PP-18"):
            return False
        utils.take_screenshot(driver, "PP18_00_PINPAD_MAIN", "t6")

        for name, xpath in SUB_SCREENS:
            print(f"\n{'─'*55}")
            print(f"  🔍 TESTING: {name}")
            print(f"{'─'*55}")
            tag = name[:12].replace(' ', '_')

            if not _is_on_pinpad_screen(driver):
                results[name] = (False, "NOT ON PINPAD SCREEN BEFORE ENTERING")
                continue

            if not _open_pinpad_option(driver, xpath, name) or _is_on_pinpad_screen(driver):
                utils.take_screenshot(driver, f"PP18_{tag}_FAIL_ENTER", "t6")
                results[name] = (False, "SUB-SCREEN DID NOT OPEN")
                continue
            utils.take_screenshot(driver, f"PP18_{tag}_ENTERED", "t6")

            clicked, strategy = _click_back_arrow(driver)
            utils.take_screenshot(driver, f"PP18_{tag}_BACK_RESULT", "t6")
            if clicked and _is_on_pinpad_screen(driver):
                print("   ✅ RETURNED TO PINPAD ✓")
                results[name] = (True, f"OK — {strategy}")
            else:
                print("   ❌ DID NOT RETURN TO PINPAD — screen dump:")
                _dump_screen(driver)
                results[name] = (False, f"BACK ({strategy}) DID NOT RETURN TO PINPAD")
                # RECOVER FOR THE NEXT SUB-SCREEN
                _navigate_to_pinpad(driver, wait)

        # PINPAD → AJUSTES
        print(f"\n{'─'*55}")
        print("  🔍 TESTING: PinPad → Ajustes")
        print(f"{'─'*55}")
        clicked, strategy = _click_back_arrow(driver)
        on_ajustes = _is_visible(driver, config.XPATH_PP_BTN_SERVIDOR_PINPAD) or \
                     _is_visible(driver, config.XPATH_AJ_SECTION_LECTOR)
        results["PinPad → Ajustes"] = (
            clicked and on_ajustes,
            f"OK — {strategy}" if on_ajustes else f"BACK ({strategy}) DID NOT RETURN TO AJUSTES",
        )
        utils.take_screenshot(driver, "PP18_PINPAD_BACK_TO_AJUSTES", "t6")

    except Exception as e:
        print(f"\n💥 PP-18 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "PP18_CRITICAL_ERROR", "t6")
        except: pass
    finally:
        utils.close_driver(driver)

    passed_count = sum(1 for v in results.values() if v[0])
    failed_count = len(results) - passed_count

    print("\n" + "=" * 65)
    print("📊 PP-18 — BACK ARROW SUMMARY")
    print("=" * 65)
    print(f"  {'SUB-SCREEN':<32} {'RESULT':<8} NOTE")
    print("  " + "─" * 62)
    for name, (passed, note) in results.items():
        print(f"  {name:<32} {'✅ PASS' if passed else '❌ FAIL':<8} {note}")
    print("  " + "─" * 62)
    print(f"  TOTAL: {passed_count} PASSED / {failed_count} FAILED / {len(results)} TESTED")
    print("=" * 65)

    overall = len(results) > 0 and failed_count == 0
    print(f"\n  PP-18 OVERALL: {'✅ PASS' if overall else '❌ FAIL'}")
    print("=" * 65)
    return overall


# ==================================================================================
# MAIN EXECUTION
# ==================================================================================

if __name__ == "__main__":

    logger, log_file, timestamp = utils.start_report("OPERATIONALS_T6")

    try:
        # EACH CASE RUNS ISOLATED: IF APPIUM DROPS A SESSION THE SUITE CONTINUES
        for case in [PP_01, PP_02, PP_03, PP_04, PP_05, PP_06, PP_07, PP_08, PP_09,
                     PP_10, PP_11, PP_12, PP_13, PP_14, PP_15, PP_16, PP_17, PP_18]:
            try:
                case()
            except Exception as e:
                print(f"\n💥 {case.__name__.replace('_', '-')} ABORTED — SESSION ERROR: {e.__class__.__name__}: {e}")
                print("   💡 CHECK THAT APPIUM IS RUNNING AND THE T6 IS CONNECTED (adb devices)")

    finally:
        logger.close()
        utils.generate_zip_report("OPERATIONALS_T6", logger, log_file, timestamp)
        utils.generate_html_report("OPERATIONALS_T6", log_file, timestamp)
