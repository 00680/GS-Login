# GSLogin — Build & Packaging Guide

## English

**Project Description:**
- GSLogin is a GUI application that automates login flows using Playwright (includes Firefox support). This repository contains the source under `src/` and build helpers for creating a standalone Windows executable with PyInstaller.

**Prerequisites:**
- Python 3.8+ and pip
- A virtual environment (recommended)
- `PyInstaller` installed in the environment
- `playwright` Python package to download browser runtimes

**Quick setup:**
- Create and activate a virtual environment (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

- Install Python dependencies:

```powershell
pip install -r requirements.txt
pip install PyInstaller
```

**Prepare Playwright Firefox browsers (recommended):**
- Use the helper script to install Firefox into `resources/playwright_browsers`:

```powershell
.\scripts\install_playwright_browsers.ps1
```

- This sets `PLAYWRIGHT_BROWSERS_PATH` to `resources\playwright_browsers` and runs `playwright install firefox` using the `.venv` Python if available.

**Build the executable with PyInstaller:**
- The project includes a spec at [gslogin.spec](gslogin.spec) that bundles the `playwright_browsers` data and uses a runtime hook to set `PLAYWRIGHT_BROWSERS_PATH` at startup.

Run the build from the project root:

```powershell
python -m PyInstaller --clean --noconfirm gslogin.spec
```

- Default behavior: builds a one-file EXE named `GSLogin.exe` (located in `dist` when complete).

**Runtime notes:**
- The runtime hook is `runtime_hooks/set_playwright_browsers_path.py` and will set `PLAYWRIGHT_BROWSERS_PATH` automatically when the app runs from the bundled archive (`_MEIPASS`).
- You can override or set the browser path manually by exporting `PLAYWRIGHT_BROWSERS_PATH` before running the app.
- Useful env vars:
  - `PLAYWRIGHT_BROWSERS_PATH`: folder containing Playwright browser runtimes
  - `GSLOGIN_CONSOLE=1`: enable console logging for debugging
  - `GSLOGIN_DISABLE_LOG=1`: disable logging entirely

**Debugging builds:**
- For easier inspection, change the spec to build `ONEFILE = False` or run PyInstaller with a one-folder build. This leaves browser files and runtime hooks as regular files on disk.

**Where to look:**
- Spec: [gslogin.spec](gslogin.spec)
- Runtime hook: [runtime_hooks/set_playwright_browsers_path.py](runtime_hooks/set_playwright_browsers_path.py)
- Playwright helper: [scripts/install_playwright_browsers.ps1](scripts/install_playwright_browsers.ps1)

## 繁體中文（Traditional Chinese）

**專案說明：**
- GSLogin 是一個使用 Playwright（含 Firefox）來自動化登入流程的桌面應用程式。本專案的原始碼位於 `src/`，並包含使用 PyInstaller 打包成 Windows 可執行檔的相關輔助工具。

**先決條件：**
- 安裝 Python 3.8 以上與 pip
- 建議使用虛擬環境
- 在環境中安裝 `PyInstaller`
- 安裝 `playwright` 套件以下載瀏覽器執行檔

**快速設定步驟：**
- 建立並啟用虛擬環境（PowerShell 範例）：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

- 安裝相依套件：

```powershell
pip install -r requirements.txt
pip install PyInstaller
```

**準備 Playwright Firefox 瀏覽器：**
- 建議使用專案內的安裝腳本，將 Firefox 安裝到 `resources/playwright_browsers`：

```powershell
.\scripts\install_playwright_browsers.ps1
```

- 此腳本會把 `PLAYWRIGHT_BROWSERS_PATH` 設為 `resources\playwright_browsers`，並使用 `.venv` 的 Python 執行 `playwright install firefox`。

**使用 PyInstaller 建置：**
- 專案包含一個位於 [gslogin.spec](gslogin.spec) 的 spec，會將 `playwright_browsers` 相關資料打包，並在啟動時透過 runtime hook 設定 `PLAYWRIGHT_BROWSERS_PATH`。

於專案根目錄執行：

```powershell
python -m PyInstaller --clean --noconfirm gslogin.spec
```

- 預設會產生一個名為 `GSLogin.exe` 的單一檔案（完成後位於 `dist` 資料夾）。

**執行時要點：**
- runtime hook 位於 `runtime_hooks/set_playwright_browsers_path.py`，在打包為可執行檔後會自動設定 `PLAYWRIGHT_BROWSERS_PATH` 指向解壓出的 `playwright_browsers`。
- 若要手動覆寫，請在執行程式前設定環境變數 `PLAYWRIGHT_BROWSERS_PATH`。
- 常用環境變數：
  - `PLAYWRIGHT_BROWSERS_PATH`：Playwright 瀏覽器執行檔所在資料夾
  - `GSLOGIN_CONSOLE=1`：啟用主控台日誌以便除錯
  - `GSLOGIN_DISABLE_LOG=1`：完全關閉日誌

**除錯建議：**
- 若要方便檢視打包內容，請在 spec 將 `ONEFILE` 設為 `False` 或以 one-folder 方式打包，這樣檔案會以資料夾形式保留在磁碟上。

---
