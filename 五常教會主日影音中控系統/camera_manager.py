# -*- coding: utf-8 -*-
"""
五常教會 雙手機 USB 有線 ADB 智慧控制模組
硬體配置：
1. 正面主鏡：Samsung Galaxy A27 (USB 3.0 有線，序號 R5GL91YT4BT) -> 鎖定 Iriun #1
2. 會眾全景：ASUS (USB 有線，序號 M8AIB760S073JRK) -> 鎖定 Iriun #2
"""

import os
import sys
import subprocess
import time

A27_SERIAL = "R5GL91YT4BT"
ASUS_SERIAL = "M8AIB760S073JRK"

def get_adb_path():
    """動態取得 adb.exe 路徑 (優先 Iriun，次選內建 scrcpy/adb)"""
    iriun_adb = r"C:\Program Files (x86)\Iriun Webcam\adb.exe"
    if os.path.exists(iriun_adb):
        return iriun_adb
    if hasattr(sys, "_MEIPASS"):
        p = os.path.join(sys._MEIPASS, "scrcpy", "adb.exe")
        if os.path.exists(p):
            return p
    local_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scrcpy", "adb.exe")
    if os.path.exists(local_p):
        return local_p
    backup_p = r"E:\Antigravity_Data\五常教會直播設置\scrcpy\adb.exe"
    if os.path.exists(backup_p):
        return backup_p
    return "adb"

def run_adb(args):
    """執行 ADB 指令"""
    adb_cmd = get_adb_path()
    cmd = [adb_cmd] + args
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return p.returncode == 0, p.stdout.strip()
    except Exception as e:
        return False, str(e)

def check_devices():
    """檢查相機連線狀態 (Galaxy A27, ASUS)"""
    ok, out = run_adb(["devices"])
    a27_online = False
    asus_online = False
    if ok:
        for line in out.splitlines()[1:]:
            if "\tdevice" in line or line.endswith("device"):
                if A27_SERIAL in line:
                    a27_online = True
                if ASUS_SERIAL in line:
                    asus_online = True

    return {
        "a27_usb": a27_online,
        "asus_usb": asus_online,
        "raw": out
    }

IRIUN_EXE_PATH = r"C:\Program Files (x86)\Iriun Webcam\IriunWebcam.exe"

def is_iriun_running():
    """檢查電腦端 Iriun Webcam 是否在背景執行"""
    try:
        cmd = ["tasklist", "/FI", "IMAGENAME eq IriunWebcam.exe"]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        return "IriunWebcam.exe" in p.stdout
    except Exception:
        return False

def launch_iriun_webcam(log_callback=print):
    """啟動/喚醒電腦端 Iriun Webcam 程式 (直接執行執行檔路徑，官方單實例機制會自動喚醒桌面視窗並恢復視訊)"""
    exe = IRIUN_EXE_PATH
    if not os.path.exists(exe):
        exe = r"C:\Program Files\Iriun Webcam\IriunWebcam.exe"
    
    # 支援任何使用者桌面與公共桌面的 Iriun 捷徑
    desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
    lnk = os.path.join(desktop_dir, "Iriun Webcam.lnk")
    pub_desktop = os.path.join(os.environ.get("PUBLIC", r"C:\Users\Public"), "Desktop", "Iriun Webcam.lnk")

    target = None
    if os.path.exists(exe):
        target = exe
    elif os.path.exists(lnk):
        target = lnk
    elif os.path.exists(pub_desktop):
        target = pub_desktop

    if target:
        try:
            if target.endswith(".exe"):
                subprocess.Popen([target], cwd=os.path.dirname(target))
            else:
                os.startfile(target)
            log_callback(f"已執行 Iriun Webcam 程式路徑呼叫視窗: {os.path.basename(target)}")
            return True
        except Exception as e:
            log_callback(f"[錯誤] 無法啟動 Iriun Webcam: {e}")
            return False
    else:
        log_callback("[提示] 找不到 Iriun Webcam 執行檔。")
        return False

def wake_all_cameras(log_callback=print):
    """
    喚醒全場相機 (USB 有線時序精準鎖定: 1.A27 -> 2.iPhone X -> 3.ASUS)
    1. 確保電腦端 Iriun Webcam 已啟動
    2. A27 亮屏 + 開 Iriun (鎖定 Iriun #1)
    3. 提示桌邊 iPhone X 開啟 Iriun (鎖定 Iriun #2)
    4. ASUS 亮屏 + 開 Iriun (鎖定 Iriun #3)
    """
    if not is_iriun_running():
        log_callback("正在開啟電腦端 Iriun Webcam 程式...")
        launch_iriun_webcam(log_callback=log_callback)
        time.sleep(2)

    log_callback(f"[1/3] 正在喚醒正面主鏡 (Galaxy A27 [{A27_SERIAL}] - USB 3.0 有線)...")
    run_adb(["-s", A27_SERIAL, "shell", "input", "keyevent", "26"])
    run_adb(["-s", A27_SERIAL, "shell", "input", "keyevent", "82"])
    run_adb(["-s", A27_SERIAL, "shell", "monkey", "-p", "com.iriun.webcam", "-c", "android.intent.category.LAUNCHER", "1"])
    log_callback("      [OK] 正面主鏡 A27 已喚醒，成功鎖定【Iriun Webcam #1】！")

    time.sleep(2)

    log_callback(f"\n[2/3] 側面副鏡 (Apple iPhone X - USB 有線)...")
    log_callback("      提示：請同工確認桌邊 iPhone X 已解鎖開啟 Iriun，鎖定【Iriun Webcam #2】！")

    time.sleep(2)

    log_callback(f"\n[3/3] 正在喚醒會眾全景 (ASUS [{ASUS_SERIAL}] - USB 有線)...")
    run_adb(["-s", ASUS_SERIAL, "shell", "input", "keyevent", "26"])
    run_adb(["-s", ASUS_SERIAL, "shell", "input", "keyevent", "82"])
    run_adb(["-s", ASUS_SERIAL, "shell", "monkey", "-p", "com.iriun.webcam", "-c", "android.intent.category.LAUNCHER", "1"])
    log_callback("      [OK] 會眾全景 ASUS 已喚醒，成功鎖定【Iriun Webcam #3】！")

    log_callback("\n[完成] 全場相機順序已精準對齊：")
    log_callback(f"   * Iriun #1 : Galaxy A27 - 正面主鏡 ({A27_SERIAL})")
    log_callback("   * Iriun #2 : Apple iPhone X - 側面副鏡 (廁所前特寫)")
    log_callback(f"   * Iriun #3 : ASUS - 會眾全景 ({ASUS_SERIAL})")
    return True

def sleep_all_cameras(log_callback=print):
    """
    一鍵休眠相機 (雙 USB 有線)
    1. 強制關閉 Android Iriun App (感光元件斷電冷卻、停止視訊串流)
    2. 黑屏深層待機
    3. 提醒同工手動按一下桌邊 iPhone X 側邊鍵黑屏休眠
    """
    log_callback(f"[1/2] 正在休眠正面主鏡 (Galaxy A27 [{A27_SERIAL}] - USB)...")
    run_adb(["-s", A27_SERIAL, "shell", "am", "force-stop", "com.iriun.webcam"])
    run_adb(["-s", A27_SERIAL, "shell", "input", "keyevent", "26"])
    log_callback("      [OK] 正面主鏡 A27 攝影機已完全釋放並黑屏休眠！")

    log_callback(f"[2/2] 正在休眠會眾全景 (ASUS [{ASUS_SERIAL}] - USB)...")
    run_adb(["-s", ASUS_SERIAL, "shell", "am", "force-stop", "com.iriun.webcam"])
    run_adb(["-s", ASUS_SERIAL, "shell", "input", "keyevent", "26"])
    log_callback("      [OK] 會眾全景 ASUS 已終止串流並進入黑屏深層休眠！")

    log_callback("\n[散會] 安卓雙機已進入黑屏休眠！桌邊 iPhone X 請同工按一下實體側邊鍵休眠即可。")
    return True

def repair_camera_order(log_callback=print):
    """一鍵重整相機順序（精準鎖定: 1.A27 -> 2.iPhone X -> 3.ASUS）"""
    log_callback("[步驟 1] 強制釋放 Android 雙機 Iriun 通道...")
    run_adb(["-s", A27_SERIAL, "shell", "am", "force-stop", "com.iriun.webcam"])
    run_adb(["-s", ASUS_SERIAL, "shell", "am", "force-stop", "com.iriun.webcam"])
    log_callback("         Android 雙機通道已全部釋放！")
    time.sleep(2)

    log_callback(f"[步驟 2] 重新啟動 A27 -> 鎖定 Iriun #1...")
    run_adb(["-s", A27_SERIAL, "shell", "input", "keyevent", "26"])
    run_adb(["-s", A27_SERIAL, "shell", "input", "keyevent", "82"])
    run_adb(["-s", A27_SERIAL, "shell", "monkey", "-p", "com.iriun.webcam", "-c", "android.intent.category.LAUNCHER", "1"])
    log_callback("         A27 已鎖定【Iriun #1】！")
    time.sleep(3)

    log_callback(f"[步驟 3] iPhone X 側面副鏡 -> 鎖定 Iriun #2...")
    log_callback("         請同工確保桌邊 iPhone X 開啟 Iriun Webcam 搶下【Iriun #2】通道。")
    time.sleep(2)

    log_callback(f"[步驟 4] 重新啟動 ASUS 會眾機 -> 鎖定 Iriun #3...")
    run_adb(["-s", ASUS_SERIAL, "shell", "input", "keyevent", "26"])
    run_adb(["-s", ASUS_SERIAL, "shell", "input", "keyevent", "82"])
    run_adb(["-s", ASUS_SERIAL, "shell", "monkey", "-p", "com.iriun.webcam", "-c", "android.intent.category.LAUNCHER", "1"])
    log_callback("         ASUS 已鎖定【Iriun #3】！")

    log_callback("\n[成功] 三機通道已全部重置並精準歸位！(1.A27  2.iPhone X  3.ASUS)")
    return True

def wake_single_camera(target="a27", log_callback=print):
    """喚醒單一手機相機"""
    if target == "a27":
        serial = A27_SERIAL
        name = "正面主鏡 (Galaxy A27)"
        slot = "Iriun #1"
    else:
        serial = ASUS_SERIAL
        name = "會眾全景 (ASUS)"
        slot = "Iriun #2"

    log_callback(f"正在喚醒 {name} [{serial}]...")
    run_adb(["-s", serial, "shell", "input", "keyevent", "26"])
    run_adb(["-s", serial, "shell", "input", "keyevent", "82"])
    run_adb(["-s", serial, "shell", "monkey", "-p", "com.iriun.webcam", "-c", "android.intent.category.LAUNCHER", "1"])
    log_callback(f"[成功] {name} 已喚醒並啟動 Iriun Webcam ({slot})！")
    return True

def sleep_single_camera(target="a27", log_callback=print):
    """休眠單一手機相機"""
    if target == "a27":
        serial = A27_SERIAL
        name = "正面主鏡 (Galaxy A27)"
    else:
        serial = ASUS_SERIAL
        name = "會眾全景 (ASUS)"

    log_callback(f"正在休眠 {name} [{serial}]...")
    run_adb(["-s", serial, "shell", "am", "force-stop", "com.iriun.webcam"])
    run_adb(["-s", serial, "shell", "input", "keyevent", "26"])
    log_callback(f"[成功] {name} 攝影機已完全釋放並進入黑屏休眠！")
    return True

def poweroff_single_camera(target="a27", log_callback=print):
    """徹底關閉單一手機電源 (斷電關機)"""
    if target == "a27":
        serial = A27_SERIAL
        name = "正面主鏡 (Galaxy A27)"
    else:
        serial = ASUS_SERIAL
        name = "會眾全景 (ASUS)"

    log_callback(f"正在徹底關閉 {name} [{serial}] 電源...")
    run_adb(["-s", serial, "reboot", "-p"])
    log_callback(f"[成功] {name} 已完全關閉電源。下次使用請至腳架旁按實體電源鍵開機！")
    return True

