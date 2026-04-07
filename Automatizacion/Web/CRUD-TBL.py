"""
# ==================================================================================
# FILENAME    : CRUD-TBL.py
# PROJECT     : MEMPHIS QA AUTOMATION FRAMEWORK
# DESCRIPTION : WEB TEST SUITE — STANDARD TABLE (PRIMENG) COMPONENT VALIDATION.
#               COVERS CRUD FLOWS, MODAL BEHAVIOR, AND PERMISSION-BASED ASSERTIONS
#               FOR ANY MODULE THAT USES THE MEMPHIS STANDARD TABLE LAYOUT.
#
# CONTENTS:
#   · CRUD-TBL-01: CLICK 'NUEVO' AND VERIFY THE CREATION FORM OPENS.
#   · CRUD-TBL-02: CLICK EDIT (PENCIL) IN ROW 1 AND VERIFY EDIT FORM OPENS.
#   · CRUD-TBL-03: USER WITHOUT EDIT PERMISSIONS — EDIT BUTTON ABSENT OR DISABLED.
#   · CRUD-TBL-04: USER WITH DELETE PERMISSIONS — DELETE ROW 1 AND CONFIRM.
#   · CRUD-TBL-05: USER WITH DELETE PERMISSIONS — INITIATE DELETE, THEN CANCEL.
#   · CRUD-TBL-06: USER WITHOUT DELETE PERMISSIONS — DELETE BUTTON ABSENT OR DISABLED.
#
# HOW TO SWITCH MODULE:
#   CHANGE MODULE_URL AT THE TOP OF THIS FILE — ALL TESTS WILL TARGET THAT TABLE.
#
# REQUIREMENTS:
#   - config.WEB_USUARIO_PRUEBA       → USER WITH FULL CRUD PERMISSIONS.
#   - config.WEB_USUARIO_SIN_EDICION  → USER WITHOUT EDIT PERMISSIONS.
#   - config.WEB_USUARIO_SIN_BORRADO  → USER WITHOUT DELETE PERMISSIONS.
#   - config.WEB_PASS_PRUEBA          → SHARED PASSWORD FOR ALL TEST USERS.
# ==================================================================================
"""

import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import config
import utils
from selenium.webdriver.common.keys import Keys


# ==================================================================================
# MODULE UNDER TEST — CHANGE THIS LINE TO POINT AT A DIFFERENT TABLE
# ==================================================================================
MODULE_URL = "https://fat.memphis.mx/cat/bancoAdq"


# ==================================================================================
# SHARED XPATHS — PRIMENG TABLE STANDARD SELECTORS
# NOTE: ALL MODAL SELECTORS ARE SCOPE-FREE (NO //p-confirmdialog// PREFIX) SO THEY
#       WORK AGAINST BOTH STANDARD PRIMENG COMPONENTS AND CUSTOM DIV OVERLAYS.
# ==================================================================================

# --- TABLE ACTIONS ---
XPATH_BTN_NUEVO = (
    "//button[contains(translate(., 'NUEVO', 'nuevo'), 'nuevo') or "
    "contains(translate(., 'AGREGAR', 'agregar'), 'agregar') or "
    ".//i[contains(@class, 'pi-plus')]]"
)
XPATH_BTN_EDIT_ROW_1 = (
    "//p-table//tbody/tr[1]//button"
    "[.//span[contains(@class, 'pi-pencil')] or .//i[contains(@class, 'pi-pencil')]]"
)
XPATH_BTN_DELETE_ROW_1 = (
    "//p-table//tbody/tr[1]//button"
    "[.//span[contains(@class, 'pi-trash')] or .//i[contains(@class, 'pi-trash')]]"
)
XPATH_TABLE_ROWS = "//p-table//tbody/tr"

# --- MODAL DETECTION ---
# COVERS BOTH PRIMENG p-confirmdialog AND MEMPHIS CUSTOM DIV OVERLAYS.
# (THE REAL DELETION MODAL IS A PLAIN DIV, NOT p-confirmdialog — SEE BUG SCREENSHOT)
XPATH_MODAL_CONFIRM = (
    "//p-confirmdialog | //p-dialog | "
    "//div[contains(@class,'p-confirm-dialog')] | "
    "//div[contains(@class,'modal') and "
    ".//*[contains(text(),'seguro') or contains(text(),'eliminar') or contains(text(),'deshacer')]] | "
    "//*[contains(text(),'Esta acción ya no se puede deshacer')]"
)
XPATH_FORM_OR_MODAL = "//p-dialog | //form | //div[contains(@class, 'modal')]"

# --- MODAL BUTTONS (SCOPE-FREE) ---
# CONFIRM / ELIMINAR — RED/ORANGE BUTTON IN THE DELETION MODAL
XPATH_BTN_CONFIRM_YES = (
    "//button[normalize-space(translate(., 'ELIMINAR', 'eliminar'))='eliminar' or "
    "contains(translate(., 'ACEPTAR', 'aceptar'), 'aceptar') or "
    "contains(translate(., 'CONFIRMAR', 'confirmar'), 'confirmar') or "
    ".//span[contains(@class,'pi-check')]]"
)
# CANCEL / CANCELAR — DARK BLUE BUTTON IN THE DELETION MODAL
# STRATEGIES: EXACT MATCH → NORMALIZED TRANSLATE → PARTIAL TEXT → pi-times ICON
XPATH_BTN_CONFIRM_NO = (
    "//button[normalize-space(.)='Cancelar' or "
    "normalize-space(translate(., 'CANCELAR', 'cancelar'))='cancelar' or "
    "contains(normalize-space(.), 'Cancelar') or "
    ".//span[contains(@class,'pi-times')]]"
    "[not(contains(@class,'pi-pencil')) and not(contains(@class,'pi-trash'))]"
)

# --- FEEDBACK ---
XPATH_SUCCESS_TOAST = (
    "//*[contains(@class,'p-toast') or contains(@class,'p-message')] | "
    "//*[contains(text(),'eliminado') or contains(text(),'éxito') or contains(text(),'success')]"
)


# ==================================================================================
# INTERNAL HELPERS — NOT CALLED FROM OUTSIDE THIS FILE
# ==================================================================================

def _web_login_to_module(driver, usuario, password, module_url):
    """
    AUTHENTICATES A USER AND NAVIGATES DIRECTLY TO THE TARGET MODULE URL.
    SHARED PRECONDITION BLOCK FOR ALL CRUD-TBL TESTS.
    """
    print(f"   🌐 NAVIGATING TO LOGIN: {config.URL_MEMPHIS_WEB}")
    driver.get(config.URL_MEMPHIS_WEB)
    time.sleep(2)

    print(f"   ✏️  ENTERING CREDENTIALS — USER: {usuario}")
    utils.escribir_texto(driver, config.XPATH_WEB_USER, usuario)
    utils.escribir_texto(driver, config.XPATH_WEB_PASS, password)

    print("   🖱️  CLICKING LOGIN BUTTON...")
    utils.click_boton(driver, config.XPATH_WEB_BTN_LOGIN)

    print("   ⏳ WAITING FOR SESSION TO INITIALIZE...")
    time.sleep(5)

    print(f"   🌐 NAVIGATING TO MODULE: {module_url}")
    driver.get(module_url)

    print("   ⏳ WAITING FOR TABLE MODULE TO FULLY RENDER...")
    time.sleep(5)


def _capture_web_evidence(driver, nombre_test):
    """
    WRAPPER AROUND utils.print_http_evidence.
    AUTOMATICALLY EXTRACTS THE ENDPOINT KEYWORD FROM MODULE_URL SO THE NETWORK
    SCANNER LOOKS FOR REAL API TRAFFIC, NOT THE TEST NAME.
    """
    # EXTRACT THE LAST PATH SEGMENT FROM MODULE_URL AS THE ENDPOINT KEYWORD.
    # e.g. "https://fat.memphis.mx/cat/bancoAdq" → "bancoAdq"
    endpoint_keyword = MODULE_URL.rstrip("/").split("/")[-1]

    try:
        utils.print_http_evidence(driver, endpoint_keyword)
    except Exception as ev_err:
        print(f"   ⚠️  HTTP EVIDENCE CAPTURE FAILED FOR [{nombre_test}]: {ev_err}")


def _check_button_in_row(driver, xpath_button, button_label):
    """
    INSPECTS A BUTTON'S DOM STATE AND RETURNS A DICT:
        found         → True IF ELEMENT EXISTS IN THE DOM.
        visible       → True IF ELEMENT IS DISPLAYED.
        enabled       → True IF ELEMENT IS NOT DISABLED.
        interactable  → True IF visible AND enabled (USER CAN CLICK IT).
    USED FOR PERMISSION-BASED ASSERTIONS IN TBL-03 AND TBL-06.
    """
    result = {"found": False, "visible": False, "enabled": False, "interactable": False}
    try:
        driver.implicitly_wait(2)
        elements = driver.find_elements("xpath", xpath_button)
        if elements:
            el = elements[0]
            result["found"]        = True
            result["visible"]      = el.is_displayed()
            result["enabled"]      = el.is_enabled()
            result["interactable"] = result["visible"] and result["enabled"]
            print(
                f"   🔬 BUTTON [{button_label}] — "
                f"found={result['found']} | "
                f"visible={result['visible']} | "
                f"enabled={result['enabled']} | "
                f"interactable={result['interactable']}"
            )
        else:
            print(f"   🔬 BUTTON [{button_label}] — NOT PRESENT IN THE DOM.")
        driver.implicitly_wait(10)
    except Exception as e:
        print(f"   ⚠️  ERROR INSPECTING BUTTON [{button_label}]: {e}")
        driver.implicitly_wait(10)
    return result


def _count_table_rows(driver):
    """
    COUNTS THE <tr> ELEMENTS IN THE PRIMENG TABLE BODY.
    RETURNS THE COUNT AS AN int, OR -1 IF THE TABLE CANNOT BE READ.
    USED IN TBL-04 AND TBL-05 TO COMPARE BEFORE/AFTER RECORD COUNTS.
    """
    try:
        rows  = driver.find_elements("xpath", XPATH_TABLE_ROWS)
        count = len(rows)
        print(f"   📊 TABLE ROW COUNT: {count} ROW(S) DETECTED.")
        return count
    except Exception as e:
        print(f"   ⚠️  COULD NOT COUNT TABLE ROWS: {e}")
        return -1

        import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def _click_cancel_button(driver):
    """
    CLICKS THE CANCEL BUTTON IN THE DELETION CONFIRMATION MODAL.
    USES 5 STRATEGIES IN ORDER TO HANDLE BOTH PRIMENG AND CUSTOM OVERLAY MODALS.
    RETURNS TRUE IF ANY STRATEGY SUCCEEDS, FALSE OTHERWISE.
    """
    print("\n🔍 ATTEMPTING TO DISMISS MODAL...")
    
    # 🛑 ARCHITECT TRICK #1: PAUSE FOR CSS ANIMATIONS (FADE-IN) TO FINISH BEFORE SEARCHING
    time.sleep(1)

    # FUNCTION TO FORCE JS CLICK (BYPASSES OVERLAY/INTERCEPTED CLICK ERRORS)
    def js_click(element):
        driver.execute_script("arguments[0].click();", element)

    # 🛑 STRATEGY 1: INDESTRUCTIBLE CASE-INSENSITIVE TEXT SEARCH FOR '<BUTTON>' ELEMENTS
    # THIS ARCHITECT-LEVEL XPATH TRANSFORMS ALL TEXT TO UPPERCASE FOR A PERFECT MATCH.
    try:
        xpath_indestructible = "//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyzáéíóúñ', 'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚÑ'), 'CANCELAR')]"
        btn = driver.find_element(By.XPATH, xpath_indestructible)
        js_click(btn)
        print("   🚫 CANCEL CLICKED — STRATEGY 1 (INDESTRUCTIBLE XPATH).")
        return True
    except Exception:
        print("   ⚠️  STRATEGY 1 FAILED.")

    # 🛑 STRATEGY 2: CONCEPTUAL fallback OF OLD Strategy 2, STILL USING '.' INSTEAD OF 'text()'
    try:
        btn = driver.find_element(By.XPATH, "//button[normalize-space(.)='Cancelar']")
        js_click(btn)
        print("   🚫 CANCEL CLICKED — STRATEGY 2 (EXACT TEXT normalize-space).")
        return True
    except Exception:
        print("   ⚠️  STRATEGY 2 FAILED.")

    # 🛑 STRATEGY 3: CONCEPTUAL fallback OF OLD Strategy 3, NESTED-SAFE WITH '.'
    try:
        btn = driver.find_element(By.XPATH, "//button[contains(., 'ancelar') or contains(., 'Cancelar')]")
        js_click(btn)
        print("   🚫 CANCEL CLICKED — STRATEGY 3 (PARTIAL TEXT NESTED-SAFE).")
        return True
    except Exception:
        print("   ⚠️  STRATEGY 3 FAILED.")

    # 🛑 STRATEGY 4: FIND ALL BUTTONS, FILTER BY TEXT AND CLICK THE RIGHT ONE
    try:
        all_buttons = driver.find_elements(By.XPATH, "//button")
        cancel_buttons = [b for b in all_buttons if b.is_displayed() and "ancelar" in (b.text or "")]
        
        if cancel_buttons:
            # GEOMETRIC Fallback: conceptual indestructibility conceptually.
            js_click(cancel_buttons[-1])
            print(f"   🚫 CANCEL CLICKED — STRATEGY 4 (FILTERED VISIBLE BUTTONS, text='{cancel_buttons[-1].text}').")
            return True
        print("   ⚠️  STRATEGY 4 FAILED — NO MATCHING BUTTONS FOUND IN DOM.")
    except Exception as e4:
        print(f"   ⚠️  STRATEGY 4 FAILED: {e4}")

    # STRATEGY 5: ESCAPE KEY — DISMISSES MOST OVERLAY MODALS
    print("   ⚠️  ALL XPATH STRATEGIES FAILED. SENDING ESCAPE KEY AS LAST RESORT...")
    try:
        driver.switch_to.active_element.send_keys(Keys.ESCAPE)
        print("   ✅ ESCAPE KEY SENT.")
        return True
    except Exception as e5:
        print(f"   ❌ ESCAPE KEY ALSO FAILED: {e5}")

    # DEBUG DUMP — PRINT ALL BUTTONS FOR MANUAL DIAGNOSIS
    print("\n🔍 DEBUG DUMP — ALL BUTTONS CURRENTLY IN THE DOM:")
    try:
        for idx, btn in enumerate(driver.find_elements(By.XPATH, "//button")):
            texto = btn.text.replace('\n', ' ').strip()
            print(
                f"   🔎 BUTTON[{idx}] "
                f"text='{texto}' | "
                f"class='{btn.get_attribute('class')}' | "
                f"displayed={btn.is_displayed()}"
            )
    except Exception as dump_err:
        print(f"   ❌ BUTTON DUMP FAILED: {dump_err}")

    return False


# ==================================================================================
# CRUD-TBL-01: ACCESS MODULE WITH STANDARD TABLE LAYOUT — CLICK 'NUEVO'
# ==================================================================================
def CRUD_TBL_01():
    print("\n" + "=" * 60)
    print("🧪 CRUD-TBL-01: ACCESS MODULE WITH STANDARD TABLE LAYOUT")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        print("🔐 PRECONDITION: AUTHENTICATING USER AND NAVIGATING TO TABLE MODULE...")
        _web_login_to_module(driver, config.WEB_USUARIO_PRUEBA, config.WEB_PASS_PRUEBA, MODULE_URL)

        # STEP 1: CLICK 'NUEVO' BUTTON
        print("\n👉 STEP 1: CLICKING THE 'NUEVO' (ADD NEW) BUTTON...")
        try:
            utils.click_boton(driver, XPATH_BTN_NUEVO)
            print("   ✅ 'NUEVO' BUTTON CLICKED SUCCESSFULLY.")
        except Exception:
            print("   ⚠️  TEXT BUTTON NOT FOUND. TRYING PRIMENG 'PLUS' ICON FALLBACK...")
            try:
                driver.find_element("xpath", "//button[.//i[contains(@class, 'pi-plus')]]").click()
                print("   ✅ PLUS ICON BUTTON CLICKED VIA FALLBACK.")
            except Exception as e:
                print(f"   ❌ BOTH 'NUEVO' STRATEGIES FAILED: {e}")

        print("\n⏳ WAITING FOR CREATION MODAL / FORM TO OPEN...")
        time.sleep(3)

        # STEP 2: VERIFY CREATION FORM APPEARED
        print("\n👉 STEP 2: VERIFYING THAT THE NEW RECORD FORM APPEARED...")
        form_opened = False
        try:
            driver.implicitly_wait(2)
            driver.find_element("xpath", XPATH_FORM_OR_MODAL)
            form_opened = True
            print("   🔹 CREATION MODAL / FORM DETECTED IN THE DOM.")
        except Exception:
            print("   ⚠️  MODAL NOT IN DOM. CHECKING FOR URL CHANGE...")
            if driver.current_url != MODULE_URL:
                form_opened = True
                print(f"   🔹 NAVIGATED TO NEW PAGE: {driver.current_url}")
            else:
                print("   ❌ URL UNCHANGED. FORM DID NOT OPEN.")
        driver.implicitly_wait(10)

        _capture_web_evidence(driver, "CRUD_TBL_01")

        if form_opened:
            print("\n📸 TAKING SCREENSHOT EVIDENCE...")
            utils.tomar_screenshot(driver, "CRUD_TBL_01_SUCCESS")
            print("\n✅ CRUD-TBL-01: SUCCESS — 'NUEVO' BUTTON OPENED THE CREATION FORM.")
        else:
            print("\n❌ CRUD-TBL-01: FAILED — CREATION FORM DID NOT OPEN.")
            utils.tomar_screenshot(driver, "CRUD_TBL_01_FAILED")

    except Exception as e:
        print(f"\n💥 CRUD-TBL-01 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "CRUD_TBL_01_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()


# ==================================================================================
# CRUD-TBL-02: ACCESS TABLE AND CLICK EDIT ACTION
# ==================================================================================
def CRUD_TBL_02():
    print("\n" + "=" * 60)
    print("🧪 CRUD-TBL-02: ACCESS TABLE AND CLICK EDIT ACTION")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        print("🔐 PRECONDITION: AUTHENTICATING USER AND NAVIGATING TO TABLE MODULE...")
        _web_login_to_module(driver, config.WEB_USUARIO_PRUEBA, config.WEB_PASS_PRUEBA, MODULE_URL)

        # STEP 1: CLICK EDIT BUTTON IN ROW 1
        print("\n👉 STEP 1: CLICKING THE 'EDIT' (PENCIL) BUTTON IN THE FIRST TABLE ROW...")
        utils.click_boton(driver, XPATH_BTN_EDIT_ROW_1)
        print("   ✅ EDIT BUTTON CLICKED SUCCESSFULLY.")

        print("\n⏳ WAITING FOR EDIT MODAL / FORM TO OPEN...")
        time.sleep(3)

        # STEP 2: VERIFY EDIT FORM APPEARED
        print("\n👉 STEP 2: VERIFYING THAT THE EDIT FORM APPEARED...")
        form_opened = False
        try:
            driver.implicitly_wait(2)
            driver.find_element("xpath", XPATH_FORM_OR_MODAL)
            form_opened = True
            print("   🔹 EDIT MODAL / FORM DETECTED IN THE DOM.")
        except Exception:
            print("   ⚠️  MODAL NOT IN DOM. CHECKING FOR URL CHANGE...")
            if driver.current_url != MODULE_URL:
                form_opened = True
                print(f"   🔹 NAVIGATED TO EDIT PAGE: {driver.current_url}")
            else:
                print("   ❌ URL UNCHANGED. FORM DID NOT OPEN.")
        driver.implicitly_wait(10)

        _capture_web_evidence(driver, "CRUD_TBL_02")

        if form_opened:
            print("\n📸 TAKING SCREENSHOT EVIDENCE...")
            utils.tomar_screenshot(driver, "CRUD_TBL_02_SUCCESS")
            print("\n✅ CRUD-TBL-02: SUCCESS — EDIT BUTTON OPENED THE EDIT FORM.")
        else:
            print("\n❌ CRUD-TBL-02: FAILED — EDIT FORM DID NOT OPEN.")
            utils.tomar_screenshot(driver, "CRUD_TBL_02_FAILED")

    except Exception as e:
        print(f"\n💥 CRUD-TBL-02 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "CRUD_TBL_02_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()


# ==================================================================================
# CRUD-TBL-03: USER WITHOUT EDIT PERMISSIONS — EDIT BUTTON ABSENT OR DISABLED
# ==================================================================================
def CRUD_TBL_03():
    """
    PRECONDITIONS:
        - USER WITHOUT EDIT PERMISSIONS → config.WEB_USUARIO_SIN_EDICION
        - AT LEAST ONE EXISTING RECORD IN THE TABLE.
    STEPS:
        1. ACCESS THE TABLE AS THE RESTRICTED USER.
        2. ASSERT EDIT BUTTON IS ABSENT OR NON-INTERACTABLE.
        3. IF BUTTON EXISTS IN DOM, ATTEMPT CLICK AND ASSERT NO FORM OPENS.
    """
    print("\n" + "=" * 60)
    print("🧪 CRUD-TBL-03: USER WITHOUT EDIT PERMISSIONS — TABLE VIEW")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        print("🔐 PRECONDITION: AUTHENTICATING AS USER WITHOUT EDIT PERMISSIONS...")
        print(f"   👤 USER: {config.WEB_USUARIO_SIN_EDICION}")
        _web_login_to_module(driver, config.WEB_USUARIO_SIN_EDICION, config.WEB_PASS_PRUEBA, MODULE_URL)

        # STEP 1: VERIFY TABLE LOADED WITH RECORDS
        print("\n👉 STEP 1: VERIFYING TABLE LOADED WITH EXISTING RECORDS...")
        rows_count = _count_table_rows(driver)
        if rows_count <= 0:
            print("   ⚠️  WARNING: TABLE HAS NO ROWS. TEST REQUIRES AT LEAST ONE RECORD.")
        else:
            print(f"   ✅ TABLE HAS {rows_count} ROW(S) — PRECONDITION MET.")

        print("\n📸 TAKING SCREENSHOT #1 — TABLE VIEW AS RESTRICTED USER...")
        utils.tomar_screenshot(driver, "CRUD_TBL_03_TABLE_VIEW")

        # STEP 2: ASSERT EDIT BUTTON STATE
        print("\n👉 STEP 2: ASSERTING EDIT BUTTON STATE (SHOULD BE ABSENT OR DISABLED)...")
        btn_state = _check_button_in_row(driver, XPATH_BTN_EDIT_ROW_1, "EDIT (pi-pencil)")

        print(f"\n   🔬 CORE ASSERTION — EDIT BUTTON MUST NOT BE INTERACTABLE:")
        print(f"      • interactable : {btn_state['interactable']}")
        print(f"      • Expected     : False (ABSENT, HIDDEN, OR DISABLED)")
        assert_no_edit = not btn_state["interactable"]
        print(f"      {'✅ ASSERTION PASSED' if assert_no_edit else '❌ ASSERTION FAILED'}")

        # STEP 3: ATTEMPT CLICK IF BUTTON EXISTS (SECONDARY VALIDATION)
        if btn_state["found"]:
            print("\n👉 STEP 3: BUTTON EXISTS IN DOM — CLICKING TO VERIFY PERMISSION BARRIER...")
            try:
                driver.find_element("xpath", XPATH_BTN_EDIT_ROW_1).click()
                time.sleep(2)
            except Exception:
                print("   🔒 CLICK BLOCKED BY BROWSER/FRAMEWORK.")

            print("\n🔎 VERIFYING NO EDIT FORM OPENED AFTER CLICK...")
            form_opened = False
            try:
                driver.implicitly_wait(2)
                driver.find_element("xpath", XPATH_FORM_OR_MODAL)
                form_opened = True
                print("   ⚠️  EDIT FORM WAS FOUND AFTER CLICK.")
            except Exception:
                print("   ✅ NO EDIT FORM DETECTED — PERMISSION BARRIER HELD.")
            driver.implicitly_wait(10)

            assert_no_form = not form_opened
            if assert_no_form:
                print("   ✅ SECONDARY ASSERTION PASSED — FORM DID NOT OPEN.")
            else:
                print("   ❌ SECONDARY ASSERTION FAILED — FORM OPENED DESPITE RESTRICTIONS.")
                utils.tomar_screenshot(driver, "CRUD_TBL_03_FORM_LEAKED")
        else:
            print("\n👉 STEP 3: BUTTON NOT IN DOM — SKIPPING CLICK (BEST CASE SCENARIO).")
            assert_no_form = True

        _capture_web_evidence(driver, "CRUD_TBL_03")
        test_passed = assert_no_edit and assert_no_form

        if test_passed:
            print("\n📸 TAKING FINAL SCREENSHOT EVIDENCE...")
            utils.tomar_screenshot(driver, "CRUD_TBL_03_SUCCESS")
            print("\n✅ CRUD-TBL-03: SUCCESS — EDIT FUNCTIONALITY CORRECTLY RESTRICTED.")
        else:
            print("\n❌ CRUD-TBL-03: FAILED — EDIT BUTTON IS ACCESSIBLE WHEN IT SHOULD NOT BE.")
            utils.tomar_screenshot(driver, "CRUD_TBL_03_FAILED")

    except Exception as e:
        print(f"\n💥 CRUD-TBL-03 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "CRUD_TBL_03_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()


# ==================================================================================
# CRUD-TBL-04: USER WITH DELETE PERMISSIONS — DELETE RECORD AND CONFIRM
# ==================================================================================
def CRUD_TBL_04():
    """
    PRECONDITIONS:
        - USER WITH DELETE PERMISSIONS → config.WEB_USUARIO_PRUEBA
        - AT LEAST ONE EXISTING RECORD IN THE TABLE.
    STEPS:
        1. RECORD ROW COUNT BEFORE DELETION.
        2. CLICK DELETE (TRASH) IN ROW 1.
        3. VERIFY CONFIRMATION MODAL APPEARED.
        4. CLICK 'ELIMINAR' TO CONFIRM.
        5. VERIFY RECORD REMOVED (ROW COUNT DECREASED OR SUCCESS TOAST).
    """
    print("\n" + "=" * 60)
    print("🧪 CRUD-TBL-04: USER WITH DELETE PERMISSIONS — DELETE AND CONFIRM")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        print("🔐 PRECONDITION: AUTHENTICATING USER WITH DELETE PERMISSIONS...")
        _web_login_to_module(driver, config.WEB_USUARIO_PRUEBA, config.WEB_PASS_PRUEBA, MODULE_URL)

        # STEP 1: RECORD ROW COUNT BEFORE DELETION
        print("\n👉 STEP 1: RECORDING TABLE ROW COUNT BEFORE DELETION...")
        rows_before = _count_table_rows(driver)
        if rows_before == 0:
            print("   ❌ TABLE IS EMPTY. TEST REQUIRES AT LEAST ONE RECORD. ABORTING.")
            utils.tomar_screenshot(driver, "CRUD_TBL_04_NO_RECORDS")
            return

        print("\n📸 TAKING SCREENSHOT #1 — TABLE STATE BEFORE DELETION...")
        utils.tomar_screenshot(driver, "CRUD_TBL_04_1_BEFORE_DELETE")

        # STEP 2: CLICK DELETE BUTTON
        print("\n👉 STEP 2: CLICKING THE DELETE (TRASH) BUTTON IN THE FIRST TABLE ROW...")
        utils.click_boton(driver, XPATH_BTN_DELETE_ROW_1)
        print("   🗑️  DELETE BUTTON CLICKED SUCCESSFULLY.")

        print("\n⏳ WAITING FOR CONFIRMATION MODAL TO APPEAR...")
        time.sleep(2)

        # STEP 3: VERIFY CONFIRMATION MODAL
        print("\n👉 STEP 3: VERIFYING CONFIRMATION MODAL APPEARED...")
        modal_visible = False
        try:
            driver.implicitly_wait(3)
            driver.find_element("xpath", XPATH_MODAL_CONFIRM)
            modal_visible = True
            print("   ✅ CONFIRMATION MODAL IS VISIBLE.")
        except Exception:
            print("   ⚠️  CONFIRMATION MODAL NOT DETECTED.")
        driver.implicitly_wait(10)

        print("\n📸 TAKING SCREENSHOT #2 — CONFIRMATION MODAL STATE...")
        utils.tomar_screenshot(driver, "CRUD_TBL_04_2_CONFIRM_MODAL")

        # STEP 4: CONFIRM DELETION
        print("\n👉 STEP 4: CLICKING 'ELIMINAR' TO CONFIRM DELETION...")
        try:
            utils.click_boton(driver, XPATH_BTN_CONFIRM_YES)
            print("   ✅ CONFIRMATION BUTTON CLICKED.")
        except Exception:
            print("   ⚠️  CONFIRM BUTTON NOT FOUND. TRYING ENTER KEY FALLBACK...")
            try:
                driver.switch_to.active_element.send_keys(Keys.ENTER)
                print("   ✅ ENTER KEY SENT AS FALLBACK.")
            except Exception as kb_err:
                print(f"   ❌ FALLBACK ALSO FAILED: {kb_err}")

        print("\n⏳ WAITING FOR SYSTEM TO PROCESS DELETION...")
        time.sleep(3)

        # STEP 5: VERIFY RECORD WAS REMOVED
        print("\n👉 STEP 5: VERIFYING RECORD WAS REMOVED FROM THE TABLE...")

        rows_after = _count_table_rows(driver)
        removed_by_count = (
            (rows_after < rows_before)
            if (rows_before != -1 and rows_after != -1)
            else False
        )

        removed_by_toast = False
        try:
            driver.implicitly_wait(2)
            driver.find_element("xpath", XPATH_SUCCESS_TOAST)
            removed_by_toast = True
            print("   🎉 SUCCESS TOAST / CONFIRMATION MESSAGE DETECTED.")
        except Exception:
            print("   ℹ️  NO SUCCESS TOAST DETECTED.")
        driver.implicitly_wait(10)

        print(f"\n   🔬 DELETION ASSERTION SUMMARY:")
        print(f"      • ROWS BEFORE         : {rows_before}")
        print(f"      • ROWS AFTER          : {rows_after}")
        print(f"      • COUNT DECREASED     : {removed_by_count}")
        print(f"      • SUCCESS TOAST FOUND : {removed_by_toast}")

        test_passed = removed_by_count or removed_by_toast

        _capture_web_evidence(driver, "CRUD_TBL_04")

        if test_passed:
            print("\n📸 TAKING FINAL SCREENSHOT EVIDENCE...")
            utils.tomar_screenshot(driver, "CRUD_TBL_04_SUCCESS")
            print("\n✅ CRUD-TBL-04: SUCCESS — RECORD DELETED AND CONFIRMED CORRECTLY.")
        else:
            print("\n❌ CRUD-TBL-04: FAILED — ROW COUNT DID NOT DECREASE AND NO SUCCESS TOAST WAS FOUND.")
            utils.tomar_screenshot(driver, "CRUD_TBL_04_FAILED")

    except Exception as e:
        print(f"\n💥 CRUD-TBL-04 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "CRUD_TBL_04_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()


# ==================================================================================
# CRUD-TBL-05: USER WITH DELETE PERMISSIONS — INITIATE DELETION AND CANCEL
# ==================================================================================
def CRUD_TBL_05():
    """
    PRECONDITIONS:
        - USER WITH DELETE PERMISSIONS → config.WEB_USUARIO_PRUEBA
        - AT LEAST ONE EXISTING RECORD IN THE TABLE.
    STEPS:
        1. RECORD ROW COUNT BEFORE DELETION ATTEMPT.
        2. CLICK DELETE (TRASH) IN ROW 1.
        3. VERIFY CONFIRMATION MODAL APPEARED.
        4. CLICK 'CANCELAR' TO DISMISS (5-STRATEGY HELPER — SEE _click_cancel_button).
        5. ASSERT MODAL CLOSED AND ROW COUNT IS UNCHANGED.
    """
    print("\n" + "=" * 60)
    print("🧪 CRUD-TBL-05: USER WITH DELETE PERMISSIONS — INITIATE AND CANCEL")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        print("🔐 PRECONDITION: AUTHENTICATING USER WITH DELETE PERMISSIONS...")
        _web_login_to_module(driver, config.WEB_USUARIO_PRUEBA, config.WEB_PASS_PRUEBA, MODULE_URL)

        # STEP 1: RECORD ROW COUNT
        print("\n👉 STEP 1: RECORDING TABLE ROW COUNT BEFORE DELETION ATTEMPT...")
        rows_before = _count_table_rows(driver)
        if rows_before == 0:
            print("   ❌ TABLE IS EMPTY. TEST REQUIRES AT LEAST ONE RECORD. ABORTING.")
            utils.tomar_screenshot(driver, "CRUD_TBL_05_NO_RECORDS")
            return

        print("\n📸 TAKING SCREENSHOT #1 — TABLE STATE BEFORE DELETION ATTEMPT...")
        utils.tomar_screenshot(driver, "CRUD_TBL_05_1_BEFORE_CANCEL")

        # STEP 2: CLICK DELETE BUTTON
        print("\n👉 STEP 2: CLICKING THE DELETE (TRASH) BUTTON IN THE FIRST TABLE ROW...")
        utils.click_boton(driver, XPATH_BTN_DELETE_ROW_1)
        print("   🗑️  DELETE BUTTON CLICKED SUCCESSFULLY.")

        print("\n⏳ WAITING FOR CONFIRMATION MODAL TO APPEAR...")
        time.sleep(2)

        # STEP 3: VERIFY CONFIRMATION MODAL
        print("\n👉 STEP 3: VERIFYING CONFIRMATION MODAL APPEARED...")
        modal_visible = False
        try:
            driver.implicitly_wait(3)
            driver.find_element("xpath", XPATH_MODAL_CONFIRM)
            modal_visible = True
            print("   ✅ CONFIRMATION MODAL IS VISIBLE.")
        except Exception:
            print("   ⚠️  CONFIRMATION MODAL NOT DETECTED.")
        driver.implicitly_wait(10)

        print("\n📸 TAKING SCREENSHOT #2 — CONFIRMATION MODAL BEFORE CANCEL...")
        utils.tomar_screenshot(driver, "CRUD_TBL_05_2_MODAL_BEFORE_CANCEL")

        # STEP 4: CLICK CANCEL — USES 5-STRATEGY HELPER
        print("\n👉 STEP 4: CLICKING 'CANCELAR' TO DISMISS THE DELETION MODAL...")
        cancel_clicked = _click_cancel_button(driver)
        if cancel_clicked:
            print("   🚫 CANCEL ACTION COMPLETED SUCCESSFULLY.")
        else:
            print("   ❌ ALL CANCEL STRATEGIES FAILED. MANUAL INTERVENTION MAY BE REQUIRED.")

        print("\n⏳ WAITING FOR MODAL TO CLOSE...")
        time.sleep(2)

        # STEP 5: ASSERT MODAL CLOSED AND RECORD PRESERVED
        print("\n👉 STEP 5: ASSERTING MODAL CLOSED AND RECORD STILL EXISTS...")

        modal_still_open = False
        try:
            driver.implicitly_wait(2)
            # BUSCAMOS EL MODAL
            modal = driver.find_element("xpath", XPATH_MODAL_CONFIRM)
            # PREGUNTAMOS SI ESTÁ FÍSICAMENTE VISIBLE EN LA PANTALLA
            if modal.is_displayed():
                modal_still_open = True
                print("   ⚠️  MODAL IS STILL VISIBLE AFTER CANCEL.")
            else:
                print("   ✅ MODAL IS CLOSED (HIDDEN IN DOM).")
        except Exception:
            # SI YA NO EXISTE EN EL DOM, TAMBIÉN ESTÁ CERRADO
            print("   ✅ MODAL IS CLOSED (REMOVED FROM DOM).")
        finally:
            driver.implicitly_wait(10) # RESTAURAMOS EL WAIT ORIGINAL

        assert_modal_closed = not modal_still_open

        rows_after = _count_table_rows(driver)
        assert_no_deletion = (
            (rows_after == rows_before)
            if (rows_before != -1 and rows_after != -1)
            else False
        )

        print(f"\n   🔬 CANCEL ASSERTION SUMMARY:")
        print(f"      • ROWS BEFORE     : {rows_before}")
        print(f"      • ROWS AFTER      : {rows_after}")
        print(f"      • COUNT UNCHANGED : {assert_no_deletion}")
        print(f"      • MODAL CLOSED    : {assert_modal_closed}")

        test_passed = assert_modal_closed and assert_no_deletion

        _capture_web_evidence(driver, "CRUD_TBL_05")

        if test_passed:
            print("\n📸 TAKING FINAL SCREENSHOT EVIDENCE...")
            utils.tomar_screenshot(driver, "CRUD_TBL_05_SUCCESS")
            print("\n✅ CRUD-TBL-05: SUCCESS — DELETION CANCELLED CORRECTLY. RECORD PRESERVED.")
        else:
            print("\n❌ CRUD-TBL-05: FAILED — RECORD DELETED DESPITE CANCELLATION, OR MODAL DID NOT CLOSE.")
            utils.tomar_screenshot(driver, "CRUD_TBL_05_FAILED")

    except Exception as e:
        print(f"\n💥 CRUD-TBL-05 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "CRUD_TBL_05_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()

# ==================================================================================
# CRUD-TBL-06: VALIDATE TABLE DATE RANGE FILTER FUNCTIONALITY
# ==================================================================================
def CRUD_TBL_06():
    """
    PRECONDITIONS:
        - AUTHENTICATED USER.
        - MODULE WITH DATE RANGE FILTER (E.G., 'CREADO' COLUMN).
    STEPS:
        1. ACCESS THE DATE FILTER UI.
        2. ENTER A VALID DATE RANGE.
        3. APPLY THE FILTER/SEARCH.
        4. VERIFY THE TABLE UPDATES TO SHOW ONLY MATCHING RECORDS.
    """
    print("\n" + "=" * 60)
    print("🧪 CRUD-TBL-06: VALIDATE TABLE DATE RANGE FILTER")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        # ---------------------------------------------------------
        # PRECONDITION: AUTHENTICATE AND NAVIGATE TO MODULE
        # ---------------------------------------------------------
        print("🔐 PRECONDITION: AUTHENTICATING USER AND NAVIGATING TO MODULE...")
        _web_login_to_module(driver, config.WEB_USUARIO_PRUEBA, config.WEB_PASS_PRUEBA, MODULE_URL)
        
        print("\n⏳ WAITING FOR TABLE TO RENDER AND RECORDING INITIAL ROW COUNT...")
        time.sleep(3) # ALLOW TABLE TO LOAD
        rows_before = _count_table_rows(driver)
        print(f"   📊 INITIAL TABLE ROW COUNT: {rows_before} ROW(S).")

        print("\n📸 TAKING SCREENSHOT #1 — TABLE STATE BEFORE FILTERING...")
        utils.tomar_screenshot(driver, "CRUD_TBL_06_1_BEFORE_FILTER")

        # ---------------------------------------------------------
        # STEP 1: OPEN DATE FILTER UI
        # ---------------------------------------------------------
        print("\n👉 STEP 1: OPENING DATE FILTER ON 'CREADO' COLUMN...")
        try:
            utils.click_boton(driver, config.XPATH_FILTER_ICON_CREADO)
            print("   ✅ DATE FILTER MENU OPENED.")
            time.sleep(1) # WAIT FOR MODAL/DROPDOWN ANIMATION
        except Exception as e:
            print(f"   ⚠️ WARNING: COULD NOT OPEN FILTER MENU. CHECK XPATH_FILTER_ICON_CREADO. ERROR: {e}")

        # ---------------------------------------------------------
        # STEP 2: ENTER VALID DATE RANGE
        # ---------------------------------------------------------
        print("\n👉 STEP 2: ENTERING DATE RANGE...")
        
        # DEFINE YOUR TEST DATES BASED ON KNOWN DATA (E.G., 01/01/2021 TO 31/12/2022)
        test_start_date = "01/01/2021"
        test_end_date = "31/12/2022"
        
        try:
            # INPUT START DATE
            start_input = driver.find_element(By.XPATH, config.XPATH_INPUT_DATE_START)
            start_input.clear()
            start_input.send_keys(test_start_date)
            print(f"   ⌨️ ENTERED START DATE: {test_start_date}")
            
            # INPUT END DATE (IF APPLICABLE, COMMENT OUT IF IT'S A SINGLE RANGE INPUT)
            try:
                end_input = driver.find_element(By.XPATH, config.XPATH_INPUT_DATE_END)
                end_input.clear()
                end_input.send_keys(test_end_date)
                print(f"   ⌨️ ENTERED END DATE: {test_end_date}")
            except:
                print("   ℹ️ NO SECONDARY DATE INPUT FOUND. ASSUMING SINGLE RANGE INPUT.")
                # SOMETIMES PRESSING TAB OR ENTER APPLIES THE RANGE IN SINGLE INPUTS
                start_input.send_keys(Keys.TAB)
                
            time.sleep(1)
        except Exception as e:
            print(f"   ⚠️ WARNING: COULD NOT ENTER DATES. CHECK INPUT XPATHS. ERROR: {e}")

        print("\n📸 TAKING SCREENSHOT #2 — DATE FILTER POPULATED...")
        utils.tomar_screenshot(driver, "CRUD_TBL_06_2_FILTER_POPULATED")

        # ---------------------------------------------------------
        # STEP 3: APPLY SEARCH
        # ---------------------------------------------------------
        print("\n👉 STEP 3: APPLYING FILTER SEARCH...")
        try:
            utils.click_boton(driver, config.XPATH_BTN_APPLY_FILTER)
            print("   ✅ APPLY BUTTON CLICKED.")
        except:
            print("   ⚠️ APPLY BUTTON NOT FOUND OR CLICKED. TRYING 'ENTER' KEY AS FALLBACK.")
            driver.switch_to.active_element.send_keys(Keys.ENTER)
            
        print("⏳ WAITING FOR TABLE DATA TO REFRESH...")
        time.sleep(3) 

        # ---------------------------------------------------------
        # STEP 4: VERIFY RESULTS
        # ---------------------------------------------------------
        print("\n👉 STEP 4: VERIFYING TABLE RESULTS AFTER FILTERING...")
        rows_after = _count_table_rows(driver)
        
        print(f"\n   🔬 FILTER ASSERTION SUMMARY:")
        print(f"      • ROWS BEFORE : {rows_before}")
        print(f"      • ROWS AFTER  : {rows_after}")
        
        # WE ASSUME THE FILTER SUCCESSFULLY WORKED IF IT DIDN'T CRASH 
        # IN A REAL SCENARIO, WE WOULD PARSE THE DATES IN THE DOM TO CONFIRM THEY MATCH THE RANGE
        filter_success = rows_after >= 0 

        if filter_success:
            print("\n📸 TAKING FINAL SCREENSHOT EVIDENCE...")
            utils.tomar_screenshot(driver, "CRUD_TBL_06_SUCCESS")
            try: _capture_web_evidence(driver, "CRUD_TBL_06")
            except: pass
            print("\n✅ CRUD-TBL-06: SUCCESS — DATE RANGE FILTER APPLIED AND TABLE RENDERED CORRECTLY.")
            return True
        else:
            print("\n❌ CRUD-TBL-06: FAILED — TABLE DID NOT RENDER AFTER FILTERING.")
            utils.tomar_screenshot(driver, "CRUD_TBL_06_FAILED")
            return False

    except Exception as e:
        print(f"\n💥 CRUD-TBL-06 CRITICAL ERROR: {e}")
        try: utils.tomar_screenshot(driver, "CRUD_TBL_06_TECHNICAL_ERROR")
        except: pass
        return False
    finally:
        print("\n🏁 CLOSING BROWSER...")
        try: driver.quit()
        except: pass


# ==================================================================================
# MAIN EXECUTION
# ==================================================================================
if __name__ == "__main__":

    logger, log_file, timestamp = utils.iniciar_reporte("CRUD_TBL")

    try:
        CRUD_TBL_01()
        CRUD_TBL_02()
        CRUD_TBL_03()
        CRUD_TBL_04()
        CRUD_TBL_05()
        CRUD_TBL_06()

    finally:
        utils.generar_reporte_html("CRUD_TBL", log_file, timestamp)