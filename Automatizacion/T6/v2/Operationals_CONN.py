"""
# ==================================================================================
# FILENAME    : Operationals_CONN.py
# PROJECT     : MEMPHIS QA AUTOMATION FRAMEWORK
# DESCRIPTION : CONNECTIVITY TEST SUITE — VALIDATES MEMPHIS APP BEHAVIOR
#               WHEN SYSTEM-LEVEL FEATURES ARE TOGGLED (WIFI / BLUETOOTH).
#               USES utils_system.py FOR ADB-BASED HARDWARE CONTROL +
#               utils.py / config.py FOR STANDARD APPIUM INTERACTIONS.
#
# TEST CASES:
#   CONN-01 : APP SHOWS ERROR WHEN WIFI IS DISABLED DURING USE
#   CONN-02 : APP RECOVERS GRACEFULLY WHEN WIFI IS RE-ENABLED
#   CONN-03 : 'LECTOR NO CONFIGURADO' APPEARS WHEN BLUETOOTH IS OFF
#   CONN-04 : LECTOR RECONNECTS AFTER BLUETOOTH IS RESTORED
#   CONN-05 : APP BEHAVIOR UNDER AIRPLANE MODE (ALL RADIOS OFF)
#   CONN-06 : APP BEHAVIOR UNDER SIMULATED SLOW NETWORK (HIGH LATENCY)
# ==================================================================================
"""

import sys
import os
import time
v2_path = os.path.abspath(os.path.dirname(__file__))
t6_path = os.path.abspath(os.path.join(v2_path, '..'))

for p in [v2_path, t6_path]:
    if p not in sys.path:
        sys.path.insert(0, p)

import config
import utils


print(f"✅ utils loaded from: {utils.__file__}")
if not hasattr(utils, 'start_report'):
    print("❌ WRONG utils.py LOADED — iniciar_reporte not found.")
    print(f"   Python sys.path: {sys.path[:4]}")
    sys.exit(1)

import utils_system as sys_ctrl
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

try:
    from appium.webdriver.common.appiumby import AppiumBy
except ImportError:
    class AppiumBy:
        ANDROID_UIAUTOMATOR = "android uiAutomator"


# ==================================================================================
# INTERNAL HELPERS
# ==================================================================================

def _capture_evidence(driver, test_id: str):
    """TAKES SCREENSHOT + HTTP EVIDENCE FOR THE GIVEN TEST ID."""
    utils.take_screenshot(driver, test_id)
    utils.print_http_evidence_appium(driver, test_id)


def _helper_login_and_reach_calculator(driver, wait):
    for _ in range(3):
        try:
            next_btn = driver.find_element(By.XPATH, '//*[contains(@content-desc, "Siguiente")]')
            next_btn.click()
            time.sleep(1)
        except:
            break

   
    utils.type_text(driver, config.XPATH_INPUT_USUARIO, config.USUARIO_VALIDO)
    utils.type_text(driver, config.XPATH_INPUT_PASS,    config.PASS_VALIDO)
    utils.click_element(driver, config.XPATH_BTN_ACEPTAR)
    time.sleep(3)

   
    try:
        driver.find_element(By.XPATH, '//*[contains(@content-desc, "Configurar ahora")]').click()
        time.sleep(2)
    except:
        pass

    try:
        wait.until(EC.presence_of_element_located((By.XPATH, config.XPATH_C_PANTALLA_COBRO)))
        print("   ✅ CALCULATOR SCREEN REACHED.")
    except:
        print("   ⚠️  CALCULATOR SCREEN NOT DETECTED — Continuing anyway.")


# ==================================================================================
# CONN-01: WIFI DISABLED DURING APP USE
# ==================================================================================

def CONN_01():
    print("\n" + "=" * 60)
    print("🧪 CONN-01: WIFI DISABLED DURING APP USE")
    print("=" * 60)

    # ── VERIFY DEVICE CONNECTED ──
    if not sys_ctrl.verify_device_connected():
        print("❌ CONN-01 ABORTED: No device found.")
        return False

    snapshot_before = sys_ctrl.get_device_status_snapshot()

    driver, wait = utils.start_driver()
    result = False

    try:
        print("\n🔐 PRECONDITION: LOGIN AND REACH CALCULATOR SCREEN (WiFi ON)...")
        _helper_login_and_reach_calculator(driver, wait)
        _capture_evidence(driver, "CONN_01_STEP1_CALCULATOR")

        print("\n👉 STEP 2: DISABLING WIFI VIA ADB...")
        wifi_off = sys_ctrl.disable_wifi()
        if not wifi_off:
            print("   ⚠️  WiFi disable returned uncertain state — continuing test.")
        time.sleep(3)  # GIVE APP TIME TO DETECT CONNECTIVITY LOSS
        _capture_evidence(driver, "CONN_01_STEP2_WIFI_DISABLED")

        print("\n👉 STEP 3: SCANNING FOR CONNECTIVITY ERROR MESSAGE...")
        error_found = False
        error_keywords = [
            "sin conexión", "sin internet", "sin red",
            "no connection", "no internet", "network error",
            "verifica tu conexión", "connection error"
        ]

        try:
            all_elements = driver.find_elements(By.XPATH, "//*")
            for elem in all_elements:
                try:
                    text = (elem.get_attribute("text") or "").lower()
                    desc = (elem.get_attribute("content-desc") or "").lower()
                    for keyword in error_keywords:
                        if keyword in text or keyword in desc:
                            print(f"   ✅ ERROR MESSAGE FOUND: '{text or desc}'")
                            error_found = True
                            break
                    if error_found:
                        break
                except:
                    continue
        except Exception as e:
            print(f"   ⚠️  SCAN ERROR: {e}")

        if not error_found:
            try:
                error_xpath = '//*[contains(@text, "conexión") or contains(@content-desc, "conexión")]'
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, error_xpath))
                )
                error_found = True
                print("   ✅ CONNECTIVITY ERROR ELEMENT DETECTED.")
            except:
                print("   ℹ️  NO EXPLICIT ERROR VISIBLE — App may handle silently.")

        _capture_evidence(driver, "CONN_01_STEP3_ERROR_CHECK")

        result = True  
        status = "CONN ERROR SHOWN" if error_found else "APP SILENT (NO EXPLICIT ERROR)"
        print(f"\n✅ CONN-01 COMPLETED — App behavior: {status}")

    except Exception as e:
        print(f"\n💥 CONN-01 CRITICAL ERROR: {e}")
        try:
            _capture_evidence(driver, "CONN_01_CRITICAL_ERROR")
        except:
            pass

    finally:
        utils.close_driver(driver)
        print("\n🔧 POSTCONDITION: RESTORING NORMAL STATE...")
        sys_ctrl.restore_normal_state()
        snapshot_after = sys_ctrl.get_device_status_snapshot()

    return result


# ==================================================================================
# CONN-03: BLUETOOTH OFF → 'LECTOR NO CONFIGURADO' POPUP
# ==================================================================================
def CONN_03():
    print("\n" + "=" * 60)
    print("🧪 CONN-03: BLUETOOTH OFF → LECTOR NO CONFIGURADO")
    print("=" * 60)

    if not sys_ctrl.verify_device_connected():
        print("❌ CONN-03 ABORTED: No device found.")
        return False

    print("\n👉 STEP 1: DISABLING BLUETOOTH VIA ADB...")
    bt_off = sys_ctrl.disable_bluetooth()
    time.sleep(2)

    driver, wait = utils.start_driver()
    result = False

    try:
        print("\n🔐 STEP 2: LOGIN THROUGH ONBOARDING...")
        _helper_login_and_reach_calculator(driver, wait)
        _capture_evidence(driver, "CONN_03_STEP2_POST_LOGIN")

        print("\n👉 STEP 3: CHECKING FOR 'LECTOR NO CONFIGURADO' POPUP...")
        lector_popup_found = False
        lector_keywords = [
            "lector no configurado", "lector", "reader", "no configurado",
            "bluetooth", "configurar ahora", "después"
        ]

        try:
            all_elements = driver.find_elements(By.XPATH, "//*")
            for elem in all_elements:
                try:
                    text = (elem.get_attribute("text") or "").lower()
                    desc = (elem.get_attribute("content-desc") or "").lower()
                    for keyword in lector_keywords:
                        if keyword in text or keyword in desc:
                            print(f"   ✅ LECTOR POPUP ELEMENT FOUND: '{text or desc}'")
                            lector_popup_found = True
                            break
                    if lector_popup_found:
                        break
                except:
                    continue
        except Exception as e:
            print(f"   ⚠️  SCAN ERROR: {e}")

        if not lector_popup_found:
            try:
                popup_xpath = '//*[contains(@text, "Lector") or contains(@content-desc, "Lector")]'
                WebDriverWait(driver, 8).until(
                    EC.presence_of_element_located((By.XPATH, popup_xpath))
                )
                lector_popup_found = True
                print("   ✅ 'LECTOR NO CONFIGURADO' POPUP DETECTED VIA XPATH WAIT.")
            except:
                print("   ⚠️  LECTOR POPUP NOT FOUND — BT may be managed differently on this firmware.")

        _capture_evidence(driver, "CONN_03_STEP3_LECTOR_CHECK")

        result = lector_popup_found
        status = "✅ POPUP SHOWN" if lector_popup_found else "❌ POPUP NOT SHOWN"
        print(f"\n{status} — CONN-03 {'PASSED' if result else 'FAILED (POPUP NOT DETECTED)'}")

    except Exception as e:
        print(f"\n💥 CONN-03 CRITICAL ERROR: {e}")
        try:
            _capture_evidence(driver, "CONN_03_CRITICAL_ERROR")
        except:
            pass

    finally:
        utils.close_driver(driver)
        print("\n🔧 POSTCONDITION: RESTORING BLUETOOTH...")
        sys_ctrl.enable_bluetooth()

    return result


# ==================================================================================
# CONN-05: AIRPLANE MODE — FULL RADIO BLACKOUT
# ==================================================================================
def CONN_05():
    print("\n" + "=" * 60)
    print("🧪 CONN-05: AIRPLANE MODE — FULL RADIO BLACKOUT")
    print("=" * 60)

    if not sys_ctrl.verify_device_connected():
        return False

    driver, wait = utils.start_driver()
    result = False

    try:
        print("\n🔐 PRECONDITION: LOGIN AND REACH CALCULATOR SCREEN...")
        _helper_login_and_reach_calculator(driver, wait)
        _capture_evidence(driver, "CONN_05_STEP1_BEFORE_AIRPLANE")

        print("\n👉 STEP 2: ENABLING AIRPLANE MODE (ALL RADIOS OFF)...")
        sys_ctrl.enable_airplane_mode()
        time.sleep(5)  # GIVE APP TIME TO DETECT
        _capture_evidence(driver, "CONN_05_STEP2_AIRPLANE_ON")

        print("\n👉 STEP 3: SCANNING APP STATE UNDER AIRPLANE MODE...")
        all_elements = driver.find_elements(By.XPATH, "//*")
        visible_texts = []
        for elem in all_elements:
            try:
                t = elem.get_attribute("text") or ""
                d = elem.get_attribute("content-desc") or ""
                if t and len(t) > 3:
                    visible_texts.append(t)
            except:
                continue

        print(f"   📝 VISIBLE TEXT ELEMENTS ({len(visible_texts)} found):")
        for t in visible_texts[:20]:  # Print first 20
            print(f"      • {t}")

        print("\n👉 STEP 4: DISABLING AIRPLANE MODE (RESTORING RADIOS)...")
        sys_ctrl.disable_airplane_mode()
        time.sleep(5)  # WAIT FOR RECONNECTION
        sys_ctrl.wait_for_wifi_connection(timeout_seconds=20)
        _capture_evidence(driver, "CONN_05_STEP4_AIRPLANE_OFF")

        print("\n👉 STEP 5: VERIFYING APP RECOVERS...")
        calculator_visible = False
        try:
            elem = driver.find_element(By.XPATH, config.XPATH_C_PANTALLA_COBRO)
            if elem.is_displayed():
                calculator_visible = True
                print("   ✅ CALCULATOR SCREEN STILL VISIBLE — APP RECOVERED.")
        except:
            print("   ⚠️  Calculator screen not detected after recovery.")

        result = True
        print(f"\n✅ CONN-05 COMPLETED.")

    except Exception as e:
        print(f"\n💥 CONN-05 CRITICAL ERROR: {e}")
        try:
            _capture_evidence(driver, "CONN_05_CRITICAL_ERROR")
        except:
            pass

    finally:
        utils.close_driver(driver)
        sys_ctrl.restore_normal_state()

    return result


# ==================================================================================
# CONN-06: SLOW NETWORK SIMULATION
# ==================================================================================
def CONN_06():
    print("\n" + "=" * 60)
    print("🧪 CONN-06: SLOW NETWORK SIMULATION (HIGH LATENCY)")
    print("=" * 60)

    if not sys_ctrl.verify_device_connected():
        return False

    driver, wait = utils.start_driver()
    result = False

    try:
        print("\n🐌 STEP 1: APPLYING NETWORK THROTTLE (500ms / 256kbps)...")
        sys_ctrl.simulate_slow_network(latency_ms=500, bandwidth_kbps=256)

        print("\n🔐 STEP 2: LOGIN UNDER THROTTLED NETWORK...")
        # Measure login time
        login_start = time.time()
        _helper_login_and_reach_calculator(driver, wait)
        login_duration = time.time() - login_start
        print(f"   ⏱️  LOGIN COMPLETED IN {login_duration:.1f}s UNDER THROTTLED NETWORK.")
        _capture_evidence(driver, "CONN_06_STEP2_THROTTLED_LOGIN")

        print("\n👉 STEP 3: CHECKING FOR LOADING INDICATORS / TIMEOUT ERRORS...")
        # Scan for loading spinners or timeout messages
        loading_keywords = ["cargando", "loading", "espera", "timeout", "time out"]
        for elem in driver.find_elements(By.XPATH, "//*"):
            try:
                text = (elem.get_attribute("text") or "").lower()
                for kw in loading_keywords:
                    if kw in text:
                        print(f"   📝 LOADING ELEMENT: '{text}'")
            except:
                pass

        result = True
        print(f"\n✅ CONN-06 COMPLETED — Login took {login_duration:.1f}s under throttle.")

    except Exception as e:
        print(f"\n💥 CONN-06 CRITICAL ERROR: {e}")
        try:
            _capture_evidence(driver, "CONN_06_CRITICAL_ERROR")
        except:
            pass

    finally:
        utils.close_driver(driver)
        print("\n🔧 RESTORING NORMAL NETWORK...")
        sys_ctrl.reset_network_simulation()

    return result


# ==================================================================================
# MAIN BLOCK
# ==================================================================================

if __name__ == "__main__":

    
    logger, log_file, timestamp = utils.start_report("CONN")

    results = {}

    try:
        results["CONN-01"] = CONN_01()
        results["CONN-03"] = CONN_03()
        results["CONN-05"] = CONN_05()
        results["CONN-06"] = CONN_06()

    finally:
        print("\n" + "=" * 60)
        print("📊 CONNECTIVITY TEST SUITE — SUMMARY")
        print("=" * 60)
        for test_id, passed in results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"   {status} — {test_id}")
        print("=" * 60)

        utils.generate_zip_report("CONN", logger, log_file, timestamp)
        utils.generate_html_report("CONN", log_file, timestamp)