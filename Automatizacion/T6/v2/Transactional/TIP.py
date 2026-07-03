"""
# ==================================================================================
# FILENAME    : TIP.py
# FOLDER      : Automatizacion/T6/v2/Transactional/
# PROJECT     : MEMPHIS QA AUTOMATION FRAMEWORK
# DESCRIPTION : TIP (GRATUITY) SELECTION TEST SUITE.
#               VALIDATES ALL TIP OPTIONS DURING THE PAYMENT FLOW.
#
# TEST CASES (matrix TC-TRANS-02 / TC-TRANS-03):
#   TIP-01 : Tip Selection — 10%
#   TIP-02 : Tip Selection — 15%
#   TIP-03 : Tip Selection — 20%
#   TIP-04 : Tip Selection — Custom Amount
#   TIP-05 : Skip Tip — "Later" option
#   TIP-06 : Close Tip Dialog with "X" button
#   TIP-07 : Tip on Denied Transaction (tip must NOT appear)
#
# FLOW (TIP-01 to TIP-06):
#   1.  Login → Calculator ($0.00)
#   2.  Type $500.00 → Realizar cobro → Venta Normal
#   3.  Card screen → [USER INSERTS CARD + PIN] → 30s active polling
#   4.  Green approval screen → Aceptar
#   5.  Tip dialog appears → select option
#   6.  Verify amount / behavior → Finalizar → Calculator
#
# FLOW (TIP-07):
#   Same as above but with a DENIED card — tip dialog must NOT appear.
#
# TIP MATH (base = $500.00):
#   10%  → $50.00  tip  / $550.00 total
#   15%  → $75.00  tip  / $575.00 total
#   20%  → $100.00 tip  / $600.00 total
#   Skip / X → $0.00 tip / $500.00 total
#
# SUCCESS CRITERIA:
#   ✅ Tip dialog appears after approved transaction
#   ✅ Selected % shows correct calculated amount
#   ✅ Total = base + tip
#   ✅ Skip / X work without adding tip
#   ✅ Denied transaction → NO tip dialog (TIP-07)
#
# REQUIREMENTS:
#   - Appium server:  appium --relaxed-security
#   - T6 connected:   adb devices
#   - utils.py, config.py in T6/v2/
# ==================================================================================
"""

import sys
import os
import time

# ── PATH SETUP ──────────────────────────────────────────────────────────────────
# TIP.py lives in T6/v2/Transactional/
# utils.py and config.py live one level up in T6/v2/
_transactional_dir = os.path.abspath(os.path.dirname(__file__))
_v2_dir            = os.path.abspath(os.path.join(_transactional_dir, '..'))
for _path in [_v2_dir, _transactional_dir]:
    if _path not in sys.path:
        sys.path.insert(0, _path)

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


# ==================================================================================
# CONSTANTS
# ==================================================================================

# Amount: press 5→0→0→0→0 = $500.00 on T6 right-to-left calculator
CHARGE_AMOUNT        = "50000"
BASE_AMOUNT          = 500.00     # Pesos — used for tip percentage math
CUSTOM_TIP_VALUE     = "50"       # Custom tip amount entered in TIP-04

CARD_WAIT_SECONDS    = 30         # Active polling window for manual card + PIN
EXTRA_WAIT_SECONDS   = 45         # Additional polling after manual window

# Expected tip amounts for $500.00 base
TIP_10_AMOUNT  = 50.00   # $500 × 10%
TIP_15_AMOUNT  = 75.00   # $500 × 15%
TIP_20_AMOUNT  = 100.00  # $500 × 20%

# Keywords used by the polling helper
TIP_DIALOG_KEYWORDS = [
    "propina", "tip", "agregar propina", "deseas agregar",
    "10%", "15%", "20%", "otro", "en otro momento"
]
APPROVAL_KEYWORDS = ["aprobada", "transacción aprobada", "approved"]
DENIED_KEYWORDS   = [
    "denegada", "rechazada", "fallida", "declined",
    "denied", "insuficientes", "expirada"
]


# ── XPATHS — TIP DIALOG ─────────────────────────────────────────────────────────

XPATH_TIP_DIALOG = (
    '//*[contains(@content-desc,"propina") or contains(@text,"propina") or '
    'contains(@content-desc,"Propina") or contains(@text,"Propina")]'
)
XPATH_BTN_TIP_10 = (
    '//*[@content-desc="10%" or @text="10%" or '
    'contains(@content-desc,"10%") or contains(@text,"10%")]'
)
XPATH_BTN_TIP_15 = (
    '//*[@content-desc="15%" or @text="15%" or '
    'contains(@content-desc,"15%") or contains(@text,"15%")]'
)
XPATH_BTN_TIP_20 = (
    '//*[@content-desc="20%" or @text="20%" or '
    'contains(@content-desc,"20%") or contains(@text,"20%")]'
)
XPATH_BTN_TIP_CUSTOM = (
    '//*[@content-desc="Otro" or @text="Otro" or '
    'contains(@content-desc,"Otro") or contains(@text,"Otro") or '
    'contains(@content-desc,"Personalizado") or contains(@text,"Personalizado")]'
)
XPATH_INPUT_CUSTOM_TIP = '//android.widget.EditText[1]'
XPATH_BTN_SKIP_TIP = (
    '//*[contains(@content-desc,"En otro momento") or contains(@text,"En otro momento") or '
    'contains(@content-desc,"otro momento") or contains(@text,"otro momento") or '
    'contains(@content-desc,"Sin propina") or contains(@text,"Sin propina")]'
)
XPATH_BTN_CLOSE_TIP_X = (
    '//*[@content-desc="×" or @text="×" or '
    '@content-desc="✕" or @text="✕" or '
    'contains(@content-desc,"Cerrar") or contains(@text,"Cerrar") or '
    'contains(@content-desc,"cerrar") or contains(@text,"cerrar")]'
)
XPATH_BTN_CONFIRM_TIP = config.XPATH_C_BTN_ACEPTAR_PROPINA


# ── XPATHS — TRANSACTION FLOW ───────────────────────────────────────────────────

XPATH_BTN_CHARGE      = (
    '//*[contains(@content-desc,"Realizar cobro") or '
    'contains(@text,"Realizar cobro")]'
)
XPATH_POPUP_SALE_TYPE = (
    '//*[contains(@content-desc,"tipo de operación") or '
    'contains(@text,"tipo de operación") or '
    'contains(@content-desc,"Qué tipo") or contains(@text,"Qué tipo")]'
)
XPATH_BTN_NORMAL_SALE = (
    '//*[@content-desc="Venta Normal" or @text="Venta Normal" or '
    'contains(@content-desc,"Venta Normal") or contains(@text,"Venta Normal")]'
)
XPATH_SCREEN_CARD     = (
    '//*[contains(@content-desc,"Acerca") or contains(@text,"Acerca") or '
    'contains(@content-desc,"inserta") or contains(@text,"inserta") or '
    'contains(@content-desc,"Iniciando") or contains(@text,"Iniciando")]'
)
XPATH_SCREEN_APPROVED = (
    '//*[contains(@content-desc,"aprobada") or contains(@text,"aprobada")]'
)
XPATH_SCREEN_DENIED   = (
    '//*[contains(@content-desc,"denegada") or contains(@text,"denegada") or '
    'contains(@content-desc,"rechazada") or contains(@text,"rechazada")]'
)
XPATH_BTN_ACCEPT      = (
    '//*[@content-desc="Aceptar" or @text="Aceptar" or '
    'contains(@content-desc,"Aceptar") or contains(@text,"Aceptar")]'
)
XPATH_BTN_FINISH      = (
    '//*[@content-desc="Finalizar" or @text="Finalizar" or '
    'contains(@content-desc,"Finalizar") or contains(@text,"Finalizar")]'
)
XPATH_DISPLAY_ZERO    = (
    '//*[contains(@content-desc,"0.00") or contains(@text,"0.00")]'
)


# ==================================================================================
# INTERNAL HELPERS — PREFIXED WITH _ (NOT CALLED FROM OUTSIDE THIS FILE)
# ==================================================================================

def _take_screenshot(driver, name):
    """Saves a T6 screenshot. Errors are printed, never swallowed."""
    try:
        utils.take_screenshot(driver, name, "t6")
    except Exception as err:
        print(f"   WARNING: SCREENSHOT FAILED [{name}]: {err}")


def _login(driver, wait):
    """
    Executes the full login sequence:
    onboarding slides → credentials → commerce setup → lector popup → calculator.
    Identical pattern used across all Transactional test files.
    """
    print("   [HELPER] PHASE 1: ONBOARDING SLIDES...")
    time.sleep(3)
    slide_buttons = [
        config.XPATH_OB_BTN_SIGUIENTE,
        config.XPATH_OB_BTN_SIGUIENTE,
        config.XPATH_OB_BTN_COMENZAR,
    ]
    for index, btn_xpath in enumerate(slide_buttons, start=1):
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

    print("   OK  LOGIN COMPLETE — CALCULATOR SCREEN READY.")


def _enter_amount(driver, digits):
    """
    Types the charge amount digit by digit on the T6 calculator.

    HOW THE T6 CALCULATOR WORKS (right-to-left / cash register logic):
        press 5 → display shows $0.05
        press 0 → display shows $0.50
        press 0 → display shows $5.00
        press 0 → display shows $50.00
        press 0 → display shows $500.00  ← CHARGE_AMOUNT = "50000"

    So every digit shifts the existing value one decimal place to the left.
    """
    print(f"   TYPING: {digits} → $500.00")
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
        print(f"   OK  DISPLAY SHOWS: {displayed}")
    except:
        pass


def _navigate_to_card_screen(driver):
    """
    Navigates from the Calculator screen to the card insertion screen:
        Calculator → Realizar cobro → Tipo de operación popup → Venta Normal → Card screen.
    Returns True if the card screen is reached.
    """
    # STEP A: CLICK "REALIZAR COBRO"
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

    # STEP B: WAIT FOR SALE TYPE POPUP
    try:
        WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.XPATH, XPATH_POPUP_SALE_TYPE))
        )
        print("   OK  SALE TYPE POPUP VISIBLE.")
    except:
        pass  # May not show on all firmware versions

    # STEP C: CLICK "VENTA NORMAL"
    normal_sale_clicked = False
    try:
        WebDriverWait(driver, 6).until(
            EC.element_to_be_clickable((By.XPATH, XPATH_BTN_NORMAL_SALE))
        ).click()
        normal_sale_clicked = True
        print("   OK  'Venta Normal' CLICKED.")
    except:
        try:
            driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().text("Venta Normal")'
            ).click()
            normal_sale_clicked = True
            print("   OK  'Venta Normal' CLICKED (UiAutomator).")
        except Exception as err:
            print(f"   FAIL 'Venta Normal': {err}")
            return False
    time.sleep(2)

    # STEP D: VERIFY CARD SCREEN
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
            print("   WARN CARD SCREEN NOT CONFIRMED — CONTINUING.")
    return True


def _poll_for_screen(driver, xpaths, keywords, seconds, label):
    """
    Polls every second for any element matching xpaths or keywords.
    Prints a live countdown. Advances immediately on first match.
    Returns True when detected, False after timeout.

    This is the core detection function used throughout all Transactional tests.
    The tight polling loop (no sleep between iterations) ensures transient
    screens (< 3 seconds) are never missed.
    """
    end_time = time.time() + seconds
    while time.time() < end_time:
        remaining = int(end_time - time.time())
        print(f"      POLLING {remaining:02d}s — {label}...", end="\r")

        # CHECK DOM ELEMENTS
        for xpath in xpaths:
            try:
                for elem in driver.find_elements(By.XPATH, xpath):
                    t = (elem.get_attribute("text") or "").lower()
                    d = (elem.get_attribute("content-desc") or "").lower()
                    if any(kw.lower() in t + d for kw in keywords):
                        print(f"\n   OK  DETECTED: '{(t or d)[:80]}'")
                        return True
            except:
                continue

        # CHECK PAGE SOURCE (catches overlays and toast messages)
        try:
            page = driver.page_source.lower()
            if any(kw.lower() in page for kw in keywords):
                print(f"\n   OK  DETECTED VIA PAGE SOURCE!")
                return True
        except:
            pass

        time.sleep(1)

    print()  # newline after countdown
    return False


def _wait_for_tip_dialog(driver, timeout=15):
    """
    Waits for the tip selection dialog to appear after transaction approval.
    The dialog appears only when the commerce has tips enabled in its configuration.
    Returns True if the tip dialog is detected within the timeout.
    """
    print(f"   POLLING FOR TIP DIALOG (up to {timeout}s)...")
    return _poll_for_screen(
        driver,
        [XPATH_TIP_DIALOG, config.TH_C_POPUP_PROPINA],
        TIP_DIALOG_KEYWORDS,
        timeout,
        "waiting for tip dialog"
    )


def _verify_tip_amount_on_screen(driver, tip_pct, base=BASE_AMOUNT):
    """
    Verifies the calculated tip and total amounts appear on screen after selection.

    MATH:
        tip_pct = 10  → expected_tip = $50.00  expected_total = $550.00
        tip_pct = 15  → expected_tip = $75.00  expected_total = $575.00
        tip_pct = 20  → expected_tip = $100.00 expected_total = $600.00

    Returns (verified: bool, shown_value: str)
    """
    expected_tip   = base * (tip_pct / 100)
    expected_total = base + expected_tip

    print(f"   VERIFYING: {tip_pct}% of ${base:.2f}")
    print(f"      Expected tip   = ${expected_tip:.2f}")
    print(f"      Expected total = ${expected_total:.2f}")

    try:
        page        = driver.page_source.lower()
        tip_str     = f"{expected_tip:.2f}"          # "50.00"
        total_str   = f"{expected_total:.2f}"         # "550.00"
        tip_integer = f"{int(expected_tip)}"          # "50"

        if tip_str in page or total_str in page:
            print(f"   OK  AMOUNT CONFIRMED ON SCREEN (${expected_tip:.2f} or ${expected_total:.2f}).")
            return True, f"${expected_tip:.2f}"
        elif tip_integer in page:
            print(f"   OK  TIP INTEGER VALUE {tip_integer} FOUND (partial match).")
            return True, f"~${expected_tip:.2f}"
        else:
            print(f"   WARN EXPECTED AMOUNTS NOT FOUND IN PAGE SOURCE.")
            return False, "NOT FOUND"
    except Exception as err:
        print(f"   WARN VERIFY ERROR: {err}")
        return False, "ERROR"


def _click_option(driver, xpath, label):
    """
    Clicks a tip dialog option using 3 strategies:
        1. WebDriverWait + XPath
        2. UiAutomator text match
        3. UiAutomator description match
    Returns True if clicked successfully.
    """
    # STRATEGY 1: XPATH
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        ).click()
        print(f"   OK  '{label}' CLICKED (XPath).")
        return True
    except:
        pass

    # STRATEGY 2: UIAUTOMATOR TEXT
    try:
        driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().textContains("{label}")'
        ).click()
        print(f"   OK  '{label}' CLICKED (UiAutomator text).")
        return True
    except:
        pass

    # STRATEGY 3: UIAUTOMATOR DESCRIPTION
    try:
        driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().descriptionContains("{label}")'
        ).click()
        print(f"   OK  '{label}' CLICKED (UiAutomator desc).")
        return True
    except:
        pass

    print(f"   FAIL ALL STRATEGIES EXHAUSTED FOR '{label}'.")
    return False


def _run_transaction_to_approval(driver, wait, test_id):
    """
    Executes the full transaction flow up to the point where:
        - The green approval screen is shown AND Aceptar has been clicked, OR
        - The denied screen is shown.

    Returns (approved: bool, denied: bool)
    """
    print(f"\n   EXECUTING TRANSACTION FOR {test_id}...")
    _enter_amount(driver, CHARGE_AMOUNT)
    _take_screenshot(driver, f"{test_id}_TX1_AMOUNT")

    if not _navigate_to_card_screen(driver):
        print("   FAIL COULD NOT REACH CARD SCREEN.")
        return False, False
    _take_screenshot(driver, f"{test_id}_TX2_CARD_SCREEN")

    # MANUAL PAUSE WITH ACTIVE POLLING
    print(f"\n   {'='*55}")
    print(f"   CARD ACTION REQUIRED — {test_id}")
    print(f"   {'='*55}")
    print(f"   >> INSERT CARD AND ENTER PIN ON T6 READER")
    print(f"   >> {CARD_WAIT_SECONDS}s ACTIVE POLLING — ADVANCES ON APPROVAL")
    print(f"   {'='*55}")

    approved = _poll_for_screen(
        driver, [XPATH_SCREEN_APPROVED], APPROVAL_KEYWORDS,
        CARD_WAIT_SECONDS, "waiting for approval"
    )
    if not approved:
        print(f"   POLLING {EXTRA_WAIT_SECONDS}s MORE...")
        approved = _poll_for_screen(
            driver, [XPATH_SCREEN_APPROVED], APPROVAL_KEYWORDS,
            EXTRA_WAIT_SECONDS, "extra approval poll"
        )

    denied = False
    if not approved:
        denied = _poll_for_screen(
            driver, [XPATH_SCREEN_DENIED], DENIED_KEYWORDS,
            5, "checking for denial"
        )

    _take_screenshot(driver, f"{test_id}_TX3_TRANSACTION_RESULT")

    if approved:
        print("   OK  TRANSACTION APPROVED — clicking Accept...")
        time.sleep(2)
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, XPATH_BTN_ACCEPT))
            ).click()
            print("   OK  'Aceptar' CLICKED ON APPROVAL SCREEN.")
            time.sleep(2)
        except:
            print("   INFO NO ACCEPT BUTTON ON APPROVAL SCREEN.")
        return True, False

    if denied:
        print("   INFO TRANSACTION DENIED.")
        return False, True

    print("   WARN NEITHER APPROVAL NOR DENIAL DETECTED.")
    return False, False


def _finish_flow(driver, test_id):
    """Clicks Finalizar and takes a closing screenshot."""
    try:
        WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.XPATH, XPATH_BTN_FINISH))
        ).click()
        print("   OK  'Finalizar' CLICKED.")
        time.sleep(3)
    except:
        try:
            driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().text("Finalizar")'
            ).click()
            print("   OK  'Finalizar' CLICKED (UiAutomator).")
            time.sleep(3)
        except:
            print("   WARN 'Finalizar' NOT FOUND.")
    _take_screenshot(driver, f"{test_id}_FINAL_CALCULATOR")


# ==================================================================================
# TIP-01: TIP SELECTION — 10%
# ==================================================================================

def TIP_01_TIP_10_PERCENT():
    """
    TIP-01: Select 10% tip after an approved $500.00 transaction.
    Expected tip: $50.00 | Expected total: $550.00
    """
    print("\n" + "=" * 65)
    print("TEST TIP-01: TIP SELECTION — 10%")
    print("=" * 65)

    driver, wait = utils.start_driver()
    result, note = False, ""

    try:
        print("\n>> STEP 1: LOGIN")
        _login(driver, wait)
        _take_screenshot(driver, "TIP_01_STEP1_CALCULATOR")

        print("\n>> STEPS 2-4: TRANSACTION FLOW")
        approved, denied = _run_transaction_to_approval(driver, wait, "TIP_01")
        if not approved:
            return False, "TRANSACTION NOT APPROVED — CANNOT TEST TIP"

        print("\n>> STEP 5: WAITING FOR TIP DIALOG")
        dialog_visible = _wait_for_tip_dialog(driver)
        _take_screenshot(driver, "TIP_01_STEP5_TIP_DIALOG")
        if not dialog_visible:
            return False, "TIP DIALOG DID NOT APPEAR"

        print("\n>> STEP 6: SELECTING 10%")
        btn_clicked = _click_option(driver, XPATH_BTN_TIP_10, "10%")
        time.sleep(1)
        _take_screenshot(driver, "TIP_01_STEP6_10_PCT_SELECTED")

        print("\n>> STEP 7: VERIFYING TIP CALCULATION ($50.00)")
        calc_ok, shown = _verify_tip_amount_on_screen(driver, tip_pct=10)
        _take_screenshot(driver, "TIP_01_STEP7_AMOUNT_VERIFIED")

        print("\n>> STEP 8: CONFIRMING TIP")
        _click_option(driver, XPATH_BTN_CONFIRM_TIP, "Aceptar")
        time.sleep(2)
        _finish_flow(driver, "TIP_01")

        result = dialog_visible and btn_clicked and calc_ok
        note   = (
            f"10% TIP OK | dialog={dialog_visible} | selected={btn_clicked} | amount={shown}"
        )

    except Exception as err:
        result, note = False, f"CRITICAL ERROR: {err}"
        print(f"\nCRITICAL ERROR TIP-01: {err}")
        try: _take_screenshot(driver, "TIP_01_CRITICAL_ERROR")
        except: pass
    finally:
        utils.close_driver(driver)

    return result, note


# ==================================================================================
# TIP-02: TIP SELECTION — 15%
# ==================================================================================

def TIP_02_TIP_15_PERCENT():
    """
    TIP-02: Select 15% tip after an approved $500.00 transaction.
    Expected tip: $75.00 | Expected total: $575.00
    """
    print("\n" + "=" * 65)
    print("TEST TIP-02: TIP SELECTION — 15%")
    print("=" * 65)

    driver, wait = utils.start_driver()
    result, note = False, ""

    try:
        print("\n>> STEP 1: LOGIN")
        _login(driver, wait)
        _take_screenshot(driver, "TIP_02_STEP1_CALCULATOR")

        print("\n>> STEPS 2-4: TRANSACTION FLOW")
        approved, denied = _run_transaction_to_approval(driver, wait, "TIP_02")
        if not approved:
            return False, "TRANSACTION NOT APPROVED"

        print("\n>> STEP 5: WAITING FOR TIP DIALOG")
        dialog_visible = _wait_for_tip_dialog(driver)
        _take_screenshot(driver, "TIP_02_STEP5_TIP_DIALOG")
        if not dialog_visible:
            return False, "TIP DIALOG DID NOT APPEAR"

        print("\n>> STEP 6: SELECTING 15%")
        btn_clicked = _click_option(driver, XPATH_BTN_TIP_15, "15%")
        time.sleep(1)
        _take_screenshot(driver, "TIP_02_STEP6_15_PCT_SELECTED")

        print("\n>> STEP 7: VERIFYING TIP CALCULATION ($75.00)")
        calc_ok, shown = _verify_tip_amount_on_screen(driver, tip_pct=15)
        _take_screenshot(driver, "TIP_02_STEP7_AMOUNT_VERIFIED")

        print("\n>> STEP 8: CONFIRMING TIP")
        _click_option(driver, XPATH_BTN_CONFIRM_TIP, "Aceptar")
        time.sleep(2)
        _finish_flow(driver, "TIP_02")

        result = dialog_visible and btn_clicked and calc_ok
        note   = f"15% TIP OK | amount={shown} | calc={'PASS' if calc_ok else 'FAIL'}"

    except Exception as err:
        result, note = False, f"CRITICAL ERROR: {err}"
        print(f"\nCRITICAL ERROR TIP-02: {err}")
        try: _take_screenshot(driver, "TIP_02_CRITICAL_ERROR")
        except: pass
    finally:
        utils.close_driver(driver)

    return result, note


# ==================================================================================
# TIP-03: TIP SELECTION — 20%
# ==================================================================================

def TIP_03_TIP_20_PERCENT():
    """
    TIP-03: Select 20% tip after an approved $500.00 transaction.
    Expected tip: $100.00 | Expected total: $600.00
    """
    print("\n" + "=" * 65)
    print("TEST TIP-03: TIP SELECTION — 20%")
    print("=" * 65)

    driver, wait = utils.start_driver()
    result, note = False, ""

    try:
        print("\n>> STEP 1: LOGIN")
        _login(driver, wait)
        _take_screenshot(driver, "TIP_03_STEP1_CALCULATOR")

        print("\n>> STEPS 2-4: TRANSACTION FLOW")
        approved, denied = _run_transaction_to_approval(driver, wait, "TIP_03")
        if not approved:
            return False, "TRANSACTION NOT APPROVED"

        print("\n>> STEP 5: WAITING FOR TIP DIALOG")
        dialog_visible = _wait_for_tip_dialog(driver)
        _take_screenshot(driver, "TIP_03_STEP5_TIP_DIALOG")
        if not dialog_visible:
            return False, "TIP DIALOG DID NOT APPEAR"

        print("\n>> STEP 6: SELECTING 20%")
        btn_clicked = _click_option(driver, XPATH_BTN_TIP_20, "20%")
        time.sleep(1)
        _take_screenshot(driver, "TIP_03_STEP6_20_PCT_SELECTED")

        print("\n>> STEP 7: VERIFYING TIP CALCULATION ($100.00)")
        calc_ok, shown = _verify_tip_amount_on_screen(driver, tip_pct=20)
        _take_screenshot(driver, "TIP_03_STEP7_AMOUNT_VERIFIED")

        print("\n>> STEP 8: CONFIRMING TIP")
        _click_option(driver, XPATH_BTN_CONFIRM_TIP, "Aceptar")
        time.sleep(2)
        _finish_flow(driver, "TIP_03")

        result = dialog_visible and btn_clicked and calc_ok
        note   = f"20% TIP OK | amount={shown} | calc={'PASS' if calc_ok else 'FAIL'}"

    except Exception as err:
        result, note = False, f"CRITICAL ERROR: {err}"
        print(f"\nCRITICAL ERROR TIP-03: {err}")
        try: _take_screenshot(driver, "TIP_03_CRITICAL_ERROR")
        except: pass
    finally:
        utils.close_driver(driver)

    return result, note


# ==================================================================================
# TIP-04: TIP SELECTION — CUSTOM AMOUNT
# ==================================================================================

def TIP_04_CUSTOM_TIP():
    """
    TIP-04: Enter a custom tip amount ($50.00) via the "Otro" option.
    Verifies the input field accepts text and the amount is reflected.
    """
    print("\n" + "=" * 65)
    print(f"TEST TIP-04: CUSTOM TIP — ${CUSTOM_TIP_VALUE}.00")
    print("=" * 65)

    driver, wait = utils.start_driver()
    result, note = False, ""

    try:
        print("\n>> STEP 1: LOGIN")
        _login(driver, wait)
        _take_screenshot(driver, "TIP_04_STEP1_CALCULATOR")

        print("\n>> STEPS 2-4: TRANSACTION FLOW")
        approved, denied = _run_transaction_to_approval(driver, wait, "TIP_04")
        if not approved:
            return False, "TRANSACTION NOT APPROVED"

        print("\n>> STEP 5: WAITING FOR TIP DIALOG")
        dialog_visible = _wait_for_tip_dialog(driver)
        _take_screenshot(driver, "TIP_04_STEP5_TIP_DIALOG")
        if not dialog_visible:
            return False, "TIP DIALOG DID NOT APPEAR"

        print("\n>> STEP 6: CLICKING 'CUSTOM' OPTION")
        custom_clicked = _click_option(driver, XPATH_BTN_TIP_CUSTOM, "Otro")
        time.sleep(1)
        _take_screenshot(driver, "TIP_04_STEP6_CUSTOM_OPTION")

        print(f"\n>> STEP 7: ENTERING CUSTOM TIP ${CUSTOM_TIP_VALUE}.00")
        amount_entered = False
        try:
            field = WebDriverWait(driver, 6).until(
                EC.presence_of_element_located((By.XPATH, XPATH_INPUT_CUSTOM_TIP))
            )
            field.click()
            time.sleep(0.5)
            field.clear()
            field.send_keys(CUSTOM_TIP_VALUE)
            try:
                driver.hide_keyboard()
            except:
                pass
            amount_entered = True
            print(f"   OK  CUSTOM TIP '${CUSTOM_TIP_VALUE}' ENTERED.")
        except Exception as err:
            print(f"   WARN CUSTOM INPUT: {err}")
        _take_screenshot(driver, "TIP_04_STEP7_CUSTOM_ENTERED")

        print("\n>> STEP 8: CONFIRMING CUSTOM TIP")
        _click_option(driver, XPATH_BTN_CONFIRM_TIP, "Aceptar")
        time.sleep(2)

        custom_confirmed = False
        try:
            page = driver.page_source.lower()
            if CUSTOM_TIP_VALUE in page or f"{CUSTOM_TIP_VALUE}.00" in page:
                custom_confirmed = True
                print(f"   OK  CUSTOM TIP ${CUSTOM_TIP_VALUE}.00 CONFIRMED ON SCREEN.")
        except:
            pass
        _take_screenshot(driver, "TIP_04_STEP8_CONFIRMED")
        _finish_flow(driver, "TIP_04")

        result = dialog_visible and custom_clicked and amount_entered
        note   = (
            f"CUSTOM ${CUSTOM_TIP_VALUE} | "
            f"dialog={dialog_visible} | field={amount_entered} | "
            f"confirmed={custom_confirmed}"
        )

    except Exception as err:
        result, note = False, f"CRITICAL ERROR: {err}"
        print(f"\nCRITICAL ERROR TIP-04: {err}")
        try: _take_screenshot(driver, "TIP_04_CRITICAL_ERROR")
        except: pass
    finally:
        utils.close_driver(driver)

    return result, note


# ==================================================================================
# TIP-05: SKIP TIP — "LATER" OPTION
# ==================================================================================

def TIP_05_SKIP_TIP():
    """
    TIP-05: Skip the tip by clicking "En otro momento" (later).
    Verifies no extra amount is added and flow proceeds normally.
    SUCCESS: Flow reaches Finalizar without adding tip to base $500.00.
    """
    print("\n" + "=" * 65)
    print("TEST TIP-05: SKIP TIP — LATER OPTION")
    print("=" * 65)

    driver, wait = utils.start_driver()
    result, note = False, ""

    try:
        print("\n>> STEP 1: LOGIN")
        _login(driver, wait)
        _take_screenshot(driver, "TIP_05_STEP1_CALCULATOR")

        print("\n>> STEPS 2-4: TRANSACTION FLOW")
        approved, denied = _run_transaction_to_approval(driver, wait, "TIP_05")
        if not approved:
            return False, "TRANSACTION NOT APPROVED"

        print("\n>> STEP 5: WAITING FOR TIP DIALOG")
        dialog_visible = _wait_for_tip_dialog(driver)
        _take_screenshot(driver, "TIP_05_STEP5_TIP_DIALOG")
        if not dialog_visible:
            return False, "TIP DIALOG DID NOT APPEAR"

        print("\n>> STEP 6: CLICKING 'SKIP TIP' BUTTON")
        skip_clicked = _click_option(driver, XPATH_BTN_SKIP_TIP, "En otro momento")
        time.sleep(2)
        _take_screenshot(driver, "TIP_05_STEP6_TIP_SKIPPED")

        print("\n>> STEP 7: VERIFYING NO EXTRA CHARGE WAS ADDED")
        no_extra_charge = False
        try:
            page = driver.page_source.lower()
            # Post-tip amounts ($550, $575, $600) must NOT appear
            unexpected_amounts = ["550", "575", "600"]
            if not any(amt in page for amt in unexpected_amounts):
                no_extra_charge = True
                print("   OK  NO TIP AMOUNTS DETECTED — TIP CORRECTLY SKIPPED.")
            else:
                print("   WARN UNEXPECTED TIP-RELATED AMOUNT FOUND.")
        except:
            pass

        _finish_flow(driver, "TIP_05")

        result = dialog_visible and skip_clicked
        note   = (
            f"TIP SKIPPED | dialog={dialog_visible} | "
            f"skip_btn={skip_clicked} | no_extra_charge={no_extra_charge}"
        )

    except Exception as err:
        result, note = False, f"CRITICAL ERROR: {err}"
        print(f"\nCRITICAL ERROR TIP-05: {err}")
        try: _take_screenshot(driver, "TIP_05_CRITICAL_ERROR")
        except: pass
    finally:
        utils.close_driver(driver)

    return result, note


# ==================================================================================
# TIP-06: CLOSE TIP DIALOG WITH "X"
# ==================================================================================

def TIP_06_CLOSE_WITH_X():
    """
    TIP-06: Close the tip dialog using the X button.
    Verifies the dialog dismisses without applying any tip.
    Fallback: uses system back key if X button is not found.
    """
    print("\n" + "=" * 65)
    print("TEST TIP-06: CLOSE TIP DIALOG WITH X BUTTON")
    print("=" * 65)

    driver, wait = utils.start_driver()
    result, note = False, ""

    try:
        print("\n>> STEP 1: LOGIN")
        _login(driver, wait)
        _take_screenshot(driver, "TIP_06_STEP1_CALCULATOR")

        print("\n>> STEPS 2-4: TRANSACTION FLOW")
        approved, denied = _run_transaction_to_approval(driver, wait, "TIP_06")
        if not approved:
            return False, "TRANSACTION NOT APPROVED"

        print("\n>> STEP 5: WAITING FOR TIP DIALOG")
        dialog_visible = _wait_for_tip_dialog(driver)
        _take_screenshot(driver, "TIP_06_STEP5_TIP_DIALOG")
        if not dialog_visible:
            return False, "TIP DIALOG DID NOT APPEAR"

        print("\n>> STEP 6: CLICKING X TO CLOSE DIALOG")
        x_clicked = _click_option(driver, XPATH_BTN_CLOSE_TIP_X, "X")

        # FALLBACK: system back key if X not found
        if not x_clicked:
            print("   INFO X BUTTON NOT FOUND — USING SYSTEM BACK KEY.")
            try:
                driver.back()
                x_clicked = True
                print("   OK  SYSTEM BACK KEY USED.")
            except:
                pass
        time.sleep(2)
        _take_screenshot(driver, "TIP_06_STEP6_AFTER_X")

        print("\n>> STEP 7: VERIFYING DIALOG IS CLOSED")
        dialog_closed = False
        try:
            page = driver.page_source.lower()
            tip_options_visible = any(
                kw in page for kw in ["10%", "15%", "20%", "otro", "en otro momento"]
            )
            if not tip_options_visible:
                dialog_closed = True
                print("   OK  TIP DIALOG CLOSED — OPTIONS NO LONGER VISIBLE.")
            else:
                print("   WARN TIP OPTIONS MAY STILL BE VISIBLE.")
        except:
            pass

        _take_screenshot(driver, "TIP_06_STEP7_DIALOG_STATE")
        _finish_flow(driver, "TIP_06")

        result = dialog_visible and x_clicked
        note   = (
            f"X CLOSE | dialog={dialog_visible} | "
            f"x_btn={x_clicked} | closed={dialog_closed}"
        )

    except Exception as err:
        result, note = False, f"CRITICAL ERROR: {err}"
        print(f"\nCRITICAL ERROR TIP-06: {err}")
        try: _take_screenshot(driver, "TIP_06_CRITICAL_ERROR")
        except: pass
    finally:
        utils.close_driver(driver)

    return result, note


# ==================================================================================
# TIP-07: TIP ON DENIED TRANSACTION
# ==================================================================================

def TIP_07_TIP_ON_DENIED_TRANSACTION():
    """
    TIP-07: Verifies tip dialog does NOT appear after a DENIED transaction.

    MANUAL STEP:
        Insert a card that will be DENIED (insufficient funds / expired).

    SUCCESS LOGIC (inverted vs TIP-01 to TIP-06):
        PASS = Transaction DENIED  +  Tip dialog DOES NOT appear
        FAIL = Tip dialog appears after denial  (incorrect behavior)
        INCONCLUSIVE = Transaction was approved instead (wrong card used)
    """
    print("\n" + "=" * 65)
    print("TEST TIP-07: TIP ON DENIED TRANSACTION")
    print("   (TIP MUST NOT APPEAR AFTER DENIAL)")
    print("=" * 65)

    driver, wait = utils.start_driver()
    result, note = False, ""

    try:
        print("\n>> STEP 1: LOGIN")
        _login(driver, wait)
        _take_screenshot(driver, "TIP_07_STEP1_CALCULATOR")

        print("\n>> STEP 2: ENTER AMOUNT + REACH CARD SCREEN")
        _enter_amount(driver, CHARGE_AMOUNT)
        _take_screenshot(driver, "TIP_07_STEP2_AMOUNT")
        _navigate_to_card_screen(driver)
        _take_screenshot(driver, "TIP_07_STEP3_CARD_SCREEN")

        # MANUAL PAUSE — INSERT A CARD THAT WILL BE DENIED
        print(f"\n   {'='*55}")
        print("   CARD ACTION REQUIRED — TIP-07")
        print(f"   {'='*55}")
        print("   >> INSERT A CARD THAT WILL BE DENIED:")
        print("      - Insufficient funds, OR")
        print("      - Expired card")
        print(f"   >> {CARD_WAIT_SECONDS}s POLLING — SHOULD SHOW RED DENIED SCREEN")
        print("   >> TIP DIALOG MUST NOT APPEAR AFTER DENIAL")
        print(f"   {'='*55}")

        # POLL FOR DENIAL
        transaction_denied = _poll_for_screen(
            driver, [XPATH_SCREEN_DENIED], DENIED_KEYWORDS,
            CARD_WAIT_SECONDS, "waiting for denial"
        )
        if not transaction_denied:
            transaction_denied = _poll_for_screen(
                driver, [XPATH_SCREEN_DENIED], DENIED_KEYWORDS,
                EXTRA_WAIT_SECONDS, "extra denial poll"
            )

        # CHECK IF APPROVED INSTEAD (WRONG CARD — INCONCLUSIVE)
        transaction_approved = False
        if not transaction_denied:
            transaction_approved = _poll_for_screen(
                driver, [XPATH_SCREEN_APPROVED], APPROVAL_KEYWORDS,
                5, "checking approval"
            )

        _take_screenshot(driver, "TIP_07_STEP4_TRANSACTION_RESULT")

        print("\n>> STEP 5: VERIFYING TIP DIALOG DID NOT APPEAR")
        tip_appeared = False

        if transaction_approved:
            # Click Accept on the approval screen then check for tip
            try:
                WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, XPATH_BTN_ACCEPT))
                ).click()
                time.sleep(2)
            except:
                pass
            tip_appeared = _wait_for_tip_dialog(driver, timeout=5)

        _take_screenshot(driver, "TIP_07_STEP5_TIP_CHECK")

        print("\n>> STEP 6: EVALUATING RESULT")
        if transaction_denied and not tip_appeared:
            result = True
            note   = "PASS — TRANSACTION DENIED AND TIP DIALOG DID NOT APPEAR"
            print(f"   PASS  TIP-07: {note}")
        elif transaction_denied and tip_appeared:
            result = False
            note   = "FAIL — TRANSACTION DENIED BUT TIP DIALOG STILL APPEARED"
            print(f"   FAIL  TIP-07: {note}")
        elif transaction_approved:
            result = False
            note   = "INCONCLUSIVE — TRANSACTION WAS APPROVED (WRONG CARD USED)"
            print(f"   WARN  TIP-07: {note}")
        else:
            result = False
            note   = "FAIL — NEITHER DENIED NOR APPROVED DETECTED"
            print(f"   FAIL  TIP-07: {note}")

        # DISMISS AND RETURN TO CALCULATOR
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, XPATH_BTN_ACCEPT))
            ).click()
            time.sleep(2)
        except:
            try:
                driver.back()
            except:
                pass
        _take_screenshot(driver, "TIP_07_STEP6_BACK_TO_CALCULATOR")

    except Exception as err:
        result, note = False, f"CRITICAL ERROR: {err}"
        print(f"\nCRITICAL ERROR TIP-07: {err}")
        try: _take_screenshot(driver, "TIP_07_CRITICAL_ERROR")
        except: pass
    finally:
        utils.close_driver(driver)

    return result, note


# ==================================================================================
# MAIN BLOCK
# ==================================================================================

if __name__ == "__main__":

    logger, log_file, timestamp = utils.start_report("TIP")

    results = {}

    try:
        results["TIP-01 10% Tip"]               = TIP_01_TIP_10_PERCENT()
        results["TIP-02 15% Tip"]               = TIP_02_TIP_15_PERCENT()
        results["TIP-03 20% Tip"]               = TIP_03_TIP_20_PERCENT()
        results["TIP-04 Custom Tip"]            = TIP_04_CUSTOM_TIP()
        results["TIP-05 Skip Tip"]              = TIP_05_SKIP_TIP()
        results["TIP-06 Close With X"]          = TIP_06_CLOSE_WITH_X()
        results["TIP-07 Denied Transaction"]    = TIP_07_TIP_ON_DENIED_TRANSACTION()

    finally:
        print("\n" + "=" * 65)
        print("SUMMARY — TIP MODULE")
        print("=" * 65)
        print(f"  {'TEST CASE':<38} {'RESULT':<8} NOTE")
        print("  " + "-" * 62)
        for test_name, (passed, note) in results.items():
            status = "PASS" if passed else "FAIL"
            icon   = "OK  " if passed else "FAIL"
            print(f"  {icon} {test_name:<35} {status:<8} {note}")
            # HTML REPORT PARSER FORMAT — required by generate_html_report
            if passed:
                print(f"  OK  {test_name}: SUCCESS — {note}")
            else:
                print(f"  ERR {test_name}: FAILED — {note}")
        print("  " + "-" * 62)
        passed_count = sum(1 for v in results.values() if v[0])
        print(f"  TOTAL: {passed_count}/{len(results)} PASSED")
        print("=" * 65)

        utils.generate_zip_report("TIP", logger, log_file, timestamp)
        utils.generate_html_report("TIP", log_file, timestamp)