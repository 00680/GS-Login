# Preparing Playwright Firefox browsers for bundling

Place Playwright browser files under one of these folders (relative to `v2`):

- `resources/playwright_browsers`
- `vendor/playwright_browsers`

Recommended: use the included PowerShell helper to download Firefox into `resources/playwright_browsers`.

PowerShell (from repo root):

```powershell
cd v2
.\scripts\install_playwright_browsers.ps1
```

Manual steps (PowerShell):

```powershell
cd v2
$env:PLAYWRIGHT_BROWSERS_PATH = (Resolve-Path resources\playwright_browsers).Path
python -m pip install --upgrade playwright
python -m playwright install firefox
```

If you already have a populated `vendor\playwright_browsers` folder (from previous builds), you can copy it into `v2\vendor\playwright_browsers` before running the PyInstaller build.

After the folder exists, build with PyInstaller using the spec at `v2/gslogin.spec`.

```powershell
cd v2
python -m PyInstaller --clean --noconfirm gslogin.spec
```
