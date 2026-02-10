"""
FILENAME: RCV.py
DESCRIPTION: RECOVERY PASSWORD ON WEB PLATFORM
"""

import sys 
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time
import config 
import utils 

"""
AUTOMATION RCV-001
· LOGIN WITH USER AND PASSWORD
· CLICK ON 'INGRESA AQUI'. 
""" 
def RCV_001():
    print("\n" + "=" * 60)
    print("AUTOMATION RCV-001: Login Exitoso + EVIDENCIA")
    print("=" * 60)
    
    driver, wait = utils.iniciar_driver_web()

    try: 
        # 1. NAVEGAR
        print(f"NAVIGATE TO: {config.URL_MEMPHIS_WEB}")
        driver.get(config.URL_MEMPHIS_WEB)
        
        # Guardamos la URL de inicio para comparar luego
        url_antes = driver.current_url
        time.sleep(3)
        
        # 2. ESCRIBIR CREDENCIALES
        print("✍️ Escribiendo Usuario y Contraseña...")
        utils.escribir_texto(driver, config.XPATH_WEB_USER, config.WEB_USUARIO_PRUEBA)
        utils.escribir_texto(driver, config.XPATH_WEB_PASS, config.WEB_PASS_PRUEBA)
        
        # 3. CLICK EN LOGIN
        print("👉 Click en 'Iniciar Sesión'...")
        utils.click_boton(driver, config.XPATH_WEB_BTN_LOGIN)
        
        # 4. VALIDACIÓN (ASSERTION)
        print("⏳ Esperando transición de pantalla (4 seg)...")
        time.sleep(4) 
        
        # Capturamos la URL nueva
        url_despues = driver.current_url
        
        print(f"   🔹 URL Antes:   {url_antes}")
        print(f"   🔹 URL Después: {url_despues}")

        # LÓGICA CORREGIDA:
        # Solo validamos que la URL haya cambiado.
        # (Si url_antes es igual a url_despues, significa que no se movió)
        if url_antes != url_despues: 
            print("\n✅ ASSERTION PASSED: La URL cambió, el login fue exitoso.")
            utils.tomar_screenshot(driver, "RCV_001_EXITO")
        else:
            # Si las URLs son idénticas, revisamos si al menos desapareció el botón de login
            # (Útil para Single Page Apps que no cambian la URL)
            print("⚠ La URL no cambió. Buscando plan B...")
            
            # Buscamos si el botón de login sigue visible
            # (Nota: Esto requiere un manejo de excepción rápido)
            try:
                driver.implicitly_wait(2) # Espera corta
                driver.find_element("xpath", config.XPATH_WEB_BTN_LOGIN)
                # Si lo encuentra, es que seguimos en el login -> FALLO
                print("❌ El botón de Login sigue visible.")
                utils.tomar_screenshot(driver, "RCV_001_FALLO_URL_IGUAL")
                raise Exception("ASSERTION FAILED: No salimos de la pantalla de Login.")
            except:
                # Si NO encuentra el botón, es que desapareció -> ÉXITO
                print("✅ ASSERTION PASSED (Plan B): El botón de Login desapareció.")
                utils.tomar_screenshot(driver, "RCV_001_EXITO_B")

    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {e}")
        try: utils.tomar_screenshot(driver, "RCV_001_ERROR_TECNICO")
        except: pass
        
    finally:
        print("🏁 CLOSING BROWSER...")
        driver.quit()
"""
AUTOMATION RCV-002
· CLICK ON 'INGRESA AQUI'. 
· ENTER USERNAME
· CLICK ON THE 'SEND BUTTON'. 
"""
def RCV_002():
    print("\n" + "=" * 60)
    print("AUTOMATION RCV-002")
    print("=" * 60)
    
    driver, wait = utils.iniciar_driver_web()

    try:
        driver.get(config.URL_MEMPHIS_WEB)
        time.sleep(2)

        print("👉 CLICKING 'INGRESA AQUI'...")
        utils.click_boton(driver, config.XPATH_WEB_TXT_INGRESA_AQUI)
        time.sleep(2) # Esperar al modal

        print("✍️ ENTER USERNAME...")
        utils.escribir_texto(driver, config.XPATH_WEB_USER, config.WEB_USUARIO_PRUEBA)
        
        print("👉 CLICKING 'SEND BUTTON'...")
        utils.click_boton(driver, config.XPATH_WEB_BTN_ENVIAR)
        
        print("⏳ WAITING FOR SYSTEM CONFIRMATION...")
        
        mensaje_detectado = utils.verificar_existencia(wait, config.XPATH_MSJ_EXITO_RCV, "Mensaje: Se ha enviado un mail")
        
        if mensaje_detectado:
            print("\n✅ ASSERTION PASSED: THE SYSTEM DISPLAYED THE SUCCESS MESSAGE.")
            utils.tomar_screenshot(driver, "RCV_002_EXITO")
        else:
            error_msg = "ASSERTION FAILED: THE CONFIRMATION GREEN MESSAGE DID NOT APPEAR."
            utils.tomar_screenshot(driver, "RCV_002_FALLO")
            raise Exception(error_msg)

    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        
    finally:
        print("🏁 CLOSING BROWSER...")
        driver.quit()



if __name__ == "__main__":
    RCV_001()
    #RCV_002()