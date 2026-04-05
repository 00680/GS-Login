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

# Also include qt_material_icons resources (installed in site-packages) so
# the frozen bundle can import `qt_material_icons.resources.*` modules.
extra_datas = []
try:
    import importlib.util
    spec = importlib.util.find_spec('qt_material_icons')
    if spec and getattr(spec, 'submodule_search_locations', None):
        pkg_dir = spec.submodule_search_locations[0]
        resources_dir = os.path.join(pkg_dir, 'resources')
        if os.path.isdir(resources_dir):
            for root, dirs, files in os.walk(resources_dir):
                for f in files:
                    full = os.path.join(root, f)
                    rel_dir = os.path.relpath(root, pkg_dir)
                    target_dir = os.path.join('qt_material_icons', rel_dir)
                    extra_datas.append((full, target_dir))
except Exception:
    # If detection fails, continue without raising; user can populate manually.
    pass

# Include project icon if present (now located at `src/images/`)
icon_rel = os.path.join('src', 'images', 'icon.ico')
if os.path.exists(icon_rel):
    extra_datas.append((icon_rel, 'src/images'))

# Runtime hook to configure bundled Playwright browser path at startup.
runtime_hooks = [os.path.join('runtime_hooks', 'set_playwright_browsers_path.py')]

a = Analysis([
    'src/main.py',
],
    pathex=pathex,
    binaries=[],
    datas=playwright_datas + extra_datas,
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
UAC_ADMIN = True
DISABLE_LOGS = True

if ONEFILE:
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        exclude_binaries=False,
        name='GSLogin',
        icon=['src/images/icon.ico'],
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
        icon=['src/images/icon.ico'],
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
