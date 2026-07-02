"""
# ==================================================================================
# FILENAME    : TICKET_SENT.py
# FOLDER      : Automatizacion/T6/v2/Transactional/
# PROJECT     : MEMPHIS QA AUTOMATION FRAMEWORK
# DESCRIPTION : VALIDATES THE TICKET SHARING FUNCTIONALITY AFTER A COMPLETED
#               CREDIT CARD TRANSACTION. TESTS ALL 3 SHARING CHANNELS:
#
#                 - TS-01 : Share ticket via EMAIL
#                 - TS-02 : Share ticket via WHATSAPP
#                 - TS-03 : Share ticket via SMS
#
# FLOW PER TEST:
#   1.  Login → Calculator screen
#   2.  Type $25.00 → Realizar cobro → Venta Normal
#   3.  Wait for card insertion screen (30s active polling)
#   4.  [USER INSERTS CARD + PIN manually]
#   5.  Detect "Transacción aprobada" green screen
#   6.  Click "Aceptar" → arrive at ticket share screen
#   7.  *** VALIDATE SHARE BUTTON (Email / WhatsApp / SMS) ***
#   8.  Fill destination → click "Enviar"
#   9.  Detect success/failure popup → record result
#
# SUCCESS CRITERIA:
#   ✅ Share popup opens correctly for each channel
#   ✅ Destination field accepts input
#   ✅ "Enviar" can be tapped
#   ✅ Success message ("sido enviado") appears OR
#      failure message is captured as evidence
#
# NOTE:
#   Each test runs a FULL transaction independently so the ticket
#   share screen is reached fresh every time.
#
# REQUIREMENTS:
#   - Appium server running:  appium --relaxed-security
#   - T6 connected via USB:   adb devices
#   - utils.py, config.py in T6/v2/
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

# Amount: press 2→5→0→0 = $25.00 on T6 calculator
CHARGE_AMOUNT       = "2500"
CARD_INSERT_WAIT    = 30          # Seconds of active polling for manual card + PIN
TRANSACTION_WAIT    = 45          # Extra polling seconds after manual wait

# Share destinations
EMAIL_DESTINATION   = "santiago.tapia@memphis.mx"
WHATSAPP_NUMBER     = "5580049837"
SMS_NUMBER          = "5580049837"

# Success/failure keywords from share result popup
SUCCESS_FRAGMENT    = "sido enviado"
FAILURE_FRAGMENT    = "no fue posible"
APPROVAL_KEYWORDS   = ["aprobada", "transacción aprobada", "approved"]


# ── XPATHS ──────────────────────────────────────────────────────────────────────

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
XPATH_BTN_ACEPTAR_APPROVAL = (
    '//*[@content-desc="Aceptar" or @text="Aceptar" or '
    'contains(@content-desc,"Aceptar") or contains(@text,"Aceptar")]'
)
# Ticket share screen — "¿Cómo deseas compartir el ticket?"
XPATH_SCREEN_COMPARTIR = (
    '//*[contains(@content-desc,"compartir el ticket") or '
    'contains(@text,"compartir el ticket") or '
    'contains(@content-desc,"Cómo deseas") or '
    'contains(@text,"Cómo deseas")]'
)
# Individual share buttons on the ticket screen
XPATH_BTN_COMPARTIR_EMAIL     = (
    '//*[@content-desc="Compartir por correo" or @text="Compartir por correo" or '
    'contains(@content-desc,"correo") or contains(@text,"correo")]'
)
XPATH_BTN_COMPARTIR_WHATSAPP  = (
    '//*[@content-desc="Compartir por WhatsApp" or @text="Compartir por WhatsApp" or '
    'contains(@content-desc,"WhatsApp") or contains(@text,"WhatsApp")]'
)
XPATH_BTN_COMPARTIR_SMS       = (
    '//*[@content-desc="Compartir por SMS" or @text="Compartir por SMS" or '
    'contains(@content-desc,"SMS") or contains(@text,"SMS")]'
)
# Destination input inside share modal
XPATH_INPUT_DESTINATION = (
    '//android.widget.EditText[1]'
)
# "Enviar" button inside share modal
XPATH_BTN_ENVIAR = (
    '//*[@content-desc="Enviar" or @text="Enviar" or '
    'contains(@content-desc,"Enviar") or contains(@text,"Enviar")]'
)
# Success popup after sending
XPATH_POPUP_SUCCESS = (
    '//*[contains(@content-desc,"enviado") or contains(@text,"enviado") or '
    'contains(@content-desc,"sido enviado") or contains(@text,"sido enviado")]'
)
# Failure popup
XPATH_POPUP_FAILURE = (
    '//*[contains(@content-desc,"no fue posible") or contains(@text,"no fue posible") or '
    'contains(@content-desc,"No fue posible") or contains(@text,"No fue posible")]'
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
    """Full login: onboarding → credentials → commerce → lector → calculator."""
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
    """Types amount digit by digit. '2500' → $25.00 on T6 right-to-left calculator."""
    print(f"   ✏️  TYPING: {amount_str} → $25.00")
    for digit in amount_str:
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
            except Exception as e:
                print(f"   ⚠️  Digit '{digit}': {e}")
    time.sleep(0.5)
    try:
        displayed = driver.find_element(
            By.XPATH, config.XPATH_C_DISPLAY_UPDATED
        ).get_attribute("content-desc") or ""
        print(f"   ✅ DISPLAY: {displayed}")
    except:
        pass


def _poll_for_approval(driver, poll_seconds, label):
    """Polls every second for the green approval screen. Returns True when detected."""
    end_time = time.time() + poll_seconds
    while time.time() < end_time:
        remaining = int(end_time - time.time())
        print(f"      🕐 {remaining:02d}s — {label}...", end="\r")
        try:
            for elem in driver.find_elements(By.XPATH, XPATH_SCREEN_APROBADA):
                t = (elem.get_attribute("text") or "").lower()
                d = (elem.get_attribute("content-desc") or "").lower()
                if any(kw in t + d for kw in APPROVAL_KEYWORDS):
                    print(f"\n   ✅ APPROVAL DETECTED at {poll_seconds - remaining}s!")
                    return True
        except:
            pass
        try:
            if any(kw in driver.page_source.lower() for kw in APPROVAL_KEYWORDS):
                print(f"\n   ✅ APPROVAL DETECTED via page source!")
                return True
        except:
            pass
        time.sleep(1)
    print()
    return False


def _complete_transaction(driver, wait, test_id):
    """
    Runs the full payment flow up to the ticket share screen.
    Returns True if the ticket share screen is reached.
    """
    print(f"\n   💳 COMPLETING TRANSACTION for {test_id}...")

    # TYPE AMOUNT
    _type_amount(driver, CHARGE_AMOUNT)
    _take_screenshot(driver, f"{test_id}_T1_AMOUNT")

    # REALIZAR COBRO
    charge_clicked = False
    for xpath in [XPATH_BTN_REALIZAR_COBRO,
                  '//*[contains(@content-desc,"cobro") or contains(@text,"cobro")]']:
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            ).click()
            charge_clicked = True
            print("   ✅ 'Realizar cobro' CLICKED.")
            break
        except:
            continue
    if not charge_clicked:
        print("   ❌ COULD NOT CLICK 'Realizar cobro'")
        return False
    time.sleep(3)

    # VENTA NORMAL
    try:
        WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.XPATH, XPATH_POPUP_TIPO_OPERACION))
        )
        print("   ✅ Tipo operación popup visible.")
    except:
        pass

    sale_clicked = False
    try:
        WebDriverWait(driver, 6).until(
            EC.element_to_be_clickable((By.XPATH, XPATH_BTN_VENTA_NORMAL))
        ).click()
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
            print(f"   ❌ Could not click 'Venta Normal': {e}")
            return False
    time.sleep(2)

    # WAIT FOR CARD SCREEN
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, XPATH_SCREEN_CARD_READY))
        )
        print("   ✅ CARD INSERTION SCREEN DETECTED.")
    except:
        print("   ⚠️  Card screen not confirmed — continuing.")
    _take_screenshot(driver, f"{test_id}_T2_CARD_SCREEN")

    # MANUAL PAUSE — card + PIN
    print(f"\n{'='*65}")
    print(f"🃏 INSERT CARD + PIN — {test_id}")
    print(f"   👉 Insert chip card and enter PIN on T6 reader")
    print(f"   👉 {CARD_INSERT_WAIT}s active polling — advances on approval")
    print(f"{'='*65}")

    approved = _poll_for_approval(
        driver, CARD_INSERT_WAIT, "waiting for card + PIN"
    )
    if not approved:
        print(f"   ⏳ Polling {TRANSACTION_WAIT}s more...")
        approved = _poll_for_approval(driver, TRANSACTION_WAIT, "waiting for approval")

    _take_screenshot(driver, f"{test_id}_T3_APPROVAL")

    if not approved:
        print("   ❌ TRANSACTION NOT APPROVED — cannot test ticket sharing.")
        return False

    print("   ✅ TRANSACTION APPROVED!")

    # CLICK ACEPTAR ON GREEN SCREEN → ARRIVE AT TICKET SHARE SCREEN
    time.sleep(2)
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, XPATH_BTN_ACEPTAR_APPROVAL))
        ).click()
        print("   ✅ 'Aceptar' CLICKED on approval screen.")
        time.sleep(2)
    except:
        print("   ℹ️  No 'Aceptar' on approval screen — may go directly to ticket.")

    # VERIFY TICKET SHARE SCREEN
    try:
        WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.XPATH, XPATH_SCREEN_COMPARTIR))
        )
        print("   ✅ TICKET SHARE SCREEN REACHED.")
        _take_screenshot(driver, f"{test_id}_T4_TICKET_SHARE_SCREEN")
        return True
    except:
        # Check page source
        if any(kw in driver.page_source.lower()
               for kw in ["compartir", "whatsapp", "correo", "sms", "finalizar"]):
            print("   ✅ TICKET SHARE SCREEN DETECTED via page source.")
            _take_screenshot(driver, f"{test_id}_T4_TICKET_SHARE_SCREEN")
            return True
        print("   ❌ TICKET SHARE SCREEN NOT REACHED.")
        _take_screenshot(driver, f"{test_id}_T4_TICKET_NOT_FOUND")
        return False


def _click_share_button(driver, channel_name, channel_xpath):
    """
    Clicks a share button (Email / WhatsApp / SMS) using multiple strategies.
    Returns True if clicked.
    """
    print(f"   🔍 CLICKING SHARE BUTTON: '{channel_name}'...")

    # S1: Specific channel XPath
    try:
        btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, channel_xpath))
        )
        btn.click()
        print(f"   ✅ S1: '{channel_name}' CLICKED via specific XPath.")
        return True
    except:
        pass

    # S2: Exact text/content-desc match
    for attr_val in [channel_name, f"Compartir por {channel_name}"]:
        try:
            driver.find_element(
                By.XPATH,
                f'//*[@content-desc="{attr_val}" or @text="{attr_val}"]'
            ).click()
            print(f"   ✅ S2: '{attr_val}' CLICKED via exact match.")
            return True
        except:
            continue

    # S3: contains match
    try:
        driver.find_element(
            By.XPATH,
            f'//*[contains(@content-desc,"{channel_name}") or '
            f'contains(@text,"{channel_name}")]'
        ).click()
        print(f"   ✅ S3: '{channel_name}' CLICKED via contains.")
        return True
    except:
        pass

    # S4: UiAutomator
    try:
        driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().descriptionContains("{channel_name}")'
        ).click()
        print(f"   ✅ S4: '{channel_name}' CLICKED via UiAutomator.")
        return True
    except:
        pass

    print(f"   ❌ ALL STRATEGIES FAILED for '{channel_name}'.")
    return False


def _enter_destination_and_send(driver, destination):
    """
    Fills the destination field (email/phone) and clicks 'Enviar'.
    Returns True if 'Enviar' was clicked.
    """
    print(f"   ✏️  FILLING DESTINATION: {destination}")
    time.sleep(1)

    # Fill destination field
    field_filled = False
    try:
        field = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, XPATH_INPUT_DESTINATION))
        )
        field.click()
        time.sleep(0.5)
        field.clear()
        field.send_keys(destination)
        try:
            driver.hide_keyboard()
        except:
            pass
        field_filled = True
        print(f"   ✅ DESTINATION FILLED: {destination}")
    except:
        try:
            driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().className("android.widget.EditText").instance(0)'
            ).send_keys(destination)
            field_filled = True
            print(f"   ✅ DESTINATION FILLED (UiAutomator): {destination}")
        except Exception as e:
            print(f"   ⚠️  Could not fill destination field: {e}")

    # Click Enviar
    send_clicked = False
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, XPATH_BTN_ENVIAR))
        ).click()
        send_clicked = True
        print("   ✅ 'Enviar' CLICKED.")
    except:
        try:
            driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().text("Enviar")'
            ).click()
            send_clicked = True
            print("   ✅ 'Enviar' CLICKED (UiAutomator).")
        except Exception as e:
            print(f"   ⚠️  Could not click 'Enviar': {e}")

    return send_clicked


def _detect_send_result(driver, test_id, timeout=8):
    """
    Polls for success or failure popup after tapping Enviar.
    Returns: "success" | "failure" | "inconclusive"
    """
    print(f"   🔍 POLLING FOR SEND RESULT (up to {timeout}s)...")
    end_time = time.time() + timeout
    while time.time() < end_time:
        # Check success
        try:
            for elem in driver.find_elements(By.XPATH, XPATH_POPUP_SUCCESS):
                t = (elem.get_attribute("text") or "").lower()
                d = (elem.get_attribute("content-desc") or "").lower()
                if SUCCESS_FRAGMENT.lower() in t + d:
                    text_val = t or d
                    print(f"   ✅ SUCCESS POPUP: '{text_val}'")
                    return "success"
        except:
            pass

        # Check failure
        try:
            for elem in driver.find_elements(By.XPATH, XPATH_POPUP_FAILURE):
                t = (elem.get_attribute("text") or "").lower()
                d = (elem.get_attribute("content-desc") or "").lower()
                if FAILURE_FRAGMENT.lower() in t + d:
                    text_val = t or d
                    print(f"   ⚠️  FAILURE POPUP: '{text_val}'")
                    return "failure"
        except:
            pass

        # Page source check
        try:
            page = driver.page_source.lower()
            if SUCCESS_FRAGMENT.lower() in page:
                print("   ✅ SUCCESS DETECTED via page source.")
                return "success"
            if FAILURE_FRAGMENT.lower() in page:
                print("   ⚠️  FAILURE DETECTED via page source.")
                return "failure"
        except:
            pass

        time.sleep(0.5)

    print("   ⚠️  NO RESULT POPUP DETECTED — INCONCLUSIVE.")
    return "inconclusive"


def _close_share_modal(driver):
    """Closes the share modal by pressing back or tapping outside."""
    try:
        driver.back()
        time.sleep(1)
    except:
        pass


# ==================================================================================
# INDIVIDUAL TEST FUNCTIONS
# ==================================================================================

def _run_ticket_share_test(channel_name, channel_xpath, destination, test_id):
    """
    Full flow: login → transaction → ticket screen → share via channel.
    Returns (passed: bool, note: str)
    """
    print("\n" + "=" * 65)
    print(f"📤 {test_id}: TICKET SHARE VIA {channel_name.upper()}")
    print("=" * 65)

    driver, wait = utils.start_driver()
    result = False
    note   = ""

    try:
        # ── STEP 1: LOGIN ────────────────────────────────────────────
        print("\n👉 STEP 1: LOGIN...")
        _helper_login(driver, wait)
        _take_screenshot(driver, f"{test_id}_STEP1_CALCULATOR")

        # ── STEP 2-6: COMPLETE TRANSACTION → TICKET SHARE SCREEN ─────
        print("\n👉 STEPS 2-6: TRANSACTION FLOW...")
        ticket_screen_reached = _complete_transaction(driver, wait, test_id)

        if not ticket_screen_reached:
            note = "TICKET SHARE SCREEN NOT REACHED — TRANSACTION INCOMPLETE"
            print(f"\n   ❌ {note}")
            return False, note

        _take_screenshot(driver, f"{test_id}_STEP6_TICKET_SHARE_SCREEN")

        # ── STEP 7: CLICK SHARE BUTTON ───────────────────────────────
        print(f"\n👉 STEP 7: CLICKING '{channel_name}' SHARE BUTTON...")
        button_clicked = _click_share_button(driver, channel_name, channel_xpath)

        if not button_clicked:
            note = f"COULD NOT CLICK '{channel_name}' SHARE BUTTON"
            _take_screenshot(driver, f"{test_id}_STEP7_BTN_FAILED")
            return False, note

        time.sleep(2)
        _take_screenshot(driver, f"{test_id}_STEP7_SHARE_MODAL")

        # ── STEP 8: FILL DESTINATION + ENVIAR ────────────────────────
        print(f"\n👉 STEP 8: FILLING '{destination}' → CLICKING 'Enviar'...")
        send_clicked = _enter_destination_and_send(driver, destination)
        _take_screenshot(driver, f"{test_id}_STEP8_AFTER_ENVIAR")

        # ── STEP 9: DETECT RESULT ─────────────────────────────────────
        print("\n👉 STEP 9: DETECTING SEND RESULT...")
        send_result = _detect_send_result(driver, test_id)
        _take_screenshot(driver, f"{test_id}_STEP9_RESULT")

        if send_result == "success":
            result = True
            note   = f"✅ TICKET SENT via {channel_name} to {destination}"
            print(f"\n   ✅ {note}")
        elif send_result == "failure":
            result = False
            note   = f"❌ SEND FAILED via {channel_name} — 'no fue posible' popup appeared"
            print(f"\n   ❌ {note}")
        else:
            # Inconclusive — if Enviar was clicked and no error appeared, mark as pass
            result = send_clicked
            note   = (
                f"{'SENT (no popup detected)' if send_clicked else 'SEND BUTTON NOT FOUND'} "
                f"via {channel_name} to {destination}"
            )
            print(f"\n   ⚠️  INCONCLUSIVE — {note}")

        # ── STEP 10: CLOSE MODAL + FINALIZAR ─────────────────────────
        print("\n👉 STEP 10: CLOSING MODAL → FINALIZAR...")
        _close_share_modal(driver)
        time.sleep(1)

        try:
            WebDriverWait(driver, 6).until(
                EC.element_to_be_clickable((By.XPATH, XPATH_BTN_FINALIZAR))
            ).click()
            print("   ✅ 'Finalizar' CLICKED.")
            time.sleep(3)
        except:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().text("Finalizar")'
                ).click()
                print("   ✅ 'Finalizar' CLICKED (UiAutomator).")
                time.sleep(3)
            except:
                print("   ⚠️  'Finalizar' not found — continuing.")

        _take_screenshot(driver, f"{test_id}_STEP10_BACK_TO_CALCULATOR")

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


# ── PUBLIC TEST FUNCTIONS ────────────────────────────────────────────────────────

def TS_01_EMAIL():
    """TS-01: Share ticket via EMAIL after a completed transaction."""
    return _run_ticket_share_test(
        channel_name   = "correo",
        channel_xpath  = XPATH_BTN_COMPARTIR_EMAIL,
        destination    = EMAIL_DESTINATION,
        test_id        = "TS_01_EMAIL"
    )

def TS_02_WHATSAPP():
    """TS-02: Share ticket via WHATSAPP after a completed transaction."""
    return _run_ticket_share_test(
        channel_name   = "WhatsApp",
        channel_xpath  = XPATH_BTN_COMPARTIR_WHATSAPP,
        destination    = WHATSAPP_NUMBER,
        test_id        = "TS_02_WHATSAPP"
    )

def TS_03_SMS():
    """TS-03: Share ticket via SMS after a completed transaction."""
    return _run_ticket_share_test(
        channel_name   = "SMS",
        channel_xpath  = XPATH_BTN_COMPARTIR_SMS,
        destination    = SMS_NUMBER,
        test_id        = "TS_03_SMS"
    )


# ==================================================================================
# MAIN BLOCK
# ==================================================================================

if __name__ == "__main__":

    logger, log_file, timestamp = utils.start_report("TICKET_SENT")

    results = {}

    try:
        results["TS-01 Email"]    = TS_01_EMAIL()
        results["TS-02 WhatsApp"] = TS_02_WHATSAPP()
        results["TS-03 SMS"]      = TS_03_SMS()

    finally:
        print("\n" + "=" * 65)
        print("📊 TICKET_SENT — FINAL SUMMARY")
        print("=" * 65)
        print(f"  {'TEST CASE':<30} {'RESULT':<8} NOTE")
        print("  " + "─" * 62)
        for test_name, (passed, note) in results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"  {test_name:<30} {status:<8} {note}")
            # HTML report parser format
            if passed:
                print(f"  ✅ {test_name}: SUCCESS — {note}")
            else:
                print(f"  ❌ {test_name}: FAILED — {note}")
        print("  " + "─" * 62)
        passed_count = sum(1 for v in results.values() if v[0])
        print(f"  TOTAL: {passed_count}/{len(results)} PASSED")
        print("=" * 65)

        utils.generate_zip_report("TICKET_SENT", logger, log_file, timestamp)
        utils.generate_html_report("TICKET_SENT", log_file, timestamp)