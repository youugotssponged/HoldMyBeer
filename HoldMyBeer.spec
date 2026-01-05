# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# Collect all submodules of pyperclipimg (in case it has dynamic imports)
hiddenimports = collect_submodules('pyperclipimg')

# Collect data files for pyperclipimg if needed
datas = collect_data_files('pyperclipimg')

block_cipher = None

a = Analysis(
    ['HoldMyBeer.py'],         # your script
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='HoldMyBeerScreenshot',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,   # No console window
    icon='HMB.ico'  # Replace with your icon file path or remove this line
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='HoldMyBeerScreenshot'
)