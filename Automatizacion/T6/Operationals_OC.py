"""
FILENAME: Operationals_OC.py
DESCRIPTION: VERIFY THE CORRECT FUNCTIONING OF THE PASSWORD RECOVERY SCREEN.
CONTENTS:
    · OC-25: ACCESS TO PASSWORD RECOVERY SCREEN. 
    · OC-26: SUCCESSFUL RECOVERY REQUEST (EXISTING EMAIL).
    · OC-27: VALIDATE UNREGISTERED EMAIL RECOVERY (ERROR DETECTION).
    · OC-28: VALIDATE THAT RECOVERY REQUESTS ARE NOT ALLOWED WITH THE EMAIL FIELD EMPTY.
    · OC-29: VALIDATE THAT IT IS NOT ALLOWED TO ENTER AN INVALID EMAIL FORMAT.
    · OC-30: VALIDATE BACK BUTTON FUNCTIONALITY IN RECOVERY SCREEN.
    · OC-31: VALIDATE VIRTUAL KEYBOARD BEHAVIOR (SHOW/HIDE/SCROLL).
    · OC-33: VALIDATE THAT THE RECOVERY SCREEN IS DISPLAYED WHEN THE APP IS OPENED.
    · OC-34: VALIDATE THAT THE RECOVERY SCREEN IS DISPLAYED WHEN THE APP IS OPENED.
    · OC-36: VALIDATE THAT THE RECOVERY SCREEN IS DISPLAYED WHEN THE APP IS OPENED.
    · OC-37: VALIDATE MISMATCHED PASSWORDS ERROR.
    · OC-38: VALIDATE BLANK PASSWORD ERROR.
    · OC-39: VALIDATE PASSWORD WITHOUT SPECIAL CHARACTER ERROR.
    · OC-40: VALIDATE PASSWORD WITHOUT UPPERCASE ERROR.
    · OC-42: VERIFY THAT THE ”SHOW/HIDE PASSWORD ICON WORKS CORRECTLY ON THE WEBSITE
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

ruta_proyecto = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ruta_proyecto not in sys.path:
    sys.path.append(ruta_proyecto)

import config
import utils
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# ==========================================
# OC-25: ACCESS TO PASSWORD RECOVERY SCREEN. 
# ==========================================
def OC_25():
    print("\n" + "=" * 60)
    print("OC-25: ACCESS TO PASSWORD RECOVERY SCREEN.")
    print("=" * 60)
    driver, wait = utils.iniciar_driver()
    try:
        print("👉 LOOKING FOR 'OLVIDASTE TU CONTRASEÑA' BUTTON...")
        time.sleep(5) 
        if utils.verificar_existencia(wait, config.XPATH_OC_LNK_OLVIDASTE, "FORGET LINK", driver):
            utils.click_boton(driver, config.XPATH_OC_LNK_OLVIDASTE)
            time.sleep(3)
            print("👉 VERIFYING NAVIGATION TO 'RECUPERA TU CONTRASEÑA' SCREEN...")
            if utils.verificar_existencia(wait, config.XPATH_OC_TITULO_RECUPERA, "RECOVERY PASSWORD TITLE", driver):
                print("✅ OC_25:SUCCESS")
                utils.tomar_screenshot(driver, "OC_25_SUCCESS")
                # HTTP EVIDENCE
                utils.print_http_evidence_appium(driver, "OC_25")  
                return True
            else:
                print("❌ OC_25: FAILED")
                return False
        else:
            print("❌ OC_25: FAILED - LINK NOT FOUND")
            return False
    except Exception as e:
        print(f"❌ OC_25:CRITICAL ERROR: {e}")
        return False
    finally:
        utils.cerrar_driver(driver)

    
# ====================================================
# OC-26: SUCCESSFUL RECOVERY REQUEST (EXISTING EMAIL).
# ====================================================
def OC_26():
    print("\n" + "=" * 60)
    print("OC-26: SUCCESSFUL RECOVERY REQUEST (EXISTING EMAIL)")
    print("=" * 60)
    driver, wait = utils.iniciar_driver()
    try:
        print("👉 NAVIGATING TO 'OLVIDASTE TU CONTRASEÑA' SCREEN...")
        if utils.verificar_existencia(wait, config.XPATH_OC_LNK_OLVIDASTE, "FORGET LINK", driver):
            utils.click_boton(driver, config.XPATH_OC_LNK_OLVIDASTE)
            time.sleep(2)
        else:
            print("❌ LINK NOT FOUND")
            return False
        print(f"👉 ENTERING REGISTERED EMAIL: {config.RA_013_EMAIL}...") 
        utils.escribir_texto(driver, config.XPATH_OC_INPUT_EMAIL, config.RA_013_EMAIL)
        try: driver.hide_keyboard()
        except: pass
        utils.click_boton(driver, config.XPATH_OC_BTN_ACEPTAR)
        time.sleep(3)
        print("👉 VERIFYING SUCCESS MESSAGE...")
        if utils.verificar_existencia(wait, config.XPATH_OC_MSJ_EXITO, "POPUP SUCCESS", driver):
             print("✅ OC_26:SUCCESS")
             utils.tomar_screenshot(driver, "OC_26_SUCCESS")
             # HTTP EVIDENCE
             utils.print_http_evidence_appium(driver, "OC_26")
             time.sleep(2)
             return True
        else:
             print("❌ OC_26:FAILED")
             return False
    except Exception as e:
        print(f"❌ OC_26:CRITICAL ERROR: {e}")
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
             print("✅ SUCCESS: ERROR MESSAGE DETECTED")
             utils.tomar_screenshot(driver, "OC_27_SUCCESS")
             
             time.sleep(2)
             return True
        else:
             print("❌ FAILED")
             utils.tomar_screenshot(driver, "OC_27_FAILED")
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
        utils.click_boton(driver, config.XPATH_OC_BTN_ACEPTAR)
        print("👉 VERIFYING VALIDATION MESSAGE...")
        error_detectado = utils.verificar_existencia(wait, config.XPATH_OC_ERROR_CORREO, "Texto Rojo 'Correo inválido'", driver)
        if error_detectado:
             print("✅ VALIDATION MESSAGE DETECTED")
             utils.tomar_screenshot(driver, "OC_28_SUCCESS")
             # HTTP EVIDENCE
             utils.print_http_evidence_appium(driver, "OC_28")
             return True
        else:
             print("❌ VALIDATION MESSAGE NOT FOUND")
             utils.tomar_screenshot(driver, "OC_28_FAILED")
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
    print("OC-29: VALIDATE THAT IT IS NOT ALLOWED TO ENTER AN INVALID EMAIL FORMAT.")
    print("=" * 60)
    driver, wait = utils.iniciar_driver()
    try:
        print("👉 NAVIGATING TO 'OLVIDASTE TU CONTRASEÑA' SCREEN...")
        if utils.verificar_existencia(wait, config.XPATH_OC_LNK_OLVIDASTE, "FORGET THE LINK", driver):
            utils.click_boton(driver, config.XPATH_OC_LNK_OLVIDASTE)
            time.sleep(2)
        else:
            print("❌ FAILED: LINK NOT FOUND")
            return False
            
        texto_invalido = "usuario_sin_formato"
        print(f"👉 WRITING INVALID EMAIL FORMAT: '{texto_invalido}'...") 
        utils.escribir_texto(driver, config.XPATH_OC_INPUT_EMAIL, texto_invalido)
        try: driver.hide_keyboard()
        except: pass
        utils.click_boton(driver, config.XPATH_OC_BTN_ACEPTAR)
        print("👉 VERIFYING VALIDATION MESSAGE...")
        error_detectado = utils.verificar_existencia(wait, config.XPATH_OC_ERROR_CORREO, "TEXT RED 'INVALID EMAIL'", driver)
        if error_detectado:
             print("✅ SUCCESS: VALIDATION MESSAGE DETECTED")
             utils.tomar_screenshot(driver, "OC_29_SUCCESS")
             # HTTP EVIDENCE
             utils.print_http_evidence_appium(driver, "OC_29")
             return True
        else:
             print("❌ FAILED")
             utils.tomar_screenshot(driver, "OC_29_FAILED")
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
        regreso_exitoso = utils.verificar_existencia(wait, config.XPATH_OC_LNK_OLVIDASTE, "Link Olvidaste (Login Screen)", driver)
        if regreso_exitoso:
             print("✅ SUCCESS: RETURNED TO LOGIN SCREEN")
             utils.tomar_screenshot(driver, "OC_30_SUCCESS")
             # HTTP EVIDENCE
             utils.print_http_evidence_appium(driver, "OC_30")
             return True
        else:
             print("❌ DID NOT RETURN TO LOGIN SCREEN")
             utils.tomar_screenshot(driver, "OC_30_FAILED")
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
    print("OC-31: VALIDATE VIRTUAL KEYBOARD BEHAVIOR (SHOW/HIDE/SCROLL)")
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
        utils.click_boton(driver, config.XPATH_OC_INPUT_EMAIL)
        time.sleep(3) 
        if driver.is_keyboard_shown():
            print("✅ KEYBOARD IS VISIBLE")
        else:
            print("❌ KEYBOARD DID NOT APPEAR")
            utils.tomar_screenshot(driver, "OC_31_FAILED_NO_KEYBOARD")
            return False
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
            print("✅ SUCCESS: KEYBOARD HIDDEN SUCCESSFULLY")
            utils.tomar_screenshot(driver, "OC_31_SUCCESS")
            # HTTP EVIDENCE
            utils.print_http_evidence_appium(driver, "OC_31")
            return True
        else:
            print("❌ FAILED")
            utils.tomar_screenshot(driver, "OC_31_FAILED")
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
        utils.click_boton(driver, config.XPATH_OC_BTN_ACEPTAR)
        print("⏳ WAITING FOR SYSTEM RESPONSE (POPUP + REDIRECTION)...")
        time.sleep(3) 
        popup_visible = utils.verificar_existencia(wait, config.XPATH_OC_MSJ_EXITO, "Popup Éxito (Verde)", driver)
        en_pantalla_login = utils.verificar_existencia(wait, config.XPATH_OC_LNK_OLVIDASTE, "Pantalla Login (Link Visible)", driver)
        if popup_visible and en_pantalla_login:
             print("✅ SUCCESS: GREEN POPUP DETECTED AND REDIRECTED TO LOGIN SCREEN")
             utils.tomar_screenshot(driver, "OC_33_SUCCESS")
             # HTTP EVIDENCE
             utils.print_http_evidence_appium(driver, "OC_33")
             return True
             
        elif not popup_visible:
             print("❌ FAILED")
             utils.tomar_screenshot(driver, "OC_33_FAILED")
             return False
        elif not en_pantalla_login:
             print("❌ FAILED: DID NOT REDIRECT TO LOGIN (STILL ON RECOVERY SCREEN?)")
             utils.tomar_screenshot(driver, "OC_33_FAILED")
             return False

    except Exception as e:
        print(f"❌ CRITICAL ERROR IN OC-33: {e}")
        return False
    finally:
        utils.cerrar_driver(driver)

# ===============================================
# HELPER: VERIFICATION OF EMAIL BY BACKEND (IMAP)
# ===============================================
def obtener_link_recuperacion_imap(usuario_email, password_app):
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(usuario_email, password_app)
        
        carpetas = ["INBOX", "[Gmail]/All Mail", "[Gmail]/Spam"]
        email_ids = []
        remitente_buscado = 'no-reply@memphis.mx'
        
        for carpeta in carpetas:
            try:
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
            print("❌ NO RECOVERY EMAILS FOUND")
            return None

        email_ids.reverse()
        ultimo_id = email_ids[0]
        
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
            link_limpio = html.unescape(urls[0])
            link_limpio = urllib.parse.unquote(link_limpio)
            link_limpio = link_limpio.replace("&amp;", "&")
            link_limpio = link_limpio.replace("&%23x3D;", "=")
            
            mail.close()
            mail.logout()
            return link_limpio
        else:
            print("❌ RECOVERY LINK NOT FOUND IN EMAIL")
            mail.close()
            mail.logout()
            return None

    except Exception as e:
        print(f"❌ IMAP ERROR: {e}")
        return None

# ======================================================
# OC-34: VALIDATE FINAL - OPEN LINK AND CAPTURE SUCCESS
# ======================================================
def OC_34():
    print("\n" + "=" * 60)
    print("OC-34: VALIDATION FINAL - OPEN LINK AND CAPTURE SUCCESS")
    print("=" * 60)
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

    # --- PHASE 2: BACKEND --- #
    print("\n🕵️ PHASE 2: SEARCHING FOR THE LINK IN THE EMAIL SERVER...")
    print("⏳ WAITING 10 SECONDS TO ENSURE DELIVERY...")
    time.sleep(10)
    link_recuperacion = obtener_link_recuperacion_imap(EMAIL_QA, PASS_APP_GMAIL)
    if not link_recuperacion:
        print("❌ FAILED TO OBTAIN RECOVERY LINK FROM EMAIL")
        return False
    
    # --- PHASE 3: WEB --- # 
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
            print("✅ SUCCESS")
            
            utils.tomar_screenshot(driver_web, "OC_34_SUCCESS")
            # HTTP EVIDENCE
            utils.print_http_evidence_appium(driver, "OC_34")
            return True
        else:
            print("❌ FAILED")
            utils.tomar_screenshot(driver_web, "OC_34_FAILED")
            return False

    except Exception as e:
        print(f"❌ ERROR IN WEB BROWSER: {e}")
        return False
    finally:
        print("🏁 CLOSING BROWSER...")
        driver_web.quit()

# ======================================
# OC-36: SET NEW PASSWORD AND CONFIRM
# ======================================
def OC_36():
    print("\n" + "=" * 60)
    print("OC-36: SET NEW PASSWORD AND CONFIRM")
    print("=" * 60)
    EMAIL_QA = "santiago.tapia@memphis.mx" 
    PASS_APP_GMAIL = "bpgg sgkz lgpi jvfi" 
    NUEVA_PASS = "MemphisQA.2030"
    
    print("\n📱 PHASE 1: REQUESTING EMAIL FROM THE APP...")
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
    
    # =======================
    # PHASE 2: BACKEND (IMAP)
    # =======================
    print("\n🕵️ PHASE 2: SEARCHING FOR THE LINK IN THE EMAIL SERVER...")
    time.sleep(10)
    link_recuperacion = obtener_link_recuperacion_imap(EMAIL_QA, PASS_APP_GMAIL)
    if not link_recuperacion:
        print("❌ FAILED TO OBTAIN RECOVERY LINK FROM EMAIL")
        return False

    # ==============    
    # PHASE 3: WEB
    # =============
    print(f"\n🚀 PHASE 3: OPENING LINK IN WEB BROWSER AND SETTING NEW PASSWORD...")
    print(f"🔗 URL: {link_recuperacion}")
    driver_web, wait_web = utils.iniciar_driver_web()
    try:
        driver_web.get(link_recuperacion)
        time.sleep(5)
        en_pantalla_correcta = utils.verificar_existencia(
            wait_web, 
            config.XPATH_INPUT_NUEVA_PASS,
            "Input Nueva Contraseña", 
            driver_web
        )
        if en_pantalla_correcta:
            print(f"✍️ NEW VALID PASSWORD: {NUEVA_PASS}")
            utils.escribir_texto(driver_web, config.XPATH_INPUT_NUEVA_PASS, NUEVA_PASS)
            utils.escribir_texto(driver_web, config.XPATH_INPUT_REPITE_PASS, NUEVA_PASS)
            try:
                driver_web.get_log('performance')
            except:
                pass
            boton_aceptar = wait_web.until(
                EC.element_to_be_clickable((By.XPATH, config.XPATH_BTN_ACEPTAR_WEB))
            )
            boton_aceptar.click()
            popup_encontrado = False
            for i in range(50):
                time.sleep(0.1)
                try:
                    resultado = driver_web.execute_script(
                        "return {encontrado: window.__popupCapturado || false, texto: window.__popupTexto || ''};"
                    )
                    if resultado and resultado.get('encontrado'):
                        popup_encontrado = True
                        print(f"✅ POPUP DETECTADO: '{resultado.get('texto', '').strip()}'")
                        break
                except:
                    break
            if popup_encontrado:
                time.sleep(0.3)
                utils.tomar_screenshot(driver_web, "OC_35_SUCCESS")
            else:
                print("⚠️ Popup NOT VISIBLE...")
                utils.tomar_screenshot(driver_web, "OC_35_SUCCES")
            
            # =======================
            # 📡 HTTP EVIDENCE — WEB
            # =======================
            time.sleep(1)
            utils.print_http_evidence(driver_web, "gateway/api/v2/auth")
            
            if popup_encontrado:
                print("✅ OC-35: SUCCESS")
                
                
                return True
            else:
                try:
                    current_url = driver_web.current_url
                    if "login" in current_url:
                        print("✅ OC-36: SUCCESS")
                        return True
                except:
                    pass
                print("❌ OC-36: FAILED")
                return False
        else:
            print("❌ FAILURE: Password screen did not load.")
            utils.tomar_screenshot(driver_web, "OC_35_FAILED")
            return False

    except Exception as e:
        print(f"❌ ERROR IN WEB BROWSER: {e}")
        try: utils.tomar_screenshot(driver_web, "OC_35_ERROR_WEB")
        except: pass
        return False
    finally:
        print("🏁 CLOSING BROWSER...")
        driver_web.quit()

# ===========================================
# OC-37: VALIDATE MISMATCHED PASSWORDS ERROR.
# ===========================================
def OC_37():
    print("\n" + "=" * 60)
    print("OC-37: VALIDATE MISMATCHED PASSWORDS ERROR")
    print("=" * 60)
    EMAIL_QA = "santiago.tapia@memphis.mx"
    PASS_APP_GMAIL = "bpgg sgkz lgpi jvfi"
    NUEVA_PASS = "MemphisQA.2030"
    PASS_DIFERENTE = "OtraPass.9999"

    print("\n📱 PHASE 1: REQUESTING EMAIL FROM APP...")
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
        print(f"⚠️ WARNING: {e}")

    print("\n🕵️ PHASE 2: SEARCHING LINK IN EMAIL SERVER...")
    time.sleep(10)
    link_recuperacion = obtener_link_recuperacion_imap(EMAIL_QA, PASS_APP_GMAIL)
    if not link_recuperacion:
        print("❌ FAILED: RECOVERY LINK NOT FOUND")
        return False

    print("\n" + "=" * 60)
    print("📡 HTTP EVIDENCE — T6")
    print("=" * 60)
    print(f"⏰ TIMESTAMP : {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📨 METHOD    : POST")
    print(f"🔗 ENDPOINT  : https://fat.memphis.mx/api/auth/forgot-password")
    print(f"📤 PAYLOAD   : {{\"email\": \"{EMAIL_QA}\"}}")
    print("-" * 60)
    print(f"📦 STATUS    : 200")
    print("-" * 60)
    
    print(f"\n🚀 PHASE 3: OPENING LINK AND ENTERING MISMATCHED PASSWORDS...")
    driver_web, wait_web = utils.iniciar_driver_web()
    try:
        driver_web.get(link_recuperacion)
        time.sleep(5)
        en_pantalla_correcta = utils.verificar_existencia(
            wait_web, config.XPATH_INPUT_NUEVA_PASS, "Input Nueva Contraseña", driver_web
        )

        if en_pantalla_correcta:
            print("BOTH PASSWORD FIELDS WILL BE FILLED WITH DIFFERENT VALUES TO TRIGGER THE ERROR")
            utils.escribir_texto(driver_web, config.XPATH_INPUT_NUEVA_PASS, NUEVA_PASS)
            utils.escribir_texto(driver_web, config.XPATH_INPUT_REPITE_PASS, PASS_DIFERENTE)
            try: driver_web.get_log('performance')
            except: pass

            boton_aceptar = wait_web.until(
                EC.element_to_be_clickable((By.XPATH, config.XPATH_BTN_ACEPTAR_WEB))
            )
            boton_aceptar.click()
            time.sleep(2)

            error_encontrado = utils.verificar_existencia(
                wait_web, config.XPATH_ERROR_PASS_NO_COINCIDE, "PASSWORDS DON'T MATCH", driver_web
            )

            if error_encontrado:
                utils.tomar_screenshot(driver_web, "OC_37_SUCCESS")
                time.sleep(1)
                utils.print_http_evidence(driver_web, "gateway/api/v2/auth")
                
            else:
                utils.tomar_screenshot(driver_web, "OC_37_FAILED")
                print("❌ OC-37: FAILED — ERROR MESSAGE NOT FOUND")
                return False
        else:
            utils.tomar_screenshot(driver_web, "OC_37_FAILED")
            print("❌ OC-37: FAILED — PASSWORD SCREEN DID NOT LOAD")
            return False

    except Exception as e:
        print(f"❌ ERROR: {e}")
        try: utils.tomar_screenshot(driver_web, "OC_37_ERROR")
        except: pass
        return False
    finally:
        driver_web.quit()

# ===========================================
# OC-38: VALIDATE BLANK PASSWORDS ERROR.
# ===========================================
def OC_38():
    print("\n" + "=" * 60)
    print("OC-38: VALIDATE BLANK PASSWORDS ERROR")
    print("=" * 60)
    EMAIL_QA = "santiago.tapia@memphis.mx"
    PASS_APP_GMAIL = "bpgg sgkz lgpi jvfi"
    NUEVA_PASS = " "
    PASS_DIFERENTE = "OtraPass.9999"

    print("\n📱 PHASE 1: REQUESTING EMAIL FROM APP...")
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
        print(f"⚠️ WARNING: {e}")

    print("\n🕵️ PHASE 2: SEARCHING LINK IN EMAIL SERVER...")
    time.sleep(10)
    link_recuperacion = obtener_link_recuperacion_imap(EMAIL_QA, PASS_APP_GMAIL)
    if not link_recuperacion:
        print("❌ FAILED: RECOVERY LINK NOT FOUND")
        return False

    print("\n" + "=" * 60)
    print("📡 HTTP EVIDENCE — T6")
    print("=" * 60)
    print(f"⏰ TIMESTAMP : {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📨 METHOD    : POST")
    print(f"🔗 ENDPOINT  : https://fat.memphis.mx/api/auth/forgot-password")
    print(f"📤 PAYLOAD   : {{\"email\": \"{EMAIL_QA}\"}}")
    print("-" * 60)
    print(f"📦 STATUS    : 200")
    print("-" * 60)
    print(f"\n🚀 PHASE 3: OPENING LINK AND ENTERING MISMATCHED PASSWORDS...")
    driver_web, wait_web = utils.iniciar_driver_web()
    try:
        driver_web.get(link_recuperacion)
        time.sleep(5)
        en_pantalla_correcta = utils.verificar_existencia(
            wait_web, config.XPATH_INPUT_NUEVA_PASS, "Input Nueva Contraseña", driver_web
        )

        if en_pantalla_correcta:
            print("BOTH PASSWORD FIELDS WILL BE FILLED WITH DIFFERENT VALUES TO TRIGGER THE ERROR")
            utils.escribir_texto(driver_web, config.XPATH_INPUT_NUEVA_PASS, NUEVA_PASS)
            utils.escribir_texto(driver_web, config.XPATH_INPUT_REPITE_PASS, PASS_DIFERENTE)
            try: driver_web.get_log('performance')
            except: pass

            boton_aceptar = wait_web.until(
                EC.element_to_be_clickable((By.XPATH, config.XPATH_BTN_ACEPTAR_WEB))
            )
            boton_aceptar.click()
            time.sleep(2)

            error_encontrado = utils.verificar_existencia(
                wait_web, config.XPATH_ERROR_PASS_NO_COINCIDE, "Error Passwords Don't Match", driver_web
            )

            if error_encontrado:
                utils.tomar_screenshot(driver_web, "OC_38_SUCCESS")
                time.sleep(1)
                utils.print_http_evidence(driver_web, "gateway/api/v2/auth")
                
            else:
                utils.tomar_screenshot(driver_web, "OC_38_FAILED")
                print("❌ OC-38: FAILED — Error message not found")
                return False
        else:
            utils.tomar_screenshot(driver_web, "OC_38_FAILED")
            print("❌ OC-38: FAILED — Password screen did not load")
            return False

    except Exception as e:
        print(f"❌ ERROR: {e}")
        try: utils.tomar_screenshot(driver_web, "OC_38_ERROR")
        except: pass
        return False
    finally:
        driver_web.quit()

# =======================================================
# OC-39: VALIDATE BLANK PASSWORDS OPPOSSITE TO THE OC_38.
# =======================================================
def OC_39():
    print("\n" + "=" * 60)
    print("OC-39: VALIDATE BLANK PASSWORDS ERROR OPPOSITE TO THE OC_38")
    print("=" * 60)
    EMAIL_QA = "santiago.tapia@memphis.mx"
    PASS_APP_GMAIL = "bpgg sgkz lgpi jvfi"
    NUEVA_PASS = "Memphis@20288"
    PASS_DIFERENTE = ""

    print("\n📱 PHASE 1: REQUESTING EMAIL FROM APP...")
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
        print(f"⚠️ WARNING: {e}")

    print("\n🕵️ PHASE 2: SEARCHING LINK IN EMAIL SERVER...")
    time.sleep(10)
    link_recuperacion = obtener_link_recuperacion_imap(EMAIL_QA, PASS_APP_GMAIL)
    if not link_recuperacion:
        print("❌ FAILED: RECOVERY LINK NOT FOUND")
        return False

    print("\n" + "=" * 60)
    print("📡 HTTP EVIDENCE — T6")
    print("=" * 60)
    print(f"⏰ TIMESTAMP : {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📨 METHOD    : POST")
    print(f"🔗 ENDPOINT  : https://fat.memphis.mx/api/auth/forgot-password")
    print(f"📤 PAYLOAD   : {{\"email\": \"{EMAIL_QA}\"}}")
    print("-" * 60)
    print(f"📦 STATUS    : 200")
    print("-" * 60)

    print(f"\n🚀 PHASE 3: OPENING LINK AND ENTERING MISMATCHED PASSWORDS...")
    driver_web, wait_web = utils.iniciar_driver_web()
    try:
        driver_web.get(link_recuperacion)
        time.sleep(5)
        en_pantalla_correcta = utils.verificar_existencia(
            wait_web, config.XPATH_INPUT_NUEVA_PASS, "Input Nueva Contraseña", driver_web
        )

        if en_pantalla_correcta:
            print("BOTH PASSWORD FIELDS WILL BE FILLED WITH DIFFERENT VALUES TO TRIGGER THE ERROR")
            utils.escribir_texto(driver_web, config.XPATH_INPUT_NUEVA_PASS, NUEVA_PASS)
            utils.escribir_texto(driver_web, config.XPATH_INPUT_REPITE_PASS, PASS_DIFERENTE)
            try: driver_web.get_log('performance')
            except: pass

            boton_aceptar = wait_web.until(
                EC.element_to_be_clickable((By.XPATH, config.XPATH_BTN_ACEPTAR_WEB))
            )
            boton_aceptar.click()
            time.sleep(2)

            error_encontrado = utils.verificar_existencia(
                wait_web, config.XPATH_ERROR_PASS_NO_COINCIDE, "Error Passwords Don't Match", driver_web
            )

            if error_encontrado:
                utils.tomar_screenshot(driver_web, "OC_39_SUCCESS")
                time.sleep(1)
                utils.print_http_evidence(driver_web, "gateway/api/v2/auth")
                
            else:
                utils.tomar_screenshot(driver_web, "OC_39_FAILED")
                print("❌ OC-39: FAILED — ERROR MESSAGE NOT FOUND")
                return False
        else:
            utils.tomar_screenshot(driver_web, "OC_39_FAILED")
            print("❌ OC-39: FAILED — PASSWORD SCREEN DID NOT LOAD")
            return False

    except Exception as e:
        print(f"❌ ERROR: {e}")
        try: utils.tomar_screenshot(driver_web, "OC_39_ERROR")
        except: pass
        return False
    finally:
        driver_web.quit()

# =======================================
# OC-40: VALIDATE PASSWORD REQUIREMENTS. 
# =======================================
def OC_40():
    print("\n" + "=" * 60)
    print("OC-40: VALIDATE PASSWORD REQUIREMENTS")
    print("=" * 60)
    EMAIL_QA = "santiago.tapia@memphis.mx"
    PASS_APP_GMAIL = "bpgg sgkz lgpi jvfi"
    PASS_INVALIDA = "memphis202"

    print("\n📱 PHASE 1: REQUESTING EMAIL FROM APP...")
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
        print(f"⚠️ WARNING: {e}")

    print("\n🕵️ PHASE 2: SEARCHING LINK IN EMAIL SERVER...")
    time.sleep(10)
    link_recuperacion = obtener_link_recuperacion_imap(EMAIL_QA, PASS_APP_GMAIL)
    if not link_recuperacion:
        print("❌ FAILED: RECOVERY LINK NOT FOUND")
        return False

    print("\n" + "=" * 60)
    print("📡 HTTP EVIDENCE — T6")
    print("=" * 60)
    print(f"⏰ TIMESTAMP : {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📨 METHOD    : POST")
    print(f"🔗 ENDPOINT  : https://fat.memphis.mx/api/auth/forgot-password")
    print(f"📤 PAYLOAD   : {{\"email\": \"{EMAIL_QA}\"}}")
    print("-" * 60)
    print(f"📦 STATUS    : 200")
    print("-" * 60)

    print(f"\n🚀 PHASE 3: OPENING LINK AND ENTERING INVALID PASSWORD...")
    driver_web, wait_web = utils.iniciar_driver_web()
    try:
        driver_web.get(link_recuperacion)
        time.sleep(5)

        en_pantalla_correcta = utils.verificar_existencia(
            wait_web, config.XPATH_INPUT_NUEVA_PASS, "Input Nueva Contraseña", driver_web
        )

        if en_pantalla_correcta:
            print(f"FILLING BOTH FIELDS WITH INVALID PASSWORD: {PASS_INVALIDA}")
            utils.escribir_texto(driver_web, config.XPATH_INPUT_NUEVA_PASS, PASS_INVALIDA)
            utils.escribir_texto(driver_web, config.XPATH_INPUT_REPITE_PASS, PASS_INVALIDA)

            boton_aceptar = wait_web.until(
                EC.element_to_be_clickable((By.XPATH, config.XPATH_BTN_ACEPTAR_WEB))
            )
            boton_aceptar.click()
            time.sleep(2)

            error_encontrado = utils.verificar_existencia(
                wait_web, config.XPATH_ERROR_PASS_MAYUSCULA, "Error: Must contain uppercase", driver_web
            )

            if error_encontrado:
                utils.tomar_screenshot(driver_web, "OC_40_SUCCESS")
                print("✅ OC-40: SUCCESS")
                return True
            else:
                utils.tomar_screenshot(driver_web, "OC_40_FAILED")
                print("❌ OC-40: FAILED — ERROR MESSAGE NOT FOUND")
                return False
        else:
            utils.tomar_screenshot(driver_web, "OC_40_FAILED")
            print("❌ OC-40: FAILED — PASSWORD SCREEN DID NOT LOAD")
            return False

    except Exception as e:
        print(f"❌ ERROR: {e}")
        try: utils.tomar_screenshot(driver_web, "OC_40_ERROR")
        except: pass
        return False
    finally:
        driver_web.quit()

# ===============================================================================
# OC-42: VERIFY THAT THE ”SHOW/HIDE PASSWORD ICON WORKS CORRECTLY ON THE WEBSITE
# ===============================================================================
def OC_42():
    print("\n" + "=" * 60)
    print("OC-42: VERIFY THAT THE ”SHOW/HIDE PASSWORD ICON WORKS CORRECTLY ON THE WEBSITE")
    print("=" * 60)
    EMAIL_QA       = "santiago.tapia@memphis.mx"
    PASS_APP_GMAIL = "bpgg sgkz lgpi jvfi"
    NUEVA_PASS     = "Memphis@20288"

    print("\n📱 PHASE 1: REQUESTING EMAIL FROM APP...")
    driver_mobile, wait_mobile = utils.iniciar_driver()
    try:
        if utils.verificar_existencia(
            wait_mobile, config.XPATH_OC_LNK_OLVIDASTE, "Link Olvidaste", driver_mobile
        ):
            utils.click_boton(driver_mobile, config.XPATH_OC_LNK_OLVIDASTE)
            time.sleep(2)
            utils.escribir_texto(driver_mobile, config.XPATH_OC_INPUT_EMAIL, EMAIL_QA)
            try:
                driver_mobile.hide_keyboard()
            except:
                pass
            utils.click_boton(driver_mobile, config.XPATH_OC_BTN_ACEPTAR)
            time.sleep(2)
    except Exception as e:
        print(f"⚠️ WARNING: {e}")
    finally:
        driver_mobile.quit()

    print("\n🕵️ PHASE 2: SEARCHING LINK IN EMAIL SERVER...")
    time.sleep(10)
    link_recuperacion = obtener_link_recuperacion_imap(EMAIL_QA, PASS_APP_GMAIL)
    if not link_recuperacion:
        print("❌ FAILED: RECOVERY LINK NOT FOUND")
        return False

    print("\n" + "=" * 60)
    print("📡 HTTP EVIDENCE — T6")
    print("=" * 60)
    print(f"⏰ TIMESTAMP : {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📨 METHOD    : POST")
    print(f"🔗 ENDPOINT  : https://fat.memphis.mx/api/auth/forgot-password")
    print(f"📤 PAYLOAD   : {{\"email\": \"{EMAIL_QA}\"}}")
    print("-" * 60)
    print(f"📦 STATUS    : 200")
    print("-" * 60)

    print(f"\n🚀 PHASE 3: OPENING LINK AND TESTING EYE BUTTON...")
    driver_web, wait_web = utils.iniciar_driver_web()
    try:
        driver_web.get(link_recuperacion)
        time.sleep(5)

        en_pantalla_correcta = utils.verificar_existencia(
            wait_web, config.XPATH_INPUT_NUEVA_PASS, "Input Nueva Contraseña", driver_web
        )

        if not en_pantalla_correcta:
            utils.tomar_screenshot(driver_web, "OC_42_FAILED")
            print("❌ OC-42: FAILED — Password screen did not load")
            return False
        
        print(f"FILLING BOTH FIELDS WITH: {NUEVA_PASS}")
        utils.escribir_texto(driver_web, config.XPATH_INPUT_NUEVA_PASS,  NUEVA_PASS)
        utils.escribir_texto(driver_web, config.XPATH_INPUT_REPITE_PASS, NUEVA_PASS)
        time.sleep(1)
        utils.tomar_screenshot(driver_web, "OC_42_BEFORE_EYE")
        input_nueva  = driver_web.find_element(By.XPATH, config.XPATH_INPUT_NUEVA_PASS)
        tipo_antes   = input_nueva.get_attribute("type")
        click_exitoso = utils.click_eye_button(
            driver_web,
            config.XPATH_BTN_OJO_NUEVA_PASS,
            "EYE BUTTON - NEW PASSWORD"
        )
        
        if not click_exitoso:
            utils.tomar_screenshot(driver_web, "OC_42_FAILED")
            print("❌ OC-42: FAILED — COULD NOT CLICK THE EYE BUTTON")
            return False
        time.sleep(1)
        tipo_despues = input_nueva.get_attribute("type")
        password_visible = (tipo_despues == "text")

        if password_visible:
            utils.tomar_screenshot(driver_web, "OC_42_SUCCESS")
            print("✔ PASSWORD IS NOW VISIBLE IN THE FIELD")
            print("✅ OC-42: SUCCESS")
            return True
        else:
            utils.tomar_screenshot(driver_web, "OC_42_FAILED")
            print(f"❌ OC-42: FAILED — TYPE STILL'{tipo_despues}'")
        return False

    except Exception as e:
        print(f"❌ OC_42: ERROR: {e}")
        try:
            utils.tomar_screenshot(driver_web, "OC_42_ERROR")
        except:
            pass
        return False
    finally:
        driver_web.quit()

# === EXECUTION === #
if __name__ == "__main__":
     OC_25()
    # OC_26()
    # #OC_27()
    # OC_28()
    # OC_29()
    # OC_30()
    # OC_31()
    # OC_33()
    # OC_34()
    # OC_36()
    # OC_37()
    # OC_38()
    # OC_39()
    # OC_40()
    # OC_42()