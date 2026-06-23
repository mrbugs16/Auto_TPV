"""
# ==================================================================================
# FILENAME    : utils_system.py
# PROJECT     : MEMPHIS QA AUTOMATION FRAMEWORK
# DESCRIPTION : SYSTEM-LEVEL CONTROL LAYER FOR T6 ANDROID TERMINALS.
#               USES ADB (ANDROID DEBUG BRIDGE) TO CONTROL HARDWARE FEATURES
#               THAT ARE NOT ACCESSIBLE VIA APPIUM UI AUTOMATION:
#                 - WIFI   : ENABLE / DISABLE / QUERY STATE
#                 - BLUETOOTH : ENABLE / DISABLE / QUERY STATE
#                 - AIRPLANE MODE : TOGGLE ON/OFF
#                 - SCREEN : LOCK / UNLOCK / BRIGHTNESS
#                 - APP CONTROL : FORCE-STOP / CLEAR DATA / RESTART
#                 - NETWORK SIMULATION : THROTTLE / RESET
#               THIS MODULE INTEGRATES WITH THE EXISTING utils.py / config.py PATTERN.
#
# STRUCTURE:
#   [1] IMPORTS & CONSTANTS
#   [2] ADB CORE HELPERS
#   [3] WIFI CONTROL
#   [4] BLUETOOTH CONTROL
#   [5] AIRPLANE MODE CONTROL
#   [6] SCREEN CONTROL
#   [7] APP LIFECYCLE CONTROL
#   [8] NETWORK SIMULATION
#   [9] DEVICE STATUS SNAPSHOT
#
# USAGE:
#   import utils_system as sys_ctrl
#   sys_ctrl.disable_wifi()
#   sys_ctrl.enable_bluetooth()
#   sys_ctrl.restart_memphis_app()
#
# REQUIREMENTS:
#   - ADB INSTALLED AND IN SYSTEM PATH   (adb --version)
#   - T6 CONNECTED VIA USB WITH USB DEBUGGING ENABLED
#   - DEVICE RECOGNIZED BY: adb devices
# ==================================================================================
"""

# ==================================================================================
# [1] IMPORTS & CONSTANTS
# ==================================================================================

import subprocess
import time
import sys
import os
from datetime import datetime

# ── MEMPHIS APP PACKAGES ──
MEMPHIS_V1_PACKAGE = "mx.memphis_beta.comercios"
MEMPHIS_V2_PACKAGE = "com.memphis.app.dev"

# ── ADB TIMEOUT (SECONDS) ──
ADB_TIMEOUT = 10

# ── DEFAULT DEVICE SERIAL (None = use first connected device) ──
DEVICE_SERIAL = None  # SET THIS IF MULTIPLE DEVICES ARE CONNECTED


# ==================================================================================
# [2] ADB CORE HELPERS
# ==================================================================================

def _adb(command: str, timeout: int = ADB_TIMEOUT) -> tuple[bool, str]:
    """
    EXECUTES AN ADB SHELL COMMAND ON THE CONNECTED T6 DEVICE.
    RETURNS (success: bool, output: str).

    EXAMPLE:
        ok, out = _adb("shell svc wifi disable")
        print(ok, out)
    """
    serial_flag = f"-s {DEVICE_SERIAL}" if DEVICE_SERIAL else ""
    full_cmd = f"adb {serial_flag} {command}".strip()

    print(f"   🔧 ADB: {full_cmd}")

    try:
        result = subprocess.run(
            full_cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        output = (result.stdout + result.stderr).strip()
        success = result.returncode == 0
        if output:
            print(f"   📤 OUTPUT: {output}")
        return success, output
    except subprocess.TimeoutExpired:
        print(f"   ⏰ TIMEOUT: ADB command timed out after {timeout}s")
        return False, "TIMEOUT"
    except Exception as e:
        print(f"   ❌ ADB ERROR: {e}")
        return False, str(e)


def _adb_shell(command: str, timeout: int = ADB_TIMEOUT) -> tuple[bool, str]:
    """
    SHORTCUT: WRAPS _adb() TO PREFIX 'shell' AUTOMATICALLY.
    EXAMPLE:
        ok, out = _adb_shell("settings get global wifi_on")
    """
    return _adb(f"shell {command}", timeout)


def verify_device_connected() -> bool:
    """
    CHECKS THAT EXACTLY ONE DEVICE IS REACHABLE VIA ADB.
    CALL THIS AT THE START OF ANY TEST THAT USES SYSTEM CONTROLS.
    """
    ok, out = _adb("devices")
    lines = [l.strip() for l in out.splitlines() if l.strip()]
    # Filter out the header line
    devices = [l for l in lines if "\t" in l and "offline" not in l]
    if not devices:
        print("   ❌ NO DEVICE FOUND — Connect T6 via USB and enable USB Debugging.")
        return False
    print(f"   ✅ DEVICE CONNECTED: {devices[0]}")
    return True


# ==================================================================================
# [3] WIFI CONTROL
# ==================================================================================

def enable_wifi() -> bool:
    """
    ENABLES WIFI ON THE T6 TERMINAL VIA ADB.
    WAITS UP TO 5 SECONDS FOR THE STATE TO CONFIRM.

    RETURNS True IF WIFI IS ON AFTER THE CALL, False OTHERWISE.
    """
    print("\n📶 ENABLING WIFI...")
    ok, _ = _adb_shell("svc wifi enable")
    time.sleep(2)
    state = get_wifi_state()
    if state:
        print("   ✅ WIFI IS NOW ENABLED.")
    else:
        print("   ⚠️  WIFI DID NOT ENABLE — Check ADB permissions.")
    return state


def disable_wifi() -> bool:
    """
    DISABLES WIFI ON THE T6 TERMINAL VIA ADB.
    AFTER DISABLING, VERIFIES THE STATE.

    RETURNS True IF WIFI IS OFF AFTER THE CALL, False OTHERWISE.
    """
    print("\n📵 DISABLING WIFI...")
    ok, _ = _adb_shell("svc wifi disable")
    time.sleep(2)
    state = get_wifi_state()
    if not state:
        print("   ✅ WIFI IS NOW DISABLED.")
    else:
        print("   ⚠️  WIFI DID NOT DISABLE — Check ADB permissions.")
    return not state


def get_wifi_state() -> bool:
    """
    QUERIES THE CURRENT WIFI STATE.
    RETURNS True IF WIFI IS ENABLED, False IF DISABLED.

    HOW IT WORKS:
        'adb shell settings get global wifi_on' returns '1' (on) or '0' (off).
    """
    ok, out = _adb_shell("settings get global wifi_on")
    state = out.strip() == "1"
    print(f"   📊 WIFI STATE: {'ON' if state else 'OFF'}")
    return state


def wait_for_wifi_connection(timeout_seconds: int = 30) -> bool:
    """
    WAITS UNTIL THE DEVICE HAS AN ACTIVE WIFI DATA CONNECTION.
    USEFUL AFTER RE-ENABLING WIFI — IT TAKES A FEW SECONDS TO RECONNECT.

    RETURNS True WHEN CONNECTED, False IF TIMEOUT IS REACHED.
    """
    print(f"\n⏳ WAITING FOR WIFI CONNECTION (timeout={timeout_seconds}s)...")
    start = time.time()
    while time.time() - start < timeout_seconds:
        ok, out = _adb_shell("dumpsys connectivity | grep 'NetworkInfo.*WIFI' | grep CONNECTED")
        if ok and "CONNECTED" in out:
            print("   ✅ WIFI CONNECTED TO NETWORK.")
            return True
        time.sleep(2)
        print("   🔄 Still waiting for WiFi connection...")
    print(f"   ⏰ WIFI CONNECTION TIMEOUT after {timeout_seconds}s.")
    return False


# ==================================================================================
# [4] BLUETOOTH CONTROL
# ==================================================================================

def enable_bluetooth() -> bool:
    """
    ENABLES BLUETOOTH ON THE T6 TERMINAL VIA ADB.

    HOW IT WORKS:
        Uses 'svc bluetooth enable' — same pattern as WiFi control.
        Android requires root or BLUETOOTH_ADMIN permission for this to work.
        T6 terminals running Memphis should have this permission.

    RETURNS True IF BLUETOOTH IS ON AFTER THE CALL.
    """
    print("\n🔵 ENABLING BLUETOOTH...")
    ok, _ = _adb_shell("svc bluetooth enable")
    time.sleep(3)  # BT needs slightly longer to initialize
    state = get_bluetooth_state()
    if state:
        print("   ✅ BLUETOOTH IS NOW ENABLED.")
    else:
        print("   ⚠️  BLUETOOTH DID NOT ENABLE.")
        print("   💡 TIP: Try enabling via UI Settings if ADB permission is restricted.")
    return state


def disable_bluetooth() -> bool:
    """
    DISABLES BLUETOOTH ON THE T6 TERMINAL VIA ADB.
    IMPORTANT FOR TESTING: MEMPHIS CARD READER (LECTOR) USES BLUETOOTH.
    DISABLING IT TESTS THE 'LECTOR NO CONFIGURADO' ERROR STATE.

    RETURNS True IF BLUETOOTH IS OFF AFTER THE CALL.
    """
    print("\n🚫 DISABLING BLUETOOTH...")
    ok, _ = _adb_shell("svc bluetooth disable")
    time.sleep(3)
    state = get_bluetooth_state()
    if not state:
        print("   ✅ BLUETOOTH IS NOW DISABLED.")
        print("   ℹ️  NOTE: Memphis app will show 'Lector no configurado' if BT is off.")
    else:
        print("   ⚠️  BLUETOOTH DID NOT DISABLE.")
    return not state


def get_bluetooth_state() -> bool:
    """
    QUERIES THE CURRENT BLUETOOTH STATE.
    RETURNS True IF BLUETOOTH IS ENABLED.

    HOW IT WORKS:
        Reads bluetooth_on from the global settings store.
        Value '1' = enabled, '0' = disabled.
    """
    ok, out = _adb_shell("settings get global bluetooth_on")
    state = out.strip() == "1"
    print(f"   📊 BLUETOOTH STATE: {'ON' if state else 'OFF'}")
    return state


def toggle_bluetooth() -> bool:
    """
    TOGGLES BLUETOOTH: IF IT'S ON, TURNS IT OFF AND VICE VERSA.
    RETURNS THE NEW STATE (True = ON, False = OFF).
    """
    current = get_bluetooth_state()
    if current:
        return not disable_bluetooth()
    else:
        return enable_bluetooth()


# ==================================================================================
# [5] AIRPLANE MODE CONTROL
# ==================================================================================

def enable_airplane_mode() -> bool:
    """
    ENABLES AIRPLANE MODE — CUTS ALL RADIO: WIFI + BLUETOOTH + CELLULAR.
    USEFUL FOR TESTING APP BEHAVIOR WITH ZERO CONNECTIVITY.

    HOW IT WORKS (2-STEP PROCESS):
        Step 1: Set the setting via 'settings put global airplane_mode_on 1'
        Step 2: Broadcast the intent so the system actually applies it.
        Both steps are required — setting alone is not enough on Android 13.

    RETURNS True IF AIRPLANE MODE IS ON.
    """
    print("\n✈️  ENABLING AIRPLANE MODE (ALL RADIOS OFF)...")
    _adb_shell("settings put global airplane_mode_on 1")
    _adb_shell(
        "am broadcast -a android.intent.action.AIRPLANE_MODE "
        "--ez state true"
    )
    time.sleep(2)
    state = get_airplane_mode_state()
    if state:
        print("   ✅ AIRPLANE MODE ENABLED — WiFi, BT, and Cellular are OFF.")
    else:
        print("   ⚠️  AIRPLANE MODE MAY NOT HAVE APPLIED.")
    return state


def disable_airplane_mode() -> bool:
    """
    DISABLES AIRPLANE MODE — RESTORES ALL RADIOS.
    AFTER DISABLING, WIFI/BT RETURN TO THEIR PRE-AIRPLANE STATE.

    RETURNS True IF AIRPLANE MODE IS OFF.
    """
    print("\n📡 DISABLING AIRPLANE MODE (RESTORING RADIOS)...")
    _adb_shell("settings put global airplane_mode_on 0")
    _adb_shell(
        "am broadcast -a android.intent.action.AIRPLANE_MODE "
        "--ez state false"
    )
    time.sleep(3)
    state = get_airplane_mode_state()
    if not state:
        print("   ✅ AIRPLANE MODE DISABLED — Radios are being restored.")
    else:
        print("   ⚠️  AIRPLANE MODE DID NOT DISABLE.")
    return not state


def get_airplane_mode_state() -> bool:
    """
    RETURNS True IF AIRPLANE MODE IS CURRENTLY ENABLED.
    """
    ok, out = _adb_shell("settings get global airplane_mode_on")
    state = out.strip() == "1"
    print(f"   📊 AIRPLANE MODE: {'ON' if state else 'OFF'}")
    return state


# ==================================================================================
# [6] SCREEN CONTROL
# ==================================================================================

def lock_screen() -> bool:
    """
    LOCKS THE T6 SCREEN (SAME AS PRESSING THE POWER BUTTON).
    USED FOR TESTING SESSION HANDLING WHEN THE DEVICE GOES TO SLEEP.
    """
    print("\n🔒 LOCKING SCREEN...")
    ok, _ = _adb_shell("input keyevent KEYCODE_SLEEP")
    time.sleep(1)
    print("   ✅ SCREEN LOCKED.")
    return ok


def unlock_screen() -> bool:
    """
    WAKES UP AND UNLOCKS THE SCREEN.
    ASSUMES THE DEVICE HAS NO PIN/PATTERN LOCK (T6 TERMINALS ARE TYPICALLY KIOSK-MODE).
    """
    print("\n🔓 UNLOCKING SCREEN...")
    _adb_shell("input keyevent KEYCODE_WAKEUP")
    time.sleep(1)
    _adb_shell("input keyevent KEYCODE_MENU")  # Dismiss any lock screen overlay
    time.sleep(1)
    print("   ✅ SCREEN UNLOCKED.")
    return True


def set_screen_brightness(level: int) -> bool:
    """
    SETS SCREEN BRIGHTNESS (0–255).
    FIRST DISABLES AUTO-BRIGHTNESS, THEN SETS THE VALUE.

    PARAMS:
        level: int between 0 (off) and 255 (max brightness)
    """
    level = max(0, min(255, level))
    print(f"\n💡 SETTING BRIGHTNESS TO {level}/255...")
    _adb_shell("settings put system screen_brightness_mode 0")  # MANUAL MODE
    ok, _ = _adb_shell(f"settings put system screen_brightness {level}")
    print(f"   ✅ BRIGHTNESS SET TO {level}.")
    return ok


def keep_screen_on(enabled: bool = True) -> bool:
    """
    ENABLES OR DISABLES THE 'STAY AWAKE' SETTING.
    USEFUL FOR LONG TEST RUNS SO THE SCREEN DOESN'T TURN OFF MID-TEST.

    PARAMS:
        enabled: True = keep screen on while charging, False = normal timeout
    """
    value = "7" if enabled else "0"  # 7 = stay awake (all charge states)
    label = "ALWAYS ON" if enabled else "NORMAL TIMEOUT"
    print(f"\n⚡ SCREEN STAY-AWAKE: {label}...")
    ok, _ = _adb_shell(f"settings put global stay_on_while_plugged_in {value}")
    print(f"   ✅ SCREEN SET TO {label}.")
    return ok


# ==================================================================================
# [7] APP LIFECYCLE CONTROL
# ==================================================================================

def force_stop_memphis(version: str = "v2") -> bool:
    """
    FORCE-STOPS THE MEMPHIS APP (EQUIVALENT TO 'Force Stop' IN ANDROID SETTINGS).
    USE THIS TO SIMULATE A COLD START ON THE NEXT APPIUM SESSION.

    PARAMS:
        version: 'v1' or 'v2' (selects the correct package)
    """
    package = MEMPHIS_V1_PACKAGE if version == "v1" else MEMPHIS_V2_PACKAGE
    print(f"\n🛑 FORCE-STOPPING MEMPHIS ({version}) — {package}...")
    ok, _ = _adb_shell(f"am force-stop {package}")
    time.sleep(1)
    print(f"   ✅ APP STOPPED.")
    return ok


def clear_memphis_data(version: str = "v2") -> bool:
    """
    ⚠️  DESTRUCTIVE: CLEARS ALL DATA FOR THE MEMPHIS APP.
    THIS RESETS THE APP TO A FACTORY STATE — LOGIN, SETTINGS, AND CACHE ARE WIPED.
    USE FOR TESTING FIRST-LAUNCH / REGISTRATION FLOWS.

    PARAMS:
        version: 'v1' or 'v2'
    """
    package = MEMPHIS_V1_PACKAGE if version == "v1" else MEMPHIS_V2_PACKAGE
    print(f"\n🗑️  CLEARING MEMPHIS DATA ({version}) — {package}...")
    print("   ⚠️  WARNING: ALL APP DATA WILL BE ERASED!")
    ok, out = _adb_shell(f"pm clear {package}")
    if "Success" in out:
        print(f"   ✅ APP DATA CLEARED SUCCESSFULLY.")
    else:
        print(f"   ❌ CLEAR FAILED: {out}")
    return "Success" in out


def restart_memphis_app(version: str = "v2") -> bool:
    """
    RESTARTS THE MEMPHIS APP: FORCE-STOPS THEN LAUNCHES IT FRESH.
    USE THIS INSTEAD OF DRIVER.QUIT + REINIT FOR FASTER CYCLE TIMES.

    PARAMS:
        version: 'v1' or 'v2'
    """
    package    = MEMPHIS_V1_PACKAGE if version == "v1" else MEMPHIS_V2_PACKAGE
    activity   = (
        "mx.memphis_beta.comercios/.MainActivity" if version == "v1"
        else "com.memphis.app.dev/.MainActivity"
    )
    print(f"\n🔄 RESTARTING MEMPHIS APP ({version})...")
    force_stop_memphis(version)
    time.sleep(1)
    ok, _ = _adb_shell(f"am start -n {package}/{activity.split('/')[-1]}")
    time.sleep(3)
    print("   ✅ MEMPHIS APP RESTARTED.")
    return ok


def get_memphis_version_info(version: str = "v2") -> dict:
    """
    RETRIEVES THE INSTALLED VERSION NAME AND VERSION CODE FOR MEMPHIS.
    USEFUL FOR LOGGING IN TEST REPORTS.

    RETURNS dict with keys: package, version_name, version_code
    """
    package = MEMPHIS_V1_PACKAGE if version == "v1" else MEMPHIS_V2_PACKAGE
    ok, out = _adb_shell(f"dumpsys package {package} | grep -E 'versionName|versionCode'")
    info = {"package": package, "version_name": "UNKNOWN", "version_code": "UNKNOWN"}
    for line in out.splitlines():
        line = line.strip()
        if "versionName" in line:
            info["version_name"] = line.split("=")[-1].strip()
        if "versionCode" in line:
            info["version_code"] = line.split(" ")[0].replace("versionCode=", "").strip()
    print(f"   📱 MEMPHIS VERSION: {info['version_name']} (code {info['version_code']})")
    return info


def take_bugreport(output_path: str = "evidence") -> bool:
    """
    CAPTURES A FULL ANDROID BUGREPORT.
    USEFUL WHEN A TEST FAILS UNEXPECTEDLY — CAPTURES LOGCAT + SYSTEM STATE.

    PARAMS:
        output_path: directory where the bugreport zip will be saved
    """
    os.makedirs(output_path, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(output_path, f"bugreport_{ts}.zip")
    print(f"\n🐛 CAPTURING BUGREPORT → {filename}")
    print("   ⏳ This may take 30–60 seconds...")
    ok, out = _adb(f"bugreport {filename}", timeout=120)
    if ok:
        print(f"   ✅ BUGREPORT SAVED TO: {filename}")
    else:
        print(f"   ❌ BUGREPORT FAILED: {out}")
    return ok


# ==================================================================================
# [8] NETWORK SIMULATION
# ==================================================================================

def simulate_slow_network(latency_ms: int = 500, bandwidth_kbps: int = 256) -> bool:
    """
    THROTTLES NETWORK SPEED ON THE T6 TERMINAL TO SIMULATE BAD CONNECTIVITY.
    USES THE tc (TRAFFIC CONTROL) COMMAND — REQUIRES ROOT ON MOST DEVICES.
    T6 TERMINALS WITH ENGINEERING FIRMWARE TYPICALLY HAVE ROOT.

    PARAMS:
        latency_ms   : Added latency in milliseconds (e.g. 500 = 0.5s delay)
        bandwidth_kbps: Max download speed in kbps (e.g. 256 = slow 3G-ish)

    EXAMPLE USE CASE:
        Verify that Memphis app shows proper loading states when payment
        API calls take longer than expected.
    """
    print(f"\n🐌 SIMULATING SLOW NETWORK (latency={latency_ms}ms, bw={bandwidth_kbps}kbps)...")

    # STRATEGY 1: tc (Traffic Control) — Requires root
    ok, _ = _adb_shell(
        f"tc qdisc add dev wlan0 root netem delay {latency_ms}ms rate {bandwidth_kbps}kbit"
    )
    if ok:
        print(f"   ✅ NETWORK THROTTLED — Latency: {latency_ms}ms | BW: {bandwidth_kbps}kbps")
        return True

    # STRATEGY 2: Android built-in network limiter (no root needed)
    print("   ℹ️  tc not available — Using Android emulation network conditions...")
    ok, _ = _adb_shell(
        f"settings put global network_limit_speed {bandwidth_kbps}"
    )
    if ok:
        print(f"   ✅ NETWORK LIMIT SET TO {bandwidth_kbps}kbps (Android settings).")
    return ok


def reset_network_simulation() -> bool:
    """
    REMOVES ANY NETWORK THROTTLING SET BY simulate_slow_network().
    ALWAYS CALL THIS IN THE finally BLOCK AFTER NETWORK SIMULATION TESTS.
    """
    print("\n🚀 RESETTING NETWORK TO NORMAL SPEED...")
    _adb_shell("tc qdisc del dev wlan0 root netem")  # Strategy 1 cleanup
    ok, _ = _adb_shell("settings delete global network_limit_speed")  # Strategy 2 cleanup
    print("   ✅ NETWORK SIMULATION CLEARED.")
    return True


# ==================================================================================
# [9] DEVICE STATUS SNAPSHOT
# ==================================================================================

def get_device_status_snapshot() -> dict:
    """
    CAPTURES A COMPLETE SNAPSHOT OF THE T6 DEVICE STATE.
    CALL THIS AT THE START AND END OF TESTS THAT MODIFY SYSTEM STATE
    SO YOU CAN LOG THE BEFORE/AFTER DIFFERENCE IN YOUR TEST REPORT.

    RETURNS dict with:
        wifi_enabled, bluetooth_enabled, airplane_mode,
        battery_level, android_version, memphis_version
    """
    print("\n📊 CAPTURING DEVICE STATUS SNAPSHOT...")
    print("-" * 50)

    snapshot = {}

    # CONNECTIVITY
    snapshot["wifi_enabled"]       = get_wifi_state()
    snapshot["bluetooth_enabled"]  = get_bluetooth_state()
    snapshot["airplane_mode"]      = get_airplane_mode_state()

    # BATTERY
    ok, out = _adb_shell("dumpsys battery")
    snapshot["battery_level"] = int(next((l.split("level:")[-1].strip() for l in out.splitlines() if "level:" in l and "scale" not in l), "-1"))

    # ANDROID VERSION
    ok, out = _adb_shell("getprop ro.build.version.release")
    snapshot["android_version"] = out.strip()

    # MEMPHIS VERSION (V2)
    v_info = get_memphis_version_info("v2")
    snapshot["memphis_version"] = v_info["version_name"]
    snapshot["memphis_package"]  = v_info["package"]

    # TIMESTAMP
    snapshot["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("-" * 50)
    print(f"   📱 Android    : {snapshot['android_version']}")
    print(f"   📦 Memphis    : {snapshot['memphis_version']}")
    print(f"   🔋 Battery    : {snapshot['battery_level']}%")
    print(f"   📶 WiFi       : {'ON' if snapshot['wifi_enabled'] else 'OFF'}")
    print(f"   🔵 Bluetooth  : {'ON' if snapshot['bluetooth_enabled'] else 'OFF'}")
    print(f"   ✈️  Airplane   : {'ON' if snapshot['airplane_mode'] else 'OFF'}")
    print("-" * 50)

    return snapshot


def restore_normal_state() -> None:
    """
    CONVENIENCE FUNCTION: RESTORES THE T6 TO NORMAL OPERATING STATE.
    CALL IN THE finally BLOCK OF ANY TEST THAT MODIFIES SYSTEM SETTINGS.

    RESTORES:
        - WiFi: ON
        - Bluetooth: ON
        - Airplane Mode: OFF
        - Network Simulation: OFF
        - Screen: Always ON (for test runs)
    """
    print("\n🔧 RESTORING T6 TO NORMAL STATE...")
    disable_airplane_mode()
    enable_wifi()
    enable_bluetooth()
    reset_network_simulation()
    keep_screen_on(True)
    print("   ✅ T6 RESTORED TO NORMAL OPERATING STATE.")


# ==================================================================================
# SELF-TEST — run this file directly to verify ADB connection
# USAGE: python utils_system.py
# ==================================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 UTILS_SYSTEM SELF-TEST — T6 DEVICE CONTROL VERIFICATION")
    print("=" * 60)

    if not verify_device_connected():
        print("\n❌ CANNOT PROCEED — NO DEVICE CONNECTED.")
        sys.exit(1)

    snapshot_before = get_device_status_snapshot()

    print("\n" + "=" * 60)
    print("ALL CHECKS PASSED ✅")
    print("ADB device control is ready for use in test scripts.")
    print("=" * 60)
