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

2. CapSolver (captcha solving)
- What it is: GSLogin uses CapSolver through `playwright-recaptcha` to solve reCAPTCHA challenges during TW login.
- Official website: https://www.capsolver.com/zh
- Where to set it: open Settings and find the `CapSolver API Key` field.
- How to set it:
  - Copy your API key from your CapSolver dashboard.
  - Paste it into the field and save.
- Important behavior:
  - If no key is configured, captcha solving cannot run and the automated login flow will stop.
  - If the key is invalid, has no balance, or CapSolver is temporarily unavailable, captcha solving may fail and login may not complete.

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
- CapSolver requires internet access and an active CapSolver account.
- Keep your API key private. Do not share screenshots or logs that expose it.
- If Playwright browser runtimes are required, follow the build/readme instructions to prepare `PLAYWRIGHT_BROWSERS_PATH` or install browsers via the helper script.

Troubleshooting
 - If login fails, check the application log output and confirm account credentials and folder path are correct.
- Re-check the CapSolver API key in Settings (no extra spaces/newlines).
- Confirm your CapSolver account has available quota/balance.
- If captcha solving still fails intermittently, wait and retry later.
- Check network connectivity and any antivirus/OS restrictions that may block automated browser control.
