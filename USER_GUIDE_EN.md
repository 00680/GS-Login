# GSLogin — User Guide (English)

This short guide explains how to use the GSLogin GUI to configure accounts, game folders, and start automated logins.

1. Accounts (Account page)
- Open the Account page in the application.
- Click Add / New to create a new account entry.
- Fill in the following fields:
  - Username: your account name or email.
  - Password: the account password.
  - OTP / 2FA: optional — only required for the TW server (enter one-time password if applicable).
  - Server: select the target game server from the list.
- Save the account. You can add multiple accounts and edit or remove them later.

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
- For TW server accounts that require an OTP, make sure to provide the current one-time code when creating or editing the account.
- Ensure the CapSolver API key is valid if captchas are expected; otherwise manual captcha interaction may be required.
- If Playwright browser runtimes are required, follow the build/readme instructions to prepare `PLAYWRIGHT_BROWSERS_PATH` or install browsers via the helper script.

Troubleshooting
- If login fails, check the application log output and confirm account credentials, server selection, and folder path are correct.
- Check network connectivity and any antivirus/OS restrictions that may block automated browser control.
