"""
FILENAME: Operationals_RA.py
DESCRIPTION:
    VALIDATE REGISTRATION PROCESS. 
CONTENTS:
    · TEST 1: ACCESS TO REGISTRATION SCREEN.
    · TEST 2: SUCCESSFUL USER REGISTRATION.
    · TEST 3: VALIDATION OF EMPTY FIELDS.
""" 

import sys
import os
ruta_proyecto = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ruta_proyecto not in sys.path:
    sys.path.append(ruta_proyecto)
import time
import config
import utils
import T6.Operationals_LG 

# ====================================== 
# TEST 1: ACCESS TO REGISTRATION SCREEN  
# ====================================== 
def test_1_acceso_pantalla():
    print("\n" + "=" * 60)
    print("TEST 1: ACCESS TO REGISTRATION SCREEN")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        
        print("👉 OPERACIONALES_LG FILE...")
        login_exitoso = T6.Operationals_LG.realizar_login(driver, wait)

        if not login_exitoso:
            raise Exception("LOGIN FAILED.")

        time.sleep(3) 

        
        print("👉 VALIDATION OF REGISTRATION SCREEN...")
        
        check_token = utils.verificar_existencia(wait, config.XPATH_TXT_TOKEN_REGISTRO, "Campo Token")
        check_afiliacion = utils.verificar_existencia(wait, config.XPATH_TXT_NUM_AFILIACION, "Campo Afiliación")
        
        if check_token and check_afiliacion:
            print("\n✅ SUCCESS: REGISTRATION SCREEN LOADED CORRECTLY")
        else:
            print("\n❌ ERROR: REGISTRATION SCREEN NOT LOADED")

    except Exception as e:
        print(f"❌ CRITICAL ERROR IN TEST 1: {e}")
    finally:
        utils.cerrar_driver(driver)


# ========================================== #
# TEST 2: SUCCESSFUL USER REGISTRATION  
# ========================================== #
def test_2_registro_exitoso():
    print("\n" + "=" * 60)
    print("TEST 2: SUCCESSFUL USER REGISTRATION")
    print("=" * 60)
    driver, wait = utils.iniciar_driver()
    
    try:
        # --- LOGIN --- #
        print("OPERACIONALES_LG FILE...")
        login_exitoso = T6.Operacionales_LG.realizar_login(driver, wait)
        if not login_exitoso:
            raise Exception("LOGIN FAILED. ABORTING TEST.")

        time.sleep(4) 
        print("\n📋 VALIDATION OF REGISTRATION SCREEN...")
        if not utils.verificar_existencia(wait, config.XPATH_TXT_TOKEN_REGISTRO, "Registration Screen", driver):
            return False
        print("WRITING TOKEN...")
        utils.click_boton(driver, config.XPATH_TXT_TOKEN_REGISTRO) 
        time.sleep(1)
        utils.escribir_texto(driver, config.XPATH_TXT_TOKEN_REGISTRO, config.TOKEN_REGISTRO)
        try: driver.hide_keyboard()
        except: pass
        print("WRITING AFILIATION...")
        utils.click_boton(driver, config.XPATH_TXT_NUM_AFILIACION)
        time.sleep(1)
        utils.escribir_texto(driver, config.XPATH_TXT_NUM_AFILIACION, config.NUMERO_AFILIACION)
        print("ENSURE KEYBOARD IS CLOSED...")
        try: driver.hide_keyboard()
        except: pass
        time.sleep(1) 
        print("LOOKING FOR ACCEPT BUTTON...")
        if utils.verificar_existencia(wait, config.XPATH_BTN_ACEPTAR_REGISTRO, "Accept Button", driver):
            print("CLICKING ACCEPT BUTTON...")
            utils.click_boton(driver, config.XPATH_BTN_ACEPTAR_REGISTRO)
            time.sleep(5) 
            print("\n✅ SUCCESS: ACCEPT BUTTON CLICKED")
            return True
        else:
            print("\n❌ ERROR: ACCEPT BUTTON NOT FOUND")
            return False

    except Exception as e:
        print(f"\n❌ CRITICAL ERROR IN TEST 2: {e}")
        return False
    finally:
        utils.cerrar_driver(driver)

# ==========================================
# TEST 3: VALIDATION OF EMPTY FIELDS
# ==========================================
def test_3_campos_vacios():
    print("\n" + "=" * 60)
    print("TEST 3: VALIDATION OF EMPTY FIELDS")
    print("=" * 60)
    
    driver, wait = utils.iniciar_driver()
    
    try:
        print("OPERACIONALES_LG FILE...")
        login_exitoso = T6.Operationals_LG.realizar_login(driver, wait)

        if not login_exitoso:
            raise Exception("LOGIN FAILED.")

        time.sleep(4) 
        print("📋 REGISTRATION SCREEN LOADED.")
        print("👉 TRYING TO PRESS 'ACCEPT' WITHOUT ENTERING DATA...")

        try: driver.hide_keyboard()
        except: pass
        
        if utils.verificar_existencia(wait, config.XPATH_BTN_ACEPTAR_REGISTRO, "Botón Aceptar", driver):
            utils.click_boton(driver, config.XPATH_BTN_ACEPTAR_REGISTRO)
        else:
            print("❌ ACCEPT BUTTON NOT FOUND")  
        
        time.sleep(2) 
        
        error_detectado = utils.verificar_existencia(wait, config.XPATH_ERROR_GENERICO, "Error Message/Alert", driver, timeout=3)
        seguimos_en_registro = utils.verificar_existencia(wait, config.XPATH_TXT_TOKEN_REGISTRO, "Token Field (Original Screen)", driver, timeout=3)

        if error_detectado:
            print("\n✅ SUCCESS: ERROR MESSAGE DISPLAYED.")
            return True
        elif seguimos_en_registro:
            print("\n✅ SUCCESS: SYSTEM BLOCKED ADVANCEMENT (STILL ON REGISTRATION SCREEN).")
            return True
        else:
            print("\n❌ FAILURE: SYSTEM ALLOWED ADVANCEMENT WITH EMPTY FIELDS.")
            return False

    except Exception as e:
        print(f"✅ SUCCESS IN TEST 3: {e}")
        return False
    finally:
        utils.cerrar_driver(driver)
                
# === EXECUTION === #
if __name__ == "__main__":
    test_1_acceso_pantalla()
    test_2_registro_exitoso()
    test_3_campos_vacios()