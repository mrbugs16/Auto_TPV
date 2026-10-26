"""
FILENAME: Operationals_MSI.py
DESCRIPTION:
    AUTOMATED TEST SUITE — COBRO CON MESES SIN INTERESES (MSI).
    BASED ON: Automatizacion/T6/v2/Matrices/Matriz_Operationals_MSI.xlsx

FLOW:
    Login → Inicio → monto → "Realizar cobro" → "Leyendo tarjeta..." →
    [monto >= $1,000] "¿Cuántas mensualidades?" → "Ingresa tu PIN en el lector" →
    "Transacción aprobada" → "Aceptar" → Inicio ($0.00)

MANUAL STEPS (SEMI-AUTOMATED CASES):
    THE TESTER INSERTS THE CARD AND TYPES THE PIN ON THE T6 WHEN THE CONSOLE
    SHOWS THE 🖐️ BANNER. THE SCRIPT POLLS THE SCREEN AND CONTINUES BY ITSELF.

TEST CASES COVERED:
    · TC-MSI-001 : $500 DE CONTADO APROBADO (SIN PREGUNTA DE MENSUALIDADES)
    · TC-MSI-002 : $1,000 A 6 MSI APROBADO
    · TC-MSI-003 : $999.99 NO OFRECE MSI
    · TC-MSI-004 : $1,000.00 EXACTO OFRECE 6 MSI
    · TC-MSI-005 : $1,000.01 OFRECE 6 MSI
    · TC-MSI-006 : $5,000 A 6 MSI APROBADO
    · TC-MSI-007 : ELEMENTOS DE "¿CUÁNTAS MENSUALIDADES?"
    · TC-MSI-008 : >= $1,000 ELIGIENDO "SIN MENSUALIDADES" APROBADO
    · TC-MSI-009 : "CANCELAR" EN "¿CUÁNTAS MENSUALIDADES?"
    · TC-MSI-010 : RESUMEN DEL PIN (MONTO + MENSUALIDADES)
    · TC-MSI-011 : NIP INCORRECTO RECHAZA LA TRANSACCIÓN
    · TC-MSI-012 : X ROJA DEL TECLADO DE PIN CANCELA EL COBRO
    · TC-MSI-013 : BORRAR UN DÍGITO Y CORREGIR EL NIP
    · TC-MSI-014 : "ACEPTAR" CON NIP INCOMPLETO
    · TC-MSI-015 : TECLADO DE PIN EN ORDEN ALEATORIO
    · TC-MSI-016 : SIN NIP — EL COBRO EXPIRA POR TIEMPO
    · TC-MSI-017 : SIN TARJETA — LA LECTURA EXPIRA
    · TC-MSI-018 : RETIRAR LA TARJETA DURANTE LA LECTURA          (MANUAL — NOT AUTOMATED)
    · TC-MSI-019 : TARJETA DE DÉBITO >= $1,000 NO OFRECE MSI
    · TC-MSI-020 : PANTALLA "TRANSACCIÓN APROBADA" Y "ACEPTAR"
    · TC-MSI-021 : LA TRANSACCIÓN A 6 MSI APARECE EN "TRANSACCIONES"
    · TC-MSI-022 : COBRO A 6 MSI RECHAZADO POR EL BANCO
    · TC-MSI-023 : TICKET IMPRESO CON 6 MSI                        (MANUAL — NOT AUTOMATED)
    · TC-MSI-024 : "REALIZAR COBRO" CON $0.00
    · TC-MSI-025 : CORREGIR EL MONTO CON BORRAR ($1,000 → $100)

USAGE:
    python Operationals_MSI.py                 → RUNS EVERY CASE
    python Operationals_MSI.py 001 002 024     → RUNS ONLY THOSE CASES

REQUIREMENTS:
    - APPIUM SERVER RUNNING.
    - config.py AND utils.py IN THE SAME DIRECTORY.
"""

import sys
import os
import re
import html
from decimal import Decimal

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


# KEYWORDS USED TO CLASSIFY THE CURRENT SCREEN (LOWERCASE)
KW_APROBADA = ["transacción aprobada", "transaccion aprobada"]
KW_RECHAZO  = ["rechazad", "declinad", "denegad", "no aprobada", "incorrect", "error"]
KW_TIEMPO   = ["tiempo", "expir", "agotad"]


# ==================================================================================
# HELPER: FULL LOGIN FLOW v2
#         ONBOARDING → LOGIN → CONFIGURA TU COMERCIO → LECTOR POPUP → HOME
# ==================================================================================

def helper_login_to_calculator(driver, wait):

    from selenium.webdriver.support.ui import WebDriverWait as _WDW

    # THE APP CAN TAKE >10s TO OPEN AFTER THE RESET: WAIT FOR ONBOARDING, LOGIN OR INICIO
    print("   ⏳ [HELPER] PHASE 0: WAITING FOR THE APP TO LOAD...")
    first_screen = None
    end = time.time() + 45
    while time.time() < end and first_screen is None:
        if _is_visible(driver, config.XPATH_MSI_INICIO):
            first_screen = "inicio"
        elif _is_visible(driver, config.XPATH_OB_BTN_SIGUIENTE):
            first_screen = "onboarding"
        elif _is_visible(driver, config.XPATH_LG_BTN_INICIAR):
            first_screen = "login"
        else:
            time.sleep(1)
    print(f"   ℹ️  [HELPER] FIRST SCREEN: {(first_screen or 'NOT DETECTED AFTER 45s').upper()}")
    if first_screen == "inicio":
        print("   ✅ [HELPER] ALREADY ON INICIO")
        return

    print("   📱 [HELPER] PHASE 1: NAVIGATING ONBOARDING SLIDES...")
    time.sleep(1)

    for slide_num, btn_xpath in enumerate(
        [] if first_screen == "login" else
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

    # WAIT FOR INICIO — LOGIN CAN TAKE A FEW EXTRA SECONDS ON THE T6
    try:
        WebDriverWait(driver, 15).until(
            lambda d: d.find_element(By.XPATH, config.XPATH_MSI_INICIO)
        )
        print("   ✅ [HELPER] INICIO REACHED")
    except TimeoutException:
        print("   ⚠️  [HELPER] INICIO NOT DETECTED AFTER 15s — CONTINUING")


# ==================================================================================
# INTERNAL HELPER — SCREEN READING
# ==================================================================================

def _is_visible(driver, xpath):
    try:
        return driver.find_element(By.XPATH, xpath).is_displayed()
    except:
        return False


def _screen_text(driver):
    """
    RETURNS EVERY text / content-desc ON SCREEN AS ONE STRING.
    FLUTTER OFTEN MERGES LABELS INTO ONE NODE ("Resumen\\nMonto\\n$1000.00..."),
    SO TEXT CHECKS ARE DONE OVER THE WHOLE SCREEN INSTEAD OF SINGLE ELEMENTS.
    """
    try:
        source = driver.page_source
    except Exception:
        return ""
    values = re.findall(r'(?:text|content-desc)="([^"]*)"', source)
    return html.unescape(" | ".join(v for v in values if v and v != "null"))


def _detect_state(driver):
    """
    CLASSIFIES THE CURRENT SCREEN OF THE CHARGE FLOW:
    aprobada | rechazo | msi | pin | oculta | lectura | inicio | desconocido
    "oculta" = APPIUM READS NO TEXT AT ALL. THE READER'S PIN SCREEN IS A SECURE
    WINDOW ON SOME BUILDS, SO IT SHOWS UP EMPTY INSTEAD OF "Ingresa tu PIN".
    """
    text  = _screen_text(driver)
    lower = text.lower()
    if not text.strip():
        return "oculta", text
    if any(k in lower for k in KW_APROBADA):
        return "aprobada", text
    if "ntas mensualidades" in lower or "selecciona la opci" in lower:
        return "msi", text
    if "ingresa tu pin" in lower:
        return "pin", text
    if any(k in lower for k in KW_RECHAZO) or any(k in lower for k in KW_TIEMPO):
        return "rechazo", text
    if "leyendo tarjeta" in lower or "inserta" in lower or "desliza" in lower or "acerca" in lower:
        return "lectura", text
    if "ingresa la cantidad" in lower:
        return "inicio", text
    return "desconocido", text


def _wait_state(driver, targets, timeout, label, show_countdown=False, on_state=None):
    """
    POLLS THE SCREEN UNTIL ITS STATE IS ONE OF `targets` OR THE TIMEOUT EXPIRES.
    RETURNS (state, screen_text). STATE "timeout" WHEN NOTHING MATCHED.
    on_state(state, text) IS CALLED ON EVERY POLL (USED TO CAPTURE THE PIN SCREEN
    WHILE WAITING FOR THE FINAL RESULT).
    """
    print(f"   🔎 WAITING FOR {label} (UP TO {timeout}s)...")
    end, last_print = time.time() + timeout, 0
    state, text = "desconocido", ""
    blank_polls = 0
    while time.time() < end:
        state, text = _detect_state(driver)
        if on_state:
            on_state(state, text)
        # A BLANK FRAME CAN BE A TRANSITION: "oculta" ONLY COUNTS AFTER 3 POLLS IN A ROW
        blank_polls = blank_polls + 1 if state == "oculta" else 0
        if state in targets and (state != "oculta" or blank_polls >= 3):
            print(f"   ✅ STATE DETECTED: {state.upper()}")
            return state, text
        remaining = int(end - time.time())
        if show_countdown and time.time() - last_print >= 15:
            print(f"      🕐 {remaining:03d}s REMAINING — CURRENT SCREEN: {state.upper()}")
            last_print = time.time()
        time.sleep(1)
    print(f"   ⏱️  TIMEOUT — LAST SCREEN: {state.upper()}")
    return "timeout", text


def _dump_screen(driver, limit=30):
    text = _screen_text(driver)
    print("   🔍 SCREEN DUMP:")
    for value in text.split(" | ")[:limit]:
        print(f"      📝 {value[:90]}".replace("\n", " · "))


def _manual(*lines):
    """PRINTS THE MANUAL-ACTION BANNER FOR THE TESTER."""
    print("\n" + "🖐️ " * 12)
    for line in lines:
        print(f"🖐️  {line}")
    print("🖐️ " * 12 + "\n")


def _click_label(driver, label, timeout=6):
    """
    CLICKS THE TOP-MOST ELEMENT WHOSE text / content-desc IS `label`.
    LAST RESORT: TAPS THE CENTER OF ITS bounds FROM page_source (FLUTTER NODES
    SOMETIMES SHOW IN THE SOURCE BUT ARE NOT RETURNED BY find_elements).
    """
    locators = [
        (By.XPATH, f'//*[normalize-space(@content-desc)="{label}" or normalize-space(@text)="{label}"]'),
        (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().description("{label}")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{label}")'),
    ]
    end = time.time() + timeout
    while time.time() < end:
        for locator in locators:
            try:
                elems = driver.find_elements(*locator)
                if elems:
                    elems[-1].click()
                    return True
            except Exception:
                continue
        try:
            nodes = re.findall(r'<[^>]*(?:text|content-desc)="\s*' + re.escape(label) +
                               r'\s*"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', driver.page_source)
            if nodes:
                x1, y1, x2, y2 = map(int, nodes[-1])
                driver.tap([((x1 + x2) // 2, (y1 + y2) // 2)])
                print(f"   ℹ️  '{label}' TAPPED BY COORDINATES ({(x1 + x2) // 2},{(y1 + y2) // 2})")
                return True
        except Exception:
            pass
        time.sleep(1)
    return False


def _shot(driver, test_id, name):
    try:
        utils.take_screenshot(driver, f"{test_id.replace('-', '')}_{name}", "t6")
    except Exception as e:
        print(f"   ⚠️  SCREENSHOT FAILED [{name}]: {e}")


# ==================================================================================
# INTERNAL HELPER — AMOUNTS
# ==================================================================================

def _fmt_home(monto):
    """'1000.00' → '1,000.00' (FORMAT SHOWN ON INICIO)."""
    return f"{Decimal(monto):,.2f}"


def _fmt_summary(monto):
    """'1000.00' → '1000.00' (FORMAT SHOWN IN THE PIN SUMMARY)."""
    return f"{Decimal(monto):.2f}"


def _keys_for(monto):
    """THE KEYPAD FILLS CENTS FIRST: '1000.00' → '100000' (1-0-0-0-0-0)."""
    return str(int(Decimal(monto) * 100))


def _press_key(driver, key):
    for locator in [
        (By.XPATH, f'//*[@content-desc="{key}" or @text="{key}"]'),
        (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().description("{key}")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{key}")'),
    ]:
        try:
            driver.find_element(*locator).click()
            time.sleep(0.4)
            return True
        except:
            continue
    print(f"   ⚠️  COULD NOT PRESS KEY '{key}'")
    return False


def _press_backspace(driver):
    for xpath in [config.XPATH_C_BTN_BACKSPACE, config.XPATH_C_BTN_BACKSPACE_ABSOLUTE]:
        try:
            driver.find_element(By.XPATH, xpath).click()
            time.sleep(0.5)
            return True
        except:
            continue
    print("   ⚠️  COULD NOT PRESS BACKSPACE")
    return False


def _type_amount(driver, monto):
    """TYPES THE AMOUNT AND RETURNS True IF INICIO SHOWS IT WITH THE EXPECTED FORMAT."""
    keys = _keys_for(monto)
    print(f"   ✏️  TYPING ${_fmt_home(monto)} → KEYS {'-'.join(keys)}")
    for key in keys:
        _press_key(driver, key)
    time.sleep(0.5)
    ok = _fmt_home(monto) in _screen_text(driver)
    print(f"   {'✅' if ok else '❌'} DISPLAY SHOWS ${_fmt_home(monto)}")
    return ok


def _press_realizar_cobro(driver):
    try:
        driver.find_element(By.XPATH, config.XPATH_MSI_BTN_REALIZAR_COBRO).click()
    except:
        try:
            driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Realizar cobro")'
            ).click()
        except Exception as e:
            print(f"   ❌ 'Realizar cobro' NOT CLICKABLE: {e}")
            return False
    print("   ✅ 'Realizar cobro' CLICKED")
    time.sleep(2)
    # OLDER BUILDS: "¿Qué tipo de operación?" → "Venta Normal"
    if _is_visible(driver, config.XPATH_MSI_BTN_VENTA_NORMAL):
        driver.find_element(By.XPATH, config.XPATH_MSI_BTN_VENTA_NORMAL).click()
        print("   ℹ️  'Venta Normal' SELECTED (OPERATION TYPE POPUP)")
        time.sleep(2)
    return True


# ==================================================================================
# INTERNAL HELPER — CHARGE FLOW STEPS
# ==================================================================================

def _start_charge(driver, test_id, monto, tarjeta="TARJETA DE CRÉDITO PARTICIPANTE EN MSI"):
    """
    INICIO → MONTO → "Realizar cobro" → MANUAL CARD INSERTION.
    RETURNS THE STATE AFTER READING THE CARD: msi | pin | oculta | rechazo | aprobada | inicio | timeout
    """
    print(f"\n👉 CAPTURING AMOUNT ${_fmt_home(monto)}...")
    _type_amount(driver, monto)
    _shot(driver, test_id, "01_MONTO")

    print("\n👉 CLICKING 'Realizar cobro'...")
    if not _press_realizar_cobro(driver):
        return "error"
    _shot(driver, test_id, "02_LECTURA")

    _manual(f"INSERTA LA {tarjeta} EN EL T6.",
            f"TIENES {config.MSI_TIEMPO_TARJETA}s. NO INGRESES EL NIP TODAVÍA.")
    state, _ = _wait_state(driver, {"msi", "pin", "oculta", "rechazo", "aprobada", "inicio"},
                           config.MSI_TIEMPO_TARJETA, "CARD READ", show_countdown=True)
    _shot(driver, test_id, "03_DESPUES_LECTURA")
    return state


def _to_6msi(driver, test_id, monto=None, tarjeta="TARJETA DE CRÉDITO PARTICIPANTE EN MSI",
             inspect_pin=False):
    """
    CHARGE → '¿Cuántas mensualidades?' → '6 meses sin intereses'.
    inspect_pin=True: THE TESTER MUST NOT ENTER THE NIP; WAITS FOR THE PIN SCREEN AND
    RETURNS ITS STATE (pin | oculta | aprobada | rechazo | inicio | timeout).
    inspect_pin=False: RETURNS "elegida" RIGHT AFTER CHOOSING (THE CALLER ASKS FOR THE NIP).
    RETURNS None WHEN THE MSI QUESTION DID NOT APPEAR.
    """
    monto = monto or config.MSI_MONTO_UMBRAL
    state = _start_charge(driver, test_id, monto, tarjeta)
    if state != "msi":
        print(f"   ❌ '¿Cuántas mensualidades?' DID NOT APPEAR — GOT {state.upper()}")
        return None
    _shot(driver, test_id, "03_MENSUALIDADES")
    if inspect_pin:
        _manual("NO INGRESES EL NIP: ESTA PRUEBA SOLO REVISA LA PANTALLA DE PIN.")
    if not _choose_option(driver, "6msi"):
        return None
    if not inspect_pin:
        return "elegida"
    state, _ = _wait_state(driver, {"pin", "oculta", "aprobada", "rechazo", "inicio"}, 30, "PIN SCREEN")
    _shot(driver, test_id, "04_PIN")
    if state == "oculta":
        print("   ⚠️  PIN SCREEN NOT READABLE BY APPIUM (SECURE WINDOW OF THE READER)")
    return state


def _choose_option(driver, option):
    """option: '6msi' | 'contado' | 'cancelar' ON THE '¿Cuántas mensualidades?' SHEET."""
    xpath, label = {
        "6msi":     (config.XPATH_MSI_OPC_6MSI, "6 meses sin intereses"),
        "contado":  (config.XPATH_MSI_OPC_SIN_MENSUALIDADES, "Sin mensualidades"),
        "cancelar": (config.XPATH_MSI_SHEET_CANCELAR, "Cancelar"),
    }[option]
    try:
        elems = driver.find_elements(By.XPATH, xpath)
        elems[-1].click()   # SHEET IS THE TOP-MOST LAYER
        print(f"   ✅ '{label}' SELECTED")
        time.sleep(2)
        return True
    except Exception as e:
        print(f"   ❌ COULD NOT SELECT '{label}': {e}")
        return False


def _read_summary(driver, monto):
    """READS THE PIN SCREEN 'Resumen' → (amount_ok, mensualidades or None)."""
    text = _screen_text(driver)
    amount_ok = any(f"${v}" in text or v in text for v in (_fmt_summary(monto), _fmt_home(monto)))
    match = re.search(r"Mensualidades\D{0,6}(\d+)", text)
    mens = match.group(1) if match else None
    print(f"   {'✅' if amount_ok else '❌'} SUMMARY AMOUNT ${_fmt_summary(monto)}")
    print(f"   ℹ️  SUMMARY MENSUALIDADES: {mens or 'NOT SHOWN'}")
    return amount_ok, mens


def _wait_pin_result(driver, test_id, instrucciones, monto=None):
    """
    MANUAL PIN ENTRY → WAITS FOR aprobada | rechazo | inicio | timeout.
    THE NIP BANNER IS SHOWN RIGHT AWAY (THE PIN SCREEN APPEARS 1-2s AFTER CHOOSING THE
    OPTION AND IS NOT ALWAYS READABLE). WHILE WAITING, THE SUMMARY IS READ THE FIRST
    TIME THE PIN SCREEN IS READABLE.
    RETURNS (state, text, summary) — summary = (amount_ok, mensualidades) OR None.
    """
    summary = {}

    def capture(state, _text):
        if state == "pin" and monto and "data" not in summary:
            _shot(driver, test_id, "04_PIN")
            summary["data"] = _read_summary(driver, monto)

    capture(_detect_state(driver)[0], "")
    _manual(*instrucciones, f"TIENES ~{config.MSI_TIEMPO_NIP // 60} MINUTOS.")
    state, text = _wait_state(driver, {"aprobada", "rechazo", "inicio"},
                              config.MSI_TIEMPO_NIP + 20, "TRANSACTION RESULT",
                              show_countdown=True, on_state=capture)
    _shot(driver, test_id, "05_RESULTADO")
    if monto and "data" not in summary:
        print("   ⚠️  PIN SUMMARY NOT READABLE (SECURE WINDOW OR NIP ENTERED TOO FAST) — NOT VALIDATED")
    return state, text, summary.get("data")


def _finish_approved(driver, test_id):
    """GREEN SCREEN → 'Aceptar' (→ 'Finalizar' IF TICKET SHARING IS ON) → INICIO $0.00."""
    text = _screen_text(driver)
    retira = "Ya puedes retirar tu tarjeta" in text
    # THE MESSAGE IS SHOWN ONLY WHILE THE CARD IS STILL INSERTED: INFORMATIVE, NOT A FAILURE
    print(f"   {'✅' if retira else 'ℹ️ '} 'Ya puedes retirar tu tarjeta' "
          f"{'SHOWN' if retira else 'NOT SHOWN (CARD ALREADY REMOVED?)'}")
    if _click_label(driver, "Aceptar"):
        print("   ✅ 'Aceptar' CLICKED")
        time.sleep(2)
    else:
        print("   ❌ 'Aceptar' NOT FOUND")
    if _is_visible(driver, config.XPATH_MSI_BTN_FINALIZAR):
        driver.find_element(By.XPATH, config.XPATH_MSI_BTN_FINALIZAR).click()
        print("   ℹ️  'Finalizar' CLICKED (TICKET SHARING SCREEN)")
        time.sleep(2)
    state, text = _wait_state(driver, {"inicio"}, 20, "INICIO")
    # INICIO SPLITS THE AMOUNT INTO TWO NODES: "$" | "0.00"
    en_cero = state == "inicio" and re.search(r"\$\s*(?:\|\s*)?0\.00\b", text) is not None
    print(f"   {'✅' if en_cero else '❌'} BACK ON INICIO AT $0.00")
    _shot(driver, test_id, "06_INICIO")
    return retira, en_cero


def _pin_keypad(driver):
    """
    RETURNS THE PIN KEYPAD AS ROWS OF (digit, x, y) SORTED TOP → BOTTOM.
    ONLY THE 4 BOTTOM-MOST ROWS OF SINGLE DIGITS ARE KEPT, SO THE "6" OF THE
    SUMMARY ('Mensualidades 6') IS NEVER MISTAKEN FOR A KEY.
    """
    keys = []
    for el in driver.find_elements(By.XPATH, "//*"):
        try:
            label = (el.get_attribute("content-desc") or el.get_attribute("text") or "").strip()
            if len(label) == 1 and label.isdigit():
                r = el.rect
                keys.append((label, r["x"] + r["width"] // 2, r["y"] + r["height"] // 2))
        except:
            continue
    # GROUP KEYS INTO ROWS: SAME ROW WHEN THE CENTERS ARE LESS THAN 25px APART
    rows = []
    for key in sorted(keys, key=lambda k: k[2]):
        if rows and abs(rows[-1][0][2] - key[2]) < 25:
            rows[-1].append(key)
        else:
            rows.append([key])
    return [sorted(row, key=lambda k: k[1]) for row in rows][-4:]


def _cancel_pin(driver):
    """
    PRESSES THE RED X OF THE PIN KEYPAD. THE X SITS IN THE LAST ROW, LEFT COLUMN
    (LAST ROW = X | 9 | ⌫). FALLS BACK TO ASKING THE TESTER.
    """
    for xpath in ['//*[@content-desc="Cancelar" or @content-desc="Cerrar" or '
                  '@content-desc="X" or @content-desc="✕"]']:
        if _is_visible(driver, xpath):
            driver.find_element(By.XPATH, xpath).click()
            print("   ✅ PIN CANCEL KEY CLICKED")
            return True
    rows = _pin_keypad(driver)
    if len(rows) == 4 and rows[0]:
        x = rows[0][0][1]            # LEFT COLUMN CENTER
        y = rows[-1][0][2]           # LAST ROW CENTER
        driver.tap([(x, y)])
        print(f"   ✅ RED X TAPPED AT ({x},{y})")
        time.sleep(2)
        return True
    _manual("NO PUDE UBICAR LA X ROJA (TECLADO NO LEGIBLE PARA APPIUM).",
            "PRESIONA TÚ LA X ROJA DEL TECLADO DE PIN. NO INGRESES EL NIP.")
    return False


def _back_home_after_cancel(driver, test_id):
    """AFTER A CANCELLATION: NOT APPROVED + BACK ON INICIO."""
    _manual("SI EL T6 LO PIDE, RETIRA LA TARJETA.")
    state, _ = _wait_state(driver, {"inicio", "aprobada"}, 60, "INICIO AFTER CANCEL")
    _shot(driver, test_id, "05_DESPUES_CANCELAR")
    return state == "inicio"


# ==================================================================================
# CASE RUNNER
# ==================================================================================

def _run_case(test_id, title, body):
    """
    SHARED SKELETON: SESSION → LOGIN → body(driver, wait, test_id) → RESULT.
    body RETURNS (ok, note); ok=None MEANS "NEEDS MANUAL VALIDATION" (SKIPPED (MANUAL)).
    PRINTS ONE "📊 <ID> RESULT:" LINE FOR THE HTML REPORT.
    """
    print("\n" + "=" * 60)
    print(f"{test_id}: {title}")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result, note = "FAIL", ""
    try:
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN FLOW...")
        helper_login_to_calculator(driver, wait)
        ok, note = body(driver, wait, test_id)
        result = "SKIPPED (MANUAL)" if ok is None else ("SUCCESS" if ok else "FAIL")
        if ok is False:
            _dump_screen(driver)
    except Exception as e:
        note = f"CRITICAL ERROR: {e}"
        print(f"\n💥 {test_id} CRITICAL ERROR: {e}")
        _shot(driver, test_id, "CRITICAL_ERROR")
    finally:
        print("\n" + "-" * 60)
        print(f"📊 {test_id} RESULT: {result} — {note}")
        print("-" * 60)
        utils.close_driver(driver)
    return None if result.startswith("SKIPPED") else result == "SUCCESS"


# ==================================================================================
# REUSABLE CASE BODIES
# ==================================================================================

def _body_full_charge(monto, option, expect_mens):
    """
    APPROVED CHARGE: option = '6msi' | 'contado' | None (NO SHEET EXPECTED).
    expect_mens = "6" | None (SUMMARY WITHOUT MENSUALIDADES).
    """
    def body(driver, wait, test_id):
        state = _start_charge(driver, test_id, monto)
        if option is None:
            if state == "msi":
                _choose_option(driver, "cancelar")
                _back_home_after_cancel(driver, test_id)
                return False, f"'¿Cuántas mensualidades?' SHOWN FOR ${_fmt_home(monto)} (NOT EXPECTED)"
            if state not in ("pin", "oculta", "aprobada"):
                return False, f"EXPECTED PIN WITHOUT MSI QUESTION, GOT {state.upper()}"
            print("   ✅ NO '¿Cuántas mensualidades?' — STRAIGHT TO PIN")
        else:
            if state != "msi":
                return False, f"EXPECTED '¿Cuántas mensualidades?', GOT {state.upper()}"
            _shot(driver, test_id, "03_MENSUALIDADES")
            if not _choose_option(driver, option):
                return False, f"COULD NOT CHOOSE '{option}'"

        state, _, summary = _wait_pin_result(
            driver, test_id, ["INGRESA EL NIP CORRECTO EN EL T6 Y PRESIONA 'Aceptar'."], monto)
        if state != "aprobada":
            return False, f"TRANSACTION NOT APPROVED — RESULT {state.upper()}"
        _, en_cero = _finish_approved(driver, test_id)

        # SUMMARY IS VALIDATED ONLY WHEN APPIUM COULD READ THE PIN SCREEN
        if summary:
            amount_ok, mens = summary
            mens_ok = (mens == expect_mens) if expect_mens else mens in (None, "1", "0")
            resumen = f"summary amount={amount_ok} | mensualidades={mens or '-'} (expected {expect_mens or 'none'})"
        else:
            amount_ok = mens_ok = True
            resumen = "summary NOT READABLE (not validated)"
        return amount_ok and mens_ok and en_cero, f"APPROVED | {resumen} | back to $0.00={en_cero}"
    return body


def _body_sheet_check(monto, expect_sheet):
    """VERIFIES WHETHER '¿Cuántas mensualidades?' APPEARS FOR AN AMOUNT, THEN CANCELS (NO CHARGE)."""
    def body(driver, wait, test_id):
        state = _start_charge(driver, test_id, monto)
        return _validate_sheet(driver, test_id, state, expect_sheet, f"${_fmt_home(monto)}")
    return body


def _validate_sheet(driver, test_id, state, expect_sheet, label):
    """
    SHARED BY 003/004/005/019/025: DID THE MSI QUESTION APPEAR AFTER THE CARD READ?
    pin / oculta / aprobada ALL MEAN "WENT STRAIGHT TO PIN" (NO QUESTION).
    THEN CANCELS TO AVOID A CHARGE (IF IT WAS ALREADY APPROVED, IT JUST CLOSES IT).
    """
    if state not in ("msi", "pin", "oculta", "aprobada"):
        return False, f"CARD READ DID NOT REACH MSI/PIN — GOT {state.upper()}"
    shown = state == "msi"
    print(f"   {'✅' if shown == expect_sheet else '❌'} MSI QUESTION "
          f"{'SHOWN' if shown else 'NOT SHOWN'} (EXPECTED {'SHOWN' if expect_sheet else 'NOT SHOWN'})")
    _shot(driver, test_id, "04_VALIDACION")
    note = f"{label} → MSI QUESTION {'SHOWN' if shown else 'NOT SHOWN'}"
    if state == "aprobada":
        print("   ⚠️  THE NIP WAS ENTERED — A CHARGE WAS MADE")
        _finish_approved(driver, test_id)
        return shown == expect_sheet, note + " | WARNING: CHARGE APPROVED (NIP ENTERED)"
    print("\n👉 CANCELLING TO AVOID A CHARGE...")
    _choose_option(driver, "cancelar") if shown else _cancel_pin(driver)
    _back_home_after_cancel(driver, test_id)
    return shown == expect_sheet, note


# ==================================================================================
# TC-MSI-001 … TC-MSI-025
# ==================================================================================

def TC_MSI_001():
    return _run_case("TC-MSI-001", "$500 DE CONTADO APROBADO (SIN MSI)",
                     _body_full_charge(config.MSI_MONTO_CONTADO, None, None))


def TC_MSI_002():
    return _run_case("TC-MSI-002", "$1,000 A 6 MSI APROBADO",
                     _body_full_charge(config.MSI_MONTO_UMBRAL, "6msi", config.MSI_MENSUALIDADES))


def TC_MSI_003():
    return _run_case("TC-MSI-003", "$999.99 NO OFRECE MSI",
                     _body_sheet_check(config.MSI_MONTO_DEBAJO, expect_sheet=False))


def TC_MSI_004():
    # RULE CHECK: IF THIS FAILS, THE RULE IS "> $1,000" INSTEAD OF ">= $1,000"
    return _run_case("TC-MSI-004", "$1,000.00 EXACTO OFRECE 6 MSI",
                     _body_sheet_check(config.MSI_MONTO_UMBRAL, expect_sheet=True))


def TC_MSI_005():
    return _run_case("TC-MSI-005", "$1,000.01 OFRECE 6 MSI",
                     _body_sheet_check(config.MSI_MONTO_ARRIBA, expect_sheet=True))


def TC_MSI_006():
    return _run_case("TC-MSI-006", "$5,000 A 6 MSI APROBADO",
                     _body_full_charge(config.MSI_MONTO_ALTO, "6msi", config.MSI_MENSUALIDADES))


def TC_MSI_007():
    def body(driver, wait, test_id):
        if _start_charge(driver, test_id, config.MSI_MONTO_UMBRAL) != "msi":
            return False, "'¿Cuántas mensualidades?' DID NOT APPEAR"
        _shot(driver, test_id, "04_MENSUALIDADES")
        text = _screen_text(driver)
        checks = {
            "TÍTULO '¿Cuántas mensualidades?'": "ntas mensualidades" in text,
            "'Selecciona la opción de pago'":  "Selecciona la opci" in text,
            "'Sin mensualidades'":             "Sin mensualidades" in text,
            "'Pago de contado'":               "Pago de contado" in text,
            "'6 meses sin intereses'":         "6 meses sin intereses" in text,
            "'MSI'":                           "MSI" in text,
            "BOTÓN 'Cancelar'":                _is_visible(driver, config.XPATH_MSI_SHEET_CANCELAR),
        }
        for label, ok in checks.items():
            print(f"   {'✅' if ok else '❌'} {label}")
        _choose_option(driver, "cancelar")
        _back_home_after_cancel(driver, test_id)
        missing = [k for k, v in checks.items() if not v]
        return not missing, f"MISSING: {missing}" if missing else "ALL ELEMENTS PRESENT"
    return _run_case("TC-MSI-007", "ELEMENTOS DE '¿CUÁNTAS MENSUALIDADES?'", body)


def TC_MSI_008():
    return _run_case("TC-MSI-008", ">= $1,000 CON 'SIN MENSUALIDADES' APROBADO",
                     _body_full_charge(config.MSI_MONTO_SIN_MENS, "contado", None))


def TC_MSI_009():
    def body(driver, wait, test_id):
        if _start_charge(driver, test_id, config.MSI_MONTO_UMBRAL) != "msi":
            return False, "'¿Cuántas mensualidades?' DID NOT APPEAR"
        _choose_option(driver, "cancelar")
        home = _back_home_after_cancel(driver, test_id)
        return home, "CANCELLED AND BACK ON INICIO" if home else "DID NOT RETURN TO INICIO (OR WAS APPROVED)"
    return _run_case("TC-MSI-009", "'CANCELAR' EN '¿CUÁNTAS MENSUALIDADES?'", body)


def _pin_not_reached(driver, test_id, state):
    """NOTE FOR inspect_pin CASES THAT ENDED OUTSIDE THE PIN SCREEN (CLOSES AN APPROVED CHARGE)."""
    if state == "aprobada":
        _finish_approved(driver, test_id)
        return False, "APPROVED BEFORE THE CHECK — THE NIP WAS ENTERED (A CHARGE WAS MADE)"
    return False, f"PIN SCREEN NOT REACHED — GOT {(state or 'NO MSI QUESTION').upper()}"


def TC_MSI_010():
    def body(driver, wait, test_id):
        state = _to_6msi(driver, test_id, inspect_pin=True)
        if state == "oculta":
            _cancel_pin(driver)
            _back_home_after_cancel(driver, test_id)
            return None, "PIN SCREEN NOT READABLE BY APPIUM — VALIDATE SUMMARY AND KEYPAD BY EYE"
        if state != "pin":
            return _pin_not_reached(driver, test_id, state)
        amount_ok, mens = _read_summary(driver, config.MSI_MONTO_UMBRAL)
        keypad = _pin_keypad(driver)
        digits = sorted(k[0] for row in keypad for k in row)
        text = _screen_text(driver)
        checks = {
            "'Ingresa tu PIN en el lector'": "Ingresa tu PIN" in text,
            "'Resumen'":                     "Resumen" in text,
            f"MONTO ${_fmt_summary(config.MSI_MONTO_UMBRAL)}": amount_ok,
            f"MENSUALIDADES {config.MSI_MENSUALIDADES}": mens == config.MSI_MENSUALIDADES,
            "TECLADO 0-9":                   digits == list("0123456789"),
            "BOTÓN 'Aceptar'":               _is_visible(driver, config.XPATH_MSI_PIN_BTN_ACEPTAR),
        }
        for label, ok in checks.items():
            print(f"   {'✅' if ok else '❌'} {label}")
        _cancel_pin(driver)
        _back_home_after_cancel(driver, test_id)
        missing = [k for k, v in checks.items() if not v]
        return not missing, f"MISSING: {missing}" if missing else "SUMMARY AND KEYPAD OK"
    return _run_case("TC-MSI-010", "RESUMEN DEL PIN (MONTO + MENSUALIDADES)", body)


def _body_pin_not_approved(instrucciones, label, expect_states=("rechazo", "inicio")):
    """MANUAL PIN SCENARIO THAT MUST *NOT* END APPROVED."""
    def body(driver, wait, test_id):
        if _to_6msi(driver, test_id) is None:
            return False, "'¿Cuántas mensualidades?' DID NOT APPEAR"
        state, text, _ = _wait_pin_result(driver, test_id, instrucciones)
        if state == "aprobada":
            _finish_approved(driver, test_id)
            return False, f"{label}: TRANSACTION WAS APPROVED (A CHARGE WAS MADE)"
        msg = next((v for v in text.split(" | ")
                    if any(k in v.lower() for k in KW_RECHAZO + KW_TIEMPO)), "")
        print(f"   ℹ️  MESSAGE SHOWN: '{msg or 'NONE'}'")
        _back_home_after_cancel(driver, test_id)
        return state in expect_states, f"{label}: RESULT {state.upper()} | MESSAGE '{msg[:60]}'"
    return body


def TC_MSI_011():
    return _run_case("TC-MSI-011", "NIP INCORRECTO RECHAZA LA TRANSACCIÓN", _body_pin_not_approved(
        ["INGRESA UN NIP INCORRECTO (4 DÍGITOS) Y PRESIONA 'Aceptar'.",
         "CUIDADO: VARIOS NIP INCORRECTOS PUEDEN BLOQUEAR LA TARJETA."], "WRONG PIN"))


def TC_MSI_012():
    def body(driver, wait, test_id):
        state = _to_6msi(driver, test_id, inspect_pin=True)
        if state not in ("pin", "oculta"):
            return _pin_not_reached(driver, test_id, state)
        _cancel_pin(driver)
        home = _back_home_after_cancel(driver, test_id)
        return home, "RED X CANCELLED THE CHARGE" if home else "DID NOT RETURN TO INICIO"
    return _run_case("TC-MSI-012", "X ROJA DEL TECLADO DE PIN CANCELA EL COBRO", body)


def TC_MSI_013():
    def body(driver, wait, test_id):
        if _to_6msi(driver, test_id) is None:
            return False, "'¿Cuántas mensualidades?' DID NOT APPEAR"
        state, _, _ = _wait_pin_result(driver, test_id, [
            "1) ESCRIBE 3 DÍGITOS DEL NIP.",
            "2) BORRA 1 CON LA TECLA NARANJA (DEBE DESAPARECER UN PUNTO).",
            "3) COMPLETA EL NIP CORRECTO Y PRESIONA 'Aceptar'."])
        if state != "aprobada":
            return False, f"NOT APPROVED AFTER CORRECTING THE PIN — {state.upper()}"
        _, en_cero = _finish_approved(driver, test_id)
        return True, f"APPROVED AFTER CORRECTING THE PIN | back to $0.00={en_cero}"
    return _run_case("TC-MSI-013", "BORRAR UN DÍGITO Y CORREGIR EL NIP", body)


def TC_MSI_014():
    def body(driver, wait, test_id):
        state = _to_6msi(driver, test_id, inspect_pin=True)
        if state not in ("pin", "oculta"):
            return _pin_not_reached(driver, test_id, state)
        _manual("ESCRIBE SOLO 2 DÍGITOS Y PRESIONA 'Aceptar'. NO COMPLETES EL NIP.")
        time.sleep(25)
        state, _ = _detect_state(driver)
        _shot(driver, test_id, "05_NIP_INCOMPLETO")
        still_pin = state in ("pin", "oculta")
        print(f"   {'✅' if still_pin else '❌'} STILL ON PIN SCREEN (INCOMPLETE PIN NOT SENT) — {state.upper()}")
        if still_pin:
            _cancel_pin(driver)
        _back_home_after_cancel(driver, test_id)
        return still_pin, "INCOMPLETE PIN NOT SENT" if still_pin else f"SCREEN CHANGED TO {state.upper()}"
    return _run_case("TC-MSI-014", "'ACEPTAR' CON NIP INCOMPLETO", body)


def TC_MSI_015():
    def body(driver, wait, test_id):
        orders = []
        for attempt in (1, 2):
            print(f"\n   🔁 ATTEMPT {attempt}/2")
            state = _to_6msi(driver, f"{test_id}-{attempt}", inspect_pin=True)
            if state == "oculta":
                _cancel_pin(driver)
                _back_home_after_cancel(driver, f"{test_id}-{attempt}")
                return None, "PIN KEYPAD NOT READABLE BY APPIUM — COMPARE THE ORDER BY EYE"
            if state != "pin":
                return _pin_not_reached(driver, f"{test_id}-{attempt}", state)
            order = "".join(k[0] for row in _pin_keypad(driver) for k in row)
            print(f"   ℹ️  KEYPAD ORDER: {order or 'NOT READABLE'}")
            orders.append(order)
            _cancel_pin(driver)
            if not _back_home_after_cancel(driver, f"{test_id}-{attempt}"):
                return False, "DID NOT RETURN TO INICIO BETWEEN ATTEMPTS"
        if not all(len(o) == 10 for o in orders):
            return False, f"KEYPAD NOT READABLE: {orders}"
        changed = orders[0] != orders[1]
        return changed, f"ORDERS {orders[0]} vs {orders[1]} — {'RANDOM' if changed else 'SAME ORDER'}"
    return _run_case("TC-MSI-015", "TECLADO DE PIN EN ORDEN ALEATORIO", body)


def TC_MSI_016():
    return _run_case("TC-MSI-016", "SIN NIP — EL COBRO EXPIRA POR TIEMPO", _body_pin_not_approved(
        ["NO TOQUES NADA: NO INGRESES EL NIP.",
         "LA PRUEBA ESPERA A QUE EL COBRO EXPIRE POR TIEMPO."], "PIN TIMEOUT"))


def TC_MSI_017():
    def body(driver, wait, test_id):
        print(f"\n👉 CAPTURING AMOUNT ${_fmt_home(config.MSI_MONTO_CONTADO)}...")
        _type_amount(driver, config.MSI_MONTO_CONTADO)
        if not _press_realizar_cobro(driver):
            return False, "'Realizar cobro' NOT CLICKED"
        _manual("NO INSERTES NINGUNA TARJETA. LA PRUEBA ESPERA A QUE LA LECTURA EXPIRE.")
        state, text = _wait_state(driver, {"rechazo", "inicio", "msi", "pin", "oculta", "aprobada"},
                                  config.MSI_TIEMPO_TARJETA + 60, "CARD READ TIMEOUT", show_countdown=True)
        _shot(driver, test_id, "04_SIN_TARJETA")
        if state == "rechazo":
            _back_home_after_cancel(driver, test_id)
        ok = state in ("rechazo", "inicio")
        return ok, f"WITHOUT CARD → {state.upper()}"
    return _run_case("TC-MSI-017", "SIN TARJETA — LA LECTURA EXPIRA", body)


def TC_MSI_019():
    return _run_case("TC-MSI-019", "TARJETA DE DÉBITO >= $1,000 NO OFRECE MSI", _body_debit())


def _body_debit():
    def body(driver, wait, test_id):
        state = _start_charge(driver, test_id, config.MSI_MONTO_UMBRAL, "TARJETA DE DÉBITO")
        return _validate_sheet(driver, test_id, state, False, "DEBIT CARD")
    return body


def TC_MSI_020():
    def body(driver, wait, test_id):
        if _to_6msi(driver, test_id) is None:
            return False, "'¿Cuántas mensualidades?' DID NOT APPEAR"
        _manual("NO RETIRES LA TARJETA HASTA QUE APAREZCA 'Transacción aprobada'.")
        state, text, _ = _wait_pin_result(driver, test_id, ["INGRESA EL NIP CORRECTO Y PRESIONA 'Aceptar'."])
        if state != "aprobada":
            return False, f"NOT APPROVED — {state.upper()}"
        checks = {
            "'Transacción aprobada'":        "Transacción aprobada" in text,
            "'Ya puedes retirar tu tarjeta'": "Ya puedes retirar tu tarjeta" in text,
            "BOTÓN 'Aceptar'":               "Aceptar" in _screen_text(driver),
        }
        for label, ok in checks.items():
            print(f"   {'✅' if ok else '❌'} {label}")
        _, en_cero = _finish_approved(driver, test_id)
        missing = [k for k, v in checks.items() if not v]
        return not missing and en_cero, f"MISSING: {missing} | back to $0.00={en_cero}"
    return _run_case("TC-MSI-020", "PANTALLA 'TRANSACCIÓN APROBADA' Y 'ACEPTAR'", body)


def TC_MSI_021():
    def body(driver, wait, test_id):
        print("\n👉 OPENING 'Transacciones' TAB...")
        utils.click_element(driver, config.XPATH_PÑ_TAB_TRANSACTIONS)
        time.sleep(4)
        _shot(driver, test_id, "01_TRANSACCIONES")
        target = None
        for el in driver.find_elements(By.XPATH, config.XPATH_TS_ITEM_APPROVAL_STATUS):
            label = (el.get_attribute("content-desc") or el.get_attribute("text") or "")
            if _fmt_home(config.MSI_MONTO_UMBRAL) in label or _fmt_summary(config.MSI_MONTO_UMBRAL) in label:
                target = el
                break
        if target is None:
            return False, f"NO APPROVED ${_fmt_home(config.MSI_MONTO_UMBRAL)} TRANSACTION IN THE LIST (RUN TC-MSI-002 FIRST)"
        print("   ✅ APPROVED $1,000.00 TRANSACTION FOUND — OPENING DETAIL")
        target.click()
        time.sleep(3)
        _shot(driver, test_id, "02_DETALLE")
        text = _screen_text(driver)
        approved = "APROBADA" in text.upper()
        msi_label = any(k in text for k in ("meses sin intereses", "MSI", "Mensualidades", "mensualidades"))
        print(f"   {'✅' if approved else '❌'} STATUS APROBADA")
        print(f"   {'✅' if msi_label else '⚠️ '} DETAIL MENTIONS MSI / MENSUALIDADES")
        return approved, f"DETAIL APROBADA={approved} | MSI LABEL={msi_label}"
    return _run_case("TC-MSI-021", "LA TRANSACCIÓN A 6 MSI APARECE EN 'TRANSACCIONES'", body)


def TC_MSI_022():
    def body(driver, wait, test_id):
        if _to_6msi(driver, test_id, tarjeta="TARJETA DE QA QUE SE DECLINA") is None:
            return False, "'¿Cuántas mensualidades?' DID NOT APPEAR"
        return _body_pin_not_approved_after_pin(driver, test_id)
    return _run_case("TC-MSI-022", "COBRO A 6 MSI RECHAZADO POR EL BANCO", body)


def _body_pin_not_approved_after_pin(driver, test_id):
    state, text, _ = _wait_pin_result(driver, test_id, ["INGRESA EL NIP DE LA TARJETA QUE SE DECLINA Y PRESIONA 'Aceptar'."])
    if state == "aprobada":
        _finish_approved(driver, test_id)
        return False, "DECLINED CARD WAS APPROVED"
    _back_home_after_cancel(driver, test_id)
    return state == "rechazo", f"DECLINED CARD → {state.upper()}"


def TC_MSI_024():
    def body(driver, wait, test_id):
        print("\n👉 CLICKING 'Realizar cobro' WITH $0.00...")
        _press_realizar_cobro(driver)
        error_shown = _is_visible(driver, config.XPATH_C_ERROR_CANTIDAD_VALIDA)
        time.sleep(3)
        state, _ = _detect_state(driver)
        _shot(driver, test_id, "01_MONTO_CERO")
        no_charge = state in ("inicio", "desconocido")
        print(f"   {'✅' if no_charge else '❌'} CARD READ NOT STARTED — SCREEN {state.upper()}")
        print(f"   {'✅' if error_shown else '⚠️ '} 'INGRESE UNA CANTIDAD VÁLIDA' MESSAGE")
        return no_charge, f"$0.00 → SCREEN {state.upper()} | ERROR MESSAGE={error_shown}"
    return _run_case("TC-MSI-024", "'REALIZAR COBRO' CON $0.00", body)


def TC_MSI_025():
    def body(driver, wait, test_id):
        print("\n👉 TYPING $1,000.00 AND DELETING ONE DIGIT...")
        _type_amount(driver, config.MSI_MONTO_UMBRAL)
        _press_backspace(driver)
        corregido = "100.00" in _screen_text(driver) and "1,000.00" not in _screen_text(driver)
        print(f"   {'✅' if corregido else '❌'} DISPLAY CHANGED TO $100.00")
        _shot(driver, test_id, "01_MONTO_CORREGIDO")
        if not _press_realizar_cobro(driver):
            return False, "'Realizar cobro' NOT CLICKED"
        _manual("INSERTA LA TARJETA DE CRÉDITO PARTICIPANTE EN MSI. NO INGRESES EL NIP.")
        state, _ = _wait_state(driver, {"msi", "pin", "oculta", "aprobada", "rechazo", "inicio"},
                               config.MSI_TIEMPO_TARJETA, "CARD READ", show_countdown=True)
        no_msi, note = _validate_sheet(driver, test_id, state, False, "$100.00")
        return corregido and no_msi, f"CORRECTED TO $100.00={corregido} | {note}"
    return _run_case("TC-MSI-025", "CORREGIR EL MONTO CON BORRAR ($1,000 → $100)", body)


def _manual_only(test_id, title):
    def runner():
        print("\n" + "=" * 60)
        print(f"{test_id}: {title}")
        print("=" * 60)
        print(f"   🖐️  MANUAL CASE — EXECUTE IT BY HAND AND RECORD THE RESULT IN THE MATRIX.")
        print(f"📊 {test_id} RESULT: SKIPPED (MANUAL)")
        return None
    return runner


TC_MSI_018 = _manual_only("TC-MSI-018", "RETIRAR LA TARJETA DURANTE 'LEYENDO TARJETA...'")
TC_MSI_023 = _manual_only("TC-MSI-023", "TICKET IMPRESO CON 6 MSI")


# ==================================================================================
# MAIN EXECUTION
# ==================================================================================

CASES = {f"{n:03d}": globals()[f"TC_MSI_{n:03d}"] for n in range(1, 26)}

if __name__ == "__main__":

    # OPTIONAL SUBSET: python Operationals_MSI.py 001 002 024
    selected = [a.zfill(3) for a in sys.argv[1:]] or list(CASES)
    unknown = [s for s in selected if s not in CASES]
    if unknown:
        print(f"❌ UNKNOWN CASES: {unknown} — VALID: 001 … 025")
        sys.exit(1)

    logger, log_file, timestamp = utils.start_report("OPERATIONALS_MSI")
    results = {}

    try:
        # EACH CASE RUNS ISOLATED: IF APPIUM DROPS A SESSION THE SUITE CONTINUES
        for key in selected:
            try:
                results[f"TC-MSI-{key}"] = CASES[key]()
            except Exception as e:
                results[f"TC-MSI-{key}"] = False
                print(f"\n💥 TC-MSI-{key} ABORTED — SESSION ERROR: {e.__class__.__name__}: {e}")
                print("   💡 CHECK THAT APPIUM IS RUNNING AND THE T6 IS CONNECTED (adb devices)")

    finally:
        print("\n" + "=" * 60)
        print("📋 OPERATIONALS_MSI — SUMMARY")
        print("=" * 60)
        for test_id, passed in results.items():
            status = "PASS" if passed else ("MANUAL" if passed is None else "FAIL")
            print(f"   {test_id:<12} {status}")
        print("=" * 60)
        utils.generate_zip_report("OPERATIONALS_MSI", logger, log_file, timestamp)
        utils.generate_html_report("OPERATIONALS_MSI", log_file, timestamp)
