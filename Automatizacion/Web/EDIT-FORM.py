"""
# ==================================================================================
# FILENAME    : EDIT-FORM.py
# PROJECT     : MEMPHIS QA AUTOMATION FRAMEWORK
# CONTENTS:
#   · EDIT-FORM-01: FORM IS DISPLAYED IN EDIT MODE 
#   · EDIT-FORM-02: FORM IN EDIT MODE. 
# ==================================================================================
"""

import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import config
import utils
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


# MODULE CONFIGURATION
USUARIOS_URL  = "https://fat.memphis.mx/v2/usuarios"
EVIDENCE_ENDPOINT = "usuarios"


# TEST DATA — EDIT-FORM-02: FIELD MODIFICATIONS
EF02_NOMBRE_NUEVO          = "Modificacion"   
EF02_APELLIDO_PAT_NUEVO    = "Modificaciones"  


XPATH_TOAST_UPDATE_EXITO = (
    "//*[contains(text(),'Usuario actualizado correctamente') or "
    "    contains(text(),'usuario actualizado correctamente')] | "
    "//div[contains(@class,'p-toast')]"
    "//*[contains(text(),'actualizado correctamente')]"
)

XPATH_USUARIOS_CARD = (
    
    "[routerLink='/usuarios'], [routerlink='/usuarios'], "
    "[ng-reflect-router-link='/usuarios']"
)


XPATH_BTN_PENCIL_FIRST_ROW = (
    
    "(//tbody//button[.//*[contains(@class,'pencil') or contains(@class,'edit') or "
    "                      contains(@class,'pi-pencil') or contains(@class,'pi-pen') or "
    "                      contains(@name,'edit') or contains(@name,'pencil')]])[1] | "
    # FALLBACK A: FIRST ANCHOR/BUTTON IN THE ACCIONES COLUMN (FIRST CELL OF FIRST ROW)
    "(//tbody//tr[1]//button)[1] | "
    # FALLBACK B: FIRST EDIT ICON ANYWHERE IN THE TABLE
    "(//table//button[.//*[contains(@class,'edit') or contains(@class,'pencil')]])[1]"
)


XPATH_EDIT_FORM_TITULO = (
    "//*[contains(text(),'Edición de Usuario') or "
    "    contains(text(),'EDICIÓN DE USUARIO') or "
    "    contains(text(),'Edicion de Usuario')]"
    "[not(ancestor::nav) and not(ancestor::aside)]"
)


XPATH_EDIT_INPUT_NOMBRE_USUARIO = "//input[@placeholder='Nombre de Usuario' or @formcontrolname='username']"
XPATH_EDIT_INPUT_EMAIL          = "//input[@placeholder='correo@mail.com' or @type='email']"
XPATH_EDIT_INPUT_NOMBRE         = "//input[@placeholder='Nombre' or @formcontrolname='nombre']"
XPATH_EDIT_INPUT_APELLIDO_PAT   = "//input[@placeholder='Apellido Paterno' or @formcontrolname='apellidoPaterno']"
XPATH_EDIT_INPUT_APELLIDO_MAT   = "//input[@placeholder='Apellido Materno' or @formcontrolname='apellidoMaterno']"
XPATH_EDIT_INPUT_TELEFONO       = "//input[@placeholder='Teléfono' or @formcontrolname='telefono']"


XPATH_BTN_GUARDAR = (
    "//button[contains(translate(.,'GUARDAR','guardar'),'guardar')] | "
    "//button[contains(text(),'Guardar') or contains(text(),'GUARDAR')]"
)

XPATH_TABLA_USUARIOS = (
    "//*[contains(text(),'Administración de Usuarios') or "
    "    contains(text(),'Administracion de Usuarios')]"
    "[not(ancestor::nav)]"
)


# ==================================================================================
# INTERNAL HELPERS
# ==================================================================================

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

    # STRATEGY 4: DIRECT URL NAVIGATION (FINAL FALLBACK)
    if not clicked:
        print(f"   ⚠️  ALL CLICK STRATEGIES FAILED. NAVIGATING DIRECTLY TO URL...")
        driver.get(USUARIOS_URL)
        time.sleep(4)
        print(f"   🌐 NAVIGATED DIRECTLY TO: {driver.current_url}")
    else:
        print(f"   🌐 CURRENT URL AFTER CARD CLICK: {driver.current_url}")

    print("   ⏳ WAITING FOR 'ADMINISTRACIÓN DE USUARIOS' TABLE TO RENDER...")
    time.sleep(3)


def _click_pencil_first_row(driver):
    
    print("   🖱️  CLICKING PENCIL ✏️ ON FIRST ROW (3-STRATEGY CASCADE)...")

    try:
        btn = driver.find_element(By.XPATH, "(//tbody//tr[1]//button)[1]")
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(3)
        print("   ✅ PENCIL CLICKED — STRATEGY 1 (FIRST BUTTON IN FIRST TR).")
        return True
    except Exception as s1_err:
        print(f"   ⚠️  STRATEGY 1 FAILED: {s1_err}")

    # STRATEGY 2: XPATH — ANY ELEMENT WITH PENCIL/EDIT ICON CLASS IN FIRST ROW
    try:
        btn = driver.find_element(By.XPATH, XPATH_BTN_PENCIL_FIRST_ROW)
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(3)
        print("   ✅ PENCIL CLICKED — STRATEGY 2 (PENCIL ICON XPATH).")
        return True
    except Exception as s2_err:
        print(f"   ⚠️  STRATEGY 2 FAILED: {s2_err}")

    # STRATEGY 3: JS — FIND THE FIRST CLICKABLE BUTTON IN THE TABLE AND CLICK IT
    try:
        result = driver.execute_script("""
            // FIND THE FIRST <tr> IN <tbody> AND CLICK ITS FIRST BUTTON
            var rows = document.querySelectorAll('tbody tr');
            if (rows.length === 0) return 'NO ROWS FOUND';
            var firstRow = rows[0];
            var btns = firstRow.querySelectorAll('button, a[role="button"]');
            if (btns.length === 0) return 'NO BUTTONS IN FIRST ROW';
            btns[0].click();
            return 'clicked:' + btns[0].className;
        """)
        if result and result.startswith('clicked:'):
            time.sleep(3)
            print(f"   ✅ PENCIL CLICKED — STRATEGY 3 (JS FIRST ROW BUTTON: '{result}').")
            return True
        else:
            print(f"   ❌ STRATEGY 3 — DEBUG: {result}")
    except Exception as s3_err:
        print(f"   ⚠️  STRATEGY 3 FAILED: {s3_err}")

    return False


def _edit_form_is_visible(driver):
    try:
        driver.find_element(By.XPATH, XPATH_EDIT_FORM_TITULO)
        return True
    except Exception:
        return "editar" in driver.current_url.lower()


def _capture_web_evidence(driver, nombre_test):
    try:
        utils.print_http_evidence(driver, EVIDENCE_ENDPOINT)
    except Exception as ev_err:
        print(f"   ⚠️  HTTP EVIDENCE CAPTURE FAILED FOR [{nombre_test}]: {ev_err}")


# ==================================================================================
# EDIT-FORM-01:FORM IS DISPLAYED IN EDIT MODE 
# ==================================================================================
def EDIT_FORM_01():
    print("\n" + "=" * 60)
    print("🧪 EDIT-FORM-01: FORM IS DISPLAYED IN EDIT MODE ")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO USUARIOS MODULE...")
        _login_and_go_to_usuarios(driver)

        print("\n📸 TAKING SCREENSHOT #1 — ADMINISTRACIÓN DE USUARIOS TABLE...")
        utils.tomar_screenshot(driver, "EDIT_FORM_01_1_TABLA_USUARIOS")

        print("\n👉 STEP 1: CLICKING PENCIL ✏️ ICON ON FIRST ROW...")
        pencil_clicked = _click_pencil_first_row(driver)

        print(f"   🌐 CURRENT URL AFTER PENCIL CLICK: {driver.current_url}")

        print("\n📸 TAKING SCREENSHOT #2 — AFTER CLICKING PENCIL...")
        utils.tomar_screenshot(driver, "EDIT_FORM_01_2_AFTER_PENCIL")

        print("\n👉 STEP 2: VERIFYING 'EDICIÓN DE USUARIO' FORM IS RENDERED...")
        time.sleep(2)
        form_visible = _edit_form_is_visible(driver)

        if form_visible:
            print("   ✅ EDIT FORM 'EDICIÓN DE USUARIO' IS VISIBLE ON PAGE.")
        else:
            print("   ⚠️  EDIT FORM TITLE NOT DETECTED — CHECKING URL AS FALLBACK...")

        print("\n👉 STEP 3: VERIFYING FORM FIELDS ARE PRE-FILLED WITH EXISTING DATA...")

        text_fields = {
            "NOMBRE DE USUARIO" : XPATH_EDIT_INPUT_NOMBRE_USUARIO,
            "E-MAIL"            : XPATH_EDIT_INPUT_EMAIL,
            "NOMBRE"            : XPATH_EDIT_INPUT_NOMBRE,
            "APELLIDO PATERNO"  : XPATH_EDIT_INPUT_APELLIDO_PAT,
            "APELLIDO MATERNO"  : XPATH_EDIT_INPUT_APELLIDO_MAT,
            "TELEFONO"          : XPATH_EDIT_INPUT_TELEFONO,
        }

        fields_prefilled = {}
        fields_missing   = []

        for field_name, xpath in text_fields.items():
            try:
                el    = driver.find_element(By.XPATH, xpath)
                value = el.get_attribute("value") or ""
                is_filled = value.strip() != ""
                fields_prefilled[field_name] = is_filled

                if is_filled:
                    print(f"      ✅ PRE-FILLED — {field_name}: '{value}'")
                else:
                    print(f"      ⚠️  EMPTY     — {field_name}")

            except Exception:
                fields_missing.append(field_name)
                print(f"      ⚠️  NOT FOUND IN DOM — {field_name}")

        print("\n📸 TAKING SCREENSHOT #3 — EDIT FORM WITH PRE-FILLED DATA...")
        utils.tomar_screenshot(driver, "EDIT_FORM_01_3_PREFILLED_FORM")

        any_prefilled = any(fields_prefilled.values()) if fields_prefilled else False
        test_passed   = pencil_clicked and form_visible and any_prefilled

        print(f"\n   🔬 EDIT-FORM-01 ASSERTION SUMMARY:")
        print(f"      • PENCIL CLICKED              : {pencil_clicked}")
        print(f"      • EDIT FORM VISIBLE           : {form_visible}")
        print(f"      • FIELDS CHECKED              : {len(fields_prefilled)}")
        print(f"      • FIELDS NOT FOUND IN DOM     : {fields_missing if fields_missing else 'NONE'}")
        print(f"      • AT LEAST ONE FIELD FILLED   : {any_prefilled}")
        print(f"      • FINAL URL                   : {driver.current_url}")

        _capture_web_evidence(driver, "EDIT_FORM_01")

        if test_passed:
            utils.tomar_screenshot(driver, "EDIT_FORM_01_SUCCESS")
            print("\n✅ EDIT-FORM-01: SUCCESS — EDIT FORM OPENED WITH PRE-FILLED USER DATA.")
        else:
            utils.tomar_screenshot(driver, "EDIT_FORM_01_FAILED")
            if not pencil_clicked:
                print("\n❌ EDIT-FORM-01: FAILED — PENCIL ICON COULD NOT BE CLICKED.")
            elif not form_visible:
                print("\n❌ EDIT-FORM-01: FAILED — 'EDICIÓN DE USUARIO' FORM DID NOT RENDER.")
            else:
                print("\n❌ EDIT-FORM-01: FAILED — FORM OPENED BUT ALL FIELDS ARE EMPTY.")

    except Exception as e:
        print(f"\n💥 EDIT-FORM-01 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "EDIT_FORM_01_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()


# ==================================================================================
# EDIT-FORM-02: FORM IN EDIT MODE. 
# ==================================================================================
def EDIT_FORM_02():
    print("\n" + "=" * 60)
    print("🧪 EDIT-FORM-02: FORM IN EDIT MODE. ")
    print("=" * 60)

    driver, wait = utils.iniciar_driver_web()

    try:
        
        print("🔐 PRECONDITION: LOGGING IN AND NAVIGATING TO USUARIOS MODULE...")
        _login_and_go_to_usuarios(driver)

        print("\n📸 TAKING SCREENSHOT #1 — ADMINISTRACIÓN DE USUARIOS TABLE...")
        utils.tomar_screenshot(driver, "EDIT_FORM_02_1_TABLA_USUARIOS")

        
        print("\n👉 STEP 1: CLICKING PENCIL ✏️ ICON ON FIRST ROW...")
        pencil_clicked = _click_pencil_first_row(driver)
        time.sleep(2)

        print(f"   🌐 CURRENT URL: {driver.current_url}")

        print("\n📸 TAKING SCREENSHOT #2 — EDIT FORM OPEN WITH CURRENT DATA...")
        utils.tomar_screenshot(driver, "EDIT_FORM_02_2_EDIT_FORM_OPEN")

        
        print(f"\n👉 STEP 2: MODIFYING 'NOMBRE' FIELD → '{EF02_NOMBRE_NUEVO}'...")
        nombre_modified = False

        try:
            el = driver.find_element(By.XPATH, XPATH_EDIT_INPUT_NOMBRE)
            el.click()
            time.sleep(0.3)
            
            el.send_keys(u"\ue009" + "a")  
            time.sleep(0.2)
            el.send_keys(EF02_NOMBRE_NUEVO)
            new_value = el.get_attribute("value") or ""
            nombre_modified = EF02_NOMBRE_NUEVO in new_value
            print(f"   ✅ NOMBRE MODIFIED — STRATEGY 1 (CTRL+A + TYPE). VALUE: '{new_value}'")
        except Exception as n1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {n1_err}")

        
        if not nombre_modified:
            try:
                driver.execute_script(f"""
                    var el = document.querySelector(
                        'input[placeholder="Nombre"], input[formcontrolname="nombre"]'
                    );
                    if (el) {{
                        el.value = '{EF02_NOMBRE_NUEVO}';
                        el.dispatchEvent(new Event('input', {{bubbles: true}}));
                        el.dispatchEvent(new Event('change', {{bubbles: true}}));
                    }}
                """)
                time.sleep(0.3)
                nombre_modified = True
                print(f"   ✅ NOMBRE MODIFIED — STRATEGY 2 (JS SET VALUE).")
            except Exception as n2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {n2_err}")

        # STEP 3: CLEAR AND FILL 'APELLIDO PATERNO' FIELD WITH NEW VALUE
        print(f"\n👉 STEP 3: MODIFYING 'APELLIDO PATERNO' FIELD → '{EF02_APELLIDO_PAT_NUEVO}'...")
        apellido_modified = False

        try:
            el = driver.find_element(By.XPATH, XPATH_EDIT_INPUT_APELLIDO_PAT)
            el.click()
            time.sleep(0.3)
            el.send_keys(u"\ue009" + "a")   
            time.sleep(0.2)
            el.send_keys(EF02_APELLIDO_PAT_NUEVO)
            new_value = el.get_attribute("value") or ""
            apellido_modified = EF02_APELLIDO_PAT_NUEVO in new_value
            print(f"   ✅ APELLIDO PATERNO MODIFIED — STRATEGY 1 (CTRL+A + TYPE). VALUE: '{new_value}'")
        except Exception as a1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {a1_err}")

        
        if not apellido_modified:
            try:
                driver.execute_script(f"""
                    var el = document.querySelector(
                        'input[placeholder="Apellido Paterno"], input[formcontrolname="apellidoPaterno"]'
                    );
                    if (el) {{
                        el.value = '{EF02_APELLIDO_PAT_NUEVO}';
                        el.dispatchEvent(new Event('input', {{bubbles: true}}));
                        el.dispatchEvent(new Event('change', {{bubbles: true}}));
                    }}
                """)
                time.sleep(0.3)
                apellido_modified = True
                print(f"   ✅ APELLIDO PATERNO MODIFIED — STRATEGY 2 (JS SET VALUE).")
            except Exception as a2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {a2_err}")

        print("\n📸 TAKING SCREENSHOT #3 — FORM WITH MODIFIED VALUES BEFORE GUARDAR...")
        utils.tomar_screenshot(driver, "EDIT_FORM_02_3_FORM_MODIFIED")

        # STEP 4: CLICK 'GUARDAR'
        print("\n👉 STEP 4: CLICKING 'GUARDAR' BUTTON...")
        guardar_clicked = False

        try:
            btn = driver.find_element(By.XPATH, XPATH_BTN_GUARDAR)
            btn.click()
            guardar_clicked = True
            print("   ✅ 'GUARDAR' CLICKED — STRATEGY 1 (XPATH).")
        except Exception as g1_err:
            print(f"   ⚠️  STRATEGY 1 FAILED: {g1_err}")

        if not guardar_clicked:
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
                    guardar_clicked = True
                    print(f"   ✅ 'GUARDAR' CLICKED — STRATEGY 2 (JS: '{result}').")
                else:
                    print("   ❌ 'GUARDAR' BUTTON NOT FOUND ON PAGE.")
            except Exception as g2_err:
                print(f"   ⚠️  STRATEGY 2 FAILED: {g2_err}")

        # STEP 5: WAIT FOR SUCCESS TOAST 'Usuario actualizado correctamente.'
        print("\n👉 STEP 5: WAITING FOR SUCCESS TOAST 'Usuario actualizado correctamente.'...")
        toast_detected = False
        wait_toast     = WebDriverWait(driver, 10)

        # STRATEGY 1
        try:
            wait_toast.until(EC.presence_of_element_located(
                (By.XPATH, XPATH_TOAST_UPDATE_EXITO)
            ))
            toast_detected = True
            print("   ✅ SUCCESS TOAST DETECTED — STRATEGY 1 (WebDriverWait + XPATH).")
        except Exception:
            print("   ⚠️  TOAST NOT DETECTED VIA WAIT — TRYING IMMEDIATE JS SCAN...")

        # STRATEGY 2
        if not toast_detected:
            try:
                result = driver.execute_script("""
                    var all = document.querySelectorAll('*');
                    for (var el of all) {
                        if (el.children.length === 0 &&
                            el.textContent.trim().toLowerCase()
                               .includes('actualizado correctamente')) {
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
                print(f"   ⚠️  JS TOAST SCAN FAILED: {js_err}")

        print("\n📸 TAKING SCREENSHOT #4 — AFTER GUARDAR (SUCCESS TOAST STATE)...")
        utils.tomar_screenshot(driver, "EDIT_FORM_02_4_AFTER_GUARDAR")

        test_passed = pencil_clicked and nombre_modified and apellido_modified and guardar_clicked and toast_detected

        print(f"\n   🔬 EDIT-FORM-02 ASSERTION SUMMARY:")
        print(f"      • PENCIL CLICKED              : {pencil_clicked}")
        print(f"      • NOMBRE MODIFIED             : {nombre_modified}  (→ '{EF02_NOMBRE_NUEVO}')")
        print(f"      • APELLIDO PATERNO MODIFIED   : {apellido_modified}  (→ '{EF02_APELLIDO_PAT_NUEVO}')")
        print(f"      • 'GUARDAR' CLICKED           : {guardar_clicked}")
        print(f"      • SUCCESS TOAST DETECTED      : {toast_detected}")
        print(f"      • FINAL URL                   : {driver.current_url}")

        _capture_web_evidence(driver, "EDIT_FORM_02")

        if test_passed:
            utils.tomar_screenshot(driver, "EDIT_FORM_02_SUCCESS")
            print("\n✅ EDIT-FORM-02: SUCCESS — USER UPDATED AND SUCCESS TOAST CONFIRMED.")
        else:
            utils.tomar_screenshot(driver, "EDIT_FORM_02_FAILED")
            if not pencil_clicked:
                print("\n❌ EDIT-FORM-02: FAILED — PENCIL ICON COULD NOT BE CLICKED.")
            elif not nombre_modified:
                print("\n❌ EDIT-FORM-02: FAILED — 'NOMBRE' FIELD COULD NOT BE MODIFIED.")
            elif not apellido_modified:
                print("\n❌ EDIT-FORM-02: FAILED — 'APELLIDO PATERNO' FIELD COULD NOT BE MODIFIED.")
            elif not guardar_clicked:
                print("\n❌ EDIT-FORM-02: FAILED — 'GUARDAR' BUTTON COULD NOT BE CLICKED.")
            else:
                print("\n❌ EDIT-FORM-02: FAILED — SUCCESS TOAST DID NOT APPEAR AFTER SAVING.")

    except Exception as e:
        print(f"\n💥 EDIT-FORM-02 CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver, "EDIT_FORM_02_TECHNICAL_ERROR")
        except Exception:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver.quit()


# ==================================================================================
# MAIN EXECUTION
# ==================================================================================
if __name__ == "__main__":

    logger, log_file, timestamp = utils.iniciar_reporte("EDIT_FORM")

    try:
        EDIT_FORM_01()
        EDIT_FORM_02()

    finally:
        utils.generar_reporte_html("EDIT_FORM", log_file, timestamp)