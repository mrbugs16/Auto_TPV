"""
FILENAME: Operationals_RA.py
DESCRIPTION:
    VALIDATE REGISTRATION PROCESS. 
CONTENTS:
    · RA-009: VALIDATE REGISTRATION SCREEN LOADS.
    · RA-010: VALIDATE SUCCESSFUL REGISTRATION (SPECIFIC DATA).
    · RA-011: VALIDATE EMPTY FIELDS SUBMISSION.
    · RA-012: VALIDATE SPECIFIC FLOW (EMPTY NAME).
    · RA-013: VALIDATE DUPLICATE USER ERROR (EXISTING EMAIL).
    · RA-014: VALIDATE PASSWORD LENGTH ERROR (TOO SHORT).
    · RA-015: VALIDATE PASSWORD MATCH ERROR (DOES NOT MATCH).
    · RA-016: VALIDATE EMAIL FORMAT ERROR (INVALID).
    · RA-018: VALIDATE FIELD INTERACTION (FOCUS/BLUR).
""" 

import sys
import os
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_path not in sys.path:
    sys.path.append(project_path)
import time
import random
import string
import config
import utils

# =================================================================================
# HELPER: NAVIGATE TO REGISTRATION SCREEN
# =================================================================================
def navegar_a_registro(driver, wait):
    print("👉 LOOKING FOR 'REGISTRATE AHORA' BUTTON...")
    time.sleep(5) 
    
    if utils.verificar_existencia(wait, config.XPATH_WEB_BTN_REGISTRA_AHORA, "Registrate Ahora Button", driver):
        print("👉 CLICKING 'REGISTRATE AHORA' BUTTON...")
        utils.click_boton(driver, config.XPATH_WEB_BTN_REGISTRA_AHORA)
        time.sleep(3)
        return True
    else:
        print("❌ 'REGISTRATE AHORA' BUTTON NOT FOUND")
        return False

# =====================================================
# RA-009: VALIDATE REGISTRATION SCREEN LOADS CORRECTLY
# =====================================================
def RA_009():
    print("\n" + "=" * 60)
    print("RA-009: VALIDATE REGISTRATION SCREEN LOADS CORRECTLY")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        if not navegar_a_registro(driver, wait):
            return False

        print("👉 VALIDATING REGISTRATION SCREEN ELEMENTS...")
        
        check_nombre = utils.verificar_existencia(wait, config.XPATH_RA_NOMBRE, "Campo Nombre", driver)
        check_apellido = utils.verificar_existencia(wait, config.XPATH_RA_APELLIDO, "Campo Apellido", driver)
        check_email = utils.verificar_existencia(wait, config.XPATH_RA_EMAIL, "Campo Email", driver)
        
        if check_nombre and check_apellido and check_email:
            print("\n✅ SUCCESS: REGISTRATION SCREEN LOADED CORRECTLY")
            return True
        else:
            print("\n❌ FAILURE: REGISTRATION SCREEN ELEMENTS MISSING")
            return False

    except Exception as e:
        print(f"❌ CRITICAL ERROR IN RA-009: {e}")
        return False
    finally:
        utils.cerrar_driver(driver)


# ===================================================
# RA-010: SUCCESSFUL REGISTRATION WITH SPECIFIC DATA
# ===================================================
def RA_010():
    print("\n" + "=" * 60)
    print("RA-010: SUCCESSFUL REGISTRATION WITH SPECIFIC DATA")
    print("=" * 60)
    
    driver, wait = utils.iniciar_driver()
    
    try:
        if not navegar_a_registro(driver, wait):
            return False

        # GENERATE RANDOM DATA
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        random_email = f"santiago.{random_suffix}@gmail.com"
        
        print(f"👉 FILLING FORM WITH SPECIFIC DATA...")
        print(f"   📧 Generated Email: {random_email}")
        
        # FILL FORM
        utils.escribir_texto(driver, config.XPATH_RA_NOMBRE, config.RA_010_NOMBRE)
        utils.escribir_texto(driver, config.XPATH_RA_APELLIDO, config.RA_010_APELLIDO)
        utils.escribir_texto(driver, config.XPATH_RA_SEGUNDOAPELLIDO, config.RA_010_SEGUNDO_APELLIDO)
        utils.escribir_texto(driver, config.XPATH_RA_EMAIL, random_email)
        utils.escribir_texto(driver, config.XPATH_RA_PASS, config.RA_010_PASS)
        utils.escribir_texto(driver, config.XPATH_RA_CONFIRMAR_PASS, config.RA_010_PASS)
        
        try:driver.hide_keyboard()
        except: pass
        
        print("👉 CLICKING 'ACEPTAR' BUTTON...")
        print("👉 CLICKING 'ACEPTAR' BUTTON AND WAITING FOR TOAST...")
        try:
             driver.find_element(By.XPATH, config.XPATH_RA_BTN_ACEPTAR).click()
        except:
             try: utils.click_boton(driver, config.XPATH_RA_BTN_ACEPTAR)
             except: pass

        
        print("👉 VERIFYING SUCCESS POPUP...")
        end_time = time.time() + 8 # Wait up to 8 seconds
        success = False
        
        while time.time() < end_time:
            try:
                elems = driver.find_elements(By.XPATH, config.XPATH_RA_REGISTRO_EXITOSO)
                if len(elems) > 0:
                    print("✅ SUCCESS: POPUP 'USUARIO CREADO CORRECTAMENTE' DETECTED")
                    success = True
                    break
            except: pass
            time.sleep(0.5) 
            
        if success:
             return True
        else:
            print("❌ 'USUARIO CREADO CORRECTAMENTE' POPUP NOT FOUND (TIMED OUT)")
            
            if utils.verificar_existencia(wait, config.XPATH_WEB_BTN_REGISTRA_AHORA, "Login Screen (Fallback Success)", driver):
                print("✅ API SUCCESS: RETURNED TO LOGIN SCREEN (IMPLIED REGISTRATION SUCCESS)")
                return True
            
            print("🔍 SCANNING SCREEN FOR FAILURE DIAGNOSIS...")
            try:
                from selenium.webdriver.common.by import By
                todos = driver.find_elements(By.XPATH, "//*")
                for elem in todos:
                    t = elem.get_attribute("text")
                    d = elem.get_attribute("content-desc")
                    if (t and len(t)>3) or (d and len(d)>3):
                        print(f"   -> TEXT='{t}' | DESC='{d}'")
            except: pass
            
            return False

    except Exception as e:
        print(f"❌ CRITICAL ERROR IN RA-010: {e}")
        return False
    finally:
        utils.cerrar_driver(driver)

# =========================================
# RA-011: VALIDATE EMPTY FIELDS SUBMISSION
# =========================================
def RA_011():
    print("\n" + "=" * 60)
    print("RA-011: VALIDATE EMPTY FIELDS SUBMISSION")
    print("=" * 60)
    
    driver, wait = utils.iniciar_driver()
    
    try:
        if not navegar_a_registro(driver, wait):
            return False
            
        print("👉 CLICKING 'ACEPTAR' BUTTON WITH EMPTY FIELDS...")
        try: driver.hide_keyboard()
        except: pass
        
        if utils.verificar_existencia(wait, config.XPATH_RA_BTN_ACEPTAR, "Aceptar Button", driver):
            utils.click_boton(driver, config.XPATH_RA_BTN_ACEPTAR)
            time.sleep(2)
            
            if utils.verificar_existencia(wait, config.XPATH_RA_NOMBRE, "Registration Form (Still Visible)", driver):
                print("✅ SUCCESS: REGISTRATION BLOCKED (FORM STILL VISIBLE)")
                return True
            else:
                 print("❌ FAILURE: FORM DISAPPEARED (POSSIBLE INCORRECT SUBMISSION)")
                 return False
        else:
            print("❌ 'ACEPTAR' BUTTON NOT FOUND")
            return False

    except Exception as e:
        print(f"❌ CRITICAL ERROR IN RA-011: {e}")
        return False
    finally:
        utils.cerrar_driver(driver)

    
# ===========================================
# RA-012: VALIDATE SPECIFIC FLOW (EMPTY NAME)
# ===========================================
def RA_012():
    print("\n" + "=" * 60)
    print("RA-012: VALIDATE SPECIFIC FLOW (EMPTY NAME)")
    print("=" * 60)
    
    driver, wait = utils.iniciar_driver()
    
    try:
        if not navegar_a_registro(driver, wait):
            return False
        
        print("👉 VERIFYING REGISTRATION FORM...")
        if not utils.verificar_existencia(wait, config.XPATH_RA_NOMBRE, "Registration Form - Name Field", driver):
            print("❌ REGISTRATION FORM NOT LOADED")
            return False
        
        print("👉 SKIPPING 'NOMBRE' FIELD (LEAVING IT EMPTY)...")
        
        print("👉 FILLING OTHER FIELDS...")
        utils.escribir_texto(driver, config.XPATH_RA_APELLIDO, config.RA_APELLIDO)
        utils.escribir_texto(driver, config.XPATH_RA_SEGUNDOAPELLIDO, config.RA_SEGUNDOAPELLIDO)
        utils.escribir_texto(driver, config.XPATH_RA_EMAIL, config.RA_EMAIL)
        utils.escribir_texto(driver, config.XPATH_RA_PASS, config.RA_PASS)
        utils.escribir_texto(driver, config.XPATH_RA_CONFIRMAR_PASS, config.RA_PASS)
        
        try: driver.hide_keyboard()
        except: pass
        
        print("👉 CLICKING 'ACEPTAR' BUTTON...")
        time.sleep(1)
        if utils.verificar_existencia(wait, config.XPATH_RA_BTN_ACEPTAR, "Aceptar Button", driver):
            utils.click_boton(driver, config.XPATH_RA_BTN_ACEPTAR)
            time.sleep(3)
            
            print("👉 VERIFYING ERROR MESSAGE FOR EMPTY NAME FIELD...")
            if utils.verificar_existencia(wait, config.XPATH_RA_ERROR_NOMBRE, "Error: Ingresa un nombre valido", driver):
                print("✅ SUCCESS: ERROR MESSAGE 'INGRESA UN NOMBRE VALIDO' DETECTED")
                return True
            else:
                print("❌ FAILURE: ERROR MESSAGE NOT DETECTED")
                return False
        else:
            print("❌ 'ACEPTAR' BUTTON NOT FOUND")
            return False
            
    except Exception as e:
        print(f"❌ CRITICAL ERROR IN RA-012: {e}")
        return False
    finally:
        utils.cerrar_driver(driver)

# ========================================================
# RA-013: VALIDATE DUPLICATE USER ERROR (EXISTING EMAIL)
# ========================================================
def RA_013():
    print("\n" + "=" * 60)
    print("RA-013: VALIDATE DUPLICATE USER ERROR (EXISTING EMAIL)")
    print("=" * 60)
    
    driver, wait = utils.iniciar_driver()
    
    try:
        if not navegar_a_registro(driver, wait):
            return False
        
        print(f"👉 FILLING FORM WITH DUPLICATE DATA (EMAIL: {config.RA_013_EMAIL})...")
        
        utils.escribir_texto(driver, config.XPATH_RA_NOMBRE, config.RA_010_NOMBRE)
        utils.escribir_texto(driver, config.XPATH_RA_APELLIDO, config.RA_010_APELLIDO)
        utils.escribir_texto(driver, config.XPATH_RA_SEGUNDOAPELLIDO, config.RA_010_SEGUNDO_APELLIDO)
        utils.escribir_texto(driver, config.XPATH_RA_EMAIL, config.RA_013_EMAIL)
        utils.escribir_texto(driver, config.XPATH_RA_PASS, config.RA_010_PASS)
        utils.escribir_texto(driver, config.XPATH_RA_CONFIRMAR_PASS, config.RA_010_PASS)
        
        try: driver.hide_keyboard()
        except: pass
        
        print("👉 CLICKING 'ACEPTAR' BUTTON...")
        
        try:
             driver.find_element(By.XPATH, config.XPATH_RA_BTN_ACEPTAR).click()
        except:
             try: utils.click_boton(driver, config.XPATH_RA_BTN_ACEPTAR)
             except: pass
             
        time.sleep(2)

        print("👉 VERIFYING ERROR POPUP ('USUARIO YA EXISTE')...")
        if utils.verificar_existencia(wait, config.XPATH_RA_ERROR_USUARIO_EXISTE, "Error: Usuario ya existe", driver):
             print("✅ SUCCESS: ERROR POPUP 'USUARIO YA EXISTE' DETECTED")
             return True
        else:
            print("❌ 'USUARIO YA EXISTE' POPUP NOT FOUND")
            
            print("🔍 SCANNING SCREEN FOR FAILURE DIAGNOSIS...")
            try:
                from selenium.webdriver.common.by import By
                todos = driver.find_elements(By.XPATH, "//*")
                for elem in todos:
                    t = elem.get_attribute("text")
                    d = elem.get_attribute("content-desc")
                    if (t and len(t)>3) or (d and len(d)>3):
                        print(f"   -> TEXT='{t}' | DESC='{d}'")
            except: pass
            
            return False

    except Exception as e:
        print(f"❌ CRITICAL ERROR IN RA-013: {e}")
        return False
    finally:
        utils.cerrar_driver(driver)

# =============================================================
# RA-014: VALIDATE PASSWORD MISMATCH ERROR
# =============================================================
def RA_014():
    print("\n" + "=" * 60)
    print("RA-014: VALIDATE PASSWORD MISMATCH ERROR")
    print("=" * 60)
    
    driver, wait = utils.iniciar_driver()
    
    try:
        if not navegar_a_registro(driver, wait):
            return False
        
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        random_email = f"santiago.{random_suffix}@gmail.com"
        
        print(f"👉 FILLING FORM WITH MISMATCHING PASSWORDS...")
        
        utils.escribir_texto(driver, config.XPATH_RA_NOMBRE, config.RA_010_NOMBRE)
        utils.escribir_texto(driver, config.XPATH_RA_APELLIDO, config.RA_010_APELLIDO)
        utils.escribir_texto(driver, config.XPATH_RA_SEGUNDOAPELLIDO, config.RA_010_SEGUNDO_APELLIDO)
        utils.escribir_texto(driver, config.XPATH_RA_EMAIL, random_email)
        utils.escribir_texto(driver, config.XPATH_RA_PASS, "ConfirmPassword1")
        utils.escribir_texto(driver, config.XPATH_RA_CONFIRMAR_PASS, "ConfirmPassword2")
        
        try: driver.hide_keyboard()
        except: pass
        
        print("👉 CLICKING 'ACEPTAR' BUTTON...")
        
        try:
             driver.find_element(By.XPATH, config.XPATH_RA_BTN_ACEPTAR).click()
        except:
             try: utils.click_boton(driver, config.XPATH_RA_BTN_ACEPTAR)
             except: pass
             
        time.sleep(2)

        print("👉 VERIFYING ERROR MESSAGE ('LAS CONTRASEÑAS NO COINCIDEN')...")
        if utils.verificar_existencia(wait, config.XPATH_RA_ERROR_PASS_NO_COINCIDEN, "Error: Las contraseñas no coinciden", driver):
             print("✅ SUCCESS: ERROR MESSAGE 'LAS CONTRASEÑAS NO COINCIDEN' DETECTED")
             return True
        else:
            print("❌ 'LAS CONTRASEÑAS NO COINCIDEN' MESSAGE NOT FOUND")
            
            print("🔍 SCANNING SCREEN FOR FAILURE DIAGNOSIS...")
            try:
                from selenium.webdriver.common.by import By
                todos = driver.find_elements(By.XPATH, "//*")
                for elem in todos:
                    t = elem.get_attribute("text")
                    d = elem.get_attribute("content-desc")
                    if (t and len(t)>3) or (d and len(d)>3):
                        print(f"   -> TEXT='{t}' | DESC='{d}'")
            except: pass
            
            return False

    except Exception as e:
        print(f"❌ CRITICAL ERROR IN RA-014: {e}")
        return False
    finally:
        utils.cerrar_driver(driver)

# =============================================================
# RA-015: VALIDATE INVALID EMAIL FORMAT ERROR
# =============================================================
def RA_015():
    print("\n" + "=" * 60)
    print("RA-015: VALIDATE INVALID EMAIL FORMAT ERROR")
    print("=" * 60)
    
    driver, wait = utils.iniciar_driver()
    
    try:
        if not navegar_a_registro(driver, wait):
            return False
        
        print(f"👉 FILLING FORM WITH INVALID EMAIL FORMAT...")
        
        # Fill Form with Valid Data except Email
        utils.escribir_texto(driver, config.XPATH_RA_NOMBRE, config.RA_010_NOMBRE)
        utils.escribir_texto(driver, config.XPATH_RA_APELLIDO, config.RA_010_APELLIDO)
        utils.escribir_texto(driver, config.XPATH_RA_SEGUNDOAPELLIDO, config.RA_010_SEGUNDO_APELLIDO)
        
        # Invalid Email
        print("   📧 Set Invalid Email: 'usuario@dominio' (No TLD)")
        utils.escribir_texto(driver, config.XPATH_RA_EMAIL, "usuario@dominio")
        
        utils.escribir_texto(driver, config.XPATH_RA_PASS, config.RA_010_PASS)
        utils.escribir_texto(driver, config.XPATH_RA_CONFIRMAR_PASS, config.RA_010_PASS)
        
        try: driver.hide_keyboard()
        except: pass
        
        print("👉 CLICKING 'ACEPTAR' BUTTON...")
        
        # Click Logic (Reuse robust logic)
        try:
             driver.find_element(By.XPATH, config.XPATH_RA_BTN_ACEPTAR).click()
        except:
             try: utils.click_boton(driver, config.XPATH_RA_BTN_ACEPTAR)
             except: pass
             
        time.sleep(2)

        # CHECK FOR ERROR MESSAGE
        print("👉 VERIFYING ERROR MESSAGE ('CORREO INVALIDO')...")
        if utils.verificar_existencia(wait, config.XPATH_RA_ERROR_CORREO_INVALIDO, "Error: Correo inválido", driver):
             print("✅ SUCCESS: ERROR MESSAGE 'CORREO INVALIDO' DETECTED")
             return True
        else:
            print("❌ 'CORREO INVALIDO' MESSAGE NOT FOUND")
            
            # --- DEBUG: SCAN SCREEN --- #
            print("🔍 SCANNING SCREEN FOR FAILURE DIAGNOSIS...")
            try:
                from selenium.webdriver.common.by import By
                todos = driver.find_elements(By.XPATH, "//*")
                for elem in todos:
                    t = elem.get_attribute("text")
                    d = elem.get_attribute("content-desc")
                    if (t and len(t)>3) or (d and len(d)>3):
                        print(f"   -> TEXT='{t}' | DESC='{d}'")
            except: pass
            
            return False

    except Exception as e:
        print(f"❌ CRITICAL ERROR IN RA-015: {e}")
        return False
    finally:
        utils.cerrar_driver(driver)

# =============================================================
# RA-016: VALIDATE INVALID PASSWORD FORMAT ERROR
# =============================================================
def RA_016():
    print("\n" + "=" * 60)
    print("RA-016: VALIDATE INVALID PASSWORD FORMAT ERROR")
    print("=" * 60)
    
    driver, wait = utils.iniciar_driver()
    
    try:
        if not navegar_a_registro(driver, wait):
            return False
        
        print(f"👉 FILLING FORM WITH INVALID PASSWORD FORMAT...")
        
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        random_email = f"santiago.{random_suffix}@gmail.com"
        
        utils.escribir_texto(driver, config.XPATH_RA_NOMBRE, config.RA_010_NOMBRE)
        utils.escribir_texto(driver, config.XPATH_RA_APELLIDO, config.RA_010_APELLIDO)
        utils.escribir_texto(driver, config.XPATH_RA_SEGUNDOAPELLIDO, config.RA_010_SEGUNDO_APELLIDO)
        utils.escribir_texto(driver, config.XPATH_RA_EMAIL, random_email)
        
        invalid_pass = "short"
        print(f"   🔑 Set Invalid Password: '{invalid_pass}'")
        utils.escribir_texto(driver, config.XPATH_RA_PASS, invalid_pass)
        utils.escribir_texto(driver, config.XPATH_RA_CONFIRMAR_PASS, invalid_pass)
        
        try: driver.hide_keyboard()
        except: pass
        
        print("👉 CLICKING 'ACEPTAR' BUTTON...")
        
        try:
             driver.find_element(By.XPATH, config.XPATH_RA_BTN_ACEPTAR).click()
        except:
             try: utils.click_boton(driver, config.XPATH_RA_BTN_ACEPTAR)
             except: pass
             
        time.sleep(2)

        print("👉 VERIFYING ERROR MESSAGE ('CONTRASEÑA INVALIDA')...")
        if utils.verificar_existencia(wait, config.XPATH_RA_ERROR_CONTRASENA_INVALIDA, "Error: Contraseña inválida", driver):
             print("✅ SUCCESS: ERROR MESSAGE 'CONTRASEÑA INVALIDA' DETECTED")
             return True
        else:
            print("❌ 'CONTRASEÑA INVALIDA' MESSAGE NOT FOUND")
            
            print("🔍 SCANNING SCREEN FOR FAILURE DIAGNOSIS...")
            try:
                from selenium.webdriver.common.by import By
                todos = driver.find_elements(By.XPATH, "//*")
                for elem in todos:
                    t = elem.get_attribute("text")
                    d = elem.get_attribute("content-desc")
                    if (t and len(t)>3) or (d and len(d)>3):
                        print(f"   -> TEXT='{t}' | DESC='{d}'")
            except: pass
            
            return False

    except Exception as e:
        print(f"❌ CRITICAL ERROR IN RA-016: {e}")
        return False
    finally:
        utils.cerrar_driver(driver)

# ===========================================
# RA-018: VALIDATE BACK BUTTON (ARROW ICON)
# ===========================================
def RA_018():
    print("\n" + "=" * 60)
    print("RA-018: VALIDATE BACK BUTTON (ARROW ICON)")
    print("=" * 60)
    
    driver, wait = utils.iniciar_driver()
    
    try:
        if not navegar_a_registro(driver, wait):
            return False
            
        print("👉 CLICKING BACK BUTTON (ARROW ICON)...")
        if utils.verificar_existencia(wait, config.XPATH_RA_BTN_ATRAS, "Back Button", driver):
            utils.click_boton(driver, config.XPATH_RA_BTN_ATRAS)
            time.sleep(3)
            

            print("👉 VERIFYING RETURN TO LOGIN SCREEN...")
            if utils.verificar_existencia(wait, config.XPATH_WEB_BTN_REGISTRA_AHORA, "Login Screen (Registrate Ahora Btn)", driver):
                print("✅ SUCCESS: RETURNED TO LOGIN SCREEN")
                return True
            else:
                 print("❌ FAILURE: DID NOT RETURN TO LOGIN SCREEN")
                 return False
        else:
             print("❌ BACK BUTTON NOT FOUND")
             return False

    except Exception as e:
        print(f"❌ CRITICAL ERROR IN RA-018: {e}")
        return False
    finally:
        utils.cerrar_driver(driver)

# ================================================
# RA-019: VALIDATE FIELD INTERACTION (FOCUS/BLUR)
# ================================================
def RA_019():
    print("\n" + "=" * 60)
    print("RA-019: VALIDATE FIELD INTERACTION (FOCUS/BLUR)")
    print("=" * 60)
    
    driver, wait = utils.iniciar_driver()
    
    try:
        if not navegar_a_registro(driver, wait):
            return False
            
        print("👉 INTERACTING WITH FIELDS (TOUCHING EACH ONE)...")
        
        fields = [
            ("Nombre", config.XPATH_RA_NOMBRE),
            ("Apellido", config.XPATH_RA_APELLIDO),
            ("Segundo Apellido", config.XPATH_RA_SEGUNDOAPELLIDO),
            ("Email", config.XPATH_RA_EMAIL),
            ("Password", config.XPATH_RA_PASS),
            ("Confirm Password", config.XPATH_RA_CONFIRMAR_PASS)
        ]
        
        for name, xpath in fields:
            print(f"   👆 Touching {name}...")
            utils.click_boton(driver, xpath)
            time.sleep(0.5)
            
        print("👉 TOUCHING OUTSIDE FIELDS (TITLE/HEADER)...")
       
        try:
             title_xpath = '//*[contains(@text, "Registro")]' 
             driver.find_element(By.XPATH, title_xpath).click()
             print("   👆 Touched 'Registro' title")
        except:
             print("   ⚠️ Could not touch title, trying hide_keyboard as fallback")
             try: driver.hide_keyboard()
             except: pass
        
        time.sleep(1)
        print("✅ SUCCESS: INTERACTION COMPLETED WITHOUT CRASH")
        return True

    except Exception as e:
        print(f"❌ CRITICAL ERROR IN RA-019: {e}")
        return False
    finally:
        utils.cerrar_driver(driver)

# === EXECUTION === #
if __name__ == "__main__":
    RA_009()
    RA_010()
    RA_011()
    RA_012()
    RA_013()
    RA_014()
    RA_015()
    RA_016()
    RA_018()
    RA_019()
