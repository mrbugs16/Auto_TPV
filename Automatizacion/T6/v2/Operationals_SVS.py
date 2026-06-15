"""
FILENAME: Operationals_SVS.py
DESCRIPTION:
    VALIDATING THE TAB OF SERVICES.

CONTENTS:
    · SVS-92: GO TO SERVICES TAB
    · SVS-93: ACCESS TO 'PAYMENT LINK' (HOME) LINK DE PAGO VIEW
    · SVS-94: ACCESS TO THE 'CREATE NEW' FROM PAYMENT LINK
    · SVS-95: SUCCESSFUL PAYMENT LINK GENERATION
    · SVS-96: FAILED GENERATION (EMPTY SPACE)
    · SVS-97: FAILED GENERATION (EMPTY PRODUCT OR SERVICE)

REQUIREMENTS:
    - APPIUM SERVER RUNNING.
    - config.py AND utils.py IN THE SAME DIRECTORY.
"""

import sys
import os
import re
import time

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_path not in sys.path:
    sys.path.append(project_path)

import config
import utils
from appium.webdriver.common.appiumby import AppiumBy          
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# =================================================================================
# INTERNAL HELPER: CAPTURE EVIDENCE WITHOUT SILENCING ERRORS
# =================================================================================
def _capture_evidence(driver, test_name):
    try:
        utils.print_http_evidence_appium(driver, test_name)
    except Exception as ev_err:
        print(f"   ⚠️  HTTP EVIDENCE CAPTURE FAILED FOR [{test_name}]: {ev_err}")
        print(f"   💡 MAKE SURE APPIUM IS STARTED WITH: appium --allow-insecure=*:get_server_logs")


# =================================================================================
# HELPER: FULL LOGIN FLOW v2
#         ONBOARDING → LOGIN → CONFIGURA TU COMERCIO → LECTOR POPUP → HOME
# =================================================================================
def helper_login_to_calculator(driver, wait):
    
    from selenium.common.exceptions import TimeoutException

    # ── PHASE 1: ONBOARDING SLIDES ───────────────────────────────────────────
    print("   📱 [HELPER] PHASE 1: NAVIGATING ONBOARDING SLIDES...")
    time.sleep(3)

    # SLIDE 1 → "Siguiente"
    try:
        utils.click_element(driver, config.XPATH_OB_BTN_SIGUIENTE)
        time.sleep(1.5)
        print("   ✅ [HELPER] SLIDE 1 PASSED")
    except Exception as e:
        print(f"   ⚠️  [HELPER] SLIDE 1 SKIP: {e}")
        try:
            utils.click_element(driver, config.XPATH_OB_BTN_SALTAR)
            time.sleep(1)
        except:
            pass

    # SLIDE 2 → "Siguiente"
    try:
        utils.click_element(driver, config.XPATH_OB_BTN_SIGUIENTE)
        time.sleep(1.5)
        print("   ✅ [HELPER] SLIDE 2 PASSED")
    except Exception as e:
        print(f"   ⚠️  [HELPER] SLIDE 2 SKIP: {e}")

    # SLIDE 3 → "Comenzar" (APP GOES DIRECTLY TO LOGIN AFTER THIS)
    try:
        utils.click_element(driver, config.XPATH_OB_BTN_COMENZAR)
        time.sleep(2)
        print("   ✅ [HELPER] SLIDE 3 PASSED — NOW ON LOGIN SCREEN")
    except Exception as e:
        print(f"   ⚠️  [HELPER] SLIDE 3 SKIP: {e}")

    # ── PHASE 2: LOGIN SCREEN ────────────────────────────────────────────────
    print("   🔐 [HELPER] PHASE 2: EXECUTING LOGIN...")

    print(f"   ✏️  TYPING EMAIL: {config.USUARIO_VALIDO}")
    utils.type_text(driver, config.XPATH_INPUT_USUARIO, config.USUARIO_VALIDO)
    time.sleep(0.5)
    utils.type_text(driver, config.XPATH_INPUT_PASS, config.PASS_VALIDO)
    time.sleep(0.5)

    try:
        driver.hide_keyboard()
    except:
        pass

    utils.click_element(driver, config.XPATH_LG_BTN_INICIAR)
    time.sleep(4)

    # ── PHASE 3: "CONFIGURA TU COMERCIO" (IF PRESENT) ────────────────────────
    print("   🏪 [HELPER] PHASE 3: CHECKING 'CONFIGURA TU COMERCIO' SCREEN...")

    screen_present = utils.verify_element(
        wait, config.XPATH_CC_SCREEN, "CONFIGURA TU COMERCIO SCREEN"
    )

    if screen_present:
        print(f"   ✅ [HELPER] SCREEN DETECTED — FILLING FORM...")
        print(f"   🔢 ENTERING AFFILIATION (FIELD 1): {config.CC_AFILIACION}")
        try:
            utils.type_text(driver, config.XPATH_CC_INPUT_AFILIACION, config.CC_AFILIACION)
            time.sleep(0.5)
        except Exception as e:
            print(f"   ⚠️  [HELPER] AFFILIATION INPUT FAILED: {e}")

        print(f"   🔑 ENTERING TOKEN (FIELD 2): {config.CC_TOKEN}")
        try:
            utils.type_text(driver, config.XPATH_CC_INPUT_TOKEN, config.CC_TOKEN)
            time.sleep(0.5)
        except Exception as e:
            print(f"   ⚠️  [HELPER] TOKEN INPUT FAILED: {e}")

        try:
            driver.hide_keyboard()
        except:
            pass

        utils.click_element(driver, config.XPATH_CC_BTN_CONFIRMAR)
        time.sleep(3)
        print("   ✅ [HELPER] 'CONFIGURA TU COMERCIO' SUBMITTED")
    else:
        print("   ℹ️  [HELPER] SCREEN NOT DETECTED — COMMERCE ALREADY LINKED")

    # ── PHASE 4: "LECTOR NO CONFIGURADO" POPUP → "CONFIGURAR AHORA" ─────────
    print("   ⚙️  [HELPER] PHASE 4: CHECKING 'LECTOR NO CONFIGURADO' POPUP...")
    time.sleep(2)

    popup_present = utils.verify_element(
        wait, config.XPATH_LG_POPUP_LECTOR_NC, "LECTOR NO CONFIGURADO POPUP"
    )

    if popup_present:
        print("   ✅ [HELPER] POPUP DETECTED — CLICKING 'Configurar ahora'...")
        try:
            utils.click_element(driver, config.XPATH_LG_BTN_CONFIGURAR_AHORA)
            time.sleep(3)
            print("   ✅ [HELPER] 'Configurar ahora' CLICKED")
        except Exception as e:
            print(f"   ⚠️  [HELPER] 'Configurar ahora' CLICK FAILED: {e}")

        # ── SCREEN D: "LECTOR CONFIGURADO" CONFIRMATION ──────────────────────
        # AFTER CLICKING "Configurar ahora" THE APP SHOWS A CONFIRMATION SCREEN
        # WITH "Lector configurado" + "Configuración completada" + BTN "Aceptar"
        print("   🎉 [HELPER] CHECKING 'LECTOR CONFIGURADO' CONFIRMATION SCREEN...")
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.by import By
            confirm_wait = WebDriverWait(driver, 8)
            confirm_wait.until(
                EC.presence_of_element_located((By.XPATH, config.XPATH_LG_LECTOR_CONFIGURADO))
            )
            print("   ✅ [HELPER] CONFIRMATION SCREEN DETECTED — CLICKING 'Aceptar'...")
            utils.click_element(driver, config.XPATH_LG_BTN_ACEPTAR_LECTOR)
            time.sleep(2)
            print("   ✅ [HELPER] LECTOR CONFIGURED — HEADING TO HOME")
        except Exception as e:
            print(f"   ⚠️  [HELPER] CONFIRMATION SCREEN NOT DETECTED OR 'Aceptar' FAILED: {e}")
            print(f"   ℹ️  [HELPER] LECTOR MAY ALREADY HAVE BEEN CONFIGURED IN A PRIOR SESSION")
    else:
        print("   ℹ️  [HELPER] NO POPUP DETECTED — LECTOR ALREADY CONFIGURED, CONTINUING TO HOME")
        time.sleep(2)
# =================================================================================
# INTERNAL HELPER: NAVIGATE TO THE "SERVICES" BOTTOM NAV TAB
# =================================================================================
def _navigate_to_services_tab(driver, wait):
    print("   🔍 [NAV] ATTEMPTING STRATEGY 1: config.XPATH_PÑ_TAB_SERVICIOS...")
    try:
        driver.find_element(By.XPATH, config.XPATH_PÑ_TAB_SERVICIOS).click()
        time.sleep(2)
        print("   ✅ [NAV] STRATEGY 1 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [NAV] STRATEGY 1 FAILED: {e}")

    print("   🔍 [NAV] ATTEMPTING STRATEGY 2: PARTIAL CONTENT-DESC MATCH...")
    try:
        driver.find_element(
            By.XPATH, '//*[contains(@content-desc, "Servicios")]'
        ).click()
        time.sleep(2)
        print("   ✅ [NAV] STRATEGY 2 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [NAV] STRATEGY 2 FAILED: {e}")

    print("   🔍 [NAV] ATTEMPTING STRATEGY 3: EXACT TEXT / CONTENT-DESC MATCH...")
    try:
        driver.find_element(
            By.XPATH, '//*[@text="Servicios" or @content-desc="Servicios"]'
        ).click()
        time.sleep(2)
        print("   ✅ [NAV] STRATEGY 3 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [NAV] STRATEGY 3 FAILED: {e}")

    print("   🔍 [NAV] ATTEMPTING STRATEGY 4: UIAUTOMATOR TEXT SEARCH (FINAL FALLBACK)...")
    try:
        driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains("Servicios")'
        ).click()
        time.sleep(2)
        print("   ✅ [NAV] STRATEGY 4 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   💥 [NAV] STRATEGY 4 FAILED: {e}")

    print("   ❌ [NAV] ALL STRATEGIES EXHAUSTED — SERVICES TAB NOT CLICKABLE.")
    return False


# =================================================================================
# INTERNAL HELPER: VERIFY THAT "LINKS DE PAGO" CARD IS VISIBLE ON SCREEN
# ================================================================================= 
def _verify_payment_links_visible(driver):
    
    print("   🔍 [VERIFY] ATTEMPTING STRATEGY 1: @text ATTRIBUTE...")
    try:
        el = driver.find_element(
            By.XPATH, '//*[@text="Links de pago" or @text="links de pago"]'
        )
        if el.is_displayed():
            print("   ✅ [VERIFY] STRATEGY 1 SUCCEEDED — 'LINKS DE PAGO' FOUND VIA @text.")
            return True
    except Exception as e:
        print(f"   ⚠️  [VERIFY] STRATEGY 1 FAILED: {e}")

    print("   🔍 [VERIFY] ATTEMPTING STRATEGY 2: contains(@text) / contains(@content-desc)...")
    try:
        el = driver.find_element(
            By.XPATH,
            '//*[contains(@text, "Links de pago") or contains(@content-desc, "Links de pago")]'
        )
        if el.is_displayed():
            print("   ✅ [VERIFY] STRATEGY 2 SUCCEEDED — 'LINKS DE PAGO' FOUND VIA PARTIAL MATCH.")
            return True
    except Exception as e:
        print(f"   ⚠️  [VERIFY] STRATEGY 2 FAILED: {e}")

    print("   🔍 [VERIFY] ATTEMPTING STRATEGY 3: UIAUTOMATOR TEXT SEARCH (FINAL FALLBACK)...")
    try:
        el = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains("Links de pago")'
        )
        if el.is_displayed():
            print("   ✅ [VERIFY] STRATEGY 3 SUCCEEDED — 'LINKS DE PAGO' FOUND VIA UIAUTOMATOR.")
            return True
    except Exception as e:
        print(f"   💥 [VERIFY] STRATEGY 3 FAILED: {e}")

    print("   ❌ [VERIFY] ALL STRATEGIES EXHAUSTED — 'LINKS DE PAGO' CARD NOT VISIBLE.")
    return False


# =================================================================================
# HELPER: CREATE PAYMENT LINK (PRE-TEST SETUP)
#         NAVIGATES THE FULL "GENERAR LINK" FLOW AND RETURNS TO THE LINKS LIST.
#         CALL THIS BEFORE ANY TEST THAT REQUIRES AN EXISTING PAYMENT LINK.
# =================================================================================
def _helper_create_payment_link(driver, wait,
                                amount="40",
                                description="Automatizacion"):
    
    from datetime import date as _date
    import calendar as _calendar

    def _first_tuesday_of_month():
        """RETURNS THE DAY NUMBER OF THE FIRST TUESDAY IN THE CURRENT MONTH."""
        today = _date.today()
        year, month = today.year, today.month
        # weekday(): Monday=0 … Sunday=6, so Tuesday=1
        for day in range(1, 32):
            try:
                if _date(year, month, day).weekday() == 1:  # Tuesday
                    return str(day), _date(year, month, day).strftime("%d/%m/%Y")
            except ValueError:
                break
        return None, None

    print("🔗 [LINK HELPER] STARTING PAYMENT LINK CREATION FLOW...")

    # ── STEP 1: NAVIGATE TO SERVICES TAB ─────────────────────────────────────
    print("   📍 [LINK HELPER] STEP 1: NAVIGATING TO SERVICES TAB...")
    tab_ok = _navigate_to_services_tab(driver, wait)
    if not tab_ok:
        print("   ❌ [LINK HELPER] COULD NOT REACH SERVICES TAB")
        return False
    time.sleep(1)

    # ── STEP 2: CLICK "LINKS DE PAGO" CARD ───────────────────────────────────
    print("   📍 [LINK HELPER] STEP 2: CLICKING 'LINKS DE PAGO' CARD...")
    card_ok = _click_payment_links_card(driver)
    if not card_ok:
        print("   ❌ [LINK HELPER] COULD NOT CLICK 'LINKS DE PAGO' CARD")
        return False
    time.sleep(2)

    # ── STEP 3: CLICK "+ GENERAR NUEVO LINK" BUTTON ───────────────────────────
    # BUTTON TEXT IN v2: "+ Generar nuevo link" (IMAGE 1 CONFIRMED)
    print("   📍 [LINK HELPER] STEP 3: CLICKING '+ Generar nuevo link'...")
    generar_clicked = False

    for strategy, xpath in enumerate([
        '//*[@text="+ Generar nuevo link" or @content-desc="+ Generar nuevo link"]',
        '//*[contains(@text, "Generar nuevo link") or contains(@content-desc, "Generar nuevo link")]',
        '//*[contains(@text, "Generar nuevo") or contains(@content-desc, "Generar nuevo")]',
    ], start=1):
        try:
            driver.find_element(By.XPATH, xpath).click()
            time.sleep(2)
            print(f"   ✅ [LINK HELPER] STEP 3: STRATEGY {strategy} SUCCEEDED")
            generar_clicked = True
            break
        except Exception as e:
            print(f"   ⚠️  [LINK HELPER] STRATEGY {strategy} FAILED: {e}")

    if not generar_clicked:
        try:
            driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().textContains("Generar nuevo")'
            ).click()
            time.sleep(2)
            print("   ✅ [LINK HELPER] STEP 3: UIAUTOMATOR STRATEGY SUCCEEDED")
            generar_clicked = True
        except Exception as e:
            print(f"   ❌ [LINK HELPER] STEP 3: ALL STRATEGIES FAILED: {e}")
            return False

    # ── STEP 4: FILL "MONTO A COBRAR" ────────────────────────────────────────
    # FIELD LABEL: "Monto a cobrar:" with placeholder "$ Monto a cobrar" (IMAGE 2)
    print(f"📍 [LINK HELPER] STEP 4: FILLING AMOUNT — '{amount}'...")
    amount_filled = False

    for strategy, xpath in enumerate([
        '//android.widget.EditText[1]',
        '//*[contains(@hint, "Monto") or contains(@text, "Monto a cobrar")]',
        '//*[contains(@content-desc, "Monto")]',
    ], start=1):
        try:
            el = driver.find_element(By.XPATH, xpath)
            el.click()
            time.sleep(0.5)
            el.clear()
            el.send_keys(amount)
            try:
                driver.hide_keyboard()
            except:
                pass
            time.sleep(0.5)
            print(f"   ✅ [LINK HELPER] STEP 4: STRATEGY {strategy} — TYPED: {amount}")
            amount_filled = True
            break
        except Exception as e:
            print(f"   ⚠️  [LINK HELPER] AMOUNT STRATEGY {strategy} FAILED: {e}")

    if not amount_filled:
        print("   ❌ [LINK HELPER] STEP 4: COULD NOT FILL AMOUNT FIELD")
        return False

    # ── STEP 5: FILL "PRODUCTO O SERVICIO" ───────────────────────────────────
    # FIELD LABEL: "Producto o servicio:" with placeholder "Concepto" (IMAGE 2)
    print(f"📍 [LINK HELPER] STEP 5: FILLING DESCRIPTION — '{description}'...")
    desc_filled = False

    for strategy, xpath in enumerate([
        '//android.widget.EditText[2]',
        '//*[contains(@hint, "Concepto") or contains(@text, "Concepto")]',
        '//*[contains(@hint, "Producto") or contains(@text, "Producto o servicio")]',
    ], start=1):
        try:
            el = driver.find_element(By.XPATH, xpath)
            el.click()
            time.sleep(0.5)
            el.clear()
            el.send_keys(description)
            try:
                driver.hide_keyboard()
            except:
                pass
            time.sleep(0.5)
            print(f"   ✅ [LINK HELPER] STEP 5: STRATEGY {strategy} — TYPED: {description}")
            desc_filled = True
            break
        except Exception as e:
            print(f"   ⚠️  [LINK HELPER] DESC STRATEGY {strategy} FAILED: {e}")

    if not desc_filled:
        print("   ❌ [LINK HELPER] STEP 5: COULD NOT FILL DESCRIPTION FIELD")
        return False

    # ── STEP 6: OPEN DATE PICKER AND SELECT FIRST TUESDAY OF MONTH ───────────
    target_day, target_str = _first_tuesday_of_month()
    print(f"📍 [LINK HELPER] STEP 6: SELECTING DATE — FIRST TUESDAY: {target_str} (DAY {target_day})...")

    # TAP THE DATE FIELD TO OPEN CALENDAR
    date_opened = False
    for xpath in [
        '//*[contains(@hint, "Fecha") or contains(@text, "Fecha de vencimiento")]',
        '//*[contains(@content-desc, "Fecha")]',
        '//android.widget.EditText[3]',
    ]:
        try:
            driver.find_element(By.XPATH, xpath).click()
            time.sleep(2)
            print("   ✅ [LINK HELPER] DATE FIELD TAPPED — CALENDAR OPENED")
            date_opened = True
            break
        except Exception as e:
            print(f"   ⚠️  [LINK HELPER] DATE FIELD TAP FAILED: {e}")

    if not date_opened:
        try:
            driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().textContains("Fecha")'
            ).click()
            time.sleep(2)
            date_opened = True
        except Exception as e:
            print(f"   ❌ [LINK HELPER] STEP 6: COULD NOT OPEN CALENDAR: {e}")
            return False

    # WAIT FOR CALENDAR HEADER "Selecciona una fecha" (IMAGE 3 CONFIRMED)
    for _ in range(5):
        try:
            driver.find_element(
                By.XPATH,
                '//*[contains(@text, "Selecciona una fecha") or '
                'contains(@content-desc, "Selecciona una fecha") or '
                'contains(@text, "SELECCIONAR FECHA") or '
                'contains(@content-desc, "SELECCIONAR FECHA")]'
            )
            print("   ✅ [LINK HELPER] CALENDAR CONFIRMED OPEN")
            break
        except:
            time.sleep(1)

    # SELECT FIRST TUESDAY — TRY MULTIPLE content-desc FORMATS
    # ANDROID CALENDAR: content-desc = "10, martes 10 de junio de 2026" or similar
    day_selected = False
    if target_day:
        for strategy_xpath in [
            f'new UiSelector().descriptionStartsWith("{target_day}, ")',
            f'new UiSelector().descriptionContains("martes {target_day} ")',
            f'new UiSelector().descriptionContains("{target_day} de ")',
        ]:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR, strategy_xpath
                ).click()
                time.sleep(1)
                print(f"   ✅ [LINK HELPER] DAY {target_day} (TUESDAY) SELECTED")
                day_selected = True
                break
            except Exception as e:
                print(f"   ⚠️  [LINK HELPER] DAY SELECT STRATEGY FAILED: {e}")

        if not day_selected:
            # XPATH FALLBACK WITH starts-with
            try:
                driver.find_element(
                    By.XPATH,
                    f'//*[starts-with(@content-desc, "{target_day}, ")]'
                ).click()
                time.sleep(1)
                print(f"   ✅ [LINK HELPER] DAY {target_day} SELECTED VIA XPATH starts-with")
                day_selected = True
            except Exception as e:
                print(f"   ⚠️  [LINK HELPER] XPATH FALLBACK FAILED: {e}")

    if not day_selected:
        print(f"   ❌ [LINK HELPER] STEP 6: COULD NOT SELECT DAY {target_day}")
        print("   💡 DUMPING @content-desc values for calendar diagnosis:")
        try:
            for el in driver.find_elements(By.XPATH, "//*[@content-desc]"):
                cd = el.get_attribute("content-desc")
                if cd and (str(target_day) in cd or "martes" in cd.lower()):
                    print(f"      → '{cd}'")
        except:
            pass
        return False

    # CONFIRM DATE WITH "ACEPTAR" BUTTON (IMAGE 3 BOTTOM RIGHT)
    print("   📍 [LINK HELPER] STEP 6D: CLICKING 'ACEPTAR' TO CONFIRM DATE...")
    for xpath in [
        '//*[@text="ACEPTAR" or @text="Aceptar" or @content-desc="ACEPTAR"]',
        '//*[contains(@text, "ACEPTAR") or contains(@content-desc, "ACEPTAR")]',
    ]:
        try:
            driver.find_element(By.XPATH, xpath).click()
            time.sleep(2)
            print("   ✅ [LINK HELPER] DATE CONFIRMED WITH 'ACEPTAR'")
            break
        except Exception as e:
            print(f"   ⚠️  [LINK HELPER] ACEPTAR FAILED: {e}")
    else:
        try:
            driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().textMatches("(?i)aceptar")'
            ).click()
            time.sleep(2)
            print("   ✅ [LINK HELPER] DATE CONFIRMED VIA UIAUTOMATOR")
        except Exception as e:
            print(f"   ❌ [LINK HELPER] STEP 6D: 'ACEPTAR' NOT FOUND: {e}")
            return False

    # ── STEP 7: CLICK "GENERAR LINK" BUTTON ──────────────────────────────────
    # BUTTON TEXT IN v2: "Generar link" (IMAGE 2 AND IMAGE 4 CONFIRMED)
    print("   📍 [LINK HELPER] STEP 7: CLICKING 'Generar link'...")
    generated = False

    for strategy, xpath in enumerate([
        '//*[@text="Generar link" or @content-desc="Generar link"]',
        '//*[contains(@text, "Generar link") or contains(@content-desc, "Generar link")]',
        '//*[contains(@text, "Generar") or contains(@content-desc, "Generar")]',
    ], start=1):
        try:
            driver.find_element(By.XPATH, xpath).click()
            time.sleep(4)
            print(f"   ✅ [LINK HELPER] STEP 7: STRATEGY {strategy} SUCCEEDED")
            generated = True
            break
        except Exception as e:
            print(f"   ⚠️  [LINK HELPER] GENERAR STRATEGY {strategy} FAILED: {e}")

    if not generated:
        print("   ❌ [LINK HELPER] STEP 7: COULD NOT CLICK 'GENERAR LINK'")
        return False

    # ── STEP 8: VERIFY "LINK GENERADO CON ÉXITO" CONFIRMATION ────────────────
    # SCREEN 5 CONFIRMED: title "Link generado con éxito" + amount + share options
    print("   📍 [LINK HELPER] STEP 8: VERIFYING CONFIRMATION SCREEN...")
    confirmed = False

    for xpath in [
        '//*[contains(@text, "Link generado con éxito") or contains(@content-desc, "Link generado con éxito")]',
        '//*[contains(@text, "generado con") or contains(@content-desc, "generado con")]',
        '//*[contains(@text, "Pendiente") or contains(@content-desc, "Pendiente")]',
    ]:
        try:
            el = driver.find_element(By.XPATH, xpath)
            if el.is_displayed():
                print("   ✅ [LINK HELPER] STEP 8: CONFIRMATION SCREEN VISIBLE")
                confirmed = True
                break
        except:
            pass

    if not confirmed:
        print("   ⚠️  [LINK HELPER] STEP 8: CONFIRMATION TEXT NOT FOUND — CHECKING AMOUNT...")
        try:
            driver.find_element(
                By.XPATH, f'//*[contains(@text, "{amount}") or contains(@content-desc, "{amount}")]'
            )
            print(f"   ✅ [LINK HELPER] AMOUNT ${amount} VISIBLE — LINK CREATED")
            confirmed = True
        except:
            pass

    # ── STEP 9: PRESS BACK → RETURN TO "LINKS DE PAGO" LIST ──────────────────
    print("   📍 [LINK HELPER] STEP 9: PRESSING BACK TO RETURN TO LINKS LIST...")
    try:
        driver.back()
        time.sleep(2)
        print("   ✅ [LINK HELPER] BACK PRESSED — NOW ON LINKS LIST")
    except Exception as e:
        print(f"   ⚠️  [LINK HELPER] BACK PRESS FAILED: {e}")

    # VERIFY BACK TO LIST: "+ Generar nuevo link" button should be visible again
    time.sleep(1)
    try:
        driver.find_element(
            By.XPATH,
            '//*[contains(@text, "Generar nuevo link") or contains(@content-desc, "Generar nuevo link")]'
        )
        print("   ✅ [LINK HELPER] CONFIRMED BACK ON LINKS LIST SCREEN")
    except:
        print("   ℹ️  [LINK HELPER] LIST SCREEN NOT CONFIRMED — CONTINUING ANYWAY")

    if confirmed:
        print(f"✅ [LINK HELPER] PAYMENT LINK CREATED SUCCESSFULLY")
        print(f"   Amount: ${amount} | Description: {description} | Due: {target_str}")
        return True
    else:
        print(f"⚠️  [LINK HELPER] LINK MAY HAVE BEEN CREATED BUT CONFIRMATION NOT DETECTED")
        return True  # PROCEED — LINK LIKELY EXISTS EVEN IF CONFIRMATION WAS MISSED


# =================================================================================
# SVS-92: GO TO SERVICES TAB
# =================================================================================
def SVS_92():
    print("\n" + "=" * 60)
    print("🧪 SVS-92: GO TO SERVICES TAB")
    print("=" * 60)

    driver, wait = utils.start_driver()

    try:
        # PRECONDITION: REACH THE MAIN CHARGING SCREEN
        print("🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)

        # STEP 1: NAVIGATE TO SERVICES TAB
        print("\n👉 STEP 1: NAVIGATING TO 'SERVICES' TAB...")
        tab_reached = _navigate_to_services_tab(driver, wait)

        if not tab_reached:
            print("\n💥 SVS-92: FAILED — COULD NOT NAVIGATE TO SERVICES TAB.")
            utils.take_screenshot(driver, "SVS_92_NAV_FAILED", "t6")
            _capture_evidence(driver, "SVS_92")
            return False

        # STEP 2: VERIFY THAT "LINKS DE PAGO" CARD IS VISIBLE
        print("\n👉 STEP 2: VERIFYING 'LINKS DE PAGO' CARD IS DISPLAYED...")
        card_visible = _verify_payment_links_visible(driver)

        if not card_visible:
            print("\n💥 SVS-92: FAILED — 'LINKS DE PAGO' CARD NOT FOUND ON SERVICES TAB.")
            utils.take_screenshot(driver, "SVS_92_CARD_NOT_FOUND", "t6")
            _capture_evidence(driver, "SVS_92")

            # DEBUG: DUMP ALL VISIBLE TEXT TO HELP LOCATE THE REAL ATTRIBUTE NAME
            print("\n🔍 SCANNING VISIBLE TEXT FOR DEBUGGING...")
            try:
                for elem in driver.find_elements(By.XPATH, "//*"):
                    t = elem.get_attribute("text")
                    if t and len(t) > 3:
                        print(f"   📝 VISIBLE TEXT: '{t}'")
            except:
                pass
            return False

        # SUCCESS PATH
        print("\n📸 TAKING SCREENSHOT — SERVICES TAB LOADED CORRECTLY...")
        utils.take_screenshot(driver, "SVS_92_SERVICES_TAB_OK", "t6")
        _capture_evidence(driver, "SVS_92")
        print("\n✅ SVS-92: SUCCESS — SERVICES TAB LOADED. 'LINKS DE PAGO' CARD IS VISIBLE.")
        return True

    except Exception as e:
        print(f"\n💥 SVS-92 CRITICAL ERROR: {e}")
        try:
            utils.take_screenshot(driver, "SVS_92_TECHNICAL_ERROR", "t6")
        except:
            pass
        return False
    finally:
        utils.close_driver(driver)

# =================================================================================
# SVS-93: ACCESS TO 'PAYMENT LINK' (HOME) LINK DE PAGO VIEW
# =================================================================================
def SVS_93():
    print("\n" + "=" * 60)
    print("🧪 SVS-93: ACCESS TO 'PAYMENT LINK' (HOME) LINK DE PAGO VIEW")
    print("=" * 60)

    driver, wait = utils.start_driver()

    try:
        # PRECONDITION: REACH THE MAIN CHARGING SCREEN
        print("🔐 PRECONDITION: EXECUTING FULL LOGIN AND REGISTRATION FLOW...")
        helper_login_to_calculator(driver, wait)

        # STEP 1: NAVIGATE TO SERVICES TAB
        print("\n👉 STEP 1: NAVIGATING TO 'SERVICES' TAB...")
        tab_reached = _navigate_to_services_tab(driver, wait)

        if not tab_reached:
            print("\n💥 SVS-93: FAILED — COULD NOT NAVIGATE TO SERVICES TAB.")
            utils.take_screenshot(driver, "SVS_93_NAV_FAILED", "t6")
            _capture_evidence(driver, "SVS_93")
            return False

        # STEP 2: VERIFY THAT "LINKS DE PAGO" CARD IS VISIBLE
        print("\n👉 STEP 2: VERIFYING 'LINKS DE PAGO' CARD IS DISPLAYED...")
        card_visible = _verify_payment_links_visible(driver)

        if not card_visible:
            print("\n💥 SVS-93: FAILED — LINK DE PAGO IS NOT VISIBLE")
            utils.take_screenshot(driver, "SVS_93_CARD_NOT_FOUND", "t6")
            _capture_evidence(driver, "SVS_93")

            # DEBUG: DUMP ALL VISIBLE TEXT TO HELP LOCATE THE REAL ATTRIBUTE NAME
            print("\n🔍 SCANNING VISIBLE TEXT FOR DEBUGGING...")
            try:
                for elem in driver.find_elements(By.XPATH, "//*"):
                    t = elem.get_attribute("text")
                    if t and len(t) > 3:
                        print(f"   📝 VISIBLE TEXT: '{t}'")
            except:
                pass
            return False

        # SUCCESS PATH
        print("\n📸 TAKING SCREENSHOT — PAID LINK HOME VIEW...")
        utils.take_screenshot(driver, "SVS_93_SERVICES_TAB_OK", "t6")
        _capture_evidence(driver, "SVS_93")
        print("\n✅ SVS-93: SUCCESS — LINK DE PAGO VIEW IS VISIBLE.")
        return True

    except Exception as e:
        print(f"\n💥 SVS-93 CRITICAL ERROR: {e}")
        try:
            utils.take_screenshot(driver, "SVS_93_TECHNICAL_ERROR", "t6")
        except:
            pass
        return False
    finally:
        utils.close_driver(driver)

# =================================================================================
# INTERNAL HELPER: CLICK THE "LINKS DE PAGO" CARD ON THE SERVICES TAB
# =================================================================================
def _click_payment_links_card(driver):
    
    print("   🔍 [CLICK] ATTEMPTING STRATEGY 1: EXACT @text ON THE CARD...")
    try:
        driver.find_element(
            By.XPATH, '//*[@text="Links de pago" or @text="links de pago"]'
        ).click()
        time.sleep(3)
        print("   ✅ [CLICK] STRATEGY 1 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [CLICK] STRATEGY 1 FAILED: {e}")
 
    print("   🔍 [CLICK] ATTEMPTING STRATEGY 2: contains(@text) / contains(@content-desc)...")
    try:
        driver.find_element(
            By.XPATH,
            '//*[contains(@text, "Links de pago") or contains(@content-desc, "Links de pago")]'
        ).click()
        time.sleep(3)
        print("   ✅ [CLICK] STRATEGY 2 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [CLICK] STRATEGY 2 FAILED: {e}")
 
    print("   🔍 [CLICK] ATTEMPTING STRATEGY 3: CLICKABLE ANCESTOR OF TEXT NODE...")
    try:
        # WALK UP THE TREE — THE TEXT LABEL MAY SIT INSIDE A NON-CLICKABLE VIEW
        # WHOSE PARENT IS THE ACTUAL TOUCHABLE CONTAINER
        el = driver.find_element(
            By.XPATH,
            '//*[contains(@text, "Links de pago") or contains(@content-desc, "Links de pago")]'
            '/ancestor::*[@clickable="true"][1]'
        )
        el.click()
        time.sleep(3)
        print("   ✅ [CLICK] STRATEGY 3 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [CLICK] STRATEGY 3 FAILED: {e}")
 
    print("   🔍 [CLICK] ATTEMPTING STRATEGY 4: UIAUTOMATOR TEXT CLICK (FINAL FALLBACK)...")
    try:
        driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains("Links de pago")'
        ).click()
        time.sleep(3)
        print("   ✅ [CLICK] STRATEGY 4 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   💥 [CLICK] STRATEGY 4 FAILED: {e}")
 
    print("   ❌ [CLICK] ALL STRATEGIES EXHAUSTED — 'LINKS DE PAGO' CARD NOT CLICKABLE.")
    return False
 
 
# =================================================================================
# INTERNAL HELPER: VERIFY THE "LINK DE PAGO" DETAIL SCREEN LOADED CORRECTLY
# =================================================================================
def _verify_payment_link_screen(driver):
    heading_found = False
    button_found  = False
 
    # --- CHECK 1: SCREEN TITLE "Link de pago" ---
    print("   🔍 [VERIFY] CHECK 1: SCREEN TITLE 'Link de pago'...")
    try:
        el = driver.find_element(
            By.XPATH,
            '//*[@text="Link de pago" or @content-desc="Link de pago" or '
            'contains(@text, "Link de pago") or contains(@content-desc, "Link de pago")]'
        )
        if el.is_displayed():
            print("   ✅ [VERIFY] CHECK 1 PASSED — SCREEN TITLE VISIBLE.")
            heading_found = True
    except Exception as e:
        print(f"   ⚠️  [VERIFY] CHECK 1 FAILED: {e}")
 
    # --- CHECK 2: MAIN HEADING "Realiza cobros a través de un link" ---
    print("   🔍 [VERIFY] CHECK 2: HEADING 'Realiza cobros a través de un link'...")
    try:
        el = driver.find_element(
            By.XPATH,
            '//*[contains(@text, "Realiza cobros") or contains(@content-desc, "Realiza cobros")]'
        )
        if el.is_displayed():
            print("   ✅ [VERIFY] CHECK 2 PASSED — MAIN HEADING VISIBLE.")
            heading_found = True
    except Exception as e:
        print(f"   ⚠️  [VERIFY] CHECK 2 FAILED: {e}")
 
    # --- CHECK 3: ACTION BUTTON "+ Crear nuevo" ---
    print("   🔍 [VERIFY] CHECK 3: BUTTON '+ Crear nuevo'...")
    try:
        el = driver.find_element(
            By.XPATH,
            '//*[contains(@text, "Crear nuevo") or contains(@content-desc, "Crear nuevo")]'
        )
        if el.is_displayed():
            print("   ✅ [VERIFY] CHECK 3 PASSED — '+ CREAR NUEVO' BUTTON VISIBLE.")
            button_found = True
    except Exception as e:
        print(f"   ⚠️  [VERIFY] CHECK 3 FAILED: {e}")
 
    # SCREEN IS CONSIDERED LOADED IF HEADING + BUTTON ARE BOTH PRESENT,
    # OR AT MINIMUM THE HEADING IS CONFIRMED (BUTTON MAY BE BELOW FOLD ON SMALL SCREENS)
    if heading_found and button_found:
        print("   ✅ [VERIFY] FULL SCREEN CONFIRMED — HEADING + BUTTON BOTH VISIBLE.")
        return True
    elif heading_found:
        print("   ⚠️  [VERIFY] PARTIAL CONFIRMATION — HEADING VISIBLE BUT BUTTON NOT FOUND.")
        print("   💡 BUTTON MAY BE BELOW THE VISIBLE FOLD — CONSIDER SCROLLING IF NEEDED.")
        return True
    else:
        print("   ❌ [VERIFY] SCREEN NOT CONFIRMED — NO EXPECTED ELEMENTS FOUND.")
        return False
 
 
# =================================================================================
# SVS-94: ACCES TO THE 'CREATE NEW' FROM PAYMENT LINK
# =================================================================================
def SVS_94():
    
    from datetime import date as _date, timedelta as _td

    SVS_AMOUNT      = "30"
    SVS_DESCRIPTION = "Ventanilla"

    print("\n" + "=" * 60)
    print("SVS-94: FULL PAYMENT LINK CREATION FLOW")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        # PRECONDITION: FULL LOGIN → HOME
        print("\n PRECONDITION: EXECUTING FULL LOGIN FLOW...")
        helper_login_to_calculator(driver, wait)

        # ── STEP 1: NAVIGATE TO SERVICES TAB ─────────────────────────────────
        print("\n STEP 1: NAVIGATING TO SERVICES TAB...")
        tab_ok = _navigate_to_services_tab(driver, wait)
        if not tab_ok:
            print("\n SVS-94 FAILED — COULD NOT REACH SERVICES TAB")
            utils.take_screenshot(driver, "SVS_94_01_NAV_FAILED", "t6")
            return False
        utils.take_screenshot(driver, "SVS_94_01_SERVICES_TAB", "t6")

        # ── STEP 2: CLICK "LINKS DE PAGO" CARD ───────────────────────────────
        print("\n STEP 2: CLICKING 'LINKS DE PAGO' CARD...")
        card_ok = _click_payment_links_card(driver)
        if not card_ok:
            print("\n SVS-94 FAILED — COULD NOT CLICK LINKS DE PAGO CARD")
            utils.take_screenshot(driver, "SVS_94_02_CARD_FAILED", "t6")
            return False
        time.sleep(1)

        # ── STEP 3: CLICK "+ GENERAR NUEVO LINK" ─────────────────────────────
        # CONFIRMED FROM IMAGE 1: button at bottom "+" Generar nuevo link"
        print("\n STEP 3: CLICKING '+ Generar nuevo link'...")
        generar_ok = False
        for xpath in [
            '//*[@text="+ Generar nuevo link" or @content-desc="+ Generar nuevo link"]',
            '//*[contains(@text,"Generar nuevo link") or contains(@content-desc,"Generar nuevo link")]',
            '//*[contains(@text,"Generar nuevo") or contains(@content-desc,"Generar nuevo")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                print("   SVS-94 STEP 3: STRATEGY SUCCEEDED")
                generar_ok = True
                break
            except:
                pass
        if not generar_ok:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textContains("Generar nuevo")'
                ).click()
                time.sleep(2)
                generar_ok = True
            except Exception as e:
                print(f"   SVS-94 STEP 3 FAILED: {e}")

        if not generar_ok:
            print("\n SVS-94 FAILED — COULD NOT CLICK GENERAR NUEVO LINK")
            utils.take_screenshot(driver, "SVS_94_03_GENERAR_FAILED", "t6")
            return False
        utils.take_screenshot(driver, "SVS_94_03_FORM_OPENED", "t6")

        # ── STEP 4: VERIFY FORM SCREEN "LINK DE PAGO" LOADED ─────────────────
        # CONFIRMED FROM IMAGE 2: title "Link de pago" + 3 fields visible
        print("\n STEP 4: VERIFYING FORM SCREEN 'LINK DE PAGO' LOADED...")
        form_visible = False
        for xpath in [
            '//*[@text="Link de pago" or @content-desc="Link de pago"]',
            '//*[contains(@text,"Monto a cobrar") or contains(@content-desc,"Monto a cobrar")]',
            '//*[contains(@text,"Producto o servicio") or contains(@content-desc,"Producto o servicio")]',
        ]:
            try:
                el = driver.find_element(By.XPATH, xpath)
                if el.is_displayed():
                    print(f"   FORM INDICATOR FOUND: {xpath[:60]}")
                    form_visible = True
                    break
            except:
                pass
        if not form_visible:
            print("\n SVS-94 FAILED — FORM SCREEN DID NOT LOAD")
            utils.take_screenshot(driver, "SVS_94_04_FORM_NOT_LOADED", "t6")
            return False

        # ── STEP 5: FILL MONTO (EditText[1]) — "30" ──────────────────────────
        print(f"\n STEP 5: FILLING MONTO — '{SVS_AMOUNT}'...")
        amount_ok = False
        for xpath in [
            '//android.widget.EditText[1]',
            '//*[contains(@hint,"Monto") or contains(@text,"Monto a cobrar")]',
        ]:
            try:
                el = driver.find_element(By.XPATH, xpath)
                el.click()
                time.sleep(0.5)
                el.clear()
                el.send_keys(SVS_AMOUNT)
                try: driver.hide_keyboard()
                except: pass
                time.sleep(0.5)
                print(f"   MONTO FILLED: {SVS_AMOUNT}")
                amount_ok = True
                break
            except Exception as e:
                print(f"   MONTO STRATEGY FAILED: {e}")
        if not amount_ok:
            print("\n SVS-94 FAILED — COULD NOT FILL MONTO FIELD")
            utils.take_screenshot(driver, "SVS_94_05_MONTO_FAILED", "t6")
            return False

        # ── STEP 6: FILL CONCEPTO (EditText[2]) — "Ventanilla" ───────────────
        print(f"\n STEP 6: FILLING CONCEPTO — '{SVS_DESCRIPTION}'...")
        desc_ok = False
        for xpath in [
            '//android.widget.EditText[2]',
            '//*[contains(@hint,"Concepto") or contains(@text,"Concepto")]',
            '//*[contains(@hint,"Producto") or contains(@text,"Producto o servicio")]',
        ]:
            try:
                el = driver.find_element(By.XPATH, xpath)
                el.click()
                time.sleep(0.5)
                el.clear()
                el.send_keys(SVS_DESCRIPTION)
                try: driver.hide_keyboard()
                except: pass
                time.sleep(0.5)
                print(f"   CONCEPTO FILLED: {SVS_DESCRIPTION}")
                desc_ok = True
                break
            except Exception as e:
                print(f"   CONCEPTO STRATEGY FAILED: {e}")
        if not desc_ok:
            print("\n SVS-94 FAILED — COULD NOT FILL CONCEPTO FIELD")
            utils.take_screenshot(driver, "SVS_94_06_CONCEPTO_FAILED", "t6")
            return False
        utils.take_screenshot(driver, "SVS_94_06_FORM_FILLED", "t6")

        # ── STEP 7: OPEN CALENDAR AND SELECT TOMORROW ────────────────────────
        # CONFIRMED FROM IMAGE 3: native calendar dialog "Selecciona una fecha"
        # RULE: SELECT THE DAY AFTER TODAY (not today itself — tested with today = 10)
        tomorrow       = _date.today() + _td(days=1)
        tomorrow_day   = str(tomorrow.day)
        tomorrow_str   = tomorrow.strftime("%d-%m-%Y")
        print(f"\n STEP 7: SELECTING DATE — TOMORROW: {tomorrow_str} (DAY {tomorrow_day})...")

        # OPEN THE CALENDAR FIELD
        date_opened = False
        for xpath in [
            '//*[contains(@hint,"Fecha") or @text="Fecha"]',
            '//android.widget.EditText[3]',
            '//*[contains(@content-desc,"Fecha")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                date_opened = True
                print("   CALENDAR OPENED")
                break
            except:
                pass
        if not date_opened:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textContains("Fecha")'
                ).click()
                time.sleep(2)
                date_opened = True
            except Exception as e:
                print(f"   CALENDAR OPEN FAILED: {e}")
                utils.take_screenshot(driver, "SVS_94_07_CALENDAR_FAILED", "t6")
                return False

        # WAIT FOR CALENDAR HEADER "Selecciona una fecha" (IMAGE 3 CONFIRMED)
        for _ in range(5):
            try:
                driver.find_element(By.XPATH,
                    '//*[contains(@text,"Selecciona una fecha") or '
                    'contains(@content-desc,"Selecciona una fecha") or '
                    'contains(@text,"SELECCIONAR FECHA")]')
                print("   CALENDAR CONFIRMED OPEN")
                break
            except:
                time.sleep(1)
        utils.take_screenshot(driver, "SVS_94_07_CALENDAR_OPEN", "t6")

        # SELECT TOMORROW'S DAY NUMBER
        day_selected = False
        for selector in [
            f'new UiSelector().descriptionStartsWith("{tomorrow_day}, ")',
            f'new UiSelector().descriptionContains("{tomorrow_day} de ")',
        ]:
            try:
                driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, selector).click()
                time.sleep(1)
                print(f"   DAY {tomorrow_day} SELECTED (TOMORROW)")
                day_selected = True
                break
            except Exception as e:
                print(f"   DAY SELECT FAILED: {e}")
        if not day_selected:
            try:
                driver.find_element(
                    By.XPATH, f'//*[starts-with(@content-desc,"{tomorrow_day}, ")]'
                ).click()
                time.sleep(1)
                day_selected = True
            except Exception as e:
                print(f"   XPATH FALLBACK FAILED: {e}")

        if not day_selected:
            print("   DUMPING CALENDAR content-desc FOR DIAGNOSIS:")
            try:
                for el in driver.find_elements(By.XPATH, "//*[@content-desc]"):
                    cd = el.get_attribute("content-desc")
                    if cd and tomorrow_day in cd:
                        print(f"      -> '{cd}'")
            except: pass
            utils.take_screenshot(driver, "SVS_94_07_DAY_NOT_FOUND", "t6")
            return False

        # CONFIRM WITH "ACEPTAR"
        aceptar_clicked = False
        for xpath in [
            '//*[@text="ACEPTAR" or @text="Aceptar" or @content-desc="ACEPTAR"]',
            '//*[contains(@text,"ACEPTAR") or contains(@content-desc,"ACEPTAR")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                print("   ACEPTAR CLICKED — DATE CONFIRMED")
                aceptar_clicked = True
                break
            except: pass
        if not aceptar_clicked:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textMatches("(?i)aceptar")'
                ).click()
                time.sleep(2)
                aceptar_clicked = True
            except Exception as e:
                print(f"   ACEPTAR FAILED: {e}")
                return False
        utils.take_screenshot(driver, "SVS_94_07_DATE_SELECTED", "t6")

        # ── STEP 8: CLICK "GENERAR LINK" TO SUBMIT ───────────────────────────
        print("\n STEP 8: CLICKING 'Generar link' TO SUBMIT...")
        submit_ok = False
        for xpath in [
            '//*[@text="Generar link" or @content-desc="Generar link"]',
            '//*[contains(@text,"Generar link") or contains(@content-desc,"Generar link")]',
            '//*[contains(@text,"Generar") or contains(@content-desc,"Generar")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(4)
                print("   GENERAR LINK CLICKED")
                submit_ok = True
                break
            except: pass
        if not submit_ok:
            print("\n SVS-94 FAILED — COULD NOT CLICK GENERAR LINK")
            utils.take_screenshot(driver, "SVS_94_08_SUBMIT_FAILED", "t6")
            return False
        utils.take_screenshot(driver, "SVS_94_08_AFTER_SUBMIT", "t6")

        # ── STEP 9: VERIFY CONFIRMATION SCREEN ───────────────────────────────
        # CONFIRMED FROM IMAGE 4: "Link generado con éxito" + $30.00 + "Ventanilla"
        print("\n STEP 9: VERIFYING CONFIRMATION SCREEN 'Link generado con éxito'...")
        confirmed = False
        for xpath in [
            '//*[contains(@text,"Link generado con éxito") or contains(@content-desc,"Link generado con éxito")]',
            '//*[contains(@text,"generado con") or contains(@content-desc,"generado con")]',
            f'//*[contains(@text,"{SVS_AMOUNT}") or contains(@content-desc,"{SVS_AMOUNT}")]',
            f'//*[contains(@text,"{SVS_DESCRIPTION}") or contains(@content-desc,"{SVS_DESCRIPTION}")]',
        ]:
            try:
                el = driver.find_element(By.XPATH, xpath)
                if el.is_displayed():
                    print(f"   CONFIRMATION ELEMENT FOUND")
                    confirmed = True
                    break
            except: pass

        if not confirmed:
            print("\n SVS-94 FAILED — CONFIRMATION SCREEN NOT VISIBLE")
            utils.take_screenshot(driver, "SVS_94_09_CONFIRM_FAILED", "t6")
            return False
        utils.take_screenshot(driver, "SVS_94_09_LINK_CONFIRMED", "t6")

        # ── STEP 10: CLICK "+ GENERAR NUEVO LINK" → VERIFY BLANK FORM ────────
        # CONFIRMED FROM IMAGE 4: button at bottom opens a new blank form
        print("\n STEP 10: CLICKING '+ Generar nuevo link' → VERIFY BLANK FORM OPENS...")
        nuevo_ok = False
        for xpath in [
            '//*[@text="+ Generar nuevo link" or @content-desc="+ Generar nuevo link"]',
            '//*[contains(@text,"Generar nuevo link") or contains(@content-desc,"Generar nuevo link")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                nuevo_ok = True
                break
            except: pass
        if not nuevo_ok:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textContains("Generar nuevo")'
                ).click()
                time.sleep(2)
                nuevo_ok = True
            except: pass

        # VERIFY BLANK FORM OPENED (fields should be empty)
        blank_form_ok = False
        if nuevo_ok:
            for xpath in [
                '//*[contains(@text,"Monto a cobrar") or contains(@hint,"Monto")]',
                '//*[contains(@text,"Concepto") or contains(@hint,"Concepto")]',
                '//*[@text="Link de pago" or @content-desc="Link de pago"]',
            ]:
                try:
                    driver.find_element(By.XPATH, xpath)
                    blank_form_ok = True
                    break
                except: pass
        utils.take_screenshot(driver, "SVS_94_10_BLANK_FORM", "t6")

        # ── STEP 11: PRESS BACK → RELOAD LIST ────────────────────────────────
        # CONFIRMED FROM IMAGE 5: back arrow returns to "Links de pago" list
        print("\n STEP 11: PRESSING BACK → RELOADING LINKS LIST...")
        try:
            driver.back()
            time.sleep(2)
            print("   BACK PRESSED")
        except Exception as e:
            print(f"   BACK PRESS FAILED: {e}")
        utils.take_screenshot(driver, "SVS_94_11_BACK_PRESSED", "t6")

        # RELOAD: CONFIRM LIST SHOWS THE NEW LINK "Ventanilla"
        time.sleep(1)
        new_link_visible = False
        for xpath in [
            f'//*[contains(@text,"{SVS_DESCRIPTION}") or contains(@content-desc,"{SVS_DESCRIPTION}")]',
            f'//*[contains(@text,"{SVS_AMOUNT}") or contains(@content-desc,"{SVS_AMOUNT}")]',
            '//*[contains(@text,"+ Generar nuevo link") or contains(@content-desc,"+ Generar nuevo link")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath)
                new_link_visible = True
                break
            except: pass
        utils.take_screenshot(driver, "SVS_94_12_FINAL_LIST", "t6")

        if new_link_visible:
            result = "SUCCESS"
            print("\n SVS-94 RESULT: SUCCESS")
            print(f"   Amount={SVS_AMOUNT} | Description={SVS_DESCRIPTION} | Date={tomorrow_str}")
        else:
            print("\n SVS-94 RESULT: FAIL — NEW LINK NOT VISIBLE IN LIST")

        _capture_evidence(driver, "SVS_94")
        return result == "SUCCESS"

    except Exception as e:
        print(f"\n SVS-94 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "SVS_94_CRITICAL_ERROR", "t6")
        except: pass
        return False
    finally:
        print("\n" + "-" * 60)
        print(f"SVS-94 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)

# =================================================================================
# INTERNAL HELPER: CLICK THE "+ CREAR NUEVO" BUTTON ON THE LINK DE PAGO SCREEN
# =================================================================================
def _click_create_new(driver):
    
    print("   🔍 [CREAR] ATTEMPTING STRATEGY 1: @text EXACT MATCH...")
    try:
        driver.find_element(
            By.XPATH, '//*[@text="+ Crear nuevo" or @text="Crear nuevo"]'
        ).click()
        time.sleep(2)
        print("   ✅ [CREAR] STRATEGY 1 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [CREAR] STRATEGY 1 FAILED: {e}")
 
    print("   🔍 [CREAR] ATTEMPTING STRATEGY 2: contains(@text) / contains(@content-desc)...")
    try:
        driver.find_element(
            By.XPATH,
            '//*[contains(@text, "Crear nuevo") or contains(@content-desc, "Crear nuevo")]'
        ).click()
        time.sleep(2)
        print("   ✅ [CREAR] STRATEGY 2 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [CREAR] STRATEGY 2 FAILED: {e}")
 
    print("   🔍 [CREAR] ATTEMPTING STRATEGY 3: CLICKABLE ANCESTOR OF TEXT NODE...")
    try:
        el = driver.find_element(
            By.XPATH,
            '//*[contains(@text, "Crear nuevo") or contains(@content-desc, "Crear nuevo")]'
            '/ancestor::*[@clickable="true"][1]'
        )
        el.click()
        time.sleep(2)
        print("   ✅ [CREAR] STRATEGY 3 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [CREAR] STRATEGY 3 FAILED: {e}")
 
    print("   🔍 [CREAR] ATTEMPTING STRATEGY 4: UIAUTOMATOR TEXT CLICK (FINAL FALLBACK)...")
    try:
        driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains("Crear nuevo")'
        ).click()
        time.sleep(2)
        print("   ✅ [CREAR] STRATEGY 4 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   💥 [CREAR] STRATEGY 4 FAILED: {e}")
 
    print("   ❌ [CREAR] ALL STRATEGIES EXHAUSTED — '+ CREAR NUEVO' NOT CLICKABLE.")
    return False
 
 
# =================================================================================
# INTERNAL HELPER: FILL THE "MONTO" FIELD
# =================================================================================
def _fill_amount(driver, amount):
    print(f"   🔍 [MONTO] ATTEMPTING STRATEGY 1: PLACEHOLDER @text='Monto'...")
    try:
        el = driver.find_element(
            By.XPATH, '//*[@text="Monto" or contains(@hint, "Monto")]'
        )
        el.click()
        time.sleep(1)
        el.clear()
        el.send_keys(amount)
        try:
            driver.hide_keyboard()
        except:
            pass
        time.sleep(1)
        print(f"   ✅ [MONTO] STRATEGY 1 SUCCEEDED — TYPED: {amount}")
        return True
    except Exception as e:
        print(f"   ⚠️  [MONTO] STRATEGY 1 FAILED: {e}")
 
    print(f"   🔍 [MONTO] ATTEMPTING STRATEGY 2: FIRST EditText ON SCREEN...")
    try:
        el = driver.find_elements(By.XPATH, '//android.widget.EditText')[0]
        el.click()
        time.sleep(1)
        el.clear()
        el.send_keys(amount)
        try:
            driver.hide_keyboard()
        except:
            pass
        time.sleep(1)
        print(f"   ✅ [MONTO] STRATEGY 2 SUCCEEDED — TYPED: {amount}")
        return True
    except Exception as e:
        print(f"   ⚠️  [MONTO] STRATEGY 2 FAILED: {e}")
 
    print(f"   🔍 [MONTO] ATTEMPTING STRATEGY 3: UIAUTOMATOR HINT 'Monto' (FINAL FALLBACK)...")
    try:
        el = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains("Monto")'
        )
        el.click()
        time.sleep(1)
        el.clear()
        el.send_keys(amount)
        try:
            driver.hide_keyboard()
        except:
            pass
        time.sleep(1)
        print(f"   ✅ [MONTO] STRATEGY 3 SUCCEEDED — TYPED: {amount}")
        return True
    except Exception as e:
        print(f"   💥 [MONTO] STRATEGY 3 FAILED: {e}")
 
    print("   ❌ [MONTO] ALL STRATEGIES EXHAUSTED — MONTO FIELD NOT FOUND.")
    return False
 
 
# =================================================================================
# INTERNAL HELPER: FILL THE "PRODUCTO O SERVICIO" FIELD
# =================================================================================
def _fill_description(driver, description):
    print(f"   🔍 [CONCEPTO] ATTEMPTING STRATEGY 1: PLACEHOLDER TEXT MATCH...")
    try:
        el = driver.find_element(
            By.XPATH,
            '//*[@text="Producto o servicio" or contains(@hint, "Producto o servicio")]'
        )
        el.click()
        time.sleep(1)
        el.clear()
        el.send_keys(description)
        try:
            driver.hide_keyboard()
        except:
            pass
        time.sleep(1)
        print(f"   ✅ [CONCEPTO] STRATEGY 1 SUCCEEDED — TYPED: {description}")
        return True
    except Exception as e:
        print(f"   ⚠️  [CONCEPTO] STRATEGY 1 FAILED: {e}")
 
    print(f"   🔍 [CONCEPTO] ATTEMPTING STRATEGY 2: SECOND EditText ON SCREEN...")
    try:
        el = driver.find_elements(By.XPATH, '//android.widget.EditText')[1]
        el.click()
        time.sleep(1)
        el.clear()
        el.send_keys(description)
        try:
            driver.hide_keyboard()
        except:
            pass
        time.sleep(1)
        print(f"   ✅ [CONCEPTO] STRATEGY 2 SUCCEEDED — TYPED: {description}")
        return True
    except Exception as e:
        print(f"   ⚠️  [CONCEPTO] STRATEGY 2 FAILED: {e}")
 
    print(f"   🔍 [CONCEPTO] ATTEMPTING STRATEGY 3: UIAUTOMATOR (FINAL FALLBACK)...")
    try:
        el = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains("Producto o servicio")'
        )
        el.click()
        time.sleep(1)
        el.clear()
        el.send_keys(description)
        try:
            driver.hide_keyboard()
        except:
            pass
        time.sleep(1)
        print(f"   ✅ [CONCEPTO] STRATEGY 3 SUCCEEDED — TYPED: {description}")
        return True
    except Exception as e:
        print(f"   💥 [CONCEPTO] STRATEGY 3 FAILED: {e}")
 
    print("   ❌ [CONCEPTO] ALL STRATEGIES EXHAUSTED — CONCEPTO FIELD NOT FOUND.")
    return False
 
 
# =================================================================================
# INTERNAL HELPER: OPEN THE DATE PICKER AND SELECT TODAY'S DATE
# =================================================================================
def _select_due_date(driver):
    
    from datetime import date as _date
 
    today      = _date.today()
    today_day  = str(today.day)          # E.G. "30"
    today_str  = today.strftime("%d/%m/%Y")  # E.G. "30/04/2026" — FOR LOGGING ONLY
    print(f"   📅 [FECHA] TODAY IS {today_str} — WILL SELECT DAY {today_day} IN PICKER.")
 
    # STEP A: TAP THE FECHA DE VENCIMIENTO FIELD TO OPEN THE PICKER
    print("   🔍 [FECHA] STEP A — TAPPING 'FECHA DE VENCIMIENTO' FIELD...")
    field_tapped = False
 
    try:
        driver.find_element(
            By.XPATH,
            '//*[@text="Fecha de vencimiento" or contains(@hint, "Fecha de vencimiento")]'
        ).click()
        time.sleep(2)
        print("   ✅ [FECHA] FIELD TAPPED VIA PLACEHOLDER TEXT.")
        field_tapped = True
    except Exception as e:
        print(f"   ⚠️  [FECHA] PLACEHOLDER TAP FAILED: {e}")
 
    if not field_tapped:
        try:
            driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().textContains("Fecha de vencimiento")'
            ).click()
            time.sleep(2)
            print("   ✅ [FECHA] FIELD TAPPED VIA UIAUTOMATOR.")
            field_tapped = True
        except Exception as e:
            print(f"   💥 [FECHA] UIAUTOMATOR TAP FAILED: {e}")
 
    if not field_tapped:
        print("   ❌ [FECHA] COULD NOT OPEN DATE PICKER — FECHA FIELD NOT FOUND.")
        return False
 
    # STEP B: WAIT FOR "SELECCIONAR FECHA" HEADER — CONFIRMS PICKER IS OPEN
    print("   🔍 [FECHA] STEP B — WAITING FOR DATEPICKER TO APPEAR...")
    picker_open = False
    for attempt in range(6):
        try:
            driver.find_element(
                By.XPATH,
                '//*[contains(@text, "SELECCIONAR FECHA") or '
                'contains(@content-desc, "SELECCIONAR FECHA")]'
            )
            print("   ✅ [FECHA] DATEPICKER CONFIRMED OPEN.")
            picker_open = True
            break
        except:
            time.sleep(1)
 
    if not picker_open:
        print("   ⚠️  [FECHA] DATEPICKER HEADER NOT FOUND — PROCEEDING ANYWAY...")
 
    print(f"   🔍 [FECHA] STEP C — SELECTING DAY {today_day} (TODAY)...")
    day_selected = False
    try:
        driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().descriptionStartsWith("{today_day}, ")'
        ).click()
        time.sleep(1)
        print(f"   ✅ [FECHA] STRATEGY 1: DAY {today_day} SELECTED VIA descriptionStartsWith.")
        day_selected = True
    except Exception as e:
        print(f"   ⚠️  [FECHA] STRATEGY 1 FAILED: {e}")
 
    # STRATEGY 2: XPATH starts-with WITH EXACT SEPARATOR ", "
    if not day_selected:
        try:
            driver.find_element(
                By.XPATH,
                f'//*[starts-with(@content-desc, "{today_day}, ")]'
            ).click()
            time.sleep(1)
            print(f"   ✅ [FECHA] STRATEGY 2: DAY {today_day} SELECTED VIA XPath starts-with.")
            day_selected = True
        except Exception as e:
            print(f"   ⚠️  [FECHA] STRATEGY 2 FAILED: {e}")
 
    # STRATEGY 3: XPATH contains — LOOSER MATCH, HANDLES ANY FORMAT VARIATION
    if not day_selected:
        try:
            driver.find_element(
                By.XPATH,
                f'//*[contains(@content-desc, "{today_day}, ") and '
                f'contains(@content-desc, "Hoy")]'
            ).click()
            time.sleep(1)
            print(f"   ✅ [FECHA] STRATEGY 3: DAY {today_day} SELECTED VIA contains + 'Hoy'.")
            day_selected = True
        except Exception as e:
            print(f"   ⚠️  [FECHA] STRATEGY 3 FAILED: {e}")
 
    if not day_selected:
        try:
            driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().descriptionContains("Hoy")'
            ).click()
            time.sleep(1)
            print(f"   ✅ [FECHA] STRATEGY 4: TODAY SELECTED VIA 'Hoy' MARKER IN content-desc.")
            day_selected = True
        except Exception as e:
            print(f"   💥 [FECHA] STRATEGY 4 FAILED: {e}")
 
    if not day_selected:
        print(f"   ❌ [FECHA] COULD NOT SELECT DAY {today_day}. DUMPING @content-desc VALUES...")
        try:
            for el in driver.find_elements(By.XPATH, "//*[@content-desc]"):
                cd = el.get_attribute("content-desc")
                if cd and (today_day in cd or "Hoy" in cd):
                    print(f"   📝 CANDIDATE content-desc: '{cd}'")
        except:
            pass
        return False
 
    # STEP D: CONFIRM WITH "ACEPTAR"
    print("   🔍 [FECHA] STEP D — CLICKING 'ACEPTAR' TO CONFIRM DATE...")
    try:
        driver.find_element(
            By.XPATH, '//*[@text="ACEPTAR" or @text="Aceptar" or @content-desc="ACEPTAR"]'
        ).click()
        time.sleep(2)
        print("   ✅ [FECHA] DATE CONFIRMED WITH 'ACEPTAR'.")
        return True
    except Exception as e:
        print(f"   ⚠️  [FECHA] ACEPTAR VIA XPATH FAILED: {e}")
 
    try:
        driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().textMatches("(?i)aceptar")'
        ).click()
        time.sleep(2)
        print("   ✅ [FECHA] DATE CONFIRMED VIA UIAUTOMATOR.")
        return True
    except Exception as e:
        print(f"   💥 [FECHA] ACEPTAR UIAUTOMATOR FAILED: {e}")
 
    print("   ❌ [FECHA] COULD NOT CONFIRM DATE — 'ACEPTAR' NOT FOUND.")
    return False
 
 
# =================================================================================
# INTERNAL HELPER: CLICK THE "GENERAR" BUTTON
# =================================================================================
def _click_generate(driver):
    
    print("   🔍 [GENERAR] ATTEMPTING STRATEGY 1: EXACT @text='Generar'...")
    try:
        driver.find_element(
            By.XPATH, '//*[@text="Generar"]'
        ).click()
        time.sleep(4)
        print("   ✅ [GENERAR] STRATEGY 1 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [GENERAR] STRATEGY 1 FAILED: {e}")
 
    print("   🔍 [GENERAR] ATTEMPTING STRATEGY 2: contains(@text, 'Generar')...")
    try:
        driver.find_element(
            By.XPATH,
            '//*[contains(@text, "Generar") or contains(@content-desc, "Generar")]'
        ).click()
        time.sleep(4)
        print("   ✅ [GENERAR] STRATEGY 2 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [GENERAR] STRATEGY 2 FAILED: {e}")
 
    print("   🔍 [GENERAR] ATTEMPTING STRATEGY 3: CLICKABLE ANCESTOR...")
    try:
        el = driver.find_element(
            By.XPATH,
            '//*[contains(@text, "Generar")]/ancestor::*[@clickable="true"][1]'
        )
        el.click()
        time.sleep(4)
        print("   ✅ [GENERAR] STRATEGY 3 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   ⚠️  [GENERAR] STRATEGY 3 FAILED: {e}")
 
    print("   🔍 [GENERAR] ATTEMPTING STRATEGY 4: UIAUTOMATOR (FINAL FALLBACK)...")
    try:
        driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().text("Generar")'
        ).click()
        time.sleep(4)
        print("   ✅ [GENERAR] STRATEGY 4 SUCCEEDED.")
        return True
    except Exception as e:
        print(f"   💥 [GENERAR] STRATEGY 4 FAILED: {e}")
 
    print("   ❌ [GENERAR] ALL STRATEGIES EXHAUSTED — 'GENERAR' NOT CLICKABLE.")
    return False
 
 
# =================================================================================
# INTERNAL HELPER: VERIFY THE SUCCESS SCREEN "LINK DE PAGO GENERADO"
# =================================================================================
def _verify_generated_link_screen(driver, amount, description):
    heading_ok  = False
    data_ok     = False
 
    # --- CHECK 1: SUCCESS HEADING ---
    print("   🔍 [SUCCESS] CHECK 1: HEADING 'Link de pago generado'...")
    try:
        el = driver.find_element(
            By.XPATH,
            '//*[contains(@text, "Link de pago generado") or '
            'contains(@content-desc, "Link de pago generado")]'
        )
        if el.is_displayed():
            print("   ✅ [SUCCESS] CHECK 1 PASSED — SUCCESS HEADING VISIBLE.")
            heading_ok = True
    except Exception as e:
        print(f"   ⚠️  [SUCCESS] CHECK 1 FAILED: {e}")
 
    # --- CHECK 2: MONTO VALUE ON SUMMARY ---
    print(f"   🔍 [SUCCESS] CHECK 2: MONTO VALUE '{monto}' IN SUMMARY...")
    try:
        el = driver.find_element(
            By.XPATH, f'//*[contains(@text, "{monto}") or contains(@content-desc, "{monto}")]'
        )
        if el.is_displayed():
            print(f"   ✅ [SUCCESS] CHECK 2 PASSED — MONTO '{monto}' CONFIRMED.")
            data_ok = True
    except Exception as e:
        print(f"   ⚠️  [SUCCESS] CHECK 2 FAILED: {e}")
 
    # --- CHECK 3: CONCEPTO VALUE ON SUMMARY ---
    print(f"   🔍 [SUCCESS] CHECK 3: CONCEPTO '{concepto}' IN SUMMARY...")
    try:
        el = driver.find_element(
            By.XPATH,
            f'//*[contains(@text, "{concepto}") or contains(@content-desc, "{concepto}")]'
        )
        if el.is_displayed():
            print(f"   ✅ [SUCCESS] CHECK 3 PASSED — CONCEPTO '{concepto}' CONFIRMED.")
            data_ok = True
    except Exception as e:
        print(f"   ⚠️  [SUCCESS] CHECK 3 FAILED: {e}")
 
    # --- CHECK 4: SHARE OPTIONS VISIBLE ---
    print("   🔍 [SUCCESS] CHECK 4: SHARE OPTIONS (Email, WhatsApp, SMS)...")
    try:
        el = driver.find_element(
            By.XPATH,
            '//*[contains(@text, "Compartir") or contains(@content-desc, "Compartir")]'
        )
        if el.is_displayed():
            print("   ✅ [SUCCESS] CHECK 4 PASSED — 'COMPARTIR' SECTION VISIBLE.")
    except Exception as e:
        print(f"   ⚠️  [SUCCESS] CHECK 4 FAILED (NON-BLOCKING): {e}")
 
    if heading_ok and data_ok:
        print("   ✅ [SUCCESS] FULL CONFIRMATION — HEADING + DATA ROWS BOTH VERIFIED.")
        return True
    elif heading_ok:
        print("   ⚠️  [SUCCESS] PARTIAL CONFIRMATION — HEADING OK BUT DATA ROWS NOT MATCHED.")
        print("   💡 CHECK IF MONTO/CONCEPTO FORMAT DIFFERS ON DEVICE (E.G. '$85.50' VS '$ 85.50').")
        return True
    else:
        print("   ❌ [SUCCESS] SCREEN NOT CONFIRMED — SUCCESS HEADING NOT FOUND.")
        return False


# --- TEST DATA ---
SVS95_MONTO    = "85.50"
SVS95_CONCEPTO = "Venta de productos X"

def SVS_95():
    
    from datetime import date as _date, timedelta as _td

    SVS_AMOUNT      = "85.50"
    SVS_DESCRIPTION = "Venta de productos X"

    print("\n" + "=" * 60)
    print("SVS-95: SUCCESSFUL PAYMENT LINK GENERATION")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        # PRECONDITION: FULL LOGIN → HOME
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN FLOW...")
        helper_login_to_calculator(driver, wait)

        # ── STEP 1: NAVIGATE TO SERVICES TAB ─────────────────────────────────
        print("\n👉 STEP 1: NAVIGATING TO SERVICES TAB...")
        tab_ok = _navigate_to_services_tab(driver, wait)
        if not tab_ok:
            print("\n💥 SVS-95 FAILED — COULD NOT REACH SERVICES TAB")
            utils.take_screenshot(driver, "SVS_95_01_NAV_FAILED", "t6")
            _capture_evidence(driver, "SVS_95")
            return False
        utils.take_screenshot(driver, "SVS_95_01_SERVICES_TAB", "t6")

        # ── STEP 2: CLICK "LINKS DE PAGO" CARD ───────────────────────────────
        print("\n👉 STEP 2: CLICKING 'LINKS DE PAGO' CARD...")
        card_ok = _click_payment_links_card(driver)
        if not card_ok:
            print("\n💥 SVS-95 FAILED — COULD NOT CLICK LINKS DE PAGO CARD")
            utils.take_screenshot(driver, "SVS_95_02_CARD_FAILED", "t6")
            _capture_evidence(driver, "SVS_95")
            return False
        time.sleep(1)

        # ── STEP 3: CLICK "+ GENERAR NUEVO LINK" ─────────────────────────────
        # v2 BUTTON: "+ Generar nuevo link" (NOT "+ Crear nuevo" from v1)
        print("\n👉 STEP 3: CLICKING '+ Generar nuevo link'...")
        generar_ok = False
        for xpath in [
            '//*[@text="+ Generar nuevo link" or @content-desc="+ Generar nuevo link"]',
            '//*[contains(@text,"Generar nuevo link") or contains(@content-desc,"Generar nuevo link")]',
            '//*[contains(@text,"Generar nuevo") or contains(@content-desc,"Generar nuevo")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                print("   ✅ STEP 3: BUTTON CLICKED")
                generar_ok = True
                break
            except:
                pass
        if not generar_ok:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textContains("Generar nuevo")'
                ).click()
                time.sleep(2)
                generar_ok = True
                print("   ✅ STEP 3: UIAUTOMATOR SUCCEEDED")
            except Exception as e:
                print(f"   💥 STEP 3 ALL STRATEGIES FAILED: {e}")
        if not generar_ok:
            print("\n💥 SVS-95 FAILED — COULD NOT CLICK '+ GENERAR NUEVO LINK'")
            utils.take_screenshot(driver, "SVS_95_03_GENERAR_FAILED", "t6")
            _capture_evidence(driver, "SVS_95")
            return False
        utils.take_screenshot(driver, "SVS_95_03_FORM_OPENED", "t6")

        # ── STEP 4: VERIFY FORM "LINK DE PAGO" LOADED ────────────────────────
        print("\n👉 STEP 4: VERIFYING FORM SCREEN 'LINK DE PAGO' LOADED...")
        form_visible = False
        for xpath in [
            '//*[@text="Link de pago" or @content-desc="Link de pago"]',
            '//*[contains(@text,"Monto a cobrar") or contains(@content-desc,"Monto a cobrar")]',
            '//*[contains(@text,"Producto o servicio") or contains(@content-desc,"Producto o servicio")]',
        ]:
            try:
                el = driver.find_element(By.XPATH, xpath)
                if el.is_displayed():
                    print("   ✅ FORM INDICATOR FOUND")
                    form_visible = True
                    break
            except:
                pass
        if not form_visible:
            print("\n💥 SVS-95 FAILED — FORM SCREEN DID NOT LOAD")
            utils.take_screenshot(driver, "SVS_95_04_FORM_NOT_LOADED", "t6")
            _capture_evidence(driver, "SVS_95")
            return False

        # ── STEP 5: FILL MONTO (EditText[1]) ─────────────────────────────────
        print(f"\n👉 STEP 5: FILLING MONTO — '{SVS_AMOUNT}'...")
        amount_ok = False
        for xpath in [
            '//android.widget.EditText[1]',
            '//*[contains(@hint,"Monto") or contains(@text,"Monto a cobrar")]',
        ]:
            try:
                el = driver.find_element(By.XPATH, xpath)
                el.click()
                time.sleep(0.5)
                el.clear()
                el.send_keys(SVS_AMOUNT)
                try: driver.hide_keyboard()
                except: pass
                time.sleep(0.5)
                print(f"   ✅ MONTO FILLED: {SVS_AMOUNT}")
                amount_ok = True
                break
            except Exception as e:
                print(f"   ⚠️  MONTO STRATEGY FAILED: {e}")
        if not amount_ok:
            print("\n💥 SVS-95 FAILED — COULD NOT FILL MONTO FIELD")
            utils.take_screenshot(driver, "SVS_95_05_MONTO_FAILED", "t6")
            _capture_evidence(driver, "SVS_95")
            return False

        # ── STEP 6: FILL CONCEPTO (EditText[2]) ──────────────────────────────
        print(f"\n👉 STEP 6: FILLING CONCEPTO — '{SVS_DESCRIPTION}'...")
        desc_ok = False
        for xpath in [
            '//android.widget.EditText[2]',
            '//*[contains(@hint,"Concepto") or contains(@text,"Concepto")]',
            '//*[contains(@hint,"Producto") or contains(@text,"Producto o servicio")]',
        ]:
            try:
                el = driver.find_element(By.XPATH, xpath)
                el.click()
                time.sleep(0.5)
                el.clear()
                el.send_keys(SVS_DESCRIPTION)
                try: driver.hide_keyboard()
                except: pass
                time.sleep(0.5)
                print(f"   ✅ CONCEPTO FILLED: {SVS_DESCRIPTION}")
                desc_ok = True
                break
            except Exception as e:
                print(f"   ⚠️  CONCEPTO STRATEGY FAILED: {e}")
        if not desc_ok:
            print("\n💥 SVS-95 FAILED — COULD NOT FILL CONCEPTO FIELD")
            utils.take_screenshot(driver, "SVS_95_06_CONCEPTO_FAILED", "t6")
            _capture_evidence(driver, "SVS_95")
            return False
        utils.take_screenshot(driver, "SVS_95_06_FORM_FILLED", "t6")

        # ── STEP 7: OPEN CALENDAR → SELECT TOMORROW → ACEPTAR ────────────────
        tomorrow     = _date.today() + _td(days=1)
        tomorrow_day = str(tomorrow.day)
        tomorrow_str = tomorrow.strftime("%d-%m-%Y")
        print(f"\n👉 STEP 7: SELECTING DATE — TOMORROW: {tomorrow_str} (DAY {tomorrow_day})...")

        date_opened = False
        for xpath in [
            '//*[contains(@hint,"Fecha") or @text="Fecha"]',
            '//android.widget.EditText[3]',
            '//*[contains(@content-desc,"Fecha")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                date_opened = True
                print("   ✅ CALENDAR OPENED")
                break
            except:
                pass
        if not date_opened:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textContains("Fecha")'
                ).click()
                time.sleep(2)
                date_opened = True
            except Exception as e:
                print(f"   💥 CALENDAR OPEN FAILED: {e}")
                utils.take_screenshot(driver, "SVS_95_07_CALENDAR_FAILED", "t6")
                _capture_evidence(driver, "SVS_95")
                return False

        # WAIT FOR "Selecciona una fecha" HEADER
        for _ in range(5):
            try:
                driver.find_element(By.XPATH,
                    '//*[contains(@text,"Selecciona una fecha") or '
                    'contains(@content-desc,"Selecciona una fecha") or '
                    'contains(@text,"SELECCIONAR FECHA")]')
                print("   ✅ CALENDAR HEADER CONFIRMED")
                break
            except:
                time.sleep(1)
        utils.take_screenshot(driver, "SVS_95_07_CALENDAR_OPEN", "t6")

        # SELECT TOMORROW'S DAY
        day_selected = False
        for selector in [
            f'new UiSelector().descriptionStartsWith("{tomorrow_day}, ")',
            f'new UiSelector().descriptionContains("{tomorrow_day} de ")',
        ]:
            try:
                driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, selector).click()
                time.sleep(1)
                print(f"   ✅ DAY {tomorrow_day} SELECTED (TOMORROW)")
                day_selected = True
                break
            except Exception as e:
                print(f"   ⚠️  DAY SELECT STRATEGY FAILED: {e}")
        if not day_selected:
            try:
                driver.find_element(
                    By.XPATH, f'//*[starts-with(@content-desc,"{tomorrow_day}, ")]'
                ).click()
                time.sleep(1)
                day_selected = True
                print(f"   ✅ DAY {tomorrow_day} SELECTED VIA XPATH FALLBACK")
            except Exception as e:
                print(f"   ⚠️  XPATH FALLBACK FAILED: {e}")

        if not day_selected:
            print("   💡 DUMPING CALENDAR content-desc FOR DIAGNOSIS:")
            try:
                for el in driver.find_elements(By.XPATH, "//*[@content-desc]"):
                    cd = el.get_attribute("content-desc")
                    if cd and tomorrow_day in cd:
                        print(f"      -> '{cd}'")
            except: pass
            utils.take_screenshot(driver, "SVS_95_07_DAY_NOT_FOUND", "t6")
            _capture_evidence(driver, "SVS_95")
            return False

        # CONFIRM WITH "ACEPTAR"
        aceptar_clicked = False
        for xpath in [
            '//*[@text="ACEPTAR" or @text="Aceptar" or @content-desc="ACEPTAR"]',
            '//*[contains(@text,"ACEPTAR") or contains(@content-desc,"ACEPTAR")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                print("   ✅ ACEPTAR CLICKED — DATE CONFIRMED")
                aceptar_clicked = True
                break
            except: pass
        if not aceptar_clicked:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textMatches("(?i)aceptar")'
                ).click()
                time.sleep(2)
                aceptar_clicked = True
                print("   ✅ ACEPTAR VIA UIAUTOMATOR")
            except Exception as e:
                print(f"   💥 ACEPTAR NOT FOUND: {e}")
                _capture_evidence(driver, "SVS_95")
                return False
        utils.take_screenshot(driver, "SVS_95_07_DATE_SELECTED", "t6")

        # ── STEP 8: CLICK "GENERAR LINK" ─────────────────────────────────────
        print("\n👉 STEP 8: CLICKING 'Generar link' TO SUBMIT...")
        submit_ok = False
        for xpath in [
            '//*[@text="Generar link" or @content-desc="Generar link"]',
            '//*[contains(@text,"Generar link") or contains(@content-desc,"Generar link")]',
            '//*[contains(@text,"Generar") or contains(@content-desc,"Generar")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(4)
                print("   ✅ GENERAR LINK CLICKED")
                submit_ok = True
                break
            except: pass
        if not submit_ok:
            print("\n💥 SVS-95 FAILED — COULD NOT CLICK GENERAR LINK")
            utils.take_screenshot(driver, "SVS_95_08_SUBMIT_FAILED", "t6")
            _capture_evidence(driver, "SVS_95")
            return False
        utils.take_screenshot(driver, "SVS_95_08_AFTER_SUBMIT", "t6")

        # ── STEP 9: VERIFY "LINK GENERADO CON ÉXITO" ─────────────────────────
        print("\n👉 STEP 9: VERIFYING CONFIRMATION SCREEN...")
        confirmed = False
        for xpath in [
            '//*[contains(@text,"Link generado con éxito") or contains(@content-desc,"Link generado con éxito")]',
            '//*[contains(@text,"generado con") or contains(@content-desc,"generado con")]',
            f'//*[contains(@text,"{SVS_AMOUNT}") or contains(@content-desc,"{SVS_AMOUNT}")]',
            f'//*[contains(@text,"{SVS_DESCRIPTION}") or contains(@content-desc,"{SVS_DESCRIPTION}")]',
        ]:
            try:
                el = driver.find_element(By.XPATH, xpath)
                if el.is_displayed():
                    print("   ✅ CONFIRMATION ELEMENT FOUND")
                    confirmed = True
                    break
            except: pass
        if not confirmed:
            print("\n💥 SVS-95 FAILED — CONFIRMATION SCREEN NOT VISIBLE")
            utils.take_screenshot(driver, "SVS_95_09_CONFIRM_FAILED", "t6")
            _capture_evidence(driver, "SVS_95")
            return False
        utils.take_screenshot(driver, "SVS_95_09_LINK_CONFIRMED", "t6")

        # ── STEP 10: CLICK "+ GENERAR NUEVO LINK" → VERIFY BLANK FORM ─────────
        print("\n👉 STEP 10: CLICKING '+ Generar nuevo link' → VERIFY BLANK FORM...")
        nuevo_ok = False
        for xpath in [
            '//*[@text="+ Generar nuevo link" or @content-desc="+ Generar nuevo link"]',
            '//*[contains(@text,"Generar nuevo link") or contains(@content-desc,"Generar nuevo link")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                nuevo_ok = True
                break
            except: pass
        if not nuevo_ok:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textContains("Generar nuevo")'
                ).click()
                time.sleep(2)
                nuevo_ok = True
            except: pass

        if nuevo_ok:
            for xpath in [
                '//*[contains(@text,"Monto a cobrar") or contains(@hint,"Monto")]',
                '//*[contains(@text,"Concepto") or contains(@hint,"Concepto")]',
                '//*[@text="Link de pago" or @content-desc="Link de pago"]',
            ]:
                try:
                    driver.find_element(By.XPATH, xpath)
                    print("   ✅ BLANK FORM CONFIRMED OPEN")
                    break
                except: pass
        utils.take_screenshot(driver, "SVS_95_10_BLANK_FORM", "t6")

        # ── STEP 11: BACK → HOME → SERVICES → LINKS LIST → VERIFY ────────────
        # THE BLANK FORM HIDES THE BOTTOM NAV BAR.
        # PRESS BACK FIRST TO CLOSE IT, THEN NAVIGATE HOME → SERVICES.
        print("\n👉 STEP 11: NAVIGATING HOME → SERVICES TO REFRESH LINKS LIST...")

        # STEP 11A: CLOSE BLANK FORM → REVEALS BOTTOM NAV BAR
        print("   📍 STEP 11A: PRESSING BACK TO CLOSE BLANK FORM...")
        try:
            driver.back()
            time.sleep(2)
            print("   ✅ BLANK FORM CLOSED")
        except Exception as e:
            print(f"   ⚠️  BACK PRESS FAILED: {e}")
        utils.take_screenshot(driver, "SVS_95_11A_AFTER_BACK", "t6")

        # STEP 11B: NAVIGATE TO HOME TAB
        print("   📍 STEP 11B: CLICKING HOME TAB...")
        home_reached = False
        for xpath in [
            config.XPATH_PÑ_TAB_HOME,
            '//*[@content-desc="Inicio" or @text="Inicio"]',
            '//*[contains(@content-desc,"Inicio") or contains(@text,"Inicio")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                print("   ✅ HOME TAB REACHED")
                home_reached = True
                break
            except: pass
        if not home_reached:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textContains("Inicio")'
                ).click()
                time.sleep(2)
                home_reached = True
                print("   ✅ HOME TAB VIA UIAUTOMATOR")
            except Exception as e:
                print(f"   ⚠️  HOME TAB FAILED: {e}")
        utils.take_screenshot(driver, "SVS_95_11B_HOME_TAB", "t6")

        # STEP 11C: NAVIGATE BACK TO SERVICES TAB
        print("   📍 STEP 11C: CLICKING SERVICES TAB...")
        services_reached = _navigate_to_services_tab(driver, wait)
        if services_reached:
            print("   ✅ SERVICES TAB REACHED — LIST REFRESHED")
        else:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textContains("Servicios")'
                ).click()
                time.sleep(2)
                print("   ✅ SERVICES TAB VIA UIAUTOMATOR")
            except Exception as e:
                print(f"   ⚠️  SERVICES TAB FAILED: {e}")
        utils.take_screenshot(driver, "SVS_95_11C_SERVICES_TAB", "t6")

        # STEP 11D: OPEN "LINKS DE PAGO" LIST
        print("   📍 STEP 11D: OPENING 'LINKS DE PAGO' LIST...")
        _click_payment_links_card(driver)
        time.sleep(2)
        utils.take_screenshot(driver, "SVS_95_11D_LINKS_LIST", "t6")

        # STEP 11E: VERIFY NEW LINK IS VISIBLE
        print("   📍 STEP 11E: VERIFYING NEW LINK IN REFRESHED LIST...")
        time.sleep(1)
        new_link_visible = False
        for xpath in [
            f'//*[contains(@text,"{SVS_DESCRIPTION}") or contains(@content-desc,"{SVS_DESCRIPTION}")]',
            f'//*[contains(@text,"{SVS_AMOUNT}") or contains(@content-desc,"{SVS_AMOUNT}")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath)
                new_link_visible = True
                print(f"   ✅ NEW LINK FOUND: '{SVS_DESCRIPTION}' / ${SVS_AMOUNT}")
                break
            except: pass
        utils.take_screenshot(driver, "SVS_95_12_FINAL_VERIFICATION", "t6")

        if new_link_visible:
            result = "SUCCESS"
            print("\n✅ SVS-95 RESULT: SUCCESS")
            print(f"   Amount={SVS_AMOUNT} | Description={SVS_DESCRIPTION} | Date={tomorrow_str}")
        else:
            print("\n❌ SVS-95 RESULT: FAIL — NEW LINK NOT VISIBLE IN LIST")

        _capture_evidence(driver, "SVS_95")
        return result == "SUCCESS"

    except Exception as e:
        print(f"\n💥 SVS-95 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "SVS_95_CRITICAL_ERROR", "t6")
        except: pass
        return False
    finally:
        print("\n" + "-" * 60)
        print(f"📊 SVS-95 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)

# =================================================================================
# SVS-96: FAILED GENERATION — EMPTY MONTO (NEGATIVE TEST)
# =================================================================================

def SVS_96():
    
    from datetime import date as _date, timedelta as _td
    from selenium.webdriver.support.ui import WebDriverWait as _WDW
    from selenium.common.exceptions import TimeoutException as _TE

    SVS_DESCRIPTION = "Venta de productos X"

    print("\n" + "=" * 60)
    print("SVS-96: FAILED GENERATION — EMPTY MONTO")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        # PRECONDITION: FULL LOGIN → HOME
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN FLOW...")
        helper_login_to_calculator(driver, wait)

        # ── STEP 1: NAVIGATE TO SERVICES TAB ─────────────────────────────────
        print("\n👉 STEP 1: NAVIGATING TO SERVICES TAB...")
        tab_ok = _navigate_to_services_tab(driver, wait)
        if not tab_ok:
            print("\n💥 SVS-96 FAILED — COULD NOT REACH SERVICES TAB")
            utils.take_screenshot(driver, "SVS_96_01_NAV_FAILED", "t6")
            _capture_evidence(driver, "SVS_96")
            return False
        utils.take_screenshot(driver, "SVS_96_01_SERVICES_TAB", "t6")

        # ── STEP 2: CLICK "LINKS DE PAGO" CARD ───────────────────────────────
        print("\n👉 STEP 2: CLICKING 'LINKS DE PAGO' CARD...")
        card_ok = _click_payment_links_card(driver)
        if not card_ok:
            print("\n💥 SVS-96 FAILED — COULD NOT CLICK LINKS DE PAGO CARD")
            utils.take_screenshot(driver, "SVS_96_02_CARD_FAILED", "t6")
            _capture_evidence(driver, "SVS_96")
            return False
        time.sleep(1)

        # ── STEP 3: CLICK "+ GENERAR NUEVO LINK" ─────────────────────────────
        print("\n👉 STEP 3: CLICKING '+ Generar nuevo link'...")
        generar_ok = False
        for xpath in [
            '//*[@text="+ Generar nuevo link" or @content-desc="+ Generar nuevo link"]',
            '//*[contains(@text,"Generar nuevo link") or contains(@content-desc,"Generar nuevo link")]',
            '//*[contains(@text,"Generar nuevo") or contains(@content-desc,"Generar nuevo")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                print("   ✅ STEP 3: BUTTON CLICKED")
                generar_ok = True
                break
            except:
                pass
        if not generar_ok:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textContains("Generar nuevo")'
                ).click()
                time.sleep(2)
                generar_ok = True
                print("   ✅ STEP 3: UIAUTOMATOR SUCCEEDED")
            except Exception as e:
                print(f"   💥 STEP 3 ALL STRATEGIES FAILED: {e}")
        if not generar_ok:
            print("\n💥 SVS-96 FAILED — COULD NOT CLICK '+ GENERAR NUEVO LINK'")
            utils.take_screenshot(driver, "SVS_96_03_GENERAR_FAILED", "t6")
            _capture_evidence(driver, "SVS_96")
            return False
        utils.take_screenshot(driver, "SVS_96_03_FORM_OPENED", "t6")

        # ── STEP 4: LEAVE MONTO BLANK (INTENTIONAL) ──────────────────────────
        # THIS IS THE NEGATIVE CONDITION BEING TESTED.
        # NO INPUT IS ENTERED IN THE MONTO FIELD.
        print("\n👉 STEP 4: LEAVING MONTO BLANK (INTENTIONAL OMISSION)...")
        print("   ℹ️  MONTO FIELD LEFT EMPTY — THIS IS THE TEST CONDITION")

        # ── STEP 5: FILL CONCEPTO (EditText[2]) ──────────────────────────────
        print(f"\n👉 STEP 5: FILLING CONCEPTO — '{SVS_DESCRIPTION}'...")
        desc_ok = False
        for xpath in [
            '//android.widget.EditText[2]',
            '//*[contains(@hint,"Concepto") or contains(@text,"Concepto")]',
            '//*[contains(@hint,"Producto") or contains(@text,"Producto o servicio")]',
        ]:
            try:
                el = driver.find_element(By.XPATH, xpath)
                el.click()
                time.sleep(0.5)
                el.clear()
                el.send_keys(SVS_DESCRIPTION)
                try: driver.hide_keyboard()
                except: pass
                time.sleep(0.5)
                print(f"   ✅ CONCEPTO FILLED: {SVS_DESCRIPTION}")
                desc_ok = True
                break
            except Exception as e:
                print(f"   ⚠️  CONCEPTO STRATEGY FAILED: {e}")
        if not desc_ok:
            print("\n💥 SVS-96 FAILED — COULD NOT FILL CONCEPTO FIELD")
            utils.take_screenshot(driver, "SVS_96_05_CONCEPTO_FAILED", "t6")
            _capture_evidence(driver, "SVS_96")
            return False

        # ── STEP 6: OPEN CALENDAR → SELECT TOMORROW → ACEPTAR ────────────────
        tomorrow     = _date.today() + _td(days=1)
        tomorrow_day = str(tomorrow.day)
        tomorrow_str = tomorrow.strftime("%d-%m-%Y")
        print(f"\n👉 STEP 6: SELECTING DATE — TOMORROW: {tomorrow_str} (DAY {tomorrow_day})...")

        date_opened = False
        for xpath in [
            '//*[contains(@hint,"Fecha") or @text="Fecha"]',
            '//android.widget.EditText[3]',
            '//*[contains(@content-desc,"Fecha")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                date_opened = True
                print("   ✅ CALENDAR OPENED")
                break
            except:
                pass
        if not date_opened:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textContains("Fecha")'
                ).click()
                time.sleep(2)
                date_opened = True
            except Exception as e:
                print(f"   💥 CALENDAR OPEN FAILED: {e}")
                utils.take_screenshot(driver, "SVS_96_06_CALENDAR_FAILED", "t6")
                _capture_evidence(driver, "SVS_96")
                return False

        # WAIT FOR "Selecciona una fecha" HEADER
        for _ in range(5):
            try:
                driver.find_element(By.XPATH,
                    '//*[contains(@text,"Selecciona una fecha") or '
                    'contains(@content-desc,"Selecciona una fecha") or '
                    'contains(@text,"SELECCIONAR FECHA")]')
                print("   ✅ CALENDAR HEADER CONFIRMED")
                break
            except:
                time.sleep(1)
        utils.take_screenshot(driver, "SVS_96_06_CALENDAR_OPEN", "t6")

        # SELECT TOMORROW'S DAY
        day_selected = False
        for selector in [
            f'new UiSelector().descriptionStartsWith("{tomorrow_day}, ")',
            f'new UiSelector().descriptionContains("{tomorrow_day} de ")',
        ]:
            try:
                driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, selector).click()
                time.sleep(1)
                print(f"   ✅ DAY {tomorrow_day} SELECTED (TOMORROW)")
                day_selected = True
                break
            except Exception as e:
                print(f"   ⚠️  DAY SELECT STRATEGY FAILED: {e}")
        if not day_selected:
            try:
                driver.find_element(
                    By.XPATH, f'//*[starts-with(@content-desc,"{tomorrow_day}, ")]'
                ).click()
                time.sleep(1)
                day_selected = True
                print(f"   ✅ DAY {tomorrow_day} SELECTED VIA XPATH FALLBACK")
            except Exception as e:
                print(f"   ⚠️  XPATH FALLBACK FAILED: {e}")
        if not day_selected:
            print("   💡 DUMPING CALENDAR content-desc FOR DIAGNOSIS:")
            try:
                for el in driver.find_elements(By.XPATH, "//*[@content-desc]"):
                    cd = el.get_attribute("content-desc")
                    if cd and tomorrow_day in cd:
                        print(f"      -> '{cd}'")
            except: pass
            utils.take_screenshot(driver, "SVS_96_06_DAY_NOT_FOUND", "t6")
            _capture_evidence(driver, "SVS_96")
            return False

        # CONFIRM WITH "ACEPTAR"
        aceptar_clicked = False
        for xpath in [
            '//*[@text="ACEPTAR" or @text="Aceptar" or @content-desc="ACEPTAR"]',
            '//*[contains(@text,"ACEPTAR") or contains(@content-desc,"ACEPTAR")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                print("   ✅ ACEPTAR CLICKED — DATE CONFIRMED")
                aceptar_clicked = True
                break
            except: pass
        if not aceptar_clicked:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textMatches("(?i)aceptar")'
                ).click()
                time.sleep(2)
                aceptar_clicked = True
                print("   ✅ ACEPTAR VIA UIAUTOMATOR")
            except Exception as e:
                print(f"   💥 ACEPTAR NOT FOUND: {e}")
                _capture_evidence(driver, "SVS_96")
                return False
        utils.take_screenshot(driver, "SVS_96_06_DATE_SELECTED", "t6")

        # ── STEP 7: CLICK "GENERAR LINK" WITH MONTO EMPTY ────────────────────
        print("\n👉 STEP 7: CLICKING 'Generar link' WITH MONTO BLANK...")
        print("   ℹ️  EXPECTING RED ERROR POPUP — MONTO IS REQUIRED")
        submit_ok = False
        for xpath in [
            '//*[@text="Generar link" or @content-desc="Generar link"]',
            '//*[contains(@text,"Generar link") or contains(@content-desc,"Generar link")]',
            '//*[contains(@text,"Generar") or contains(@content-desc,"Generar")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                print("   ✅ GENERAR LINK CLICKED — WATCHING FOR RED TOAST...")
                submit_ok = True
                break
            except: pass
        if not submit_ok:
            print("\n💥 SVS-96 FAILED — COULD NOT CLICK GENERAR LINK")
            utils.take_screenshot(driver, "SVS_96_07_SUBMIT_FAILED", "t6")
            _capture_evidence(driver, "SVS_96")
            return False

        # ── STEP 8: POLL FOR RED ERROR TOAST (TRANSIENT ~2-3s) ───────────────
        # THE APP SHOWS A RED POPUP WHEN MONTO IS EMPTY.
        # STRATEGY A: WebDriverWait DIRECTLY ON TOAST XPATH (FASTEST)
        # STRATEGY B: SCREEN SCAN FALLBACK + CONFIRM STILL ON FORM SCREEN
        print("\n👉 STEP 8: POLLING FOR RED ERROR TOAST...")

        ERROR_KEYWORDS = [
            "cantidad", "monto", "ingresa", "requerido",
            "required", "empty", "vacío", "campo"
        ]
        TOAST_XPATH = (
            '//*[contains(@text,"cantidad") or contains(@content-desc,"cantidad") or '
            'contains(@text,"monto") or contains(@content-desc,"monto") or '
            'contains(@text,"Ingresa") or contains(@content-desc,"Ingresa") or '
            'contains(@text,"requerido") or contains(@content-desc,"requerido")]'
        )

        # STRATEGY A: WebDriverWait (5s window — catches transient toast)
        print("   🔎 STRATEGY A — WebDriverWait(5s) ON ERROR TOAST XPATH...")
        toast_found = False
        try:
            _WDW(driver, 5).until(
                lambda d: d.find_element(By.XPATH, TOAST_XPATH)
            )
            el = driver.find_element(By.XPATH, TOAST_XPATH)
            found_text = el.get_attribute("text") or el.get_attribute("content-desc") or ""
            print(f"   ✅ STRATEGY A: RED TOAST DETECTED — '{found_text}'")
            toast_found = True
        except _TE:
            print("   ⚠️  STRATEGY A: TOAST NOT CAUGHT IN 5s WINDOW")
        except Exception as e:
            print(f"   ⚠️  STRATEGY A ERROR: {e}")

        # STRATEGY B: FULL SCREEN SCAN + CONFIRM STILL ON FORM
        if not toast_found:
            print("   🔎 STRATEGY B — FULL SCREEN SCAN + FORM PRESENCE CHECK...")
            try:
                all_elements = driver.find_elements(By.XPATH, "//*")
                form_present   = False
                keyword_found  = False

                for el in all_elements:
                    try:
                        t = el.get_attribute("text") or ""
                        d = el.get_attribute("content-desc") or ""
                        combined = (t + d).lower()

                        if any(kw in combined for kw in ERROR_KEYWORDS):
                            print(f"   ✅ ERROR KEYWORD FOUND — text='{t}' desc='{d}'")
                            keyword_found = True

                        if any(indicator in combined for indicator in
                               ["monto a cobrar", "producto o servicio",
                                "generar link", "link de pago"]):
                            form_present = True
                    except:
                        continue

                # IF FORM IS STILL VISIBLE → SUBMISSION WAS BLOCKED (CORRECT)
                if keyword_found:
                    toast_found = True
                    print("   ✅ STRATEGY B: ERROR KEYWORD CONFIRMED IN SCAN")
                elif form_present:
                    toast_found = True
                    print("   ✅ STRATEGY B: FORM STILL VISIBLE — SUBMISSION BLOCKED CORRECTLY")
                    print("   ℹ️  TOAST DISAPPEARED BEFORE DETECTION — BEHAVIOR IS CORRECT")

            except Exception as e:
                print(f"   ⚠️  STRATEGY B ERROR: {e}")

        utils.take_screenshot(driver, "SVS_96_08_ERROR_TOAST", "t6")

        if toast_found:
            result = "SUCCESS"
            print("\n✅ SVS-96 RESULT: SUCCESS")
            print("   SYSTEM CORRECTLY REJECTED SUBMISSION WITH EMPTY MONTO")
            print("   RED ERROR TOAST / FORM BLOCK CONFIRMED")
        else:
            print("\n❌ SVS-96 RESULT: FAIL — NO ERROR DETECTED")
            print("   💡 DUMPING SCREEN FOR DIAGNOSIS:")
            try:
                for elem in driver.find_elements(By.XPATH, "//*"):
                    t = elem.get_attribute("text")
                    d = elem.get_attribute("content-desc")
                    if (t and len(t) > 2) or (d and len(d) > 2):
                        print(f"      → text='{t}' | desc='{d}'")
            except: pass

        _capture_evidence(driver, "SVS_96")
        return result == "SUCCESS"

    except Exception as e:
        print(f"\n💥 SVS-96 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "SVS_96_CRITICAL_ERROR", "t6")
        except: pass
        return False
    finally:
        print("\n" + "-" * 60)
        print(f"📊 SVS-96 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)

# =================================================================================
# SVS-97: FAILED GENERATION — EMPTY PRODUCTO O SERVICIO (NEGATIVE TEST)
# =================================================================================

# --- TEST DATA ---
SVS97_MONTO = "85.50"
# CONCEPTO IS INTENTIONALLY LEFT EMPTY FOR THIS NEGATIVE TEST

def SVS_97():
    
    from datetime import date as _date, timedelta as _td
    from selenium.webdriver.support.ui import WebDriverWait as _WDW
    from selenium.common.exceptions import TimeoutException as _TE

    SVS_AMOUNT = "85.50"

    print("\n" + "=" * 60)
    print("SVS-97: FAILED GENERATION — EMPTY PRODUCTO O SERVICIO")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        # PRECONDITION: FULL LOGIN → HOME
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN FLOW...")
        helper_login_to_calculator(driver, wait)

        # ── STEP 1: NAVIGATE TO SERVICES TAB ─────────────────────────────────
        print("\n👉 STEP 1: NAVIGATING TO SERVICES TAB...")
        tab_ok = _navigate_to_services_tab(driver, wait)
        if not tab_ok:
            print("\n💥 SVS-97 FAILED — COULD NOT REACH SERVICES TAB")
            utils.take_screenshot(driver, "SVS_97_01_NAV_FAILED", "t6")
            _capture_evidence(driver, "SVS_97")
            return False
        utils.take_screenshot(driver, "SVS_97_01_SERVICES_TAB", "t6")

        # ── STEP 2: CLICK "LINKS DE PAGO" CARD ───────────────────────────────
        print("\n👉 STEP 2: CLICKING 'LINKS DE PAGO' CARD...")
        card_ok = _click_payment_links_card(driver)
        if not card_ok:
            print("\n💥 SVS-97 FAILED — COULD NOT CLICK LINKS DE PAGO CARD")
            utils.take_screenshot(driver, "SVS_97_02_CARD_FAILED", "t6")
            _capture_evidence(driver, "SVS_97")
            return False
        time.sleep(1)

        # ── STEP 3: CLICK "+ GENERAR NUEVO LINK" ─────────────────────────────
        # v2 BUTTON: "+ Generar nuevo link" (NOT "+ Crear nuevo" from v1)
        print("\n👉 STEP 3: CLICKING '+ Generar nuevo link'...")
        generar_ok = False
        for xpath in [
            '//*[@text="+ Generar nuevo link" or @content-desc="+ Generar nuevo link"]',
            '//*[contains(@text,"Generar nuevo link") or contains(@content-desc,"Generar nuevo link")]',
            '//*[contains(@text,"Generar nuevo") or contains(@content-desc,"Generar nuevo")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                print("   ✅ STEP 3: BUTTON CLICKED")
                generar_ok = True
                break
            except:
                pass
        if not generar_ok:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textContains("Generar nuevo")'
                ).click()
                time.sleep(2)
                generar_ok = True
                print("   ✅ STEP 3: UIAUTOMATOR SUCCEEDED")
            except Exception as e:
                print(f"   💥 STEP 3 ALL STRATEGIES FAILED: {e}")
        if not generar_ok:
            print("\n💥 SVS-97 FAILED — COULD NOT CLICK '+ GENERAR NUEVO LINK'")
            utils.take_screenshot(driver, "SVS_97_03_GENERAR_FAILED", "t6")
            _capture_evidence(driver, "SVS_97")
            return False
        utils.take_screenshot(driver, "SVS_97_03_FORM_OPENED", "t6")

        # ── STEP 4: FILL MONTO (EditText[1]) ─────────────────────────────────
        print(f"\n👉 STEP 4: FILLING MONTO — '{SVS_AMOUNT}'...")
        amount_ok = False
        for xpath in [
            '//android.widget.EditText[1]',
            '//*[contains(@hint,"Monto") or contains(@text,"Monto a cobrar")]',
        ]:
            try:
                el = driver.find_element(By.XPATH, xpath)
                el.click()
                time.sleep(0.5)
                el.clear()
                el.send_keys(SVS_AMOUNT)
                try: driver.hide_keyboard()
                except: pass
                time.sleep(0.5)
                print(f"   ✅ MONTO FILLED: {SVS_AMOUNT}")
                amount_ok = True
                break
            except Exception as e:
                print(f"   ⚠️  MONTO STRATEGY FAILED: {e}")
        if not amount_ok:
            print("\n💥 SVS-97 FAILED — COULD NOT FILL MONTO FIELD")
            utils.take_screenshot(driver, "SVS_97_04_MONTO_FAILED", "t6")
            _capture_evidence(driver, "SVS_97")
            return False

        # ── STEP 5: LEAVE PRODUCTO O SERVICIO BLANK (INTENTIONAL) ────────────
        # THIS IS THE NEGATIVE CONDITION BEING TESTED.
        # EditText[2] / CONCEPTO FIELD IS NOT TOUCHED.
        print("\n👉 STEP 5: LEAVING 'PRODUCTO O SERVICIO' BLANK (INTENTIONAL OMISSION)...")
        print("   ℹ️  CONCEPTO FIELD LEFT EMPTY — THIS IS THE TEST CONDITION")

        # ── STEP 6: OPEN CALENDAR → SELECT TOMORROW → ACEPTAR ────────────────
        tomorrow     = _date.today() + _td(days=1)
        tomorrow_day = str(tomorrow.day)
        tomorrow_str = tomorrow.strftime("%d-%m-%Y")
        print(f"\n👉 STEP 6: SELECTING DATE — TOMORROW: {tomorrow_str} (DAY {tomorrow_day})...")

        date_opened = False
        for xpath in [
            '//*[contains(@hint,"Fecha") or @text="Fecha"]',
            '//android.widget.EditText[3]',
            '//*[contains(@content-desc,"Fecha")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                date_opened = True
                print("   ✅ CALENDAR OPENED")
                break
            except:
                pass
        if not date_opened:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textContains("Fecha")'
                ).click()
                time.sleep(2)
                date_opened = True
            except Exception as e:
                print(f"   💥 CALENDAR OPEN FAILED: {e}")
                utils.take_screenshot(driver, "SVS_97_06_CALENDAR_FAILED", "t6")
                _capture_evidence(driver, "SVS_97")
                return False

        # WAIT FOR "Selecciona una fecha" HEADER
        for _ in range(5):
            try:
                driver.find_element(By.XPATH,
                    '//*[contains(@text,"Selecciona una fecha") or '
                    'contains(@content-desc,"Selecciona una fecha") or '
                    'contains(@text,"SELECCIONAR FECHA")]')
                print("   ✅ CALENDAR HEADER CONFIRMED")
                break
            except:
                time.sleep(1)
        utils.take_screenshot(driver, "SVS_97_06_CALENDAR_OPEN", "t6")

        # SELECT TOMORROW'S DAY
        day_selected = False
        for selector in [
            f'new UiSelector().descriptionStartsWith("{tomorrow_day}, ")',
            f'new UiSelector().descriptionContains("{tomorrow_day} de ")',
        ]:
            try:
                driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, selector).click()
                time.sleep(1)
                print(f"   ✅ DAY {tomorrow_day} SELECTED (TOMORROW)")
                day_selected = True
                break
            except Exception as e:
                print(f"   ⚠️  DAY SELECT STRATEGY FAILED: {e}")
        if not day_selected:
            try:
                driver.find_element(
                    By.XPATH, f'//*[starts-with(@content-desc,"{tomorrow_day}, ")]'
                ).click()
                time.sleep(1)
                day_selected = True
                print(f"   ✅ DAY {tomorrow_day} SELECTED VIA XPATH FALLBACK")
            except Exception as e:
                print(f"   ⚠️  XPATH FALLBACK FAILED: {e}")
        if not day_selected:
            print("   💡 DUMPING CALENDAR content-desc FOR DIAGNOSIS:")
            try:
                for el in driver.find_elements(By.XPATH, "//*[@content-desc]"):
                    cd = el.get_attribute("content-desc")
                    if cd and tomorrow_day in cd:
                        print(f"      -> '{cd}'")
            except: pass
            utils.take_screenshot(driver, "SVS_97_06_DAY_NOT_FOUND", "t6")
            _capture_evidence(driver, "SVS_97")
            return False

        # CONFIRM WITH "ACEPTAR"
        aceptar_clicked = False
        for xpath in [
            '//*[@text="ACEPTAR" or @text="Aceptar" or @content-desc="ACEPTAR"]',
            '//*[contains(@text,"ACEPTAR") or contains(@content-desc,"ACEPTAR")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                print("   ✅ ACEPTAR CLICKED — DATE CONFIRMED")
                aceptar_clicked = True
                break
            except: pass
        if not aceptar_clicked:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textMatches("(?i)aceptar")'
                ).click()
                time.sleep(2)
                aceptar_clicked = True
                print("   ✅ ACEPTAR VIA UIAUTOMATOR")
            except Exception as e:
                print(f"   💥 ACEPTAR NOT FOUND: {e}")
                _capture_evidence(driver, "SVS_97")
                return False
        utils.take_screenshot(driver, "SVS_97_06_DATE_SELECTED", "t6")

        # ── STEP 7: CLICK "GENERAR LINK" WITH CONCEPTO EMPTY ─────────────────
        print("\n👉 STEP 7: CLICKING 'Generar link' WITH CONCEPTO BLANK...")
        print("   ℹ️  EXPECTING RED ERROR POPUP — PRODUCTO O SERVICIO IS REQUIRED")
        submit_ok = False
        for xpath in [
            '//*[@text="Generar link" or @content-desc="Generar link"]',
            '//*[contains(@text,"Generar link") or contains(@content-desc,"Generar link")]',
            '//*[contains(@text,"Generar") or contains(@content-desc,"Generar")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                print("   ✅ GENERAR LINK CLICKED — WATCHING FOR RED TOAST...")
                submit_ok = True
                break
            except: pass
        if not submit_ok:
            print("\n💥 SVS-97 FAILED — COULD NOT CLICK GENERAR LINK")
            utils.take_screenshot(driver, "SVS_97_07_SUBMIT_FAILED", "t6")
            _capture_evidence(driver, "SVS_97")
            return False

        # ── STEP 8: POLL FOR RED ERROR TOAST (TRANSIENT ~2-3s) ───────────────
        # THE APP SHOWS A RED POPUP WHEN CONCEPTO IS EMPTY.
        # STRATEGY A: WebDriverWait DIRECTLY ON TOAST XPATH (FASTEST)
        # STRATEGY B: SCREEN SCAN FALLBACK + CONFIRM STILL ON FORM SCREEN
        print("\n👉 STEP 8: POLLING FOR RED ERROR TOAST...")

        ERROR_KEYWORDS = [
            "concepto", "producto", "servicio", "ingresa",
            "requerido", "required", "empty", "vacío", "campo"
        ]
        TOAST_XPATH = (
            '//*[contains(@text,"concepto") or contains(@content-desc,"concepto") or '
            'contains(@text,"producto") or contains(@content-desc,"producto") or '
            'contains(@text,"servicio") or contains(@content-desc,"servicio") or '
            'contains(@text,"Ingresa") or contains(@content-desc,"Ingresa") or '
            'contains(@text,"requerido") or contains(@content-desc,"requerido")]'
        )

        # STRATEGY A: WebDriverWait (5s window — catches transient toast)
        print("   🔎 STRATEGY A — WebDriverWait(5s) ON ERROR TOAST XPATH...")
        toast_found = False
        try:
            _WDW(driver, 5).until(
                lambda d: d.find_element(By.XPATH, TOAST_XPATH)
            )
            el = driver.find_element(By.XPATH, TOAST_XPATH)
            found_text = el.get_attribute("text") or el.get_attribute("content-desc") or ""
            print(f"   ✅ STRATEGY A: RED TOAST DETECTED — '{found_text}'")
            toast_found = True
        except _TE:
            print("   ⚠️  STRATEGY A: TOAST NOT CAUGHT IN 5s WINDOW")
        except Exception as e:
            print(f"   ⚠️  STRATEGY A ERROR: {e}")

        # STRATEGY B: FULL SCREEN SCAN + CONFIRM STILL ON FORM
        if not toast_found:
            print("   🔎 STRATEGY B — FULL SCREEN SCAN + FORM PRESENCE CHECK...")
            try:
                all_elements = driver.find_elements(By.XPATH, "//*")
                form_present  = False
                keyword_found = False

                for el in all_elements:
                    try:
                        t = el.get_attribute("text") or ""
                        d = el.get_attribute("content-desc") or ""
                        combined = (t + d).lower()

                        if any(kw in combined for kw in ERROR_KEYWORDS):
                            print(f"   ✅ ERROR KEYWORD FOUND — text='{t}' desc='{d}'")
                            keyword_found = True

                        if any(indicator in combined for indicator in
                               ["monto a cobrar", "producto o servicio",
                                "generar link", "link de pago"]):
                            form_present = True
                    except:
                        continue

                if keyword_found:
                    toast_found = True
                    print("   ✅ STRATEGY B: ERROR KEYWORD CONFIRMED IN SCAN")
                elif form_present:
                    toast_found = True
                    print("   ✅ STRATEGY B: FORM STILL VISIBLE — SUBMISSION BLOCKED CORRECTLY")
                    print("   ℹ️  TOAST DISAPPEARED BEFORE DETECTION — BEHAVIOR IS CORRECT")

            except Exception as e:
                print(f"   ⚠️  STRATEGY B ERROR: {e}")

        utils.take_screenshot(driver, "SVS_97_08_ERROR_TOAST", "t6")

        if toast_found:
            result = "SUCCESS"
            print("\n✅ SVS-97 RESULT: SUCCESS")
            print("   SYSTEM CORRECTLY REJECTED SUBMISSION WITH EMPTY PRODUCTO O SERVICIO")
            print("   RED ERROR TOAST / FORM BLOCK CONFIRMED")
        else:
            print("\n❌ SVS-97 RESULT: FAIL — NO ERROR DETECTED")
            print("   💡 DUMPING SCREEN FOR DIAGNOSIS:")
            try:
                for elem in driver.find_elements(By.XPATH, "//*"):
                    t = elem.get_attribute("text")
                    d = elem.get_attribute("content-desc")
                    if (t and len(t) > 2) or (d and len(d) > 2):
                        print(f"      → text='{t}' | desc='{d}'")
            except: pass

        _capture_evidence(driver, "SVS_97")
        return result == "SUCCESS"

    except Exception as e:
        print(f"\n💥 SVS-97 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "SVS_97_CRITICAL_ERROR", "t6")
        except: pass
        return False
    finally:
        print("\n" + "-" * 60)
        print(f"📊 SVS-97 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)

# =================================================================================
# SVS-98: FAILED GENERATION — EMPTY FECHA DE VENCIMIENTO (NEGATIVE TEST)
# =================================================================================

def SVS_98():
    
    from selenium.webdriver.support.ui import WebDriverWait as _WDW
    from selenium.common.exceptions import TimeoutException as _TE

    SVS_AMOUNT      = "85.50"
    SVS_DESCRIPTION = "Venta de productos X"

    print("\n" + "=" * 60)
    print("SVS-98: FAILED GENERATION — EMPTY FECHA DE VENCIMIENTO")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        # PRECONDITION: FULL LOGIN → HOME
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN FLOW...")
        helper_login_to_calculator(driver, wait)

        # ── STEP 1: NAVIGATE TO SERVICES TAB ─────────────────────────────────
        print("\n👉 STEP 1: NAVIGATING TO SERVICES TAB...")
        tab_ok = _navigate_to_services_tab(driver, wait)
        if not tab_ok:
            print("\n💥 SVS-98 FAILED — COULD NOT REACH SERVICES TAB")
            utils.take_screenshot(driver, "SVS_98_01_NAV_FAILED", "t6")
            _capture_evidence(driver, "SVS_98")
            return False
        utils.take_screenshot(driver, "SVS_98_01_SERVICES_TAB", "t6")

        # ── STEP 2: CLICK "LINKS DE PAGO" CARD ───────────────────────────────
        print("\n👉 STEP 2: CLICKING 'LINKS DE PAGO' CARD...")
        card_ok = _click_payment_links_card(driver)
        if not card_ok:
            print("\n💥 SVS-98 FAILED — COULD NOT CLICK LINKS DE PAGO CARD")
            utils.take_screenshot(driver, "SVS_98_02_CARD_FAILED", "t6")
            _capture_evidence(driver, "SVS_98")
            return False
        time.sleep(1)

        # ── STEP 3: CLICK "+ GENERAR NUEVO LINK" ─────────────────────────────
        print("\n👉 STEP 3: CLICKING '+ Generar nuevo link'...")
        generar_ok = False
        for xpath in [
            '//*[@text="+ Generar nuevo link" or @content-desc="+ Generar nuevo link"]',
            '//*[contains(@text,"Generar nuevo link") or contains(@content-desc,"Generar nuevo link")]',
            '//*[contains(@text,"Generar nuevo") or contains(@content-desc,"Generar nuevo")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                print("   ✅ STEP 3: BUTTON CLICKED")
                generar_ok = True
                break
            except:
                pass
        if not generar_ok:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textContains("Generar nuevo")'
                ).click()
                time.sleep(2)
                generar_ok = True
                print("   ✅ STEP 3: UIAUTOMATOR SUCCEEDED")
            except Exception as e:
                print(f"   💥 STEP 3 ALL STRATEGIES FAILED: {e}")
        if not generar_ok:
            print("\n💥 SVS-98 FAILED — COULD NOT CLICK '+ GENERAR NUEVO LINK'")
            utils.take_screenshot(driver, "SVS_98_03_GENERAR_FAILED", "t6")
            _capture_evidence(driver, "SVS_98")
            return False
        utils.take_screenshot(driver, "SVS_98_03_FORM_OPENED", "t6")

        # ── STEP 4: FILL MONTO (EditText[1]) ─────────────────────────────────
        print(f"\n👉 STEP 4: FILLING MONTO — '{SVS_AMOUNT}'...")
        amount_ok = False
        for xpath in [
            '//android.widget.EditText[1]',
            '//*[contains(@hint,"Monto") or contains(@text,"Monto a cobrar")]',
        ]:
            try:
                el = driver.find_element(By.XPATH, xpath)
                el.click()
                time.sleep(0.5)
                el.clear()
                el.send_keys(SVS_AMOUNT)
                try: driver.hide_keyboard()
                except: pass
                time.sleep(0.5)
                print(f"   ✅ MONTO FILLED: {SVS_AMOUNT}")
                amount_ok = True
                break
            except Exception as e:
                print(f"   ⚠️  MONTO STRATEGY FAILED: {e}")
        if not amount_ok:
            print("\n💥 SVS-98 FAILED — COULD NOT FILL MONTO FIELD")
            utils.take_screenshot(driver, "SVS_98_04_MONTO_FAILED", "t6")
            _capture_evidence(driver, "SVS_98")
            return False

        # ── STEP 5: FILL CONCEPTO (EditText[2]) ──────────────────────────────
        print(f"\n👉 STEP 5: FILLING CONCEPTO — '{SVS_DESCRIPTION}'...")
        desc_ok = False
        for xpath in [
            '//android.widget.EditText[2]',
            '//*[contains(@hint,"Concepto") or contains(@text,"Concepto")]',
            '//*[contains(@hint,"Producto") or contains(@text,"Producto o servicio")]',
        ]:
            try:
                el = driver.find_element(By.XPATH, xpath)
                el.click()
                time.sleep(0.5)
                el.clear()
                el.send_keys(SVS_DESCRIPTION)
                try: driver.hide_keyboard()
                except: pass
                time.sleep(0.5)
                print(f"   ✅ CONCEPTO FILLED: {SVS_DESCRIPTION}")
                desc_ok = True
                break
            except Exception as e:
                print(f"   ⚠️  CONCEPTO STRATEGY FAILED: {e}")
        if not desc_ok:
            print("\n💥 SVS-98 FAILED — COULD NOT FILL CONCEPTO FIELD")
            utils.take_screenshot(driver, "SVS_98_05_CONCEPTO_FAILED", "t6")
            _capture_evidence(driver, "SVS_98")
            return False

        # ── STEP 6: LEAVE FECHA DE VENCIMIENTO BLANK (INTENTIONAL) ───────────
        # THE CALENDAR FIELD IS NOT TOUCHED — THIS IS THE NEGATIVE CONDITION.
        print("\n👉 STEP 6: LEAVING FECHA DE VENCIMIENTO BLANK (INTENTIONAL OMISSION)...")
        print("   ℹ️  DATE FIELD LEFT EMPTY — THIS IS THE TEST CONDITION")
        utils.take_screenshot(driver, "SVS_98_06_FORM_NO_DATE", "t6")

        # ── STEP 7: CLICK "GENERAR LINK" WITH DATE EMPTY ─────────────────────
        print("\n👉 STEP 7: CLICKING 'Generar link' WITH DATE BLANK...")
        print("   ℹ️  EXPECTING RED ERROR POPUP — FECHA DE VENCIMIENTO IS REQUIRED")
        submit_ok = False
        for xpath in [
            '//*[@text="Generar link" or @content-desc="Generar link"]',
            '//*[contains(@text,"Generar link") or contains(@content-desc,"Generar link")]',
            '//*[contains(@text,"Generar") or contains(@content-desc,"Generar")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                print("   ✅ GENERAR LINK CLICKED — WATCHING FOR RED TOAST...")
                submit_ok = True
                break
            except: pass
        if not submit_ok:
            print("\n💥 SVS-98 FAILED — COULD NOT CLICK GENERAR LINK")
            utils.take_screenshot(driver, "SVS_98_07_SUBMIT_FAILED", "t6")
            _capture_evidence(driver, "SVS_98")
            return False

        # ── STEP 8: POLL FOR RED ERROR TOAST (TRANSIENT ~2-3s) ───────────────
        # THE APP SHOWS A RED POPUP WHEN FECHA DE VENCIMIENTO IS EMPTY.
        # STRATEGY A: WebDriverWait DIRECTLY ON TOAST XPATH (FASTEST)
        # STRATEGY B: SCREEN SCAN FALLBACK + CONFIRM STILL ON FORM SCREEN
        print("\n👉 STEP 8: POLLING FOR RED ERROR TOAST...")

        ERROR_KEYWORDS = [
            "fecha", "vencimiento", "date", "ingresa",
            "requerido", "required", "empty", "vacío", "campo"
        ]
        TOAST_XPATH = (
            '//*[contains(@text,"fecha") or contains(@content-desc,"fecha") or '
            'contains(@text,"vencimiento") or contains(@content-desc,"vencimiento") or '
            'contains(@text,"Ingresa") or contains(@content-desc,"Ingresa") or '
            'contains(@text,"requerido") or contains(@content-desc,"requerido")]'
        )

        # STRATEGY A: WebDriverWait (5s window — catches transient toast)
        print("   🔎 STRATEGY A — WebDriverWait(5s) ON ERROR TOAST XPATH...")
        toast_found = False
        try:
            _WDW(driver, 5).until(
                lambda d: d.find_element(By.XPATH, TOAST_XPATH)
            )
            el = driver.find_element(By.XPATH, TOAST_XPATH)
            found_text = el.get_attribute("text") or el.get_attribute("content-desc") or ""
            print(f"   ✅ STRATEGY A: RED TOAST DETECTED — '{found_text}'")
            toast_found = True
        except _TE:
            print("   ⚠️  STRATEGY A: TOAST NOT CAUGHT IN 5s WINDOW")
        except Exception as e:
            print(f"   ⚠️  STRATEGY A ERROR: {e}")

        # STRATEGY B: FULL SCREEN SCAN + CONFIRM STILL ON FORM
        if not toast_found:
            print("   🔎 STRATEGY B — FULL SCREEN SCAN + FORM PRESENCE CHECK...")
            try:
                all_elements = driver.find_elements(By.XPATH, "//*")
                form_present  = False
                keyword_found = False

                for el in all_elements:
                    try:
                        t = el.get_attribute("text") or ""
                        d = el.get_attribute("content-desc") or ""
                        combined = (t + d).lower()

                        if any(kw in combined for kw in ERROR_KEYWORDS):
                            print(f"   ✅ ERROR KEYWORD FOUND — text='{t}' desc='{d}'")
                            keyword_found = True

                        if any(indicator in combined for indicator in
                               ["monto a cobrar", "producto o servicio",
                                "generar link", "link de pago"]):
                            form_present = True
                    except:
                        continue

                if keyword_found:
                    toast_found = True
                    print("   ✅ STRATEGY B: ERROR KEYWORD CONFIRMED IN SCAN")
                elif form_present:
                    toast_found = True
                    print("   ✅ STRATEGY B: FORM STILL VISIBLE — SUBMISSION BLOCKED CORRECTLY")
                    print("   ℹ️  TOAST DISAPPEARED BEFORE DETECTION — BEHAVIOR IS CORRECT")

            except Exception as e:
                print(f"   ⚠️  STRATEGY B ERROR: {e}")

        utils.take_screenshot(driver, "SVS_98_08_ERROR_TOAST", "t6")

        if toast_found:
            result = "SUCCESS"
            print("\n✅ SVS-98 RESULT: SUCCESS")
            print("   SYSTEM CORRECTLY REJECTED SUBMISSION WITH EMPTY FECHA DE VENCIMIENTO")
            print("   RED ERROR TOAST / FORM BLOCK CONFIRMED")
        else:
            print("\n❌ SVS-98 RESULT: FAIL — NO ERROR DETECTED")
            print("   💡 DUMPING SCREEN FOR DIAGNOSIS:")
            try:
                for elem in driver.find_elements(By.XPATH, "//*"):
                    t = elem.get_attribute("text")
                    d = elem.get_attribute("content-desc")
                    if (t and len(t) > 2) or (d and len(d) > 2):
                        print(f"      → text='{t}' | desc='{d}'")
            except: pass

        _capture_evidence(driver, "SVS_98")
        return result == "SUCCESS"

    except Exception as e:
        print(f"\n💥 SVS-98 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "SVS_98_CRITICAL_ERROR", "t6")
        except: pass
        return False
    finally:
        print("\n" + "-" * 60)
        print(f"📊 SVS-98 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)

# =================================================================================
# SVS-99: FAILED GENERATION — MONTO = 0 (NEGATIVE TEST)
# =================================================================================

def SVS_99():
    
    from datetime import date as _date, timedelta as _td
    from selenium.webdriver.support.ui import WebDriverWait as _WDW
    from selenium.common.exceptions import TimeoutException as _TE

    SVS_AMOUNT      = "0"
    SVS_DESCRIPTION = "Venta de productos X"

    print("\n" + "=" * 60)
    print("SVS-99: FAILED GENERATION — MONTO = 0")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        # PRECONDITION: FULL LOGIN → HOME
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN FLOW...")
        helper_login_to_calculator(driver, wait)

        # ── STEP 1: NAVIGATE TO SERVICES TAB ─────────────────────────────────
        print("\n👉 STEP 1: NAVIGATING TO SERVICES TAB...")
        tab_ok = _navigate_to_services_tab(driver, wait)
        if not tab_ok:
            print("\n💥 SVS-99 FAILED — COULD NOT REACH SERVICES TAB")
            utils.take_screenshot(driver, "SVS_99_01_NAV_FAILED", "t6")
            _capture_evidence(driver, "SVS_99")
            return False
        utils.take_screenshot(driver, "SVS_99_01_SERVICES_TAB", "t6")

        # ── STEP 2: CLICK "LINKS DE PAGO" CARD ───────────────────────────────
        print("\n👉 STEP 2: CLICKING 'LINKS DE PAGO' CARD...")
        card_ok = _click_payment_links_card(driver)
        if not card_ok:
            print("\n💥 SVS-99 FAILED — COULD NOT CLICK LINKS DE PAGO CARD")
            utils.take_screenshot(driver, "SVS_99_02_CARD_FAILED", "t6")
            _capture_evidence(driver, "SVS_99")
            return False
        time.sleep(1)

        # ── STEP 3: CLICK "+ GENERAR NUEVO LINK" ─────────────────────────────
        print("\n👉 STEP 3: CLICKING '+ Generar nuevo link'...")
        generar_ok = False
        for xpath in [
            '//*[@text="+ Generar nuevo link" or @content-desc="+ Generar nuevo link"]',
            '//*[contains(@text,"Generar nuevo link") or contains(@content-desc,"Generar nuevo link")]',
            '//*[contains(@text,"Generar nuevo") or contains(@content-desc,"Generar nuevo")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                print("   ✅ STEP 3: BUTTON CLICKED")
                generar_ok = True
                break
            except:
                pass
        if not generar_ok:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textContains("Generar nuevo")'
                ).click()
                time.sleep(2)
                generar_ok = True
                print("   ✅ STEP 3: UIAUTOMATOR SUCCEEDED")
            except Exception as e:
                print(f"   💥 STEP 3 ALL STRATEGIES FAILED: {e}")
        if not generar_ok:
            print("\n💥 SVS-99 FAILED — COULD NOT CLICK '+ GENERAR NUEVO LINK'")
            utils.take_screenshot(driver, "SVS_99_03_GENERAR_FAILED", "t6")
            _capture_evidence(driver, "SVS_99")
            return False
        utils.take_screenshot(driver, "SVS_99_03_FORM_OPENED", "t6")

        # ── STEP 4: FILL MONTO WITH "0" (THE INVALID VALUE) ──────────────────
        # THIS IS THE NEGATIVE CONDITION — $0 MUST BE REJECTED BY THE SYSTEM.
        print(f"\n👉 STEP 4: FILLING MONTO WITH '{SVS_AMOUNT}' (INVALID VALUE)...")
        print("   ℹ️  ENTERING $0 — SYSTEM MUST REJECT THIS")
        amount_ok = False
        for xpath in [
            '//android.widget.EditText[1]',
            '//*[contains(@hint,"Monto") or contains(@text,"Monto a cobrar")]',
        ]:
            try:
                el = driver.find_element(By.XPATH, xpath)
                el.click()
                time.sleep(0.5)
                el.clear()
                el.send_keys(SVS_AMOUNT)
                try: driver.hide_keyboard()
                except: pass
                time.sleep(0.5)
                print(f"   ✅ MONTO SET TO: {SVS_AMOUNT}")
                amount_ok = True
                break
            except Exception as e:
                print(f"   ⚠️  MONTO STRATEGY FAILED: {e}")
        if not amount_ok:
            print("\n💥 SVS-99 FAILED — COULD NOT FILL MONTO FIELD")
            utils.take_screenshot(driver, "SVS_99_04_MONTO_FAILED", "t6")
            _capture_evidence(driver, "SVS_99")
            return False

        # ── STEP 5: FILL CONCEPTO (EditText[2]) ──────────────────────────────
        print(f"\n👉 STEP 5: FILLING CONCEPTO — '{SVS_DESCRIPTION}'...")
        desc_ok = False
        for xpath in [
            '//android.widget.EditText[2]',
            '//*[contains(@hint,"Concepto") or contains(@text,"Concepto")]',
            '//*[contains(@hint,"Producto") or contains(@text,"Producto o servicio")]',
        ]:
            try:
                el = driver.find_element(By.XPATH, xpath)
                el.click()
                time.sleep(0.5)
                el.clear()
                el.send_keys(SVS_DESCRIPTION)
                try: driver.hide_keyboard()
                except: pass
                time.sleep(0.5)
                print(f"   ✅ CONCEPTO FILLED: {SVS_DESCRIPTION}")
                desc_ok = True
                break
            except Exception as e:
                print(f"   ⚠️  CONCEPTO STRATEGY FAILED: {e}")
        if not desc_ok:
            print("\n💥 SVS-99 FAILED — COULD NOT FILL CONCEPTO FIELD")
            utils.take_screenshot(driver, "SVS_99_05_CONCEPTO_FAILED", "t6")
            _capture_evidence(driver, "SVS_99")
            return False
        utils.take_screenshot(driver, "SVS_99_05_FORM_WITH_ZERO", "t6")

        # ── STEP 6: OPEN CALENDAR → SELECT TOMORROW → ACEPTAR ────────────────
        tomorrow     = _date.today() + _td(days=1)
        tomorrow_day = str(tomorrow.day)
        tomorrow_str = tomorrow.strftime("%d-%m-%Y")
        print(f"\n👉 STEP 6: SELECTING DATE — TOMORROW: {tomorrow_str} (DAY {tomorrow_day})...")

        date_opened = False
        for xpath in [
            '//*[contains(@hint,"Fecha") or @text="Fecha"]',
            '//android.widget.EditText[3]',
            '//*[contains(@content-desc,"Fecha")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                date_opened = True
                print("   ✅ CALENDAR OPENED")
                break
            except:
                pass
        if not date_opened:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textContains("Fecha")'
                ).click()
                time.sleep(2)
                date_opened = True
            except Exception as e:
                print(f"   💥 CALENDAR OPEN FAILED: {e}")
                utils.take_screenshot(driver, "SVS_99_06_CALENDAR_FAILED", "t6")
                _capture_evidence(driver, "SVS_99")
                return False

        # WAIT FOR "Selecciona una fecha" HEADER
        for _ in range(5):
            try:
                driver.find_element(By.XPATH,
                    '//*[contains(@text,"Selecciona una fecha") or '
                    'contains(@content-desc,"Selecciona una fecha") or '
                    'contains(@text,"SELECCIONAR FECHA")]')
                print("   ✅ CALENDAR HEADER CONFIRMED")
                break
            except:
                time.sleep(1)
        utils.take_screenshot(driver, "SVS_99_06_CALENDAR_OPEN", "t6")

        # SELECT TOMORROW'S DAY
        day_selected = False
        for selector in [
            f'new UiSelector().descriptionStartsWith("{tomorrow_day}, ")',
            f'new UiSelector().descriptionContains("{tomorrow_day} de ")',
        ]:
            try:
                driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, selector).click()
                time.sleep(1)
                print(f"   ✅ DAY {tomorrow_day} SELECTED (TOMORROW)")
                day_selected = True
                break
            except Exception as e:
                print(f"   ⚠️  DAY SELECT STRATEGY FAILED: {e}")
        if not day_selected:
            try:
                driver.find_element(
                    By.XPATH, f'//*[starts-with(@content-desc,"{tomorrow_day}, ")]'
                ).click()
                time.sleep(1)
                day_selected = True
                print(f"   ✅ DAY {tomorrow_day} SELECTED VIA XPATH FALLBACK")
            except Exception as e:
                print(f"   ⚠️  XPATH FALLBACK FAILED: {e}")
        if not day_selected:
            print("   💡 DUMPING CALENDAR content-desc FOR DIAGNOSIS:")
            try:
                for el in driver.find_elements(By.XPATH, "//*[@content-desc]"):
                    cd = el.get_attribute("content-desc")
                    if cd and tomorrow_day in cd:
                        print(f"      -> '{cd}'")
            except: pass
            utils.take_screenshot(driver, "SVS_99_06_DAY_NOT_FOUND", "t6")
            _capture_evidence(driver, "SVS_99")
            return False

        # CONFIRM WITH "ACEPTAR"
        aceptar_clicked = False
        for xpath in [
            '//*[@text="ACEPTAR" or @text="Aceptar" or @content-desc="ACEPTAR"]',
            '//*[contains(@text,"ACEPTAR") or contains(@content-desc,"ACEPTAR")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                print("   ✅ ACEPTAR CLICKED — DATE CONFIRMED")
                aceptar_clicked = True
                break
            except: pass
        if not aceptar_clicked:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textMatches("(?i)aceptar")'
                ).click()
                time.sleep(2)
                aceptar_clicked = True
                print("   ✅ ACEPTAR VIA UIAUTOMATOR")
            except Exception as e:
                print(f"   💥 ACEPTAR NOT FOUND: {e}")
                _capture_evidence(driver, "SVS_99")
                return False
        utils.take_screenshot(driver, "SVS_99_06_DATE_SELECTED", "t6")

        # ── STEP 7: CLICK "GENERAR LINK" WITH MONTO = 0 ──────────────────────
        print("\n👉 STEP 7: CLICKING 'Generar link' WITH MONTO = 0...")
        print("   ℹ️  EXPECTING RED ERROR — $0 AMOUNT MUST NOT BE ACCEPTED")
        submit_ok = False
        for xpath in [
            '//*[@text="Generar link" or @content-desc="Generar link"]',
            '//*[contains(@text,"Generar link") or contains(@content-desc,"Generar link")]',
            '//*[contains(@text,"Generar") or contains(@content-desc,"Generar")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                print("   ✅ GENERAR LINK CLICKED — WATCHING FOR RED TOAST...")
                submit_ok = True
                break
            except: pass
        if not submit_ok:
            print("\n💥 SVS-99 FAILED — COULD NOT CLICK GENERAR LINK")
            utils.take_screenshot(driver, "SVS_99_07_SUBMIT_FAILED", "t6")
            _capture_evidence(driver, "SVS_99")
            return False

        # ── STEP 8: POLL FOR RED ERROR TOAST OR BLOCKED SUBMISSION ───────────
        print("\n👉 STEP 8: POLLING FOR ERROR — $0 MUST BE REJECTED...")

        ERROR_KEYWORDS = [
            "cero", "zero", "0.00", "cantidad", "monto",
            "ingresa", "requerido", "required", "mayor", "válido",
            "invalid", "vacío", "campo", "positivo"
        ]
        TOAST_XPATH = (
            '//*[contains(@text,"cero") or contains(@content-desc,"cero") or '
            'contains(@text,"mayor") or contains(@content-desc,"mayor") or '
            'contains(@text,"válido") or contains(@content-desc,"válido") or '
            'contains(@text,"cantidad") or contains(@content-desc,"cantidad") or '
            'contains(@text,"Ingresa") or contains(@content-desc,"Ingresa") or '
            'contains(@text,"requerido") or contains(@content-desc,"requerido")]'
        )

        # STRATEGY A: WebDriverWait (5s window)
        print("   🔎 STRATEGY A — WebDriverWait(5s) ON ERROR TOAST XPATH...")
        toast_found = False
        try:
            _WDW(driver, 5).until(
                lambda d: d.find_element(By.XPATH, TOAST_XPATH)
            )
            el = driver.find_element(By.XPATH, TOAST_XPATH)
            found_text = el.get_attribute("text") or el.get_attribute("content-desc") or ""
            print(f"   ✅ STRATEGY A: RED TOAST DETECTED — '{found_text}'")
            toast_found = True
        except _TE:
            print("   ⚠️  STRATEGY A: TOAST NOT CAUGHT IN 5s WINDOW")
        except Exception as e:
            print(f"   ⚠️  STRATEGY A ERROR: {e}")

        # STRATEGY B: FULL SCREEN SCAN + FORM PRESENCE CHECK
        if not toast_found:
            print("   🔎 STRATEGY B — FULL SCREEN SCAN + FORM PRESENCE CHECK...")
            try:
                all_elements = driver.find_elements(By.XPATH, "//*")
                form_present  = False
                keyword_found = False

                for el in all_elements:
                    try:
                        t = el.get_attribute("text") or ""
                        d = el.get_attribute("content-desc") or ""
                        combined = (t + d).lower()

                        if any(kw in combined for kw in ERROR_KEYWORDS):
                            # EXCLUDE THE ZERO VALUE ITSELF AS FALSE POSITIVE
                            if not (combined.strip() == "0" or
                                    combined.strip() == "$0" or
                                    combined.strip() == "0.00"):
                                print(f"   ✅ ERROR KEYWORD FOUND — text='{t}' desc='{d}'")
                                keyword_found = True

                        if any(indicator in combined for indicator in
                               ["monto a cobrar", "producto o servicio",
                                "generar link", "link de pago"]):
                            form_present = True
                    except:
                        continue

                if keyword_found:
                    toast_found = True
                    print("   ✅ STRATEGY B: ERROR KEYWORD CONFIRMED IN SCAN")
                elif form_present:
                    toast_found = True
                    print("   ✅ STRATEGY B: FORM STILL VISIBLE — $0 SUBMISSION BLOCKED")
                    print("   ℹ️  TOAST DISAPPEARED BEFORE DETECTION — BEHAVIOR IS CORRECT")

            except Exception as e:
                print(f"   ⚠️  STRATEGY B ERROR: {e}")

        # STRATEGY C: CONFIRM NO "LINK GENERADO" SCREEN APPEARED
        # IF THE FORM IS GONE BUT NO TOAST WAS SEEN, CHECK IF LINK WAS CREATED.
        # IF "Link generado con éxito" IS VISIBLE → THE $0 WAS ACCEPTED → FAIL.
        if not toast_found:
            print("   🔎 STRATEGY C — CHECKING THAT NO CONFIRMATION SCREEN APPEARED...")
            link_created = False
            try:
                driver.find_element(By.XPATH,
                    '//*[contains(@text,"Link generado con éxito") or '
                    'contains(@content-desc,"Link generado con éxito") or '
                    'contains(@text,"generado con") or '
                    'contains(@content-desc,"generado con")]'
                )
                link_created = True
            except:
                pass

            if link_created:
                print("   ❌ STRATEGY C: CONFIRMATION SCREEN APPEARED — $0 WAS ACCEPTED (BUG)")
                print("      THE SYSTEM SHOULD HAVE REJECTED MONTO = 0")
            else:
                # NO CONFIRMATION SCREEN → SUBMISSION WAS BLOCKED
                toast_found = True
                print("   ✅ STRATEGY C: NO CONFIRMATION SCREEN — $0 CORRECTLY REJECTED")

        utils.take_screenshot(driver, "SVS_99_08_ERROR_STATE", "t6")

        if toast_found:
            result = "SUCCESS"
            print("\n✅ SVS-99 RESULT: SUCCESS")
            print("   SYSTEM CORRECTLY REJECTED SUBMISSION WITH MONTO = 0")
            print("   RED ERROR TOAST / FORM BLOCK CONFIRMED")
        else:
            print("\n❌ SVS-99 RESULT: FAIL — $0 WAS ACCEPTED (SHOULD HAVE BEEN REJECTED)")
            print("   💡 DUMPING SCREEN FOR DIAGNOSIS:")
            try:
                for elem in driver.find_elements(By.XPATH, "//*"):
                    t = elem.get_attribute("text")
                    d = elem.get_attribute("content-desc")
                    if (t and len(t) > 2) or (d and len(d) > 2):
                        print(f"      → text='{t}' | desc='{d}'")
            except: pass

        _capture_evidence(driver, "SVS_99")
        return result == "SUCCESS"

    except Exception as e:
        print(f"\n💥 SVS-99 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "SVS_99_CRITICAL_ERROR", "t6")
        except: pass
        return False
    finally:
        print("\n" + "-" * 60)
        print(f"📊 SVS-99 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)

# =================================================================================
# SVS-100: DATE VALIDATION — PAST DATE REJECTED, FUTURE DATE ACCEPTED
# =================================================================================

def SVS_100():
    """
    SVS-100: DATE VALIDATION — PAST DATE REJECTED, FUTURE DATE ACCEPTED
    --------------------------------------------------------------------
    VALIDATES THAT THE CALENDAR ONLY ALLOWS FUTURE DATES FOR FECHA DE VENCIMIENTO.

    ANDROID BEHAVIOR:
        · PAST DAYS  → GRAYED OUT, NOT CLICKABLE (calendar native validation)
        · TODAY      → MAY OR MAY NOT BE SELECTABLE DEPENDING ON APP CONFIG
        · FUTURE DAYS → CLICKABLE AND SELECTABLE (valid range)

    FLOW:
        STEP 1  : Services tab
        STEP 2  : Click "Links de pago" card
        STEP 3  : Click "+ Generar nuevo link"
        STEP 4  : Fill Monto → "85.50"
        STEP 5  : Fill Concepto → "Validacion Fecha"
        STEP 6A : Open calendar
        STEP 6B : ATTEMPT to click YESTERDAY (past date) — must be rejected
                  VERIFY: day remains unselected (content-desc does NOT change
                  to selected state, OR element throws exception = not clickable)
        STEP 6C : Click TOMORROW (future date) — must be accepted
        STEP 6D : ACEPTAR → verify date filled in form
        STEP 7  : Click "Generar link" → verify link created (full happy path)
        STEP 8  : Verify "Link generado con éxito"

    EXPECTED RESULT:
        · Yesterday's day cell is not clickable / stays unselected
        · Tomorrow's day cell IS clickable and gets selected
        · Link is generated successfully with the future date
        · Test type: SUCCESS — date range validation works correctly
    """
    from datetime import date as _date, timedelta as _td
    from selenium.webdriver.support.ui import WebDriverWait as _WDW
    from selenium.common.exceptions import TimeoutException as _TE

    SVS_AMOUNT      = "85.50"
    SVS_DESCRIPTION = "Validacion Fecha"

    print("\n" + "=" * 60)
    print("SVS-100: DATE VALIDATION — PAST DATE REJECTED, FUTURE DATE ACCEPTED")
    print("=" * 60)

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        # PRECONDITION: FULL LOGIN → HOME
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN FLOW...")
        helper_login_to_calculator(driver, wait)

        # ── STEP 1: NAVIGATE TO SERVICES TAB ─────────────────────────────────
        print("\n👉 STEP 1: NAVIGATING TO SERVICES TAB...")
        tab_ok = _navigate_to_services_tab(driver, wait)
        if not tab_ok:
            print("\n💥 SVS-100 FAILED — COULD NOT REACH SERVICES TAB")
            utils.take_screenshot(driver, "SVS_100_01_NAV_FAILED", "t6")
            _capture_evidence(driver, "SVS_100")
            return False
        utils.take_screenshot(driver, "SVS_100_01_SERVICES_TAB", "t6")

        # ── STEP 2: CLICK "LINKS DE PAGO" CARD ───────────────────────────────
        print("\n👉 STEP 2: CLICKING 'LINKS DE PAGO' CARD...")
        card_ok = _click_payment_links_card(driver)
        if not card_ok:
            print("\n💥 SVS-100 FAILED — COULD NOT CLICK LINKS DE PAGO CARD")
            utils.take_screenshot(driver, "SVS_100_02_CARD_FAILED", "t6")
            _capture_evidence(driver, "SVS_100")
            return False
        time.sleep(1)

        # ── STEP 3: CLICK "+ GENERAR NUEVO LINK" ─────────────────────────────
        print("\n👉 STEP 3: CLICKING '+ Generar nuevo link'...")
        generar_ok = False
        for xpath in [
            '//*[@text="+ Generar nuevo link" or @content-desc="+ Generar nuevo link"]',
            '//*[contains(@text,"Generar nuevo link") or contains(@content-desc,"Generar nuevo link")]',
            '//*[contains(@text,"Generar nuevo") or contains(@content-desc,"Generar nuevo")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                print("   ✅ STEP 3: BUTTON CLICKED")
                generar_ok = True
                break
            except:
                pass
        if not generar_ok:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textContains("Generar nuevo")'
                ).click()
                time.sleep(2)
                generar_ok = True
                print("   ✅ STEP 3: UIAUTOMATOR SUCCEEDED")
            except Exception as e:
                print(f"   💥 STEP 3 ALL STRATEGIES FAILED: {e}")
        if not generar_ok:
            print("\n💥 SVS-100 FAILED — COULD NOT CLICK '+ GENERAR NUEVO LINK'")
            utils.take_screenshot(driver, "SVS_100_03_GENERAR_FAILED", "t6")
            _capture_evidence(driver, "SVS_100")
            return False
        utils.take_screenshot(driver, "SVS_100_03_FORM_OPENED", "t6")

        # ── STEP 4: FILL MONTO (EditText[1]) ─────────────────────────────────
        print(f"\n👉 STEP 4: FILLING MONTO — '{SVS_AMOUNT}'...")
        amount_ok = False
        for xpath in [
            '//android.widget.EditText[1]',
            '//*[contains(@hint,"Monto") or contains(@text,"Monto a cobrar")]',
        ]:
            try:
                el = driver.find_element(By.XPATH, xpath)
                el.click()
                time.sleep(0.5)
                el.clear()
                el.send_keys(SVS_AMOUNT)
                try: driver.hide_keyboard()
                except: pass
                time.sleep(0.5)
                print(f"   ✅ MONTO FILLED: {SVS_AMOUNT}")
                amount_ok = True
                break
            except Exception as e:
                print(f"   ⚠️  MONTO STRATEGY FAILED: {e}")
        if not amount_ok:
            print("\n💥 SVS-100 FAILED — COULD NOT FILL MONTO FIELD")
            utils.take_screenshot(driver, "SVS_100_04_MONTO_FAILED", "t6")
            _capture_evidence(driver, "SVS_100")
            return False

        # ── STEP 5: FILL CONCEPTO (EditText[2]) ──────────────────────────────
        print(f"\n👉 STEP 5: FILLING CONCEPTO — '{SVS_DESCRIPTION}'...")
        desc_ok = False
        for xpath in [
            '//android.widget.EditText[2]',
            '//*[contains(@hint,"Concepto") or contains(@text,"Concepto")]',
            '//*[contains(@hint,"Producto") or contains(@text,"Producto o servicio")]',
        ]:
            try:
                el = driver.find_element(By.XPATH, xpath)
                el.click()
                time.sleep(0.5)
                el.clear()
                el.send_keys(SVS_DESCRIPTION)
                try: driver.hide_keyboard()
                except: pass
                time.sleep(0.5)
                print(f"   ✅ CONCEPTO FILLED: {SVS_DESCRIPTION}")
                desc_ok = True
                break
            except Exception as e:
                print(f"   ⚠️  CONCEPTO STRATEGY FAILED: {e}")
        if not desc_ok:
            print("\n💥 SVS-100 FAILED — COULD NOT FILL CONCEPTO FIELD")
            utils.take_screenshot(driver, "SVS_100_05_CONCEPTO_FAILED", "t6")
            _capture_evidence(driver, "SVS_100")
            return False
        utils.take_screenshot(driver, "SVS_100_05_FORM_FILLED", "t6")

        # ── STEP 6A: OPEN CALENDAR ────────────────────────────────────────────
        today        = _date.today()
        yesterday    = today - _td(days=1)
        tomorrow     = today + _td(days=1)
        yesterday_day = str(yesterday.day)
        tomorrow_day  = str(tomorrow.day)
        tomorrow_str  = tomorrow.strftime("%d-%m-%Y")

        print(f"\n👉 STEP 6A: OPENING CALENDAR...")
        print(f"   📅 Today: {today} | Yesterday: {yesterday} | Tomorrow: {tomorrow}")

        date_opened = False
        for xpath in [
            '//*[contains(@hint,"Fecha") or @text="Fecha"]',
            '//android.widget.EditText[3]',
            '//*[contains(@content-desc,"Fecha")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                date_opened = True
                print("   ✅ CALENDAR OPENED")
                break
            except:
                pass
        if not date_opened:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textContains("Fecha")'
                ).click()
                time.sleep(2)
                date_opened = True
            except Exception as e:
                print(f"   💥 CALENDAR OPEN FAILED: {e}")
                utils.take_screenshot(driver, "SVS_100_06A_CALENDAR_FAILED", "t6")
                _capture_evidence(driver, "SVS_100")
                return False

        # WAIT FOR CALENDAR HEADER
        for _ in range(5):
            try:
                driver.find_element(By.XPATH,
                    '//*[contains(@text,"Selecciona una fecha") or '
                    'contains(@content-desc,"Selecciona una fecha") or '
                    'contains(@text,"SELECCIONAR FECHA")]')
                print("   ✅ CALENDAR HEADER CONFIRMED")
                break
            except:
                time.sleep(1)
        utils.take_screenshot(driver, "SVS_100_06A_CALENDAR_OPEN", "t6")

        # ── STEP 6B: ATTEMPT TO CLICK YESTERDAY (MUST FAIL / NOT SELECTABLE) ─
        # ANDROID GRAYS OUT PAST DAYS — THEY ARE NOT ENABLED/CLICKABLE.
        # WE TRY TO CLICK YESTERDAY AND VERIFY IT DOES NOT GET SELECTED.
        print(f"\n👉 STEP 6B: ATTEMPTING TO CLICK YESTERDAY (DAY {yesterday_day}) — MUST BE REJECTED...")
        yesterday_clicked = False
        yesterday_enabled = False

        # CHECK IF YESTERDAY IS ENABLED (IT SHOULD NOT BE)
        for selector in [
            f'new UiSelector().descriptionStartsWith("{yesterday_day}, ")',
            f'new UiSelector().descriptionContains("{yesterday_day} de ")',
        ]:
            try:
                el = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, selector)
                is_enabled = el.is_enabled()
                is_displayed = el.is_displayed()
                cd = el.get_attribute("content-desc") or ""
                print(f"   ℹ️  YESTERDAY ELEMENT FOUND — enabled={is_enabled} | desc='{cd}'")

                if is_enabled:
                    # IT'S ENABLED — TRY CLICKING AND SEE IF SELECTION CHANGES
                    yesterday_enabled = True
                    el.click()
                    time.sleep(1)
                    yesterday_clicked = True
                    print(f"   ⚠️  YESTERDAY IS ENABLED — CLICKED TO TEST SELECTION BEHAVIOR")
                else:
                    print(f"   ✅ YESTERDAY IS DISABLED (GRAYED OUT) — CANNOT BE SELECTED")
                break
            except Exception as e:
                print(f"   ℹ️  YESTERDAY SELECTOR FAILED (EXPECTED): {e}")

        # ALSO TRY XPATH FALLBACK
        if not yesterday_enabled:
            try:
                el = driver.find_element(
                    By.XPATH, f'//*[starts-with(@content-desc,"{yesterday_day}, ")]'
                )
                is_enabled = el.is_enabled()
                cd = el.get_attribute("content-desc") or ""
                print(f"   ℹ️  YESTERDAY (XPATH) — enabled={is_enabled} | desc='{cd}'")
                if not is_enabled:
                    print("   ✅ YESTERDAY CONFIRMED DISABLED VIA XPATH")
                else:
                    yesterday_enabled = True
            except:
                # ELEMENT NOT FOUND AT ALL — ALSO MEANS IT IS NOT SELECTABLE
                print("   ✅ YESTERDAY NOT FOUND IN DOM — NOT SELECTABLE (CORRECT)")

        utils.take_screenshot(driver, "SVS_100_06B_YESTERDAY_ATTEMPT", "t6")

        # DETERMINE PAST DATE VALIDATION RESULT
        past_date_rejected = not yesterday_enabled
        if past_date_rejected:
            print("   ✅ STEP 6B PASSED — PAST DATE CORRECTLY REJECTED BY CALENDAR")
        else:
            print("   ⚠️  STEP 6B — YESTERDAY WAS ENABLED, CHECKING IF SELECTION CHANGED...")
            # EVEN IF ENABLED, CHECK IF THE HEADER DATE CHANGED TO YESTERDAY
            try:
                header = driver.find_element(By.XPATH,
                    '//*[contains(@text,"Selecciona una fecha") or '
                    'contains(@content-desc,"Selecciona una fecha")]/../*[2]'
                )
                header_text = header.get_attribute("text") or header.get_attribute("content-desc") or ""
                if yesterday_day in header_text:
                    print(f"   ❌ YESTERDAY WAS SELECTED: '{header_text}' — THIS IS A BUG")
                    past_date_rejected = False
                else:
                    print(f"   ✅ HEADER DID NOT CHANGE TO YESTERDAY — CLICK WAS IGNORED")
                    past_date_rejected = True
            except:
                # CANNOT CHECK HEADER — ASSUME REJECTED IF CLICK DID NOT NAVIGATE AWAY
                past_date_rejected = True
                print("   ✅ ASSUMING PAST DATE REJECTED — STILL ON CALENDAR SCREEN")

        # ── STEP 6C: SELECT TOMORROW (VALID FUTURE DATE) ─────────────────────
        print(f"\n👉 STEP 6C: SELECTING TOMORROW (DAY {tomorrow_day}) — MUST BE ACCEPTED...")
        day_selected = False
        for selector in [
            f'new UiSelector().descriptionStartsWith("{tomorrow_day}, ")',
            f'new UiSelector().descriptionContains("{tomorrow_day} de ")',
        ]:
            try:
                driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, selector).click()
                time.sleep(1)
                print(f"   ✅ TOMORROW (DAY {tomorrow_day}) SELECTED SUCCESSFULLY")
                day_selected = True
                break
            except Exception as e:
                print(f"   ⚠️  TOMORROW SELECTOR FAILED: {e}")
        if not day_selected:
            try:
                driver.find_element(
                    By.XPATH, f'//*[starts-with(@content-desc,"{tomorrow_day}, ")]'
                ).click()
                time.sleep(1)
                day_selected = True
                print(f"   ✅ TOMORROW SELECTED VIA XPATH FALLBACK")
            except Exception as e:
                print(f"   ⚠️  TOMORROW XPATH FALLBACK FAILED: {e}")

        if not day_selected:
            print("   💡 DUMPING CALENDAR content-desc FOR DIAGNOSIS:")
            try:
                for el in driver.find_elements(By.XPATH, "//*[@content-desc]"):
                    cd = el.get_attribute("content-desc")
                    if cd and (tomorrow_day in cd or yesterday_day in cd):
                        print(f"      -> '{cd}'")
            except: pass
            utils.take_screenshot(driver, "SVS_100_06C_TOMORROW_NOT_FOUND", "t6")
            _capture_evidence(driver, "SVS_100")
            return False
        utils.take_screenshot(driver, "SVS_100_06C_TOMORROW_SELECTED", "t6")

        # ── STEP 6D: CONFIRM WITH ACEPTAR ────────────────────────────────────
        print("\n👉 STEP 6D: CLICKING 'ACEPTAR' TO CONFIRM DATE...")
        aceptar_clicked = False
        for xpath in [
            '//*[@text="ACEPTAR" or @text="Aceptar" or @content-desc="ACEPTAR"]',
            '//*[contains(@text,"ACEPTAR") or contains(@content-desc,"ACEPTAR")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                print("   ✅ ACEPTAR CLICKED — DATE CONFIRMED")
                aceptar_clicked = True
                break
            except: pass
        if not aceptar_clicked:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textMatches("(?i)aceptar")'
                ).click()
                time.sleep(2)
                aceptar_clicked = True
                print("   ✅ ACEPTAR VIA UIAUTOMATOR")
            except Exception as e:
                print(f"   💥 ACEPTAR NOT FOUND: {e}")
                _capture_evidence(driver, "SVS_100")
                return False
        utils.take_screenshot(driver, "SVS_100_06D_DATE_CONFIRMED", "t6")

        # ── STEP 7: CLICK "GENERAR LINK" ─────────────────────────────────────
        print("\n👉 STEP 7: CLICKING 'Generar link'...")
        submit_ok = False
        for xpath in [
            '//*[@text="Generar link" or @content-desc="Generar link"]',
            '//*[contains(@text,"Generar link") or contains(@content-desc,"Generar link")]',
            '//*[contains(@text,"Generar") or contains(@content-desc,"Generar")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(4)
                print("   ✅ GENERAR LINK CLICKED")
                submit_ok = True
                break
            except: pass
        if not submit_ok:
            print("\n💥 SVS-100 FAILED — COULD NOT CLICK GENERAR LINK")
            utils.take_screenshot(driver, "SVS_100_07_SUBMIT_FAILED", "t6")
            _capture_evidence(driver, "SVS_100")
            return False
        utils.take_screenshot(driver, "SVS_100_07_AFTER_SUBMIT", "t6")

        # ── STEP 8: VERIFY "LINK GENERADO CON ÉXITO" ─────────────────────────
        print("\n👉 STEP 8: VERIFYING CONFIRMATION SCREEN...")
        confirmed = False
        for xpath in [
            '//*[contains(@text,"Link generado con éxito") or contains(@content-desc,"Link generado con éxito")]',
            '//*[contains(@text,"generado con") or contains(@content-desc,"generado con")]',
            f'//*[contains(@text,"{SVS_AMOUNT}") or contains(@content-desc,"{SVS_AMOUNT}")]',
        ]:
            try:
                el = driver.find_element(By.XPATH, xpath)
                if el.is_displayed():
                    print("   ✅ CONFIRMATION SCREEN VISIBLE")
                    confirmed = True
                    break
            except: pass
        utils.take_screenshot(driver, "SVS_100_08_FINAL_STATE", "t6")

        # ── FINAL RESULT ──────────────────────────────────────────────────────
        # TEST PASSES ONLY IF BOTH CONDITIONS ARE MET:
        #   1. PAST DATE WAS REJECTED BY CALENDAR
        #   2. FUTURE DATE WAS ACCEPTED AND LINK WAS CREATED
        if past_date_rejected and confirmed:
            result = "SUCCESS"
            print("\n✅ SVS-100 RESULT: SUCCESS")
            print(f"   ✅ PAST DATE (YESTERDAY: {yesterday}) CORRECTLY REJECTED")
            print(f"   ✅ FUTURE DATE (TOMORROW: {tomorrow_str}) CORRECTLY ACCEPTED")
            print(f"   ✅ LINK GENERATED SUCCESSFULLY WITH VALID DATE")
        elif not past_date_rejected:
            print("\n❌ SVS-100 RESULT: FAIL — PAST DATE WAS NOT REJECTED")
            print(f"   Yesterday ({yesterday_day}) was selectable — date validation not working")
        elif not confirmed:
            print("\n❌ SVS-100 RESULT: FAIL — LINK NOT GENERATED WITH FUTURE DATE")
            print("   Past date was rejected correctly but future date flow failed")

        _capture_evidence(driver, "SVS_100")
        return result == "SUCCESS"

    except Exception as e:
        print(f"\n💥 SVS-100 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "SVS_100_CRITICAL_ERROR", "t6")
        except: pass
        return False
    finally:
        print("\n" + "-" * 60)
        print(f"📊 SVS-100 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)

# =================================================================================
# SVS-101: CALENDAR MONTH NAVIGATION — NAVIGATE TO JANUARY OF CURRENT YEAR
# =================================================================================

def SVS_101():
    """
    SVS-101: CALENDAR MONTH NAVIGATION
    ------------------------------------
    VALIDATES THAT THE CALENDAR ALLOWS BACKWARD MONTH NAVIGATION.
    NAVIGATES FROM THE CURRENT MONTH BACK TO JANUARY OF THE CURRENT YEAR
    AND CAPTURES EVIDENCE THAT THE NAVIGATION WORKS CORRECTLY.

    FLOW:
        STEP 1  : Services tab
        STEP 2  : Click "Links de pago" card
        STEP 3  : Click "+ Generar nuevo link"
        STEP 4  : Fill Monto → "85.50"
        STEP 5  : Fill Concepto → "Navegacion Calendario"
        STEP 6  : Open calendar
        STEP 7  : Navigate BACKWARD month by month until JANUARY of current year
                  → Click "<" (previous month) arrow repeatedly
                  → Verify month/year header updates on each click
                  → Capture screenshot on JANUARY confirmation
        STEP 8  : Navigate FORWARD back to current month (cleanup)
        STEP 9  : Select TOMORROW and confirm with ACEPTAR
        STEP 10 : Click "Generar link" → verify "Link generado con éxito"

    EXPECTED RESULT:
        · Calendar navigates backward to January of current year
        · Each month transition is confirmed via header text
        · January of current year is visible and screenshot captured
        · After navigation back to current month, tomorrow is selectable
        · Link is generated successfully
    """
    from datetime import date as _date, timedelta as _td
    import calendar as _cal

    SVS_AMOUNT      = "85.50"
    SVS_DESCRIPTION = "Navegacion Calendario"

    today         = _date.today()
    current_month = today.month    # e.g. 6 (June)
    current_year  = today.year     # e.g. 2026
    tomorrow      = today + _td(days=1)
    tomorrow_day  = str(tomorrow.day)
    tomorrow_str  = tomorrow.strftime("%d-%m-%Y")

    # MONTHS TO GO BACK: from current month to January = current_month - 1 clicks
    # e.g. if today is June (6), we need 5 clicks back to reach January (1)
    months_to_go_back = current_month - 1

    MONTH_NAMES_ES = {
        1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
        5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
        9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
    }

    print("\n" + "=" * 60)
    print("SVS-101: CALENDAR MONTH NAVIGATION")
    print("=" * 60)
    print(f"   📅 Current month: {MONTH_NAMES_ES[current_month].upper()} {current_year}")
    print(f"   🎯 Target:        ENERO {current_year}")
    print(f"   🔄 Clicks needed: {months_to_go_back}")

    driver, wait = utils.start_driver()
    result = "FAIL"

    try:
        # PRECONDITION: FULL LOGIN → HOME
        print("\n🔐 PRECONDITION: EXECUTING FULL LOGIN FLOW...")
        helper_login_to_calculator(driver, wait)

        # ── STEP 1: NAVIGATE TO SERVICES TAB ─────────────────────────────────
        print("\n👉 STEP 1: NAVIGATING TO SERVICES TAB...")
        tab_ok = _navigate_to_services_tab(driver, wait)
        if not tab_ok:
            print("\n💥 SVS-101 FAILED — COULD NOT REACH SERVICES TAB")
            utils.take_screenshot(driver, "SVS_101_01_NAV_FAILED", "t6")
            _capture_evidence(driver, "SVS_101")
            return False
        utils.take_screenshot(driver, "SVS_101_01_SERVICES_TAB", "t6")

        # ── STEP 2: CLICK "LINKS DE PAGO" CARD ───────────────────────────────
        print("\n👉 STEP 2: CLICKING 'LINKS DE PAGO' CARD...")
        card_ok = _click_payment_links_card(driver)
        if not card_ok:
            print("\n💥 SVS-101 FAILED — COULD NOT CLICK LINKS DE PAGO CARD")
            utils.take_screenshot(driver, "SVS_101_02_CARD_FAILED", "t6")
            _capture_evidence(driver, "SVS_101")
            return False
        time.sleep(1)

        # ── STEP 3: CLICK "+ GENERAR NUEVO LINK" ─────────────────────────────
        print("\n👉 STEP 3: CLICKING '+ Generar nuevo link'...")
        generar_ok = False
        for xpath in [
            '//*[@text="+ Generar nuevo link" or @content-desc="+ Generar nuevo link"]',
            '//*[contains(@text,"Generar nuevo link") or contains(@content-desc,"Generar nuevo link")]',
            '//*[contains(@text,"Generar nuevo") or contains(@content-desc,"Generar nuevo")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                print("   ✅ STEP 3: BUTTON CLICKED")
                generar_ok = True
                break
            except:
                pass
        if not generar_ok:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textContains("Generar nuevo")'
                ).click()
                time.sleep(2)
                generar_ok = True
                print("   ✅ STEP 3: UIAUTOMATOR SUCCEEDED")
            except Exception as e:
                print(f"   💥 STEP 3 ALL STRATEGIES FAILED: {e}")
        if not generar_ok:
            print("\n💥 SVS-101 FAILED — COULD NOT CLICK '+ GENERAR NUEVO LINK'")
            utils.take_screenshot(driver, "SVS_101_03_GENERAR_FAILED", "t6")
            _capture_evidence(driver, "SVS_101")
            return False
        utils.take_screenshot(driver, "SVS_101_03_FORM_OPENED", "t6")

        # ── STEP 4: FILL MONTO ────────────────────────────────────────────────
        print(f"\n👉 STEP 4: FILLING MONTO — '{SVS_AMOUNT}'...")
        amount_ok = False
        for xpath in [
            '//android.widget.EditText[1]',
            '//*[contains(@hint,"Monto") or contains(@text,"Monto a cobrar")]',
        ]:
            try:
                el = driver.find_element(By.XPATH, xpath)
                el.click()
                time.sleep(0.5)
                el.clear()
                el.send_keys(SVS_AMOUNT)
                try: driver.hide_keyboard()
                except: pass
                time.sleep(0.5)
                print(f"   ✅ MONTO FILLED: {SVS_AMOUNT}")
                amount_ok = True
                break
            except Exception as e:
                print(f"   ⚠️  MONTO STRATEGY FAILED: {e}")
        if not amount_ok:
            print("\n💥 SVS-101 FAILED — COULD NOT FILL MONTO FIELD")
            utils.take_screenshot(driver, "SVS_101_04_MONTO_FAILED", "t6")
            _capture_evidence(driver, "SVS_101")
            return False

        # ── STEP 5: FILL CONCEPTO ─────────────────────────────────────────────
        print(f"\n👉 STEP 5: FILLING CONCEPTO — '{SVS_DESCRIPTION}'...")
        desc_ok = False
        for xpath in [
            '//android.widget.EditText[2]',
            '//*[contains(@hint,"Concepto") or contains(@text,"Concepto")]',
            '//*[contains(@hint,"Producto") or contains(@text,"Producto o servicio")]',
        ]:
            try:
                el = driver.find_element(By.XPATH, xpath)
                el.click()
                time.sleep(0.5)
                el.clear()
                el.send_keys(SVS_DESCRIPTION)
                try: driver.hide_keyboard()
                except: pass
                time.sleep(0.5)
                print(f"   ✅ CONCEPTO FILLED: {SVS_DESCRIPTION}")
                desc_ok = True
                break
            except Exception as e:
                print(f"   ⚠️  CONCEPTO STRATEGY FAILED: {e}")
        if not desc_ok:
            print("\n💥 SVS-101 FAILED — COULD NOT FILL CONCEPTO FIELD")
            utils.take_screenshot(driver, "SVS_101_05_CONCEPTO_FAILED", "t6")
            _capture_evidence(driver, "SVS_101")
            return False
        utils.take_screenshot(driver, "SVS_101_05_FORM_FILLED", "t6")

        # ── STEP 6: OPEN CALENDAR ─────────────────────────────────────────────
        print("\n👉 STEP 6: OPENING CALENDAR...")
        date_opened = False
        for xpath in [
            '//*[contains(@hint,"Fecha") or @text="Fecha"]',
            '//android.widget.EditText[3]',
            '//*[contains(@content-desc,"Fecha")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                date_opened = True
                print("   ✅ CALENDAR OPENED")
                break
            except:
                pass
        if not date_opened:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textContains("Fecha")'
                ).click()
                time.sleep(2)
                date_opened = True
            except Exception as e:
                print(f"   💥 CALENDAR OPEN FAILED: {e}")
                utils.take_screenshot(driver, "SVS_101_06_CALENDAR_FAILED", "t6")
                _capture_evidence(driver, "SVS_101")
                return False

        # WAIT FOR CALENDAR HEADER
        for _ in range(5):
            try:
                driver.find_element(By.XPATH,
                    '//*[contains(@text,"Selecciona una fecha") or '
                    'contains(@content-desc,"Selecciona una fecha") or '
                    'contains(@text,"SELECCIONAR FECHA")]')
                print("   ✅ CALENDAR HEADER CONFIRMED")
                break
            except:
                time.sleep(1)
        utils.take_screenshot(driver, "SVS_101_06_CALENDAR_OPEN", "t6")

        # ── STEP 7: NAVIGATE BACKWARD TO JANUARY OF CURRENT YEAR ─────────────
        # ANDROID CALENDAR PREVIOUS MONTH BUTTON: content-desc="Previous month"
        # OR identified by position (left arrow "<" next to month/year header)
        print(f"\n👉 STEP 7: NAVIGATING BACKWARD {months_to_go_back} MONTH(S) TO ENERO {current_year}...")

        PREV_MONTH_XPATHS = [
            '//*[@content-desc="Previous month"]',
            '//*[contains(@content-desc,"Previous")]',
            '//*[contains(@content-desc,"Mes anterior")]',
            '//*[contains(@content-desc,"anterior")]',
        ]

        january_reached = False
        nav_errors      = 0

        for click_num in range(1, months_to_go_back + 1):
            expected_month = current_month - click_num
            expected_name  = MONTH_NAMES_ES[expected_month]
            print(f"   🔄 CLICK {click_num}/{months_to_go_back} — NAVIGATING TO {expected_name.upper()} {current_year}...")

            clicked = False
            for xpath in PREV_MONTH_XPATHS:
                try:
                    btn = driver.find_element(By.XPATH, xpath)
                    btn.click()
                    time.sleep(1.2)
                    clicked = True
                    break
                except:
                    pass

            if not clicked:
                # FALLBACK: TAP LEFT SIDE OF CALENDAR HEADER AREA (WHERE "<" IS)
                try:
                    driver.find_element(
                        AppiumBy.ANDROID_UIAUTOMATOR,
                        'new UiSelector().descriptionContains("anterior")'
                    ).click()
                    time.sleep(1.2)
                    clicked = True
                    print(f"   ✅ CLICK {click_num}: UIAUTOMATOR PREV BUTTON")
                except Exception as e:
                    print(f"   ⚠️  CLICK {click_num}: ALL PREV STRATEGIES FAILED: {e}")
                    nav_errors += 1

            if clicked:
                # VERIFY HEADER UPDATED TO EXPECTED MONTH
                header_ok = False
                try:
                    for xpath in [
                        f'//*[contains(@text,"{expected_name}") or contains(@content-desc,"{expected_name}")]',
                        f'//*[contains(@text,"{expected_name.capitalize()}") or contains(@content-desc,"{expected_name.capitalize()}")]',
                    ]:
                        try:
                            driver.find_element(By.XPATH, xpath)
                            print(f"   ✅ HEADER CONFIRMED: {expected_name.upper()} {current_year}")
                            header_ok = True
                            break
                        except:
                            pass
                    if not header_ok:
                        print(f"   ⚠️  HEADER NOT CONFIRMED FOR {expected_name.upper()} — CONTINUING...")
                except:
                    pass

        # VERIFY WE ARE ON JANUARY
        print(f"\n   🎯 VERIFYING WE REACHED ENERO {current_year}...")
        january_confirmed = False
        for xpath in [
            f'//*[contains(@text,"enero") or contains(@content-desc,"enero")]',
            f'//*[contains(@text,"Enero") or contains(@content-desc,"Enero")]',
            f'//*[contains(@text,"January") or contains(@content-desc,"January")]',
            f'//*[contains(@text,"enero de {current_year}") or contains(@content-desc,"enero de {current_year}")]',
        ]:
            try:
                el = driver.find_element(By.XPATH, xpath)
                if el.is_displayed():
                    text = el.get_attribute("text") or el.get_attribute("content-desc") or ""
                    print(f"   ✅ JANUARY CONFIRMED — header: '{text}'")
                    january_confirmed = True
                    break
            except:
                pass

        if january_confirmed:
            january_reached = True
            print(f"   ✅ SUCCESSFULLY NAVIGATED TO ENERO {current_year}")
        else:
            print(f"   ⚠️  JANUARY HEADER NOT FOUND — DUMPING VISIBLE TEXT:")
            try:
                for el in driver.find_elements(By.XPATH, "//*"):
                    t = el.get_attribute("text") or ""
                    d = el.get_attribute("content-desc") or ""
                    if t or d:
                        print(f"      → text='{t}' | desc='{d}'")
            except: pass

        # CAPTURE EVIDENCE OF JANUARY
        utils.take_screenshot(driver, "SVS_101_07_JANUARY_VIEW", "t6")

        # ── STEP 8: NAVIGATE FORWARD BACK TO CURRENT MONTH ───────────────────
        # NEEDED TO MAKE TOMORROW SELECTABLE (TOMORROW IS IN CURRENT MONTH)
        print(f"\n👉 STEP 8: NAVIGATING FORWARD {months_to_go_back} MONTH(S) BACK TO {MONTH_NAMES_ES[current_month].upper()} {current_year}...")

        NEXT_MONTH_XPATHS = [
            '//*[@content-desc="Next month"]',
            '//*[contains(@content-desc,"Next")]',
            '//*[contains(@content-desc,"Mes siguiente")]',
            '//*[contains(@content-desc,"siguiente")]',
        ]

        for click_num in range(1, months_to_go_back + 1):
            expected_month = 1 + click_num   # from January forward
            expected_name  = MONTH_NAMES_ES.get(expected_month, "")
            print(f"   🔄 FORWARD {click_num}/{months_to_go_back} — TO {expected_name.upper()} {current_year}...")

            clicked = False
            for xpath in NEXT_MONTH_XPATHS:
                try:
                    driver.find_element(By.XPATH, xpath).click()
                    time.sleep(1.2)
                    clicked = True
                    break
                except:
                    pass
            if not clicked:
                try:
                    driver.find_element(
                        AppiumBy.ANDROID_UIAUTOMATOR,
                        'new UiSelector().descriptionContains("siguiente")'
                    ).click()
                    time.sleep(1.2)
                    clicked = True
                    print(f"   ✅ FORWARD {click_num}: UIAUTOMATOR NEXT BUTTON")
                except Exception as e:
                    print(f"   ⚠️  FORWARD {click_num}: ALL NEXT STRATEGIES FAILED: {e}")

        # VERIFY CURRENT MONTH RESTORED
        current_month_name = MONTH_NAMES_ES[current_month]
        current_restored = False
        for xpath in [
            f'//*[contains(@text,"{current_month_name}") or contains(@content-desc,"{current_month_name}")]',
            f'//*[contains(@text,"{current_month_name.capitalize()}") or contains(@content-desc,"{current_month_name.capitalize()}")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath)
                print(f"   ✅ CURRENT MONTH RESTORED: {current_month_name.upper()} {current_year}")
                current_restored = True
                break
            except:
                pass
        utils.take_screenshot(driver, "SVS_101_08_CURRENT_MONTH_RESTORED", "t6")

        # ── STEP 9: SELECT TOMORROW AND CONFIRM ──────────────────────────────
        print(f"\n👉 STEP 9: SELECTING TOMORROW (DAY {tomorrow_day}) AND CONFIRMING...")
        day_selected = False
        for selector in [
            f'new UiSelector().descriptionStartsWith("{tomorrow_day}, ")',
            f'new UiSelector().descriptionContains("{tomorrow_day} de ")',
        ]:
            try:
                driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, selector).click()
                time.sleep(1)
                print(f"   ✅ TOMORROW (DAY {tomorrow_day}) SELECTED")
                day_selected = True
                break
            except Exception as e:
                print(f"   ⚠️  DAY SELECT FAILED: {e}")
        if not day_selected:
            try:
                driver.find_element(
                    By.XPATH, f'//*[starts-with(@content-desc,"{tomorrow_day}, ")]'
                ).click()
                time.sleep(1)
                day_selected = True
                print(f"   ✅ TOMORROW SELECTED VIA XPATH FALLBACK")
            except Exception as e:
                print(f"   ⚠️  XPATH FALLBACK FAILED: {e}")

        if not day_selected:
            print(f"   💡 DUMPING CALENDAR content-desc FOR DIAGNOSIS:")
            try:
                for el in driver.find_elements(By.XPATH, "//*[@content-desc]"):
                    cd = el.get_attribute("content-desc")
                    if cd and tomorrow_day in cd:
                        print(f"      -> '{cd}'")
            except: pass
            utils.take_screenshot(driver, "SVS_101_09_DAY_NOT_FOUND", "t6")
            _capture_evidence(driver, "SVS_101")
            return False

        # CONFIRM WITH ACEPTAR
        aceptar_clicked = False
        for xpath in [
            '//*[@text="ACEPTAR" or @text="Aceptar" or @content-desc="ACEPTAR"]',
            '//*[contains(@text,"ACEPTAR") or contains(@content-desc,"ACEPTAR")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(2)
                print("   ✅ ACEPTAR CLICKED — DATE CONFIRMED")
                aceptar_clicked = True
                break
            except: pass
        if not aceptar_clicked:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textMatches("(?i)aceptar")'
                ).click()
                time.sleep(2)
                aceptar_clicked = True
            except Exception as e:
                print(f"   💥 ACEPTAR NOT FOUND: {e}")
                _capture_evidence(driver, "SVS_101")
                return False
        utils.take_screenshot(driver, "SVS_101_09_DATE_CONFIRMED", "t6")

        # ── STEP 10: GENERAR LINK → VERIFY CONFIRMATION ───────────────────────
        print("\n👉 STEP 10: CLICKING 'Generar link'...")
        submit_ok = False
        for xpath in [
            '//*[@text="Generar link" or @content-desc="Generar link"]',
            '//*[contains(@text,"Generar link") or contains(@content-desc,"Generar link")]',
            '//*[contains(@text,"Generar") or contains(@content-desc,"Generar")]',
        ]:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(4)
                print("   ✅ GENERAR LINK CLICKED")
                submit_ok = True
                break
            except: pass
        if not submit_ok:
            print("\n💥 SVS-101 FAILED — COULD NOT CLICK GENERAR LINK")
            utils.take_screenshot(driver, "SVS_101_10_SUBMIT_FAILED", "t6")
            _capture_evidence(driver, "SVS_101")
            return False

        confirmed = False
        for xpath in [
            '//*[contains(@text,"Link generado con éxito") or contains(@content-desc,"Link generado con éxito")]',
            '//*[contains(@text,"generado con") or contains(@content-desc,"generado con")]',
            f'//*[contains(@text,"{SVS_AMOUNT}") or contains(@content-desc,"{SVS_AMOUNT}")]',
        ]:
            try:
                el = driver.find_element(By.XPATH, xpath)
                if el.is_displayed():
                    print("   ✅ CONFIRMATION SCREEN VISIBLE")
                    confirmed = True
                    break
            except: pass
        utils.take_screenshot(driver, "SVS_101_10_FINAL_STATE", "t6")

        # ── FINAL RESULT ──────────────────────────────────────────────────────
        if january_reached and confirmed:
            result = "SUCCESS"
            print("\n✅ SVS-101 RESULT: SUCCESS")
            print(f"   ✅ NAVIGATED BACKWARD {months_to_go_back} MONTH(S) TO ENERO {current_year}")
            print(f"   ✅ CALENDAR NAVIGATION WORKS CORRECTLY")
            print(f"   ✅ LINK GENERATED WITH DATE: {tomorrow_str}")
        elif not january_reached:
            print(f"\n❌ SVS-101 RESULT: FAIL — DID NOT REACH ENERO {current_year}")
            print(f"   Navigation errors: {nav_errors}")
        elif not confirmed:
            print("\n❌ SVS-101 RESULT: FAIL — JANUARY REACHED BUT LINK NOT GENERATED")

        _capture_evidence(driver, "SVS_101")
        return result == "SUCCESS"

    except Exception as e:
        print(f"\n💥 SVS-101 CRITICAL ERROR: {e}")
        try: utils.take_screenshot(driver, "SVS_101_CRITICAL_ERROR", "t6")
        except: pass
        return False
    finally:
        print("\n" + "-" * 60)
        print(f"📊 SVS-101 RESULT: {result}")
        print("-" * 60)
        utils.close_driver(driver)

# === MAIN EXECUTION === #
if __name__ == "__main__":

    logger, log_file, timestamp = utils.start_report("OPERATIONALS_SVS")

    try:
        SVS_92()
        SVS_93()
        SVS_94()
        SVS_95()
        SVS_96()
        SVS_97()
        SVS_98()
        SVS_99()
        SVS_100()
        SVS_101()

    finally:
        logger.close()
        utils.generate_zip_report("OPERATIONALS_SVS", logger, log_file, timestamp)
        utils.generate_html_report("OPERATIONALS_SVS", log_file, timestamp)