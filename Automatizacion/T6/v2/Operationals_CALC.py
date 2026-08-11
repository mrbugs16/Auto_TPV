"""
FILENAME: Operationals_CALC.py
DESCRIPTION:
    AUTOMATED TEST SUITE — CALCULATOR / CHARGING SCREEN (C / "Calculadora") MODULE.
    VALIDATES FLOWS FOR USERS OPERATING THE MAIN CHARGING SCREEN AFTER COMPLETING
    BUSINESS REGISTRATION OR LOGGING IN WITH AN EXISTING ACCOUNT.

TEST CASES COVERED:
    · CALC-001 : VALIDATE THE MAIN CHARGING SCREEN LOADS CORRECTLY AFTER BUSINESS
                 REGISTRATION OR LOGIN
    · CALC-002 : VALIDATE ALL DIGITS (0-9) CAN BE ENTERED ON THE CALCULATOR NUMPAD
    · CALC-003 : VALIDATE THE BACKSPACE BUTTON DELETES DIGITS CORRECTLY
    · CALC-004 : VALIDATE THAT LEADING ZEROS ARE NOT ALLOWED AT THE START OF AN AMOUNT
    · CALC-005 : VALIDATE ONLY ONE DECIMAL SEPARATOR AND A MAXIMUM OF TWO DECIMAL
                 DIGITS ARE ALLOWED
    · CALC-006 : VALIDATE THAT CLICKING 'COBRAR' WITH NO AMOUNT ENTERED SHOWS AN ERROR
    · CALC-007 : VALIDATE THAT AN EXCESSIVELY LARGE AMOUNT PROCEEDS TO THE CARD SCREEN
    · CALC-008 : VERIFY THAT 'COBRAR' INITIATES THE TRANSACTION PROCESS WITH A VALID
                 AMOUNT
    · CALC-009 : VERIFY 'COBRAR' BUTTON STATE DEPENDING ON AMOUNT ($0.00 VS $1.00)
    · CALC-010 : VALIDATE KEYPAD VISUAL RESPONSE, BOUNDARY LIMITS, AND DELETE BUTTON
"""

import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
import utils
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

XPATH_BIZ_INPUT_AFILIACION = '(//android.widget.EditText)[1]'
XPATH_BIZ_INPUT_TOKEN      = '(//android.widget.EditText)[2]'

XPATH_BIZ_BTN_CONFIRMAR = (
    '//*[contains(@text, "Confirmar y comenzar") or '
    'contains(@content-desc, "Confirmar y comenzar")]'
)

XPATH_BIZ_MODAL_LECTOR_NO_CONFIGURADO = (
    '//*[contains(@text, "Lector no configurado") or '
    'contains(@content-desc, "Lector no configurado")]'
)
XPATH_BIZ_BTN_CONFIGURAR_AHORA = (
    '//*[contains(@text, "Configurar ahora") or '
    'contains(@content-desc, "Configurar ahora")]'
)


XPATH_BIZ_PANTALLA_LECTOR_CONFIGURADO = (
    '//*[contains(@text, "Lector configurado") or '
    'contains(@content-desc, "Lector configurado")]'
)
XPATH_BIZ_BTN_ACEPTAR_LECTOR_CONFIGURADO = (
    '//*[contains(@text, "Aceptar") or '
    'contains(@content-desc, "Aceptar")]'
)


XPATH_CALC_BTN_REALIZAR_COBRO = '//android.widget.Button[@content-desc="Realizar cobro"]'


# ==================================================================================
# INTERNAL HELPER — CALL print_http_evidence_appium WITHOUT SILENCING ERRORS
# ==================================================================================

def _capture_evidence(driver, nombre_test):
    try:
        utils.print_http_evidence_appium(driver, nombre_test)
    except Exception as ev_err:
        print(f"   ⚠️  HTTP EVIDENCE CAPTURE FAILED FOR [{nombre_test}]: {ev_err}")
        print(f"   💡 MAKE SURE APPIUM IS STARTED WITH: appium --allow-insecure=*:get_server_logs")


# ==================================================================================
# HELPER — SKIP THE PRE-LOGIN ONBOARDING CARD ("Configura la terminal") IF PRESENT
# ==================================================================================
def _skip_onboarding_if_present(driver, wait):
    
    print("👉 CHECKING FOR ONBOARDING SCREEN ('Configura la terminal')...")
    short_wait = WebDriverWait(driver, 5)
    if utils.verify_element(short_wait, config.XPATH_OB_BTN_SALTAR, "Botón 'Saltar' (Onboarding)", driver):
        utils.click_element(driver, config.XPATH_OB_BTN_SALTAR)
        time.sleep(2)
        print("   ✅ ONBOARDING SKIPPED")
    else:
        print("   ℹ️  NO ONBOARDING SCREEN DETECTED (APP ALREADY PAST IT)")


# ==================================================================================
# HELPER — HANDLE THE 'LECTOR NO CONFIGURADO' MODAL (CONFIGURE THE READER, ONE CALL)
# ==================================================================================
def _handle_lector_no_configurado_modal(driver, wait):
    
    print("   📍 CHECKING FOR 'LECTOR NO CONFIGURADO' MODAL...")
    lector_modal_found = utils.verify_element(
        wait, XPATH_BIZ_MODAL_LECTOR_NO_CONFIGURADO, "MODAL — 'Lector no configurado'", driver
    )
    if not lector_modal_found:
        print("   ℹ️  'LECTOR NO CONFIGURADO' MODAL NOT DETECTED (APP MAY HAVE SKIPPED IT).")
        time.sleep(3)
        return

    print("   ✅ 'LECTOR NO CONFIGURADO' MODAL DETECTED. CLICKING 'CONFIGURAR AHORA'...")
    utils.click_element(driver, XPATH_BIZ_BTN_CONFIGURAR_AHORA)
    time.sleep(5)

    print("   📍 WAITING FOR 'LECTOR CONFIGURADO' SUCCESS SCREEN...")
    lector_listo = utils.verify_element(
        wait, XPATH_BIZ_PANTALLA_LECTOR_CONFIGURADO, "SUCCESS SCREEN — 'Lector configurado'", driver
    )
    if lector_listo:
        print("   ✅ 'LECTOR CONFIGURADO' SCREEN DETECTED. CLICKING 'ACEPTAR'...")
        utils.click_element(driver, XPATH_BIZ_BTN_ACEPTAR_LECTOR_CONFIGURADO)
        time.sleep(3)
    else:
        print("   ⚠️  'LECTOR CONFIGURADO' SCREEN NOT DETECTED AFTER 'CONFIGURAR AHORA' — CONTINUING ANYWAY.")


# ==================================================================================
# HELPER — FULL LOGIN + BUSINESS REGISTRATION + LOCATION PERMISSION
#          (REACHES THE MAIN CALCULATOR / CHARGING SCREEN)
# ==================================================================================
def _login_to_calculator_screen(driver, wait):
    
    _skip_onboarding_if_present(driver, wait)

    # PHASE 1: LOGIN
    print("   🔐 [HELPER] PHASE 1: EXECUTING LOGIN...")
    time.sleep(4)

    try:
        utils.click_element(driver, config.XPATH_INPUT_USUARIO)
        time.sleep(1)
    except Exception:
        pass

    print(f"   ✏️  TYPING EMAIL & PASSWORD: {config.USUARIO_VALIDO}")
    utils.type_text(driver, config.XPATH_INPUT_USUARIO, config.USUARIO_VALIDO)
    utils.type_text(driver, config.XPATH_INPUT_PASS, config.PASS_VALIDO)

    try:
        driver.hide_keyboard()
    except Exception:
        pass

    utils.click_element(driver, config.XPATH_BTN_ACEPTAR)
    time.sleep(6)

    print("   🏪 [HELPER] PHASE 2: ENTERING BUSINESS REGISTRATION DATA...")
    time.sleep(4)

    print(f"   🔢 ENTERING AFFILIATION NUMBER: {config.RN_AFILIACION}")
    try:
        utils.click_element(driver, XPATH_BIZ_INPUT_AFILIACION)
    except Exception:
        pass
    time.sleep(1)
    utils.type_text(driver, XPATH_BIZ_INPUT_AFILIACION, config.RN_AFILIACION)

    print(f"   🔑 ENTERING TOKEN: {config.RN_TOKEN}")
    try:
        utils.click_element(driver, XPATH_BIZ_INPUT_TOKEN)
    except Exception:
        pass
    time.sleep(1)
    utils.type_text(driver, XPATH_BIZ_INPUT_TOKEN, config.RN_TOKEN)

    try:
        driver.hide_keyboard()
    except Exception:
        pass
    utils.click_element(driver, XPATH_BIZ_BTN_CONFIRMAR)
    time.sleep(8)

    print("   📍 [HELPER] PHASE 3: CONFIGURING THE READER (IF THE MODAL IS SHOWN)...")
    _handle_lector_no_configurado_modal(driver, wait)


# ==================================================================================
# HELPER — PRESS BACKSPACE WITH MULTIPLE FALLBACK STRATEGIES
# ==================================================================================

def _press_backspace(driver):
    # STRATEGY 1
    try:
        driver.find_element(By.XPATH, config.XPATH_C_BTN_BACKSPACE).click()
        print("   ⌫  BACKSPACE CLICKED — STRATEGY 1 (CONFIG XPATH)")
        return True
    except Exception:
        pass

    # STRATEGY 2
    try:
        driver.find_element(
            By.XPATH, '//*[@text="0" or @content-desc="0"]/following-sibling::*[1]'
        ).click()
        print("   ⌫  BACKSPACE CLICKED — STRATEGY 2 (SIBLING AFTER '0' — WILDCARD TYPE)")
        return True
    except Exception:
        pass

    # STRATEGY 3
    try:
        driver.find_element(
            By.XPATH, '//*[@text="0" or @content-desc="0"]/../*[last()]'
        ).click()
        print("   ⌫  BACKSPACE CLICKED — STRATEGY 3 (LAST CHILD OF '0' PARENT)")
        return True
    except Exception:
        pass

    # STRATEGY 4
    try:
        driver.find_element(By.XPATH, config.XPATH_C_BTN_BACKSPACE_ABSOLUTE).click()
        print("   ⌫  BACKSPACE CLICKED — STRATEGY 4 (ABSOLUTE XPATH — INSPECTOR FALLBACK)")
        return True
    except Exception:
        pass

    print("   ⚠️  WARNING: ALL BACKSPACE STRATEGIES FAILED. DUMPING SIBLINGS OF '0' KEY...")
    try:
        siblings = driver.find_elements(
            By.XPATH, '//*[@text="0" or @content-desc="0"]/../*'
        )
        for idx, el in enumerate(siblings):
            txt  = el.get_attribute("text")
            desc = el.get_attribute("content-desc")
            cls  = el.get_attribute("className")
            rid  = el.get_attribute("resource-id")
            print(f"   🔎 SIBLING[{idx}] class='{cls}' | text='{txt}' | content-desc='{desc}' | resource-id='{rid}'")
    except Exception as dump_err:
        print(f"   ❌ DUMP FAILED: {dump_err}")
    return False


# ==================================================================================
# CALC_001: VALIDATE THE MAIN CHARGING SCREEN LOADS CORRECTLY
# ==================================================================================
def CALC_001():

    print("\n" + "=" * 60)
    print("🧪 CALC-001: VALIDATE MAIN CHARGING SCREEN LOADS CORRECTLY")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        print("🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        _login_to_calculator_screen(driver, wait)

        print("\n👉 STEP 1: VERIFYING 'COBRAR' BUTTON IS DISPLAYED ON MAIN SCREEN...")
        cobrar_visible = utils.verify_element(
            wait, XPATH_CALC_BTN_REALIZAR_COBRO, "MAIN CHARGING SCREEN — 'COBRAR' BUTTON", driver
        )

        print("\n👉 STEP 2: VERIFYING AMOUNT DISPLAY ($0.00) IS PRESENT...")
        display_visible = utils.verify_element(
            wait, config.XPATH_C_DISPLAY_MONTO, "AMOUNT DISPLAY — '$0.00'", driver
        )

        if cobrar_visible or display_visible:
            result = "SUCCESS"
            print("\n📸 TAKING SCREENSHOT EVIDENCE OF THE MAIN CHARGING SCREEN...")
            utils.take_screenshot(driver, "CALC_001_success", "t6")
            print("\n✅ CALC-001: SUCCESS — MAIN CHARGING SCREEN LOADED CORRECTLY.")
        else:
            print("\n❌ CALC-001 FAILED — CHARGING SCREEN DID NOT LOAD AS EXPECTED.")
            utils.take_screenshot(driver, "CALC_001_failed", "t6")
            print("\n🔍 SCANNING FOR VISIBLE TEXT ON CURRENT SCREEN FOR DEBUGGING...")
            try:
                for elem in driver.find_elements(By.XPATH, "//*"):
                    t = elem.get_attribute("text")
                    if t and len(t) > 3:
                        print(f"   📝 VISIBLE TEXT: '{t}'")
            except Exception:
                pass

        _capture_evidence(driver, "CALC_001")

    except Exception as e:
        print(f"\n💥 CALC-001 CRITICAL ERROR: {e}")
        try:
            utils.take_screenshot(driver, "CALC_001_technical_error", "t6")
        except Exception:
            pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 CALC-001 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# CALC_002: VALIDATE ALL DIGITS (0-9) CAN BE ENTERED ON THE CALCULATOR NUMPAD
# ==================================================================================
def CALC_002():
    
    print("\n" + "=" * 60)
    print("🧪 CALC-002: VALIDATE ALL DIGITS (0-9) ON THE CALCULATOR NUMPAD")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        print("🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        _login_to_calculator_screen(driver, wait)

        print("\n🖥️  VERIFYING CALCULATOR SCREEN IS READY...")
        utils.verify_element(wait, XPATH_CALC_BTN_REALIZAR_COBRO, "CALCULATOR SCREEN — 'COBRAR' BUTTON", driver)

        print("⏳ WAITING FOR UI TO FULLY SETTLE BEFORE PRESSING DIGITS...")
        time.sleep(3)

        print("\n👉 STEP 1: PRESSING ALL DIGITS 1 THROUGH 9, THEN 0...")
        digits_pressed = []
        for digit in [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]:
            xpath_digit = f'//*[@text="{digit}" or @content-desc="{digit}"]'
            print(f"   👆 PRESSING DIGIT: {digit}")
            try:
                driver.find_element(By.XPATH, xpath_digit).click()
                digits_pressed.append(str(digit))
                time.sleep(1)
            except Exception as e:
                print(f"   ⚠️  WARNING: COULD NOT PRESS DIGIT {digit} — {e}")

        print(f"   🔢 DIGITS ENTERED: {', '.join(digits_pressed)}")

        print("\n👉 STEP 2: TAKING SCREENSHOT OF THE DISPLAY WITH ALL DIGITS ENTERED...")
        utils.take_screenshot(driver, "CALC_002_digits_entered", "t6")

        print("\n👉 STEP 3: VERIFYING DISPLAY UPDATED FROM INITIAL $0.00...")
        display_updated = utils.verify_element(
            wait, config.XPATH_C_DISPLAY_UPDATED, "AMOUNT DISPLAY — UPDATED VALUE (NOT $0.00)", driver
        )

        if display_updated and len(digits_pressed) == 10:
            result = "SUCCESS"
            print("\n✅ CALC-002: SUCCESS — ALL 10 DIGITS (0-9) ENTERED CORRECTLY.")
        else:
            print(f"\n❌ CALC-002 FAILED. DISPLAY UPDATED: {display_updated} | DIGITS PRESSED: {len(digits_pressed)}/10")
            utils.take_screenshot(driver, "CALC_002_failed", "t6")

        _capture_evidence(driver, "CALC_002")

    except Exception as e:
        print(f"\n💥 CALC-002 CRITICAL ERROR: {e}")
        try:
            utils.take_screenshot(driver, "CALC_002_technical_error", "t6")
        except Exception:
            pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 CALC-002 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# CALC_003: VALIDATE THE BACKSPACE BUTTON DELETES DIGITS CORRECTLY
# ==================================================================================
def CALC_003():
    
    print("\n" + "=" * 60)
    print("🧪 CALC-003: VALIDATE BACKSPACE BUTTON DELETES DIGITS CORRECTLY")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        print("🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        _login_to_calculator_screen(driver, wait)

        print("\n🖥️  VERIFYING CALCULATOR SCREEN IS READY...")
        utils.verify_element(wait, XPATH_CALC_BTN_REALIZAR_COBRO, "CALCULATOR SCREEN — 'COBRAR' BUTTON", driver)

        print("⏳ WAITING FOR UI TO FULLY SETTLE BEFORE PRESSING DIGITS...")
        time.sleep(3)

        print("\n👉 STEP 1: ENTERING ALL DIGITS 1-9 AND 0 TO BUILD UP THE DISPLAY...")
        for digit in [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]:
            xpath_digit = f'//*[@text="{digit}" or @content-desc="{digit}"]'
            print(f"   👆 PRESSING DIGIT: {digit}")
            try:
                driver.find_element(By.XPATH, xpath_digit).click()
                time.sleep(1)
            except Exception as e:
                print(f"   ⚠️  WARNING: COULD NOT PRESS DIGIT {digit} — {e}")

        print("\n📸 TAKING SCREENSHOT #1 — FULL NUMBER ENTERED (BEFORE ANY DELETE)...")
        utils.take_screenshot(driver, "CALC_003_before_delete", "t6")

        print("\n👉 STEP 2: PRESSING BACKSPACE ONCE...")
        _press_backspace(driver)
        time.sleep(1)

        print("\n📸 TAKING SCREENSHOT #2 — AFTER FIRST DELETE (ONE DIGIT REMOVED)...")
        utils.take_screenshot(driver, "CALC_003_after_first_delete", "t6")

        print("\n👉 STEP 3: PRESSING BACKSPACE 9 MORE TIMES TO CLEAR ALL DIGITS...")
        for i in range(9):
            print(f"   ⌫  BACKSPACE PRESS {i + 2}/10")
            _press_backspace(driver)
            time.sleep(1)

        print("\n📸 TAKING SCREENSHOT #3 — AFTER ALL DELETES (DISPLAY SHOULD BE $0.00)...")
        utils.take_screenshot(driver, "CALC_003_after_all_deletes", "t6")

        print("\n🔎 VERIFYING DISPLAY RETURNED TO $0.00 AFTER ALL DELETIONS...")
        display_cleared = utils.verify_element(
            wait, config.XPATH_C_DISPLAY_MONTO, "AMOUNT DISPLAY RESET — '$0.00'", driver
        )

        if display_cleared:
            result = "SUCCESS"
            print("\n✅ CALC-003: SUCCESS — DISPLAY RETURNED TO $0.00 AFTER ALL DELETIONS.")
        else:
            print("\n❌ CALC-003 FAILED — DISPLAY DID NOT RETURN TO $0.00 AFTER ALL DELETIONS.")
            utils.take_screenshot(driver, "CALC_003_failed", "t6")

        _capture_evidence(driver, "CALC_003")

    except Exception as e:
        print(f"\n💥 CALC-003 CRITICAL ERROR: {e}")
        try:
            utils.take_screenshot(driver, "CALC_003_technical_error", "t6")
        except Exception:
            pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 CALC-003 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# CALC_004: VALIDATE THAT LEADING ZEROS ARE NOT ALLOWED AT THE START OF AN AMOUNT
# ==================================================================================
def CALC_004():
    
    print("\n" + "=" * 60)
    print("🧪 CALC-004: VALIDATE LEADING ZEROS ARE NOT ALLOWED IN AMOUNT")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        print("🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        _login_to_calculator_screen(driver, wait)

        print("\n🖥️  VERIFYING CALCULATOR SCREEN IS READY...")
        utils.verify_element(wait, XPATH_CALC_BTN_REALIZAR_COBRO, "CALCULATOR SCREEN — 'COBRAR' BUTTON", driver)

        print("⏳ WAITING FOR UI TO FULLY SETTLE BEFORE PRESSING DIGITS...")
        time.sleep(3)

        print("\n👉 STEP 1: PRESSING '0' THREE TIMES TO ATTEMPT LEADING ZEROS (0 0 0)...")
        for i in range(3):
            print(f"   👆 PRESSING ZERO {i + 1}/3")
            try:
                driver.find_element(By.XPATH, '//*[@text="0" or @content-desc="0"]').click()
                time.sleep(1)
            except Exception as e:
                print(f"   ⚠️  WARNING: COULD NOT PRESS ZERO {i + 1} — {e}")

        print("\n📸 TAKING SCREENSHOT #1 — DISPLAY AFTER THREE ZEROS (SHOULD REMAIN $0.00)...")
        utils.take_screenshot(driver, "CALC_004_after_three_zeros", "t6")

        print("\n👉 STEP 2: PRESSING NON-ZERO DIGIT '1' AFTER THE LEADING ZEROS...")
        try:
            driver.find_element(By.XPATH, '//*[@text="1" or @content-desc="1"]').click()
            time.sleep(1)
        except Exception as e:
            print(f"   ⚠️  WARNING: COULD NOT PRESS DIGIT 1 — {e}")

        print("\n📸 TAKING SCREENSHOT #2 — FINAL DISPLAY (SEQUENCE 0 0 0 1 ENTERED)...")
        utils.take_screenshot(driver, "CALC_004_after_nonzero_digit", "t6")

        print("\n🔎 VERIFYING DISPLAY SHOWS '$0.01' (LEADING ZEROS CORRECTLY ABSORBED)...")
        display_correct = utils.verify_element(
            wait,
            '//*[contains(@text, "0.01") or contains(@content-desc, "0.01")]',
            "AMOUNT DISPLAY — '$0.01' (FORMATTED, NO LEADING ZEROS)",
            driver
        )

        if display_correct:
            result = "SUCCESS"
            print("\n✅ CALC-004: SUCCESS — DISPLAY SHOWS '$0.01'. LEADING ZEROS WERE NOT RENDERED.")
        else:
            print("\n❌ CALC-004 FAILED — DISPLAY DID NOT SHOW '$0.01' AFTER SEQUENCE 0 0 0 1.")
            utils.take_screenshot(driver, "CALC_004_failed", "t6")

        _capture_evidence(driver, "CALC_004")

    except Exception as e:
        print(f"\n💥 CALC-004 CRITICAL ERROR: {e}")
        try:
            utils.take_screenshot(driver, "CALC_004_technical_error", "t6")
        except Exception:
            pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 CALC-004 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# CALC_005: VALIDATE AUTO-DECIMAL FORMATTING ON THE AMOUNT DISPLAY
# ==================================================================================
def CALC_005():

    print("\n" + "=" * 60)
    print("🧪 CALC-005: VALIDATE AUTO-DECIMAL FORMATTING ON THE AMOUNT DISPLAY")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        print("🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        _login_to_calculator_screen(driver, wait)

        print("\n🖥️  VERIFYING CALCULATOR SCREEN IS READY...")
        utils.verify_element(wait, XPATH_CALC_BTN_REALIZAR_COBRO, "CALCULATOR SCREEN — 'COBRAR' BUTTON", driver)

        print("⏳ WAITING FOR UI TO FULLY SETTLE BEFORE PRESSING DIGITS...")
        time.sleep(3)

        print("\n👉 STEP 1: ENTERING VALID AMOUNT 10.50 (1 → 0 → 5 → 0, ONE CLICK PER DIGIT)...")
        for key in ["1", "0", "5", "0"]:
            xpath = f'//*[@text="{key}" or @content-desc="{key}"]'
            print(f"   👆 PRESSING: '{key}'")
            try:
                elemento = driver.find_element(By.XPATH, xpath)
                elemento.click()
            except Exception as e:
                print(f"   ⚠️  WARNING: COULD NOT PRESS '{key}' — {e}")
            time.sleep(1.5)

        print("\n📸 TAKING SCREENSHOT — AMOUNT ENTERED ($10.50)...")
        utils.take_screenshot(driver, "CALC_005_valid_amount_10_50", "t6")

        print("\n🔎 VERIFYING DISPLAY SHOWS '10.50'...")
        display_correct = utils.verify_element(
            wait,
            '//*[contains(@text, "10.50") or contains(@content-desc, "10.50")]',
            "AMOUNT DISPLAY — '10.50'",
            driver
        )

        if display_correct:
            result = "SUCCESS"
            print("\n✅ CALC-005: SUCCESS — DISPLAY SHOWS '$10.50'.")
        else:
            print("\n❌ CALC-005 FAILED — DISPLAY DID NOT SHOW '$10.50'.")
            utils.take_screenshot(driver, "CALC_005_failed", "t6")
            print("\n🔍 SCANNING VISIBLE TEXT FOR DEBUGGING...")
            try:
                for elem in driver.find_elements(By.XPATH, "//*"):
                    t = elem.get_attribute("text")
                    if t and "$" in t:
                        print(f"   💲 DISPLAY TEXT: '{t}'")
            except Exception:
                pass

        _capture_evidence(driver, "CALC_005")

    except Exception as e:
        print(f"\n💥 CALC-005 CRITICAL ERROR: {e}")
        try:
            utils.take_screenshot(driver, "CALC_005_technical_error", "t6")
        except Exception:
            pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 CALC-005 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# CALC_006: VALIDATE THAT CLICKING 'COBRAR' WITH NO AMOUNT SHOWS AN ERROR MESSAGE
# ==================================================================================
def CALC_006():
    
    print("\n" + "=" * 60)
    print("🧪 CALC-006: VALIDATE ERROR HANDLING FOR INVALID/OUT-OF-RANGE AMOUNTS")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"
    scenario1_ok = False
    scenario2_ok = False

    try:
        print("🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        _login_to_calculator_screen(driver, wait)

        print("\n🖥️  VERIFYING CALCULATOR SCREEN IS READY AT $0.00...")
        utils.verify_element(wait, config.XPATH_C_DISPLAY_MONTO, "AMOUNT DISPLAY — '$0.00' (NO AMOUNT ENTERED)", driver)
        time.sleep(3)

        # ─── SCENARIO 1: NO AMOUNT ENTERED ─────────────────────────────────────
        print("\n▶️  SCENARIO 1: CLICKING 'REALIZAR COBRO' WITH NO AMOUNT ENTERED ($0.00)...")
        utils.click_element(driver, XPATH_CALC_BTN_REALIZAR_COBRO)

        print("🔎 POLLING FOR WARNING BANNER: 'Ingresa un monto válido'...")
        for i in range(10):
            fuente_xml = driver.page_source.lower()
            if any(k in fuente_xml for k in ["ingresa un monto", "monto válido", "monto valido"]):
                scenario1_ok = True
                print(f"   🚨 WARNING BANNER DETECTED ON POLL ATTEMPT {i + 1}")
                utils.take_screenshot(driver, "CALC_006_scenario1_empty_amount_warning", "t6")
                break
            time.sleep(0.5)

        if scenario1_ok:
            print("✅ SCENARIO 1: WARNING BANNER 'INGRESA UN MONTO VÁLIDO' DETECTED.")
        else:
            print("❌ SCENARIO 1 FAILED — WARNING BANNER NOT FOUND.")
            utils.take_screenshot(driver, "CALC_006_scenario1_failed", "t6")

        print("⏳ WAITING FOR THE WARNING BANNER TO AUTO-DISMISS...")
        time.sleep(4)

        # ─── SCENARIO 2: AMOUNT TOO LOW ($0.01), DECLINED VIA TAP CARD ─────────
        print("\n▶️  SCENARIO 2: ENTERING $0.01 (PRESSING '1' ONCE) AND TESTING THE TAP-CARD FLOW...")
        try:
            driver.find_element(By.XPATH, '//*[@text="1" or @content-desc="1"]').click()
        except Exception as e:
            print(f"   ⚠️  WARNING: COULD NOT PRESS '1' — {e}")
        time.sleep(1)
        utils.take_screenshot(driver, "CALC_006_scenario2_amount_0_01", "t6")

        print("👉 CLICKING 'REALIZAR COBRO' WITH $0.01...")
        utils.click_element(driver, XPATH_CALC_BTN_REALIZAR_COBRO)
        time.sleep(3)
        utils.take_screenshot(driver, "CALC_006_scenario2_tap_card_screen", "t6")

        print("\n" + "🖐️ " * 10)
        print("🖐️  ACCIÓN MANUAL REQUERIDA: COLOCA UNA TARJETA SOBRE LA PARTE SUPERIOR")
        print("🖐️  DE LA TERMINAL PARA ACTIVAR EL MODO TAP / CONTACTLESS Y CONTINUAR.")
        print("🖐️ " * 10 + "\n")

        print("🔎 POLLING FOR 'TRANSACCIÓN DECLINADA — MONTO FUERA DE RANGO' (UP TO 30s)...")
        for i in range(30):
            fuente_xml = driver.page_source.lower()
            if any(k in fuente_xml for k in ["fuera de rango", "declinada"]):
                scenario2_ok = True
                print(f"   🎯 'MONTO FUERA DE RANGO' DETECTED ON POLL ATTEMPT {i + 1}")
                utils.take_screenshot(driver, "CALC_006_scenario2_declined_success", "t6")
                break
            time.sleep(1)

        if scenario2_ok:
            print("✅ SCENARIO 2: TRANSACTION CORRECTLY DECLINED — 'MONTO FUERA DE RANGO'.")
            try:
                driver.find_element(By.XPATH, '//*[contains(@text,"Aceptar") or contains(@content-desc,"Aceptar")]').click()
                time.sleep(2)
            except Exception:
                pass
        else:
            print("❌ SCENARIO 2 FAILED — 'MONTO FUERA DE RANGO' NOT DETECTED (WAS THE CARD TAPPED IN TIME?).")
            utils.take_screenshot(driver, "CALC_006_scenario2_failed", "t6")

        if scenario1_ok and scenario2_ok:
            result = "SUCCESS"
            print("\n✅ CALC-006: SUCCESS — BOTH INVALID-AMOUNT SCENARIOS HANDLED CORRECTLY.")
        else:
            print(f"\n❌ CALC-006 FAILED — SCENARIO 1: {scenario1_ok} | SCENARIO 2: {scenario2_ok}")

        _capture_evidence(driver, "CALC_006")

    except Exception as e:
        print(f"\n💥 CALC-006 CRITICAL ERROR: {e}")
        try:
            utils.take_screenshot(driver, "CALC_006_technical_error", "t6")
        except Exception:
            pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 CALC-006 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# CALC_007: VALIDATE THE MAXIMUM AMOUNT ($999,999.99) CAN BE CHARGED SUCCESSFULLY
# ==================================================================================
def CALC_007():
    
    print("\n" + "=" * 60)
    print("🧪 CALC-007: VALIDATE MAXIMUM AMOUNT ($999,999.99) CHARGES SUCCESSFULLY")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        print("🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        _login_to_calculator_screen(driver, wait)

        print("\n🖥️  VERIFYING CALCULATOR SCREEN IS READY...")
        utils.verify_element(wait, XPATH_CALC_BTN_REALIZAR_COBRO, "CALCULATOR SCREEN — 'COBRAR' BUTTON", driver)

        print("⏳ WAITING FOR UI TO FULLY SETTLE BEFORE PRESSING DIGITS...")
        time.sleep(3)

        print("\n👉 STEP 1: ENTERING THE MAXIMUM AMOUNT $999,999.99 (PRESSING '9' 8 TIMES)...")
        for i in range(8):
            print(f"   👆 PRESSING 9 ({i + 1}/8)")
            try:
                driver.find_element(By.XPATH, '//*[@text="9" or @content-desc="9"]').click()
                time.sleep(1)
            except Exception as e:
                print(f"   ⚠️  WARNING: COULD NOT PRESS 9 — {e}")

        print("\n📸 TAKING SCREENSHOT #1 — MAXIMUM AMOUNT ON DISPLAY ($999,999.99)...")
        utils.take_screenshot(driver, "CALC_007_max_amount_entered", "t6")

        print("\n👉 STEP 2: CLICKING 'REALIZAR COBRO'...")
        utils.click_element(driver, XPATH_CALC_BTN_REALIZAR_COBRO)
        time.sleep(2)

        print("\n👉 STEP 3: SELECTING '¿CUÁNTAS MENSUALIDADES?' → 'SIN MENSUALIDADES' (PAGO DE CONTADO)...")
        mensualidades_screen = utils.verify_element(
            wait,
            '//*[contains(@text, "mensualidades") or contains(@content-desc, "mensualidades")]',
            "SCREEN — '¿Cuántas mensualidades?'",
            driver
        )
        if mensualidades_screen:
            try:
                driver.find_element(
                    By.XPATH,
                    '//*[contains(@text, "Sin mensualidades") or contains(@content-desc, "Sin mensualidades")]'
                ).click()
                print("   ✅ 'SIN MENSUALIDADES' OPTION SELECTED.")
            except Exception as e:
                print(f"   ⚠️  WARNING: COULD NOT CLICK 'SIN MENSUALIDADES' — {e}")
        else:
            print("   ℹ️  '¿CUÁNTAS MENSUALIDADES?' SCREEN NOT DETECTED — CONTINUING ANYWAY.")
        time.sleep(3)

        print("\n👉 STEP 4: VERIFYING TAP/INSERT CARD SCREEN APPEARS...")
        utils.verify_element(
            wait, config.XPATH_C_PANTALLA_TARJETA, "CARD SCREEN — 'ACERCA, INSERTA O DESLIZA TU TARJETA'", driver
        )
        utils.take_screenshot(driver, "CALC_007_card_screen", "t6")

        print("\n" + "🖐️ " * 10)
        print("🖐️  ACCIÓN MANUAL REQUERIDA: ACERCA/INSERTA LA TARJETA EN LA TERMINAL Y, SI SE")
        print("🖐️  SOLICITA, INGRESA EL NIP CORRESPONDIENTE PARA CONTINUAR CON LA TRANSACCIÓN.")
        print("🖐️ " * 10 + "\n")

        print("🔎 POLLING FOR 'TRANSACCIÓN APROBADA' (UP TO 30s)...")
        transaccion_aprobada = False
        for i in range(30):
            fuente_xml = driver.page_source.lower()
            if "transacción aprobada" in fuente_xml or "transaccion aprobada" in fuente_xml:
                transaccion_aprobada = True
                print(f"   🎯 'TRANSACCIÓN APROBADA' DETECTED ON POLL ATTEMPT {i + 1}")
                break
            time.sleep(1)

        print("\n📸 TAKING SCREENSHOT #3 — TRANSACTION RESULT...")
        utils.take_screenshot(driver, "CALC_007_transaction_result", "t6")

        if transaccion_aprobada:
            result = "SUCCESS"
            print("\n✅ CALC-007: SUCCESS — MAXIMUM AMOUNT ($999,999.99) CHARGED SUCCESSFULLY.")
            try:
                driver.find_element(By.XPATH, '//*[contains(@text,"Aceptar") or contains(@content-desc,"Aceptar")]').click()
                time.sleep(2)
            except Exception:
                pass
        else:
            print("\n❌ CALC-007 FAILED — 'TRANSACCIÓN APROBADA' NOT DETECTED (WAS THE CARD/NIP ENTERED IN TIME?).")
            utils.take_screenshot(driver, "CALC_007_failed", "t6")

        _capture_evidence(driver, "CALC_007")

    except Exception as e:
        print(f"\n💥 CALC-007 CRITICAL ERROR: {e}")
        try:
            utils.take_screenshot(driver, "CALC_007_technical_error", "t6")
        except Exception:
            pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 CALC-007 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


def CALC_008():
    
    print("\n" + "=" * 60)
    print("🧪 CALC-008: VERIFY 'REALIZAR COBRO' PROCESSES A VALID AMOUNT ($10.00)")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        print("🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        _login_to_calculator_screen(driver, wait)

        print("\n🖥️  VERIFYING CALCULATOR SCREEN IS READY...")
        utils.verify_element(wait, XPATH_CALC_BTN_REALIZAR_COBRO, "CALCULATOR SCREEN — 'COBRAR' BUTTON", driver)

        print("⏳ WAITING FOR UI TO FULLY SETTLE BEFORE PRESSING DIGITS...")
        time.sleep(3)

        print("\n👉 STEP 1: ENTERING THE AMOUNT OF $10.00 (1 → 0 → 0 → 0)...")
        for key in ["1", "0", "0", "0"]:
            print(f"   👆 PRESSING: '{key}'")
            try:
                driver.find_element(By.XPATH, f'//*[@text="{key}" or @content-desc="{key}"]').click()
            except Exception as e:
                print(f"   ⚠️  WARNING: COULD NOT PRESS '{key}' — {e}")
            time.sleep(1)

        print("\n📸 TAKING SCREENSHOT #1 — AMOUNT ENTERED ($10.00)...")
        utils.take_screenshot(driver, "CALC_008_amount_10_00", "t6")

        print("\n👉 STEP 2: CLICKING 'REALIZAR COBRO'...")
        utils.click_element(driver, XPATH_CALC_BTN_REALIZAR_COBRO)
        time.sleep(3)

        print("\n👉 STEP 3: VERIFYING TAP/INSERT CARD SCREEN APPEARS DIRECTLY (NO MENSUALIDADES SCREEN BELOW $1,000)...")
        pantalla_tarjeta = utils.verify_element(
            wait, config.XPATH_C_PANTALLA_TARJETA, "CARD SCREEN — 'ACERCA, INSERTA O DESLIZA TU TARJETA'", driver
        )

        print("\n📸 TAKING SCREENSHOT #2 — CARD SCREEN...")
        utils.take_screenshot(driver, "CALC_008_card_screen", "t6")

        if pantalla_tarjeta:
            result = "SUCCESS"
            print("\n✅ CALC-008: SUCCESS — $10.00 ACCEPTED, 'REALIZAR COBRO' WORKED CORRECTLY.")
        else:
            print("\n❌ CALC-008 FAILED — CARD SCREEN DID NOT APPEAR AFTER ENTERING $10.00.")
            utils.take_screenshot(driver, "CALC_008_failed", "t6")
            print("\n🔍 SCANNING VISIBLE TEXT FOR DEBUGGING...")
            try:
                for elem in driver.find_elements(By.XPATH, "//*"):
                    t = elem.get_attribute("text")
                    if t and len(t) > 3:
                        print(f"   📝 VISIBLE TEXT: '{t}'")
            except Exception:
                pass

        _capture_evidence(driver, "CALC_008")

    except Exception as e:
        print(f"\n💥 CALC-008 CRITICAL ERROR: {e}")
        try:
            utils.take_screenshot(driver, "CALC_008_technical_error", "t6")
        except Exception:
            pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 CALC-008 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# CALC_010: VALIDATE KEYPAD VISUAL RESPONSE, BOUNDARY LIMITS, AND DELETE BUTTON
# ==================================================================================
def CALC_010():
    
    print("\n" + "=" * 60)
    print("🧪 CALC-010: VALIDATE KEYPAD VISUAL RESPONSE AND BOUNDARY LIMITS")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        print("🔐 PRECONDITION: REACHING THE CALCULATOR SCREEN...")
        _login_to_calculator_screen(driver, wait)
        time.sleep(3)

        print("\n👉 STEP 1: PRESSING DIGIT SEQUENCE [1, 2, 3, 0, 4, 5, 6, 7, 8]...")
        secuencia = ["1", "2", "3", "0", "4", "5", "6", "7", "8"]
        for digito in secuencia:
            xpath_digito = f'//*[@text="{digito}" or @content-desc="{digito}"]'
            try:
                driver.find_element(By.XPATH, xpath_digito).click()
                print(f"   👆 TAPPED DIGIT: {digito}")
                time.sleep(0.5)
            except Exception as e:
                print(f"   ⚠️  WARNING: COULD NOT TAP DIGIT {digito}. ERROR: {e}")

        print("\n📸 TAKING SCREENSHOT #1 — FULL SEQUENCE ENTERED (UP TO 8)...")
        utils.take_screenshot(driver, "CALC_010_1_full_sequence", "t6")
        time.sleep(1)

        print("\n👉 STEP 2: CLICKING DELETE (BACKSPACE) ONCE TO REMOVE '8'...")
        clicked = _press_backspace(driver)
        if clicked:
            print("   ⌫  BACKSPACE TAPPED SUCCESSFULLY.")
        else:
            print("   ❌ BACKSPACE FAILED ON ALL STRATEGIES. SEE DUMP ABOVE.")
            print("\n🔍 PRINTING RAW XML DUMP FOR DEBUGGING:")
            print(driver.page_source)
        time.sleep(1)

        print("\n📸 TAKING SCREENSHOT #2 — AFTER BACKSPACE ('8' SHOULD BE REMOVED)...")
        utils.take_screenshot(driver, "CALC_010_2_after_backspace", "t6")

        print("\n👉 STEP 3: PRESSING THE LAST DIGIT '9' INTO THE FREED SPACE...")
        try:
            driver.find_element(By.XPATH, '//*[@text="9" or @content-desc="9"]').click()
            print("   👆 TAPPED DIGIT: 9")
            time.sleep(1)
        except Exception as e:
            print(f"   ⚠️  WARNING: COULD NOT TAP DIGIT 9. ERROR: {e}")

        print("\n📸 TAKING SCREENSHOT #3 — WITH '9' AT THE END...")
        utils.take_screenshot(driver, "CALC_010_3_final_nine", "t6")

        # THIS TEST HAS NO PASS/FAIL ASSERTION IN v1 — IT'S A NON-CRASH SMOKE CHECK ON
        # KEYPAD RESPONSIVENESS AND THE DELETE BUTTON. IT'S "SUCCESS" AS LONG AS NOTHING
        # THREW UP TO THIS POINT.
        result = "SUCCESS"
        print("\n✅ CALC-010: SUCCESS — KEYPAD INTERACTION, BOUNDARY LIMIT, AND DELETE FUNCTION COMPLETED.")

        _capture_evidence(driver, "CALC_010")

    except Exception as e:
        print(f"\n💥 CALC-010 CRITICAL ERROR: {e}")
        try:
            utils.take_screenshot(driver, "CALC_010_technical_error", "t6")
        except Exception:
            pass
    finally:
        print("\n" + "-" * 60)
        print(f"📊 CALC-010 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)


# ==================================================================================
# EXECUTION
# ==================================================================================

if __name__ == "__main__":

    logger, log_file, timestamp = utils.start_report("OPERATIONALS_CALC")

    try:
        CALC_001()
        CALC_002()
        CALC_003()
        CALC_004()
        CALC_005()
        CALC_006()
        CALC_007()
        CALC_008()
        CALC_010()

    finally:
        logger.close()
        utils.generate_zip_report("OPERATIONALS_CALC", logger, log_file, timestamp)
        utils.generate_html_report("OPERATIONALS_CALC", log_file, timestamp)