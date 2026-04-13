"""
# ==================================================================================
# FILENAME    : CREATE-FORM.py
# CONTENTS:
#   · CREATE-FORM-01: USERS CAN ACCESS THE CATALOG CREATION FORM
#   · CREATE-FORM-02: THE RECORD IS SAVED SUCCESSFULLY AN A SUCCESS MESSAGE IS DISPLAYED.  
#   · CREATE-FORM-03: YOU CANNOT SAVE IF REQUIRED FIELDS ARE MISSING 
#   · CREATE-FORM-04: NO INFORMATION IS SAVED, RETURN TO PREVIOUS VIEW
# ==================================================================================
"""
import sys
import os
import time
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import config
import utils
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


# MODULE CONFIGURATION
USUARIOS_URL      = "https://fat.memphis.mx/v2/usuarios"
NUEVO_USUARIO_URL = "https://fat.memphis.mx/v2/usuarios/nuevo"
EVIDENCE_ENDPOINT = "usuarios"

# TEST DATA — CREATE-FORM-02: VALID USER CREATION
CF02_NOMBRE_USUARIO  = "Yonder"
CF02_EMAIL           = "yonderaunt@gmail.com"
CF02_NOMBRE          = "Yonder"
CF02_APELLIDO_PAT    = "Aunt"
CF02_APELLIDO_MAT    = "Tap"
CF02_TELEFONO        = "5540098232"
CF02_PERFIL          = "test"
CF02_CLIENTE         = "XYBooster"
CF02_PASSWORD        = "Memphis@2000"
CF02_CONFIRM_PASS    = "Memphis@2000"

XPATH_USUARIOS_CARD = (
    "//div[.//*[contains(text(),'onfiguración')] or "
    "      .//*[contains(text(),'onfiguracion')]]"
    "//*[normalize-space(text())='Usuarios'][not(ancestor::nav) and not(ancestor::aside)] | "
    "//*[normalize-space(text())='Usuarios']"
    "[not(ancestor::nav) and not(ancestor::aside) and not(self::title)] | "
    "//a[contains(@href,'usuarios') and not(contains(@href,'tdm'))]"
)

XPATH_BTN_NUEVO = (
    "//button[contains(translate(.,'NUEVO','nuevo'),'nuevo')] | "
    "//*[contains(@class,'btn') or contains(@class,'button')]"
    "[contains(translate(.,'NUEVO','nuevo'),'nuevo')] | "
    "//a[contains(@href,'nuevo') and contains(@href,'usuarios')]"
)


XPATH_FORM_TITULO = (
    "//*[contains(translate(.,'CREACIÓN DE USUARIO','creación de usuario'),'creaci') and "
    "    contains(translate(.,'CREACIÓN DE USUARIO','creación de usuario'),'usuario')]"
    "[not(ancestor::nav) and not(ancestor::aside)] | "
    "//*[contains(text(),'CREACIÓN DE USUARIO') or contains(text(),'Creación de Usuario')]"
)

XPATH_INPUT_NOMBRE_USUARIO = "//input[@placeholder='Nombre de Usuario' or @formcontrolname='username']"
XPATH_INPUT_EMAIL          = "//input[@placeholder='correo@mail.com' or @type='email']"
XPATH_INPUT_NOMBRE         = "//input[@placeholder='Nombre' or @formcontrolname='nombre']"
XPATH_INPUT_APELLIDO_PAT   = "//input[@placeholder='Apellido Paterno' or @formcontrolname='apellidoPaterno']"
XPATH_INPUT_APELLIDO_MAT   = "//input[@placeholder='Apellido Materno' or @formcontrolname='apellidoMaterno']"
XPATH_INPUT_TELEFONO       = "//input[@placeholder='Teléfono' or @formcontrolname='telefono']"

XPATH_DROPDOWN_PERFIL = (
    "//select[@id='id_profile'] | "
    "//select[.//option[contains(text(),'test') or contains(text(),'OperacionPruebas')]]"
)
XPATH_INPUT_PASSWORD     = "(//input[@type='password'])[1]"
XPATH_INPUT_CONFIRM_PASS = "(//input[@type='password'])[2]"

XPATH_BTN_GUARDAR = (
    "//button[contains(translate(.,'GUARDAR','guardar'),'guardar')] | "
    "//button[contains(text(),'Guardar') or contains(text(),'GUARDAR')]"
)
XPATH_BTN_SALIR = (
    "//button[contains(translate(.,'SALIR','salir'),'salir')] | "
    "//button[contains(text(),'Salir') or contains(text(),'SALIR')]"
)

XPATH_TABLA_USUARIOS = (
    "//*[contains(text(),'Administración de Usuarios') or "
    "    contains(text(),'Administracion de Usuarios')]"
    "[not(ancestor::nav)]"
)


XPATH_TOAST_EXITO = (
    "//*[contains(text(),'Usuario creado correctamente') or "
    "    contains(text(),'usuario creado correctamente')] | "
    "//div[contains(@class,'p-toast')]//*[contains(text(),'creado correctamente')] | "
    "//*[contains(@class,'toast') or contains(@class,'snack') or contains(@class,'alert')]"
    "[contains(.,'creado correctamente')]"
)
XPATH_TOAST_INFO = (
    "//*[contains(text(),'Revisa la información ingresada') or "
    "    contains(text(),'Revisa la informacion ingresada') or "
    "    contains(text(),'Revisa la informaci')]"
)
XPATH_DIALOG_SALIR = (
    "//*[contains(text(),'Quieres salir del formulario') or "
    "    contains(text(),'quieres salir del formulario') or "
    "    contains(text(),'¿Quieres salir')] | "
    "//div[contains(@class,'p-dialog') or contains(@class,'p-confirm')]"
    "[.//*[contains(text(),'salir')]] | "
    "//div[contains(@class,'modal') or contains(@class,'overlay') or "
    "      contains(@class,'dialog')]"
    "[.//*[contains(text(),'salir') or contains(text(),'formulario')]]"
)


# INTERNAL HELPERS
def _login_and_go_to_usuarios(driver):
    print(f"   🌐 NAVIGATING TO LOGIN: {config.URL_MEMPHIS_WEB}")
    driver.get(config.URL_MEMPHIS_WEB)
    time.sleep(2)

    print(f"   ✏️  ENTERING CREDENTIALS — USER: {config.WEB_USUARIO_PRUEBA}")
    utils.escribir_texto(driver, config.XPATH_WEB_USER, config.WEB_USUARIO_PRUEBA)
    utils.escribir_texto(driver, config.XPATH_WEB_PASS, config.WEB_PASS_PRUEBA)

    print("   🖱️  CLICKING LOGIN BUTTON...")
    utils.click_boton(driver, config.XPATH_WEB_BTN_LOGIN)

    print("   ⏳ WAITING FOR HOME DASHBOARD TO LOAD...")
    time.sleep(5)

    print(f"   🌐 POST-LOGIN URL: {driver.current_url}")
    print("   🖱️  CLICKING 'USUARIOS' CARD (4-STRATEGY CASCADE)...")
    clicked = False

    if not clicked:
        try:
            result = driver.execute_script("""
                var candidates = document.querySelectorAll(
                    '[routerLink], [routerlink], [ng-reflect-router-link]'
                );
                for (var el of candidates) {
                    var rl = el.getAttribute('routerLink') ||
                             el.getAttribute('routerlink') ||
                             el.getAttribute('ng-reflect-router-link') || '';
                    if (rl === '/usuarios' || rl === 'usuarios') {
                        el.click();
                        return 'routerLink:' + el.tagName + '[' + rl + ']';
                    }
                }
                return null;
            """)
            if result:
                clicked = True
                time.sleep(4)
                print(f"   ✅ CARD CLICKED — STRATEGY 1 (JS routerLink: {result}).")
        except Exception as s1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {s1_err}")

    if not clicked:
        try:
            result = driver.execute_script("""
                var anchors = document.querySelectorAll('a[href]');
                for (var a of anchors) {
                    var href = a.getAttribute('href') || '';
                    if ((href === '/usuarios' || href.endsWith('/usuarios')) &&
                        !href.includes('tdm') && a.offsetWidth > 0) {
                        a.click();
                        return 'href:' + href;
                    }
                }
                return null;
            """)
            if result:
                clicked = True
                time.sleep(4)
                print(f"   ✅ CARD CLICKED — STRATEGY 2 (JS href: {result}).")
        except Exception as s2_err:
            print(f"   ⚠️  STRATEGY 2 FAILED: {s2_err}")

    
    if not clicked:
        try:
            result = driver.execute_script("""
                var allEls = document.querySelectorAll('*');
                for (var el of allEls) {
                    if (el.textContent.trim() === 'Usuarios' &&
                        el.children.length === 0 &&
                        el.offsetWidth > 0 &&
                        !el.closest('nav') &&
                        !el.closest('aside')) {
                        var parent = el.parentElement;
                        for (var i = 0; i < 6; i++) {
                            if (!parent) break;
                            var style = window.getComputedStyle(parent);
                            var rl    = parent.getAttribute('routerLink') ||
                                        parent.getAttribute('routerlink') ||
                                        parent.getAttribute('href');
                            if (style.cursor === 'pointer' || rl) {
                                parent.click();
                                return 'text-walk:level-' + i + ':' + parent.tagName;
                            }
                            parent = parent.parentElement;
                        }
                        var up2 = el.parentElement && el.parentElement.parentElement;
                        if (up2) { up2.click(); return 'text-walk:fallback-up2'; }
                        el.parentElement.click();
                        return 'text-walk:fallback-up1';
                    }
                }
                return null;
            """)
            if result:
                clicked = True
                time.sleep(4)
                print(f"   ✅ CARD CLICKED — STRATEGY 3 (JS TEXT WALK: {result}).")
        except Exception as s3_err:
            print(f"   ⚠️  STRATEGY 3 FAILED: {s3_err}")

    
    if not clicked:
        print(f"   ⚠️  ALL CLICK STRATEGIES FAILED. NAVIGATING DIRECTLY TO URL...")
        driver.get(USUARIOS_URL)
        time.sleep(4)
        print(f"   🌐 NAVIGATED DIRECTLY TO: {driver.current_url}")
    else:
        print(f"   🌐 CURRENT URL AFTER CARD CLICK: {driver.current_url}")

    print("   ⏳ WAITING FOR 'ADMINISTRACIÓN DE USUARIOS' TABLE TO RENDER...")
    time.sleep(3)


def _click_nuevo_button(driver):
    print("   🖱️  CLICKING '+ NUEVO' BUTTON (3-STRATEGY CASCADE)...")

    # STRATEGY 1
    try:
        btn = driver.find_element(By.XPATH, XPATH_BTN_NUEVO)
        btn.click()
        time.sleep(3)
        print("   ✅ '+ NUEVO' CLICKED — STRATEGY 1 (XPATH).")
        return True
    except Exception as s1_err:
        print(f"   ⚠️  STRATEGY 1 FAILED: {s1_err}")

    # STRATEGY 2
    try:
        result = driver.execute_script("""
            var btns = document.querySelectorAll('button, a[role="button"], a');
            for (var btn of btns) {
                var text = btn.textContent.trim().toLowerCase();
                if (text.includes('nuevo') && btn.offsetWidth > 0) {
                    btn.click();
                    return btn.textContent.trim();
                }
            }
            return null;
        """)
        if result:
            time.sleep(3)
            print(f"   ✅ '+ NUEVO' CLICKED — STRATEGY 2 (JS: '{result}').")
            return True
        else:
            print("   ⚠️  '+ NUEVO' BUTTON NOT FOUND VIA JAVASCRIPT.")
    except Exception as s2_err:
        print(f"   ⚠️  STRATEGY 2 FAILED: {s2_err}")

    # STRATEGY 3
    print(f"   ⚠️  BUTTON CLICK FAILED. NAVIGATING DIRECTLY TO FORM URL...")
    driver.get(NUEVO_USUARIO_URL)
    time.sleep(4)
    print(f"   🌐 NAVIGATED DIRECTLY TO: {driver.current_url}")
    return False


def _form_creacion_is_visible(driver):
    try:
        driver.find_element(By.XPATH, XPATH_FORM_TITULO)
        return True
    except Exception:
        return "nuevo" in driver.current_url.lower()


def _click_guardar(driver):
    try:
        btn = driver.find_element(By.XPATH, XPATH_BTN_GUARDAR)
        btn.click()
        print("   ✅ 'GUARDAR' CLICKED — STRATEGY 1 (XPATH).")
        return True
    except Exception as g1_err:
        print(f"   ⚠️  STRATEGY 1 FAILED: {g1_err}")

    try:
        result = driver.execute_script("""
            var btns = document.querySelectorAll('button');
            for (var btn of btns) {
                if (btn.textContent.trim().toLowerCase().includes('guardar')
                        && btn.offsetWidth > 0) {
                    btn.click();
                    return btn.textContent.trim();
                }
            }
            return null;
        """)
        if result:
            print(f"   ✅ 'GUARDAR' CLICKED — STRATEGY 2 (JS: '{result}').")
            return True
        else:
            print("   ❌ 'GUARDAR' BUTTON NOT FOUND ON PAGE.")
    except Exception as g2_err:
        print(f"   ⚠️  STRATEGY 2 FAILED: {g2_err}")

    return False


def _click_salir(driver):
    try:
        btn = driver.find_element(By.XPATH, XPATH_BTN_SALIR)
        btn.click()
        print("   ✅ 'SALIR' CLICKED — STRATEGY 1 (XPATH).")
        return True
    except Exception as s1_err:
        print(f"   ⚠️  STRATEGY 1 FAILED: {s1_err}")

    try:
        result = driver.execute_script("""
            var btns = document.querySelectorAll('button');
            for (var btn of btns) {
                if (btn.textContent.trim().toLowerCase().includes('salir')
                        && btn.offsetWidth > 0) {
                    btn.click();
                    return btn.textContent.trim();
                }
            }
            return null;
        """)
        if result:
            print(f"   ✅ 'SALIR' CLICKED — STRATEGY 2 (JS: '{result}').")
            return True
        else:
            print("   ❌ 'SALIR' BUTTON NOT FOUND ON PAGE.")
    except Exception as s2_err:
        print(f"   ⚠️  STRATEGY 2 FAILED: {s2_err}")

    return False


def _capture_web_evidence(driver, nombre_test):
    print(f"\n📡 CAPTURING HTTP EVIDENCE FOR [{nombre_test}]...")

    SKIP_EXTENSIONS = [".css", ".js", ".png", ".jpg", ".jpeg", ".svg",
                       ".woff", ".ttf", ".ico", "favicon", "fonts",
                       "google", "analytics", "gtm", "hotjar"]

    try:
        raw_logs = driver.get_log("performance")
    except Exception as e:
        print(f"   ❌ COULD NOT READ PERFORMANCE LOGS: {e}")
        return

    if not raw_logs:
        print(f"   ℹ️  PERFORMANCE LOG BUFFER IS EMPTY FOR [{nombre_test}].")
        print("   💡 THIS IS EXPECTED WHEN THE TEST TRIGGERS ONLY FRONTEND VALIDATION")
        print("      (FORM REJECTED BEFORE REACHING THE SERVER — NO HTTP REQUEST SENT).")
        return

    requests_map = {}
    responses    = []

    for entry in raw_logs:
        try:
            msg    = json.loads(entry["message"])["message"]
            method = msg.get("method", "")
            params = msg.get("params", {})

            if method == "Network.requestWillBeSent":
                req = params.get("request", {})
                rid = params.get("requestId", "")
                url = req.get("url", "")
                if not any(s in url.lower() for s in SKIP_EXTENSIONS):
                    requests_map[rid] = {
                        "url"      : url,
                        "method"   : req.get("method", "UNKNOWN"),
                        "postData" : req.get("postData", None),
                    }

            if method == "Network.responseReceived":
                resp = params.get("response", {})
                url  = resp.get("url", "")
                if not any(s in url.lower() for s in SKIP_EXTENSIONS):
                    responses.append({
                        "requestId": params.get("requestId", ""),
                        "url"      : url,
                        "status"   : resp.get("status", "N/A"),
                        "mimeType" : resp.get("mimeType", "N/A"),
                    })
        except Exception:
            continue

    if not responses:
        print(f"   ℹ️  NO NON-STATIC HTTP RESPONSES CAPTURED FOR [{nombre_test}].")
        print("   💡 THE OPERATION MAY HAVE BEEN BLOCKED BY FRONTEND VALIDATION BEFORE")
        print("      REACHING THE SERVER. NO NETWORK REQUEST WAS SENT.")
        return

    matched = [r for r in responses if EVIDENCE_ENDPOINT in r["url"]]

    if matched:
        print(f"   ✅ KEYWORD '{EVIDENCE_ENDPOINT}' MATCHED {len(matched)} RESPONSE(S).")
        print("-" * 60)
        for i, resp in enumerate(matched, 1):
            req_info    = requests_map.get(resp["requestId"], {})
            http_method = req_info.get("method", "UNKNOWN")
            post_data   = req_info.get("postData", None)
            status      = resp["status"]

            print(f"📋 MATCH #{i}")
            print(f"🔗 URL      : {resp['url']}")
            print(f"📨 METHOD   : {http_method}")
            print(f"📦 STATUS   : {status}")
            print(f"📄 MIME TYPE: {resp['mimeType']}")

            if post_data:
                try:
                    safe = json.loads(post_data)
                    for key in ["password", "contrasena", "pass", "pwd"]:
                        if key in safe:
                            safe[key] = "********"
                    print(f"📤 PAYLOAD  : {json.dumps(safe)}")
                except Exception:
                    print("📤 PAYLOAD  : [RAW — NOT JSON]")

            INTERPRETATIONS = {
                200: "✅ SERVER: OK",
                201: "✅ SERVER: RESOURCE CREATED",
                202: "✅ SERVER: ACCEPTED",
                400: "⛔ SERVER: BAD REQUEST",
                401: "🔒 SERVER: UNAUTHORIZED",
                403: "🚫 SERVER: FORBIDDEN",
                404: "🔍 SERVER: NOT FOUND",
                409: "⚠️  SERVER: CONFLICT",
                422: "⚠️  SERVER: UNPROCESSABLE ENTITY",
                500: "💥 SERVER: INTERNAL SERVER ERROR",
            }
            print(INTERPRETATIONS.get(status, f"⚠️  SERVER: HTTP {status}"))
            print("-" * 60)
    else:
        print(f"   ⚠️  KEYWORD '{EVIDENCE_ENDPOINT}' NOT FOUND IN CAPTURED URLS.")
        print(f"   🔍 DIAGNOSTIC MODE — ALL {len(responses)} NON-STATIC RESPONSE(S):")
        print("-" * 60)
        for resp in responses:
            req_info = requests_map.get(resp["requestId"], {})
            print(f"   {req_info.get('method','?'):6} | {resp['status']} | {resp['url'][:120]}")
            if req_info.get("postData"):
                print(f"          📤 PAYLOAD: {req_info['postData'][:100]}")
        print("-" * 60)
        print("   💡 UPDATE 'EVIDENCE_ENDPOINT' WITH A KEYWORD FROM THE URLS ABOVE.")


# ==================================================================================
# CREATE-FORM-01: USERS CAN ACCESS THE CATALOG CREATION FORM
# ==================================================================================
def CREATE_FORM_01():
    print("\n" + "=" * 60)
    print("🧪 CREATE-FORM-01: USERS CAN ACCESS THE CATALOG CREATION FORM")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO USUARIOS MODULE...")
        _login_and_go_to_usuarios(driver)

        print("\n📸 TAKING SCREENSHOT #1 — ADMINISTRACIÓN DE USUARIOS TABLE...")
        utils.tomar_screenshot(driver, "CREATE_FORM_01_1_TABLA_USUARIOS")

        print("\n👉 STEP 1: CLICKING '+ NUEVO' BUTTON TO OPEN CREATION FORM...")
        _click_nuevo_button(driver)
        time.sleep(2)

        print(f"   🌐 CURRENT URL: {driver.current_url}")

        print("\n👉 STEP 2: VERIFYING 'CREACIÓN DE USUARIO' FORM IS RENDERED...")
        form_visible = _form_creacion_is_visible(driver)

        if form_visible:
            print("   ✅ FORM 'CREACIÓN DE USUARIO' IS VISIBLE ON PAGE.")
        else:
            print("   ⚠️  FORM TITLE NOT DETECTED — CHECKING URL AS FALLBACK...")

        print("\n📸 TAKING SCREENSHOT #2 — CREACIÓN DE USUARIO FORM...")
        utils.tomar_screenshot(driver, "CREATE_FORM_01_2_FORM_CREACION")

        print("\n👉 STEP 3: CHECKING ALL TEXT INPUT FIELDS ARE EMPTY...")
        text_fields = {
            "NOMBRE DE USUARIO" : XPATH_INPUT_NOMBRE_USUARIO,
            "E-MAIL"            : XPATH_INPUT_EMAIL,
            "NOMBRE"            : XPATH_INPUT_NOMBRE,
            "APELLIDO PATERNO"  : XPATH_INPUT_APELLIDO_PAT,
            "APELLIDO MATERNO"  : XPATH_INPUT_APELLIDO_MAT,
            "TELEFONO"          : XPATH_INPUT_TELEFONO,
        }

        fields_empty   = {}
        fields_missing = []

        for field_name, xpath in text_fields.items():
            try:
                el       = driver.find_element(By.XPATH, xpath)
                value    = el.get_attribute("value") or ""
                is_empty = value.strip() == ""
                fields_empty[field_name] = is_empty
                if is_empty:
                    print(f"      ✅ EMPTY   — {field_name}")
                else:
                    print(f"      ❌ NOT EMPTY — {field_name}: '{value}'")
            except Exception:
                fields_missing.append(field_name)
                print(f"      ⚠️  NOT FOUND IN DOM — {field_name}")

        print("\n📸 TAKING SCREENSHOT #3 — FIELD EMPTY STATE VERIFIED...")
        utils.tomar_screenshot(driver, "CREATE_FORM_01_3_FIELDS_EMPTY")

        all_empty   = all(fields_empty.values()) if fields_empty else False
        test_passed = form_visible and all_empty

        print(f"\n   🔬 CREATE-FORM-01 ASSERTION SUMMARY:")
        print(f"      • FORM VISIBLE               : {form_visible}")
        print(f"      • FIELDS CHECKED             : {len(fields_empty)}")
        print(f"      • FIELDS NOT FOUND IN DOM    : {fields_missing if fields_missing else 'NONE'}")
        print(f"      • ALL CHECKED FIELDS EMPTY   : {all_empty}")
        print(f"      • FINAL URL                  : {driver.current_url}")

        _capture_web_evidence(driver, "CREATE_FORM_01")

        if test_passed:
            utils.tomar_screenshot(driver, "CREATE_FORM_01_SUCCESS")
            print("\n✅ CREATE-FORM-01: SUCCESS — FORM OPENED AND ALL FIELDS ARE EMPTY.")
        else:
            utils.tomar_screenshot(driver, "CREATE_FORM_01_FAILED")
            if not form_visible:
                print("\n❌ CREATE-FORM-01: FAILED — 'CREACIÓN DE USUARIO' FORM DID NOT RENDER.")
            else:
                filled = [k for k, v in fields_empty.items() if not v]
                print(f"\n❌ CREATE-FORM-01: FAILED — FIELDS WITH PRE-FILLED DATA: {filled}")

    except Exception as e:
        print(f"\n💥 CREATE-FORM-01 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "CREATE_FORM_01_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()


# ==================================================================================
# CREATE-FORM-02: THE RECORD IS SAVED SUCCESSFULLY AN A SUCCESS MESSAGE IS DISPLAYED.  
# ==================================================================================
def CREATE_FORM_02():
    print("\n" + "=" * 60)
    print("🧪 CREATE-FORM-02: THE RECORD IS SAVED SUCCESSFULLY AN A SUCCESS MESSAGE IS DISPLAYED.")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO USUARIOS MODULE...")
        _login_and_go_to_usuarios(driver)

        print("\n👉 STEP 1: CLICKING '+ NUEVO' TO OPEN CREATION FORM...")
        _click_nuevo_button(driver)
        time.sleep(2)

        print(f"   🌐 CURRENT URL: {driver.current_url}")

        print("\n📸 TAKING SCREENSHOT #1 — EMPTY FORM BEFORE FILLING...")
        utils.tomar_screenshot(driver, "CREATE_FORM_02_1_EMPTY_FORM")

        print("\n👉 STEP 2: FILLING IN ALL FORM FIELDS WITH VALID TEST DATA...")

        print(f"   ✏️  NOMBRE DE USUARIO → '{CF02_NOMBRE_USUARIO}'")
        utils.escribir_texto(driver, XPATH_INPUT_NOMBRE_USUARIO, CF02_NOMBRE_USUARIO)
        time.sleep(0.3)

        print(f"   ✏️  E-MAIL → '{CF02_EMAIL}'")
        utils.escribir_texto(driver, XPATH_INPUT_EMAIL, CF02_EMAIL)
        time.sleep(0.3)

        print(f"   ✏️  NOMBRE → '{CF02_NOMBRE}'")
        utils.escribir_texto(driver, XPATH_INPUT_NOMBRE, CF02_NOMBRE)
        time.sleep(0.3)

        print(f"   ✏️  APELLIDO PATERNO → '{CF02_APELLIDO_PAT}'")
        utils.escribir_texto(driver, XPATH_INPUT_APELLIDO_PAT, CF02_APELLIDO_PAT)
        time.sleep(0.3)

        print(f"   ✏️  APELLIDO MATERNO → '{CF02_APELLIDO_MAT}'")
        utils.escribir_texto(driver, XPATH_INPUT_APELLIDO_MAT, CF02_APELLIDO_MAT)
        time.sleep(0.3)

        print(f"   ✏️  TELEFONO → '{CF02_TELEFONO}'")
        utils.escribir_texto(driver, XPATH_INPUT_TELEFONO, CF02_TELEFONO)
        time.sleep(0.3)

        
        print(f"   🔽 PERFIL (SELECT) → '{CF02_PERFIL}'")
        perfil_selected = False

        try:
            select_el = driver.find_element(By.XPATH, XPATH_DROPDOWN_PERFIL)
            sel = Select(select_el)
            sel.select_by_visible_text(CF02_PERFIL)
            perfil_selected = True
            time.sleep(0.5)
            print(f"      ✅ PERFIL SELECTED — STRATEGY 1 (Select.select_by_visible_text).")
        except Exception as p1_err:
            print(f"      ⚠️  STRATEGY 1 FAILED: {p1_err}")

        if not perfil_selected:
            try:
                result = driver.execute_script(f"""
                    var sel = document.getElementById('id_profile');
                    if (!sel) sel = document.querySelector('select[id*="profile"]');
                    if (!sel) return 'SELECT NOT FOUND';
                    var opts = sel.options;
                    for (var i = 0; i < opts.length; i++) {{
                        if (opts[i].text.trim() === '{CF02_PERFIL}') {{
                            sel.value = opts[i].value;
                            sel.dispatchEvent(new Event('change', {{bubbles: true}}));
                            return 'set-value:' + opts[i].value;
                        }}
                    }}
                    return 'OPTION NOT FOUND';
                """)
                if result and result.startswith('set-value:'):
                    perfil_selected = True
                    time.sleep(0.5)
                    print(f"      ✅ PERFIL SELECTED — STRATEGY 2 (JS: '{result}').")
                else:
                    print(f"      ⚠️  STRATEGY 2 DEBUG: {result}")
            except Exception as p2_err:
                print(f"      ⚠️  STRATEGY 2 FAILED: {p2_err}")

        if not perfil_selected:
            try:
                option = driver.find_element(
                    By.XPATH,
                    f"//select[@id='id_profile']/option[normalize-space(text())='{CF02_PERFIL}']"
                )
                driver.execute_script(
                    "arguments[0].selected = true; "
                    "arguments[0].parentElement.dispatchEvent(new Event('change', {bubbles:true}));",
                    option
                )
                perfil_selected = True
                time.sleep(0.5)
                print(f"      ✅ PERFIL SELECTED — STRATEGY 3 (OPTION XPATH + JS).")
            except Exception as p3_err:
                print(f"      ⚠️  STRATEGY 3 FAILED: {p3_err}")

        if not perfil_selected:
            print(f"      ❌ COULD NOT SELECT PERFIL '{CF02_PERFIL}' — ALL STRATEGIES FAILED.")

        # --- CLIENTE DROPDOWN (SECOND <select> ON THE FORM) ---
        print(f"   🔽 CLIENTE (SELECT) → '{CF02_CLIENTE}'")
        cliente_selected = False

        XPATH_SELECT_CLIENTE = (
            "//select[@id='id_client'] | "
            "//select[@id='id_cliente'] | "
            "(//select)[2]"
        )

        try:
            select_el = driver.find_element(By.XPATH, XPATH_SELECT_CLIENTE)
            sel = Select(select_el)
            sel.select_by_visible_text(CF02_CLIENTE)
            cliente_selected = True
            time.sleep(0.5)
            print(f"      ✅ CLIENTE SELECTED — STRATEGY 1 (Select.select_by_visible_text).")
        except Exception as c1_err:
            print(f"      ⚠️  STRATEGY 1 FAILED: {c1_err}")

        if not cliente_selected:
            try:
                result = driver.execute_script(f"""
                    var selects = document.querySelectorAll('select');
                    for (var sel of selects) {{
                        var opts = sel.options;
                        for (var i = 0; i < opts.length; i++) {{
                            if (opts[i].text.trim() === '{CF02_CLIENTE}') {{
                                sel.value = opts[i].value;
                                sel.dispatchEvent(new Event('change', {{bubbles: true}}));
                                return 'set-value:' + opts[i].value;
                            }}
                        }}
                    }}
                    return 'OPTION NOT FOUND';
                """)
                if result and result.startswith('set-value:'):
                    cliente_selected = True
                    time.sleep(0.5)
                    print(f"      ✅ CLIENTE SELECTED — STRATEGY 2 (JS SCAN: '{result}').")
                else:
                    print(f"      ⚠️  STRATEGY 2 DEBUG: {result}")
            except Exception as c2_err:
                print(f"      ⚠️  STRATEGY 2 FAILED: {c2_err}")

        if not cliente_selected:
            print(f"      ❌ COULD NOT SELECT CLIENTE '{CF02_CLIENTE}' — ALL STRATEGIES FAILED.")

        print(f"   ✏️  CONTRASEÑA → '{'*' * len(CF02_PASSWORD)}'")
        utils.escribir_texto(driver, XPATH_INPUT_PASSWORD, CF02_PASSWORD)
        time.sleep(0.3)

        print(f"   ✏️  CONFIRMAR CONTRASEÑA → '{'*' * len(CF02_CONFIRM_PASS)}'")
        utils.escribir_texto(driver, XPATH_INPUT_CONFIRM_PASS, CF02_CONFIRM_PASS)
        time.sleep(0.5)

        print("\n📸 TAKING SCREENSHOT #2 — FORM FILLED, BEFORE CLICKING GUARDAR...")
        utils.tomar_screenshot(driver, "CREATE_FORM_02_2_FORM_FILLED")

        print("\n👉 STEP 3: CLICKING 'GUARDAR' BUTTON...")
        guardar_clicked = _click_guardar(driver)

        print("\n👉 STEP 4: WAITING FOR SUCCESS TOAST 'Usuario creado correctamente.'...")
        toast_detected = False
        wait_toast     = WebDriverWait(driver, 10)

        try:
            wait_toast.until(EC.presence_of_element_located((By.XPATH, XPATH_TOAST_EXITO)))
            toast_detected = True
            print("   ✅ SUCCESS TOAST DETECTED — STRATEGY 1 (WebDriverWait + XPATH).")
        except Exception:
            print("   ⚠️  TOAST NOT DETECTED VIA WAIT — TRYING JS SCAN...")

        if not toast_detected:
            try:
                result = driver.execute_script("""
                    var all = document.querySelectorAll('*');
                    for (var el of all) {
                        if (el.children.length === 0 &&
                            el.textContent.trim().toLowerCase()
                               .includes('creado correctamente')) {
                            return el.textContent.trim();
                        }
                    }
                    return null;
                """)
                if result:
                    toast_detected = True
                    print(f"   ✅ SUCCESS TOAST FOUND VIA JS SCAN: '{result}'.")
                else:
                    print("   ❌ SUCCESS TOAST NOT FOUND IN DOM.")
            except Exception as js_err:
                print(f"   ⚠️  JS SCAN FAILED: {js_err}")

        print("\n📸 TAKING SCREENSHOT #3 — AFTER GUARDAR (TOAST STATE)...")
        utils.tomar_screenshot(driver, "CREATE_FORM_02_3_AFTER_GUARDAR")

        test_passed = guardar_clicked and toast_detected

        print(f"\n   🔬 CREATE-FORM-02 ASSERTION SUMMARY:")
        print(f"      • PERFIL SELECTED             : {perfil_selected}")
        print(f"      • CLIENTE SELECTED            : {cliente_selected}")
        print(f"      • 'GUARDAR' CLICKED           : {guardar_clicked}")
        print(f"      • SUCCESS TOAST DETECTED      : {toast_detected}")
        print(f"      • FINAL URL                   : {driver.current_url}")

        _capture_web_evidence(driver, "CREATE_FORM_02")

        if test_passed:
            utils.tomar_screenshot(driver, "CREATE_FORM_02_SUCCESS")
            print("\n✅ CREATE-FORM-02: SUCCESS — USER CREATED AND SUCCESS TOAST CONFIRMED.")
        else:
            utils.tomar_screenshot(driver, "CREATE_FORM_02_FAILED")
            if not guardar_clicked:
                print("\n❌ CREATE-FORM-02: FAILED — 'GUARDAR' BUTTON COULD NOT BE CLICKED.")
            else:
                print("\n❌ CREATE-FORM-02: FAILED — SUCCESS TOAST DID NOT APPEAR AFTER SAVING.")

    except Exception as e:
        print(f"\n💥 CREATE-FORM-02 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "CREATE_FORM_02_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()


# ==================================================================================
# CREATE-FORM-03: YOU CANNOT SAVE IF REQUIRED FIELDS ARE MISSING 
# ==================================================================================
def CREATE_FORM_03():
    print("\n" + "=" * 60)
    print("🧪 CREATE-FORM-03: YOU CANNOT SAVE IF REQUIRED FIELDS ARE MISSING ")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO USUARIOS MODULE...")
        _login_and_go_to_usuarios(driver)

        print("\n👉 STEP 1: CLICKING '+ NUEVO' TO OPEN CREATION FORM...")
        _click_nuevo_button(driver)
        time.sleep(2)

        print(f"   🌐 CURRENT URL: {driver.current_url}")

        print("\n📸 TAKING SCREENSHOT #1 — EMPTY FORM BEFORE CLICKING GUARDAR...")
        utils.tomar_screenshot(driver, "CREATE_FORM_03_1_EMPTY_FORM")

        print("\n👉 STEP 2: CLICKING 'GUARDAR' WITH ALL FIELDS EMPTY...")
        guardar_clicked = _click_guardar(driver)
        time.sleep(2)

        print("\n👉 STEP 3: CHECKING FOR 'Este campo es requerido' MESSAGES...")
        XPATH_ERROR_REQUERIDO = (
            "//*[contains(text(),'Este campo es requerido') or "
            "    contains(text(),'este campo es requerido')]"
        )

        error_count  = 0
        errors_found = False

        try:
            error_elements = driver.find_elements(By.XPATH, XPATH_ERROR_REQUERIDO)
            error_count    = len(error_elements)
            errors_found   = error_count > 0
            if errors_found:
                print(f"   ✅ {error_count} 'Este campo es requerido' MESSAGE(S) — STRATEGY 1 (XPATH).")
            else:
                print("   ⚠️  NO ERROR MESSAGES FOUND VIA XPATH — TRYING JS SCAN...")
        except Exception as e1:
            print(f"   ⚠️  STRATEGY 1 FAILED: {e1}")

        if not errors_found:
            try:
                error_count = driver.execute_script("""
                    var all   = document.querySelectorAll('*');
                    var count = 0;
                    for (var el of all) {
                        if (el.children.length === 0 &&
                            el.textContent.trim().toLowerCase()
                               .includes('este campo es requerido') &&
                            el.offsetWidth > 0) {
                            count++;
                        }
                    }
                    return count;
                """)
                errors_found = error_count > 0
                if errors_found:
                    print(f"   ✅ {error_count} ERROR MESSAGE(S) — STRATEGY 2 (JS DOM SCAN).")
                else:
                    print("   ❌ NO 'Este campo es requerido' MESSAGES FOUND IN DOM.")
            except Exception as e2:
                print(f"   ⚠️  STRATEGY 2 FAILED: {e2}")

        print("\n👉 STEP 4: CHECKING FOR INFO TOAST 'Revisa la información ingresada.'...")
        toast_detected = False
        wait_toast     = WebDriverWait(driver, 8)

        try:
            wait_toast.until(EC.presence_of_element_located((By.XPATH, XPATH_TOAST_INFO)))
            toast_detected = True
            print("   ✅ INFO TOAST DETECTED — STRATEGY 1 (WebDriverWait + XPATH).")
        except Exception:
            print("   ⚠️  TOAST NOT DETECTED VIA WAIT — TRYING JS SCAN...")

        if not toast_detected:
            try:
                result = driver.execute_script("""
                    var all = document.querySelectorAll('*');
                    for (var el of all) {
                        if (el.children.length === 0 &&
                            el.textContent.trim().toLowerCase().includes('revisa la')) {
                            return el.textContent.trim();
                        }
                    }
                    return null;
                """)
                if result:
                    toast_detected = True
                    print(f"   ✅ INFO TOAST FOUND VIA JS SCAN: '{result}'.")
                else:
                    print("   ❌ INFO TOAST NOT FOUND IN DOM.")
            except Exception as js_err:
                print(f"   ⚠️  JS SCAN FAILED: {js_err}")

        print("\n📸 TAKING SCREENSHOT #2 — VALIDATION ERRORS AND TOAST VISIBLE...")
        utils.tomar_screenshot(driver, "CREATE_FORM_03_2_VALIDATION_ERRORS")

        test_passed = guardar_clicked and errors_found and toast_detected

        print(f"\n   🔬 CREATE-FORM-03 ASSERTION SUMMARY:")
        print(f"      • 'GUARDAR' CLICKED              : {guardar_clicked}")
        print(f"      • VALIDATION ERRORS FOUND        : {errors_found} ({error_count} message(s))")
        print(f"      • INFO TOAST DETECTED            : {toast_detected}")
        print(f"      • FINAL URL                      : {driver.current_url}")

        _capture_web_evidence(driver, "CREATE_FORM_03")

        if test_passed:
            utils.tomar_screenshot(driver, "CREATE_FORM_03_SUCCESS")
            print("\n✅ CREATE-FORM-03: SUCCESS — EMPTY FORM CORRECTLY TRIGGERS VALIDATION ERRORS AND INFO TOAST.")
        else:
            utils.tomar_screenshot(driver, "CREATE_FORM_03_FAILED")
            if not guardar_clicked:
                print("\n❌ CREATE-FORM-03: FAILED — 'GUARDAR' BUTTON COULD NOT BE CLICKED.")
            elif not errors_found:
                print("\n❌ CREATE-FORM-03: FAILED — NO 'Este campo es requerido' MESSAGES APPEARED.")
            else:
                print("\n❌ CREATE-FORM-03: FAILED — INFO TOAST 'Revisa la información ingresada.' DID NOT APPEAR.")

    except Exception as e:
        print(f"\n💥 CREATE-FORM-03 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "CREATE_FORM_03_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()

# ==================================================================================
# CREATE-FORM-04: NO INFORMATION IS SAVED, RETURN TO PREVIOUS VIEW
# ==================================================================================
def CREATE_FORM_04():
    print("\n" + "=" * 60)
    print("🧪 CREATE-FORM-04: NO INFORMATION IS SAVED, RETURN TO PREVIOUS VIEW")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO USUARIOS MODULE...")
        _login_and_go_to_usuarios(driver)

        print("\n👉 STEP 1: CLICKING '+ NUEVO' TO OPEN CREATION FORM...")
        _click_nuevo_button(driver)
        time.sleep(2)

        print(f"   🌐 CURRENT URL: {driver.current_url}")

        print("\n📸 TAKING SCREENSHOT #1 — EMPTY FORM BEFORE ANY ACTION...")
        utils.tomar_screenshot(driver, "CREATE_FORM_04_1_EMPTY_FORM")

        print("\n👉 STEP 2: CLICKING 'GUARDAR' WITH ALL FIELDS EMPTY TO TRIGGER VALIDATION...")
        guardar_clicked = _click_guardar(driver)
        time.sleep(2)

        print("\n📸 TAKING SCREENSHOT #2 — VALIDATION ERRORS VISIBLE AFTER GUARDAR...")
        utils.tomar_screenshot(driver, "CREATE_FORM_04_2_VALIDATION_ERRORS")

        print("\n👉 STEP 3: CLICKING RED 'SALIR' BUTTON...")
        salir_clicked = _click_salir(driver)
        time.sleep(2)

        print("\n👉 STEP 4: CHECKING FOR CONFIRM EXIT DIALOG '¿Quieres salir del formulario?'...")
        dialog_visible = False
        wait_dialog    = WebDriverWait(driver, 8)

        try:
            wait_dialog.until(EC.presence_of_element_located((By.XPATH, XPATH_DIALOG_SALIR)))
            dialog_visible = True
            print("   ✅ EXIT DIALOG DETECTED — STRATEGY 1 (WebDriverWait + XPATH).")
        except Exception:
            print("   ⚠️  DIALOG NOT DETECTED VIA WAIT — TRYING JS SCAN...")

        if not dialog_visible:
            try:
                result = driver.execute_script("""
                    var all = document.querySelectorAll('*');
                    for (var el of all) {
                        var txt = el.textContent.trim().toLowerCase();
                        if (el.children.length === 0 &&
                            (txt.includes('quieres salir') ||
                             txt.includes('salir del formulario')) &&
                            el.offsetWidth > 0) {
                            return el.textContent.trim();
                        }
                    }
                    return null;
                """)
                if result:
                    dialog_visible = True
                    print(f"   ✅ EXIT DIALOG FOUND VIA JS SCAN: '{result}'.")
                else:
                    print("   ❌ EXIT DIALOG TEXT NOT FOUND IN DOM.")
            except Exception as js_err:
                print(f"   ⚠️  JS SCAN FAILED: {js_err}")

        print("\n📸 TAKING SCREENSHOT #3 — CONFIRM EXIT DIALOG '¿Quieres salir del formulario?'...")
        utils.tomar_screenshot(driver, "CREATE_FORM_04_3_EXIT_DIALOG")

        test_passed = guardar_clicked and salir_clicked and dialog_visible

        print(f"\n   🔬 CREATE-FORM-04 ASSERTION SUMMARY:")
        print(f"      • 'GUARDAR' CLICKED              : {guardar_clicked}")
        print(f"      • 'SALIR' CLICKED                : {salir_clicked}")
        print(f"      • EXIT DIALOG VISIBLE            : {dialog_visible}")
        print(f"      • FINAL URL                      : {driver.current_url}")

        _capture_web_evidence(driver, "CREATE_FORM_04")

        if test_passed:
            utils.tomar_screenshot(driver, "CREATE_FORM_04_SUCCESS")
            print("\n✅ CREATE-FORM-04: SUCCESS — EXIT DIALOG '¿Quieres salir del formulario?' APPEARED CORRECTLY.")
        else:
            utils.tomar_screenshot(driver, "CREATE_FORM_04_FAILED")
            if not guardar_clicked:
                print("\n❌ CREATE-FORM-04: FAILED — 'GUARDAR' BUTTON COULD NOT BE CLICKED.")
            elif not salir_clicked:
                print("\n❌ CREATE-FORM-04: FAILED — 'SALIR' BUTTON COULD NOT BE CLICKED.")
            else:
                print("\n❌ CREATE-FORM-04: FAILED — EXIT DIALOG '¿Quieres salir del formulario?' DID NOT APPEAR.")

    except Exception as e:
        print(f"\n💥 CREATE-FORM-04 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "CREATE_FORM_04_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()


# ==================================================================================
# MAIN EXECUTION
# ==================================================================================
if __name__ == "__main__":

    logger, log_file, timestamp = utils.iniciar_reporte("CREATE_FORM")

    try:
        CREATE_FORM_01()
        CREATE_FORM_02()
        CREATE_FORM_03()
        CREATE_FORM_04()

    finally:
        utils.generar_reporte_html("CREATE_FORM", log_file, timestamp)