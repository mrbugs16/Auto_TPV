"""
# ==================================================================================
# FILENAME    : CARD_CREDIT.py
# FOLDER      : Automatizacion/T6/v2/Transactional/
# PROJECT     : MEMPHIS QA AUTOMATION FRAMEWORK
# DESCRIPTION : CREDIT CARD PAYMENT TEST SUITE — VALIDATES END-TO-END
#               PAYMENT FLOW FOR 5 DIFFERENT CREDIT CARDS:
#                 - CT-01 : Crédito Nu
#                 - CT-02 : Crédito Rappi
#                 - CT-03 : Crédito BBVA
#                 - CT-04 : Crédito Banamex
#                 - CT-05 : Crédito American Express
#
# FLOW (same for all 5 cards):
#   1. Login → Calculator screen
#   2. Type charge amount ($50.00)
#   3. Click "Realizar cobro"
#   4. Select "Venta Normal" (not Check In)
#   5. Wait for "Acerca, inserta o desliza tu tarjeta" screen
#   6. *** USER MANUALLY INSERTS CARD VIA CHIP — 20 SECOND PAUSE ***
#   7. User enters PIN on physical reader
#   8. Verify green "Transacción aprobada" screen
#   9. Click "Finalizar"
#  10. Verify return to Calculator ($0.00) — SUCCESS
#
# SUCCESS CRITERIA:
#   ✅ Green "Transacción aprobada" screen appears
#   ✅ After "Finalizar" → Calculator shows $0.00
#   ❌ FAIL if green screen never appears (transaction rejected)
#
# MANUAL STEP:
#   Step 6 requires physical card insertion + PIN entry on the T6 reader.
#   A 20-second countdown is printed so the tester knows how much time remains.
#
# REQUIREMENTS:
#   - Appium server running:  appium --relaxed-security
#   - T6 connected via USB:   adb devices
#   - utils.py, config.py in parent directory (T6/v2/)
# ==================================================================================
"""

import sys
import os
import time

# ── PATH SETUP ──────────────────────────────────────────────────────────────────
# CARD_CREDIT.py is in T6/v2/Transactional/
# utils.py and config.py are in T6/v2/
transactional_path = os.path.abspath(os.path.dirname(__file__))
v2_path            = os.path.abspath(os.path.join(transactional_path, '..'))
for p in [v2_path, transactional_path]:
    if p not in sys.path:
        sys.path.insert(0, p)

import config
import utils
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

try:
    from appium.webdriver.common.appiumby import AppiumBy
except ImportError:
    class AppiumBy:
        ANDROID_UIAUTOMATOR = "android uiAutomator"


# ==================================================================================
# CONSTANTS
# ==================================================================================

CHARGE_AMOUNT     = "500"       # Amount: press 5→0→0 = $500.00 (calculator adds right-to-left)
CARD_INSERT_WAIT  = 35          # Seconds to wait for manual card insertion + PIN
TRANSACTION_WAIT  = 45          # Max seconds to wait for approval screen after pause


# ── TRANSACTION FLOW XPATHs ─────────────────────────────────────────────────────
# "Realizar cobro" button — blue button at bottom of calculator screen
XPATH_BTN_REALIZAR_COBRO = (
    '//*[contains(@content-desc,"Realizar cobro") or '
    'contains(@text,"Realizar cobro")]'
)

# "¿Qué tipo de operación?" popup — appears after clicking Realizar cobro
XPATH_POPUP_TIPO_OPERACION = (
    '//*[contains(@content-desc,"tipo de operación") or '
    'contains(@text,"tipo de operación") or '
    'contains(@content-desc,"Qué tipo") or '
    'contains(@text,"Qué tipo")]'
)

# "Venta Normal" option in the popup
XPATH_BTN_VENTA_NORMAL = (
    '//*[@content-desc="Venta Normal" or @text="Venta Normal" or '
    'contains(@content-desc,"Venta Normal") or contains(@text,"Venta Normal")]'
)

# "Iniciando transacción..." or "Acerca, inserta o desliza" screen
XPATH_SCREEN_CARD_INSERT = (
    '//*[contains(@content-desc,"Acerca") or contains(@text,"Acerca") or '
    'contains(@content-desc,"inserta") or contains(@text,"inserta") or '
    'contains(@content-desc,"desliza") or contains(@text,"desliza") or '
    'contains(@content-desc,"Iniciando transacción") or '
    'contains(@text,"Iniciando transacción")]'
)

# "Transacción aprobada" — GREEN SUCCESS SCREEN
XPATH_SCREEN_APROBADA = (
    '//*[contains(@content-desc,"Transacción aprobada") or '
    'contains(@text,"Transacción aprobada") or '
    'contains(@content-desc,"aprobada") or contains(@text,"aprobada")]'
)

# "¿Cómo deseas compartir el ticket?" screen
XPATH_SCREEN_COMPARTIR = (
    '//*[contains(@content-desc,"compartir el ticket") or '
    'contains(@text,"compartir el ticket") or '
    'contains(@content-desc,"Cómo deseas") or '
    'contains(@text,"Cómo deseas")]'
)

# "Finalizar" button on ticket share screen
XPATH_BTN_FINALIZAR = (
    '//*[@content-desc="Finalizar" or @text="Finalizar" or '
    'contains(@content-desc,"Finalizar") or contains(@text,"Finalizar")]'
)

# Calculator back at $0.00 — confirms return to home
XPATH_DISPLAY_CERO = (
    '//*[contains(@content-desc,"0.00") or contains(@text,"0.00")]'
)


# ==================================================================================
# INTERNAL HELPERS
# ==================================================================================

def _take_screenshot(driver, name):
    try:
        utils.take_screenshot(driver, name, "t6")
    except Exception as e:
        print(f"   ⚠️  SCREENSHOT FAILED [{name}]: {e}")


def _countdown(seconds, message):
    """Prints a live countdown so the tester knows how much time remains."""
    print(f"\n   ⏳ {message}")
    for remaining in range(seconds, 0, -1):
        print(f"      🕐 {remaining:02d}s remaining...", end="\r")
        time.sleep(1)
    print(f"      ✅ WAIT COMPLETE — continuing automation.        ")


def _helper_login(driver, wait):
    """
    Full login flow identical to other Operationals_*.py files.
    Onboarding → Login → Commerce config → Lector popup → Calculator home.
    """
    print("   📱 [HELPER] PHASE 1: ONBOARDING...")
    time.sleep(3)

    for slide_num, btn_xpath in enumerate([
        config.XPATH_OB_BTN_SIGUIENTE,
        config.XPATH_OB_BTN_SIGUIENTE,
        config.XPATH_OB_BTN_COMENZAR
    ], 1):
        label = "Siguiente" if slide_num < 3 else "Comenzar"
        try:
            utils.click_element(driver, btn_xpath)
            time.sleep(1.5 if slide_num < 3 else 2)
            print(f"   ✅ SLIDE {slide_num} — '{label}'")
        except:
            print(f"   ⚠️  SLIDE {slide_num} skip")
            if slide_num == 1:
                try:
                    utils.click_element(driver, config.XPATH_OB_BTN_SALTAR)
                    time.sleep(1)
                except:
                    pass

    print("   🔐 [HELPER] PHASE 2: LOGIN...")
    utils.type_text(driver, config.XPATH_INPUT_USUARIO, config.USUARIO_VALIDO)
    utils.type_text(driver, config.XPATH_INPUT_PASS,    config.PASS_VALIDO)
    try:
        driver.hide_keyboard()
    except:
        pass
    utils.click_element(driver, config.XPATH_LG_BTN_INICIAR)
    time.sleep(5)

    print("   🏪 [HELPER] PHASE 3: COMMERCE CONFIG...")
    if utils.verify_element(wait, config.XPATH_CC_SCREEN, "CONFIGURA TU COMERCIO"):
        try:
            utils.type_text(driver, config.XPATH_CC_INPUT_AFILIACION, config.CC_AFILIACION)
            utils.type_text(driver, config.XPATH_CC_INPUT_TOKEN,      config.CC_TOKEN)
            try:
                driver.hide_keyboard()
            except:
                pass
            utils.click_element(driver, config.XPATH_CC_BTN_CONFIRMAR)
            time.sleep(3)
        except Exception as e:
            print(f"   ⚠️  Commerce form: {e}")
    else:
        print("   ℹ️  Commerce already linked.")

    print("   ⚙️  [HELPER] PHASE 4: LECTOR POPUP...")
    time.sleep(2)
    if utils.verify_element(wait, config.XPATH_LG_POPUP_LECTOR_NC, "LECTOR NC POPUP"):
        try:
            utils.click_element(driver, config.XPATH_LG_BTN_CONFIGURAR_AHORA)
            time.sleep(3)
            WebDriverWait(driver, 8).until(
                lambda d: d.find_element(By.XPATH, config.XPATH_LG_LECTOR_CONFIGURADO)
            )
            utils.click_element(driver, config.XPATH_LG_BTN_ACEPTAR_LECTOR)
            time.sleep(2)
            print("   ✅ LECTOR CONFIGURED.")
        except Exception as e:
            print(f"   ⚠️  Lector popup: {e}")
    else:
        print("   ℹ️  No lector popup.")
        time.sleep(2)

    print("   ✅ [HELPER] LOGIN COMPLETE.")


def _type_amount(driver, amount_str):
    """
    Types the charge amount digit by digit on the calculator.
    Uses coordinate-based tap on each number key — same pattern as Operationals_C.py.
    """
    print(f"   ✏️  TYPING AMOUNT: ${amount_str}")
    for digit in amount_str:
        digit_xpath = f'//*[@content-desc="{digit}" or @text="{digit}"]'
        try:
            btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, digit_xpath))
            )
            btn.click()
            time.sleep(0.3)
        except:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    f'new UiSelector().text("{digit}")'
                ).click()
                time.sleep(0.3)
            except Exception as e:
                print(f"   ⚠️  Could not type digit '{digit}': {e}")

    # Verify the amount appears on display
    time.sleep(0.5)
    try:
        display = driver.find_element(By.XPATH, config.XPATH_C_DISPLAY_UPDATED)
        displayed = display.get_attribute("content-desc") or display.get_attribute("text") or ""
        print(f"   ✅ DISPLAY SHOWS: {displayed}")
    except:
        print(f"   ⚠️  Could not read display — continuing.")


def _run_credit_card_test(card_name, test_id):
    """
    Executes the full credit card payment flow for one card.

    AUTOMATED steps:
        1. Login → Calculator
        2. Type $50 → Realizar cobro
        3. Select Venta Normal
        4. Wait for card insertion screen
        5. [PAUSE 20s for manual card + PIN]
        6. Detect green Transacción aprobada
        7. Click Finalizar
        8. Confirm return to $0.00 calculator

    MANUAL step:
        Step 5 — tester inserts physical card chip + enters PIN on T6 reader.

    Returns (passed: bool, note: str)
    """
    print("\n" + "=" * 65)
    print(f"💳 {test_id}: {card_name.upper()}")
    print("=" * 65)

    driver, wait = utils.start_driver()
    result = False
    note   = ""

    try:
        # ──────────────────────────────────────────────────────────────
        # STEP 1: LOGIN → CALCULATOR
        # ──────────────────────────────────────────────────────────────
        print("\n👉 STEP 1: LOGIN...")
        _helper_login(driver, wait)
        _take_screenshot(driver, f"{test_id}_STEP1_CALCULATOR")

        # ──────────────────────────────────────────────────────────────
        # STEP 2: TYPE AMOUNT ($50)
        # ──────────────────────────────────────────────────────────────
        print(f"\n👉 STEP 2: TYPING AMOUNT ${CHARGE_AMOUNT}...")
        _type_amount(driver, CHARGE_AMOUNT)
        _take_screenshot(driver, f"{test_id}_STEP2_AMOUNT_ENTERED")

        # ──────────────────────────────────────────────────────────────
        # STEP 3: CLICK "REALIZAR COBRO"
        # ──────────────────────────────────────────────────────────────
        print("\n👉 STEP 3: CLICKING 'Realizar cobro'...")
        btn_clicked = False
        for xpath in [
            XPATH_BTN_REALIZAR_COBRO,
            config.XPATH_C_BTN_CANCELAR.replace("Cancelar", "Realizar cobro"),
            '//*[contains(@content-desc,"cobro") or contains(@text,"cobro")]',
        ]:
            try:
                btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                btn.click()
                btn_clicked = True
                print("   ✅ 'Realizar cobro' CLICKED.")
                break
            except:
                continue

        if not btn_clicked:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().descriptionContains("cobro")'
                ).click()
                btn_clicked = True
                print("   ✅ 'Realizar cobro' CLICKED (UiAutomator).")
            except Exception as e:
                note = f"COULD NOT CLICK 'Realizar cobro': {e}"
                print(f"   ❌ {note}")
                return False, note

        time.sleep(3)
        _take_screenshot(driver, f"{test_id}_STEP3_AFTER_REALIZAR_COBRO")

        # ──────────────────────────────────────────────────────────────
        # STEP 4: SELECT "VENTA NORMAL"
        # ──────────────────────────────────────────────────────────────
        print("\n👉 STEP 4: SELECTING 'Venta Normal'...")

        # Wait for the ¿Qué tipo de operación? popup
        popup_appeared = False
        try:
            WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.XPATH, XPATH_POPUP_TIPO_OPERACION))
            )
            popup_appeared = True
            print("   ✅ 'Qué tipo de operación' POPUP VISIBLE.")
        except:
            print("   ⚠️  Popup not detected via XPath — scanning screen...")
            try:
                page = driver.page_source.lower()
                if "tipo de operación" in page or "venta normal" in page:
                    popup_appeared = True
                    print("   ✅ Popup detected via page_source.")
            except:
                pass

        _take_screenshot(driver, f"{test_id}_STEP4_TIPO_OPERACION_POPUP")

        # Click "Venta Normal"
        sale_clicked = False
        for xpath in [XPATH_BTN_VENTA_NORMAL]:
            try:
                btn = WebDriverWait(driver, 6).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                btn.click()
                sale_clicked = True
                print("   ✅ 'Venta Normal' CLICKED.")
                break
            except:
                continue

        if not sale_clicked:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().text("Venta Normal")'
                ).click()
                sale_clicked = True
                print("   ✅ 'Venta Normal' CLICKED (UiAutomator).")
            except Exception as e:
                note = f"COULD NOT CLICK 'Venta Normal': {e}"
                print(f"   ❌ {note}")
                return False, note

        time.sleep(2)
        _take_screenshot(driver, f"{test_id}_STEP4_VENTA_NORMAL_SELECTED")

        # ──────────────────────────────────────────────────────────────
        # STEP 5: WAIT FOR CARD INSERTION SCREEN
        # ──────────────────────────────────────────────────────────────
        print("\n👉 STEP 5: WAITING FOR CARD INSERTION SCREEN...")
        card_screen_ok = False
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, XPATH_SCREEN_CARD_INSERT))
            )
            card_screen_ok = True
            print("   ✅ CARD INSERTION SCREEN DETECTED.")
        except:
            print("   ⚠️  Card screen XPath not matched — checking page source...")
            try:
                page = driver.page_source.lower()
                if any(kw in page for kw in ["acerca", "inserta", "desliza", "iniciando"]):
                    card_screen_ok = True
                    print("   ✅ Card screen detected via page source.")
            except:
                pass

        _take_screenshot(driver, f"{test_id}_STEP5_CARD_INSERT_SCREEN")

        # ──────────────────────────────────────────────────────────────
        # STEP 6: MANUAL PAUSE — USER INSERTS CARD + ENTERS PIN
        # ALSO POLLS FOR APPROVAL SCREEN DURING THE WAIT so we don't
        # miss the green screen if the user is fast.
        # ──────────────────────────────────────────────────────────────
        print(f"\n{'='*65}")
        print(f"🃏 MANUAL ACTION REQUIRED — {card_name}")
        print(f"{'='*65}")
        print(f"   👉 INSERT THE CHIP of: {card_name}")
        print(f"   👉 ENTER THE PIN on the T6 physical reader")
        print(f"   👉 You have {CARD_INSERT_WAIT} seconds — automation polls in background")
        print(f"{'='*65}")

        # ACTIVE POLLING DURING MANUAL WAIT
        # Checks every second for the approval screen — catches fast users
        transaction_approved = False
        approval_keywords    = ["aprobada", "transacción aprobada", "approved"]

        wait_end = time.time() + CARD_INSERT_WAIT
        elapsed  = 0
        while time.time() < wait_end:
            remaining = int(wait_end - time.time())
            print(f"      🕐 {remaining:02d}s remaining — polling for approval...", end="\r")

            # CHECK FOR GREEN SCREEN DURING PAUSE
            try:
                elems = driver.find_elements(By.XPATH, XPATH_SCREEN_APROBADA)
                for elem in elems:
                    try:
                        t = (elem.get_attribute("text") or "").lower()
                        d = (elem.get_attribute("content-desc") or "").lower()
                        if any(kw in t+d for kw in approval_keywords):
                            transaction_approved = True
                            break
                    except:
                        continue
            except:
                pass

            if not transaction_approved:
                try:
                    page = driver.page_source.lower()
                    if any(kw in page for kw in approval_keywords):
                        transaction_approved = True
                except:
                    pass

            if transaction_approved:
                print(f"\n   ✅ APPROVAL DETECTED DURING MANUAL WAIT — proceeding immediately!")
                break

            time.sleep(1)

        print(f"\n   ✅ MANUAL WAIT COMPLETE.")

        # ──────────────────────────────────────────────────────────────
        # STEP 7: DETECT GREEN "TRANSACCIÓN APROBADA" SCREEN
        # If not already found during the pause, keep polling
        # ──────────────────────────────────────────────────────────────
        print("\n👉 STEP 7: CONFIRMING 'Transacción aprobada' (GREEN SCREEN)...")

        if not transaction_approved:
            # Continue polling for up to TRANSACTION_WAIT more seconds
            poll_end = time.time() + TRANSACTION_WAIT
            while time.time() < poll_end and not transaction_approved:
                try:
                    elems = driver.find_elements(By.XPATH, XPATH_SCREEN_APROBADA)
                    for elem in elems:
                        try:
                            t = (elem.get_attribute("text") or "").lower()
                            d = (elem.get_attribute("content-desc") or "").lower()
                            if any(kw in t+d for kw in approval_keywords):
                                transaction_approved = True
                                print("   ✅ 'Transacción aprobada' DETECTED!")
                                break
                        except:
                            continue
                except:
                    pass

                if not transaction_approved:
                    try:
                        page = driver.page_source.lower()
                        if any(kw in page for kw in approval_keywords):
                            transaction_approved = True
                            print("   ✅ 'Transacción aprobada' DETECTED via page source!")
                    except:
                        pass

                if not transaction_approved:
                    time.sleep(1)
        else:
            print("   ✅ 'Transacción aprobada' ALREADY CONFIRMED DURING MANUAL WAIT.")

        _take_screenshot(driver, f"{test_id}_STEP7_APPROVAL_SCREEN")

        if not transaction_approved:
            note = "GREEN 'Transacción aprobada' SCREEN NOT DETECTED — TRANSACTION FAILED OR TIMED OUT"
            print(f"\n   ❌ {note}")
            # Dump screen for diagnosis
            print("   🔍 SCREEN DUMP:")
            try:
                for elem in driver.find_elements(By.XPATH, "//*"):
                    try:
                        t = elem.get_attribute("text") or ""
                        d = elem.get_attribute("content-desc") or ""
                        if (t and len(t) > 2) or (d and len(d) > 2 and d != "null"):
                            print(f"      📝 text='{t}' | desc='{d}'")
                    except:
                        continue
            except:
                pass
            return False, note

        # ──────────────────────────────────────────────────────────────
        # STEP 8: HANDLE TICKET SHARE SCREEN → CLICK "FINALIZAR"
        # ──────────────────────────────────────────────────────────────
        print("\n👉 STEP 8: CLICKING 'Finalizar'...")

        # The flow is: Aprobada screen → Aceptar → Ticket share → Finalizar
        # First try "Aceptar" on the green screen
        time.sleep(2)
        try:
            aceptar = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, config.XPATH_C_BTN_ACEPTAR_PROPINA))
            )
            aceptar.click()
            print("   ✅ 'Aceptar' CLICKED on approval screen.")
            time.sleep(2)
        except:
            print("   ℹ️  No 'Aceptar' button on approval screen — trying Finalizar directly.")

        _take_screenshot(driver, f"{test_id}_STEP8_TICKET_SCREEN")

        # Now click "Finalizar" on ticket share screen
        finalize_clicked = False
        for xpath in [XPATH_BTN_FINALIZAR]:
            try:
                btn = WebDriverWait(driver, 8).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                btn.click()
                finalize_clicked = True
                print("   ✅ 'Finalizar' CLICKED.")
                break
            except:
                continue

        if not finalize_clicked:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().text("Finalizar")'
                ).click()
                finalize_clicked = True
                print("   ✅ 'Finalizar' CLICKED (UiAutomator).")
            except:
                # Try "Aceptar" as last resort (some flows merge the screens)
                try:
                    driver.find_element(
                        AppiumBy.ANDROID_UIAUTOMATOR,
                        'new UiSelector().text("Aceptar")'
                    ).click()
                    finalize_clicked = True
                    print("   ✅ 'Aceptar' CLICKED as Finalizar fallback.")
                except Exception as e:
                    print(f"   ⚠️  Could not click Finalizar: {e}")

        time.sleep(3)
        _take_screenshot(driver, f"{test_id}_STEP8_AFTER_FINALIZAR")

        # ──────────────────────────────────────────────────────────────
        # STEP 9: VERIFY RETURN TO CALCULATOR ($0.00)
        # ──────────────────────────────────────────────────────────────
        print("\n👉 STEP 9: VERIFYING RETURN TO CALCULATOR ($0.00)...")
        returned_to_calculator = False
        try:
            WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.XPATH, XPATH_DISPLAY_CERO))
            )
            returned_to_calculator = True
            print("   ✅ CALCULATOR SHOWS $0.00 — TEST COMPLETE.")
        except:
            # Check for calculator screen by other indicators
            try:
                driver.find_element(By.XPATH, config.XPATH_C_PANTALLA_COBRO)
                returned_to_calculator = True
                print("   ✅ CALCULATOR SCREEN CONFIRMED.")
            except:
                print("   ⚠️  Could not confirm return to calculator.")

        _take_screenshot(driver, f"{test_id}_STEP9_BACK_TO_CALCULATOR")

        # ──────────────────────────────────────────────────────────────
        # RESULT
        # ──────────────────────────────────────────────────────────────
        result = transaction_approved  # Green screen = success
        note   = (
            f"APPROVED ✅ | Finalizar: {'OK' if finalize_clicked else 'SKIP'} | "
            f"Back to calc: {'OK' if returned_to_calculator else 'NOT CONFIRMED'}"
        )

    except Exception as e:
        result = False
        note   = f"CRITICAL ERROR: {e}"
        print(f"\n💥 {test_id} CRITICAL ERROR: {e}")
        try:
            _take_screenshot(driver, f"{test_id}_CRITICAL_ERROR")
        except:
            pass

    finally:
        utils.close_driver(driver)

    return result, note


# ==================================================================================
# INDIVIDUAL TEST FUNCTIONS — ONE PER CARD
# ==================================================================================

def CT_01_CREDITO_NU():
    """CT-01: Crédito Nu — full payment flow with manual chip + PIN."""
    return _run_credit_card_test("Crédito Nu", "CT_01_NU")

def CT_02_CREDITO_RAPPI():
    """CT-02: Crédito Rappi — full payment flow with manual chip + PIN."""
    return _run_credit_card_test("Crédito Rappi", "CT_02_RAPPI")

def CT_03_CREDITO_BBVA():
    """CT-03: Crédito BBVA — full payment flow with manual chip + PIN."""
    return _run_credit_card_test("Crédito BBVA", "CT_03_BBVA")

def CT_04_CREDITO_BANAMEX():
    """CT-04: Crédito Banamex — full payment flow with manual chip + PIN."""
    return _run_credit_card_test("Crédito Banamex", "CT_04_BANAMEX")

def CT_05_CREDITO_AMEX():
    """CT-05: Crédito American Express — full payment flow with manual chip + PIN."""
    return _run_credit_card_test("Crédito American Express", "CT_05_AMEX")


# ==================================================================================
# MAIN BLOCK
# ==================================================================================

if __name__ == "__main__":

    logger, log_file, timestamp = utils.start_report("CARD_CREDIT")

    results = {}

    try:
        results["CT-01 Crédito Nu"]               = CT_01_CREDITO_NU()
        results["CT-02 Crédito Rappi"]             = CT_02_CREDITO_RAPPI()
        results["CT-03 Crédito BBVA"]              = CT_03_CREDITO_BBVA()
        results["CT-04 Crédito Banamex"]           = CT_04_CREDITO_BANAMEX()
        results["CT-05 Crédito American Express"]  = CT_05_CREDITO_AMEX()

    finally:
        print("\n" + "=" * 65)
        print("📊 CARD_CREDIT — FINAL SUMMARY")
        print("=" * 65)
        print(f"  {'TEST CASE':<35} {'RESULT':<8} NOTE")
        print("  " + "─" * 62)
        for test_name, (passed, note) in results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"  {test_name:<35} {status:<8} {note}")
            # ── FORMAT REQUIRED BY generate_html_report PARSER ──
            # Parser looks for: "✅" + ": SUCCESS" OR "❌" + ": FAILED"
            if passed:
                print(f"  ✅ {test_name}: SUCCESS — {note}")
            else:
                print(f"  ❌ {test_name}: FAILED — {note}")
        print("  " + "─" * 62)
        passed_count = sum(1 for v in results.values() if v[0])
        print(f"  TOTAL: {passed_count}/{len(results)} PASSED")
        print("=" * 65)

        utils.generate_zip_report("CARD_CREDIT", logger, log_file, timestamp)
        utils.generate_html_report("CARD_CREDIT", log_file, timestamp)