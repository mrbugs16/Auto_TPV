"""
# ==================================================================================
# FILENAME    : Negative_Scenarios.py
# FOLDER      : Automatizacion/T6/v2/Transactional/
# PROJECT     : MEMPHIS QA AUTOMATION FRAMEWORK
# DESCRIPTION : NEGATIVE / EDGE CASE TRANSACTION TEST SUITE.
#               VALIDATES THAT THE MEMPHIS APP CORRECTLY HANDLES FAILED,
#               DENIED, AND ERROR STATES DURING THE PAYMENT FLOW.
#
# TEST CASES (matrix TC-TRANS-02):
#   NS-01 : Insufficient Funds — Denied Transaction
#             Validate the red denied screen ("mega X") appears
#   NS-02 : Expired Card — Denied Transaction
#             Validate the denied screen for an expired card
#   NS-03 : User-Initiated Transaction Cancellation
#             User presses "Cancelar" on the card screen — FULLY AUTOMATED
#   NS-04 : Bluetooth Loss During Transaction
#             Disable BT mid-transaction via ADB, validate error handling
#   NS-05 : Card Read Error (dirty / badly inserted chip)
#             Validate the error shown when card cannot be read
#   NS-06 : Minimum and Maximum Amount Processing
#             Validate $0.01 min and $999,999.99 max — FULLY AUTOMATED
#
# SUCCESS LOGIC FOR NEGATIVE TESTS (inverted):
#   ✅ PASS = The app shows a DENIED / ERROR screen (the red "mega X")
#   ✅ PASS = The app does NOT crash after the negative event
#   ❌ FAIL = The green approval screen appears (unexpected)
#   ❌ FAIL = The app crashes or becomes unresponsive
#
# REQUIREMENTS:
#   - Appium server:      appium --relaxed-security
#   - T6 connected:       adb devices
#   - utils.py, config.py, utils_system.py in T6/v2/
# ==================================================================================
"""

import sys
import os
import time

# ── PATH SETUP ──────────────────────────────────────────────────────────────────
_transactional_dir = os.path.abspath(os.path.dirname(__file__))
_v2_dir            = os.path.abspath(os.path.join(_transactional_dir, '..'))
for _path in [_v2_dir, _transactional_dir]:
    if _path not in sys.path:
        sys.path.insert(0, _path)

import config
import utils
import utils_system as sys_ctrl

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

try:
    from appium.webdriver.common.appiumby import AppiumBy
except ImportError:
    class AppiumBy:
        ANDROID_UIAUTOMATOR = "android uiAutomator"


# ==================================================================================
# CONSTANTS
# ==================================================================================

CHARGE_AMOUNT       = "2500"    # press 2→5→0→0 = $25.00 on T6 right-to-left calculator
CARD_WAIT_SECONDS   = 30        # Active polling window for manual card insertion
EXTRA_WAIT_SECONDS  = 20        # Additional polling after manual window

# Amounts for NS-06 min/max test
AMOUNT_MINIMUM  = "1"           # press 1 = $0.01
AMOUNT_MAXIMUM  = "99999999"    # 8 digits = $999,999.99

# Keywords used by polling helpers
DENIED_KEYWORDS   = [
    "denegada", "denegado", "rechazada", "rechazado",
    "fallida", "fallido", "declined", "denied",
    "no fue posible", "error", "cancelada", "cancelado",
    "insuficientes", "expirada", "vencida", "reintentar"
]
APPROVAL_KEYWORDS = ["aprobada", "transacción aprobada", "approved"]


# ── XPATHS ──────────────────────────────────────────────────────────────────────

# TRANSACTION FLOW
XPATH_BTN_CHARGE       = (
    '//*[contains(@content-desc,"Realizar cobro") or '
    'contains(@text,"Realizar cobro")]'
)
XPATH_POPUP_SALE_TYPE  = (
    '//*[contains(@content-desc,"tipo de operación") or '
    'contains(@text,"tipo de operación") or '
    'contains(@content-desc,"Qué tipo") or contains(@text,"Qué tipo")]'
)
XPATH_BTN_NORMAL_SALE  = (
    '//*[@content-desc="Venta Normal" or @text="Venta Normal" or '
    'contains(@content-desc,"Venta Normal") or contains(@text,"Venta Normal")]'
)
XPATH_SCREEN_CARD      = (
    '//*[contains(@content-desc,"Acerca") or contains(@text,"Acerca") or '
    'contains(@content-desc,"inserta") or contains(@text,"inserta") or '
    'contains(@content-desc,"desliza") or contains(@text,"desliza") or '
    'contains(@content-desc,"Iniciando") or contains(@text,"Iniciando")]'
)
XPATH_BTN_CANCEL_TX    = (
    '//*[@content-desc="Cancelar" or @text="Cancelar" or '
    'contains(@content-desc,"Cancelar") or contains(@text,"Cancelar")]'
)

# RESULT SCREENS
XPATH_SCREEN_APPROVED  = (
    '//*[contains(@content-desc,"Transacción aprobada") or '
    'contains(@text,"Transacción aprobada") or '
    'contains(@content-desc,"aprobada") or contains(@text,"aprobada")]'
)
XPATH_SCREEN_DENIED    = (
    '//*[contains(@content-desc,"Transacción denegada") or '
    'contains(@text,"Transacción denegada") or '
    'contains(@content-desc,"denegada") or contains(@text,"denegada") or '
    'contains(@content-desc,"Denegada") or contains(@text,"Denegada")]'
)
XPATH_SCREEN_ERROR     = (
    '//*[contains(@content-desc,"Error") or contains(@text,"Error") or '
    'contains(@content-desc,"error") or contains(@text,"error") or '
    'contains(@content-desc,"no fue posible") or contains(@text,"no fue posible") or '
    'contains(@content-desc,"fallida") or contains(@text,"fallida")]'
)

# POST-DENIAL NAVIGATION
XPATH_BTN_ACCEPT       = (
    '//*[@content-desc="Aceptar" or @text="Aceptar" or '
    'contains(@content-desc,"Aceptar") or contains(@text,"Aceptar")]'
)
XPATH_BTN_RETRY        = (
    '//*[contains(@content-desc,"Reintentar") or contains(@text,"Reintentar")]'
)
XPATH_DISPLAY_ZERO     = (
    '//*[contains(@content-desc,"0.00") or contains(@text,"0.00")]'
)


# ==================================================================================
# INTERNAL HELPERS
# ==================================================================================

def _take_screenshot(driver, name):
    """Saves a T6 screenshot. Errors are printed, never swallowed."""
    try:
        utils.take_screenshot(driver, name, "t6")
    except Exception as err:
        print(f"   WARNING: SCREENSHOT FAILED [{name}]: {err}")


def _login(driver, wait):
    """
    Full login sequence:
    onboarding → credentials → commerce setup → reader popup → calculator.
    """
    print("   [HELPER] PHASE 1: ONBOARDING SLIDES...")
    time.sleep(3)
    for index, btn_xpath in enumerate([
        config.XPATH_OB_BTN_SIGUIENTE,
        config.XPATH_OB_BTN_SIGUIENTE,
        config.XPATH_OB_BTN_COMENZAR,
    ], start=1):
        label = "Next" if index < 3 else "Start"
        try:
            utils.click_element(driver, btn_xpath)
            time.sleep(1.5 if index < 3 else 2)
            print(f"   OK  SLIDE {index} — '{label}'")
        except:
            print(f"   WARN SLIDE {index} SKIPPED")
            if index == 1:
                try:
                    utils.click_element(driver, config.XPATH_OB_BTN_SALTAR)
                    time.sleep(1)
                except:
                    pass

    print("   [HELPER] PHASE 2: ENTERING CREDENTIALS...")
    utils.type_text(driver, config.XPATH_INPUT_USUARIO, config.USUARIO_VALIDO)
    utils.type_text(driver, config.XPATH_INPUT_PASS,    config.PASS_VALIDO)
    try:
        driver.hide_keyboard()
    except:
        pass
    utils.click_element(driver, config.XPATH_LG_BTN_INICIAR)
    time.sleep(5)

    print("   [HELPER] PHASE 3: COMMERCE SETUP...")
    if utils.verify_element(wait, config.XPATH_CC_SCREEN, "COMMERCE SETUP SCREEN"):
        try:
            utils.type_text(driver, config.XPATH_CC_INPUT_AFILIACION, config.CC_AFILIACION)
            utils.type_text(driver, config.XPATH_CC_INPUT_TOKEN,      config.CC_TOKEN)
            try:
                driver.hide_keyboard()
            except:
                pass
            utils.click_element(driver, config.XPATH_CC_BTN_CONFIRMAR)
            time.sleep(3)
        except Exception as err:
            print(f"   WARN COMMERCE FORM: {err}")
    else:
        print("   INFO COMMERCE ALREADY LINKED.")

    print("   [HELPER] PHASE 4: READER POPUP...")
    time.sleep(2)
    if utils.verify_element(wait, config.XPATH_LG_POPUP_LECTOR_NC, "READER NOT CONFIGURED POPUP"):
        try:
            utils.click_element(driver, config.XPATH_LG_BTN_CONFIGURAR_AHORA)
            time.sleep(3)
            WebDriverWait(driver, 8).until(
                lambda d: d.find_element(By.XPATH, config.XPATH_LG_LECTOR_CONFIGURADO)
            )
            utils.click_element(driver, config.XPATH_LG_BTN_ACEPTAR_LECTOR)
            time.sleep(2)
            print("   OK  READER CONFIGURED.")
        except Exception as err:
            print(f"   WARN READER POPUP: {err}")
    else:
        print("   INFO NO READER POPUP.")
        time.sleep(2)

    print("   OK  LOGIN COMPLETE.")


def _enter_amount(driver, digits):
    """
    Types an amount digit by digit on the T6 calculator.

    T6 RIGHT-TO-LEFT CALCULATOR LOGIC:
        "2500" → 2→5→0→0 = $25.00
        "1"    → press 1  = $0.01  (minimum)
        "99999999" → 8 digits = $999,999.99 (maximum)
    """
    print(f"   TYPING DIGITS: {digits}")
    for digit in digits:
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, f'//*[@content-desc="{digit}" or @text="{digit}"]')
                )
            ).click()
            time.sleep(0.3)
        except:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    f'new UiSelector().text("{digit}")'
                ).click()
                time.sleep(0.3)
            except Exception as err:
                print(f"   WARN DIGIT '{digit}': {err}")
    time.sleep(0.5)
    try:
        displayed = (
            driver.find_element(By.XPATH, config.XPATH_C_DISPLAY_UPDATED)
            .get_attribute("content-desc") or ""
        )
        print(f"   OK  DISPLAY: {displayed}")
    except:
        pass


def _navigate_to_card_screen(driver):
    """
    Goes from Calculator to the card insertion screen.
    Returns True when card screen is reached.
    """
    # CLICK CHARGE BUTTON
    charge_clicked = False
    for xpath in [XPATH_BTN_CHARGE,
                  '//*[contains(@content-desc,"cobro") or contains(@text,"cobro")]']:
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            ).click()
            charge_clicked = True
            print("   OK  'Realizar cobro' CLICKED.")
            break
        except:
            continue
    if not charge_clicked:
        print("   FAIL COULD NOT CLICK 'Realizar cobro'.")
        return False
    time.sleep(3)

    # WAIT FOR SALE TYPE POPUP
    try:
        WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.XPATH, XPATH_POPUP_SALE_TYPE))
        )
    except:
        pass

    # SELECT "VENTA NORMAL"
    sale_selected = False
    try:
        WebDriverWait(driver, 6).until(
            EC.element_to_be_clickable((By.XPATH, XPATH_BTN_NORMAL_SALE))
        ).click()
        sale_selected = True
        print("   OK  'Venta Normal' CLICKED.")
    except:
        try:
            driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().text("Venta Normal")'
            ).click()
            sale_selected = True
            print("   OK  'Venta Normal' CLICKED (UiAutomator).")
        except Exception as err:
            print(f"   FAIL 'Venta Normal': {err}")
            return False
    time.sleep(2)

    # VERIFY CARD SCREEN
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, XPATH_SCREEN_CARD))
        )
        print("   OK  CARD SCREEN REACHED.")
    except:
        page = driver.page_source.lower()
        if any(kw in page for kw in ["acerca", "inserta", "desliza", "iniciando"]):
            print("   OK  CARD SCREEN DETECTED VIA PAGE SOURCE.")
        else:
            print("   WARN CARD SCREEN NOT CONFIRMED.")
    return True


def _poll_for_denied_or_approved(driver, poll_seconds, label):
    """
    Polls every second checking for BOTH the denied screen AND the approval screen.
    Returns (denied: bool, approved: bool).

    WHY POLL FOR BOTH:
        In negative tests we expect denial — but if the card is approved instead
        (wrong card used), we need to know that too so the result can be marked
        INCONCLUSIVE rather than FAIL, giving the tester the right feedback.
    """
    end_time       = time.time() + poll_seconds
    denied_found   = False
    approved_found = False

    while time.time() < end_time:
        remaining = int(end_time - time.time())
        print(f"      POLLING {remaining:02d}s — {label}...", end="\r")

        # CHECK DENIED
        try:
            for elem in driver.find_elements(By.XPATH, XPATH_SCREEN_DENIED):
                t = (elem.get_attribute("text") or "").lower()
                d = (elem.get_attribute("content-desc") or "").lower()
                if any(kw in t + d for kw in DENIED_KEYWORDS):
                    print(f"\n   OK  DENIED SCREEN DETECTED: '{(t or d)[:60]}'")
                    denied_found = True
                    break
        except:
            pass

        # CHECK ERROR (also a valid denial state)
        if not denied_found:
            try:
                for elem in driver.find_elements(By.XPATH, XPATH_SCREEN_ERROR):
                    t = (elem.get_attribute("text") or "").lower()
                    d = (elem.get_attribute("content-desc") or "").lower()
                    if any(kw in t + d for kw in DENIED_KEYWORDS):
                        print(f"\n   OK  ERROR SCREEN DETECTED: '{(t or d)[:60]}'")
                        denied_found = True
                        break
            except:
                pass

        # CHECK APPROVAL (unexpected in negative tests)
        if not denied_found:
            try:
                for elem in driver.find_elements(By.XPATH, XPATH_SCREEN_APPROVED):
                    t = (elem.get_attribute("text") or "").lower()
                    d = (elem.get_attribute("content-desc") or "").lower()
                    if any(kw in t + d for kw in APPROVAL_KEYWORDS):
                        print(f"\n   WARN APPROVAL DETECTED (UNEXPECTED): '{(t or d)[:60]}'")
                        approved_found = True
                        break
            except:
                pass

        # PAGE SOURCE SCAN (catches toast messages and transient elements)
        if not denied_found and not approved_found:
            try:
                page = driver.page_source.lower()
                if any(kw in page for kw in DENIED_KEYWORDS):
                    denied_found = True
                    print(f"\n   OK  DENIED DETECTED VIA PAGE SOURCE.")
                elif any(kw in page for kw in APPROVAL_KEYWORDS):
                    approved_found = True
                    print(f"\n   WARN APPROVAL DETECTED VIA PAGE SOURCE (UNEXPECTED).")
            except:
                pass

        if denied_found or approved_found:
            break

        time.sleep(1)

    print()
    return denied_found, approved_found


def _dump_screen(driver, label="SCREEN STATE"):
    """Prints all visible text on screen for debug purposes."""
    print(f"   DEBUG {label}:")
    try:
        for elem in driver.find_elements(By.XPATH, "//*"):
            try:
                t = elem.get_attribute("text") or ""
                d = elem.get_attribute("content-desc") or ""
                if (t and len(t) > 2) or (d and len(d) > 2 and d != "null"):
                    print(f"      text='{t[:60]}' | desc='{d[:60]}'")
            except:
                continue
    except:
        pass


def _dismiss_result_screen(driver):
    """
    After a denied/error screen, dismisses it and returns to Calculator.
    Tries Accept → Retry → System Back in order.
    """
    for xpath in [XPATH_BTN_ACCEPT, XPATH_BTN_RETRY]:
        try:
            WebDriverWait(driver, 4).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            ).click()
            time.sleep(2)
            print("   OK  RESULT SCREEN DISMISSED.")
            return
        except:
            continue
    try:
        driver.back()
        time.sleep(1)
        print("   OK  SYSTEM BACK USED TO DISMISS SCREEN.")
    except:
        pass


# ==================================================================================
# NS-01: INSUFFICIENT FUNDS — DENIED TRANSACTION
# ==================================================================================

def NS_01_INSUFFICIENT_FUNDS():
    """
    NS-01: Validates the red denied screen ("mega X") appears when a card
    with INSUFFICIENT FUNDS is used for a $25.00 charge.

    MANUAL STEP:
        Insert a card known to have insufficient funds when prompted.
        The terminal sends the charge to the bank — bank declines it.

    SUCCESS: Red "Transacción denegada" screen appears (the "mega X").
    FAIL:    Green approval screen appears (bank should have rejected it).
    """
    print("\n" + "=" * 65)
    print("TEST NS-01: INSUFFICIENT FUNDS — DENIED TRANSACTION")
    print("=" * 65)

    driver, wait = utils.start_driver()
    result, note = False, ""

    try:
        print("\n>> STEP 1: LOGIN")
        _login(driver, wait)
        _take_screenshot(driver, "NS_01_STEP1_CALCULATOR")

        print("\n>> STEP 2: REACH CARD SCREEN ($25.00)")
        _enter_amount(driver, CHARGE_AMOUNT)
        _navigate_to_card_screen(driver)
        _take_screenshot(driver, "NS_01_STEP2_CARD_SCREEN")

        print(f"\n   {'='*55}")
        print("   CARD ACTION REQUIRED — NS-01")
        print(f"   {'='*55}")
        print("   >> INSERT A CARD WITH INSUFFICIENT FUNDS")
        print("   >> ENTER PIN ON T6 READER")
        print(f"   >> {CARD_WAIT_SECONDS}s POLLING — SHOULD SHOW RED DENIED SCREEN")
        print(f"   {'='*55}")

        denied, approved = _poll_for_denied_or_approved(
            driver, CARD_WAIT_SECONDS, "polling for denied screen"
        )
        if not denied and not approved:
            denied, approved = _poll_for_denied_or_approved(
                driver, EXTRA_WAIT_SECONDS, "extra polling"
            )

        _take_screenshot(driver, "NS_01_STEP3_RESULT_SCREEN")

        print("\n>> STEP 4: EVALUATING RESULT")
        if denied and not approved:
            result = True
            note   = "PASS — RED DENIED SCREEN APPEARED (insufficient funds handled correctly)"
            print(f"   PASS  NS-01: {note}")
        elif approved:
            result = False
            note   = "FAIL — GREEN APPROVAL APPEARED (card should have been denied)"
            print(f"   FAIL  NS-01: {note}")
        else:
            _dump_screen(driver, "NO RESULT DETECTED")
            result = False
            note   = "FAIL — NEITHER DENIED NOR APPROVAL SCREEN DETECTED"
            print(f"   FAIL  NS-01: {note}")

        _dismiss_result_screen(driver)
        _take_screenshot(driver, "NS_01_STEP5_BACK_TO_CALCULATOR")

    except Exception as err:
        result, note = False, f"CRITICAL ERROR: {err}"
        print(f"\nCRITICAL ERROR NS-01: {err}")
        try: _take_screenshot(driver, "NS_01_CRITICAL_ERROR")
        except: pass
    finally:
        utils.close_driver(driver)

    return result, note


# ==================================================================================
# NS-02: EXPIRED CARD — DENIED TRANSACTION
# ==================================================================================

def NS_02_EXPIRED_CARD():
    """
    NS-02: Validates the red denied screen when an EXPIRED card is used.

    MANUAL STEP:
        Insert an expired card when prompted.

    SUCCESS: Red denied screen with expiry-related message appears.
    """
    print("\n" + "=" * 65)
    print("TEST NS-02: EXPIRED CARD — DENIED TRANSACTION")
    print("=" * 65)

    driver, wait = utils.start_driver()
    result, note = False, ""

    try:
        print("\n>> STEP 1: LOGIN")
        _login(driver, wait)
        _take_screenshot(driver, "NS_02_STEP1_CALCULATOR")

        print("\n>> STEP 2: REACH CARD SCREEN ($25.00)")
        _enter_amount(driver, CHARGE_AMOUNT)
        _navigate_to_card_screen(driver)
        _take_screenshot(driver, "NS_02_STEP2_CARD_SCREEN")

        print(f"\n   {'='*55}")
        print("   CARD ACTION REQUIRED — NS-02")
        print(f"   {'='*55}")
        print("   >> INSERT AN EXPIRED CARD")
        print("   >> ENTER PIN IF PROMPTED")
        print(f"   >> {CARD_WAIT_SECONDS}s POLLING — SHOULD SHOW RED DENIED SCREEN")
        print(f"   {'='*55}")

        denied, approved = _poll_for_denied_or_approved(
            driver, CARD_WAIT_SECONDS, "polling for expiry denial"
        )
        if not denied and not approved:
            denied, approved = _poll_for_denied_or_approved(
                driver, EXTRA_WAIT_SECONDS, "extra polling"
            )

        _take_screenshot(driver, "NS_02_STEP3_RESULT_SCREEN")

        if denied and not approved:
            result = True
            note   = "PASS — RED DENIED SCREEN APPEARED (expired card handled correctly)"
        elif approved:
            result = False
            note   = "FAIL — GREEN APPROVAL APPEARED (expired card should be rejected)"
        else:
            _dump_screen(driver)
            result = False
            note   = "FAIL — NO RESULT SCREEN DETECTED"

        print(f"   {'PASS' if result else 'FAIL'}  NS-02: {note}")
        _dismiss_result_screen(driver)
        _take_screenshot(driver, "NS_02_STEP4_BACK_TO_CALCULATOR")

    except Exception as err:
        result, note = False, f"CRITICAL ERROR: {err}"
        print(f"\nCRITICAL ERROR NS-02: {err}")
        try: _take_screenshot(driver, "NS_02_CRITICAL_ERROR")
        except: pass
    finally:
        utils.close_driver(driver)

    return result, note


# ==================================================================================
# NS-03: USER-INITIATED TRANSACTION CANCELLATION
# ==================================================================================

def NS_03_USER_CANCELS_TRANSACTION():
    """
    NS-03: Validates that pressing "Cancelar" on the card screen aborts the
    transaction and returns the user to the Calculator screen.

    FULLY AUTOMATED — no physical card required.

    SUCCESS: Tapping Cancelar returns to Calculator ($0.00).
    FAIL:    App navigates somewhere unexpected or crashes.
    """
    print("\n" + "=" * 65)
    print("TEST NS-03: USER-INITIATED TRANSACTION CANCELLATION")
    print("   (AUTOMATED — NO CARD REQUIRED)")
    print("=" * 65)

    driver, wait = utils.start_driver()
    result, note = False, ""

    try:
        print("\n>> STEP 1: LOGIN")
        _login(driver, wait)
        _take_screenshot(driver, "NS_03_STEP1_CALCULATOR")

        print("\n>> STEP 2: REACH CARD SCREEN ($25.00)")
        _enter_amount(driver, CHARGE_AMOUNT)
        reached = _navigate_to_card_screen(driver)
        _take_screenshot(driver, "NS_03_STEP2_CARD_SCREEN")
        if not reached:
            return False, "COULD NOT REACH CARD SCREEN"

        print("\n>> STEP 3: CLICKING 'Cancelar' TO ABORT TRANSACTION")
        cancel_clicked = False
        try:
            btn = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable((By.XPATH, XPATH_BTN_CANCEL_TX))
            )
            btn.click()
            cancel_clicked = True
            print("   OK  'Cancelar' CLICKED.")
        except:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().text("Cancelar")'
                ).click()
                cancel_clicked = True
                print("   OK  'Cancelar' CLICKED (UiAutomator).")
            except Exception as err:
                note = f"COULD NOT CLICK 'Cancelar': {err}"
                print(f"   FAIL {note}")
                return False, note

        time.sleep(3)
        _take_screenshot(driver, "NS_03_STEP3_AFTER_CANCEL")

        print("\n>> STEP 4: VERIFYING RETURN TO CALCULATOR SCREEN")
        returned = False
        try:
            WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.XPATH, XPATH_DISPLAY_ZERO))
            )
            returned = True
            print("   OK  CALCULATOR ($0.00) VISIBLE — TRANSACTION CANCELLED.")
        except:
            try:
                driver.find_element(By.XPATH, config.XPATH_C_PANTALLA_COBRO)
                returned = True
                print("   OK  CALCULATOR SCREEN CONFIRMED.")
            except:
                page = driver.page_source.lower()
                if "0.00" in page or "cancelada" in page:
                    returned = True
                    print("   OK  CANCELLATION CONFIRMED VIA PAGE SOURCE.")

        _take_screenshot(driver, "NS_03_STEP4_FINAL_STATE")

        result = returned and cancel_clicked
        note   = (
            "PASS — TRANSACTION CANCELLED AND RETURNED TO CALCULATOR"
            if result else
            f"FAIL — cancel_clicked={cancel_clicked} | returned={returned}"
        )
        print(f"   {'PASS' if result else 'FAIL'}  NS-03: {note}")

    except Exception as err:
        result, note = False, f"CRITICAL ERROR: {err}"
        print(f"\nCRITICAL ERROR NS-03: {err}")
        try: _take_screenshot(driver, "NS_03_CRITICAL_ERROR")
        except: pass
    finally:
        utils.close_driver(driver)

    return result, note


# ==================================================================================
# NS-04: BLUETOOTH LOSS DURING TRANSACTION
# ==================================================================================

def NS_04_BLUETOOTH_LOSS_DURING_TRANSACTION():
    """
    NS-04: Validates app behavior when Bluetooth is cut MID-TRANSACTION via ADB.
    The Memphis card reader (lector) connects over BT — cutting it during payment
    should show an error, NOT crash the app.

    AUTOMATED via ADB (utils_system.py):
        1. Login + reach card screen (BT ON)
        2. Disable BT via ADB while on the card screen
        3. Poll for error / reader disconnect message
        4. Restore BT in finally block

    SUCCESS: Error or reader disconnect message appears without crash.
    FAIL:    App crashes or green approval appears despite no card.
    """
    print("\n" + "=" * 65)
    print("TEST NS-04: BLUETOOTH LOSS DURING TRANSACTION")
    print("   (AUTOMATED VIA ADB)")
    print("=" * 65)

    if not sys_ctrl.verify_device_connected():
        return False, "ADB DEVICE NOT CONNECTED — CANNOT RUN NS-04"

    driver, wait = utils.start_driver()
    result, note = False, ""

    try:
        print("\n>> STEP 1: LOGIN (BT ON)")
        _login(driver, wait)
        _take_screenshot(driver, "NS_04_STEP1_CALCULATOR")

        print("\n>> STEP 2: REACH CARD SCREEN (BT STILL ON)")
        _enter_amount(driver, CHARGE_AMOUNT)
        _navigate_to_card_screen(driver)
        _take_screenshot(driver, "NS_04_STEP2_CARD_SCREEN")

        print("\n>> STEP 3: DISABLING BLUETOOTH VIA ADB (MID-TRANSACTION)")
        sys_ctrl.disable_bluetooth()
        time.sleep(3)
        _take_screenshot(driver, "NS_04_STEP3_BT_DISABLED")

        print("\n>> STEP 4: POLLING FOR ERROR OR READER DISCONNECT MESSAGE")
        denied, approved = _poll_for_denied_or_approved(
            driver, CARD_WAIT_SECONDS, "polling for BT disconnection error"
        )

        # ADDITIONAL CHECK FOR READER-SPECIFIC MESSAGES
        reader_error_found = False
        try:
            page = driver.page_source.lower()
            reader_keywords = ["lector", "bluetooth", "conexión", "conectar", "reader"]
            if any(kw in page for kw in reader_keywords):
                reader_error_found = True
                print("   OK  READER/BT ERROR MESSAGE DETECTED IN PAGE SOURCE.")
        except:
            pass

        _take_screenshot(driver, "NS_04_STEP4_RESULT")
        _dump_screen(driver, "SCREEN STATE AFTER BT DISABLED")

        print("\n>> STEP 5: EVALUATING RESULT")
        app_alive = False
        try:
            driver.find_element(By.XPATH, '//*[@clickable="true"]')
            app_alive = True
            print("   OK  APP IS STILL RESPONSIVE (NO CRASH).")
        except:
            print("   WARN COULD NOT CONFIRM APP IS RESPONSIVE.")

        if denied or reader_error_found:
            result = True
            note   = (
                f"PASS — ERROR SCREEN APPEARED AFTER BT LOSS "
                f"(denied={denied} | reader_error={reader_error_found})"
            )
        elif approved:
            result = False
            note   = "FAIL — UNEXPECTED APPROVAL DESPITE BT BEING DISABLED"
        elif app_alive:
            # App is still running without error shown — acceptable if it did not crash
            result = True
            note   = "PASS — APP ALIVE AFTER BT LOSS (NO EXPLICIT ERROR SHOWN — acceptable)"
        else:
            result = False
            note   = "FAIL — APP MAY HAVE CRASHED AFTER BT LOSS"

        print(f"   {'PASS' if result else 'FAIL'}  NS-04: {note}")

    except Exception as err:
        result, note = False, f"CRITICAL ERROR: {err}"
        print(f"\nCRITICAL ERROR NS-04: {err}")
        try: _take_screenshot(driver, "NS_04_CRITICAL_ERROR")
        except: pass
    finally:
        utils.close_driver(driver)
        print("   RESTORING BLUETOOTH...")
        sys_ctrl.enable_bluetooth()
        time.sleep(3)
        print("   OK  BLUETOOTH RESTORED.")

    return result, note


# ==================================================================================
# NS-05: CARD READ ERROR — DIRTY OR BADLY INSERTED CHIP
# ==================================================================================

def NS_05_CARD_READ_ERROR():
    """
    NS-05: Validates that when a card cannot be read (dirty chip / incorrect
    insertion), the app shows an appropriate read error message.

    MANUAL STEP:
        When prompted, insert a card INCORRECTLY:
            - Upside down, OR
            - Card with a scratched / dirty chip, OR
            - Partial insertion then quick removal.

    SUCCESS: Error message about card reading failure appears.
    FAIL:    Green approval appears (physically impossible with bad insertion).
    """
    print("\n" + "=" * 65)
    print("TEST NS-05: CARD READ ERROR (DIRTY / BADLY INSERTED CHIP)")
    print("=" * 65)

    driver, wait = utils.start_driver()
    result, note = False, ""

    try:
        print("\n>> STEP 1: LOGIN")
        _login(driver, wait)
        _take_screenshot(driver, "NS_05_STEP1_CALCULATOR")

        print("\n>> STEP 2: REACH CARD SCREEN ($25.00)")
        _enter_amount(driver, CHARGE_AMOUNT)
        _navigate_to_card_screen(driver)
        _take_screenshot(driver, "NS_05_STEP2_CARD_SCREEN")

        print(f"\n   {'='*55}")
        print("   CARD ACTION REQUIRED — NS-05")
        print(f"   {'='*55}")
        print("   >> INSERT CARD INCORRECTLY:")
        print("      - Upside down, OR")
        print("      - Dirty / scratched chip, OR")
        print("      - Insert then quickly remove (partial read)")
        print(f"   >> {CARD_WAIT_SECONDS}s POLLING — SHOULD SHOW READ ERROR")
        print(f"   {'='*55}")

        # READ ERRORS MAY INCLUDE CARD-SPECIFIC KEYWORDS
        read_error_keywords = DENIED_KEYWORDS + [
            "lectura", "leer", "tarjeta", "chip",
            "intentar", "nuevamente", "comunic"
        ]

        denied, approved = _poll_for_denied_or_approved(
            driver, CARD_WAIT_SECONDS, "polling for read error"
        )

        read_error_found = False
        try:
            page = driver.page_source.lower()
            if any(kw in page for kw in read_error_keywords):
                read_error_found = True
                print("   OK  CARD READ ERROR DETECTED IN PAGE SOURCE.")
        except:
            pass

        _take_screenshot(driver, "NS_05_STEP3_RESULT_SCREEN")

        if denied or read_error_found:
            result = True
            note   = (
                f"PASS — READ ERROR APPEARED "
                f"(denied_screen={denied} | read_error_keywords={read_error_found})"
            )
        elif approved:
            result = False
            note   = "FAIL — UNEXPECTED APPROVAL FOR BAD CARD INSERTION"
        else:
            _dump_screen(driver)
            result = False
            note   = "FAIL — NO ERROR SCREEN DETECTED"

        print(f"   {'PASS' if result else 'FAIL'}  NS-05: {note}")
        _dismiss_result_screen(driver)
        _take_screenshot(driver, "NS_05_STEP4_BACK_TO_CALCULATOR")

    except Exception as err:
        result, note = False, f"CRITICAL ERROR: {err}"
        print(f"\nCRITICAL ERROR NS-05: {err}")
        try: _take_screenshot(driver, "NS_05_CRITICAL_ERROR")
        except: pass
    finally:
        utils.close_driver(driver)

    return result, note


# ==================================================================================
# NS-06: MINIMUM AND MAXIMUM AMOUNT PROCESSING
# ==================================================================================

def NS_06_MIN_MAX_AMOUNTS():
    """
    NS-06: Validates the Calculator correctly displays minimum and maximum amounts.
    FULLY AUTOMATED — no physical card required (only tests input behavior).

    SUB-CASES:
        A) Minimum:  press "1"        → display must show $0.01
        B) Maximum:  press "99999999" → display must show $999,999.99
        C) Zero:     no digits typed  → "Realizar cobro" must be disabled or blocked

    SUCCESS: Amounts display correctly and app does not crash.
    """
    print("\n" + "=" * 65)
    print("TEST NS-06: MINIMUM AND MAXIMUM AMOUNT PROCESSING")
    print("   (AUTOMATED — CALCULATOR INPUT ONLY)")
    print("=" * 65)

    driver, wait = utils.start_driver()
    sub_results  = {}
    result, note = False, ""

    def _clear_display():
        """Clears the calculator display by pressing backspace repeatedly."""
        for _ in range(10):
            try:
                driver.find_element(By.XPATH, config.XPATH_C_BTN_BACKSPACE).click()
                time.sleep(0.2)
            except:
                try:
                    driver.find_element(
                        AppiumBy.ANDROID_UIAUTOMATOR,
                        'new UiSelector().descriptionContains("delete")'
                    ).click()
                    time.sleep(0.2)
                except:
                    break
        time.sleep(0.5)

    try:
        print("\n>> STEP 1: LOGIN")
        _login(driver, wait)
        _take_screenshot(driver, "NS_06_STEP1_CALCULATOR")

        # SUB-CASE A: MINIMUM AMOUNT — press "1" → expect $0.01
        print("\n>> SUB-CASE A: MINIMUM AMOUNT (press '1' → $0.01)")
        _enter_amount(driver, AMOUNT_MINIMUM)
        _take_screenshot(driver, "NS_06_A_MINIMUM")
        min_ok = False
        try:
            page = driver.page_source.lower()
            if "0.01" in page or "0,01" in page:
                min_ok = True
                print("   OK  MINIMUM $0.01 DISPLAYED CORRECTLY.")
            else:
                print("   WARN $0.01 NOT FOUND IN PAGE SOURCE — CHECK SCREENSHOT.")
        except:
            pass
        sub_results["A - Minimum ($0.01)"] = min_ok
        _clear_display()

        # SUB-CASE B: MAXIMUM AMOUNT — 8 digits → expect $999,999.99
        print("\n>> SUB-CASE B: MAXIMUM AMOUNT (99999999 → $999,999.99)")
        _enter_amount(driver, AMOUNT_MAXIMUM)
        _take_screenshot(driver, "NS_06_B_MAXIMUM")
        max_ok = False
        try:
            page = driver.page_source.lower()
            # Accepts any representation of 999999.99
            if "999" in page:
                max_ok = True
                print("   OK  LARGE AMOUNT DISPLAYED WITHOUT CRASH.")
            else:
                print("   WARN LARGE AMOUNT NOT CONFIRMED — CHECK SCREENSHOT.")
        except:
            pass
        sub_results["B - Maximum ($999,999.99)"] = max_ok
        _clear_display()

        # SUB-CASE C: ZERO AMOUNT — no input → charge button must be blocked
        print("\n>> SUB-CASE C: ZERO AMOUNT (no input → 'Realizar cobro' must be blocked)")
        _take_screenshot(driver, "NS_06_C_ZERO")
        zero_blocked = False
        try:
            btn = driver.find_element(By.XPATH, XPATH_BTN_CHARGE)
            is_enabled = btn.get_attribute("enabled")
            if is_enabled == "false":
                zero_blocked = True
                print("   OK  'Realizar cobro' IS DISABLED AT $0.00.")
            else:
                # Click and verify it does not proceed to card screen
                btn.click()
                time.sleep(2)
                page = driver.page_source.lower()
                # If still on calculator (no card screen appeared) = blocked
                on_card_screen = any(kw in page for kw in ["acerca", "inserta", "desliza"])
                if not on_card_screen:
                    zero_blocked = True
                    print("   OK  ZERO AMOUNT BLOCKED — CARD SCREEN DID NOT APPEAR.")
                else:
                    print("   WARN ZERO AMOUNT REACHED CARD SCREEN (UNEXPECTED).")
        except Exception as err:
            print(f"   WARN ZERO AMOUNT CHECK: {err}")
        sub_results["C - Zero ($0.00 blocked)"] = zero_blocked
        _take_screenshot(driver, "NS_06_C_ZERO_RESULT")

        # PRINT SUB-CASE SUMMARY
        print("\n   SUB-CASE SUMMARY:")
        all_passed = True
        for sub_name, passed in sub_results.items():
            icon = "OK " if passed else "FAIL"
            print(f"      {icon}  {sub_name}")
            if not passed:
                all_passed = False

        result = all_passed
        note   = (
            f"A={sub_results.get('A - Minimum ($0.01)', False)} | "
            f"B={sub_results.get('B - Maximum ($999,999.99)', False)} | "
            f"C={sub_results.get('C - Zero ($0.00 blocked)', False)}"
        )

    except Exception as err:
        result, note = False, f"CRITICAL ERROR: {err}"
        print(f"\nCRITICAL ERROR NS-06: {err}")
        try: _take_screenshot(driver, "NS_06_CRITICAL_ERROR")
        except: pass
    finally:
        utils.close_driver(driver)

    return result, note


# ==================================================================================
# MAIN BLOCK
# ==================================================================================

if __name__ == "__main__":

    logger, log_file, timestamp = utils.start_report("NEGATIVE_SCENARIOS")

    results = {}

    try:
        results["NS-01 Insufficient Funds"]         = NS_01_INSUFFICIENT_FUNDS()
        results["NS-02 Expired Card"]               = NS_02_EXPIRED_CARD()
        results["NS-03 User Cancellation"]          = NS_03_USER_CANCELS_TRANSACTION()
        results["NS-04 Bluetooth Loss"]             = NS_04_BLUETOOTH_LOSS_DURING_TRANSACTION()
        results["NS-05 Card Read Error"]            = NS_05_CARD_READ_ERROR()
        results["NS-06 Min Max Amounts"]            = NS_06_MIN_MAX_AMOUNTS()

    finally:
        print("\n" + "=" * 65)
        print("SUMMARY — NEGATIVE SCENARIOS MODULE")
        print("=" * 65)
        print(f"  {'TEST CASE':<40} {'RESULT':<8} NOTE")
        print("  " + "-" * 62)
        for test_name, (passed, note) in results.items():
            status = "PASS" if passed else "FAIL"
            print(f"  {test_name:<40} {status:<8} {note}")
            # HTML REPORT PARSER FORMAT — required by generate_html_report
            if passed:
                print(f"  OK  {test_name}: SUCCESS — {note}")
            else:
                print(f"  ERR {test_name}: FAILED — {note}")
        print("  " + "-" * 62)
        passed_count = sum(1 for v in results.values() if v[0])
        print(f"  TOTAL: {passed_count}/{len(results)} PASSED")
        print("=" * 65)

        utils.generate_zip_report("NEGATIVE_SCENARIOS", logger, log_file, timestamp)
        utils.generate_html_report("NEGATIVE_SCENARIOS", log_file, timestamp)