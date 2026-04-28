"""
# ==================================================================================
# FILENAME    : config.py
# PROJECT     : MEMPHIS QA AUTOMATION FRAMEWORK
# DESCRIPTION : GLOBAL CONFIGURATION HUB — SINGLE SOURCE OF TRUTH FOR ALL TEST
#               SCRIPTS. CENTRALIZES CREDENTIALS, URLS, DEVICE CAPABILITIES,
#               AND XPATH SELECTORS FOR BOTH MOBILE (T6) AND WEB PLATFORMS.
#
# STRUCTURE:
#   [1] T6 MOBILE — APPIUM & DEVICE SETTINGS
#   [2] T6 MOBILE — CREDENTIALS
#   [3] T6 MOBILE — XPATHS: LOGIN
#   [4] T6 MOBILE — XPATHS: REGISTRO DE NEGOCIO (RN)
#   [5] T6 MOBILE — XPATHS: CALCULADORA (C)
#   [6] T6 MOBILE — XPATHS: PESTAÑAS (PÑ)
#   [7] T6 MOBILE — XPATHS: REGISTRO DE AHORA (RA)
#   [8] T6 MOBILE — XPATHS: OLVIDASTE CONTRASEÑA (OC)
#   [9] T6 MOBILE — XPATHS: GENERIC ERRORS
#   [10] WEB PLATFORM — URLS & DRIVER SETTINGS
#   [11] WEB PLATFORM — CREDENTIALS
#   [12] WEB PLATFORM — XPATHS: LOGIN
#   [13] WEB PLATFORM — XPATHS: PASSWORD RECOVERY
#   [14] WEB PLATFORM — XPATHS: SYSTEM MESSAGES
#
# USAGE CONVENTION:
#   - ALL T6 CONSTANTS ARE PREFIXED WITH THEIR MODULE ABBREVIATION (RN_, C_, RA_, OC_).
#   - ALL WEB CONSTANTS ARE PREFIXED WITH XPATH_WEB_ OR WEB_.
#   - XPATHS ARE NEVER HARDCODED INSIDE TEST FILES — ALWAYS REFERENCE THIS FILE.
# ==================================================================================
"""


# ==================================================================================
# [1] T6 MOBILE — APPIUM & DEVICE SETTINGS
# ==================================================================================

URL_APPIUM = "http://localhost:4723"

CAPABILITIES = {
    "platformName"              : "Android",
    "appium:automationName"     : "UiAutomator2",
    "appium:platformVersion"    : "13",
    "appium:deviceName"         : "vnd_tb8766p1_64_bsp",
    "appium:appPackage"         : "mx.memphis_beta.comercios",
    "appium:appActivity"        : "mx.memphis_beta.comercios/.MainActivity",
    "appium:autoGrantPermissions": False,
    "appium:noReset"            : False,
}


# ==================================================================================
# [2] T6 MOBILE — CREDENTIALS
# ==================================================================================

USUARIO_VALIDO   = "david.santos@ijuba.solutions"
PASS_VALIDO      = "Memphis@2021"
USUARIO_INVALIDO = "usuario.noexiste@prueba.com"
PASS_INVALIDO    = "ContrasenaFalsa123"


# ==================================================================================
# [3] T6 MOBILE — XPATHS: LOGIN SCREEN
# ==================================================================================

XPATH_INPUT_USUARIO = (
    '//android.widget.FrameLayout[@resource-id="android:id/content"]'
    '//android.widget.EditText[1]'
)
XPATH_INPUT_PASS = (
    '//android.widget.FrameLayout[@resource-id="android:id/content"]'
    '//android.widget.EditText[2]'
)
XPATH_BTN_ACEPTAR = '//android.widget.Button[@content-desc="Aceptar"]'


# ==================================================================================
# [4] T6 MOBILE — XPATHS & DATA: REGISTRO DE NEGOCIO (RN)
# ==================================================================================

# --- SCREEN IDENTIFIERS ---
XPATH_RN_TITULO_NEGOCIO = (
    '//*[contains(@text, "Registro de negocio") or '
    'contains(@content-desc, "Registro de negocio")]'
)
XPATH_RN_PANTALLA_EXITO = (
    '//*[contains(@text, "permitir") or '
    'contains(@text, "ubicaci") or '
    'contains(@text, "memphis beta")]'
)
XPATH_RN_MENSAJE_ERROR = (
    '//*[contains(@text, "El token o afiliacion no son correctos o el comercio no existe") or '
    'contains(@content-desc, "El token o afiliacion no son correctos o el comercio no existe") or '
    'contains(@text, "comercio no existe")]'
)

# --- FORM INPUTS ---
XPATH_RN_INPUT_TOKEN     = '(//android.widget.EditText)[1]'
XPATH_RN_INPUT_AFILIACION = '(//android.widget.EditText)[2]'

# --- BUTTONS ---
XPATH_RN_BTN_ACEPTAR_REGISTRO = (
    '//android.widget.Button[contains(@text, "Aceptar") or '
    'contains(@content-desc, "Aceptar") or '
    'contains(@text, "Continuar") or '
    'contains(@content-desc, "Continuar")]'
)
XPATH_RN_BTN_OTRA_OCASION = (
    '//*[contains(@text, "otra") or '
    'contains(@content-desc, "otra") or '
    'contains(@text, "Ocasión")]'
)

# --- TEST DATA: TOKEN ---
RN_TOKEN         = "1737498440884ivb"    # VALID 16-CHAR TOKEN
RN_TOKEN_INVALIDO = "0000000000000err"   # INVALID TOKEN (WRONG CREDENTIALS)
RN_TOKEN_CORTO   = "123456890"           # SHORT TOKEN  (< 16 CHARS)
RN_TOKEN_LARGO   = "1737498440884ivbEXTRA"  # LONG TOKEN (> 16 CHARS)

# --- TEST DATA: AFFILIATION ---
RN_AFILIACION         = "9096021"   # VALID 7-DIGIT AFFILIATION
RN_AFILIACION_CORTA   = "12345"     # SHORT AFFILIATION (< 7 CHARS)
RN_AFILIACION_LARGA   = "12345678"  # LONG AFFILIATION  (> 7 CHARS)
RN_AFILIACION_INVALIDA = "9096011"  # INVALID (WRONG COMMERCE)

# --- REGISTRATION FORM (GENERIC) ---
XPATH_TXT_TOKEN_REGISTRO  = '//android.widget.EditText[1]'
XPATH_TXT_NUM_AFILIACION  = '//android.widget.EditText[2]'
XPATH_BTN_ACEPTAR_REGISTRO = (
    '//*[contains(@content-desc, "Aceptar") or '
    'contains(@text, "Aceptar")]'
)


# ==================================================================================
# [5] T6 MOBILE — XPATHS: CALCULADORA (C)
# ==================================================================================

# --- SCREEN IDENTIFIERS ---
XPATH_C_PANTALLA_COBRO       = '//*[contains(@text, "Cobrar") or contains(@content-desc, "Cobrar")]'
XPATH_C_DISPLAY_MONTO        = '//*[contains(@text, "0.00") or contains(@content-desc, "0.00")]'
XPATH_C_DISPLAY_UPDATED      = (
    '//*[(contains(@text, "$") and not(contains(@text, "$0.00"))) or '
    '(contains(@content-desc, "$") and not(contains(@content-desc, "$0.00")))]'
)
XPATH_C_DISPLAY_ZERO_LEADING = '//*[contains(@text, "0001") or contains(@content-desc, "0001")]'
XPATH_C_PANTALLA_TARJETA     = (
    '//*[contains(@text, "Inserta") or contains(@content-desc, "Inserta") or '
    'contains(@text, "Desliza") or contains(@content-desc, "Desliza")]'
)

# --- POPUPS ---
XPATH_C_BTN_MIENTRAS_USO = (
    '//*[contains(@text, "MIENTRAS LA APP") or contains(@content-desc, "MIENTRAS LA APP") or '
    'contains(@text, "Mientras la app") or contains(@content-desc, "Mientras la app") or '
    'contains(@text, "mientras la app") or contains(@content-desc, "mientras la app")]'
)
XPATH_C_POPUP_PROPINA       = (
    '//*[contains(@text, "propina") or contains(@content-desc, "propina") or '
    'contains(@text, "Propina") or contains(@content-desc, "Propina")]'
)
XPATH_C_POPUP_LECTOR        = '//*[contains(@text, "lector configurado") or contains(@content-desc, "lector configurado")]'
XPATH_C_POPUP_AJUSTES_VERDE = (
    '//*[contains(@text, "terminal configurada correctamente") or '
    'contains(@content-desc, "terminal configurada correctamente") or '
    'contains(@text, "Terminal configurada correctamente") or '
    'contains(@content-desc, "Terminal configurada correctamente")]'
)

# --- BUTTONS ---
XPATH_C_BTN_ACEPTAR_PROPINA   = '//*[contains(@text, "Aceptar") or contains(@content-desc, "Aceptar")]'
XPATH_C_BTN_CANCELAR          = '//*[contains(@text, "Cancelar") or contains(@content-desc, "Cancelar")]'
XPATH_C_BTN_OK_POPUP          = '//*[@text="Ok" or @content-desc="Ok" or @text="OK" or @content-desc="OK"]'
XPATH_C_BTN_DECIMAL           = '//*[@text="+" or @content-desc="+"]'
XPATH_C_BTN_CONFIGURAR_LECTOR = (
    '//*[contains(@text, "Configurar lector") or '
    'contains(@content-desc, "Configurar lector")]'
)

# --- BACKSPACE BUTTON ---
# STANDARD ATTRIBUTE-BASED SELECTOR (WORKS WHEN DISPLAY IS NOT FULL)
XPATH_C_BTN_BACKSPACE = (
    '//*[@text="\u232B" or @content-desc="\u232B" or '
    '@text="\u2190" or @content-desc="\u2190" or '
    'contains(@content-desc, "erase") or contains(@content-desc, "delete") or '
    'contains(@content-desc, "backspace") or contains(@content-desc, "borrar") or '
    'contains(@content-desc, "Borrar") or contains(@text, "borrar")]'
)
# ABSOLUTE XPATH FROM APPIUM INSPECTOR — USED AS LAST RESORT WHEN DISPLAY IS FULL
# (8+ DIGITS ENTERED). THE KEY LOSES ALL text/content-desc ATTRIBUTES IN THAT STATE.
XPATH_C_BTN_BACKSPACE_ABSOLUTE = (
    '//android.widget.FrameLayout[@resource-id="android:id/content"]'
    '/android.widget.FrameLayout'
    '/android.widget.FrameLayout'
    '/android.widget.FrameLayout'
    '/android.view.View/android.view.View/android.view.View'
    '/android.view.View/android.view.View[13]'
)

# --- ERROR MESSAGES ---
XPATH_C_ERROR_CANTIDAD_VALIDA = (
    '//*[contains(@text, "ingrese una cantidad") or '
    'contains(@content-desc, "ingrese una cantidad") or '
    'contains(@text, "cantidad valida") or '
    'contains(@content-desc, "cantidad valida")]'
)


# ==================================================================================
# [6] T6 MOBILE — XPATHS: PESTAÑAS (PÑ) — BOTTOM NAV TABS
# ==================================================================================

XPATH_C_TAB_INICIO       = '//*[contains(@content-desc, "Inicio") and contains(@content-desc, "1")]'
XPATH_C_TAB_AJUSTES      = '//*[contains(@content-desc, "Ajustes") and contains(@content-desc, "4")]'

XPATH_PÑ_TAB_HOME       = '//*[contains(@content-desc, "Inicio") and contains(@content-desc, "1")]'
XPATH_PÑ_TAB_TRANSACTIONS = '//*[contains(@content-desc, "Transacciones") and contains(@content-desc, "2")]'
XPATH_PÑ_TAB_SERVICIOS     = '//*[contains(@content-desc, "Servicios") and contains(@content-desc, "3")]'
XPATH_PÑ_TAB_AJUSTES       = '//*[contains(@content-desc, "Ajustes") and contains(@content-desc, "4")]'


# ==================================================================================
# [7] T6 MOBILE — XPATHS & DATA: REGISTRO DE AHORA (RA)
# ==================================================================================

# --- TEST DATA ---
RA_NOMBRE           = "Antonio"
RA_APELLIDO         = "Garcia"
RA_SEGUNDOAPELLIDO  = "Garcia"
RA_EMAIL            = "usuariofake@prueba.com"
RA_PASS             = "contrasenafake"

RA_010_NOMBRE           = "Santiago"
RA_010_APELLIDO         = "martinez"
RA_010_SEGUNDO_APELLIDO = "martinez"
RA_010_EMAIL            = "sss@gmail.com"
RA_010_PASS             = "Memphis@2030"

RA_013_EMAIL = "david.santos@ijuba.solutions"

# --- FORM INPUTS ---
XPATH_RA_NOMBRE          = '//android.widget.EditText[1]'
XPATH_RA_APELLIDO        = '//android.widget.EditText[2]'
XPATH_RA_SEGUNDOAPELLIDO = '//android.widget.EditText[3]'
XPATH_RA_EMAIL           = '//android.widget.EditText[4]'
XPATH_RA_PASS            = '//android.widget.EditText[5]'
XPATH_RA_CONFIRMAR_PASS  = '//android.widget.EditText[6]'

# --- BUTTONS ---
XPATH_RA_BTN_ACEPTAR = '//android.widget.Button[@content-desc="Aceptar"]'
XPATH_RA_BTN_ATRAS   = '//android.widget.Button[1]'

# --- VALIDATION ERROR MESSAGES ---
XPATH_RA_ERROR_NOMBRE = (
    '//*[contains(@text, "Ingresa un nombre") or '
    'contains(@content-desc, "Ingresa un nombre")]'
)
XPATH_RA_ERROR_USUARIO_EXISTE = (
    '//*[contains(@text, "usuario ya está registrado") or '
    'contains(@content-desc, "usuario ya está registrado") or '
    'contains(@text, "ya está registrado") or '
    'contains(@content-desc, "ya está registrado")]'
)
XPATH_RA_ERROR_PASS_NO_COINCIDEN = (
    '//*[contains(@text, "Las contraseñas no coinciden") or '
    'contains(@content-desc, "Las contraseñas no coinciden")]'
)
XPATH_RA_ERROR_CORREO_INVALIDO = (
    '//*[contains(@text, "Correo inválido") or '
    'contains(@content-desc, "Correo inválido")]'
)
XPATH_RA_ERROR_CONTRASENA_INVALIDA = (
    '//*[contains(@text, "Contraseña inválida") or '
    'contains(@content-desc, "Contraseña inválida")]'
)
XPATH_RA_REGISTRO_EXITOSO = (
    '//*[contains(@text, "suario creado correctamente") or '
    'contains(@text, "orrectamente") or '
    'contains(@content-desc, "suario creado correctamente") or '
    '//android.widget.Toast]'
)


# ==================================================================================
# [8] T6 MOBILE — XPATHS: OLVIDASTE CONTRASEÑA (OC)
# ==================================================================================

XPATH_OC_LNK_OLVIDASTE  = (
    '//*[contains(@text, "Olvidaste tu contraseña") or '
    'contains(@content-desc, "Olvidaste tu contraseña")]'
)
XPATH_OC_TITULO_RECUPERA = (
    '//*[contains(@text, "Recupera tu contraseña") or '
    'contains(@content-desc, "Recupera tu contraseña")]'
)
XPATH_OC_BTN_ATRAS   = '//android.widget.Button[1]'
XPATH_OC_INPUT_EMAIL = '//android.widget.EditText[1]'
XPATH_OC_BTN_ACEPTAR = '//android.widget.Button[@content-desc="Aceptar"]'
XPATH_OC_MSJ_EXITO   = (
    '//*[contains(@text, "ceso de recuperaci") or '
    'contains(@content-desc, "ceso de recuperaci")]'
)
XPATH_OC_ERROR_CORREO = (
    '//*[contains(@text, "Correo inválido") or '
    'contains(@content-desc, "Correo inválido")]'
)
NUMERO_AFILIACION = "9096021"


# ==================================================================================
# [9] T6 MOBILE — XPATHS: GENERIC ERROR SELECTORS
# ==================================================================================

XPATH_ERROR_GENERICO = (
    '//*['
    'contains(@content-desc, "Ocurri") or contains(@text, "Ocurri") or '
    'contains(@content-desc, "un error") or contains(@text, "un error") or '
    'contains(@content-desc, "intental") or contains(@text, "intental") or '
    'contains(@content-desc, "tarde") or contains(@text, "tarde") or '
    'contains(@text, "Ocurrió un error, inténtalo más tarde")'
    '] | //android.widget.Toast'
)

# ==================================================================================
# [10] T6 MOBILE — XPATHS: TRANSACCIONES [TS-70]
# ==================================================================================
# --- SCREEN VERIFICATION INDICATORS ---
# INDICATOR 1: TRANSACTIONS SCREEN HEADER / TITLE
XPATH_TS_HEADER_TITLE = (
    '//*[contains(@text, "Transacciones") or '
    'contains(@content-desc, "Transacciones")]'
)

# INDICATOR 2: TRANSACTION LIST ITEMS OR EMPTY STATE MESSAGE
XPATH_TS_EMPTY_STATE = (
    '//*[contains(@text, "No hay transacciones") or '
    'contains(@content-desc, "No hay transacciones") or '
    'contains(@text, "sin transacciones") or '
    'contains(@text, "historial") or '
    'contains(@content-desc, "historial")]'
)

# INDICATOR 3: TAB IN SELECTED/ACTIVE STATE
XPATH_TS_TAB_SELECTED_STATE = (
    '//*[contains(@content-desc, "Transacciones") and '
    '(@selected="true" or contains(@content-desc, "selected"))]'
)


# ==================================================================================
# [11] T6 MOBILE — XPATHS: TRANSACCIONES [TS-71]
# ==================================================================================
# THE DEFAULT ACTIVE TAB LABEL ON THE TRANSACTIONS SCREEN
XPATH_TS_TAB_30_DAYS = (
    '//*[contains(@text, "ltimos 30") or '
    'contains(@content-desc, "ltimos 30") or '
    'contains(@text, "30 d") or '
    'contains(@content-desc, "30 d")]'
)

# A TRANSACTION ROW ITEM — IDENTIFIED BY THE DATE FORMAT (DD-MM-YYYY, HH:MM:SS)
XPATH_TS_TRANSACTION_ITEM = (
    '//*[contains(@text, "2026") or contains(@content-desc, "2026") or '
    'contains(@text, "2025") or contains(@content-desc, "2025")]'
)

# DATE FIELD WITHIN A TRANSACTION ROW (SAME PATTERN — USED FOR STRUCTURE CHECK)
XPATH_TS_TRANSACTION_DATE = (
    '//*[contains(@text, "-202") or contains(@content-desc, "-202")]'
)

# AMOUNT FIELD — TRANSACTIONS SHOW DOLLAR AMOUNTS WITH "$" SIGN
XPATH_TS_TRANSACTION_AMOUNT = (
    '//*[contains(@text, "$") and not(contains(@text, "$0.00")) or '
    'contains(@content-desc, "$") and not(contains(@content-desc, "$0.00"))]'
)

# STATUS BADGE — "APROBACIÓN" OR "CANCELACIÓN"
XPATH_TS_TRANSACTION_STATUS = (
    '//*[contains(@text, "APROBACI") or contains(@content-desc, "APROBACI") or '
    'contains(@text, "CANCELACI") or contains(@content-desc, "CANCELACI")]'
)

# ==================================================================================
# [12] T6 MOBILE — XPATHS: TRANSACCIONES [TS-73]
# ==================================================================================
XPATH_TS_TAB_DAILY_CUT = (
    '//*[contains(@content-desc, "Corte por d") or '
    'contains(@content-desc, "corte por d")]'
)

XPATH_TS_TAB_DAILY_CUT_TEXT = (
    '//*[@text="Corte por día" or @text="Corte por dia"]'
)

XPATH_TS_TAB_DAILY_CUT_PARTIAL = (
    '//*[contains(@text, "Corte") or contains(@content-desc, "Corte")]'
)

XPATH_TS_TAB_DAILY_CUT_SIBLING = (
    '(//android.view.View[contains(@content-desc, "ltimos") or '
    'contains(@text, "ltimos")]/following-sibling::android.view.View)[1]'
)

# SUMMARY SECTION LABELS
XPATH_TS_TOTAL_COUNT_AMOUNT = (
    '//*[contains(@text, "Monto total") or '
    'contains(@content-desc, "Monto total")]'
)
XPATH_TS_SUBTOTAL_CUT_PAYMENTS = (
    '//*[contains(@text, "Subtotal de pagos") or '
    'contains(@content-desc, "Subtotal de pagos")]'
)

# ACTION BUTTON
XPATH_TS_BTN_PRINT_CUT = (
    '//*[contains(@text, "Imprimir corte") or '
    'contains(@content-desc, "Imprimir corte")]'
)

# MOVIMIENTOS SECTION LABEL (BOTTOM OF SCREEN, WITH CHEVRON)
XPATH_TS_CUT_MOVEMENTS = (
    '//*[contains(@text, "Movimientos") or '
    'contains(@content-desc, "Movimientos")]'
)

# ==================================================================================
# [13] T6 MOBILE — XPATHS: TRANSACCIONES [TS-74]
# ==================================================================================
XPATH_TS_BTN_PREVIOUS_DATE = (
    '//*[@content-desc="◄" or @text="◄" or '
    'contains(@content-desc, "anterior") or '
    'contains(@content-desc, "atr")]'
)
# STRATEGY 2: FIRST ARROW-LIKE ELEMENT NEAR THE DATE DISPLAY
XPATH_TS_BTN_FECHA_ANTERIOR_ALT = (
    '(//android.view.View[@clickable="true"])[1]'
)

# EMPTY STATE MESSAGE
XPATH_TS_FECHA_SIN_REGISTROS = (
    '//*[contains(@text, "sin registros") or '
    'contains(@content-desc, "sin registros") or '
    'contains(@text, "Sin registros") or '
    'contains(@content-desc, "Sin registros")]'
)

XPATH_TS_CORTE_MONTO_CERO = (
    '//*[@text="$0.00" or @content-desc="$0.00"]'
)

TS_DIAS_ATRAS_SIN_REGISTRO = 60
TS_FECHA_SIN_REGISTROS = "~60 DAYS AGO (EXPECTED EMPTY)"

# ==============================================================================================
# [14] T6 MOBILE — XPATHS: TRANSACCIONES [TS-75] ◄ BACK ARROW — STRATEGY 2: ATTRIBUTE-BASED
# ==============================================================================================
XPATH_TS_BTN_PREVIOUS_DATE = (
    '//*[contains(@content-desc, "anterior") or '
    'contains(@content-desc, "atr") or '
    'contains(@content-desc, "prev") or '
    '@content-desc="◄" or @text="◄"]'
)
# ◄ BACK ARROW — FROM APPIUM INSPECTOR (ABSOLUTE — MOST RELIABLE)
XPATH_TS_BTN_PREVIOUS_DATE = (
    '//android.widget.ScrollView/android.widget.Button[1]'
)

# ► FORWARD ARROW — SIBLING OF ◄ (BUTTON[2] IN SAME SCROLLVIEW)
XPATH_TS_BTN_NEXT_DATE = (
    '//android.widget.ScrollView/android.widget.Button[2]'
)
# DATE TEXT IN NAVIGATOR BAR — MATCHES "Miércoles, 15 abril" FORMAT
XPATH_TS_NAVIGATOR_DATE_TEXT = (
    '//*[contains(@text, ",") or contains(@content-desc, ",")]'
)

TS_ARROW_BACK_X = 60    
TS_ARROW_FWD_X  = 390   
TS_ARROW_Y      = 315   


# ==============================================================================================
# [15] T6 MOBILE — XPATHS: TRANSACCIONES [TS-76]
# ==============================================================================================
# LIST — STATUS BADGE SELECTOR
XPATH_TS_ITEM_APPROVAL_STATUS = (
    '//*[contains(@text, "APROBACI") or '
    'contains(@content-desc, "APROBACI")]'
)

# LIST — FIRST ROW FALLBACK 
XPATH_TS_FIRST_LIST_ROW = (
    '//android.widget.ScrollView//android.view.View[1]'
)

# DETAIL SCREEN — TITLE
XPATH_TS_TITLE_DETAILS = (
    '//*[@text="Detalle" or @content-desc="Detalle" or '
    'contains(@text, "Detalle") or contains(@content-desc, "Detalle")]'
)

# DETAIL SCREEN — LARGE AMOUNT AT TOP
XPATH_TS_LARGE_SCALE_DETAIL = (
    '//*[contains(@text, "$") and contains(@text, ".") and '
    'not(contains(@text, "0.00"))]'
)

# DETAIL SCREEN — ESTATUS VALUE
XPATH_TS_DETAIL_APPROVED_STATUS = (
    '//*[@text="APROBADA" or @content-desc="APROBADA" or '
    'contains(@text, "APROBADA") or contains(@content-desc, "APROBADA")]'
)

# EACH KEY IS THE LABEL NAME, VALUE IS ITS XPATH
TS_DETAILS_REQUIRED_FIELDS = {
    "ESTATUS"           : '//*[contains(@text, "Estatus") or contains(@content-desc, "Estatus")]',
    "VENTA"             : '//*[contains(@text, "Venta") or contains(@content-desc, "Venta")]',
    "PROPINA"           : '//*[contains(@text, "Propina") or contains(@content-desc, "Propina")]',
    "NOMBRE COMERCIO"   : '//*[contains(@text, "Nombre del comercio") or contains(@content-desc, "Nombre del comercio")]',
    "ID"                : '//*[@text="ID" or @content-desc="ID"]',
    "FECHA"             : '//*[contains(@text, "Fecha") or contains(@content-desc, "Fecha")]',
    "TARJETA"           : '//*[contains(@text, "Tarjeta") or contains(@content-desc, "Tarjeta")]',
    "BTN_REIMPRIMIR"    : '//*[contains(@text, "Reimprimir") or contains(@content-desc, "Reimprimir")]',
}

# ==============================================================================================
# [15] T6 MOBILE — XPATHS: TRANSACCIONES [TS-77]
# ==============================================================================================
# --- TS-77: CANCELACIÓN DETAIL ---

# LIST — CANCELACIÓN STATUS BADGE
XPATH_TS_ITEM_STATUS_CANCELATION = (
    '//*[contains(@text, "CANCELACI") or '
    'contains(@content-desc, "CANCELACI")]'
)

# DETAIL SCREEN — VENTA / CANCELACIÓN TABS
XPATH_TS_DETAIL_SELL_TAB = (
    '//*[@text="Venta" or @content-desc="Venta" or '
    'contains(@text, "Venta") or contains(@content-desc, "Venta")]'
)
XPATH_TS_DETAIL_CANCELATION_TAB = (
    '//*[@text="Cancelación" or @content-desc="Cancelación" or '
    'contains(@text, "Cancelaci") or contains(@content-desc, "Cancelaci")]'
)

# ==============================================================================================
# [16] T6 MOBILE — XPATHS: TRANSACCIONES [TS-79 - TS-80]
# ==============================================================================================
TS_MAX_SEARCH_DAYS = 120
XPATH_TS_LOADING_CARGANDO = (
    '//*[contains(@text, "Cargando") or contains(@content-desc, "Cargando") or '
    'contains(@text, "cargando") or contains(@content-desc, "cargando") or '
    'contains(@text, "Loading") or contains(@content-desc, "Loading")]'
)

# ==================================================================================
# [10] WEB PLATFORM — URLS & DRIVER SETTINGS
# ==================================================================================

URL_MEMPHIS_WEB = "https://fat.memphis.mx/v2/login"
URL_MEMPHIS_PWD = "https://fat.memphis.mx/recovery-password"

# DEFAULT IMPLICIT WAIT FOR WEB DRIVER (SECONDS)
WEB_IMPLICIT_WAIT   = 10
WEB_EXPLICIT_WAIT   = 15


# ==================================================================================
# [11] WEB PLATFORM — CREDENTIALS
# ==================================================================================

# --- FULL-ACCESS USER (CRUD PERMISSIONS) ---
WEB_USUARIO_PRUEBA = "eamartin"
WEB_PASS_PRUEBA    = "Patito4."

# --- NEGATIVE TEST CREDENTIALS ---
WEB_WRONGUSER = "usuariofake"
WEB_WRONGPASS = "contrasenafake"

# --- PERMISSION-RESTRICTED USERS ---
# NOTE: REPLACE WITH REAL RESTRICTED ACCOUNTS FROM YOUR QA ENVIRONMENT.
WEB_USUARIO_SIN_EDICION = "usuario.readonly@memphis.mx"   # NO EDIT PERMISSIONS
WEB_USUARIO_SIN_BORRADO = "usuario.nodelete@memphis.mx"   # NO DELETE PERMISSIONS


# ==================================================================================
# [12] WEB PLATFORM — XPATHS: LOGIN SCREEN
# ==================================================================================

XPATH_WEB_USER      = '//input[@type="email" or @type="text"]'
XPATH_WEB_PASS      = '//input[@type="password"]'
XPATH_WEB_BTN_LOGIN = '//button[contains(text(), "Inicia") or contains(text(), "Login")]'

# NEGATIVE TEST SELECTORS (SAME DOM LOCATION — KEPT SEPARATE FOR READABILITY)
XPATH_WEB_WRONG_USER = '//input[@type="email" or @type="text"]'
XPATH_WEB_WRONG_PASS = '//input[@type="password"]'

# NAVIGATION LINKS ON THE LOGIN SCREEN
XPATH_WEB_TXT_INGRESA_AQUI    = "//*[contains(text(), 'Ingresa aquí')]"
XPATH_WEB_BTN_REGISTRA_AHORA  = '//android.widget.Button[@content-desc="Regístrate ahora"]'
XPATH_REGISTRA_AHORA_ALT1     = '//*[contains(@content-desc, "Regístrate")]'
XPATH_REGISTRA_AHORA_ALT2     = '//*[contains(@content-desc, "gístrate")]'


# ==================================================================================
# [13] WEB PLATFORM — XPATHS: PASSWORD RECOVERY FLOW
# ==================================================================================

# --- FORGOT PASSWORD SCREEN ---
XPATH_WEB_TITULO_OLVIDASTE = "//*[contains(text(), 'Olvidaste tu contraseña')]"
XPATH_WEB_BTN_ENVIAR       = "//*[contains(text(), 'Enviar')]"
XPATH_MSJ_EXITO_RCV        = "//*[contains(text(), 'Se ha enviado un mail')]"

# --- EMAIL RECOVERY LINK ---
XPATH_EMAIL_LINK_RESET = (
    '//a[contains(text(), "Restablecer") or '
    'contains(text(), "Recuperar") or '
    'contains(text(), "aquí")]'
)

# --- NEW PASSWORD SCREEN ---
XPATH_TITULO_NUEVA_PASS = (
    '//*[contains(text(), "Nueva contraseña") or '
    'contains(text(), "Restablecer") or '
    'contains(text(), "Crear")]'
)
XPATH_INPUT_NUEVA_PASS = '//input[@type="password"]'

# --- CHANGE PASSWORD FORM ---
XPATH_PWD_ACTUAL      = '//input[@name="currentPassword" or @type="password"][1]'
XPATH_PWD_NUEVA       = '(//input[@type="password"])[2]'
XPATH_PWD_CONFIRMAR   = '(//input[@type="password"])[3]'
XPATH_PWD_BTN_ESTABLECER = (
    '//*[contains(text(), "Establecer contraseña") or '
    'contains(text(), "Guardar")]'
)
XPATH_BTN_ACEPTAR_WEB = '//*[contains(text(), "Reestablecer Contraseña")]'

# --- EYE TOGGLE BUTTONS ---
XPATH_BTN_OJO_NUEVA_PASS = (
    "(//span[contains(@class,'ng-star-inserted') and "
    "./i[contains(@class,'pi-eye')]])[1]"
)
XPATH_BTN_OJO_CONFIRMAR  = "(//i[contains(@class,'pi-eye')])[2]"

# COMBINED SELECTOR FOR SECOND PASSWORD FIELD (VISIBLE OR MASKED)
XPATH_INPUT_REPITE_PASS = '(//input[@type="password" or @type="text"])[2]'


# ==================================================================================
# [14] WEB PLATFORM — XPATHS: ERROR / VALIDATION MESSAGES
# ==================================================================================

XPATH_PWD_ERROR_VACIO       = '//*[contains(text(), "requerido") or contains(text(), "obligatorio")]'
XPATH_PWD_ERROR_INCORRECTA  = '//*[contains(text(), "incorrecta")]'
XPATH_PWD_ERROR_REGLAS      = '//*[contains(text(), "Debe contener mínimo") or contains(text(), "caracteres")]'
XPATH_PWD_ERROR_NO_COINCIDEN = '//*[contains(text(), "no coinciden")]'
XPATH_ERROR_PASS_NO_COINCIDE = "//*[contains(text(), 'Las contraseñas no coinciden')]"
XPATH_ERROR_PASS_MAYUSCULA   = "//*[contains(text(), 'Debe contener al menos una mayúscula')]"
XPATH_BTN_APPLY_FILTER       = "//button[contains(text(), 'CREADO') or contains(text(), 'Creado')]"

# ==================================================================================
# MODULE CONFIGURATION
# ==================================================================================
USUARIOS_URL      = "https://fat.memphis.mx/cat/users"
NUEVO_USUARIO_URL = "https://fat.memphis.mx/cat/users/create"