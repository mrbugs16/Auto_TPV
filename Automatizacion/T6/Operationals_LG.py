"""
FILENAME: Operationals_LG.py
DESCRIPTION:
    Automated test suite focused on the LOGIN (Authentication) module.
    Executes critical access validations on the POS terminal.

TEST CASES COVERED:
    · TEST 1: LOG IN WITH VALID CREDENTIALS.
    · TEST 2: INCORRECT PASSWORD VALIDATION.
    · TEST 4: UNREGISTERED USER VALIDATION.

REQUIREMENTS:
    - Requires config.py and utils.py in the same directory.
"""

import sys 
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time
import config
import utils
from selenium.webdriver.common.by import By

# ============================ #
# CALLING FUNCTION LOGIN 
# ============================ #
def realizar_login(driver, wait):

    """
    AUXILIARY FUNCTION TO PERFORM ONLY THE LOGIN STEPS.
    IT CAN BE CALLED FROM OTHER SCRIPTS.
    """
    print("RUNNING LOGIN FROM SHARED MODULE");
    try :
        utils.escribir_texto(driver, config.XPATH_INPUT_USUARIO, config.USUARIO_VALIDO)
        utils.escribir_texto(driver, config.XPATH_INPUT_PASS, config.PASS_VALIDO)
        driver.hide_keyboard()
        utils.click_boton(driver, config.XPATH_BTN_ACEPTAR)

        time.sleep(4)
        print(" ✅ SHARE LOGIN SUCCESSFUL");
        return True
    except Exception as e:
        print(f"❌ ERROR SHARE LOGIN: {e}")
        return False


# =============================================== #
# TEST 1: LOG IN WITH VALID CREDENTIALS 
# =============================================== #
def test_1_login_exitoso():
    print("\n" + "=" * 60)
    print("TEST 1: LOG IN WITH VALID CREDENTIALS")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        time.sleep(3)
        utils.escribir_texto(driver, config.XPATH_INPUT_USUARIO, config.USUARIO_VALIDO)
        utils.escribir_texto(driver, config.XPATH_INPUT_PASS, config.PASS_VALIDO)
        driver.hide_keyboard()
        utils.click_boton(driver, config.XPATH_BTN_ACEPTAR)

        # === WE SUCCESSFULLY VALIDATED === #
        if utils.verificar_existencia(wait, config.XPATH_INPUT_USUARIO, "NEXT SCREEN"):
            print("✅ SUCCESSFUL LOGIN")

    except Exception as e:
        print(f"❌ TEST FAILURE 1: {e}")
    finally:
        utils.cerrar_driver(driver)


# ================================================ #
# TEST 2: INCORRECT PASSWORD VALIDATION 
# ================================================ #
def test_2_pass_incorrecto():
    print("\n" + "=" * 60)
    print("TEST 2: INCORRECT PASSWORD VALIDATION")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        time.sleep(3)
        utils.escribir_texto(driver, config.XPATH_INPUT_USUARIO, config.USUARIO_VALIDO)
        utils.escribir_texto(driver, config.XPATH_INPUT_PASS, config.PASS_INVALIDO)
        driver.hide_keyboard()
        utils.click_boton(driver, config.XPATH_BTN_ACEPTAR)

        # === VALIDATE THE ERROR === #
        if utils.verificar_existencia(wait, config.XPATH_ERROR_GENERICO, "ERROR MESSAGE", driver):
            print("✅ CREDENTIAL ERROR DETECTED ")
        else:
            print("❌ VISUAL FAILURE")

    except Exception as e:
        print(f"❌ TEST FAILURE 2 {e}")
    finally:
        utils.cerrar_driver(driver)

# =============================================== #
# TEST 4: UNREGISTERED USER VALIDATION 
# =============================================== #
def test_4_usuario_no_registrado():
    print("\n" + "=" * 60)
    print("TEST 4: UNREGISTERED USER VALIDATION ")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        time.sleep(3)
        print("⌨️ ENTERING FALSE CREDENTIALS...")
        utils.escribir_texto(driver, config.XPATH_INPUT_USUARIO, config.USUARIO_INVALIDO)
        utils.escribir_texto(driver, config.XPATH_INPUT_PASS, config.PASS_VALIDO)
        driver.hide_keyboard()

        print("👆 BY CLICKING ACCEPT...")
        utils.click_boton(driver, config.XPATH_BTN_ACEPTAR)

        print("⏳ WAITING 6 SECONDS FOR THE ERROR... ")
        time.sleep(6)

        # === SCREEN SCANNER === #
        print("\n🔍 SCANNING THE SCREEN FOR ERRORS...")
        #
        todos_elementos = driver.find_elements(By.XPATH, "//*")

        encontrado = False
        mensajes_vistos = []

        for e in todos_elementos:
            try:

                t_text = e.get_attribute("text")
                t_desc = e.get_attribute("content-desc")

                
                if t_text or t_desc:

                    txt_log = t_text if t_text else "null"
                    desc_log = t_desc if t_desc else "null"
                    mensajes_vistos.append(f"Text: '{txt_log}' | Desc: '{desc_log}'")

                # === KEYWORDS === #
                texto_unido = (str(t_text) + str(t_desc)).lower()
                palabras_clave = ["usuario", "incorrect", "aviso", "registrado", "no existe", "error", "validar"]

                if any(palabra in texto_unido for palabra in palabras_clave):
                    print(f"✅ Text='{t_text}' Desc='{t_desc}'")
                    encontrado = True
                    #
            except:
                continue

        if encontrado:
            print("✅ ERROR DETECTED ")
        else:
            print("❌ SPECIFIC MESSAGE NOT FOUND ")
            for m in mensajes_vistos:
                print(f"   -> {m}")

    except Exception as e:
        print(f"❌ RUN-TIME ERROR: {e}")
    finally:
        utils.cerrar_driver(driver)

# === EXECUTION === #
if __name__ == "__main__":
    
    test_1_login_exitoso()
    test_2_pass_incorrecto()
    test_4_usuario_no_registrado()
    driver, wait = utils.iniciar_driver()
    realizar_login(driver,wait)