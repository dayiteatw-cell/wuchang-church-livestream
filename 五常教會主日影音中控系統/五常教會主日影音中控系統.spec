# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['E:/Antigravity_Data/五常教會直播設置/五常教會主日影音中控系統/main_gui.py'],
    pathex=[],
    binaries=[],
    datas=[('E:/Antigravity_Data/五常教會直播設置/五常教會主日影音中控系統/scrcpy', 'scrcpy'), ('E:/Antigravity_Data/五常教會直播設置/五常教會主日影音中控系統/assets', 'assets')],
    hiddenimports=['win32com', 'win32com.client', 'pythoncom', 'win32gui', 'win32con', 'win32api', 'PIL', 'PIL.ImageTk', 'window_layout_manager'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='五常教會主日影音中控系統',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['E:/Antigravity_Data/五常教會直播設置/五常教會主日影音中控系統/assets/app_icon_v3.ico'],
)
