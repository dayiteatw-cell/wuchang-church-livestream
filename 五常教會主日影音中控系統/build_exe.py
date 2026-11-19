# -*- coding: utf-8 -*-
import os
import sys
import shutil
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

pyinstaller = r"E:\Antigravity_Data\church-automation\.venv\Scripts\pyinstaller.exe"
main_script = os.path.join(BASE_DIR, "main_gui.py")

# 清理舊的建置暫存
for folder in ["build", "dist"]:
    p = os.path.join(BASE_DIR, folder)
    if os.path.exists(p):
        try:
            shutil.rmtree(p)
        except Exception:
            pass

spec_file = os.path.join(BASE_DIR, "五常教會主日影音中控系統.spec")
if os.path.exists(spec_file):
    try:
        os.remove(spec_file)
    except Exception:
        pass

scrcpy_dir = os.path.join(BASE_DIR, "scrcpy")
assets_dir = os.path.join(BASE_DIR, "assets")
icon_file = os.path.join(assets_dir, "app_icon_v3.ico")
if not os.path.exists(icon_file):
    icon_file = os.path.join(assets_dir, "app_icon.ico")

cmd = [
    pyinstaller,
    "--noconsole",
    "--onefile",
    "--name", "五常教會主日影音中控系統",
    "--icon", icon_file,
    "--add-data", f"{scrcpy_dir};scrcpy",
    "--add-data", f"{assets_dir};assets",
    "--hidden-import", "win32com",
    "--hidden-import", "win32com.client",
    "--hidden-import", "pythoncom",
    "--hidden-import", "win32gui",
    "--hidden-import", "win32con",
    "--hidden-import", "win32api",
    "--hidden-import", "PIL",
    "--hidden-import", "PIL.ImageTk",
    "--hidden-import", "window_layout_manager",
    "--clean",
    main_script
]

print("=" * 60)
print("正在使用 PyInstaller 進行單一 EXE 打包...")
print("=" * 60)
sys.stdout.flush()

res = subprocess.run(cmd)

if res.returncode == 0:
    dist_exe = os.path.join(BASE_DIR, "dist", "五常教會主日影音中控系統.exe")
    target_local = os.path.join(BASE_DIR, "五常教會主日影音中控系統.exe")
    user_desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    desktop_exe = os.path.join(user_desktop, "五常教會主日影音中控系統.exe")

    if os.path.exists(dist_exe):
        shutil.copy2(dist_exe, target_local)
        print(f"\n[OK] 已產出本地 EXE: {target_local}")
        try:
            # 若桌面執行檔正在執行中，先關閉舊進程以利覆蓋更新
            subprocess.run(["powershell", "-NoProfile", "-Command", "Stop-Process -Name '五常教會*' -Force -ErrorAction SilentlyContinue"], timeout=5)
            import time; time.sleep(0.5)
            shutil.copy2(dist_exe, desktop_exe)
            print(f"[OK] 已同步複製至桌面: {desktop_exe}")
            
            # 建立或更新桌面捷徑並強制綁定五常教會專屬 ICO 圖標
            import win32com.client
            import ctypes
            shell = win32com.client.Dispatch("WScript.Shell")
            lnk_path = os.path.join(user_desktop, "五常教會主日影音中控系統.lnk")
            shortcut = shell.CreateShortCut(lnk_path)
            shortcut.TargetPath = desktop_exe
            shortcut.WorkingDirectory = user_desktop
            shortcut.IconLocation = f"{icon_file},0"
            shortcut.Description = "五常教會主日影音與直播總控系統"
            shortcut.save()
            print(f"[OK] 已同步建立桌面捷徑並鎖定官方圖標: {lnk_path}")

            # 刷新 Windows 桌面圖示快取 (強制 FLUSH)
            ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x1000, 0, 0)
            subprocess.run(["ie4uinit.exe", "-show"], capture_output=True, timeout=3)
        except Exception as e:
            print(f"[!] 複製至桌面提示: {e}")
    print("\n================== 全部打包流程完成！ ==================")
else:
    print(f"\n[ERROR] 打包失敗，Exit Code: {res.returncode}")
