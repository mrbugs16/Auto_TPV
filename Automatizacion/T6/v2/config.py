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
    "appium:appPackage"         : "com.memphis.app.dev",
    "appium:appActivity"        : "com.memphis.app.MainActivity",
    "appium:autoGrantPermissions": False,
    "appium:noReset"            : False,
}


# ==================================================================================
# [2] T6 MOBILE — CREDENTIALS
# ==================================================================================

USUARIO_VALIDO   = "david.santos@ijuba.solutions"
PASS_VALIDO      = "Memphis@2026"
USUARIO_INVALIDO = "usuario.noexiste@prueba.com"
PASS_INVALIDO    = "ContrasenaFalsa123"


# ==================================================================================
# [3] T6 MOBILE — XPATHS: ONBOARDING SCREENS (NEW APP v2)
# ==================================================================================
# SCREEN 1 — "CONFIGURA LA TERMINAL"
# SCREEN 2 — "INGRESA LA INFORMACIÓN DE TU COMERCIO"
# SCREEN 3 — "EMPIEZA A REALIZAR COBROS"

# --- NAVIGATION BUTTONS (SHARED ACROSS ONBOARDING SLIDES) ---
XPATH_OB_BTN_SIGUIENTE  = '//android.widget.Button[@content-desc="Siguiente"]'
XPATH_OB_BTN_COMENZAR   = '//android.widget.Button[@content-desc="Comenzar"]'
XPATH_OB_BTN_SALTAR     = '//*[contains(@content-desc, "Saltar") or contains(@text, "Saltar")]'

# --- LINK TO LOGIN (BOTTOM OF ONBOARDING) ---
XPATH_OB_LNK_INGRESA    = (
    '//*[contains(@content-desc, "Ingresa aquí") or '
    'contains(@text, "Ingresa aquí")]'
)

# --- SCREEN IDENTIFIERS ---
XPATH_OB_SLIDE_1 = (
    '//*[contains(@content-desc, "Configura la terminal") or '
    'contains(@text, "Configura la terminal")]'
)
XPATH_OB_SLIDE_2 = (
    '//*[contains(@content-desc, "Ingresa la información") or '
    'contains(@text, "Ingresa la información")]'
)
XPATH_OB_SLIDE_3 = (
    '//*[contains(@content-desc, "Empieza a realizar cobros") or '
    'contains(@text, "Empieza a realizar cobros")]'
)


# ==================================================================================
# [3B] T6 MOBILE — XPATHS: LOGIN SCREEN (NEW APP v2)
# ==================================================================================
# SCREEN A: "INICIAR SESIÓN"
#   FLOW: Onboarding → Login → Configura tu comercio → Lector no configurado → Home

# --- SCREEN A: LOGIN INPUTS ---
XPATH_INPUT_USUARIO = '//android.widget.EditText[1]'
XPATH_INPUT_PASS    = '//android.widget.EditText[2]'

# --- SCREEN A: LOGIN BUTTONS ---
XPATH_BTN_ACEPTAR    = '//android.widget.Button[@content-desc="Iniciar sesión"]'
XPATH_LG_BTN_INICIAR = '//android.widget.Button[@content-desc="Iniciar sesión"]'

# --- SCREEN A: LOGIN LINKS ---
XPATH_LG_LNK_OLVIDASTE    = (
    '//*[contains(@content-desc, "Olvidaste la contraseña") or '
    'contains(@text, "Olvidaste la contraseña")]'
)
XPATH_LG_LNK_CREAR_CUENTA = (
    '//*[contains(@content-desc, "Crear cuenta") or '
    'contains(@text, "Crear cuenta")]'
)

# --- SCREEN A: ERROR TOAST ---
# OBSERVED TEXT: "Usuario o contraseña incorrectos"
# TRANSIENT RED BANNER (~2-3s) — POLL IMMEDIATELY AFTER SUBMIT
XPATH_LG_ERROR_TOAST = (
    '//*[contains(@content-desc, "incorrectos") or '
    'contains(@text, "incorrectos") or '
    'contains(@content-desc, "Usuario o contrase") or '
    'contains(@text, "Usuario o contrase")]'
)
XPATH_LG_ERROR_CREDENCIALES = XPATH_LG_ERROR_TOAST   # BACKWARD COMPATIBILITY ALIAS


# ==================================================================================
# [3C] T6 MOBILE — XPATHS: "CONFIGURA TU COMERCIO" SCREEN (NEW APP v2)
# ==================================================================================
# SCREEN B — APPEARS AFTER FIRST SUCCESSFUL LOGIN WHEN COMMERCE IS NOT YET LINKED.
#
# LAYOUT (CONFIRMED FROM APPIUM INSPECTOR):
#   FIELD 1 : "Número de afiliación"   placeholder "Ej. 1234567"
#   FIELD 2 : "Token"                  placeholder "Token de registro"
#   BUTTON  : "Confirmar y comenzar"
#   LINK    : "Cancelar"

# --- SCREEN IDENTIFIER ---
XPATH_CC_SCREEN = (
    '//*[contains(@content-desc, "Configura tu comercio") or '
    'contains(@text, "Configura tu comercio")]'
)

# --- FORM INPUTS (ORDER: Afiliación=1, Token=2) ---
XPATH_CC_INPUT_AFILIACION = '//android.widget.EditText[1]'
XPATH_CC_INPUT_TOKEN      = '//android.widget.EditText[2]'

# --- BUTTONS (EXACT XPATHS FROM APPIUM INSPECTOR) ---
XPATH_CC_BTN_CONFIRMAR = '//android.widget.Button[@content-desc="Confirmar y comenzar"]'
XPATH_CC_BTN_CANCELAR  = (
    '//*[contains(@content-desc, "Cancelar") or '
    'contains(@text, "Cancelar")]'
)

# --- TEST DATA ---
CC_AFILIACION = "8920377"           # VALID AFFILIATION NUMBER (NEW APP v2)
CC_TOKEN      = "1733258724574qkd"  # VALID REGISTRATION TOKEN  (NEW APP v2)


# ==================================================================================
# [3D] T6 MOBILE — XPATHS: "LECTOR NO CONFIGURADO" POPUP (NEW APP v2)
# ==================================================================================
# SCREEN C — BOTTOM SHEET AFTER "CONFIGURA TU COMERCIO" IS SUBMITTED.
# ALSO APPEARS ON SUBSEQUENT LOGINS IF READER IS STILL NOT SET UP.
#
# BUTTONS (EXACT XPATHS FROM APPIUM INSPECTOR):
#   "Configurar ahora" → navigates to reader setup flow
#   "Después"          → dismisses popup, lands on home / calculadora

# --- POPUP IDENTIFIER ---
XPATH_LG_POPUP_LECTOR_NC = (
    '//*[contains(@content-desc, "Lector no configurado") or '
    'contains(@text, "Lector no configurado")]'
)

# --- POPUP BUTTONS ---
XPATH_LG_BTN_CONFIGURAR_AHORA = '//android.widget.Button[@content-desc="Configurar ahora"]'
XPATH_LG_BTN_DESPUES          = (
    '//*[contains(@content-desc, "Después") or '
    'contains(@text, "Después")]'
)


# ==================================================================================
# [3D-EXT] T6 MOBILE — XPATHS: "LECTOR CONFIGURADO" CONFIRMATION SCREEN
# ==================================================================================
# SCREEN D-EXT — APPEARS AFTER CLICKING "Configurar ahora" FROM THE LECTOR POPUP.
# CONTENT   : Memphis icon + "Lector configurado" + "Configuración completada" + 100% bar
# ACTION    : CLICK "Aceptar" TO DISMISS AND LAND ON THE HOME / CALCULADORA SCREEN.

XPATH_LG_LECTOR_CONFIGURADO      = (
    '//*[contains(@content-desc, "Lector configurado") or '
    'contains(@text, "Lector configurado")]'
)
XPATH_LG_BTN_ACEPTAR_LECTOR       = '//android.widget.Button[@content-desc="Aceptar"]'
XPATH_LG_CONFIGURACION_COMPLETADA = (
    '//*[contains(@content-desc, "Configuración completada") or '
    'contains(@text, "Configuración completada")]'
)


# ==================================================================================
# [3E] T6 MOBILE — XPATHS: HOME SCREEN / CALCULADORA (NEW APP v2)
# ==================================================================================
# SCREEN D — FINAL DESTINATION AFTER COMPLETING THE FULL LOGIN FLOW.
# VISIBLE ELEMENTS: "INGRESA LA CANTIDAD A COBRAR", "$0.00", "MXN"

XPATH_LG_PANTALLA_HOME = (
    '//*[contains(@content-desc, "INGRESA LA CANTIDAD") or '
    'contains(@text, "INGRESA LA CANTIDAD") or '
    'contains(@content-desc, "MXN") or '
    'contains(@text, "MXN") or '
    'contains(@content-desc, "0.00") or '
    'contains(@text, "0.00")]'
)

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
RN_TOKEN         = "1733258724574qkd"    # VALID TOKEN (NEW APP v2)
RN_TOKEN_INVALIDO = "0000000000000err"   # INVALID TOKEN (WRONG CREDENTIALS)
RN_TOKEN_CORTO   = "123456890"           # SHORT TOKEN  (< 16 CHARS)
RN_TOKEN_LARGO   = "1733258724574qkdEXTRA"  # LONG TOKEN (> 16 CHARS)

# --- TEST DATA: AFFILIATION ---
RN_AFILIACION         = "8920377"   # VALID AFFILIATION (NEW APP v2)
RN_AFILIACION_CORTA   = "12345"     # SHORT AFFILIATION (< 7 CHARS)
RN_AFILIACION_LARGA   = "12345678"  # LONG AFFILIATION  (> 7 CHARS)
RN_AFILIACION_INVALIDA = "0000000"  # INVALID (WRONG COMMERCE)

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

XPATH_C_TAB_HOME       = '//*[contains(@content-desc, "Inicio") or @content-desc="Inicio"]'
XPATH_C_TAB_AJUSTES      = '//*[contains(@content-desc, "Ajustes") or @content-desc="Ajustes"]'

XPATH_PÑ_TAB_HOME       = '//*[contains(@content-desc, "Inicio") or @content-desc="Inicio"]'
XPATH_PÑ_TAB_TRANSACTIONS = '//*[contains(@content-desc, "Transacciones") or @content-desc="Transacciones"]'
XPATH_PÑ_TAB_SERVICES     = '//*[contains(@content-desc, "Servicios") or @content-desc="Servicios"]'
XPATH_PÑ_TAB_AJUSTES       = '//*[contains(@content-desc, "Ajustes") or @content-desc="Ajustes"]'


# ==================================================================================
# [7] T6 MOBILE — XPATHS & DATA: REGISTRO DE AHORA (RA)
# ==================================================================================

# --- TEST DATA ---
RA_FIRST_NAME           = "Antonio"
RA_APELLIDO         = "Garcia"
RA_SEGUNDOAPELLIDO  = "Garcia"
RA_EMAIL            = "usuariofake@prueba.com"
RA_PASS             = "contrasenafake"

RA_010_FIRST_NAME           = "Santiago"
RA_010_APELLIDO         = "martinez"
RA_010_SEGUNDO_APELLIDO = "martinez"
RA_010_EMAIL            = "sss@gmail.com"
RA_010_PASS             = "Memphis@2030"

RA_013_EMAIL = "david.santos@ijuba.solutions"

# --- FORM INPUTS ---
XPATH_RA_FIRST_NAME      = '//android.widget.EditText[1]'
XPATH_RA_APELLIDO        = '//android.widget.EditText[2]'
XPATH_RA_SEGUNDOAPELLIDO = '//android.widget.EditText[3]'
XPATH_RA_EMAIL           = '//android.widget.EditText[4]'
XPATH_RA_PASS            = '//android.widget.EditText[5]'
XPATH_RA_CONFIRMAR_PASS  = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.EditText[6]'

# --- BUTTONS ---
XPATH_RA_BTN_ACEPTAR = '//android.widget.Button[@content-desc="Aceptar"]'
XPATH_RA_BTN_ATRAS   = '//android.widget.Button[1]'

# --- VALIDATION ERROR MESSAGES ---
XPATH_RA_ERROR_FIRST_NAME = (
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
# STRATEGY 2: FIRST ARROW-LIKE ELEMENT NEAR THE DATE DISPLAY
XPATH_TS_BTN_PREVIOUS_DATE_ALT = (
    '(//android.view.View[@clickable="true"])[1]'
)

# EMPTY STATE MESSAGE
XPATH_TS_NO_RECORDS_DATE = (
    '//*[contains(@text, "sin registros") or '
    'contains(@content-desc, "sin registros") or '
    'contains(@text, "Sin registros") or '
    'contains(@content-desc, "Sin registros")]'
)

XPATH_TS_CUT_ZERO_AMOUNT = (
    '//*[@text="$0.00" or @content-desc="$0.00"]'
)

TS_DAYS_BACK_NO_RECORD = 60
TS_DATE_NO_RECORDS = "~60 DAYS AGO (EXPECTED EMPTY)"

# ==============================================================================================
# [14] T6 MOBILE — XPATHS: TRANSACCIONES [TS-75] ◄ BACK ARROW — STRATEGY 2: ATTRIBUTE-BASED
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
XPATH_TS_LOADING_INDICATOR = (
    '//*[contains(@text, "Cargando") or contains(@content-desc, "Cargando") or '
    'contains(@text, "cargando") or contains(@content-desc, "cargando") or '
    'contains(@text, "Loading") or contains(@content-desc, "Loading")]'
)
# WEB PLATFORM — XPATHS: COMERCIOS (MER)
# ==================================================================================

# 1. BOTÓN PARA CREAR UN NUEVO COMERCIO
XPATH_BTN_NUEVO = "//button[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyzáéíóúñ', 'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚÑ'), 'NUEVO') or contains(., '+')]"

# 2. BOTÓN DE LÁPIZ (EDITAR) EN LA PRIMERA FILA DE LA TABLA
XPATH_BTN_PENCIL_FIRST_ROW = "(//tbody//tr[1]//button[contains(@class, 'edit') or contains(@class, 'pencil') or .//i[contains(@class, 'pi-pencil')]])[1]"


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

# ==================================================================================
# [AJ] T6 MOBILE — XPATHS & DATA: AJUSTES (SETTINGS) MODULE
# ==================================================================================
# SCREEN: "Ajustes" — bottom nav tab [4]
# SECTIONS: Cuenta | Lector | PinPad | Desarrollador

# --- TAB NAVIGATION ---
XPATH_AJ_TAB_SETTINGS   = '//*[contains(@content-desc, "Ajustes") or @content-desc="Ajustes"]'

# --- SETTINGS SCREEN IDENTIFIERS ---
XPATH_AJ_SCREEN_TITLE   = (
    '//*[@text="Ajustes" or @content-desc="Ajustes"]'
)
XPATH_AJ_SECTION_CUENTA = (
    '//*[@text="Cuenta" or @content-desc="Cuenta"]'
)
XPATH_AJ_SECTION_LECTOR = (
    '//*[@text="Lector" or @content-desc="Lector"]'
)

# --- SETTINGS MENU ITEMS (CONFIRMED FROM SCREENSHOT 2) ---
XPATH_AJ_BTN_INFO_PERSONAL = (
    '//*[contains(@text,"Información personal") or '
    'contains(@content-desc,"Información personal")]'
)
XPATH_AJ_BTN_CAMBIAR_PASS = (
    '//*[contains(@text,"Cambiar contraseña") or '
    'contains(@content-desc,"Cambiar contraseña")]'
)
XPATH_AJ_BTN_CAMBIAR_COMERCIO = (
    '//*[contains(@text,"Cambiar comercio") or '
    'contains(@content-desc,"Cambiar comercio")]'
)
XPATH_AJ_BTN_ACTUALIZAR_CONFIG = (
    '//*[contains(@text,"Actualizar configuraciones") or '
    'contains(@content-desc,"Actualizar configuraciones")]'
)
XPATH_AJ_BTN_CERRAR_SESION = (
    '//*[contains(@text,"Cerrar sesión") or '
    'contains(@content-desc,"Cerrar sesión")]'
)

# --- PERSONAL INFO SCREEN (SCREENSHOT 3) ---
XPATH_AJ_INFO_SCREEN_TITLE = (
    '//*[@text="Información personal" or @content-desc="Información personal"]'
)
XPATH_AJ_INFO_AFILIACION   = '//*[@text="Afiliación" or @content-desc="Afiliación"]'
XPATH_AJ_INFO_NOMBRE       = '//*[@text="Nombre" or @content-desc="Nombre"]'
XPATH_AJ_INFO_LECTOR       = '//*[@text="Lector asociado" or @content-desc="Lector asociado"]'
XPATH_AJ_INFO_EMAIL        = '//*[@text="Correo electrónico" or @content-desc="Correo electrónico"]'
XPATH_AJ_INFO_UUID         = '//*[@text="UUID" or @content-desc="UUID"]'
XPATH_AJ_INFO_VERSION      = (
    '//*[contains(@text,"Versión") or contains(@content-desc,"Versión")]'
)

# --- PERSONAL INFO: EXPECTED DATA VALUES (CONFIRMED FROM SCREENSHOT 3) ---
AJ_EXPECTED_AFILIACION  = "8920377"
AJ_EXPECTED_EMAIL       = "david.santos@ijuba.solutions"

# --- CHANGE PASSWORD SCREEN (SCREENSHOTS 4-8) ---
XPATH_AJ_PASS_SCREEN_TITLE  = (
    '//*[@text="Cambiar contraseña" or @content-desc="Cambiar contraseña"]'
)
# INPUT FIELDS — ORDER: current(1) → new(2) → confirm(3)
XPATH_AJ_INPUT_PASS_CURRENT = '//android.widget.EditText[1]'
XPATH_AJ_INPUT_PASS_NEW     = '//android.widget.EditText[2]'
XPATH_AJ_INPUT_PASS_CONFIRM = '//android.widget.EditText[3]'

# SUBMIT BUTTON
XPATH_AJ_BTN_ACTUALIZAR = (
    '//*[@text="Actualizar" or @content-desc="Actualizar"]'
)

# VISIBILITY TOGGLE ICONS (eye icons — one per field)
XPATH_AJ_EYE_CURRENT  = '//android.widget.EditText[1]/..//*[@content-desc="Toggle password visibility"]'
XPATH_AJ_EYE_NEW      = '//android.widget.EditText[2]/..//*[@content-desc="Toggle password visibility"]'
XPATH_AJ_EYE_CONFIRM  = '//android.widget.EditText[3]/..//*[@content-desc="Toggle password visibility"]'

# --- CHANGE PASSWORD: TEST DATA (CONFIRMED FROM SCREENSHOTS 5, 8) ---
AJ_PASS_CURRENT_VALID      = "Memphis@2021"   # VALID CURRENT PASSWORD
AJ_PASS_NEW_VALID          = "Memphis@2026"   # VALID NEW PASSWORD (AJ-109)
AJ_PASS_WRONG_CURRENT      = "Memphis@2004"   # WRONG CURRENT PASSWORD (AJ-110)
AJ_PASS_NEW_MISMATCH_A     = "123456$M"       # NEW PASS (AJ-111 — mismatch test)
AJ_PASS_NEW_MISMATCH_B     = "123456$"        # CONFIRM PASS (AJ-111 — different)
AJ_PASS_TOO_SHORT          = "123456$"        # < 8 CHARS (AJ-112)
AJ_PASS_TOO_SHORT_CONFIRM  = "........"       # CONFIRM FILLER (AJ-112)
AJ_PASS_VISIBILITY_CURRENT = "Memphis@2004"   # (AJ-113)
AJ_PASS_VISIBILITY_NEW     = "123456$M"       # (AJ-113)

# --- CHANGE PASSWORD: RESPONSE TOASTS ---
XPATH_AJ_TOAST_SUCCESS = (
    '//*[contains(@text,"actualiz") or contains(@content-desc,"actualiz") or '
    'contains(@text,"éxito") or contains(@content-desc,"éxito") or '
    'contains(@text,"correcta") or contains(@content-desc,"correcta")]'
)
XPATH_AJ_TOAST_WRONG_PASS = (
    '//*[contains(@text,"incorrecta") or contains(@content-desc,"incorrecta") or '
    'contains(@text,"actual") or contains(@content-desc,"actual") or '
    'contains(@text,"anterior") or contains(@content-desc,"anterior")]'
)
XPATH_AJ_ERROR_NO_MATCH = (
    '//*[contains(@text,"no coinciden") or contains(@content-desc,"no coinciden")]'
)
XPATH_AJ_ERROR_MIN_CHARS = (
    '//*[contains(@text,"8 caracteres") or contains(@content-desc,"8 caracteres") or '
    'contains(@text,"Mínimo") or contains(@content-desc,"Mínimo")]'
)

# ==================================================================================
# [AJ-EXT] T6 MOBILE — XPATHS & DATA: CAMBIAR COMERCIO + CERRAR SESIÓN + LECTOR
# ==================================================================================

# --- CAMBIAR COMERCIO SCREEN (SCREENSHOTS 2-5) ---
XPATH_AJ_BTN_CAMBIAR_COMERCIO_MENU = (
    '//*[contains(@text,"Cambiar comercio") or '
    'contains(@content-desc,"Cambiar comercio")]'
)
XPATH_AJ_CC_SCREEN_TITLE = (
    '//*[@text="Cambiar comercio" or @content-desc="Cambiar comercio"]'
)
# FIELD 1: "Número de afiliación"
XPATH_AJ_CC_INPUT_AFILIACION = '//android.widget.EditText[1]'
# FIELD 2: "Token de registro"
XPATH_AJ_CC_INPUT_TOKEN = '//android.widget.EditText[2]'
# SUBMIT BUTTON
XPATH_AJ_CC_BTN_ACEPTAR = (
    '//*[@text="Aceptar" or @content-desc="Aceptar"]'
)

# --- CAMBIAR COMERCIO: VALIDATION ERRORS (SCREENSHOT 4) ---
XPATH_AJ_CC_ERROR_AFILIACION = (
    '//*[contains(@text,"ingresa el número de afiliación") or '
    'contains(@content-desc,"ingresa el número de afiliación") or '
    'contains(@text,"afiliación") or contains(@content-desc,"afiliación")]'
)
XPATH_AJ_CC_ERROR_TOKEN = (
    '//*[contains(@text,"ingresa el token") or '
    'contains(@content-desc,"ingresa el token") or '
    'contains(@text,"token de registro") or contains(@content-desc,"token de registro")]'
)
# RED TOAST: "Error de registro" (SCREENSHOTS 3 AND 5)
XPATH_AJ_CC_TOAST_ERROR = (
    '//*[contains(@text,"Error de registro") or '
    'contains(@content-desc,"Error de registro") or '
    'contains(@text,"Error") or contains(@content-desc,"Error")]'
)

# --- CAMBIAR COMERCIO: TEST DATA ---
# INVALID CREDENTIALS (SCREENSHOT 3)
AJ_CC_INVALID_AFILIACION = "2342423"
AJ_CC_INVALID_TOKEN      = "2343242342343242"
# FORMAT-VALID BUT NON-EXISTENT CREDENTIALS (SCREENSHOT 5)
AJ_CC_FAKE_AFILIACION    = "1234567"
AJ_CC_FAKE_TOKEN         = "1234567891234567"

# --- CERRAR SESIÓN (SCREENSHOT 6) ---
XPATH_AJ_BTN_CERRAR_SESION_MENU = (
    '//*[contains(@text,"Cerrar sesión") or '
    'contains(@content-desc,"Cerrar sesión")]'
)
# CONFIRMATION DIALOG (IF ANY)
XPATH_AJ_CERRAR_CONFIRM = (
    '//*[contains(@text,"Cerrar") or contains(@content-desc,"Cerrar") or '
    'contains(@text,"Confirmar") or contains(@content-desc,"Confirmar")]'
)
# LOGIN SCREEN IDENTIFIER (SCREENSHOT 6 — AFTER LOGOUT)
XPATH_AJ_LOGIN_SCREEN_AFTER_LOGOUT = (
    '//*[@text="Iniciar sesión" or @content-desc="Iniciar sesión" or '
    'contains(@text,"Ingresa tu correo") or contains(@content-desc,"Ingresa tu correo")]'
)

# --- CONFIGURAR NUEVAMENTE (LECTOR SETUP FROM SETTINGS) ---
XPATH_AJ_BTN_CONFIGURAR_NUEVAMENTE = (
    '//*[contains(@text,"Configurar nuevamente") or '
    'contains(@content-desc,"Configurar nuevamente")]'
)
# LECTOR SETUP SCREEN IDENTIFIER
XPATH_AJ_LECTOR_SETUP_SCREEN = (
    '//*[contains(@text,"Lector") or contains(@content-desc,"Lector") or '
    'contains(@text,"configurar") or contains(@content-desc,"configurar") or '
    'contains(@text,"cifrado") or contains(@content-desc,"cifrado")]'
)

# ==================================================================================
# [PP] T6 MOBILE — XPATHS & DATA: PINPAD (AJUSTES → SERVIDOR PINPAD)
# ==================================================================================
# FLOW   : Ajustes → sección "PinPad" → "Servidor PinPad" → pantalla "PinPad"
# OPTIONS: Servidor activo (toggle) | Configuración | Protector PinPad |
#          Comandos recibidos | Horarios de actualizaciones

# --- AJUSTES: PINPAD SECTION ---
# FLUTTER MERGES THE SECTION HEADER INTO THE ROW:
#   content-desc = "PinPad\nServidor PinPad\nEnciéndelo para recibir comandos del PinPad"
XPATH_PP_SECTION_PINPAD = (
    '//*[@text="PinPad" or @content-desc="PinPad" or '
    'starts-with(@content-desc,"PinPad")]'
)
XPATH_PP_BTN_SERVIDOR_PINPAD = (
    '//*[contains(@text,"Servidor PinPad") or '
    'contains(@content-desc,"Servidor PinPad")]'
)
# STATUS WHEN THE SERVER IS ON
XPATH_PP_STATUS_RECIBIENDO = (
    '//*[contains(@text,"Recibiendo comandos") or '
    'contains(@content-desc,"Recibiendo comandos")]'
)
# STATUS WHEN THE SERVER IS OFF (DEFAULT AFTER A FRESH INSTALL)
XPATH_PP_STATUS_ENCIENDELO = (
    '//*[contains(@text,"Enciéndelo") or '
    'contains(@content-desc,"Enciéndelo")]'
)

# --- PINPAD SCREEN ---
# SERVER OFF: ONLY THE SERVER ROW IS SHOWN ("Servidor inactivo").
# SERVER ON : "Servidor activo" + "Escuchando en <IP>:8080" + 4 OPTIONS.
XPATH_PP_SCREEN_TITLE = '//*[@text="PinPad" or @content-desc="PinPad"]'
XPATH_PP_SERVIDOR_ACTIVO = (
    '//*[contains(@text,"Servidor activo") or '
    'contains(@content-desc,"Servidor activo")]'
)
XPATH_PP_SERVIDOR_INACTIVO = (
    '//*[contains(@text,"Servidor inactivo") or '
    'contains(@content-desc,"Servidor inactivo")]'
)
XPATH_PP_ESCUCHANDO = (
    '//*[contains(@text,"Escuchando en") or '
    'contains(@content-desc,"Escuchando en")]'
)
XPATH_PP_BTN_CONFIGURACION = (
    '//*[@text="Configuración" or @content-desc="Configuración" or '
    'starts-with(@content-desc,"Configuración")]'
)
XPATH_PP_BTN_PROTECTOR = (
    '//*[contains(@text,"Protector PinPad") or '
    'contains(@content-desc,"Protector PinPad")]'
)
XPATH_PP_BTN_COMANDOS = (
    '//*[contains(@text,"Comandos recibidos") or '
    'contains(@content-desc,"Comandos recibidos")]'
)
XPATH_PP_BTN_HORARIOS = (
    '//*[contains(@text,"Horarios de actualizaciones") or '
    'contains(@content-desc,"Horarios de actualizaciones")]'
)

# --- CONFIGURACIÓN SCREEN ---
XPATH_PP_CFG_IMPRESION = (
    '//*[contains(@text,"Impresión automática") or '
    'contains(@content-desc,"Impresión automática")]'
)
XPATH_PP_CFG_CANCELACIONES = (
    '//*[contains(@text,"Cancelaciones y devoluciones") or '
    'contains(@content-desc,"Cancelaciones y devoluciones")]'
)
XPATH_PP_CFG_COMPARTIR = (
    '//*[contains(@text,"Compartir ticket") or '
    'contains(@content-desc,"Compartir ticket")]'
)
XPATH_PP_CFG_INTERNET_USB = (
    '//*[contains(@text,"Obtener internet por cable USB") or '
    'contains(@content-desc,"Obtener internet por cable USB")]'
)

# --- COMANDOS RECIBIDOS SCREEN ---
XPATH_PP_CMD_SCREEN_TITLE = XPATH_PP_BTN_COMANDOS
XPATH_PP_CMD_PINPAD_STARTED = (
    '//*[contains(@text,"PINPAD_STARTED") or '
    'contains(@content-desc,"PINPAD_STARTED")]'
)
XPATH_PP_CMD_BTN_LIMPIAR = '//*[@text="Limpiar" or @content-desc="Limpiar"]'

# --- HORARIOS DE ACTUALIZACIONES SCREEN ---
XPATH_PP_UPD_SCREEN_TITLE = '//*[@text="Actualizaciones" or @content-desc="Actualizaciones"]'
XPATH_PP_UPD_DESCRIPCION = (
    '//*[contains(@text,"Configura los horarios") or '
    'contains(@content-desc,"Configura los horarios")]'
)
XPATH_PP_UPD_HORA_INICIO = (
    '//*[contains(@text,"Hora de inicio") or '
    'contains(@content-desc,"Hora de inicio")]'
)
XPATH_PP_UPD_HORA_FIN = (
    '//*[contains(@text,"Hora de fin") or '
    'contains(@content-desc,"Hora de fin")]'
)
XPATH_PP_UPD_BTN_CONFIRMAR = '//*[@text="Confirmar" or @content-desc="Confirmar"]'
XPATH_PP_UPD_BTN_CANCELAR  = '//*[@text="Cancelar" or @content-desc="Cancelar"]'

# --- TIME PICKER BOTTOM SHEET ---
XPATH_PP_PICKER_SHEET = (
    '//*[contains(@text,"Selecciona la hora") or '
    'contains(@content-desc,"Selecciona la hora")]'
)

# --- TEST DATA ---
PP_EXPECTED_PORT       = "8080"
PP_DEFAULT_HORA_INICIO = "12:00 AM"
PP_DEFAULT_HORA_FIN    = "02:00 AM"


# ==================================================================================
# [MSI] T6 MOBILE — XPATHS & DATA: COBRO CON MESES SIN INTERESES (Operationals_MSI)
# ==================================================================================
# FLOW: Inicio → monto → "Realizar cobro" → "Leyendo tarjeta..." →
#       [monto >= umbral] "¿Cuántas mensualidades?" → "Ingresa tu PIN en el lector" →
#       "Transacción aprobada" → "Aceptar" → Inicio ($0.00)
# MATRIX: Automatizacion/T6/v2/Matrices/Matriz_Operationals_MSI.xlsx

# --- INICIO / CALCULADORA ---
XPATH_MSI_BTN_REALIZAR_COBRO = (
    '//*[contains(@content-desc,"Realizar cobro") or '
    'contains(@text,"Realizar cobro")]'
)
XPATH_MSI_INICIO = (
    '//*[contains(@content-desc,"INGRESA LA CANTIDAD") or '
    'contains(@text,"INGRESA LA CANTIDAD")]'
)
# OLDER BUILDS ASK "¿Qué tipo de operación?" BEFORE READING THE CARD (OPTIONAL)
XPATH_MSI_BTN_VENTA_NORMAL = (
    '//*[contains(@content-desc,"Venta Normal") or contains(@text,"Venta Normal")]'
)

# --- LECTURA DE TARJETA ---
XPATH_MSI_LEYENDO_TARJETA = (
    '//*[contains(@content-desc,"Leyendo tarjeta") or '
    'contains(@text,"Leyendo tarjeta")]'
)

# --- HOJA "¿CUÁNTAS MENSUALIDADES?" ---
# NOTE: LOWERCASE "mensualidades" — THE PIN SUMMARY USES "Mensualidades" (CAPITAL M)
XPATH_MSI_SHEET_TITULO = (
    '//*[contains(@content-desc,"ntas mensualidades") or '
    'contains(@text,"ntas mensualidades") or '
    'contains(@content-desc,"Selecciona la opci") or '
    'contains(@text,"Selecciona la opci")]'
)
XPATH_MSI_OPC_SIN_MENSUALIDADES = (
    '//*[contains(@content-desc,"Sin mensualidades") or '
    'contains(@text,"Sin mensualidades")]'
)
XPATH_MSI_OPC_6MSI = (
    '//*[contains(@content-desc,"6 meses sin intereses") or '
    'contains(@text,"6 meses sin intereses")]'
)
XPATH_MSI_SHEET_CANCELAR = '//*[@content-desc="Cancelar" or @text="Cancelar"]'

# --- PANTALLA DE PIN ---
XPATH_MSI_PANTALLA_PIN = (
    '//*[contains(@content-desc,"Ingresa tu PIN") or '
    'contains(@text,"Ingresa tu PIN")]'
)
XPATH_MSI_PIN_BTN_ACEPTAR = '//*[@content-desc="Aceptar" or @text="Aceptar"]'

# --- RESULTADO ---
XPATH_MSI_APROBADA = (
    '//*[contains(@content-desc,"Transacción aprobada") or '
    'contains(@text,"Transacción aprobada")]'
)
XPATH_MSI_BTN_ACEPTAR = '//*[@content-desc="Aceptar" or @text="Aceptar"]'
XPATH_MSI_BTN_FINALIZAR = '//*[@content-desc="Finalizar" or @text="Finalizar"]'

# --- TEST DATA (AMOUNTS IN PESOS; THE KEYPAD FILLS CENTS FIRST: 1000 → $10.00) ---
MSI_UMBRAL           = "1000.00"   # RULE: 6 MSI OFFERED FROM THIS AMOUNT (TC-MSI-004 CONFIRMS >= vs >)
MSI_MONTO_CONTADO    = "500.00"    # TC-MSI-001
MSI_MONTO_UMBRAL     = "1000.00"   # TC-MSI-002 / 004
MSI_MONTO_DEBAJO     = "999.99"    # TC-MSI-003
MSI_MONTO_ARRIBA     = "1000.01"   # TC-MSI-005
MSI_MONTO_ALTO       = "5000.00"   # TC-MSI-006
MSI_MONTO_SIN_MENS   = "1500.00"   # TC-MSI-008
MSI_MENSUALIDADES    = "6"
MSI_TIEMPO_TARJETA   = 90          # SECONDS TO INSERT THE CARD (MANUAL)
MSI_TIEMPO_NIP       = 180         # SECONDS TO ENTER THE PIN (MANUAL, ~3 MIN)
