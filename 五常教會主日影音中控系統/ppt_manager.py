# -*- coding: utf-8 -*-
"""
五常教會 PowerPoint 雙螢幕投影自動化模組
使用 win32com 自動啟動簡報並全螢幕放映至延伸螢幕（投影機）
"""

import os
import subprocess

current_pres = None
ppt_app = None

def get_ppt_app():
    global ppt_app
    try:
        import win32com.client
        try:
            ppt_app = win32com.client.GetActiveObject("PowerPoint.Application")
        except Exception:
            ppt_app = win32com.client.Dispatch("PowerPoint.Application")
        ppt_app.Visible = True
        return ppt_app
    except Exception as e:
        print(f"無法載入 win32com: {e}")
        return None

def start_slideshow(pptx_path, log_callback=print):
    """開啟指定簡報並全螢幕放映至延伸螢幕"""
    global current_pres
    if not os.path.exists(pptx_path):
        log_callback(f"[錯誤] 找不到簡報檔案：{pptx_path}")
        return False

    app = get_ppt_app()
    if app:
        try:
            log_callback(f"正在載入簡報: {os.path.basename(pptx_path)} ...")
            current_pres = app.Presentations.Open(os.path.abspath(pptx_path), WithWindow=True)
            log_callback("啟動全螢幕放映 (投影至延伸螢幕)...")
            current_pres.SlideShowSettings.Run()
            log_callback("[成功] 簡報已全螢幕投影放映！")
            return True
        except Exception as e:
            log_callback(f"[錯誤] PowerPoint 放映失敗: {e}")
            # 備援直接調用系統關聯程式開啟
            os.startfile(pptx_path)
            log_callback("已透過系統預設程式開啟簡報，請按 F5 放映。")
            return True
    else:
        # 備援開啟
        os.startfile(pptx_path)
        log_callback("已開啟簡報，請於 PowerPoint 中按 F5 開始放映。")
        return True

def next_slide(log_callback=print):
    global current_pres, ppt_app
    try:
        app = get_ppt_app()
        if app and app.SlideShowWindows.Count > 0:
            app.SlideShowWindows(1).View.Next()
            log_callback("簡報 -> 下一頁")
            return True
        elif current_pres and current_pres.SlideShowWindow:
            current_pres.SlideShowWindow.View.Next()
            log_callback("簡報 -> 下一頁")
            return True
    except Exception:
        pass

    # 備援：向放映視窗送出空白鍵
    hwnd = find_ppt_slideshow_hwnd()
    if hwnd:
        import time, win32api, win32con
        focus_slideshow(log_callback)
        win32api.keybd_event(win32con.VK_SPACE, 0, 0, 0)
        time.sleep(0.015)
        win32api.keybd_event(win32con.VK_SPACE, 0, win32con.KEYEVENTF_KEYUP, 0)
        log_callback("簡報 -> 下一頁")
        return True
    return False

def prev_slide(log_callback=print):
    global current_pres, ppt_app
    try:
        app = get_ppt_app()
        if app and app.SlideShowWindows.Count > 0:
            app.SlideShowWindows(1).View.Previous()
            log_callback("簡報 -> 上一頁")
            return True
        elif current_pres and current_pres.SlideShowWindow:
            current_pres.SlideShowWindow.View.Previous()
            log_callback("簡報 -> 上一頁")
            return True
    except Exception:
        pass

    # 備援：向放映視窗送出 PageUp
    hwnd = find_ppt_slideshow_hwnd()
    if hwnd:
        import time, win32api, win32con
        focus_slideshow(log_callback)
        win32api.keybd_event(win32con.VK_PRIOR, 0, 0, 0)
        time.sleep(0.015)
        win32api.keybd_event(win32con.VK_PRIOR, 0, win32con.KEYEVENTF_KEYUP, 0)
        log_callback("簡報 -> 上一頁")
        return True
    return False

def goto_slide(slide_index, log_callback=print):
    """跳轉至指定投影片頁碼並確保放映視窗具備鍵盤焦點 (雙引擎保證)"""
    global current_pres, ppt_app
    target_idx = int(slide_index)
    jumped = False

    # 確保 COM 跨線程正常運作
    try:
        import pythoncom
        pythoncom.CoInitialize()
    except Exception:
        pass

    # 方法 A：透過 PowerPoint COM API 精確跳頁
    try:
        app = get_ppt_app()
        if app and app.SlideShowWindows.Count > 0:
            ssw = app.SlideShowWindows(1)
            ssw.View.GotoSlide(target_idx)
            try:
                ssw.Activate()
            except Exception:
                pass
            jumped = True
            log_callback(f"[PPT 投影] 簡報已跳至第 {target_idx} 頁！")
        elif current_pres and current_pres.SlideShowWindow:
            current_pres.SlideShowWindow.View.GotoSlide(target_idx)
            try:
                current_pres.SlideShowWindow.Activate()
            except Exception:
                pass
            jumped = True
            log_callback(f"[PPT 投影] 簡報已跳至第 {target_idx} 頁！")
    except Exception as e:
        pass

    # 方法 B：若 COM 未跳頁成功，透過 PowerPoint 原生指令 [頁碼 + Enter] 秒跳
    try:
        hwnd = find_ppt_slideshow_hwnd()
        if hwnd:
            focus_slideshow(log_callback=log_callback)
            if not jumped:
                import time, win32api, win32con
                time.sleep(0.04)
                for ch in str(target_idx):
                    vk = ord(ch)
                    win32api.keybd_event(vk, 0, 0, 0)
                    time.sleep(0.015)
                    win32api.keybd_event(vk, 0, win32con.KEYEVENTF_KEYUP, 0)
                time.sleep(0.02)
                win32api.keybd_event(win32con.VK_RETURN, 0, 0, 0)
                time.sleep(0.015)
                win32api.keybd_event(win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0)
                log_callback(f"[PPT 投影] 簡報已透過指令跳至第 {target_idx} 頁！")
                jumped = True
    except Exception as e:
        pass

    return jumped

def force_focus_window(hwnd):
    """突破 Windows 焦點限制，強制將鍵盤輸入焦點指定給目標視窗 (絕不送出 ALT 避免干擾放映)"""
    try:
        import win32process, win32gui, win32api, win32con
        if not hwnd or not win32gui.IsWindow(hwnd):
            return False

        cur_thread = win32api.GetCurrentThreadId()
        fg_hwnd = win32gui.GetForegroundWindow()
        fg_thread = 0
        if fg_hwnd and win32gui.IsWindow(fg_hwnd):
            fg_thread, _ = win32process.GetWindowThreadProcessId(fg_hwnd)
        target_thread, _ = win32process.GetWindowThreadProcessId(hwnd)

        # 1. 綁定線程輸入隊列 (AttachThreadInput) 賦予調用 SetForegroundWindow 的合法權限
        if fg_thread and fg_thread != target_thread:
            try:
                win32process.AttachThreadInput(fg_thread, target_thread, True)
            except Exception:
                pass
        try:
            win32process.AttachThreadInput(cur_thread, target_thread, True)
        except Exception:
            pass

        # 2. 激活視窗並設置焦點 (不送出 ALT 鍵，避免觸發 Office KeyTips)
        win32gui.BringWindowToTop(hwnd)
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        win32gui.SetForegroundWindow(hwnd)
        win32gui.SetFocus(hwnd)

        # 3. 解除線程綁定
        try:
            win32process.AttachThreadInput(cur_thread, target_thread, False)
        except Exception:
            pass
        if fg_thread and fg_thread != target_thread:
            try:
                win32process.AttachThreadInput(fg_thread, target_thread, False)
            except Exception:
                pass
        return True
    except Exception:
        return False

def find_ppt_slideshow_hwnd():
    """尋找目前正在放映中的 PowerPoint 視窗 HWND"""
    try:
        import win32gui
        # 1. 優先尋找 screenClass (全螢幕放映專用視窗)
        hwnd = win32gui.FindWindow("screenClass", None)
        if hwnd and win32gui.IsWindow(hwnd):
            return hwnd

        # 2. 透過 COM 尋找 SlideShowWindow.HWND
        try:
            app = get_ppt_app()
            if app and app.SlideShowWindows.Count > 0:
                return app.SlideShowWindows(1).HWND
        except Exception:
            pass

        # 3. 備援尋找 PPTFrameClass (PowerPoint 視窗)
        hwnd = win32gui.FindWindow("PPTFrameClass", None)
        if hwnd and win32gui.IsWindow(hwnd):
            return hwnd
    except Exception:
        pass
    return 0

def focus_slideshow(log_callback=print):
    """將鍵盤焦點歸還給 PowerPoint 放映視窗，確保後續按 Enter 或數字鍵無縫響應"""
    global current_pres, ppt_app
    # 1. 優先透過 PowerPoint COM API 啟用放映視窗
    try:
        app = get_ppt_app()
        if app and app.SlideShowWindows.Count > 0:
            app.SlideShowWindows(1).Activate()
    except Exception:
        pass

    # 2. 透過 Windows 頂級強制回焦 (AttachThreadInput + 解除 Lock)
    hwnd = find_ppt_slideshow_hwnd()
    if hwnd:
        return force_focus_window(hwnd)
    return False

def exit_slideshow(log_callback=print):
    global current_pres
    try:
        if current_pres and current_pres.SlideShowWindow:
            current_pres.SlideShowWindow.View.Exit()
            log_callback("簡報放映已結束。")
            return True
    except Exception:
        pass
    return False
