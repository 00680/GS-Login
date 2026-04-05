# -*- mode: python ; coding: utf-8 -*-
import os
from glob import glob

block_cipher = None

pathex = [os.path.abspath('.')]

# Include Playwright browsers from both `resources/playwright_browsers` and
# `vendor/playwright_browsers` so you can choose which folder to populate.
playwright_datas = []
for pw_root in [os.path.join('resources', 'playwright_browsers'), os.path.join('vendor', 'playwright_browsers')]:
    if os.path.isdir(pw_root):
        for root, dirs, files in os.walk(pw_root):
            for f in files:
                full = os.path.join(root, f)
                rel_dir = os.path.relpath(root, pw_root)
                target_dir = os.path.join('playwright_browsers', rel_dir)
                playwright_datas.append((full, target_dir))

# Runtime hook to configure bundled Playwright browser path at startup.
runtime_hooks = [os.path.join('runtime_hooks', 'set_playwright_browsers_path.py')]

a = Analysis([
    'src/main.py',
],
    pathex=pathex,
    binaries=[],
    datas=playwright_datas,
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=runtime_hooks,
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
# Build options
ONEFILE = True
UAC_ADMIN = False
DISABLE_LOGS = False

if ONEFILE:
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        exclude_binaries=False,
        name='GSLogin',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=False,
        uac_admin=UAC_ADMIN,
    )
else:
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name='GSLogin',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=False,
        uac_admin=UAC_ADMIN,
        runtime_hooks=runtime_hooks,
    )

    coll = COLLECT(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=False,
        upx=True,
        name='GSLogin',
    )
