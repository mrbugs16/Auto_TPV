"""
FILENAME: config.py
DESCRIPTION:
    GLOBAL CONFIGURATION HUB FOR THE POS AUTOMATION PROJECT.
    STORES CONSTANTS REUSABLE ACROSS MULTIPLE TEST SCRIPTS TO ENSURE MODULARITY.

CONTENTS:
    - APPIUM CAPABILITIES (T6 DEVICE CONFIGURATION).
    - TEST CREDENTIALS (QA USERS & PASSWORDS).
    - SELECTOR REPOSITORY (CENTRALIZED XPATHS).
"""

# === DATA T6 === #
USUARIO_VALIDO = "david.santos@ijuba.solutions"
PASS_VALIDO = "Memphis@2021"
USUARIO_INVALIDO = "usuario.noexiste@prueba.com"
PASS_INVALIDO = "ContrasenaFalsa123"

# === OPERACIONALES_LG === #
XPATH_INPUT_USUARIO = '//android.widget.FrameLayout[@resource-id="android:id/content"]//android.widget.EditText[1]'
XPATH_INPUT_PASS = '//android.widget.FrameLayout[@resource-id="android:id/content"]//android.widget.EditText[2]'
XPATH_BTN_ACEPTAR = '//android.widget.Button[@content-desc="Aceptar"]'

# === XPATHS RN === #
XPATH_RN_TITULO_NEGOCIO = '//*[contains(@text, "Registro de negocio") or contains(@content-desc, "Registro de negocio")]'
RN_TOKEN = "1737498440884ivb"
RN_TOKEN_INVALIDO = "0000000000000err" 
RN_TOKEN_CORTO = "123456890" 
RN_TOKEN_LARGO = "1737498440884ivbEXTRA"
RN_AFILIACION = "9096021"
RN_AFILIACION_CORTA = "12345"
RN_AFILIACION_LARGA = "12345678"
RN_AFILIACION_INVALIDA = "9096011"


# === XPATHS RN (REGISTRO DE NEGOCIO) === #
XPATH_RN_INPUT_TOKEN = '(//android.widget.EditText)[1]'
XPATH_RN_INPUT_AFILIACION = '(//android.widget.EditText)[2]'
XPATH_RN_BTN_ACEPTAR_REGISTRO = '//android.widget.Button[contains(@text, "Aceptar") or contains(@content-desc, "Aceptar") or contains(@text, "Continuar") or contains(@content-desc, "Continuar")]'
XPATH_RN_PANTALLA_EXITO = '//*[contains(@text, "permitir") or contains(@text, "ubicaci") or contains(@text, "memphis beta")]'
XPATH_RN_MENSAJE_ERROR = '//*[contains(@text, "El token o afiliacion no son correctos o el comercio no existe") or contains(@content-desc, "El token o afiliacion no son correctos o el comercio no existe") or contains(@text, "comercio no existe")]'
XPATH_RN_BTN_OTRA_OCASION = '//*[contains(@text, "otra") or contains(@content-desc, "otra") or contains(@text, "Ocasión")]'

# === XPATHS C (CALCULADORA) === #
XPATH_C_BTN_MIENTRAS_USO = (
    '//*[contains(@text, "MIENTRAS LA APP") or contains(@content-desc, "MIENTRAS LA APP") or '
    'contains(@text, "Mientras la app") or contains(@content-desc, "Mientras la app") or '
    'contains(@text, "mientras la app") or contains(@content-desc, "mientras la app")]'
)
XPATH_C_PANTALLA_COBRO  = '//*[contains(@text, "Cobrar") or contains(@content-desc, "Cobrar")]'
XPATH_C_DISPLAY_MONTO   = '//*[contains(@text, "0.00") or contains(@content-desc, "0.00")]'
XPATH_C_DISPLAY_UPDATED  = '//*[(contains(@text, "$") and not(contains(@text, "$0.00"))) or (contains(@content-desc, "$") and not(contains(@content-desc, "$0.00")))]'
XPATH_C_DISPLAY_ZERO_LEADING  = '//*[contains(@text, "0001") or contains(@content-desc, "0001")]'
XPATH_C_POPUP_PROPINA         = '//*[contains(@text, "propina") or contains(@content-desc, "propina") or contains(@text, "Propina") or contains(@content-desc, "Propina")]'
XPATH_C_BTN_ACEPTAR_PROPINA   = '//*[contains(@text, "Aceptar") or contains(@content-desc, "Aceptar")]'
XPATH_C_PANTALLA_TARJETA      = '//*[contains(@text, "Inserta") or contains(@content-desc, "Inserta") or contains(@text, "Desliza") or contains(@content-desc, "Desliza")]'
XPATH_C_BTN_CANCELAR          = '//*[contains(@text, "Cancelar") or contains(@content-desc, "Cancelar")]'
XPATH_C_POPUP_LECTOR          = '//*[contains(@text, "lector configurado") or contains(@content-desc, "lector configurado")]'
XPATH_C_BTN_OK_POPUP          = '//*[@text="Ok" or @content-desc="Ok" or @text="OK" or @content-desc="OK"]'
XPATH_C_TAB_AJUSTES = '//*[contains(@content-desc, "Ajustes") and contains(@content-desc, "4")]'
XPATH_C_TAB_INICIO = '//*[contains(@content-desc, "Inicio") and contains(@content-desc, "1")]'
XPATH_C_BTN_CONFIGURAR_LECTOR = '//*[contains(@text, "Configurar lector") or contains(@content-desc, "Configurar lector")]'
XPATH_C_BTN_DECIMAL           = '//*[@text="+" or @content-desc="+"]'
XPATH_C_ERROR_CANTIDAD_VALIDA = '//*[contains(@text, "ingrese una cantidad") or contains(@content-desc, "ingrese una cantidad") or contains(@text, "cantidad valida") or contains(@content-desc, "cantidad valida")]'
# === XPATHS C (CALCULADORA) === #
XPATH_C_BTN_BACKSPACE    = (
    '//*[@text="\u232B" or @content-desc="\u232B" or '
    '@text="\u2190" or @content-desc="\u2190" or '
    'contains(@content-desc, "erase") or contains(@content-desc, "delete") or '
    'contains(@content-desc, "backspace") or contains(@content-desc, "borrar") or '
    'contains(@content-desc, "Borrar") or contains(@text, "borrar")]'
)

# ABSOLUTE XPATH OBTAINED FROM APPIUM INSPECTOR.
# THE BACKSPACE KEY RENDERS AS A PLAIN android.view.View WITH NO TEXT/CONTENT-DESC
# WHEN THE DISPLAY IS FULL (E.G. AFTER 8+ DIGITS ARE ENTERED). USE THIS AS LAST RESORT.
XPATH_C_BTN_BACKSPACE_ABSOLUTE = (
    '//android.widget.FrameLayout[@resource-id="android:id/content"]'
    '/android.widget.FrameLayout'
    '/android.widget.FrameLayout'
    '/android.widget.FrameLayout'
    '/android.view.View/android.view.View/android.view.View'
    '/android.view.View/android.view.View[13]'
)
XPATH_C_POPUP_AJUSTES_VERDE = '//*[contains(@text, "terminal configurada correctamente") or contains(@content-desc, "terminal configurada correctamente") or contains(@text, "Terminal configurada correctamente") or contains(@content-desc, "Terminal configurada correctamente")]'


# === XPATHS PÑ (PESTAÑAS) === #
XPATH_PÑ_TAB_INICIO = '//*[contains(@content-desc, "Inicio") and contains(@content-desc, "1")]'
XPATH_PÑ_TAB_TRANSACCIONES = '//*[contains(@content-desc, "Transacciones") and contains(@content-desc, "2")]'
XPATH_PÑ_TAB_SERVICIOS = '//*[contains(@content-desc, "Servicios") and contains(@content-desc, "3")]'
XPATH_PÑ_TAB_AJUSTES = '//*[contains(@content-desc, "Ajustes") and contains(@content-desc, "4")]'




# === DATA RA === #
RA_NOMBRE = "Antonio"
RA_APELLIDO = "Garcia"
RA_SEGUNDOAPELLIDO = "Garcia"
RA_EMAIL = "usuariofake@prueba.com"
RA_PASS = "contrasenafake"

# === DATA RA_010 === #
RA_010_NOMBRE = "Santiago"
RA_010_APELLIDO = "martinez"
RA_010_SEGUNDO_APELLIDO = "martinez"
RA_010_EMAIL = "sss@gmail.com"
RA_010_PASS = "Memphis@2030"

# === DATA RA_013 === #
RA_013_EMAIL = "david.santos@ijuba.solutions"

# === XPATHS RA === #
XPATH_RA_NOMBRE = '//android.widget.EditText[1]'
XPATH_RA_APELLIDO = '//android.widget.EditText[2]'
XPATH_RA_SEGUNDOAPELLIDO = '//android.widget.EditText[3]'
XPATH_RA_EMAIL = '//android.widget.EditText[4]'
XPATH_RA_PASS = '//android.widget.EditText[5]'
XPATH_RA_CONFIRMAR_PASS = '//android.widget.EditText[6]'
XPATH_RA_BTN_ACEPTAR = '//android.widget.Button[@content-desc="Aceptar"]'
XPATH_RA_BTN_ATRAS = '//android.widget.Button[1]'  # Usually the first button/imagebutton in the header

# === VALIDATION ERROR MESSAGES RA === #
XPATH_RA_ERROR_NOMBRE = '//*[contains(@text, "Ingresa un nombre") or contains(@content-desc, "Ingresa un nombre")]'
XPATH_RA_ERROR_USUARIO_EXISTE = (
    '//*[contains(@text, "usuario ya está registrado") or '
    'contains(@content-desc, "usuario ya está registrado") or '
    'contains(@text, "ya está registrado") or '
    'contains(@content-desc, "ya está registrado")]'
)
XPATH_RA_ERROR_PASS_NO_COINCIDEN = '//*[contains(@text, "Las contraseñas no coinciden") or contains(@content-desc, "Las contraseñas no coinciden")]'
XPATH_RA_ERROR_CORREO_INVALIDO = '//*[contains(@text, "Correo inválido") or contains(@content-desc, "Correo inválido")]'
XPATH_RA_ERROR_CONTRASENA_INVALIDA = '//*[contains(@text, "Contraseña inválida") or contains(@content-desc, "Contraseña inválida")]'

XPATH_RA_REGISTRO_EXITOSO = (
    '//*[contains(@text, "suario creado correctamente") or '
    'contains(@text, "orrectamente") or '
    'contains(@content-desc, "suario creado correctamente") or '
    '//android.widget.Toast]'
)

# === REGISTRAAHORA_RA === #
XPATH_TXT_TOKEN_REGISTRO = '//android.widget.EditText[1]'
XPATH_TXT_NUM_AFILIACION = '//android.widget.EditText[2]'
XPATH_BTN_ACEPTAR_REGISTRO = '//*[contains(@content-desc, "Aceptar") or contains(@text, "Aceptar")]'

# === XPATHS OC (FORGOT PASSWORD) === #
XPATH_OC_LNK_OLVIDASTE = '//*[contains(@text, "Olvidaste tu contraseña") or contains(@content-desc, "Olvidaste tu contraseña")]'
XPATH_OC_TITULO_RECUPERA = '//*[contains(@text, "Recupera tu contraseña") or contains(@content-desc, "Recupera tu contraseña")]'
XPATH_OC_BTN_ATRAS = '//android.widget.Button[1]'
XPATH_OC_INPUT_EMAIL = '//android.widget.EditText[1]' 
XPATH_OC_BTN_ACEPTAR = '//android.widget.Button[@content-desc="Aceptar"]'

XPATH_OC_MSJ_EXITO = '//*[contains(@text, "ceso de recuperaci") or contains(@content-desc, "ceso de recuperaci")]'
NUMERO_AFILIACION = "9096021"

# === IMPROVED ERROR SELECTOR === #
XPATH_ERROR_GENERICO = (
    '//*['
    'contains(@content-desc, "Ocurri") or contains(@text, "Ocurri") or '
    'contains(@content-desc, "un error") or contains(@text, "un error") or '
    'contains(@content-desc, "intental") or contains(@text, "intental") or '
    'contains(@content-desc, "tarde") or contains(@text, "tarde") or '
    'contains(@text, "Ocurrió un error, inténtalo más tarde")'
    'contains(translate(text(), "Correo inválido", "error"), "error")'
    '] | //android.widget.Toast'
)

XPATH_OC_ERROR_CORREO = '//*[contains(@text, "Correo inválido") or contains(@content-desc, "Correo inválido")]'


# === WEB CONFIGURATION === #
URL_MEMPHIS_WEB = "https://fat.memphis.mx/v2/login"
XPATH_WEB_USER = '//input[@type="email" or @type="text"]'  
XPATH_WEB_PASS = '//input[@type="password"]'
XPATH_WEB_WRONG_USER = '//input[@type="email" or @type="text"]'  
XPATH_WEB_WRONG_PASS = '//input[@type="password"]'
XPATH_WEB_BTN_LOGIN = '//button[contains(text(), "Inicia") or contains(text(), "Login")]'
XPATH_WEB_TXT_INGRESA_AQUI = "//*[contains(text(), 'Ingresa aquí')]"
XPATH_WEB_TITULO_OLVIDASTE = "//*[contains(text(), 'Olvidaste tu contraseña')]"
XPATH_WEB_BTN_ENVIAR = "//*[contains(text(), 'Enviar')]"
XPATH_WEB_BTN_REGISTRA_AHORA = '//android.widget.Button[@content-desc="Regístrate ahora"]'
XPATH_REGISTRA_AHORA_ALT1 = '//*[contains(@content-desc, "Regístrate")]'
XPATH_REGISTRA_AHORA_ALT2 = '//*[contains(@content-desc, "gístrate")]'

# === MENSAJES DE SISTEMA (WEB) ===
XPATH_WEB_TITULO_OLVIDASTE = "//*[contains(text(), 'Olvidaste tu contraseña')]"
XPATH_MSJ_EXITO_RCV = "//*[contains(text(), 'Se ha enviado un mail')]"

# === DATA WEB === #
WEB_USUARIO_PRUEBA = "eamartin"
WEB_PASS_PRUEBA = "Patito4."
WEB_WRONGUSER = "usuariofake"
WEB_WRONGPASS = "contrasenafake"

# === SELECTOR ON THE WEB    EMAIL ===

XPATH_EMAIL_LINK_RESET = '//a[contains(text(), "Restablecer") or contains(text(), "Recuperar") or contains(text(), "aquí")]'

# VALIDATE NEW PASSWORD SCREEN
XPATH_TITULO_NUEVA_PASS = '//*[contains(text(), "Nueva contraseña") or contains(text(), "Restablecer") or contains(text(), "Crear")]'
XPATH_INPUT_NUEVA_PASS = '//input[@type="password"]'

# === PWD ===
URL_MEMPHIS_PWD = "https://fat.memphis.mx/recovery-password"
XPATH_PWD_ACTUAL = '//input[@name="currentPassword" or @type="password"][1]'
XPATH_PWD_NUEVA = '(//input[@type="password"])[2]'
XPATH_PWD_CONFIRMAR = '(//input[@type="password"])[3]'
XPATH_PWD_BTN_ESTABLECER = '//*[contains(text(), "Establecer contraseña") or contains(text(), "Guardar")]'

# MESSAGESS ERRORS 
XPATH_PWD_ERROR_VACIO = '//*[contains(text(), "requerido") or contains(text(), "obligatorio")]'
XPATH_PWD_ERROR_INCORRECTA = '//*[contains(text(), "incorrecta")]'
XPATH_PWD_ERROR_REGLAS = '//*[contains(text(), "debe contener") or contains(text(), "caracteres")]'
XPATH_PWD_ERROR_NO_COINCIDEN = '//*[contains(text(), "no coinciden")]'

XPATH_INPUT_REPITE_PASS = '(//input[@type="password"])[2]' 
XPATH_BTN_ACEPTAR_WEB = '//*[contains(text(), "Reestablecer Contraseña")]'

XPATH_ERROR_PASS_NO_COINCIDE = "//*[contains(text(), 'Las contraseñas no coinciden')]" 
XPATH_ERROR_PASS_MAYUSCULA = "//*[contains(text(), 'Debe contener al menos una mayúscula')]"
XPATH_BTN_OJO_NUEVA_PASS = "(//span[contains(@class,'ng-star-inserted') and ./i[contains(@class,'pi-eye')]])[1]"
XPATH_BTN_OJO_CONFIRMAR = "(//i[contains(@class,'pi-eye')])[2]"
XPATH_INPUT_REPITE_PASS = '(//input[@type="password" or @type="text"])[2]'
XPATH_PWD_ERROR_REGLAS = '//*[contains(text(), "Debe contener mínimo") or contains(text(), "caracteres")]'


# === SETTINGS (GENERAL / DRIVER) === #
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