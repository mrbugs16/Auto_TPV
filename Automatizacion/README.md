[MEMPHIS]

Modular automation framework for E2E testing on Android POS (T6) terminals.
It utilizes Python + Appium with an architecture based on reusable functions 
to ensure scalability and efficient maintenance.

[ CORE FILES ]
* config.py
Global file that centralizes all project constants.
Contains Appium Desired Capabilities, test credentials (valid/invalid users), server URLs 
and the (XPaths).
* utils.py
Abstraction layer that wraps native Selenium/Appium interactions (click, send_keys, waits).
Detailed debugging logs, and smart explicit waits.
