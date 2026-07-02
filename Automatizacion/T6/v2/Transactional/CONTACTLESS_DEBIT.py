"""
# ==================================================================================
# FILENAME    : Contactless_Debit.py
# FOLDER      : Automatizacion/T6/v2/Transactional/
# PROJECT     : MEMPHIS QA AUTOMATION FRAMEWORK
# DESCRIPTION : CONTACTLESS DEBIT CARD PAYMENT TEST SUITE.
#               VALIDATES END-TO-END CONTACTLESS (NFC) PAYMENT FLOW FOR:
#                 - CDL-01 : Débito Banamex
#                 - CDL-02 : Débito Plata
#
# AMOUNT: $25.00 → press 2 → 5 → 0 → 0  (T6 calculator right-to-left logic)
#
# FLOW (same for both cards):
#   1.  Login → Calculator screen
#   2.  Type charge amount ($25.00) → press 2→5→0→0
#   3.  Click "Realizar cobro"
#   4.  Select "Venta Normal"
#   5.  Wait for "Acerca, inserta o desliza tu tarjeta" screen
#   6.  *** USER TAPS CARD CONTACTLESS — 30 SECOND ACTIVE PAUSE ***
#       (automation polls every second for green screen during wait)
#   7.  Confirm green "Transacción aprobada" screen → SUCCESS
#   8.  Click "Aceptar" → "Finalizar"
#   9.  Verify return to Calculator ($0.00)
#
# SUCCESS CRITERIA:
#   ✅ Green "Transacción aprobada" screen appears
#   ✅ After "Finalizar" → Calculator shows $0.00
#   ❌ FAIL if green screen never appears
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

try:
    from appium.webdriver.common.appiumby import AppiumBy
except ImportError:
    class AppiumBy:
        ANDROID_UIAUTOMATOR = "android uiAutomator"


# ==================================================================================
# CONSTANTS
# ==================================================================================

# Amount: press 2→5→0→0 = $25.00 on T6 calculator (right-to-left digit logic)
CHARGE_AMOUNT        = "2500"
CONTACTLESS_WAIT     = 30    # Seconds of active polling while user taps card
TRANSACTION_WAIT     = 45    # Additional polling seconds after manual wait if needed
APPROVAL_KEYWORDS    = ["aprobada", "transacción aprobada", "approved"]


# ── TRANSACTION FLOW XPATHs ─────────────────────────────────────────────────────

XPATH_BTN_REALIZAR_COBRO = (
    '//*[contains(@content-desc,"Realizar cobro") or '
    'contains(@text,"Realizar cobro")]'
)
XPATH_POPUP_TIPO_OPERACION = (
    '//*[contains(@content-desc,"tipo de operación") or '
    'contains(@text,"tipo de operación") or '
    'contains(@content-desc,"Qué tipo") or '
    'contains(@text,"Qué tipo")]'
)
XPATH_BTN_VENTA_NORMAL = (
    '//*[@content-desc="Venta Normal" or @text="Venta Normal" or '
    'contains(@content-desc,"Venta Normal") or contains(@text,"Venta Normal")]'
)
XPATH_SCREEN_CARD_READY = (
    '//*[contains(@content-desc,"Acerca") or contains(@text,"Acerca") or '
    'contains(@content-desc,"inserta") or contains(@text,"inserta") or '
    'contains(@content-desc,"desliza") or contains(@text,"desliza") or '
    'contains(@content-desc,"Iniciando transacción") or '
    'contains(@text,"Iniciando transacción")]'
)
XPATH_SCREEN_APROBADA = (
    '//*[contains(@content-desc,"Transacción aprobada") or '
    'contains(@text,"Transacción aprobada") or '
    'contains(@content-desc,"aprobada") or contains(@text,"aprobada")]'
)
XPATH_BTN_FINALIZAR = (
    '//*[@content-desc="Finalizar" or @text="Finalizar" or '
    'contains(@content-desc,"Finalizar") or contains(@text,"Finalizar")]'
)
XPATH_DISPLAY_ZERO = (
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


def _helper_login(driver, wait):
    """Full login flow: onboarding → credentials → commerce → lector → calculator."""
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
    Types the charge amount digit by digit on the T6 calculator.
    T6 calculator right-to-left digit logic:
        "2500" → 2→5→0→0 = $25.00 ✅
    """
    print(f"   ✏️  TYPING AMOUNT: {amount_str} → produces $25.00")
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
    time.sleep(0.5)
    try:
        display = driver.find_element(By.XPATH, config.XPATH_C_DISPLAY_UPDATED)
        displayed = (
            display.get_attribute("content-desc") or
            display.get_attribute("text") or ""
        )
        print(f"   ✅ DISPLAY SHOWS: {displayed}")
    except:
        print(f"   ⚠️  Could not read display — continuing.")


def _poll_for_approval(driver, poll_seconds, label):
    """
    Polls every second for the green 'Transacción aprobada' screen.
    Advances immediately when detected.
    """
    end_time = time.time() + poll_seconds
    while time.time() < end_time:
        remaining = int(end_time - time.time())
        print(f"      🕐 {remaining:02d}s remaining — {label}...", end="\r")

        try:
            elems = driver.find_elements(By.XPATH, XPATH_SCREEN_APROBADA)
            for elem in elems:
                try:
                    t = (elem.get_attribute("text") or "").lower()
                    d = (elem.get_attribute("content-desc") or "").lower()
                    if any(kw in t + d for kw in APPROVAL_KEYWORDS):
                        print(f"\n   ✅ APPROVED DETECTED at {poll_seconds - remaining}s!")
                        return True
                except:
                    continue
        except:
            pass

        try:
            if any(kw in driver.page_source.lower() for kw in APPROVAL_KEYWORDS):
                print(f"\n   ✅ APPROVED DETECTED via page source at {poll_seconds - remaining}s!")
                return True
        except:
            pass

        time.sleep(1)

    print()
    return False


def _run_contactless_debit_test(card_name, test_id):
    """
    Executes the full contactless debit card payment flow for one card.
    Returns (passed: bool, note: str)
    """
    print("\n" + "=" * 65)
    print(f"💳 {test_id}: {card_name.upper()} — CONTACTLESS")
    print("=" * 65)

    driver, wait = utils.start_driver()
    result = False
    note   = ""

    try:
        # ── STEP 1: LOGIN ────────────────────────────────────────────
        print("\n👉 STEP 1: LOGIN...")
        _helper_login(driver, wait)
        _take_screenshot(driver, f"{test_id}_STEP1_CALCULATOR")

        # ── STEP 2: TYPE AMOUNT ($25.00) ─────────────────────────────
        print(f"\n👉 STEP 2: TYPING AMOUNT ({CHARGE_AMOUNT} → $25.00)...")
        _type_amount(driver, CHARGE_AMOUNT)
        _take_screenshot(driver, f"{test_id}_STEP2_AMOUNT_ENTERED")

        # ── STEP 3: REALIZAR COBRO ───────────────────────────────────
        print("\n👉 STEP 3: CLICKING 'Realizar cobro'...")
        charge_clicked = False
        for xpath in [
            XPATH_BTN_REALIZAR_COBRO,
            '//*[contains(@content-desc,"cobro") or contains(@text,"cobro")]',
        ]:
            try:
                btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                btn.click()
                charge_clicked = True
                print("   ✅ 'Realizar cobro' CLICKED.")
                break
            except:
                continue
        if not charge_clicked:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().descriptionContains("cobro")'
                ).click()
                charge_clicked = True
                print("   ✅ 'Realizar cobro' CLICKED (UiAutomator).")
            except Exception as e:
                note = f"COULD NOT CLICK 'Realizar cobro': {e}"
                print(f"   ❌ {note}")
                return False, note

        time.sleep(3)
        _take_screenshot(driver, f"{test_id}_STEP3_AFTER_COBRO")

        # ── STEP 4: VENTA NORMAL ─────────────────────────────────────
        print("\n👉 STEP 4: SELECTING 'Venta Normal'...")
        try:
            WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.XPATH, XPATH_POPUP_TIPO_OPERACION))
            )
            print("   ✅ 'Qué tipo de operación' POPUP VISIBLE.")
        except:
            page = driver.page_source.lower()
            if "tipo de operación" in page or "venta normal" in page:
                print("   ✅ Popup detected via page source.")
            else:
                print("   ⚠️  Popup not detected — attempting Venta Normal anyway.")

        _take_screenshot(driver, f"{test_id}_STEP4_TIPO_OPERACION")

        sale_clicked = False
        try:
            btn = WebDriverWait(driver, 6).until(
                EC.element_to_be_clickable((By.XPATH, XPATH_BTN_VENTA_NORMAL))
            )
            btn.click()
            sale_clicked = True
            print("   ✅ 'Venta Normal' CLICKED.")
        except:
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
        _take_screenshot(driver, f"{test_id}_STEP4_VENTA_NORMAL")

        # ── STEP 5: CARD READY SCREEN ────────────────────────────────
        print("\n👉 STEP 5: WAITING FOR CARD READY SCREEN...")
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, XPATH_SCREEN_CARD_READY))
            )
            print("   ✅ CARD READY SCREEN DETECTED.")
        except:
            page = driver.page_source.lower()
            if any(kw in page for kw in ["acerca", "inserta", "desliza", "iniciando"]):
                print("   ✅ Card screen detected via page source.")
            else:
                print("   ⚠️  Card screen not confirmed — continuing.")
        _take_screenshot(driver, f"{test_id}_STEP5_CARD_READY")

        # ── STEP 6: MANUAL PAUSE — USER TAPS CARD CONTACTLESS ────────
        print(f"\n{'='*65}")
        print(f"📲 MANUAL ACTION REQUIRED — {card_name}")
        print(f"{'='*65}")
        print(f"   👉 TAP CARD CONTACTLESS: {card_name}")
        print(f"   👉 Acerca la tarjeta al lector NFC del T6")
        print(f"   👉 {CONTACTLESS_WAIT}s active polling — advances immediately on approval")
        print(f"{'='*65}")

        transaction_approved = _poll_for_approval(
            driver, CONTACTLESS_WAIT, f"waiting for {card_name} contactless tap"
        )

        # ── STEP 7: CONFIRM APPROVAL ─────────────────────────────────
        print("\n👉 STEP 7: CONFIRMING 'Transacción aprobada'...")
        if not transaction_approved:
            print(f"   ⏳ Not yet detected — polling {TRANSACTION_WAIT}s more...")
            transaction_approved = _poll_for_approval(
                driver, TRANSACTION_WAIT, "waiting for server response"
            )

        _take_screenshot(driver, f"{test_id}_STEP7_APPROVAL")

        if not transaction_approved:
            note = "GREEN 'Transacción aprobada' NOT DETECTED — TRANSACTION FAILED OR TIMED OUT"
            print(f"\n   ❌ {note}")
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

        print("   ✅ TRANSACTION APPROVED!")

        # ── STEP 8: ACEPTAR + FINALIZAR ──────────────────────────────
        print("\n👉 STEP 8: CLICKING 'Aceptar' → 'Finalizar'...")
        time.sleep(2)

        try:
            btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, config.XPATH_C_BTN_ACEPTAR_PROPINA)
                )
            )
            btn.click()
            print("   ✅ 'Aceptar' CLICKED.")
            time.sleep(2)
        except:
            print("   ℹ️  No 'Aceptar' button — going straight to Finalizar.")

        _take_screenshot(driver, f"{test_id}_STEP8_TICKET_SCREEN")

        finalize_clicked = False
        try:
            btn = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable((By.XPATH, XPATH_BTN_FINALIZAR))
            )
            btn.click()
            finalize_clicked = True
            print("   ✅ 'Finalizar' CLICKED.")
        except:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().text("Finalizar")'
                ).click()
                finalize_clicked = True
                print("   ✅ 'Finalizar' CLICKED (UiAutomator).")
            except:
                try:
                    driver.find_element(
                        AppiumBy.ANDROID_UIAUTOMATOR,
                        'new UiSelector().text("Aceptar")'
                    ).click()
                    finalize_clicked = True
                    print("   ✅ 'Aceptar' CLICKED as Finalizar fallback.")
                except Exception as e:
                    print(f"   ⚠️  Finalizar not found: {e}")

        time.sleep(3)
        _take_screenshot(driver, f"{test_id}_STEP8_AFTER_FINALIZAR")

        # ── STEP 9: VERIFY RETURN TO CALCULATOR ──────────────────────
        print("\n👉 STEP 9: VERIFYING RETURN TO CALCULATOR ($0.00)...")
        returned_to_calculator = False
        try:
            WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.XPATH, XPATH_DISPLAY_ZERO))
            )
            returned_to_calculator = True
            print("   ✅ CALCULATOR SHOWS $0.00 — FLOW COMPLETE.")
        except:
            try:
                driver.find_element(By.XPATH, config.XPATH_C_PANTALLA_COBRO)
                returned_to_calculator = True
                print("   ✅ CALCULATOR SCREEN CONFIRMED.")
            except:
                print("   ⚠️  Could not confirm return to calculator.")

        _take_screenshot(driver, f"{test_id}_STEP9_BACK_TO_CALCULATOR")

        result = True
        note   = (
            f"APPROVED ✅ | "
            f"Finalizar: {'OK' if finalize_clicked else 'SKIP'} | "
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

def CDL_01_DEBITO_BANAMEX():
    """CDL-01: Débito Banamex — contactless NFC tap."""
    return _run_contactless_debit_test("Débito Banamex", "CDL_01_BANAMEX")

def CDL_02_DEBITO_PLATA():
    """CDL-02: Débito Plata — contactless NFC tap."""
    return _run_contactless_debit_test("Débito Plata", "CDL_02_PLATA")


# ==================================================================================
# MAIN BLOCK
# ==================================================================================

if __name__ == "__main__":

    logger, log_file, timestamp = utils.start_report("CONTACTLESS_DEBIT")

    results = {}

    try:
        results["CDL-01 Débito Banamex"] = CDL_01_DEBITO_BANAMEX()
        results["CDL-02 Débito Plata"]   = CDL_02_DEBITO_PLATA()

    finally:
        print("\n" + "=" * 65)
        print("📊 CONTACTLESS_DEBIT — FINAL SUMMARY")
        print("=" * 65)
        print(f"  {'TEST CASE':<35} {'RESULT':<8} NOTE")
        print("  " + "─" * 62)
        for test_name, (passed, note) in results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"  {test_name:<35} {status:<8} {note}")
            if passed:
                print(f"  ✅ {test_name}: SUCCESS — {note}")
            else:
                print(f"  ❌ {test_name}: FAILED — {note}")
        print("  " + "─" * 62)
        passed_count = sum(1 for v in results.values() if v[0])
        print(f"  TOTAL: {passed_count}/{len(results)} PASSED")
        print("=" * 65)

        utils.generate_zip_report("CONTACTLESS_DEBIT", logger, log_file, timestamp)
        utils.generate_html_report("CONTACTLESS_DEBIT", log_file, timestamp)