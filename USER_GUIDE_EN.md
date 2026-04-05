# GSLogin — User Guide (English)

This short guide explains how to use the GSLogin GUI to configure accounts, game folders, and start automated logins.

1. Accounts (Account page)
- Open the Account page in the application.
- Click Add / New to create a new account entry.
- Fill in the following fields (required):
  - Username: your account name or email. (required)
  - Password: the account password. (required)
  - OTP / 2FA: enter the account's OTP secret key (TOTP/HOTP shared secret). The app uses this secret to generate one-time codes automatically; do not enter a single-use one-time code here. (required)
Save the account. You can add multiple accounts and edit or remove them later.

2. CapSolver API Key (Settings page)
- Open the Settings page.
- Locate the CapSolver / captcha solver API key field.
- Paste your CapSolver API key and save settings. This enables automated captcha solving when required.

3. Game Folders (Process page)
- Open the Process page (or the page that manages game folders/processes).
- Use the Add Folder / Browse button to open a file dialog and select the local game installation folder(s).
- Each selected folder will be listed; you can add multiple game folders.

4. Running the Login Automation
- On the Process page, select the target game folder from the folder list.
- Select one of your configured accounts from the account selector.
- Press the Run / Start button to launch the automated login process.
- The application will launch the game/browser and attempt the configured login using the selected account and folder. Monitor logs or on-screen status for progress and errors.

Notes
 - For TW accounts that require an OTP, provide the account's OTP secret key in the OTP field so the app can generate one-time codes. If you prefer not to store the secret, you may be prompted to enter a one-time code at runtime.
 - Ensure the CapSolver API key is valid if captchas are expected; otherwise manual captcha interaction may be required.
- If Playwright browser runtimes are required, follow the build/readme instructions to prepare `PLAYWRIGHT_BROWSERS_PATH` or install browsers via the helper script.

Troubleshooting
 - If login fails, check the application log output and confirm account credentials and folder path are correct.
- Check network connectivity and any antivirus/OS restrictions that may block automated browser control.
