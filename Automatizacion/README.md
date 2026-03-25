# [MEMPHIS]

Modular automation framework for E2E testing on Android POS (T6) terminals AND Web Platforms.
It utilizes Python + Appium (Mobile) and Selenium (Web) with an architecture based on reusable functions.

---
Marco de automatización modular para pruebas E2E en terminales Android POS (T6) Y plataformas Web.
Utiliza Python + Appium (Móvil) y Selenium (Web) con una arquitectura basada en funciones reutilizables.

---

## [ CORE FILES / ARCHIVOS PRINCIPALES ]

* **config.py**
  Global file that centralizes all project constants.
  Contains Appium Capabilities, Web URLs, test credentials, and XPaths for both Mobile and Web.
  
  ---
  Archivo global que centraliza todas las constantes del proyecto.
  Contiene Appium Capabilities, URLs Web, credenciales de prueba y XPaths tanto para Móvil como Web.

* **utils.py**
  Abstraction layer that wraps native interactions (click, send_keys, waits).
  - `iniciar_driver()`: Starts Android session.
  - `iniciar_driver_web()`: Starts Chrome session using WebDriver Manager.
  
  ---
  Capa de abstracción que envuelve interacciones nativas (click, send_keys, esperas).
  - `iniciar_driver()`: Inicia sesión Android.
  - `iniciar_driver_web()`: Inicia sesión Chrome usando WebDriver Manager.

* **T6**
  Specific code for testing the T6 terminal flow on Memphis.
  
  ---
  Código específico para probar el flujo de la terminal T6 en Memphis.

* **WEB**
  Specific suite for testing the Web Authentication flow on Memphis FAT environment.
  
  ---
  Suite específica para probar el flujo de Autenticación Web en el entorno FAT de Memphis.

---

## [ PREREQUISITES / REQUISITOS PREVIOS ]

### Appium Server

For the HTTP evidence capture to work correctly, Appium **must** be started with the relaxed security flag:

---
Para que la captura de evidencia HTTP funcione correctamente, Appium **debe** iniciarse con el flag de seguridad relajada:

```bash
# ✅ REQUIRED — Enables server log capture for HTTP evidence
# ✅ REQUERIDO — Habilita la captura de server logs para evidencia HTTP
appium --relaxed-security