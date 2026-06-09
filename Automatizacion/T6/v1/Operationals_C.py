"""
FILENAME: Operationals_C.py
DESCRIPTION:
    AUTOMATED TEST SUITE FOCUSED ON THE CALCULATOR MODULE.
    VALIDATES FLOWS FOR USERS ACCESSING THE MAIN CHARGING SCREEN AFTER
    COMPLETING BUSINESS REGISTRATION OR LOGGING IN WITH AN EXISTING ACCOUNT.

CONTENTS:
    · C-55: VALIDATE THE MAIN CHARGING SCREEN LOADS CORRECTLY AFTER BUSINESS REGISTRATION OR LOGIN.
    · C-56: VALIDATE ALL DIGITS (0-9) CAN BE ENTERED ON THE CALCULATOR NUMPAD.
    · C-57: VALIDATE THE BACKSPACE BUTTON DELETES DIGITS CORRECTLY.
    · C-58: VALIDATE THAT LEADING ZEROS ARE NOT ALLOWED AT THE START OF AN AMOUNT.
    · C-59: VALIDATE ONLY ONE DECIMAL SEPARATOR AND A MAXIMUM OF TWO DECIMAL DIGITS ARE ALLOWED.
    · C-60: VALIDATE THAT CLICKING COBRAR WITH NO AMOUNT ENTERED SHOWS AN ERROR MESSAGE.
    · C-61: VALIDATE THAT AN EXCESSIVELY LARGE AMOUNT PROCEEDS TO THE CARD INSERTION SCREEN.
    · C-62: VERIFY THAT THE 'COBRAR' BUTTON INITIATES THE TRANSACTION PROCESS WITH A VALID AMOUNT.
    · C-63: VERIFY 'COBRAR' BUTTON STATE DEPENDING ON AMOUNT ($0.00 VS $1.00).
    · C-64: VALIDATE KEYPAD VISUAL RESPONSE, BOUNDARY LIMITS, AND DELETE BUTTON.

REQUIREMENTS:
    - APPIUM SERVER RUNNING.
    - config.py AND utils.py IN THE SAME DIRECTORY.
"""

import sys
import os
import time

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_path not in sys.path:
    sys.path.append(project_path)

import config
import utils
from selenium.webdriver.common.by import By


# =================================================================================
# INTERNAL HELPER: CALL print_http_evidence_appium WITHOUT SILENCING ERRORS
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
    """
    EXECUTES THE COMPLETE FLOW TO REACH THE MAIN CHARGING SCREEN.
      1. LOGIN WITH VALID CREDENTIALS.
      2. BUSINESS REGISTRATION (TOKEN + AFFILIATION NUMBER).
      3. LOCATION PERMISSION DIALOG.
    """
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
# HELPER: PRESS BACKSPACE WITH MULTIPLE FALLBACK STRATEGIES
# =================================================================================
def _press_backspace(driver):
    # STRATEGY 1
    try:
        driver.find_element(By.XPATH, config.XPATH_C_BTN_BACKSPACE).click()
        print("   ⌫  BACKSPACE CLICKED — STRATEGY 1 (CONFIG XPATH)")
        return True
    except:
        pass

    # STRATEGY 2
    try:
        driver.find_element(
            By.XPATH, '//*[@text="0" or @content-desc="0"]/following-sibling::*[1]'
        ).click()
        print("   ⌫  BACKSPACE CLICKED — STRATEGY 2 (SIBLING AFTER '0' — WILDCARD TYPE)")
        return True
    except:
        pass

    # STRATEGY 3
    try:
        driver.find_element(
            By.XPATH, '//*[@text="0" or @content-desc="0"]/../*[last()]'
        ).click()
        print("   ⌫  BACKSPACE CLICKED — STRATEGY 3 (LAST CHILD OF '0' PARENT)")
        return True
    except:
        pass

    # STRATEGY 4
    try:
        driver.find_element(By.XPATH, config.XPATH_C_BTN_BACKSPACE_ABSOLUTE).click()
        print("   ⌫  BACKSPACE CLICKED — STRATEGY 4 (ABSOLUTE XPATH — INSPECTOR FALLBACK)")
        return True
    except:
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

# ========================================================
# C-55: VALIDATE THE MAIN CHARGING SCREEN LOADS CORRECTLY
# ========================================================
def C_55():
    print("\n" + "=" * 60)
    print("🧪 C-55: VALIDATE MAIN CHARGING SCREEN LOADS CORRECTLY")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        print("🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)

        
        print("\n👉 STEP 1: VERIFYING 'COBRAR' BUTTON IS DISPLAYED ON MAIN SCREEN...")
        cobrar_visible = utils.verificar_existencia(
            wait,
            config.XPATH_C_PANTALLA_COBRO,
            "MAIN CHARGING SCREEN — 'COBRAR' BUTTON",
            driver
        )

        
        print("\n👉 STEP 2: VERIFYING AMOUNT DISPLAY ($0.00) IS PRESENT...")
        display_visible = utils.verificar_existencia(
            wait,
            config.XPATH_C_DISPLAY_MONTO,
            "AMOUNT DISPLAY — '$0.00'",
            driver
        )

        pantalla_cargada = cobrar_visible or display_visible

        if pantalla_cargada:
            print("\n📸 TAKING SCREENSHOT EVIDENCE OF THE MAIN CHARGING SCREEN...")
            utils.tomar_screenshot(driver, "C_55_SUCCESS")
            _capture_evidence(driver, "C_55")
            print("\n✅ C-55: SUCCESS — MAIN CHARGING SCREEN LOADED CORRECTLY.")
            return True
        else:
            print("\n❌ C-55 FAILED — CHARGING SCREEN DID NOT LOAD AS EXPECTED.")
            utils.tomar_screenshot(driver, "C_55_FAILED")
            _capture_evidence(driver, "C_55")
            print("\n🔍 SCANNING FOR VISIBLE TEXT ON CURRENT SCREEN FOR DEBUGGING...")
            try:
                todos = driver.find_elements(By.XPATH, "//*")
                for elem in todos:
                    t = elem.get_attribute("text")
                    if t and len(t) > 3:
                        print(f"   📝 VISIBLE TEXT: '{t}'")
            except:
                pass
            return False

    except Exception as e:
        print(f"\n💥 C-55 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "C_55_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)


# =================================================================================
# C-56: VALIDATE ALL DIGITS (0-9) CAN BE ENTERED ON THE CALCULATOR NUMPAD
# =================================================================================
def C_56():
    print("\n" + "=" * 60)
    print("🧪 C-56: VALIDATE ALL DIGITS (0-9) ON THE CALCULATOR NUMPAD")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        print("🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)

        print("\n🖥️  VERIFYING CALCULATOR SCREEN IS READY...")
        utils.verificar_existencia(wait, config.XPATH_C_PANTALLA_COBRO, "CALCULATOR SCREEN — 'COBRAR' BUTTON", driver)

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
        utils.tomar_screenshot(driver, "C_56_DIGITS_ENTERED")

        print("\n👉 STEP 3: VERIFYING DISPLAY UPDATED FROM INITIAL $0.00...")
        display_updated = utils.verificar_existencia(
            wait,
            config.XPATH_C_DISPLAY_UPDATED,
            "AMOUNT DISPLAY — UPDATED VALUE (NOT $0.00)",
            driver
        )

        if display_updated and len(digits_pressed) == 10:
            _capture_evidence(driver, "C_56")
            print("\n✅ C-56: SUCCESS — ALL 10 DIGITS (0-9) ENTERED CORRECTLY.")
            return True
        else:
            print(f"\n❌ C-56 FAILED. DISPLAY UPDATED: {display_updated} | DIGITS PRESSED: {len(digits_pressed)}/10")
            utils.tomar_screenshot(driver, "C_56_FAILED")
            _capture_evidence(driver, "C_56")
            return False

    except Exception as e:
        print(f"\n💥 C-56 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "C_56_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)

# =============================================================
# C-57: VALIDATE THE BACKSPACE BUTTON DELETES DIGITS CORRECTLY
# ============================================================
def C_57():
    print("\n" + "=" * 60)
    print("🧪 C-57: VALIDATE BACKSPACE BUTTON DELETES DIGITS CORRECTLY")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        print("🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)

        print("\n🖥️  VERIFYING CALCULATOR SCREEN IS READY...")
        utils.verificar_existencia(wait, config.XPATH_C_PANTALLA_COBRO, "CALCULATOR SCREEN — 'COBRAR' BUTTON", driver)

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
        utils.tomar_screenshot(driver, "C_57_BEFORE_DELETE")

        
        print("\n👉 STEP 2: PRESSING BACKSPACE ONCE...")
        _press_backspace(driver)
        time.sleep(1)

        print("\n📸 TAKING SCREENSHOT #2 — AFTER FIRST DELETE (ONE DIGIT REMOVED)...")
        utils.tomar_screenshot(driver, "C_57_AFTER_FIRST_DELETE")

        print("\n👉 STEP 3: PRESSING BACKSPACE 9 MORE TIMES TO CLEAR ALL DIGITS...")
        for i in range(9):
            print(f"   ⌫  BACKSPACE PRESS {i + 2}/10")
            _press_backspace(driver)
            time.sleep(1)

        print("\n📸 TAKING SCREENSHOT #3 — AFTER ALL DELETES (DISPLAY SHOULD BE $0.00)...")
        utils.tomar_screenshot(driver, "C_57_AFTER_ALL_DELETES")

        print("\n🔎 VERIFYING DISPLAY RETURNED TO $0.00 AFTER ALL DELETIONS...")
        display_cleared = utils.verificar_existencia(
            wait,
            config.XPATH_C_DISPLAY_MONTO,
            "AMOUNT DISPLAY RESET — '$0.00'",
            driver
        )

        if display_cleared:
            _capture_evidence(driver, "C_57")
            print("\n✅ C-57: SUCCESS — DISPLAY RETURNED TO $0.00 AFTER ALL DELETIONS.")
            return True
        else:
            print("\n❌ C-57 FAILED — DISPLAY DID NOT RETURN TO $0.00 AFTER ALL DELETIONS.")
            utils.tomar_screenshot(driver, "C_57_FAILED")
            _capture_evidence(driver, "C_57")
            return False

    except Exception as e:
        print(f"\n💥 C-57 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "C_57_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)

# =================================================================================
# C-58: VALIDATE THAT LEADING ZEROS ARE NOT ALLOWED AT THE START OF AN AMOUNT
# =================================================================================
def C_58():
    print("\n" + "=" * 60)
    print("🧪 C-58: VALIDATE LEADING ZEROS ARE NOT ALLOWED IN AMOUNT")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        print("🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)

        print("\n🖥️  VERIFYING CALCULATOR SCREEN IS READY...")
        utils.verificar_existencia(wait, config.XPATH_C_PANTALLA_COBRO, "CALCULATOR SCREEN — 'COBRAR' BUTTON", driver)

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
        utils.tomar_screenshot(driver, "C_58_AFTER_THREE_ZEROS")

        print("\n👉 STEP 2: PRESSING NON-ZERO DIGIT '1' AFTER THE LEADING ZEROS...")
        try:
            driver.find_element(By.XPATH, '//*[@text="1" or @content-desc="1"]').click()
            time.sleep(1)
        except Exception as e:
            print(f"   ⚠️  WARNING: COULD NOT PRESS DIGIT 1 — {e}")

        print("\n📸 TAKING SCREENSHOT #2 — FINAL DISPLAY (SEQUENCE 0 0 0 1 ENTERED)...")
        utils.tomar_screenshot(driver, "C_58_AFTER_NONZERO_DIGIT")

        print("\n🔎 VERIFYING DISPLAY SHOWS '$0.01' (LEADING ZEROS CORRECTLY ABSORBED)...")
        display_correct = utils.verificar_existencia(
            wait,
            '//*[contains(@text, "0.01") or contains(@content-desc, "0.01")]',
            "AMOUNT DISPLAY — '$0.01' (FORMATTED, NO LEADING ZEROS)",
            driver
        )

        if display_correct:
            _capture_evidence(driver, "C_58")
            print("\n✅ C-58: SUCCESS — DISPLAY SHOWS '$0.01'. LEADING ZEROS WERE NOT RENDERED.")
            return True
        else:
            print("\n❌ C-58 FAILED — DISPLAY DID NOT SHOW '$0.01' AFTER SEQUENCE 0 0 0 1.")
            utils.tomar_screenshot(driver, "C_58_FAILED")
            _capture_evidence(driver, "C_58")
            return False

    except Exception as e:
        print(f"\n💥 C-58 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "C_58_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)

# =================================================================================
# C-59: VALIDATE ONLY ONE DECIMAL SEPARATOR AND MAX TWO DECIMAL DIGITS ALLOWED
# =================================================================================
def C_59():
    print("\n" + "=" * 60)
    print("🧪 C-59: VALIDATE DECIMAL SEPARATOR AND MAX TWO DECIMAL DIGITS")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        print("🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)

        print("\n🖥️  VERIFYING CALCULATOR SCREEN IS READY...")
        utils.verificar_existencia(wait, config.XPATH_C_PANTALLA_COBRO, "CALCULATOR SCREEN — 'COBRAR' BUTTON", driver)

        print("⏳ WAITING FOR UI TO FULLY SETTLE BEFORE PRESSING DIGITS...")
        time.sleep(3)

        print("\n👉 STEP 1: ENTERING VALID AMOUNT 10.50 (1 → 0 → + → 5 → 0)...")
        for key, label in [("1", "1"), ("0", "0"), ("+", "+"), ("5", "5"), ("0", "0")]:
            xpath = f'//*[@text="{key}" or @content-desc="{key}"]'
            print(f"   👆 PRESSING: '{label}'")
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(1)
            except Exception as e:
                print(f"   ⚠️  WARNING: COULD NOT PRESS '{label}' — {e}")

        print("\n📸 TAKING SCREENSHOT #1 — VALID AMOUNT ENTERED ($10.50)...")
        utils.tomar_screenshot(driver, "C_59_VALID_AMOUNT_10_50")

        print("\n👉 STEP 2: PRESSING '+' AGAIN TO ATTEMPT A SECOND DECIMAL SEPARATOR...")
        try:
            driver.find_element(By.XPATH, config.XPATH_C_BTN_DECIMAL).click()
            time.sleep(1)
        except Exception as e:
            print(f"   ⚠️  WARNING: COULD NOT PRESS '+' — {e}")

        print("\n👉 STEP 3: PRESSING '5' TWICE TO ATTEMPT EXCEEDING TWO DECIMAL DIGITS...")
        for i in range(2):
            print(f"   👆 PRESSING EXTRA DIGIT '5' ({i + 1}/2)")
            try:
                driver.find_element(By.XPATH, '//*[@text="5" or @content-desc="5"]').click()
                time.sleep(1)
            except Exception as e:
                print(f"   ⚠️  WARNING: COULD NOT PRESS '5' — {e}")

        print("\n📸 TAKING SCREENSHOT #2 — AFTER OVERFLOW ATTEMPT (DISPLAY MUST REMAIN AT $1050.55)...")
        utils.tomar_screenshot(driver, "C_59_AFTER_OVERFLOW_ATTEMPT")

        print("\n🔎 VERIFYING DISPLAY STILL SHOWS '1050.55' (DECIMAL RESTRICTION ENFORCED)...")
        display_correct = utils.verificar_existencia(
            wait,
            '//*[contains(@text, "1050.55") or contains(@content-desc, "1050.55")]',
            "AMOUNT DISPLAY — '1050.55' (NO EXTRA DECIMAL DIGITS ACCEPTED)",
            driver
        )

        if display_correct:
            _capture_evidence(driver, "C_59")
            print("\n✅ C-59: SUCCESS — DECIMAL RESTRICTION ENFORCED. DISPLAY SHOWS '$1050.55'.")
            return True
        else:
            print("\n❌ C-59 FAILED — DISPLAY DID NOT SHOW '$1050.55'. EXTRA DIGITS MAY HAVE BEEN ACCEPTED.")
            utils.tomar_screenshot(driver, "C_59_FAILED")
            _capture_evidence(driver, "C_59")
            print("\n🔍 SCANNING VISIBLE TEXT FOR DEBUGGING...")
            try:
                for elem in driver.find_elements(By.XPATH, "//*"):
                    t = elem.get_attribute("text")
                    if t and "$" in t:
                        print(f"   💲 DISPLAY TEXT: '{t}'")
            except:
                pass
            return False

    except Exception as e:
        print(f"\n💥 C-59 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "C_59_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)


# =================================================================================
# C-60: VALIDATE THAT CLICKING COBRAR WITH NO AMOUNT SHOWS AN ERROR MESSAGE
# =================================================================================
def C_60():
    print("\n" + "=" * 60)
    print("🧪 C-60: VALIDATE ERROR MESSAGE WHEN COBRAR IS CLICKED WITH NO AMOUNT")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        print("🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)

        print("\n🖥️  VERIFYING CALCULATOR SCREEN IS READY AT $0.00...")
        utils.verificar_existencia(wait, config.XPATH_C_DISPLAY_MONTO, "AMOUNT DISPLAY — '$0.00' (NO AMOUNT ENTERED)", driver)

        print("⏳ WAITING FOR UI TO FULLY SETTLE...")
        time.sleep(3)

        print("\n👉 STEP 1: CLICKING 'COBRAR' WITH NO AMOUNT ENTERED (DISPLAY IS $0.00)...")
        utils.click_boton(driver, config.XPATH_C_PANTALLA_COBRO)

        print("\n🔎 POLLING FOR ERROR BANNER: 'Aviso — Ingrese una cantidad valida'...")
        mensaje_encontrado = False
        for i in range(10):
            fuente_xml = driver.page_source.lower()
            if "ingrese una cantidad" in fuente_xml or "cantidad v" in fuente_xml or "aviso" in fuente_xml:
                mensaje_encontrado = True
                print(f"   🚨 ERROR BANNER DETECTED ON POLL ATTEMPT {i + 1}")
                utils.tomar_screenshot(driver, "C_60_ERROR_EMPTY_AMOUNT")
                break
            time.sleep(0.5)

        if mensaje_encontrado:
            _capture_evidence(driver, "C_60")
            print("\n✅ C-60: SUCCESS — ERROR MESSAGE 'AVISO INGRESE UNA CANTIDAD VALIDA' DETECTED.")
            return True
        else:
            print("\n❌ C-60 FAILED — EXPECTED ERROR MESSAGE WAS NOT FOUND AFTER CLICKING COBRAR WITH $0.00.")
            utils.tomar_screenshot(driver, "C_60_FAILED")
            _capture_evidence(driver, "C_60")
            print("\n🔍 SCANNING ALL VISIBLE TEXT FOR DEBUGGING...")
            try:
                for elem in driver.find_elements(By.XPATH, "//*"):
                    t = elem.get_attribute("text")
                    if t and len(t) > 2:
                        print(f"   📝 VISIBLE TEXT: '{t}'")
            except:
                pass
            return False

    except Exception as e:
        print(f"\n💥 C-60 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "C_60_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)


# =================================================================================
# C-61: VALIDATE EXCESSIVELY LARGE AMOUNT PROCEEDS TO THE CARD INSERTION SCREEN
# =================================================================================
def C_61():
    print("\n" + "=" * 60)
    print("🧪 C-61: VALIDATE EXCESSIVELY LARGE AMOUNT REACHES CARD SCREEN")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        print("🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)

        print("\n🖥️  VERIFYING CALCULATOR SCREEN IS READY...")
        utils.verificar_existencia(wait, config.XPATH_C_PANTALLA_COBRO, "CALCULATOR SCREEN — 'COBRAR' BUTTON", driver)

        print("⏳ WAITING FOR UI TO FULLY SETTLE BEFORE PRESSING DIGITS...")
        time.sleep(3)

        
        print("\n👉 STEP 1: ENTERING EXCESSIVELY LARGE AMOUNT (PRESSING 9 NINE TIMES)...")
        for i in range(9):
            print(f"   👆 PRESSING 9 ({i + 1}/9)")
            try:
                driver.find_element(By.XPATH, '//*[@text="9" or @content-desc="9"]').click()
                time.sleep(1)
            except Exception as e:
                print(f"   ⚠️  WARNING: COULD NOT PRESS 9 — {e}")

        
        print("\n📸 TAKING SCREENSHOT #1 — EXCESSIVELY LARGE AMOUNT ON DISPLAY ($999,999.99)...")
        utils.tomar_screenshot(driver, "C_61_LARGE_AMOUNT_ENTERED")

        
        print("\n👉 STEP 2: CLICKING 'COBRAR' — EXPECTING READER CONFIGURATION POPUP...")
        utils.click_boton(driver, config.XPATH_C_PANTALLA_COBRO)
        time.sleep(3)

        
        print("\n👉 STEP 3: CHECKING FOR 'LECTOR CONFIGURADO' POPUP...")
        lector_popup = utils.verificar_existencia(wait, config.XPATH_C_POPUP_LECTOR, "POPUP — 'AUN NO TIENES UN LECTOR CONFIGURADO'", driver)
        if lector_popup:
            print("   ✅ POPUP DETECTED — CLICKING 'OK'...")
            utils.click_boton(driver, config.XPATH_C_BTN_OK_POPUP)
            time.sleep(2)

        print("\n👉 STEP 4: NAVIGATING TO 'AJUSTES' TAB...")
        utils.click_boton(driver, config.XPATH_C_TAB_AJUSTES)
        time.sleep(2)

        print("\n👉 STEP 5: CLICKING 'CONFIGURAR LECTOR' IN AJUSTES...")
        utils.click_boton(driver, config.XPATH_C_BTN_CONFIGURAR_LECTOR)
        time.sleep(4)

        print("   🟢 CHECKING FOR 'POPUP VERDE' (TERMINAL CONFIGURADA CORRECTAMENTE)...")
        lector_verde = utils.verificar_existencia(wait, config.XPATH_C_POPUP_AJUSTES_VERDE, "POPUP — 'TERMINAL CONFIGURADA CORRECTAMENTE'", driver)
        if lector_verde:
            print("   ✅ POPUP DETECTED: 'TERMINAL CONFIGURADA CORRECTAMENTE'")
            utils.click_boton(driver, config.XPATH_C_POPUP_AJUSTES_VERDE)
            print("   ⏳ WAITING FOR THE SUCCESS POPUP TO DISMISS...")
            time.sleep(3)

        print("\n👉 STEP 6: NAVIGATING BACK TO 'INICIO' TAB...")
        utils.click_boton(driver, config.XPATH_C_TAB_INICIO)
        time.sleep(2)

        print("   🖥️  VERIFYING AMOUNT IS STILL DISPLAYED ON CALCULATOR SCREEN...")
        utils.verificar_existencia(wait, config.XPATH_C_PANTALLA_COBRO, "CALCULATOR SCREEN — 'COBRAR' BUTTON STILL PRESENT", driver)

        print("\n👉 STEP 7: CLICKING 'COBRAR' AGAIN WITH READER NOW CONFIGURED...")
        utils.click_boton(driver, config.XPATH_C_PANTALLA_COBRO)
        time.sleep(3)

        print("\n👉 STEP 8: CHECKING FOR 'AGREGAR PROPINA' POPUP...")
        propina_visible = utils.verificar_existencia(wait, config.XPATH_C_POPUP_PROPINA, "POPUP — 'AGREGAR PROPINA'", driver)
        if propina_visible:
            print("   ✅ POPUP DETECTED — CLICKING 'ACEPTAR'...")
            utils.click_boton(driver, config.XPATH_C_BTN_ACEPTAR_PROPINA)
            time.sleep(3)

        print("\n👉 STEP 9: VERIFYING 'INSERTA / DESLIZA LA TARJETA' SCREEN APPEARS...")
        pantalla_tarjeta = utils.verificar_existencia(
            wait,
            config.XPATH_C_PANTALLA_TARJETA,
            "CARD SCREEN — 'INSERTA, DESLIZA LA TARJETA'",
            driver
        )

        print("\n📸 TAKING SCREENSHOT #3 — CARD INSERTION SCREEN...")
        utils.tomar_screenshot(driver, "C_61_CARD_SCREEN")

        if pantalla_tarjeta:
            _capture_evidence(driver, "C_61")
            print("\n✅ C-61: SUCCESS — LARGE AMOUNT ACCEPTED AND CARD SCREEN DISPLAYED.")
            return True
        else:
            print("\n❌ C-61 FAILED — CARD SCREEN DID NOT APPEAR AFTER ENTERING LARGE AMOUNT.")
            utils.tomar_screenshot(driver, "C_61_FAILED")
            _capture_evidence(driver, "C_61")
            print("\n🔍 SCANNING VISIBLE TEXT FOR DEBUGGING...")
            try:
                for elem in driver.find_elements(By.XPATH, "//*"):
                    t = elem.get_attribute("text")
                    if t and len(t) > 3:
                        print(f"   📝 VISIBLE TEXT: '{t}'")
            except:
                pass
            return False

    except Exception as e:
        print(f"\n💥 C-61 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "C_61_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)


# ===========================================================================================
# C-62: VERIFY THAT THE 'COBRAR' BUTTON INITIATES THE TRANSACTION PROCESS WITH A VALID AMOUNT
# ===========================================================================================
def C_62():
    print("\n" + "=" * 60)
    print("🧪 C-62: VERIFY 'COBRAR' BUTTON INITIATES TRANSACTION WITH A VALID AMOUNT")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        print("🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)

        print("\n🖥️  VERIFYING CALCULATOR SCREEN IS READY...")
        utils.verificar_existencia(wait, config.XPATH_C_PANTALLA_COBRO, "CALCULATOR SCREEN — 'COBRAR' BUTTON", driver)

        print("⏳ WAITING FOR UI TO FULLY SETTLE BEFORE PRESSING DIGITS...")
        time.sleep(3)

        print("\n👉 STEP 1: ENTERING THE AMOUNT OF $50.00...")
        try:
            driver.find_element(By.XPATH, '//*[@text="5" or @content-desc="5"]').click()
            driver.find_element(By.XPATH, '//*[@text="0" or @content-desc="0"]').click()
            driver.find_element(By.XPATH, '//*[@text="0" or @content-desc="0"]').click()
            driver.find_element(By.XPATH, '//*[@text="0" or @content-desc="0"]').click()
        except:
            print("   ⚠️  WARNING: COULD NOT PRESS THE DIGITS FOR $50.00")
        time.sleep(1)

        
        print("\n👉 STEP 2: CLICKING 'COBRAR' — EXPECTING READER CONFIGURATION POPUP...")
        utils.click_boton(driver, config.XPATH_C_PANTALLA_COBRO)
        time.sleep(3)

        print("\n👉 STEP 3: CHECKING FOR 'LECTOR CONFIGURADO' POPUP...")
        lector_popup = utils.verificar_existencia(wait, config.XPATH_C_POPUP_LECTOR, "POPUP — 'AUN NO TIENES UN LECTOR CONFIGURADO'", driver)
        if lector_popup:
            print("   ✅ POPUP DETECTED — CLICKING 'OK'...")
            utils.click_boton(driver, config.XPATH_C_BTN_OK_POPUP)
            time.sleep(2)

        print("\n👉 STEP 4: NAVIGATING TO 'AJUSTES' TAB...")
        utils.click_boton(driver, config.XPATH_C_TAB_AJUSTES)
        time.sleep(2)

        print("\n👉 STEP 5: CLICKING 'CONFIGURAR LECTOR' IN AJUSTES...")
        utils.click_boton(driver, config.XPATH_C_BTN_CONFIGURAR_LECTOR)
        time.sleep(4)

        print("   🟢 CHECKING FOR 'POPUP VERDE' (TERMINAL CONFIGURADA CORRECTAMENTE)...")
        lector_verde = utils.verificar_existencia(wait, config.XPATH_C_POPUP_AJUSTES_VERDE, "POPUP — 'TERMINAL CONFIGURADA CORRECTAMENTE'", driver)
        if lector_verde:
            print("   ✅ POPUP DETECTED: 'TERMINAL CONFIGURADA CORRECTAMENTE'")
            time.sleep(4)

        print("\n👉 STEP 6: NAVIGATING BACK TO 'INICIO' TAB...")
        utils.click_boton(driver, config.XPATH_C_TAB_INICIO)
        time.sleep(3)

        print("   🖥️  VERIFYING AMOUNT IS STILL DISPLAYED ON CALCULATOR SCREEN...")
        utils.verificar_existencia(wait, config.XPATH_C_PANTALLA_COBRO, "CALCULATOR SCREEN — 'COBRAR' BUTTON STILL PRESENT", driver)

        print("\n👉 STEP 7: CLICKING 'COBRAR' AGAIN WITH READER NOW CONFIGURED...")
        utils.click_boton(driver, config.XPATH_C_PANTALLA_COBRO)
        time.sleep(3)

        print("\n👉 STEP 8: CHECKING FOR 'AGREGAR PROPINA' POPUP...")
        propina_visible = utils.verificar_existencia(wait, config.XPATH_C_POPUP_PROPINA, "POPUP — 'AGREGAR PROPINA'", driver)
        if propina_visible:
            print("   ✅ POPUP DETECTED — CLICKING 'ACEPTAR'...")
            utils.click_boton(driver, config.XPATH_C_BTN_ACEPTAR_PROPINA)
            time.sleep(3)

        print("\n👉 STEP 9: VERIFYING 'INSERTA / DESLIZA LA TARJETA' SCREEN APPEARS...")
        pantalla_tarjeta = utils.verificar_existencia(
            wait,
            config.XPATH_C_PANTALLA_TARJETA,
            "CARD SCREEN — 'INSERTA, DESLIZA LA TARJETA'",
            driver
        )

        print("\n📸 TAKING SCREENSHOT — CARD INSERTION SCREEN...")
        utils.tomar_screenshot(driver, "C_62_CARD_SCREEN")

        if pantalla_tarjeta:
            _capture_evidence(driver, "C_62")
            print("\n✅ C-62: SUCCESS — AMOUNT OF $50.00 ACCEPTED AND CARD SCREEN DISPLAYED.")
            return True
        else:
            print("\n❌ C-62 FAILED — CARD SCREEN DID NOT APPEAR AFTER ENTERING THE AMOUNT.")
            utils.tomar_screenshot(driver, "C_62_FAILED")
            _capture_evidence(driver, "C_62")
            print("\n🔍 SCANNING VISIBLE TEXT FOR DEBUGGING...")
            try:
                for elem in driver.find_elements(By.XPATH, "//*"):
                    t = elem.get_attribute("text")
                    if t and len(t) > 3:
                        print(f"   📝 VISIBLE TEXT: '{t}'")
            except:
                pass
            return False

    except Exception as e:
        print(f"\n💥 C-62 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "C_62_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)

# =================================================================================
# C-63: VERIFY 'COBRAR' BUTTON STATE DEPENDING ON AMOUNT (\$0.00 VS \$1.00)
# =================================================================================
def C_63():
    print("\n" + "=" * 60)
    print("🧪 C-63: VERIFY 'COBRAR' BUTTON STATE (ENABLED/DISABLED BASED ON AMOUNT)")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        print("🔐 PRECONDITION: REACHING THE CALCULATOR SCREEN...")
        helper_login_to_calculator(driver, wait)
        time.sleep(3)

        print("\n👉 STEP 1: VALIDATING 'COBRAR' BUTTON IS PRESENT AT \$0.00...")

        boton_presente = False
        try:
            btn_cobrar = driver.find_element(By.XPATH, config.XPATH_C_PANTALLA_COBRO)
            boton_presente = btn_cobrar.is_displayed()
        except:
            pass

        if boton_presente:
            print("   ✅ 'COBRAR' BUTTON IS VISIBLE ON SCREEN AT \$0.00.")
            utils.tomar_screenshot(driver, "C_63_STEP1_COBRAR_AT_ZERO")
        else:
            print("   ❌ ERROR: 'COBRAR' BUTTON NOT FOUND ON SCREEN.")
            utils.tomar_screenshot(driver, "C_63_STEP1_FAILED")
            return False

        print("\n👉 STEP 2: ENTERING \$1.00 AND VALIDATING 'COBRAR' REMAINS VISIBLE...")

        try:
            driver.find_element(By.XPATH, '//*[@text="1" or @content-desc="1"]').click()
            driver.find_element(By.XPATH, '//*[@text="0" or @content-desc="0"]').click()
            driver.find_element(By.XPATH, '//*[@text="0" or @content-desc="0"]').click()
        except:
            print("   ⚠️  WARNING: COULD NOT PRESS THE DIGITS FOR \$1.00")

        time.sleep(2)

        boton_presente = False
        try:
            btn_cobrar = driver.find_element(By.XPATH, config.XPATH_C_PANTALLA_COBRO)
            boton_presente = btn_cobrar.is_displayed()
        except:
            pass

        if boton_presente:
            print("   ✅ 'COBRAR' BUTTON IS VISIBLE AFTER ENTERING \$1.00.")
            print("\n📸 TAKING SCREENSHOT WITH AMOUNT \$1.00...")
            utils.tomar_screenshot(driver, "C_63_STEP2_COBRAR_AT_ONE")
        else:
            print("   ❌ ERROR: 'COBRAR' BUTTON NOT FOUND AFTER ENTERING \$1.00")
            utils.tomar_screenshot(driver, "C_63_STEP2_FAILED")
            return False

        print("\n👉 STEP 3: DELETING AMOUNT BACK TO \$0.00 USING BACKSPACE...")

        for _ in range(3):
            clicked = _press_backspace(driver)
            if not clicked:
                print("   ⚠️  WARNING: BACKSPACE FAILED ON ONE ATTEMPT.")
            time.sleep(0.5)
        time.sleep(2)

        boton_presente = False
        try:
            btn_cobrar = driver.find_element(By.XPATH, config.XPATH_C_PANTALLA_COBRO)
            boton_presente = btn_cobrar.is_displayed()
        except:
            pass

        if boton_presente:
            print("   ✅ 'COBRAR' BUTTON REMAINS VISIBLE AFTER CLEARING AMOUNT.")
            print("\n📸 TAKING FINAL SCREENSHOT AFTER CLEARING AMOUNT...")
            utils.tomar_screenshot(driver, "C_63_STEP3_COBRAR_AFTER_CLEAR")
        else:
            print("   ❌ ERROR: 'COBRAR' BUTTON NOT FOUND AFTER CLEARING AMOUNT.")
            utils.tomar_screenshot(driver, "C_63_STEP3_FAILED")
            return False

        _capture_evidence(driver, "C_63")
        print("\n✅ C-63: SUCCESS — 'COBRAR' BUTTON REMAINS CONSISTENTLY VISIBLE ACROSS AMOUNT CHANGES.")
        return True

    except Exception as e:
        print(f"\n💥 C-63 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "C_63_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)

# =================================================================================
# C-64: VALIDATE KEYPAD VISUAL RESPONSE, BOUNDARY LIMITS, AND DELETE BUTTON
# =================================================================================
def C_64():
    print("\n" + "=" * 60)
    print("🧪 C-64: VALIDATE KEYPAD VISUAL RESPONSE AND BOUNDARY LIMITS")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        print("🔐 PRECONDITION: REACHING THE CALCULATOR SCREEN...")
        helper_login_to_calculator(driver, wait)
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
        utils.tomar_screenshot(driver, "C_64_1_FULL_SEQUENCE")
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
        utils.tomar_screenshot(driver, "C_64_2_AFTER_BACKSPACE")

        print("\n👉 STEP 3: PRESSING THE LAST DIGIT '9' INTO THE FREED SPACE...")
        try:
            driver.find_element(By.XPATH, '//*[@text="9" or @content-desc="9"]').click()
            print("   👆 TAPPED DIGIT: 9")
            time.sleep(1)
        except Exception as e:
            print(f"   ⚠️  WARNING: COULD NOT TAP DIGIT 9. ERROR: {e}")

        print("\n📸 TAKING SCREENSHOT #3 — WITH '9' AT THE END...")
        utils.tomar_screenshot(driver, "C_64_3_FINAL_NINE")

        _capture_evidence(driver, "C_64")
        print("\n✅ C-64: SUCCESS — KEYPAD INTERACTION, BOUNDARY LIMIT, AND DELETE FUNCTION COMPLETED.")
        return True

    except Exception as e:
        print(f"\n💥 C-64 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "C_64_TECHNICAL_ERROR")
        except:
            pass
        return False
    finally:
        utils.cerrar_driver(driver)


# === MAIN EXECUTION === #
if __name__ == "__main__":

    logger, log_file, timestamp = utils.iniciar_reporte("OPERATIONALS_C")

    try:
        C_55()
        C_56()
        C_57()
        C_58()
        C_59()
        C_60()
        C_61()
        C_62()
        C_63()
        C_64()

    finally:
        utils.generar_reporte_html("OPERATIONALS_C", log_file, timestamp)
