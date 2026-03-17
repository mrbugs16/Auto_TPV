"""
FILENAME: Operationals_LG.py
DESCRIPTION:
    Automated test suite focused on the LOGIN (Authentication) module.
    Executes critical access validations on the POS terminal.

TEST CASES COVERED:
    · LG_005: LOG IN WITH VALID CREDENTIALS.
    · LG_006: INCORRECT PASSWORD VALIDATION.
    · LG_008: UNREGISTERED USER VALIDATION.

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
# LG-005: LOG IN WITH VALID CREDENTIALS 
# =============================================== #
def LG_005():
    print("\n" + "=" * 60)
    print("LG-005: LOG IN WITH VALID CREDENTIALS")
    print("=" * 60)

    driver, wait = utils.iniciar_driver()

    try:
        time.sleep(3)
        utils.escribir_texto(driver, config.XPATH_INPUT_USUARIO, config.USUARIO_VALIDO)
        utils.escribir_texto(driver, config.XPATH_INPUT_PASS, config.PASS_VALIDO)
        driver.hide_keyboard()
        utils.click_boton(driver, config.XPATH_BTN_ACEPTAR)
        if utils.verificar_existencia(wait, config.XPATH_INPUT_USUARIO, "NEXT SCREEN"):
            print("✅ LG-005: SUCCESSFUL")

    except Exception as e:
        print(f"❌ LG-005: FAILED: {e}")
    finally:
        utils.cerrar_driver(driver)


# ================================================ #
# LG-006: INCORRECT PASSWORD VALIDATION 
# ================================================ #
def LG_006():
    print("\n" + "=" * 60)
    print("LG-006: INCORRECT PASSWORD VALIDATION")
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
            print("✅ LG-006: SUCCESS")
        else:
            print("❌ LG-006: FAILED")

    except Exception as e:
        print(f"❌ LG-006: FAILED: {e}")
    finally:
        utils.cerrar_driver(driver)

# =============================================== #
# LG-008: UNREGISTERED USER VALIDATION 
# =============================================== #
def LG_008():
    print("\n" + "=" * 60)
    print("LG-008: UNREGISTERED USER VALIDATION ")
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
            print("✅ LG-008: SUCCESS")
        else:
            print("❌ LG-008: FAILED")
            for m in mensajes_vistos:
                print(f"   -> {m}")

    except Exception as e:
        print(f"❌ LG-008: FAILED: {e}")
    finally:
        utils.cerrar_driver(driver)

# === EXECUTION === #
if __name__ == "__main__":
    
    LG_005()
    LG_006()
    LG_008() 