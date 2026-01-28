"""
FILENAME: config.py
DESCRIPTION:
    Global configuration hub for the POS automation project.
    Stores constants reusable across multiple test scripts to ensure modularity.

CONTENTS:
    - Appium Capabilities (T6 Device Configuration).
    - Test Credentials (QA Users & Passwords).
    - Selector Repository (Centralized XPaths).

USAGE:
    import config
    driver.find_element(By.XPATH, config.XPATH_INPUT_USER)
"""

# === SETTINGS === #
URL_APPIUM = 'http://localhost:4723'

CAPABILITIES = {
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:platformVersion": "13",
    "appium:deviceName": "vnd_tb8766p1_64_bsp",
    "appium:appPackage": "mx.memphis_beta.comercios",
    "appium:appActivity": "mx.memphis_beta.comercios/.MainActivity",
    "appium:autoGrantPermissions": False,
    "appium:noReset": False
}

# === DATA === #
USUARIO_VALIDO = "david.santos@ijuba.solutions"
PASS_VALIDO = "Memphis@2021"

USUARIO_INVALIDO = "usuario.noexiste@prueba.com"
PASS_INVALIDO = "ContrasenaFalsa123"

# === SELECTORS === #
XPATH_INPUT_USUARIO = '//android.widget.FrameLayout[@resource-id="android:id/content"]//android.widget.EditText[1]'
XPATH_INPUT_PASS = '//android.widget.FrameLayout[@resource-id="android:id/content"]//android.widget.EditText[2]'
XPATH_BTN_ACEPTAR = '//android.widget.Button[@content-desc="Aceptar"]'

# === IMPROVED ERROR SELECTOR === #
XPATH_ERROR_GENERICO = (
    '//*['
    'contains(@content-desc, "Aviso") or contains(@text, "Aviso") or '
    'contains(@content-desc, "incorrect") or contains(@text, "incorrect") or '
    'contains(@content-desc, "encontrado") or contains(@text, "encontrado") or '
    'contains(@content-desc, "Error") or contains(@text, "Error") or '
    'contains(@resource-id, "message") or '  # Busca IDs de mensajes del sistema
    'name()="android.widget.Toast"'          # Busca mensajes Toast (burbujas grises)
    ']'
)