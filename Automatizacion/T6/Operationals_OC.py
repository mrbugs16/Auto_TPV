"""
FILENAME: Operationals_OC.py
DESCRIPTION: VERIFY THE CORRECT FUNCTIONING OF THE PASSWORD RECOVERY SCREEN.
CONTENTS:
    · OC-25: VERIFY THAT THE PASSWORD RECOVERY SCREEN LOADS CORRECTLY.
    · OC-26: VALIDATE THAT PASSWORD RECOVERY CAN BE REQUESTED FOR A REGISTERED EMAIL ADDRESS.
    · OC-27: VALIDATE UNREGISTERED EMAIL RECOVERY (ERROR DETECTION).
    · OC-28: VALIDATE THAT RECOVERY REQUESTS ARE NOT ALLOWED WITH THE EMAIL FIELD EMPTY.
    · OC-29: VALIDATE THAT IT IS NOT ALLOWED TO ENTER AN INVALID EMAIL FORMAT.
    · OC-30: VALIDATE BACK BUTTON FUNCTIONALITY IN RECOVERY SCREEN.
    · OC-31: VALIDATE VIRTUAL KEYBOARD BEHAVIOR (SHOW/HIDE/SCROLL).
    · OC-33: VALIDATE THAT THE RECOVERY SCREEN IS DISPLAYED WHEN THE APP IS OPENED.
    · OC-34: VALIDATE THAT THE RECOVERY SCREEN IS DISPLAYED WHEN THE APP IS OPENED.
"""

import sys
import os
import time
import random
import string
import imaplib 
import email 
import re 
from email.header import decode_header
import html
import urllib.parse

# Add parent directory to path to import config and utils
ruta_proyecto = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ruta_proyecto not in sys.path:
    sys.path.append(ruta_proyecto)

import config
import utils
from selenium.webdriver.common.by import By

# ===============================================================
# OC-25: VERIFY THAT THE PASSWORD RECOVERY SCREEN LOADS CORRECTLY
# ===============================================================
def OC_25():
    print("\n" + "=" * 60)
    print("OC-25: VERIFY THAT THE PASSWORD RECOVERY SCREEN LOADS CORRECTLY")
    print("=" * 60)
    driver, wait = utils.iniciar_driver()
    
    try:
        print("👉 LOOKING FOR 'OLVIDASTE TU CONTRASEÑA' LINK...")
        time.sleep(5) 
        
        if utils.verificar_existencia(wait, config.XPATH_OC_LNK_OLVIDASTE, "Olvidaste tu contraseña Link", driver):
            print("👉 CLICKING 'OLVIDASTE TU CONTRASEÑA'...")
            utils.click_boton(driver, config.XPATH_OC_LNK_OLVIDASTE)
            time.sleep(3)
            
            print("👉 VERIFYING NAVIGATION TO 'RECUPERA TU CONTRASEÑA' SCREEN...")
            if utils.verificar_existencia(wait, config.XPATH_OC_TITULO_RECUPERA, "Titulo Recupera tu contraseña", driver):
                print("✅ SCREEN LOADED")
                utils.tomar_screenshot(driver, "OC_25_Exito")
                return True
            else:
                 print("❌ SCREEN NOT LOADED")
                 return False
        else:
            print("❌ LINK NOT FOUND")
            return False

    except Exception as e:
        print(f"❌ CRITICAL ERROR IN OC-25: {e}")
        return False
    finally:
        utils.cerrar_driver(driver)

# ======================================================================================= 
# OC-26: VALIDATE THAT PASSWORD RECOVERY CAN BE REQUESTED FOR A REGISTERED EMAIL ADDRESS.
# =======================================================================================
def OC_26():
    print("\n" + "=" * 60)
    print("OC-26: VALIDATE THAT PASSWORD RECOVERY CAN BE REQUESTED FOR A REGISTERED EMAIL ADDRESS.")
    print("=" * 60)
    driver, wait = utils.iniciar_driver()
    
    try:
        print("👉 NAVIGATING TO 'OLVIDASTE TU CONTRASEÑA' SCREEN...")
        if utils.verificar_existencia(wait, config.XPATH_OC_LNK_OLVIDASTE, "Olvidaste Link", driver):
            utils.click_boton(driver, config.XPATH_OC_LNK_OLVIDASTE)
            time.sleep(2)
        else:
            print("❌ LINK NOT FOUND")
            return False
            
        print(f"👉 ENTERING REGISTERED EMAIL: {config.RA_013_EMAIL}...") 
        utils.escribir_texto(driver, config.XPATH_OC_INPUT_EMAIL, config.RA_013_EMAIL)
        
        try: driver.hide_keyboard()
        except: pass
        
        print("👉 CLICKING 'ACEPTAR' BUTTON...")
        utils.click_boton(driver, config.XPATH_OC_BTN_ACEPTAR)
        time.sleep(3)
        
        print("👉 VERIFYING SUCCESS MESSAGE...")
        if utils.verificar_existencia(wait, config.XPATH_OC_MSJ_EXITO, "Popup Exito Recuperacion", driver):
             print("✅ POPUP DETECTED")
             utils.tomar_screenshot(driver, "OC_26_Exito")
             time.sleep(2)
             return True
        else:
             print("❌ POPUP NOT FOUND")
             return False

    except Exception as e:
        print(f"❌ CRITICAL ERROR IN OC-26: {e}")
        return False
    finally:
        utils.cerrar_driver(driver)

# =============================================================
# OC-27: VALIDATE UNREGISTERED EMAIL RECOVERY (ERROR DETECTION)
# =============================================================
def OC_27():
    print("\n" + "=" * 60)
    print("OC-27: VALIDATE UNREGISTERED EMAIL RECOVERY (ERROR DETECTION)")
    print("=" * 60)
    driver, wait = utils.iniciar_driver()
    
    try:
        print("👉 NAVIGATING TO 'OLVIDASTE TU CONTRASEÑA' SCREEN...")
        if utils.verificar_existencia(wait, config.XPATH_OC_LNK_OLVIDASTE, "Olvidaste Link", driver):
            utils.click_boton(driver, config.XPATH_OC_LNK_OLVIDASTE)
            time.sleep(2)
        else:
            print("❌ LINK NOT FOUND")
            return False
            
        print(f"👉 ENTERING UNREGISTERED EMAIL: {config.USUARIO_INVALIDO}...") 
        utils.escribir_texto(driver, config.XPATH_OC_INPUT_EMAIL, config.USUARIO_INVALIDO)
        
        try: driver.hide_keyboard()
        except: pass
        
        print("👉 CLICKING 'ACEPTAR' BUTTON...")
        utils.click_boton(driver, config.XPATH_OC_BTN_ACEPTAR)
        
        print("👉 VERIFYING ERROR MESSAGE...")
        if utils.verificar_existencia(wait, config.XPATH_ERROR_GENERICO, "Error Popup", driver):
             print("✅ ERROR MESSAGE DETECTED")
             utils.tomar_screenshot(driver, "OC_27_Exito")
             time.sleep(2)
             return True
        else:
             print("❌ ERROR MESSAGE NOT FOUND")
             utils.tomar_screenshot(driver, "OC_27_Fallo")
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
        print(f"❌ CRITICAL ERROR IN OC-27: {e}")
        return False
    finally:
        utils.cerrar_driver(driver)

# =================================================================================
# OC-28: VALIDATE THAT RECOVERY REQUESTS ARE NOT ALLOWED WITH THE EMAIL FIELD EMPTY.
# =================================================================================
def OC_28():
    print("\n" + "=" * 60)
    print("OC-28: VALIDATE THAT RECOVERY REQUESTS ARE NOT ALLOWED WITH THE EMAIL FIELD EMPTY.")
    print("=" * 60)
    driver, wait = utils.iniciar_driver()
    
    try:
        print("👉 NAVIGATING TO 'OLVIDASTE TU CONTRASEÑA' SCREEN...")
        if utils.verificar_existencia(wait, config.XPATH_OC_LNK_OLVIDASTE, "Olvidaste Link", driver):
            utils.click_boton(driver, config.XPATH_OC_LNK_OLVIDASTE)
            time.sleep(2)
        else:
            print("❌ LINK NOT FOUND")
            return False
            
        print("👉 LEAVING EMAIL FIELD EMPTY...") 
        utils.escribir_texto(driver, config.XPATH_OC_INPUT_EMAIL, "")
        try: driver.hide_keyboard()
        except: pass
        print("👉 CLICKING 'ACEPTAR' BUTTON...")
        utils.click_boton(driver, config.XPATH_OC_BTN_ACEPTAR)
        print("👉 VERIFYING VALIDATION MESSAGE...")
        error_detectado = utils.verificar_existencia(wait, config.XPATH_OC_ERROR_CORREO, "Texto Rojo 'Correo inválido'", driver)
        if error_detectado:
             print("✅ VALIDATION MESSAGE DETECTED")
             utils.tomar_screenshot(driver, "OC_28_Exito")
             return True
        else:
             print("❌ VALIDATION MESSAGE NOT FOUND")
             utils.tomar_screenshot(driver, "OC_28_Fallo")
             return False

    except Exception as e:
        print(f"❌ CRITICAL ERROR IN OC-28: {e}")
        return False
    finally:
        utils.cerrar_driver(driver)

# =========================================================================
# OC-29: VALIDATE THAT IT IS NOT ALLOWED TO ENTER AN INVALID EMAIL FORMAT.
# =========================================================================
def OC_29():
    print("\n" + "=" * 60)
    print("OC-29: VALIDATION OF EMAIL FORMAT (INVALID TEXT)")
    print("=" * 60)
    driver, wait = utils.iniciar_driver()
    
    try:
        print("👉 NAVIGATING TO 'OLVIDASTE TU CONTRASEÑA' SCREEN...")
        if utils.verificar_existencia(wait, config.XPATH_OC_LNK_OLVIDASTE, "FORGET THE LINK", driver):
            utils.click_boton(driver, config.XPATH_OC_LNK_OLVIDASTE)
            time.sleep(2)
        else:
            print("❌ LINK NOT FOUND")
            return False
            
        texto_invalido = "usuario_sin_formato"
        print(f"👉 WRITING INVALID EMAIL FORMAT: '{texto_invalido}'...") 
        utils.escribir_texto(driver, config.XPATH_OC_INPUT_EMAIL, texto_invalido)
        
        try: driver.hide_keyboard()
        except: pass
        
        print("👉 CLICKING 'ACCEPT' BUTTON...")
        utils.click_boton(driver, config.XPATH_OC_BTN_ACEPTAR)
        
        print("👉 VERIFYING VALIDATION MESSAGE...")
        
        error_detectado = utils.verificar_existencia(wait, config.XPATH_OC_ERROR_CORREO, "TEXT RED 'INVALID EMAIL'", driver)
        
        if error_detectado:
             print("✅ VALIDATION MESSAGE DETECTED")
             utils.tomar_screenshot(driver, "OC_29_Exito")
             return True
        else:
             print("❌ FAILURE: VALIDATION MESSAGE NOT FOUND")
             utils.tomar_screenshot(driver, "OC_29_Fallo")
             return False

    except Exception as e:
        print(f"❌ CRITICAL ERROR IN OC-29: {e}")
        return False
    finally:
        utils.cerrar_driver(driver)

# ==============================================================
# OC-30: VALIDATE BACK BUTTON FUNCTIONALITY IN RECOVERY SCREEN
# ==============================================================
def OC_30():
    print("\n" + "=" * 60)
    print("OC-30: VALIDATE BACK BUTTON FUNCTIONALITY IN RECOVERY SCREEN")
    print("=" * 60)
    driver, wait = utils.iniciar_driver()
    
    try:
        print("👉 NAVIGATING TO 'OLVIDASTE TU CONTRASEÑA' SCREEN...")
        if utils.verificar_existencia(wait, config.XPATH_OC_LNK_OLVIDASTE, "Olvidaste Link", driver):
            utils.click_boton(driver, config.XPATH_OC_LNK_OLVIDASTE)
            time.sleep(2)
        else:
            print("❌ LINK TO RECOVERY NOT FOUND")
            return False
            
        if not utils.verificar_existencia(wait, config.XPATH_OC_TITULO_RECUPERA, "Título Pantalla Recuperación", driver):
            print("❌ DID NOT LOAD RECOVERY SCREEN")
            return False
            
        print("✅ RECOVERY SCREEN LOADED. PREPARING TO GO BACK...")
        
        print("👉 CLICKING 'BACK' ARROW...")
        utils.click_boton(driver, config.XPATH_OC_BTN_ATRAS)
        time.sleep(2)
        
        print("👉 VERIFYING RETURN TO LOGIN SCREEN...")
        
        regreso_exitoso = utils.verificar_existencia(wait, config.XPATH_OC_LNK_OLVIDASTE, "Link Olvidaste (Login Screen)", driver)
        
        if regreso_exitoso:
             print("✅ RETURNED TO LOGIN SCREEN")
             utils.tomar_screenshot(driver, "OC_30_Exito")
             return True
        else:
             print("❌ DID NOT RETURN TO LOGIN SCREEN")
             utils.tomar_screenshot(driver, "OC_30_Fallo")
             return False

    except Exception as e:
        print(f"❌ CRITICAL ERROR IN OC-30: {e}")
        return False
    finally:
        utils.cerrar_driver(driver)

# =============================================================
# OC-31: VALIDATE VIRTUAL KEYBOARD BEHAVIOR (SHOW/HIDE/SCROLL)
# =============================================================
def OC_31():
    print("\n" + "=" * 60)
    print("OC-31: VALIDATE VIRTUAL KEYBOARD BEHAVIOR")
    print("=" * 60)
    driver, wait = utils.iniciar_driver()
    
    try:
        print("👉 NAVIGATING TO 'OLVIDASTE TU CONTRASEÑA' SCREEN...")
        if utils.verificar_existencia(wait, config.XPATH_OC_LNK_OLVIDASTE, "Link Olvidaste", driver):
            utils.click_boton(driver, config.XPATH_OC_LNK_OLVIDASTE)
            time.sleep(2)
        else:
            print("❌ LINK NOT FOUND")
            return False

        print("👉 TAPPING EMAIL FIELD TO TRIGGER KEYBOARD...")
        utils.click_boton(driver, config.XPATH_OC_INPUT_EMAIL)
        time.sleep(3) 
        
        if driver.is_keyboard_shown():
            print("✅ KEYBOARD IS VISIBLE")
        else:
            print("❌ KEYBOARD DID NOT APPEAR")
            utils.tomar_screenshot(driver, "OC_31_Fallo_NoTeclado")
            return False

        print("👉 VERIFYING 'ACEPTAR' BUTTON VISIBILITY...")
        if utils.verificar_existencia(wait, config.XPATH_OC_BTN_ACEPTAR, "Boton Aceptar", driver):
            print("✅ 'ACEPTAR' BUTTON DETECTED")
        else:
            print("⚠️ BUTTON MIGHT BE COVERED")

        print("👉 ATTEMPTING TO HIDE KEYBOARD...")
        
        try:
            driver.hide_keyboard()
            print("   -> Command 'hide_keyboard()' sent.")
        except Exception as e:
            print(f"   -> Native hide failed ({e}), trying click outside...")
            utils.click_boton(driver, config.XPATH_OC_TITULO_RECUPERA)

        time.sleep(2)
        
        if not driver.is_keyboard_shown():
            print("✅ KEYBOARD HIDDEN SUCCESSFULLY")
            utils.tomar_screenshot(driver, "OC_31_Exito")
            return True
        else:
            print("❌ KEYBOARD STAYED OPEN")
            utils.tomar_screenshot(driver, "OC_31_Fallo_TecladoPegado")
            return False

    except Exception as e:
        print(f"❌ CRITICAL ERROR IN OC-31: {e}")
        return False
    finally:
        utils.cerrar_driver(driver)

# =================================================================================
# OC-33: VALIDATE REDIRECTION TO LOGIN SCREEN AFTER SUCCESSFUL RECOVERY REQUEST
# =================================================================================
def OC_33():
    print("\n" + "=" * 60)
    print("OC-33: VALIDATE REDIRECTION TO LOGIN SCREEN AFTER SUCCESSFUL RECOVERY REQUEST")
    print("=" * 60)
    
    driver, wait = utils.iniciar_driver()
    
    try:
        print("👉 NAVIGATING TO 'OLVIDASTE TU CONTRASEÑA' SCREEN...")
        if utils.verificar_existencia(wait, config.XPATH_OC_LNK_OLVIDASTE, "Link Olvidaste", driver):
            utils.click_boton(driver, config.XPATH_OC_LNK_OLVIDASTE)
            time.sleep(2)
        else:
            print("❌ LINK TO RECOVERY NOT FOUND")
            return False
            
        email_valido = config.RA_013_EMAIL
        print(f"👉 ENTERING VALID EMAIL: {email_valido}...") 
        utils.escribir_texto(driver, config.XPATH_OC_INPUT_EMAIL, email_valido)
        
        try: driver.hide_keyboard()
        except: pass
        
        print("👉 CLICKING 'ACEPTAR' BUTTON...")
        utils.click_boton(driver, config.XPATH_OC_BTN_ACEPTAR)
        
        print("⏳ WAITING FOR SYSTEM RESPONSE (POPUP + REDIRECTION)...")
        time.sleep(3) # Damos tiempo a la transición
        
        popup_visible = utils.verificar_existencia(wait, config.XPATH_OC_MSJ_EXITO, "Popup Éxito (Verde)", driver)
        
        en_pantalla_login = utils.verificar_existencia(wait, config.XPATH_OC_LNK_OLVIDASTE, "Pantalla Login (Link Visible)", driver)
        
        if popup_visible and en_pantalla_login:
             print("✅ SUCCESS: GREEN POPUP DETECTED AND REDIRECTED TO LOGIN SCREEN")
             utils.tomar_screenshot(driver, "OC_33_Exito")
             return True
             
        elif not popup_visible:
             print("❌ FAILURE: SUCCESS POPUP DID NOT APPEAR")
             utils.tomar_screenshot(driver, "OC_33_Fallo_NoPopup")
             return False
             
        elif not en_pantalla_login:
             print("❌ FAILURE: DID NOT REDIRECT TO LOGIN (STILL ON RECOVERY SCREEN?)")
             utils.tomar_screenshot(driver, "OC_33_Fallo_NoRedireccion")
             return False

    except Exception as e:
        print(f"❌ CRITICAL ERROR IN OC-33: {e}")
        return False
    finally:
        utils.cerrar_driver(driver)

# =================================================================================
# HELPER: VERIFICATION OF EMAIL BY BACKEND (IMAP)
# =================================================================================
def obtener_link_recuperacion_imap(usuario_email, password_app):
    print(f"📧 CONNECTING TO IMAP SERVER FOR: {usuario_email}...")
    
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(usuario_email, password_app)
        
        carpetas = ["INBOX", "[Gmail]/All Mail", "[Gmail]/Spam"]
        
        email_ids = []
        
        remitente_buscado = 'no-reply@memphis.mx'
        
        for carpeta in carpetas:
            try:
                print(f"📂 SCANNING FOLDER: {carpeta}...")
                mail.select(carpeta)
                typ, data = mail.search(None, f'(FROM "{remitente_buscado}")')
                
                if data[0]:
                    ids_encontrados = data[0].split()
                    if ids_encontrados:
                        email_ids = ids_encontrados[-3:] 
                        break 
            except Exception:
                continue
        
        if not email_ids:
            print("❌ FAILURE: NO EMAILS FOUND FROM 'no-reply@memphis.mx'.")
            return None

        email_ids.reverse() 
        ultimo_id = email_ids[0] 
        
        print(f"🔎 ANALYZING EMAIL ID: {ultimo_id.decode()}...")
        status, msg_data = mail.fetch(ultimo_id, "(RFC822)")
        
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        
        cuerpo = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    try: cuerpo += part.get_payload(decode=True).decode(errors="ignore")
                    except: pass
        else:
            try: cuerpo = msg.get_payload(decode=True).decode(errors="ignore")
            except: pass

        patron = r'https?://(?:fat|api)\.memphis\.mx/resetPwd[^\s"\'<>]+'
        urls = re.findall(patron, cuerpo)
        
        if urls:
            link_sucio = urls[0]
            print(f"⚠️ RAW LINK DETECTED: {link_sucio[:60]}...")

            link_limpio = html.unescape(link_sucio)
            
            link_limpio = urllib.parse.unquote(link_limpio)
            
            link_limpio = link_limpio.replace("&amp;", "&")
            link_limpio = link_limpio.replace("&%23x3D;", "=") 
            
            print(f"✅ CLEAN AND CORRECT LINK: {link_limpio}")
            
            mail.close()
            mail.logout()
            return link_limpio
        else:
            print("❌ THE EMAIL DOES NOT HAVE THE EXPECTED LINK.")
            mail.close()
            mail.logout()
            return None

    except Exception as e:
        print(f"❌ TECHNICAL ERROR IMAP: {e}")
        return None

# =================================================================================
# OC-34: VALIDATE FINAL - OPEN LINK AND CAPTURE SUCCESS
# =================================================================================
def OC_34():
    print("\n" + "=" * 60)
    print("OC-34: VALIDATION FINAL - OPEN LINK AND CAPTURE SUCCESS")
    print("=" * 60)
    
    # DATA
    EMAIL_QA = "santiago.tapia@memphis.mx" 
    PASS_APP_GMAIL = "bpgg sgkz lgpi jvfi" 
    
    print("📱 PHASE 1: REQUESTING EMAIL FROM THE APP...")
    driver_mobile, wait_mobile = utils.iniciar_driver()
    try:
        if utils.verificar_existencia(wait_mobile, config.XPATH_OC_LNK_OLVIDASTE, "Link Olvidaste", driver_mobile):
            utils.click_boton(driver_mobile, config.XPATH_OC_LNK_OLVIDASTE)
            time.sleep(2)
            utils.escribir_texto(driver_mobile, config.XPATH_OC_INPUT_EMAIL, EMAIL_QA)
            try: driver_mobile.hide_keyboard()
            except: pass
            utils.click_boton(driver_mobile, config.XPATH_OC_BTN_ACEPTAR)
            time.sleep(2)
    except Exception as e:
        print(f"⚠️ WARNING MOBILE: {e}")
    finally:
        utils.cerrar_driver(driver_mobile)

    # --- PHASE 2: BACKEND ---
    print("\n🕵️ PHASE 2: SEARCHING FOR THE LINK IN THE EMAIL SERVER...")
    print("⏳ WAITING 10 SECONDS TO ENSURE DELIVERY...")
    time.sleep(10)
    link_recuperacion = obtener_link_recuperacion_imap(EMAIL_QA, PASS_APP_GMAIL)
    
    if not link_recuperacion:
        print("❌ FALLO: No se pudo obtener el link del correo.")
        return False

    # --- PHASE 3: WEB (OPEN LINK AND CAPTURE SUCCESS) ---
    print(f"\n🚀 PHASE 3: OPENING LINK IN WEB BROWSER...")
    print(f"🔗 URL: {link_recuperacion}")
    
    driver_web, wait_web = utils.iniciar_driver_web()
    
    try:
        driver_web.get(link_recuperacion)
        
        print("⏳ WAITING FOR THE 'NEW PASSWORD' SCREEN TO LOAD...")
        time.sleep(5)
        
        en_pantalla_correcta = utils.verificar_existencia(
            wait_web, 
            config.XPATH_INPUT_NUEVA_PASS,
            "Input Nueva Contraseña", 
            driver_web
        )
        
        if en_pantalla_correcta:
            print("✅ ASSERTION PASSED")
            
            utils.tomar_screenshot(driver_web, "OC_34_SUCCESS_RESET_SCREEN")
            return True
        else:
            print("❌ FAILURE")
            utils.tomar_screenshot(driver_web, "OC_34_FAILURE_WHITE_SCREEN")
            return False

    except Exception as e:
        print(f"❌ ERROR IN WEB BROWSER: {e}")
        return False
    finally:
        print("🏁 CLOSING BROWSER...")
        driver_web.quit()

# === EXECUTION === #
if __name__ == "__main__":
    OC_25()
    OC_26()
    OC_27()
    OC_28()
    OC_29()
    OC_30()
    OC_31()
    OC_33()
    OC_34()
