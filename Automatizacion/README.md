[MEMPHIS]

Modular automation framework for E2E testing on Android POS (T6) terminals AND Web Platforms.
It utilizes Python + Appium (Mobile) and Selenium (Web) with an architecture based on reusable functions.

[ CORE FILES ]
* config.py
  Global file that centralizes all project constants.
  Contains Appium Capabilities, Web URLs, test credentials, and XPaths for both Mobile and Web.

* utils.py
  Abstraction layer that wraps native interactions (click, send_keys, waits).
  - iniciar_driver(): Starts Android session.
  - iniciar_driver_web(): Starts Chrome session using WebDriver Manager.

* T6
  Specific code for testing the T6 terminal flow on Memphis. 

* WEB 
  Specific suite for testing the Web Authentication flow on Memphis FAT environment.

[ HOW TO RUN ]
1. Mobile: python Operacionales_LG.py
2. Web: python Web/Web_Login.py