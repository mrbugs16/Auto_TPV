"""
FILENAME: config.py
DESCRIPTION:
    Global configuration hub for the POS automation project.
    Stores constants reusable across multiple test scripts to ensure modularity.

CONTENTS:
    - Appium Capabilities (T6 Device Configuration).
    - Test Credentials (QA Users & Passwords).
    - Selector Repository (Centralized XPaths).
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

# === WEB CONFIGURATION === #
URL_MEMPHIS_WEB = "https://fat.memphis.mx/v2/login"
XPATH_WEB_USER = '//input[@type="email" or @type="text"]'  
XPATH_WEB_PASS = '//input[@type="password"]'
XPATH_WEB_WRONG_USER = '//input[@type="email" or @type="text"]'  
XPATH_WEB_WRONG_PASS = '//input[@type="password"]'
XPATH_WEB_BTN_LOGIN = '//button[contains(text(), "Inicia") or contains(text(), "Login")]'
# === DATA WEB === #
WEB_USUARIO_PRUEBA = "eamartin"
WEB_PASS_PRUEBA = "Patito4."
WEB_WRONGUSER = "usuariofake"
WEB_WRONGPASS = "contrasenafake"

# === DATA T6 === #
USUARIO_VALIDO = "david.santos@ijuba.solutions"
PASS_VALIDO = "Memphis@2021"
USUARIO_INVALIDO = "usuario.noexiste@prueba.com"
PASS_INVALIDO = "ContrasenaFalsa123"

# === OPERACIONALES_LG === #
XPATH_INPUT_USUARIO = '//android.widget.FrameLayout[@resource-id="android:id/content"]//android.widget.EditText[1]'
XPATH_INPUT_PASS = '//android.widget.FrameLayout[@resource-id="android:id/content"]//android.widget.EditText[2]'
XPATH_BTN_ACEPTAR = '//android.widget.Button[@content-desc="Aceptar"]'

# === REGISTRAAHORA_RA === #
XPATH_TXT_TOKEN_REGISTRO = '//android.widget.EditText[1]'
XPATH_TXT_NUM_AFILIACION = '//android.widget.EditText[2]'
XPATH_BTN_ACEPTAR_REGISTRO = '//*[contains(@content-desc, "Aceptar") or contains(@text, "Aceptar")]'
TOKEN_REGISTRO = "1737498440884ivb"
NUMERO_AFILIACION = "9096021"

# === IMPROVED ERROR SELECTOR === #
XPATH_ERROR_GENERICO = (
    '//*['
    'contains(@content-desc, "Aviso") or contains(@text, "Aviso") or '
    'contains(@content-desc, "incorrect") or contains(@text, "incorrect") or '
    'contains(@content-desc, "encontrado") or contains(@text, "encontrado") or '
    'contains(@content-desc, "Error") or contains(@text, "Error") or '
    'contains(@resource-id, "message") or '  
    'name()="android.widget.Toast"'
    ']'
)