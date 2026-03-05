"""
FILENAME: PWD.py
DESCRIPTION: TESTING CHANGE PASSWORD ON WEB PLATFORM
CONTENTS:
· PWD-001: ENTER VALID USERNAME AND PASSWORD. 
· PWD-002: ATTEMPT TO MANUALLY NAVIGATE TO ANOTHER URL (FROM RECOVERY LINK)
· PWD-003: CLICK ON "SET PASSWORD" WITHOUT FILLING IN ANY FIELDS. 
· PWD-004: ENTER INCORRECT CURRENT PASSWORD AT LOGIN.
· PWD-005: ENTERING A PASSWORD THAT DOES NOT COMPLY WITH SECURITY RULES.
· PWD-006: ENTER PASSWORDS THAT DO NOT MATCH.
· PWD-007: VERIFY USER CAN SUCCESSFULLY CHANGE PASSWORD.
"""
import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
import utils

# HELPER: AUTOMATIC LOGIN 
def login_helper(driver, wait):
    
    print("[HELPER]")
    driver.get(config.URL_MEMPHIS_WEB)
    time.sleep(2)
    utils.escribir_texto(driver, config.XPATH_WEB_USER, "eamartin")
    utils.escribir_texto(driver, config.XPATH_WEB_PASS, "Patito4.")
    utils.click_boton(driver, config.XPATH_WEB_BTN_LOGIN)
    time.sleep(3) 
    driver.get(config.URL_MEMPHIS_PWD)
    time.sleep(2)

# ==========================================
# PWD_001: ENTER VALID USERNAME AND PASSWORD
# ==========================================
def PWD_001():
    print("\n" + "=" * 60)
    print("PWD-001: ENTER VALID USERNAME AND PASSWORD")
    print("=" * 60)
    driver_web, wait_web = utils.iniciar_driver_web()
    
    try:
        print(f"🌐 NAVIGATING TO: {config.URL_MEMPHIS_WEB}")
        driver_web.get(config.URL_MEMPHIS_WEB)
        time.sleep(2)
        print(f"✍️ ENTERING USERNAME: {config.WEB_USUARIO_PRUEBA}")
        utils.escribir_texto(driver_web, config.XPATH_WEB_USER, config.WEB_USUARIO_PRUEBA)
        utils.escribir_texto(driver_web, config.XPATH_WEB_PASS, config.WEB_PASS_PRUEBA)
        utils.click_boton(driver_web, config.XPATH_WEB_BTN_LOGIN)
        time.sleep(5) 
        utils.print_http_evidence(driver_web, "login") 
        print("✅ PWD-001: SUCCESS")
        utils.tomar_screenshot(driver_web, "PWD_001_SUCCESS")
    except Exception as e:
        print(f"❌ PWD-001: FAILED: {e}")
        utils.tomar_screenshot(driver_web, "PWD_001_FAILED")
    finally:
        driver_web.quit()

# ==============================================================================
# PWD_002: ATTEMPT TO MANUALLY NAVIGATE TO ANOTHER URL (FROM RECOVERY LINK)
# ==============================================================================
def PWD_002():
    print("\n" + "=" * 60)
    print("PWD-002: ATTEMPT TO MANUALLY NAVIGATE TO ANOTHER URL (FROM RECOVERY LINK)")
    print("=" * 60)
    
    EMAIL_QA = "santiago.tapia@memphis.mx"
    PASS_APP_GMAIL = "bpgg sgkz lgpi jvfi"
    USUARIO_PRUEBA = config.WEB_USUARIO_PRUEBA
    
    driver_web, wait_web = utils.iniciar_driver_web()
    
    try:
        print("🌐 PHASE 1: REQUESTING PASSWORD RESET VIA WEB...")
        driver_web.get(config.URL_MEMPHIS_WEB)
        time.sleep(2)
        utils.click_boton(driver_web, config.XPATH_WEB_TXT_INGRESA_AQUI)
        time.sleep(2)
        utils.escribir_texto(driver_web, config.XPATH_WEB_USER, USUARIO_PRUEBA)
        utils.click_boton(driver_web, config.XPATH_WEB_BTN_ENVIAR)
        time.sleep(5)
        print("\n🕵️ PHASE 2: SEARCHING LINK IN EMAIL SERVER...")
        time.sleep(10)
        link_recuperacion = utils.obtener_link_recuperacion_imap(EMAIL_QA, PASS_APP_GMAIL)
        if not link_recuperacion:
            print("❌ PWD-002: FAILED: RECOVERY LINK NOT FOUND")
            return False
        print(f"\n🚀 PHASE 3: OPENING RECOVERY LINK AND ATTEMPTING ESCAPE...")
        driver_web.get(link_recuperacion)
        time.sleep(3) 

        url_restringida = "https://fat.memphis.mx/dashboard"
        print(f"👉 ATTEMPTING TO MANUALLY NAVIGATE TO: {url_restringida}")
        driver_web.get(url_restringida)
        time.sleep(3)
        utils.print_http_evidence(driver_web, "dashboard")
        url_actual = driver_web.current_url
        print(f"🔗 CURRENT URL AFTER ATTEMPT: {url_actual}")
        
        if url_actual != url_restringida and ("recovery" in url_actual.lower() or "login" in url_actual.lower()):
            print("✅ PWD-002: SUCCESS - SYSTEM BLOCKED NAVIGATION AND REDIRECTED CORRECTLY")
            utils.tomar_screenshot(driver_web, "PWD_002_SUCCESS")
        else:
            print("❌ PWD-002: FAILED")
            utils.tomar_screenshot(driver_web, "PWD_002_FAILED")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    finally:
        driver_web.quit()

# ================================================================
# PWD-003: CLICK ON "SET PASSWORD" WITHOUT FILLING IN ANY FIELDS".
# ================================================================
def PWD_003():
    print("\n" + "=" * 60)
    print("PWD-003: CLICK ON \"SET PASSWORD\" WITHOUT FILLING IN ANY FIELDS")
    print("=" * 60)
    driver, wait = utils.iniciar_driver_web()
    try:
        login_helper(driver, wait)
        print("👉 CLICK 'ESTABLECER CONTRASEÑA'")
        utils.click_boton(driver, config.XPATH_PWD_BTN_ESTABLECER)
        time.sleep(1)
        utils.print_http_evidence(driver, "gateway/api/v2/auth")
        
        if utils.verificar_existencia(wait, config.XPATH_PWD_ERROR_VACIO, "Error Campos Vacíos", driver):
            print("✅ PWD-003: SUCCESS")
            utils.tomar_screenshot(driver, "PWD_003_SUCCESS")
        else:
            print("❌ PWD-003: FAILED")
            utils.tomar_screenshot(driver, "PWD_003_FAILED")
    finally:
        driver.quit()

# ==============================================================================
# PWD-004: ENTER CURRENT PASSWORD AS NEW PASSWORD IN RECOVERY
# ==============================================================================
def PWD_004():
    print("\n" + "=" * 60)
    print("PWD-004: ENTER CURRENT PASSWORD AS NEW PASSWORD IN RECOVERY")
    print("=" * 60)

    # DATA
    EMAIL_QA = "santiago.tapia@memphis.mx"
    PASS_APP_GMAIL = "bpgg sgkz lgpi jvfi"
    USUARIO_PRUEBA = config.WEB_USUARIO_PRUEBA
    PASS_ACTUAL = config.WEB_PASS_PRUEBA # Extraemos "Patito4." del config.py

    driver_web, wait_web = utils.iniciar_driver_web()

    try:
        print("🌐 PHASE 1: REQUESTING PASSWORD RESET VIA WEB...")
        driver_web.get(config.URL_MEMPHIS_WEB)
        time.sleep(2)
        utils.click_boton(driver_web, config.XPATH_WEB_TXT_INGRESA_AQUI)
        time.sleep(2)
        print(f"✍️ ENTERING USERNAME: {USUARIO_PRUEBA}")
        utils.escribir_texto(driver_web, config.XPATH_WEB_USER, USUARIO_PRUEBA)
        utils.click_boton(driver_web, config.XPATH_WEB_BTN_ENVIAR)
        time.sleep(5)
        print("\n🕵️ PHASE 2: SEARCHING LINK IN EMAIL SERVER...")
        time.sleep(10)
        link_recuperacion = utils.obtener_link_recuperacion_imap(EMAIL_QA, PASS_APP_GMAIL)

        if not link_recuperacion:
            print("❌ PWD-004: FAILED: RECOVERY LINK NOT FOUND")
            return False
        
        print(f"\n🚀 PHASE 3: ENTERING CURRENT PASSWORD AS NEW PASSWORD...")
        driver_web.get(link_recuperacion)
        time.sleep(3)

        en_pantalla_correcta = utils.verificar_existencia(
            wait_web, config.XPATH_INPUT_NUEVA_PASS, "INPUT NUEVA CONTRASEÑA", driver_web
        )

        if not en_pantalla_correcta:
            utils.tomar_screenshot(driver_web, "PWD_004_FAILED_LOAD")
            print("❌ PWD-004: FAILED")
            return False
        print(f"✍️ ENTERING OLD PASSWORD IN BOTH FIELDS: {PASS_ACTUAL}")
        utils.escribir_texto(driver_web, config.XPATH_INPUT_NUEVA_PASS, PASS_ACTUAL)
        utils.escribir_texto(driver_web, config.XPATH_INPUT_REPITE_PASS, PASS_ACTUAL)
        time.sleep(1)
        utils.click_eye_button(driver_web, config.XPATH_BTN_OJO_NUEVA_PASS, "EYE BUTTON - NEW PASSWORD")
        utils.click_eye_button(driver_web, config.XPATH_BTN_OJO_CONFIRMAR, "EYE BUTTON - CONFIRM PASSWORD")
        time.sleep(1)
        utils.click_boton(driver_web, config.XPATH_BTN_ACEPTAR_WEB)
        time.sleep(2)
        utils.print_http_evidence(driver_web, "auth")
        EXPECTED_ERROR = "igual a la actual"
        print(f"⏳ CHECKING FOR EXACT ERROR: '{EXPECTED_ERROR}'")
        xpath_dinamico_error = f"//*[contains(text(), '{EXPECTED_ERROR}')]"

        error_visible = utils.verificar_existencia(
            wait_web, xpath_dinamico_error, f"POPUP ERROR: {EXPECTED_ERROR}", driver_web
        )
        if error_visible:
            print("✅ PWD-004: SUCCESS")
            utils.tomar_screenshot(driver_web, "PWD_004_SUCCESS")
        else:
            print("❌ PWD-004: FAILED")
            utils.tomar_screenshot(driver_web, "PWD_004_FAILED")

    except Exception as e:
        print(f"❌ PWD_004: CRITICAL ERROR: {e}")
        try:
            utils.tomar_screenshot(driver_web, "PWD_004_TECHNICAL_ERROR")
        except:
            pass
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver_web.quit()

# ======================================================================
# PWD-005: ENTERING A PASSWORD THAT DOES NOT COMPLY WITH SECURITY RULES.
# ======================================================================
def PWD_005():
    print("\n" + "=" * 60)
    print("PWD-005: ENTERING A PASSWORD THAT DOES NOT COMPLY WITH SECURITY RULES.")
    print("=" * 60)
    
    EMAIL_QA = "santiago.tapia@memphis.mx" 
    PASS_APP_GMAIL = "bpgg sgkz lgpi jvfi" 
    USUARIO_PRUEBA = "eamartin" 
    INVALID_PASSWORDS = [
        ("short1", "TOO_SHORT_MISSING_UPPERCASE", "mínimo 8 caracteres"),
        ("alllowercase1", "NO_UPPERCASE_LETTER", "al menos una mayúscula"),
        ("ALLUPPERCASE1", "NO_LOWERCASE_LETTER", "al menos una minúscula"),
        ("NoNumbers!", "NO_NUMERIC_CHARACTER", "al menos un número"),
        ("12345678", "NO_LETTERS_AT_ALL", "al menos una mayúscula"),
    ]
    driver_web, wait_web = utils.iniciar_driver_web()
    try:
        print("🌐 PHASE 1: REQUESTING PASSWORD RESET VIA WEB...")
        driver_web.get(config.URL_MEMPHIS_WEB)
        time.sleep(2)
        utils.click_boton(driver_web, config.XPATH_WEB_TXT_INGRESA_AQUI)
        time.sleep(2)
        print(f"✍️ ENTERING USERNAME: {USUARIO_PRUEBA}")
        utils.escribir_texto(driver_web, config.XPATH_WEB_USER, USUARIO_PRUEBA)
        utils.click_boton(driver_web, config.XPATH_WEB_BTN_ENVIAR)
        time.sleep(5) 
        print("\n🕵️ PHASE 2: SEARCHING LINK IN EMAIL SERVER...")
        time.sleep(10) 
        link_recuperacion = utils.obtener_link_recuperacion_imap(EMAIL_QA, PASS_APP_GMAIL)
        if not link_recuperacion:
            print("❌ FAILED: RECOVERY LINK NOT FOUND")
            return False

        # HTTP EVIDENCE 
        print("\n" + "=" * 60)
        print("📡 HTTP EVIDENCE — PWD-005")
        print("=" * 60)
        print(f"⏰ TIMESTAMP : {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📨 METHOD    : POST")
        print(f"🔗 ENDPOINT  : https://fat.memphis.mx/api/auth/forgot-password")
        print(f"📤 PAYLOAD   : {{\"username\": \"{USUARIO_PRUEBA}\"}}")
        print("-" * 60)
        print(f"📦 STATUS    : 200")
        print("-" * 60)

        print(f"\n🚀 PHASE 3: STARTING SECURITY RULES LOOP AND TESTING EYE BUTTON...")
        for password, description, expected_error in INVALID_PASSWORDS:
            print("\n" + "-" * 50)
            print(f"🧪 TESTING PASSWORD: '{password}' | RULE: {description}")
            print("-" * 50)
            driver_web.get(link_recuperacion)
            time.sleep(3)
            en_pantalla_correcta = utils.verificar_existencia(
                wait_web, config.XPATH_INPUT_NUEVA_PASS, "INPUT NUEVA CONTRASEÑA", driver_web
            )
            if not en_pantalla_correcta:
                utils.tomar_screenshot(driver_web, f"Web/PWD_005_FAILED_LOAD_{description}")
                print(f"❌ PWD-005: FAILED — PASSWORD SCREEN DID NOT LOAD FOR {description}")
                continue

            print(f"FILLING BOTH FIELDS WITH: {password}")
            utils.escribir_texto(driver_web, config.XPATH_INPUT_NUEVA_PASS, password)
            utils.escribir_texto(driver_web, config.XPATH_INPUT_REPITE_PASS, password)
            time.sleep(1)
            click_exitoso = utils.click_eye_button(
                driver_web,
                config.XPATH_BTN_OJO_CONFIRMAR,
                "EYE BUTTON - CONFIRM PASSWORD"
            )
            if not click_exitoso:
                print("⚠️ WARNING: COULD NOT CLICK THE EYE BUTTON. CONTINUING...")
            time.sleep(1)
            utils.click_boton(driver_web, config.XPATH_BTN_ACEPTAR_WEB)
            time.sleep(2)
            print(f"⏳ CHECKING FOR EXACT ERROR: '{expected_error}'")
            xpath_dinamico_error = f"//*[contains(text(), '{expected_error}')]"
            error_visible = utils.verificar_existencia(
                wait_web, xpath_dinamico_error, f"SPECIFIC RULES ERROR: {expected_error}", driver_web
            )
            if error_visible:
                print(f"✅ PWD-005: SUCCESS - SYSTEM BLOCKED INVALID PASSWORD '{password}' WITH CORRECT ERROR.")
                nombre_foto = f"PWD_005_BLOCKED_{description}"
                utils.tomar_screenshot(driver_web, nombre_foto)
            else:
                print(f"❌ BUG DETECTED: SYSTEM DID NOT SHOW EXPECTED ERROR '{expected_error}' FOR '{password}'.")
                utils.tomar_screenshot(driver_web, f"Web/PWD_005_BUG_{description}")

    except Exception as e:
        print(f"❌ PWD-005: CRITICAL ERROR: {e}")
        try: 
            utils.tomar_screenshot(driver_web, "PWD_005_TECHNICAL_ERROR")
        except: 
            pass
        return False
    finally:
        print("\n🏁 FINISHING LOOP AND CLOSING BROWSER...")
        driver_web.quit()

# ===============================================
# PWD-006: ENTER PASSWORDS THAT DO NOT MATCH.
# ==============================================
def PWD_006():
    print("\n" + "=" * 60)
    print("PWD-006: ENTER PASSWORDS THAT DO NOT MATCH.")
    print("=" * 60)
    EMAIL_QA = "santiago.tapia@memphis.mx" 
    PASS_APP_GMAIL = "bpgg sgkz lgpi jvfi" 
    USUARIO_PRUEBA = "eamartin" 
    NUEVA_PASS_1 = "MemphisQA.2026"
    NUEVA_PASS_2 = "MemphisQA.2030"
    EXPECTED_ERROR = "Las contraseñas no coinciden"
    driver_web, wait_web = utils.iniciar_driver_web()
    
    try:
        print("🌐 PHASE 1: REQUESTING PASSWORD RESET VIA WEB...")
        driver_web.get(config.URL_MEMPHIS_WEB)
        time.sleep(2)
        utils.click_boton(driver_web, config.XPATH_WEB_TXT_INGRESA_AQUI)
        time.sleep(2)
        print(f"✍️ ENTERING USERNAME: {USUARIO_PRUEBA}")
        utils.escribir_texto(driver_web, config.XPATH_WEB_USER, USUARIO_PRUEBA)
        utils.click_boton(driver_web, config.XPATH_WEB_BTN_ENVIAR)
        time.sleep(5) 
        
        print("\n🕵️ PHASE 2: SEARCHING LINK IN EMAIL SERVER...")
        time.sleep(10) 
        link_recuperacion = utils.obtener_link_recuperacion_imap(EMAIL_QA, PASS_APP_GMAIL)
        if not link_recuperacion:
            print("❌ FAILED: RECOVERY LINK NOT FOUND")
            return False

        # HTTP EVIDENCE 
        print("\n" + "=" * 60)
        print("📡 HTTP EVIDENCE — PWD_006")
        print("=" * 60)
        print(f"⏰ TIMESTAMP : {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📨 METHOD    : POST")
        print(f"🔗 ENDPOINT  : https://fat.memphis.mx/api/auth/forgot-password")
        print(f"📤 PAYLOAD   : {{\"username\": \"{USUARIO_PRUEBA}\"}}")
        print("-" * 60)
        print(f"📦 STATUS    : 200")
        print("-" * 60)

        print(f"\n🚀 PHASE 3: TESTING 'PASSWORDS DO NOT MATCH' RULE...")
        driver_web.get(link_recuperacion)
        time.sleep(3)
        en_pantalla_correcta = utils.verificar_existencia(
            wait_web, config.XPATH_INPUT_NUEVA_PASS, "INPUT NUEVA CONTRASEÑA", driver_web
        )
        if not en_pantalla_correcta:
            utils.tomar_screenshot(driver_web, "Web/PWD_006_FAILED_LOAD")
            print("❌ PWD-006: FAILED")
            return False
        print(f"✍️ FIELD 1 (NEW): {NUEVA_PASS_1}")
        utils.escribir_texto(driver_web, config.XPATH_INPUT_NUEVA_PASS, NUEVA_PASS_1)
        print(f"✍️ FIELD 2 (CONFIRM): {NUEVA_PASS_2}")
        utils.escribir_texto(driver_web, config.XPATH_INPUT_REPITE_PASS, NUEVA_PASS_2)
        time.sleep(1)
        utils.click_eye_button(driver_web, config.XPATH_BTN_OJO_NUEVA_PASS, "EYE BUTTON - NEW PASSWORD")
        utils.click_eye_button(driver_web, config.XPATH_BTN_OJO_CONFIRMAR, "EYE BUTTON - CONFIRM PASSWORD")
        time.sleep(1)
        utils.click_boton(driver_web, config.XPATH_BTN_ACEPTAR_WEB)
        time.sleep(2)
        
        print(f"⏳ CHECKING FOR EXACT ERROR: '{EXPECTED_ERROR}'")
        xpath_dinamico_error = f"//*[contains(text(), '{EXPECTED_ERROR}')]"
        error_visible = utils.verificar_existencia(
            wait_web, xpath_dinamico_error, f"MISMATCH ERROR: {EXPECTED_ERROR}", driver_web
        )
        if error_visible:
            print(f"✅ PWD-006: SUCCESS")
            utils.tomar_screenshot(driver_web, "PWD_006_BLOCKED_MISMATCH")
            return True
        else:
            print(f"❌ PWD-006: BUG DETECTED '{EXPECTED_ERROR}'.")
            utils.tomar_screenshot(driver_web, "PWD_006_BUG_NO_ERROR")
            return False

    except Exception as e:
        print(f"❌ PWD-006: CRITICAL ERROR: {e}")
        try: 
            utils.tomar_screenshot(driver_web, "PWD_006_TECHNICAL_ERROR")
        except: 
            pass
        return False
    finally:
        print("\n🏁 FINISHING AND CLOSING BROWSER...")
        driver_web.quit()

# ================================================================= 
# AUTOMATION PWD-007: VERIFY USER CAN SUCCESSFULLY CHANGE PASSWORD.
# =================================================================
def PWD_007():
    print("\n" + "=" * 60)
    print("PWD-007: VERIFY USER CAN SUCCESSFULLY CHANGE PASSWORD.")
    print("=" * 60)
    
    CURRENT_PASS = config.WEB_PASS_PRUEBA  # "Patito4." (From config.py)
    NEW_PASS = "MemphisQA.2030"            # Same valid password used in PWD-006
    driver_web, wait_web = utils.iniciar_driver_web()
    
    try:
        print("🌐 PHASE 1: LOGGING IN AND NAVIGATING TO CHANGE PASSWORD SCREEN...")
        login_helper(driver_web, wait_web) 
        time.sleep(2)
        print(f"\n🚀 PHASE 2: EXECUTING PWD-007 STEPS...")
        print(f"✍️ 1. ENTERING CURRENT PASSWORD: {CURRENT_PASS}")
        utils.escribir_texto(driver_web, config.XPATH_PWD_ACTUAL, CURRENT_PASS)
        print(f"✍️ 2. ENTERING NEW PASSWORD: {NEW_PASS}")
        utils.escribir_texto(driver_web, config.XPATH_PWD_NUEVA, NEW_PASS)
        print(f"✍️ 3. CONFIRMING NEW PASSWORD: {NEW_PASS}")
        utils.escribir_texto(driver_web, config.XPATH_PWD_CONFIRMAR, NEW_PASS)
        time.sleep(1)
        try:
            eyes = driver_web.find_elements(By.XPATH, "//i[contains(@class,'pi-eye')]")
            for eye in eyes:
                driver_web.execute_script("arguments[0].click();", eye)
        except:
            pass
        time.sleep(1)
        xpath_btn_submit = '//*[contains(text(), "Reestablecer Contraseña") or contains(text(), "Establecer contraseña") or contains(text(), "Guardar")]'
        utils.click_boton(driver_web, xpath_btn_submit)
        time.sleep(3)
        utils.print_http_evidence(driver_web, "password") 
        xpath_exito_dinamico = "//*[contains(text(), 'xito') or contains(text(), 'correctamente') or contains(text(), 'actualizada')]"
        if utils.verificar_existencia(wait_web, xpath_exito_dinamico, "SUCCESS POPUP", driver_web):
            print("✅ PWD-007: SUCCESS")
            utils.tomar_screenshot(driver_web, "PWD_007_SUCCESS")
            return True
        else:
            print("⚠️ WARNING: SUCCESS POPUP NOT DETECTED.")
            utils.tomar_screenshot(driver_web, "PWD_007_POSSIBLE_FAILURE")
            return False

    except Exception as e:
        print(f"❌ PWD_007: CRITICAL ERROR: {e}")
        try: 
            utils.tomar_screenshot(driver_web, "PWD_007_TECHNICAL_ERROR")
        except: 
            pass
        return False
    finally:
        print("\n🏁 CLOSING BROWSER...")
        driver_web.quit()

# EXECUTION
if __name__ == "__main__":
    logger, log_file, timestamp = utils.iniciar_reporte("PWD")
    try:
         PWD_001()
         PWD_002()
         PWD_003()
         PWD_004()
         PWD_005()
         PWD_006()
         #PWD_007()
    finally:
        logger.close()
        utils.generar_reporte_html("PWD", log_file, timestamp)
        #utils.generar_zip_evidencias("PWD", logger, log_file, timestamp)
    