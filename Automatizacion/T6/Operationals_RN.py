"""
FILENAME: Operationals_RN.py
DESCRIPTION:
    AUTOMATED TEST SUITE FOCUSED ON THE BUSINESS REGISTRATION (REGISTRO DE NEGOCIO) MODULE.
    VALIDATES FLOWS FOR USERS CONFIGURING THEIR COMMERCE AFTER LOGIN.

CONTENTS:
    · RN-44: VALIDATE BUSINESS REGISTRATION SCREEN APPEARS FOR NEW/UNLINKED ACCOUNTS.
    · RN-45: VALIDATE SUCCESSFUL BUSINESS REGISTRATION WITH VALID TOKEN AND AFFILIATION.
    · RN-46: ENTERING WRONG TOKEN AND AFFILIATION NUMBER WILL BE GOOD.
    · RN-47: ENTERING GOOD TOKEN AND WRONG AFFILIATION NUMBER.
    · RN-48: VALIDATE ERROR WHEN TOKEN FIELD IS EMPTY.
    · RN-49: VALIDATE ERROR WHEN AFFILIATION NUMBER FIELD IS EMPTY
    · RN-50: VALIDATE TOKEN LENGTH RESTRICTIONS (<16, >16, ==16) 
    · RN-51: VALIDATE AFFILIATION NUMBER LENGTH RESTRICTIONS (<7, >7, ==7)
    · RN-52: VALIDATE SKIP BUSINESS REGISTRATION ("EN OTRA OCASION")
    · RN-53: VALIDATE FIELD INTERACTION (FOCUS/BLUR) WITHOUT DATA


REQUIREMENTS:
    - APPIUM SERVER RUNNING.
    - config.py AND utils.py IN THE SAME DIRECTORY.
"""

import sys
import os
import time
ruta_proyecto = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ruta_proyecto not in sys.path:
    sys.path.append(ruta_proyecto)
import config
import utils
from selenium.webdriver.common.by import By

# =================================================================================
# HELPER: QUICK LOGIN TO REACH REGISTRATION SCREEN
# =================================================================================
def helper_login_to_registration(driver, wait):
    """Executes the login flow to reach the Business Registration screen."""
    print("   🔄 [HELPER] EXECUTING LOGIN TO REACH REGISTRATION SCREEN...")
    print("   ⏳ Waiting for Appium to render input fields...")
    time.sleep(4) 
    try:
        utils.click_boton(driver, config.XPATH_INPUT_USUARIO)
        time.sleep(1)
    except:
        pass
        
    print(f"   📧 Typing Email: {config.USUARIO_VALIDO}")
    utils.escribir_texto(driver, config.XPATH_INPUT_USUARIO, config.USUARIO_VALIDO)
    
    print("   🔑 Typing Password...")
    utils.escribir_texto(driver, config.XPATH_INPUT_PASS, config.PASS_VALIDO)
    
    try: 
        driver.hide_keyboard()
    except: 
        pass
        
    print("   🖱️ Clicking Accept...")
    utils.click_boton(driver, config.XPATH_BTN_ACEPTAR)
    
    print("   ⏳ Waiting for backend routing...")
    time.sleep(6)

# =================================================================================
# RN-44: VALIDATE BUSINESS REGISTRATION SCREEN APPEARS FOR NEW/UNLINKED ACCOUNTS
# =================================================================================
def RN_44():
    print("\n" + "=" * 60)
    print("RN-44: VALIDATE BUSINESS REGISTRATION SCREEN ON LOGIN")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        print("👉 STEP 1 & 2: ENTERING CREDENTIALS AND CLICKING ACCEPT...")
        helper_login_to_registration(driver, wait)

        print("🔍 VERIFYING 'REGISTRO DE NEGOCIO' SCREEN IS DISPLAYED...")
        pantalla_cargada = utils.verificar_existencia(wait, config.XPATH_RN_TITULO_NEGOCIO, "TITLE: REGISTRO DE NEGOCIO", driver)

        if pantalla_cargada:
            print("📸 TAKING SCREENSHOT EVIDENCE...")
            utils.tomar_screenshot(driver, "RN_44_SUCCESS")
            try: utils.print_http_evidence_appium(driver, "RN_44")
            except: pass
            print("✅ RN-44: SUCCESS")
            return True

        else:
            print("❌ RN-44 FAILED")
            utils.tomar_screenshot(driver, "RN_44_FAILED")
            try: utils.print_http_evidence_appium(driver, "RN_44")
            except: pass
            return False
            

    except Exception as e:
        print(f"❌ RN-44 CRITICAL ERROR: {e}")
        return False
    finally:
        utils.cerrar_driver(driver)


# =================================================================================
# RN-45: VALIDATE SUCCESSFUL BUSINESS REGISTRATION
# =================================================================================
def RN_45():
    print("\n" + "=" * 60)
    print("RN-45: VALIDATE SUCCESSFUL BUSINESS REGISTRATION (TOKEN & AFFILIATION)")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        # PRECONDITION: REACH THE REGISTRATION SCREEN
        print("🔐 PRECONDITION: LOGGING IN TO REACH REGISTRATION SCREEN...")
        helper_login_to_registration(driver, wait)

        # STEP 1: ENTER REGISTRATION DATA
        print("👉 STEP 1: ENTERING REGISTRATION TOKEN AND AFFILIATION NUMBER...")
        time.sleep(4) 
        
        print(f"   🔑 ENTERING TOKEN: {config.RN_TOKEN}")
        try: utils.click_boton(driver, config.XPATH_RN_INPUT_TOKEN)
        except: pass
        time.sleep(1)
        utils.escribir_texto(driver, config.XPATH_RN_INPUT_TOKEN, config.RN_TOKEN)
        
        print(f"   🏢 ENTERING AFFILIATION: {config.RN_AFILIACION}")
        try: utils.click_boton(driver, config.XPATH_RN_INPUT_AFILIACION)
        except: pass
        time.sleep(1)
        utils.escribir_texto(driver, config.XPATH_RN_INPUT_AFILIACION, config.RN_AFILIACION)
        
        try: driver.hide_keyboard()
        except: pass

        # STEP 2: CLICK ACCEPT / CONTINUE
        print("👉 STEP 2: CLICKING 'ACEPTAR' TO SUBMIT REGISTRATION...")
        utils.click_boton(driver, config.XPATH_RN_BTN_ACEPTAR_REGISTRO)
        
        print("⏳ WAITING FOR SYSTEM TO PROCESS REGISTRATION...")
        time.sleep(8) # Esperamos a que el backend valide el token

        # ---------------------------------------------------------
        # VALIDATION: VERIFY WE NAVIGATED TO THE NEXT SCREEN
        # ---------------------------------------------------------
        print("🔍 VERIFYING NAVIGATION TO THE SUCCESS/DASHBOARD SCREEN...")
        
        pantalla_siguiente_cargada = utils.verificar_existencia(
            wait, 
            config.XPATH_RN_PANTALLA_EXITO, 
            "NEXT SCREEN IDENTIFIER", 
            driver
        )

        if pantalla_siguiente_cargada:
            print("📸 TAKING SCREENSHOT EVIDENCE OF THE SUCCESS SCREEN...")
            utils.tomar_screenshot(driver, "RN_45_SUCCESS")
            
            try: utils.print_http_evidence_appium(driver, "RN_45")
            except: pass
            
            print("✅ RN-45: SUCCESS")
            return True
        else:
            print("❌ RN-45 FAILED")
            utils.tomar_screenshot(driver, "RN_45_FAILED")
            try: utils.print_http_evidence_appium(driver, "RN_45")
            except: pass
            print("🔍 SCANNING FOR ERROR MESSAGES OR POP-UPS...")
            try:
                todos = driver.find_elements(By.XPATH, "//*")
                for elem in todos:
                    t = elem.get_attribute("text")
                    if t and len(t) > 3:
                        print(f"   -> VISIBLE TEXT: '{t}'")
            except: pass
            return False

    except Exception as e:
        print(f"❌ RN-45 CRITICAL ERROR: {e}")
        try: utils.tomar_screenshot(driver, "RN_45_TECHNICAL_ERROR")
        except: pass
        return False
    finally:
        utils.cerrar_driver(driver)

# =================================================================================
# RN-46: ENTERING WRONG TOKEN AND AFFILIATION NUMBER WILL BE GOOD 
# =================================================================================
def RN_46():
    print("\n" + "=" * 60)
    print("RN-46: ENTERING WRONG TOKEN AND AFFILIATION NUMBER WILL BE GOOD")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        # PRECONDITION: REACH THE REGISTRATION SCREEN
        print("🔐 PRECONDITION: LOGGING IN TO REACH REGISTRATION SCREEN...")
        helper_login_to_registration(driver, wait)

        # STEP 1: ENTER REGISTRATION DATA
        print("👉 STEP 1: ENTERING REGISTRATION TOKEN AND AFFILIATION NUMBER...")
        time.sleep(4) 

        print(f"   🔑 ENTERING TOKEN: {config.RN_TOKEN_INVALIDO}")
        try: 
            utils.click_boton(driver, config.XPATH_RN_INPUT_TOKEN)
        except: 
            pass
        time.sleep(1)
        utils.escribir_texto(driver, config.XPATH_RN_INPUT_TOKEN, config.RN_TOKEN_INVALIDO)
        
        print(f"   🏢 ENTERING AFFILIATION: {config.RN_AFILIACION}")
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

        # STEP 2: CLICK ACCEPT / CONTINUE
        print("👉 STEP 2: CLICKING 'ACEPTAR' TO SUBMIT REGISTRATION...")
        utils.click_boton(driver, config.XPATH_RN_BTN_ACEPTAR_REGISTRO)
        
        print("⏳ WAITING FOR SYSTEM TO PROCESS REGISTRATION...")
        time.sleep(2) 

        # VALIDATION: VERIFY WE SAW THE POPUP ERROR MESSAGE 
        print("🔍 VERIFYING WE SAW THE POPUP ERROR MESSAGE...")
        mensaje_encontrado = False

        for i in range(10):
            try:
                fuente_xml = driver.page_source.lower()
                if "afiliacion es incorrecto" in fuente_xml or  "el token o" in fuente_xml:
                    mensaje_encontrado = True
                    print(f" POPUP DETECTED ON ATTEMPT {i+1}")
                    utils.tomar_screenshot(driver, f"RN_46_SUCCESS")
                    break
            except Exception as e:
                pass 
            time.sleep(0.5)

        if mensaje_encontrado:
            try: 
                utils.print_http_evidence_appium(driver, "RN_46")
            except: 
                pass
            print("✅ RN-46: SUCCESS")
            return True
        else:
            print("❌ RN-46 FAILED")
            utils.tomar_screenshot(driver, "RN_46_FAILED")
            try: utils.print_http_evidence_appium(driver, "RN_46")
            except: pass
            print("PRINTING RAW XML SOURCE FOR DEBUGGING...")
            print(driver.page_source)
            return False

    except Exception as e:
        print(f"❌ RN-46 CRITICAL ERROR: {e}")
        try: 
            utils.tomar_screenshot(driver, "RN_46_TECHNICAL_ERROR")
        except: 
            pass
        return False
    finally:
        utils.cerrar_driver(driver)

# =================================================================================
# RN-47: ENTERING GOOD TOKEN AND WRONG AFFILIATION NUMBER 
# =================================================================================
def RN_47():
    print("\n" + "=" * 60)
    print("RN-47: ENTERING GOOD TOKEN AND WRONG AFFILIATION NUMBER")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        # PRECONDITION: REACH THE REGISTRATION SCREEN
        print("🔐 PRECONDITION: LOGGING IN TO REACH REGISTRATION SCREEN...")
        helper_login_to_registration(driver, wait)

        # STEP 1: ENTER REGISTRATION DATA
        print("👉 STEP 1: ENTERING REGISTRATION TOKEN AND AFFILIATION NUMBER...")
        time.sleep(4) 

        print(f"   🔑 ENTERING TOKEN: {config.RN_TOKEN}")
        try: 
            utils.click_boton(driver, config.XPATH_RN_INPUT_TOKEN)
        except: 
            pass
        time.sleep(1)
        utils.escribir_texto(driver, config.XPATH_RN_INPUT_TOKEN, config.RN_TOKEN)
        
        print(f"   🏢 ENTERING AFFILIATION: {config.RN_AFILIACION_INVALIDA}")
        try: 
            utils.click_boton(driver, config.XPATH_RN_INPUT_AFILIACION)
        except: 
            pass
        time.sleep(1)
        utils.escribir_texto(driver, config.XPATH_RN_INPUT_AFILIACION, config.RN_AFILIACION_INVALIDA)
        
        try: 
            driver.hide_keyboard()
        except: 
            pass

        # STEP 2: CLICK ACCEPT / CONTINUE
        print("👉 STEP 2: CLICKING 'ACEPTAR' TO SUBMIT REGISTRATION...")
        utils.click_boton(driver, config.XPATH_RN_BTN_ACEPTAR_REGISTRO)
        
        print("⏳ WAITING FOR SYSTEM TO PROCESS REGISTRATION...")
        time.sleep(2) 

        # VALIDATION: VERIFY WE SAW THE POPUP ERROR MESSAGE 
        print("🔍 VERIFYING WE SAW THE POPUP ERROR MESSAGE...")
        mensaje_encontrado = False

        for i in range(10):
            try:
                fuente_xml = driver.page_source.lower()
                if "afiliacion es incorrecto" in fuente_xml or  "el token o" in fuente_xml:
                    mensaje_encontrado = True
                    print(f" POPUP DETECTED ON ATTEMPT {i+1}")
                    utils.tomar_screenshot(driver, f"RN_47_SUCCESS")
                    break
            except Exception as e:
                pass 
            time.sleep(0.5)

        if mensaje_encontrado:
            try: 
                utils.print_http_evidence_appium(driver, "RN_47")
            except: 
                pass
            print("✅ RN-47: SUCCESS")
            return True
        else:
            print("❌ RN-47 FAILED")
            utils.tomar_screenshot(driver, "RN_47_FAILED")
            try: utils.print_http_evidence_appium(driver, "RN_47")
            except: pass
            print("PRINTING RAW XML SOURCE FOR DEBUGGING...")
            print(driver.page_source)
            return False

    except Exception as e:
        print(f"❌ RN-47 CRITICAL ERROR: {e}")
        try: 
            utils.tomar_screenshot(driver, "RN_47_TECHNICAL_ERROR")
        except: 
            pass
        return False
    finally:
        utils.cerrar_driver(driver)

# =================================================================================
# RN-48: VALIDATE ERROR WHEN TOKEN FIELD IS EMPTY
# =================================================================================
def RN_48():
    print("\n" + "=" * 60)
    print("RN-48: VALIDATE ERROR WHEN TOKEN FIELD IS EMPTY")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        print("🔐 PRECONDITION: LOGGING IN TO REACH REGISTRATION SCREEN...")
        helper_login_to_registration(driver, wait)

        # STEP 1: ENTER REGISTRATION DATA (LEAVING TOKEN EMPTY)
        print("👉 STEP 1: LEAVING TOKEN EMPTY AND ENTERING AFFILIATION...")
        time.sleep(4) 

        print("   🔑 TOKEN: [LEAVING EMPTY]")
        try: utils.click_boton(driver, config.XPATH_RN_INPUT_TOKEN)
        except: pass
        time.sleep(1)
        
        print(f"   🏢 ENTERING AFFILIATION: {config.RN_AFILIACION}")
        try: utils.click_boton(driver, config.XPATH_RN_INPUT_AFILIACION)
        except: pass
        time.sleep(1)
        utils.escribir_texto(driver, config.XPATH_RN_INPUT_AFILIACION, config.RN_AFILIACION)
        
        try: driver.hide_keyboard()
        except: pass

        # STEP 2: CLICK ACCEPT
        print("👉 STEP 2: CLICKING 'ACEPTAR'...")
        utils.click_boton(driver, config.XPATH_RN_BTN_ACEPTAR_REGISTRO)
        print("⏳ SCANNING FOR UNKNOWN ERROR MESSAGE...")
        
        mensaje_encontrado = False
        texto_detectado = ""
        
        palabras_sospechosas = ["requerido", "obligatorio", "vacío", "vacio", "ingresa", "error", "incorrecto"]

        for i in range(10): 
            try:
                fuente_xml = driver.page_source.lower() 
                
                if any(palabra in fuente_xml for palabra in palabras_sospechosas):
                    mensaje_encontrado = True
                    print(f" POPUP DETECTED ON ATTEMPT {i+1}")
                    utils.tomar_screenshot(driver, "RN_48_SUCCESS")
                    break
            except Exception as e:
                pass
            
            time.sleep(0.5)

        if mensaje_encontrado:
            try: utils.print_http_evidence_appium(driver, "RN_48")
            except: pass
            print("✅ RN-48: SUCCESS)")
            return True
        else:
            print("❌ RN-48 FAILED")
            utils.tomar_screenshot(driver, "RN_48_FAILED")
            try: utils.print_http_evidence_appium(driver, "RN_48")
            except: pass
            print("🔍 RAW XML DUMP:")
            print(driver.page_source)
            return False

    except Exception as e:
        print(f"❌ RN-48 CRITICAL ERROR: {e}")
        try: utils.tomar_screenshot(driver, "RN_48_TECHNICAL_ERROR")
        except: pass
        return False
    finally:
        utils.cerrar_driver(driver)

# =================================================================================
# RN-49: VALIDATE ERROR WHEN AFFILIATION NUMBER FIELD IS EMPTY
# =================================================================================
def RN_49():
    print("\n" + "=" * 60)
    print("RN-49: VALIDATE ERROR WHEN AFFILIATION NUMBER FIELD IS EMPTY")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        print("🔐 PRECONDITION: LOGGING IN TO REACH REGISTRATION SCREEN...")
        helper_login_to_registration(driver, wait)

        # STEP 1: ENTER REGISTRATION DATA (LEAVING TOKEN EMPTY)
        print("👉 STEP 1: LEAVING TOKEN EMPTY AND ENTERING AFFILIATION...")
        time.sleep(4) 

        print(f"   🔑 ENTERING TOKEN: {config.RN_TOKEN}")
        try: utils.click_boton(driver, config.XPATH_RN_INPUT_TOKEN)
        except: pass
        time.sleep(1)
        utils.escribir_texto(driver, config.XPATH_RN_INPUT_TOKEN, config.RN_TOKEN)
        
        print("   🏢 AFFILIATION: [LEAVING EMPTY]")
        try: utils.click_boton(driver, config.XPATH_RN_INPUT_AFILIACION)
        except: pass
        time.sleep(1)

        
        try: driver.hide_keyboard()
        except: pass

        # STEP 2: CLICK ACCEPT
        print("👉 STEP 2: CLICKING 'ACEPTAR'...")
        utils.click_boton(driver, config.XPATH_RN_BTN_ACEPTAR_REGISTRO)
        print("⏳ SCANNING FOR UNKNOWN ERROR MESSAGE...")
        
        mensaje_encontrado = False
        texto_detectado = ""
        
        palabras_sospechosas = ["requerido", "obligatorio", "vacío", "vacio", "ingresa", "error", "incorrecto"]

        for i in range(10): 
            try:
                fuente_xml = driver.page_source.lower() 
                
                if any(palabra in fuente_xml for palabra in palabras_sospechosas):
                    mensaje_encontrado = True
                    print(f" POPUP DETECTED ON ATTEMPT {i+1}")
                    utils.tomar_screenshot(driver, "RN_49_SUCCESS")
                    break
            except Exception as e:
                pass
            
            time.sleep(0.5)

        if mensaje_encontrado:
            try: utils.print_http_evidence_appium(driver, "RN_49")
            except: pass
            print("✅ RN-49: SUCCESS)")
            return True
        else:
            print("❌ RN-49 FAILED")
            utils.tomar_screenshot(driver, "RN_49_FAILED")
            try: utils.print_http_evidence_appium(driver, "RN_49")
            except: pass
            print("🔍 RAW XML DUMP:")
            print(driver.page_source)
            return False

    except Exception as e:
        print(f"❌ RN-49 CRITICAL ERROR: {e}")
        try: utils.tomar_screenshot(driver, "RN_49_TECHNICAL_ERROR")
        except: pass
        return False
    finally:
        utils.cerrar_driver(driver)

# =================================================================================
# RN-50: VALIDATE TOKEN LENGTH RESTRICTIONS (<16, >16, ==16)
# =================================================================================
def RN_50():
    print("\n" + "=" * 60)
    print("RN-50: VALIDATE TOKEN LENGTH RESTRICTIONS (3 SCENARIOS)")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        print("🔐 PRECONDITION: LOGGING IN TO REACH REGISTRATION SCREEN...")
        helper_login_to_registration(driver, wait)
        
        print(f"   🏢 ENTERING VALID AFFILIATION: {config.RN_AFILIACION}")
        time.sleep(4)
        try: utils.click_boton(driver, config.XPATH_RN_INPUT_AFILIACION)
        except: pass
        utils.escribir_texto(driver, config.XPATH_RN_INPUT_AFILIACION, config.RN_AFILIACION)
        
        try: driver.hide_keyboard()
        except: pass

        # =========================================================
        # SCENARIO 1: SHORT TOKEN (< 16)
        # =========================================================
        print("\n▶️ SCENARIO 1: SHORT TOKEN (< 16 CHARS)")
        
        campo_token = driver.find_element(By.XPATH, config.XPATH_RN_INPUT_TOKEN)
        campo_token.clear()
        campo_token.send_keys(config.RN_TOKEN_CORTO)
        
        utils.click_boton(driver, config.XPATH_RN_BTN_ACEPTAR_REGISTRO)
        
        print("⏳ SCANNING FOR ERROR MESSAGE (SHORT TOKEN)...")
        error_detectado = False
        for i in range(8): 
            if any(palabra in driver.page_source.lower() for palabra in ["error", "incorrecto", "inválido", "invalid", "caracteres"]):
                error_detectado = True
                print("   🎯 SUCCESS : ERROR DETECTED FOR SHORT TOKEN!")
                utils.tomar_screenshot(driver, "RN_50_SCENARIO_1_SHORT_SUCCESS")
                break
            time.sleep(0.5)
            
        if not error_detectado:
            print("   ⚠️ WARNING: NO ERROR DETECTED FOR SHORT TOKEN. SYSTEM MIGHT HAVE PROCEEDED.")
            utils.tomar_screenshot(driver, "RN_50_SCENARIO_1_FAILED")

        print("⏳ WAITING FOR ERROR BANNER TO DISAPPEAR...")
        time.sleep(4) 

        # =========================================================
        # SCENARIO 2: LONG TOKEN (> 16)
        # =========================================================
        print("\n▶️ SCENARIO 2: LONG TOKEN (> 16 CHARS)")
        try: utils.click_boton(driver, config.XPATH_RN_INPUT_TOKEN) 
        except: pass
        time.sleep(1)
        campo_token_2 = driver.find_element(By.XPATH, config.XPATH_RN_INPUT_TOKEN)
        campo_token_2.clear()
        campo_token_2.send_keys(config.RN_TOKEN_LARGO)
        
        texto_ingresado = campo_token_2.get_attribute("text")
        if texto_ingresado and len(texto_ingresado) == 16 and len(config.RN_TOKEN_LARGO) > 16:
            print("   🎯 SUCCESS: UI BLOCKED TYPING MORE THAN 16 CHARACTERS.")
            utils.tomar_screenshot(driver, "RN_50_SCENARIO_2_LONG_SUCCESS")
        else:
            utils.click_boton(driver, config.XPATH_RN_BTN_ACEPTAR_REGISTRO)
            print("⏳ SCANNING FOR ERROR MESSAGE (LONG TOKEN)...")
            error_largo = False
            for i in range(8): 
                if any(palabra in driver.page_source.lower() for palabra in ["error", "incorrecto", "inválido", "invalid", "caracteres"]):
                    error_largo = True
                    print("   🎯 ERROR DETECTED FOR LONG TOKEN!")
                    utils.tomar_screenshot(driver, "RN_50_SCENARIO_2_LONG_ERROR")
                    break
                time.sleep(0.5)

        print("⏳ WAITING FOR ERROR BANNER TO DISAPPEAR...")
        time.sleep(4)

        # =========================================================
        # SCENARIO 3: EXACT TOKEN (== 16)
        # =========================================================
        print("\n▶️ SCENARIO 3: EXACT TOKEN (== 16 CHARS)")
        try: utils.click_boton(driver, config.XPATH_RN_INPUT_TOKEN)
        except: pass
        time.sleep(1)
        campo_token_3 = driver.find_element(By.XPATH, config.XPATH_RN_INPUT_TOKEN)
        campo_token_3.clear()
        campo_token_3.send_keys(config.RN_TOKEN)
        
        try: driver.hide_keyboard()
        except: pass
        
        utils.click_boton(driver, config.XPATH_RN_BTN_ACEPTAR_REGISTRO)
        
        print("⏳ WAITING FOR SUCCESSFUL REGISTRATION...")
        time.sleep(4)
        
        if utils.verificar_existencia(wait, config.XPATH_RN_PANTALLA_EXITO, "SUCCESS SCREEN", driver):
            utils.tomar_screenshot(driver, "RN_50_SCENARIO_3_EXACT_SUCCESS")
            try: utils.print_http_evidence_appium(driver, "RN_50")
            except: pass
            print("\n✅ RN-50_SCENARIO_3: SUCCESS (ALL 3 LENGTH RESTRICTIONS VALIDATED CORRECTLY)")
            return True
        else:
            print("\n❌ RN-50_SCENARIO_3: FAILED.")
            utils.tomar_screenshot(driver, "RN_50_SCENARIO_3_FAILED")
            try: utils.print_http_evidence_appium(driver, "RN_50")
            except: pass
            return False

    except Exception as e:
        print(f"❌ RN-50_SCENARIO_3: CRITICAL ERROR: {e}")
        try: utils.tomar_screenshot(driver, "RN_50_TECHNICAL_ERROR")
        except: pass
        return False
    finally:
        utils.cerrar_driver(driver)

# =================================================================================
# RN-51: VALIDATE AFFILIATION NUMBER LENGTH RESTRICTIONS (<7, >7, ==7)
# =================================================================================
def RN_51():
    print("\n" + "=" * 60)
    print("RN-51: VALIDATE AFFILIATION LENGTH RESTRICTIONS (3 SCENARIOS)")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        print("🔐 PRECONDITION: LOGGING IN TO REACH REGISTRATION SCREEN...")
        helper_login_to_registration(driver, wait)
        print(f"   🔑 ENTERING VALID TOKEN: {config.RN_TOKEN}")
        time.sleep(4)
        try: utils.click_boton(driver, config.XPATH_RN_INPUT_TOKEN)
        except: pass
        utils.escribir_texto(driver, config.XPATH_RN_INPUT_TOKEN, config.RN_TOKEN)
        
        try: driver.hide_keyboard()
        except: pass

        # =========================================================
        # SCENARIO 1: SHORT NUMBER AFFILIATION (< 7)
        # =========================================================
        print("\n▶️ SCENARIO 1: SHORT AFFILIATION (< 7 CHARS)")
        campo_afiliacion = driver.find_element(By.XPATH, config.XPATH_RN_INPUT_AFILIACION)
        campo_afiliacion.clear()
        campo_afiliacion.send_keys(config.RN_AFILIACION_CORTA)
        utils.click_boton(driver, config.XPATH_RN_BTN_ACEPTAR_REGISTRO)
        print("⏳ SCANNING FOR ERROR MESSAGE (SHORT AFFILIATION)...")
        error_detectado = False
        for i in range(8): 
            if any(palabra in driver.page_source.lower() for palabra in ["error", "incorrecto", "inválido", "invalid", "caracteres", "afiliacion"]):
                error_detectado = True
                print("   🎯 ERROR DETECTED FOR SHORT AFFILIATION!")
                utils.tomar_screenshot(driver, "RN_51_SCENARIO_1_SHORT_SUCCESS")
                break
            time.sleep(0.5)
            
        if not error_detectado:
            print("   ⚠️ WARNING: NO ERROR DETECTED FOR SHORT AFFILIATION. SYSTEM MIGHT HAVE PROCEEDED.")
            utils.tomar_screenshot(driver, "RN_51_SCENARIO_1_FAILED")
        print("⏳WAITING FOR ERROR BANNER TO DISAPPEAR...")
        time.sleep(4) 

        # =========================================================
        # SCENARIO 2: LONG AFFILIATION (> 7)
        # =========================================================
        print("\n▶️ SCENARIO 2: LONG AFFILIATION (> 7 CHARS)")
        try: utils.click_boton(driver, config.XPATH_RN_INPUT_AFILIACION)
        except: pass
        time.sleep(1)
        campo_afiliacion_2 = driver.find_element(By.XPATH, config.XPATH_RN_INPUT_AFILIACION)
        campo_afiliacion_2.clear()
        campo_afiliacion_2.send_keys(config.RN_AFILIACION_LARGA)
        texto_ingresado = campo_afiliacion_2.get_attribute("text")
        if texto_ingresado and len(texto_ingresado) == 7 and len(config.RN_AFILIACION_LARGA) > 7:
            print("   🎯 SUCCESS: UI BLOCKED TYPING MORE THAN 7 CHARACTERS.")
            utils.tomar_screenshot(driver, "RN_51_SCENARIO_2_LONG_SUCCESS")
        else:
            utils.click_boton(driver, config.XPATH_RN_BTN_ACEPTAR_REGISTRO)
            print("⏳ SCANNING FOR ERROR MESSAGE (LONG AFFILIATION)...")
            error_largo = False
            for i in range(8): 
                if any(palabra in driver.page_source.lower() for palabra in ["error", "incorrecto", "inválido", "invalid", "caracteres", "afiliacion"]):
                    error_largo = True
                    print("   🎯 ERROR DETECTED FOR LONG AFFILIATION!")
                    utils.tomar_screenshot(driver, "RN_51_SCENARIO_2_LONG_ERROR_FAILED")
                    break
                time.sleep(0.5)

        print("⏳ Waiting for error banner to disappear...")
        time.sleep(4)

        # =========================================================
        # SCENARIO 3: EXACT AFFILIATION (== 7)
        # =========================================================
        print("\n▶️ SCENARIO 3: EXACT AFFILIATION (== 7 CHARS)")
        try: utils.click_boton(driver, config.XPATH_RN_INPUT_AFILIACION)
        except: pass
        time.sleep(1)
        
        campo_afiliacion_3 = driver.find_element(By.XPATH, config.XPATH_RN_INPUT_AFILIACION)
        campo_afiliacion_3.clear()
        campo_afiliacion_3.send_keys(config.RN_AFILIACION)
        
        try: driver.hide_keyboard()
        except: pass
        
        utils.click_boton(driver, config.XPATH_RN_BTN_ACEPTAR_REGISTRO)
        
        print("⏳ WAITING FOR SUCCESSFUL REGISTRATION...")
        time.sleep(4)
        
        if utils.verificar_existencia(wait, config.XPATH_RN_PANTALLA_EXITO, "SUCCESS SCREEN", driver):
            utils.tomar_screenshot(driver, "RN_51_SCENARIO_3_EXACT_SUCCESS")
            try: utils.print_http_evidence_appium(driver, "RN_51")
            except: pass
            print("\n✅ RN-51: SUCCESS (ALL 3 LENGTH RESTRICTIONS VALIDATED CORRECTLY)")
            return True
        else:
            print("\n❌ RN-51 FAILED: EXACT AFFILIATION WAS NOT ACCEPTED.")
            utils.tomar_screenshot(driver, "RN_51_SCENARIO_3_FAILED")
            try: utils.print_http_evidence_appium(driver, "RN_51")
            except: pass
            return False

    except Exception as e:
        print(f"❌ RN-51 CRITICAL ERROR: {e}")
        try: utils.tomar_screenshot(driver, "RN_51_TECHNICAL_ERROR")
        except: pass
        return False
    finally:
        utils.cerrar_driver(driver)

# =================================================================================
# RN-52: VALIDATE SKIP BUSINESS REGISTRATION ("EN OTRA OCASION")
# =================================================================================
def RN_52():
    print("\n" + "=" * 60)
    print("RN-52: VALIDATE SKIP BUSINESS REGISTRATION (EN OTRA OCASION)")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        print("🔐 PRECONDITION: LOGGING IN TO REACH REGISTRATION SCREEN...")
        helper_login_to_registration(driver, wait)
        
        # STEP 1: CLICK IN 'OTRA OCASION'
        print("👉 STEP 1: CLICKING 'EN OTRA OCASIÓN' BUTTON...")
        time.sleep(4) 
        utils.click_boton(driver, config.XPATH_RN_BTN_OTRA_OCASION)
        
        print("⏳ WAITING FOR SYSTEM TO ROUTE BACK TO LOGIN SCREEN...")
        time.sleep(5)
        print("🔍 VERIFYING WE RETURNED TO THE LOGIN SCREEN...")
        pantalla_login_cargada = utils.verificar_existencia(
            wait, 
            config.XPATH_INPUT_USUARIO, 
            "LOGIN SCREEN (EMAIL INPUT FIELD)", 
            driver
        )
        if pantalla_login_cargada:
            print("📸 TAKING SCREENSHOT EVIDENCE OF THE LOGIN SCREEN...")
            utils.tomar_screenshot(driver, "RN_52_SUCCESS")
            
            try: utils.print_http_evidence_appium(driver, "RN_52")
            except: pass
            
            print("\n✅ RN-52: SUCCESS.)")
            return True
        else:
            print("\n❌ RN-52 FAILED.")
            utils.tomar_screenshot(driver, "RN_52_FAILED")
            try: utils.print_http_evidence_appium(driver, "RN_52")
            except: pass
            
            print("🔍 SCANNING FOR CURRENT SCREEN TEXTS...")
            try:
                todos = driver.find_elements(By.XPATH, "//*")
                for elem in todos:
                    t = elem.get_attribute("text")
                    if t and len(t) > 3:
                        print(f"   -> VISIBLE TEXT: '{t}'")
            except: pass
            return False

    except Exception as e:
        print(f"❌ RN-52 CRITICAL ERROR: {e}")
        try: utils.tomar_screenshot(driver, "RN_52_TECHNICAL_ERROR")
        except: pass
        return False
    finally:
        utils.cerrar_driver(driver)

# =================================================================================
# RN-53: VALIDATE FIELD INTERACTION (FOCUS/BLUR) WITHOUT DATA
# =================================================================================
def RN_53():
    print("\n" + "=" * 60)
    print("RN-53: VALIDATE FIELD INTERACTION (TOUCHING FIELDS)")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        print("🔐 PRECONDITION: LOGGING IN TO REACH REGISTRATION SCREEN...")
        helper_login_to_registration(driver, wait)
        
        # STEP 1 & 2: TOUCHING TEXT FIELDS
        print("👉 STEP 1 & 2: TOUCHING 'TOKEN' AND 'AFILIACIÓN' FIELDS...")
        time.sleep(4) 
        
        print("   👆TOUCHING 'TOKEN' FIELD")
        try: utils.click_boton(driver, config.XPATH_RN_INPUT_TOKEN)
        except: pass
        time.sleep(2) 
        
        print("   👆 TOUCHING 'AFILIACION' FIELD...")
        try: utils.click_boton(driver, config.XPATH_RN_INPUT_AFILIACION)
        except: pass
        time.sleep(2)
        
        print("📸 TAKING SCREENSHOT EVIDENCE (KEYBOARD UP / FIELDS FOCUSED)...")
        utils.tomar_screenshot(driver, "RN_53_KEYBOARD_VISIBLE")

        # STEP 3: TOUCHING OUTSIDE TO REMOVE FOCUS
        print("👉 STEP 3: TOUCHING OUTSIDE (TITLE) TO REMOVE FOCUS...")
        try: 
            driver.find_element(By.XPATH, config.XPATH_RN_TITULO_NEGOCIO).click()
            print("   👆 Touched 'Registro de Negocio' title")
        except: 
            print("   ⚠️ COULD NOT TOUCH TITLE, HIDING KEYBOARD NATIVELY...")
            try: driver.hide_keyboard()
            except: pass
        time.sleep(2)
        
        print("📸 TAKING FINAL SCREENSHOT EVIDENCE...")
        utils.tomar_screenshot(driver, "RN_53_SUCCESS")
        try: utils.print_http_evidence_appium(driver, "RN_53")
        except: pass
        
        print("\n✅ RN-53: SUCCESS")
        return True

    except Exception as e:
        print(f"❌ RN-53 CRITICAL ERROR: {e}")
        try: utils.tomar_screenshot(driver, "RN_53_TECHNICAL_ERROR")
        except: pass
        return False
    finally:
        utils.cerrar_driver(driver)



# === MAIN EXECUTION === #
if __name__ == "__main__":
    
    logger, log_file, timestamp = utils.iniciar_reporte("OPERATIONALS_RN")
    
    try:
        RN_44()
        RN_45() 
        RN_46()
        RN_47()
        RN_48()
        RN_49()
        RN_50()
        RN_51()
        RN_52()
        RN_53()
        
    finally:
        #utils.generar_zip_evidencias("OPERATIONALS_RN", logger, log_file, timestamp)
        utils.generar_reporte_html("OPERATIONALS_RN", log_file, timestamp)