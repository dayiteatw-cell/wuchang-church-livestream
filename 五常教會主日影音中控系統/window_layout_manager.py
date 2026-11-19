# -*- coding: utf-8 -*-
"""
五常教會 主日視窗一鍵排版歸位模組 (Window Layout Manager)
專為五常教會主日影音同工操作螢幕設計的自動化視窗佈局系統。

標準版面分配（螢幕 1 操作螢幕）：
1. 【右半側】 (50% 寬 x 100% 高)：PowerPoint 簡報者檢視畫面 (Presenter View) 置頂於右半側
2. 【左上格】 (50% 寬 x 50% 高)：同步歌詞瀏覽器 (Chrome / Edge / Firefox)
3. 【懸浮導航視窗】 (480x158 置頂白框圓邊)：置頂於左下格右上方 (PPT_Sync_Navigator)
4. 【左下格】 (50% 寬 x 50% 高)：相機畫面監控 (Iriun Webcam 或 scrcpy A27 + ASUS 雙機)
5. 【中控台主畫面】：自動最小化至工作列，清空操作視野
"""

import sys
import time

try:
    import win32gui
    import win32con
    import win32api
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False


def ensure_default_desktop():
    """確保目前執行緒切換至使用者互動桌面 (default)，以利在背景排程或測試環境中操作視窗"""
    try:
        import ctypes
        user32 = ctypes.windll.user32
        hDesk = user32.OpenDesktopW("default", 0, False, 0x10000000)
        if hDesk:
            user32.SetThreadDesktop(hDesk)
    except Exception:
        pass


def get_primary_monitor_work_area():
    """
    動態取得主操作螢幕 (螢幕 1) 之工作區座標與長寬 (扣除 Windows 工作列)
    返回: (work_x, work_y, work_w, work_h, half_w, half_h)
    """
    if not HAS_WIN32:
        return 0, 0, 1920, 1080, 960, 540

    try:
        ensure_default_desktop()
        primary_mon = win32api.MonitorFromPoint((0, 0))
        mon_info = win32api.GetMonitorInfo(primary_mon)
        work_rect = mon_info.get("Work", (0, 0, 1707, 912))
        wx, wy, wr, wb = work_rect
        ww = max(800, wr - wx)
        wh = max(600, wb - wy)
        half_w = ww // 2
        half_h = wh // 2
        return wx, wy, ww, wh, half_w, half_h
    except Exception:
        return 0, 0, 1707, 912, 853, 456


def is_real_iriun_main_window(h):
    """精確判斷是否為 Iriun Webcam 視訊主視窗，嚴格排除 WPF 內部通知視窗與輔助視窗"""
    if not HAS_WIN32 or not h or not win32gui.IsWindow(h):
        return False
    title = win32gui.GetWindowText(h).strip()
    if not title:
        return False
    # 主視窗標題必為 "Iriun Webcam" 開頭 (例如 "Iriun Webcam v2.9.9" 或 "Iriun Webcam")
    if not title.startswith("Iriun Webcam"):
        return False
    # 嚴格排除 WPF 內部通知視窗與 GDI+ 勾點視窗
    if any(k in title for k in ["Notify", "Context", "GDI+", "Event", "Resource", "System"]):
        return False
    return True


def apply_window_round_corners(hwnd, width, height, radius=26):
    """Win32 GDI API 為視窗套用四角平滑圓邊 (現代圓角視窗)"""
    if not HAS_WIN32 or not hwnd or not win32gui.IsWindow(hwnd):
        return False
    try:
        import ctypes
        gdi32 = ctypes.windll.gdi32
        user32 = ctypes.windll.user32
        hrgn = gdi32.CreateRoundRectRgn(0, 0, int(width) + 1, int(height) + 1, int(radius), int(radius))
        if hrgn:
            user32.SetWindowRgn(hwnd, hrgn, True)
            return True
    except Exception:
        pass
    return False


def safe_restore_and_move(hwnd, x, y, w, h, topmost=False, round_radius=0):
    """安全還原並重設目標視窗大小與位置 (自動處理最小化或最大化狀態，可選圓角)"""
    if not HAS_WIN32 or not hwnd or not win32gui.IsWindow(hwnd):
        return False

    try:
        cls = win32gui.GetClassName(hwnd)
        title = win32gui.GetWindowText(hwnd)
        is_iriun = ("HwndWrapper" in cls) or ("Iriun" in title)

        import ctypes
        user32 = ctypes.windll.user32

        is_zoomed = bool(user32.IsZoomed(hwnd))
        is_iconic = bool(user32.IsIconic(hwnd))
        placement = win32gui.GetWindowPlacement(hwnd)

        # 1. 確保視窗徹底脫離「最大化」與「最小化」狀態
        # 特別處理 Chrome 等瀏覽器：當視窗曾最大化再縮小至工作列 (placement[0] 帶有 WPF_RESTORETOMAXIMIZED = 2)，
        # 若呼叫 SW_RESTORE 會使 Windows 自動將其還原為「全螢幕最大化」並鎖定尺寸，導致排版無效！
        # 故一律先以 SW_SHOWNORMAL (1) 強制以標準大小還原視窗；若仍處於 Zoomed 則發送 SC_RESTORE。
        if is_zoomed or is_iconic or placement[1] in (win32con.SW_SHOWMINIMIZED, win32con.SW_SHOWMAXIMIZED) or (placement[0] & 2):
            user32.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
            if user32.IsZoomed(hwnd):
                user32.SendMessageW(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
        else:
            win32gui.ShowWindow(hwnd, win32con.SW_SHOW)

        # Iriun Webcam (WPF Direct3D 視訊表面) 必須使用純淨的 MoveWindow 移動縮放，絕不可呼叫 RedrawWindow，避免覆蓋黑底
        if is_iriun:
            win32gui.MoveWindow(hwnd, int(x), int(y), int(w), int(h), True)
            win32gui.BringWindowToTop(hwnd)
            return True

        flags = win32con.SWP_SHOWWINDOW
        z_order = win32con.HWND_TOPMOST if topmost else win32con.HWND_TOP
        win32gui.SetWindowPos(hwnd, z_order, int(x), int(y), int(w), int(h), flags)

        # 雙重防護：若定位後視窗仍被系統鎖定為最大化 (某些瀏覽器分頁非同步回應)，再次發送 SC_RESTORE 並重新定位
        if user32.IsZoomed(hwnd):
            user32.SendMessageW(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
            win32gui.SetWindowPos(hwnd, z_order, int(x), int(y), int(w), int(h), flags)

        win32gui.BringWindowToTop(hwnd)

        # 非 Iriun 視窗才呼叫 RedrawWindow 確保介面重繪
        win32gui.RedrawWindow(hwnd, None, None, win32con.RDW_INVALIDATE | win32con.RDW_UPDATENOW | win32con.RDW_ALLCHILDREN)
        if round_radius > 0:
            apply_window_round_corners(hwnd, w, h, radius=round_radius)
        return True
    except Exception:
        return False


def minimize_other_windows(keep_hwnds, wx, wy, ww, wh, log_callback=print):
    """
    排版前將操作螢幕 (螢幕 1) 上的所有其他無關工作視窗全部最小化
    (如: PowerPoint 編輯主視窗、其他瀏覽器分頁/視窗、檔案總管、LINE、記事本等)
    - 絕不最小化已定位的四象限目標視窗 (keep_hwnds)
    - 絕不最小化投影在螢幕 2 (會堂投影幕) 的 PowerPoint 全螢幕放映視窗
    - 絕不干擾 Windows 系統底層列或桌面
    """
    if not HAS_WIN32:
        return 0

    ensure_default_desktop()

    ignore_classes = {
        "Shell_TrayWnd", "Shell_SecondaryTrayWnd", "Progman", "WorkerW",
        "Windows.UI.Core.CoreWindow", "TopLevelWindowForOverflowXamlIsland",
        "CEF-OSC-WIDGET", "EdgeUiInputWndClass", "XamlExplorerHostIslandWindow"
    }

    to_minimize = []

    def enum_cb(h, _):
        if h in keep_hwnds:
            return True
        if not win32gui.IsWindow(h) or not win32gui.IsWindowVisible(h):
            return True
        if win32gui.IsIconic(h):
            return True
        if win32gui.GetParent(h) != 0:
            return True
        owner = win32gui.GetWindow(h, win32con.GW_OWNER)
        if owner != 0 and owner in keep_hwnds:
            return True
        cls = win32gui.GetClassName(h)
        if cls in ignore_classes:
            return True
        title = win32gui.GetWindowText(h).strip()
        if not title:
            return True
        # 嚴格保護 Iriun Webcam 相關的所有視窗與其 WPF 內部通知管線，絕不最小化
        title_lower = title.lower()
        cls_lower = cls.lower()
        if "iriun" in title_lower or "iriun" in cls_lower or "mediacontext" in title_lower or "systemresource" in title_lower:
            return True
        # 嚴格保護會堂投影幕 (螢幕 2) 之全螢幕投影片放映
        if cls == "screenClass" or "投影片放映" in title or "Slide Show" in title:
            return True
        rect = win32gui.GetWindowRect(h)
        w = rect[2] - rect[0]
        h_dim = rect[3] - rect[1]
        if w <= 100 or h_dim <= 100:
            return True
        # 僅最小化主操作螢幕 (螢幕 1) 上的視窗，延伸螢幕 (會堂投影) 視窗絕不觸碰
        cx = (rect[0] + rect[2]) // 2
        if cx < wx or cx >= wx + ww:
            return True
        ex_style = win32gui.GetWindowLong(h, win32con.GWL_EXSTYLE)
        WS_EX_APPWINDOW = 0x00040000
        if (ex_style & win32con.WS_EX_TOOLWINDOW) and not (ex_style & WS_EX_APPWINDOW):
            return True
        to_minimize.append((h, title))
        return True

    try:
        win32gui.EnumWindows(enum_cb, None)
    except Exception as e:
        log_callback(f"[最小化提示] 列舉視窗發生例外: {e}")

    minimized_count = 0
    for h, title in to_minimize:
        try:
            win32gui.ShowWindow(h, win32con.SW_MINIMIZE)
            minimized_count += 1
        except Exception:
            pass

    if minimized_count > 0:
        log_callback(f"  [清空桌面] 已自動最小化 {minimized_count} 個其他背景工作視窗，保持操作視野純淨。")
        time.sleep(0.08)

    return minimized_count


def find_target_windows():
    """
    精準定位主日所需之所有關聯視窗：
    - lyrics: 標題含「同步歌詞」的瀏覽器視窗
    - presenter: PowerPoint 簡報者檢視畫面 (Presenter View)
    - ppt_editor: PowerPoint 主視窗 (若尚未進入簡報者檢視模式)
    - navigator: PPT 歌詞懸浮導航視窗 (PPT_Sync_Navigator)
    - iriun: Iriun Webcam 視訊視窗
    - scrcpy_a27: 正面主鏡 A27 手機投影
    - scrcpy_asus: 會眾全景 ASUS 手機投影
    """
    if not HAS_WIN32:
        return {}

    ensure_default_desktop()

    found = {
        "lyrics": None,
        "presenter": None,
        "ppt_editor": None,
        "navigator": None,
        "iriun": None,
        "scrcpy_a27": None,
        "scrcpy_asus": None,
    }

    def enum_cb(h, _):
        if not win32gui.IsWindow(h):
            return True

        title = win32gui.GetWindowText(h)
        cls = win32gui.GetClassName(h)

        # 1. 同步歌詞瀏覽器
        if ("同步歌詞" in title or "sync-lyrics" in title.lower()) and not found["lyrics"]:
            found["lyrics"] = (h, title)

        # 2. PowerPoint 簡報者檢視畫面 (Presenter View)
        elif ("簡報者檢視畫面" in title or "Presenter View" in title) and not found["presenter"]:
            found["presenter"] = (h, title)

        # 3. PowerPoint 主視窗 (備援)
        elif ("PowerPoint" in title or cls == "PPTFrameClass") and not found["presenter"] and not found["ppt_editor"]:
            # 排除投影在延伸螢幕 (Monitor 2, x >= 2000) 的投影片全螢幕放映視窗
            rect = win32gui.GetWindowRect(h)
            if rect[0] < 2000 and "投影片放映" not in title:
                found["ppt_editor"] = (h, title)

        # 4. 原生置頂懸浮導航視窗
        elif title == "PPT_Sync_Navigator" and not found["navigator"]:
            found["navigator"] = (h, title)

        # 5. Iriun Webcam 視訊主視窗 (嚴格排除所有 WPF 內部輔助視窗)
        elif is_real_iriun_main_window(h) and not found["iriun"]:
            found["iriun"] = (h, title)

        # 6. scrcpy 正面主鏡 A27
        elif ("A27" in title or "正面主鏡" in title) and ("會眾全景" not in title) and not found["scrcpy_a27"]:
            found["scrcpy_a27"] = (h, title)

        # 7. scrcpy 會眾全景 ASUS
        elif ("ASUS" in title or "會眾全景" in title) and ("正面主鏡" not in title) and not found["scrcpy_asus"]:
            found["scrcpy_asus"] = (h, title)

        return True

    win32gui.EnumWindows(enum_cb, None)
    return found


def ensure_iriun_on_desktop(log_callback=print):
    """
    確保 Iriun Webcam 視窗從工作列隱藏通知區/最小化跳出至桌面。
    與手動點擊「開啟 Iriun Webcam」按鈕完全一致：直接呼叫 launch_iriun_webcam 執行路徑！
    不使用任何可能干擾 Direct3D 視訊表面之外部 API。
    """
    if not HAS_WIN32:
        return None

    ensure_default_desktop()

    from camera_manager import launch_iriun_webcam
    launch_iriun_webcam(log_callback=log_callback)
    time.sleep(0.5)

    main_hwnd = None
    def cb(h, _):
        nonlocal main_hwnd
        if is_real_iriun_main_window(h):
            main_hwnd = h
        return True

    win32gui.EnumWindows(cb, None)
    return main_hwnd


def confirm_preflight_checklist(parent=None):
    """
    排版前置作業檢核對話框 (提示詞美化版)
    提醒同工確認：
    1. OBS 串流與 YouTube 直播已開始
    2. Iriun Webcam 視訊與手機通道鎖定
    """
    import tkinter as tk
    from tkinter import messagebox

    try:
        # 建立專屬頂層模態對話視窗
        dlg = tk.Toplevel(parent) if parent and hasattr(parent, "winfo_exists") and parent.winfo_exists() else tk.Toplevel()
        dlg.title("五常基督長老教會 • 主日開場檢核清單")
        dlg.attributes("-topmost", True)
        dlg.configure(bg="#F8FAFC")

        w, h = 560, 310
        sw = dlg.winfo_screenwidth()
        sh = dlg.winfo_screenheight()
        dlg.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        dlg.resizable(False, False)

        if parent and hasattr(parent, "winfo_exists") and parent.winfo_exists():
            dlg.transient(parent)

        result = {"confirmed": False}

        def _do_confirm(event=None):
            result["confirmed"] = True
            dlg.destroy()

        def _do_cancel(event=None):
            result["confirmed"] = False
            dlg.destroy()

        dlg.protocol("WM_DELETE_WINDOW", _do_cancel)
        dlg.bind("<Return>", _do_confirm)
        dlg.bind("<KP_Enter>", _do_confirm)
        dlg.bind("<Escape>", _do_cancel)

        # 頂部形象標題列 (湖水綠底)
        hdr = tk.Frame(dlg, bg="#0D9488", padx=18, pady=12)
        hdr.pack(fill="x")
        tk.Label(
            hdr,
            text="📋 主日直播開場 • 前置作業檢核清單",
            font=("微軟正黑體", 13, "bold"),
            fg="white",
            bg="#0D9488"
        ).pack(anchor="w")
        tk.Label(
            hdr,
            text="排版執行後中控台將自動最小化，請確認以下關鍵設備與串流均已就緒：",
            font=("微軟正黑體", 9),
            fg="#CCFBF1",
            bg="#0D9488"
        ).pack(anchor="w", pady=(3, 0))

        # 中間白色清單卡片
        card = tk.Frame(dlg, bg="#FFFFFF", highlightbackground="#CBD5E1", highlightthickness=1)
        card.pack(fill="both", expand=True, padx=16, pady=12)

        # 檢核項 1: OBS 與 YouTube 直播
        i1 = tk.Frame(card, bg="#FFFFFF")
        i1.pack(fill="x", padx=14, pady=(10, 6))
        tk.Label(i1, text="📡 1. OBS 串流與 YouTube 直播已正式開始", font=("微軟正黑體", 10, "bold"), fg="#1E3A8A", bg="#FFFFFF").pack(anchor="w")
        tk.Label(
            i1,
            text="   • 請確認 OBS 已經點擊【開始串流】(綠燈穩定連線中)\n   • 請確認 YouTube 直播後台狀態顯示【正在直播】(影音訊號正常傳送)",
            font=("微軟正黑體", 9),
            fg="#475569",
            bg="#FFFFFF",
            justify="left"
        ).pack(anchor="w", padx=8, pady=(2, 0))

        # 檢核項 2: Iriun Webcam 與 手機序號對齊 (1.A27  2.iPhone X  3.ASUS)
        i2 = tk.Frame(card, bg="#FFFFFF")
        i2.pack(fill="x", padx=14, pady=(6, 12))
        tk.Label(i2, text="📷 2. Iriun Webcam 視訊與手機通道鎖定 (1.A27  2.iPhone X  3.ASUS)", font=("微軟正黑體", 10, "bold"), fg="#0D9488", bg="#FFFFFF").pack(anchor="w")
        tk.Label(
            i2,
            text="   • 【Iriun Webcam #1】 ➔ Samsung Galaxy A27 (正面主鏡 [R5GL91YT4BT])\n"
                 "   • 【Iriun Webcam #2】 ➔ Apple iPhone X (側面副鏡 - 廁所前特寫機位)\n"
                 "   • 【Iriun Webcam #3】 ➔ ASUS (會眾全景 [M8AIB760S073JRK])",
            font=("微軟正黑體", 9),
            fg="#475569",
            bg="#FFFFFF",
            justify="left"
        ).pack(anchor="w", padx=8, pady=(2, 0))

        # 底部操作按鈕列
        btn_bar = tk.Frame(dlg, bg="#F8FAFC")
        btn_bar.pack(fill="x", padx=16, pady=(0, 14))

        b_ok = tk.Button(
            btn_bar,
            text="✅ 確認全部就緒，開始排版 (Enter)",
            font=("微軟正黑體", 10, "bold"),
            bg="#0D9488",
            fg="white",
            activebackground="#0F766E",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=16,
            pady=7,
            cursor="hand2",
            command=_do_confirm
        )
        b_ok.pack(side="right", padx=(8, 0))

        b_cancel = tk.Button(
            btn_bar,
            text="稍後再排 (Esc)",
            font=("微軟正黑體", 10),
            bg="#E2E8F0",
            fg="#334155",
            activebackground="#CBD5E1",
            activeforeground="#334155",
            relief="flat",
            bd=0,
            padx=14,
            pady=7,
            cursor="hand2",
            command=_do_cancel
        )
        b_cancel.pack(side="right")

        try:
            dlg.grab_set()
        except Exception:
            pass
        b_ok.focus_set()
        dlg.wait_window()

        return result["confirmed"]

    except Exception:
        # 降級備援：系統原生訊息視窗
        title = "主日直播開場前置檢核"
        msg = (
            "【📋 主日直播開場前置作業檢核】\n\n"
            "排版執行後中控台將自動最小化至工作列。\n"
            "請同工確認以下關鍵項目均已就緒：\n\n"
            "📡 1. OBS 串流與 YouTube 直播：\n"
            "    • OBS 已按下【開始串流】\n"
            "    • YouTube 後台狀態顯示【正在直播】(綠燈傳輸中)\n\n"
            "📷 2. Iriun Webcam 視訊與手機通道鎖定 (1.A27  2.iPhone X  3.ASUS)：\n"
            "    • Iriun #1 : 正面主鏡 (Galaxy A27 [R5GL91YT4BT])\n"
            "    • Iriun #2 : 側面副鏡 (Apple iPhone X)\n"
            "    • Iriun #3 : 會眾全景 (ASUS [M8AIB760S073JRK])\n\n"
            "是否確認全部就緒，立即開始自動排版？"
        )
        return messagebox.askyesno(title, msg)


def snap_sunday_layout(app_instance=None, log_callback=print, skip_confirm=False):
    """
    一鍵自動排版歸位核心函式
    將當前螢幕 1 上的視窗精準排版為四象限標準配置：
    - 右半側: PowerPoint 簡報者檢視畫面
    - 左上格: 同步歌詞瀏覽器
    - 左下格右上方: 懸浮導航視窗 (白色外框 + 四角圓邊置頂)
    - 左下格: Iriun Webcam 與 scrcpy 相機畫面
    - 中控台: 最小化至工作列
    """
    if not HAS_WIN32:
        log_callback("[排版歸位] ⚠️ 僅支援 Windows 系統排版。")
        return False

    # 若未略過確認，先彈出前置檢核清單對話框
    if not skip_confirm:
        parent = getattr(app_instance, "root", None)
        if not confirm_preflight_checklist(parent=parent):
            log_callback("[排版歸位] 同工已取消排版作業。")
            return False

    log_callback("=" * 60)
    log_callback("📐 正在執行【主日視窗一鍵自動排版歸位】...")

    # 1. 取得操作螢幕工作區尺寸
    wx, wy, ww, wh, half_w, half_h = get_primary_monitor_work_area()
    log_callback(f"偵測到操作螢幕 (螢幕 1) 工作區: {ww} x {wh} (半寬: {half_w}, 半高: {half_h})")

    # 2. 尋找所有關聯視窗 (若 Iriun 尚未在桌面則執行路徑喚醒)
    wins = find_target_windows()
    if not wins.get("iriun"):
        iriun_h = ensure_iriun_on_desktop(log_callback=log_callback)
        if iriun_h:
            wins["iriun"] = (iriun_h, "Iriun Webcam")

    arranged_count = 0

    # ---------------- 區塊 1: 【右半側】 (PowerPoint 簡報者檢視畫面) ----------------
    # 規格: x = half_w, y = 0, w = ww - half_w, h = wh
    right_x = wx + half_w
    right_y = wy
    right_w = ww - half_w
    right_h = wh

    target_ppt_h = None
    target_ppt_name = ""
    if wins.get("presenter"):
        target_ppt_h, target_ppt_name = wins["presenter"]
    elif wins.get("ppt_editor"):
        target_ppt_h, target_ppt_name = wins["ppt_editor"]

    # 建立四象限目標視窗保護清單 (keep_hwnds)
    keep_hwnds = set()
    if target_ppt_h:
        keep_hwnds.add(target_ppt_h)
    if wins.get("lyrics"):
        keep_hwnds.add(wins["lyrics"][0])
    if wins.get("navigator"):
        keep_hwnds.add(wins["navigator"][0])
    if app_instance and hasattr(app_instance, "lyrics_mgr"):
        lm = app_instance.lyrics_mgr
        if lm.navigator_window and hasattr(lm.navigator_window, "root") and lm.navigator_window.root:
            try:
                keep_hwnds.add(lm.navigator_window.root.winfo_id())
            except Exception:
                pass
    if wins.get("iriun"):
        keep_hwnds.add(wins["iriun"][0])
    if wins.get("scrcpy_a27"):
        keep_hwnds.add(wins["scrcpy_a27"][0])
    if wins.get("scrcpy_asus"):
        keep_hwnds.add(wins["scrcpy_asus"][0])
    if app_instance and hasattr(app_instance, "root") and app_instance.root:
        try:
            keep_hwnds.add(app_instance.root.winfo_id())
        except Exception:
            pass

    # 【排版前置清理】將主操作螢幕 (螢幕 1) 上的所有其他無關工作視窗全部最小化
    # 徹底清除 PPT 編輯視窗、背景瀏覽器、檔案總管等雜訊，保持排版後四象限乾淨純粹
    minimize_other_windows(keep_hwnds, wx, wy, ww, wh, log_callback=log_callback)

    if target_ppt_h:
        safe_restore_and_move(target_ppt_h, right_x, right_y, right_w, right_h, topmost=False)
        log_callback(f"  [1/4] 【右半側 50%】已定位: {target_ppt_name} ({right_w}x{right_h})")
        arranged_count += 1
    else:
        log_callback("  [1/4] 【右半側】提示：尚未偵測到 PowerPoint 簡報者檢視畫面 (放映後可再次點選排版)")

    # ---------------- 區塊 2: 【左上格】 (同步歌詞瀏覽器) ----------------
    # 規格: x = 0, y = 0, w = half_w, h = half_h
    tl_x = wx
    tl_y = wy
    tl_w = half_w
    tl_h = half_h

    if wins.get("lyrics"):
        lyr_h, lyr_title = wins["lyrics"]
        safe_restore_and_move(lyr_h, tl_x, tl_y, tl_w, tl_h, topmost=False)
        log_callback(f"  [2/4] 【左上格 25%】已定位: {lyr_title} ({tl_w}x{tl_h})")
        arranged_count += 1
    else:
        log_callback("  [2/4] 【左上格】提示：未偵測到「同步歌詞」瀏覽器視窗 (可按步驟 4 開啟雲端歌詞)")

    # ---------------- 區塊 3: 【懸浮導航視窗】 (置頂於左下格右上方，白框圓邊) ----------------
    # 規格: 置頂懸浮於左下格 (相機畫面) 的右上方，避開 Iriun 標題列，寬 480，高 158 (充足高度不遮擋按鈕)
    bl_x = wx
    bl_y = wy + half_h
    bl_w = half_w
    bl_h = wh - half_h

    nav_w = min(480, bl_w - 20)
    nav_h = 158
    nav_x = bl_x + bl_w - nav_w - 12  # 緊鄰左下格右側交界 (留 12px 留白)
    nav_y = bl_y + 30                 # 避開 Iriun Webcam 視窗標題列

    # 若中控系統實例存在，優先透過實例控制懸浮導航視窗
    if app_instance and hasattr(app_instance, "lyrics_mgr"):
        lm = app_instance.lyrics_mgr
        if not (lm.navigator_window and lm.navigator_window.is_alive()):
            # 若尚未開啟則自動啟動
            app_instance.btn_start_lyrics_nav()
            time.sleep(0.1)

        if lm.navigator_window and lm.navigator_window.is_alive():
            lm.navigator_window.snap_to_bottom_left_top_right(wx, wy, half_w, half_h)
            log_callback(f"  [3/4] 【左下格右上方】懸浮導航視窗已置頂歸位 (白色外框 + 四角圓邊 @ {nav_x},{nav_y})")
            arranged_count += 1
    elif wins.get("navigator"):
        nav_h_win, nav_title = wins["navigator"]
        safe_restore_and_move(nav_h_win, nav_x, nav_y, nav_w, nav_h, topmost=True, round_radius=26)
        log_callback(f"  [3/4] 【左下格右上方】已定位: {nav_title} (白色外框 + 四角圓邊 @ {nav_x},{nav_y})")
        arranged_count += 1

    # ---------------- 區塊 4: 【左下格】 (相機畫面: Iriun 或 scrcpy 雙機) ----------------
    # 規格: x = 0, y = half_h, w = half_w, h = wh - half_h
    bl_x = wx
    bl_y = wy + half_h
    bl_w = half_w
    bl_h = wh - half_h

    cam_count = 0
    scrcpy_a27 = wins.get("scrcpy_a27")
    scrcpy_asus = wins.get("scrcpy_asus")
    iriun_win = wins.get("iriun")

    # 若 scrcpy 雙機同時開啟：左右並排分切左下格
    if scrcpy_a27 and scrcpy_asus:
        sub_w1 = bl_w // 2
        sub_w2 = bl_w - sub_w1
        safe_restore_and_move(scrcpy_a27[0], bl_x, bl_y, sub_w1, bl_h, topmost=False)
        safe_restore_and_move(scrcpy_asus[0], bl_x + sub_w1, bl_y, sub_w2, bl_h, topmost=False)
        log_callback(f"  [4/4] 【左下格 25%】雙機 scrcpy 已並排歸位: A27 ({sub_w1}x{bl_h}) + ASUS ({sub_w2}x{bl_h})")
        cam_count += 2
        arranged_count += 2
    elif scrcpy_a27:
        safe_restore_and_move(scrcpy_a27[0], bl_x, bl_y, bl_w, bl_h, topmost=False)
        log_callback(f"  [4/4] 【左下格 25%】已定位 A27 scrcpy 視窗 ({bl_w}x{bl_h})")
        cam_count += 1
        arranged_count += 1
    elif scrcpy_asus:
        safe_restore_and_move(scrcpy_asus[0], bl_x, bl_y, bl_w, bl_h, topmost=False)
        log_callback(f"  [4/4] 【左下格 25%】已定位 ASUS scrcpy 視窗 ({bl_w}x{bl_h})")
        cam_count += 1
        arranged_count += 1

    # 若有 Iriun Webcam 視窗
    if iriun_win:
        safe_restore_and_move(iriun_win[0], bl_x, bl_y, bl_w, bl_h, topmost=False)
        log_callback(f"  [4/4] 【左下格 25%】已定位 Iriun Webcam 視窗 ({bl_w}x{bl_h})")
        cam_count += 1
        arranged_count += 1

    if cam_count == 0:
        log_callback("  [4/4] 【左下格】提示：未偵測到相機視窗 (Iriun 或 scrcpy 未開啟)")

    # ---------------- 區塊 5: 【中控台主畫面最小化】 ----------------
    if app_instance and hasattr(app_instance, "root"):
        def _minimize():
            try:
                app_instance.root.iconify()
                log_callback("  [5/5] 【中控台主畫面】已自動最小化至工作列，清空操作視野！")
            except Exception:
                pass
        # 延遲 350ms 最小化，讓同工能清楚看見日誌完成提示
        app_instance.root.after(350, _minimize)

    log_callback("=" * 60)
    log_callback(f"🎉【排版完成】共已精準歸位 {arranged_count} 個視窗！同工可直接操作投影片與詩歌。")
    return True


def dock_presenter_view_to_right(log_callback=print, app_root=None):
    """
    將 PowerPoint 簡報者檢視畫面自動移至螢幕 1 右半側 50%，
    徹底解除全螢幕最大化狀態，絕不遮蓋中控台主程式視野！
    """
    if not HAS_WIN32:
        return False

    ensure_default_desktop()
    wx, wy, ww, wh, half_w, half_h = get_primary_monitor_work_area()
    right_x = wx + half_w
    right_y = wy
    right_w = ww - half_w
    right_h = wh

    presenter_hwnd = None
    presenter_title = ""

    # 等待 PowerPoint 簡報者檢視視窗生成 (最多嘗試 15 次，約 3 秒)
    for _ in range(15):
        time.sleep(0.2)
        def cb(h, _):
            nonlocal presenter_hwnd, presenter_title
            if not win32gui.IsWindow(h) or not win32gui.IsWindowVisible(h):
                return True
            title = win32gui.GetWindowText(h)
            rect = win32gui.GetWindowRect(h)
            # 確保是在操作螢幕 (螢幕 1, rect[0] < ww) 上的簡報者檢視畫面，排除延伸螢幕投影放映
            if rect[0] < ww and ("簡報者檢視畫面" in title or "Presenter View" in title):
                presenter_hwnd = h
                presenter_title = title
            return True

        win32gui.EnumWindows(cb, None)
        if presenter_hwnd:
            break

    # 若未找到專屬簡報者檢視畫面，尋找螢幕 1 上的 PowerPoint 主視窗作為備援
    if not presenter_hwnd:
        def cb_backup(h, _):
            nonlocal presenter_hwnd, presenter_title
            if not win32gui.IsWindow(h) or not win32gui.IsWindowVisible(h):
                return True
            title = win32gui.GetWindowText(h)
            cls = win32gui.GetClassName(h)
            rect = win32gui.GetWindowRect(h)
            if rect[0] < ww and ("PowerPoint" in title or cls == "PPTFrameClass") and "投影片放映" not in title:
                presenter_hwnd = h
                presenter_title = title
            return True
        win32gui.EnumWindows(cb_backup, None)

    if presenter_hwnd:
        safe_restore_and_move(presenter_hwnd, right_x, right_y, right_w, right_h, topmost=False)
        log_callback(f"[PPT 投影] 簡報檢視畫面已自動就位至右半側 ({right_w}x{right_h})，不遮蔽主程式！")

        # 同步將中控台主程式提至前景，確保同工操作視野完全通透
        if app_root and hasattr(app_root, "lift"):
            try:
                app_root.after(100, lambda: app_root.lift())
                app_root.after(150, lambda: app_root.focus_force())
            except Exception:
                pass
        return True

    return False


def dock_lyrics_view_to_top_left(log_callback=print, app_root=None):
    """
    開啟雲端歌詞時，自動將瀏覽器視窗移至螢幕 1 左上格 (50% 寬 x 50% 高)，
    徹底解除全螢幕最大化狀態，絕不蓋住中控台主程式視野！
    """
    if not HAS_WIN32:
        return False

    ensure_default_desktop()
    wx, wy, ww, wh, half_w, half_h = get_primary_monitor_work_area()

    target_hwnd = None
    target_title = ""
    import ctypes
    user32 = ctypes.windll.user32

    # 嘗試等待瀏覽器響應並定位 (最多重試 15 次，約 3 秒)
    for _ in range(15):
        time.sleep(0.2)
        def cb(h, _):
            nonlocal target_hwnd, target_title
            if not win32gui.IsWindow(h) or not win32gui.IsWindowVisible(h):
                return True
            t = win32gui.GetWindowText(h)
            c = win32gui.GetClassName(h)
            r = win32gui.GetWindowRect(h)
            # 確保是在操作螢幕 (螢幕 1, r[0] < ww) 上的瀏覽器
            if r[0] < ww and ("Chrome_WidgetWin_1" in c or "Mozilla" in c or "Edge" in c):
                if "同步歌詞" in t or "sync-lyrics" in t.lower() or "role=display" in t.lower():
                    target_hwnd = h
                    target_title = t
                    return True
                # 若該瀏覽器處於最大化或全寬狀態，標記為候選
                if user32.IsZoomed(h) or (r[2] - r[0] >= ww - 20):
                    if not target_hwnd:
                        target_hwnd = h
                        target_title = t
            return True

        win32gui.EnumWindows(cb, None)
        if target_hwnd:
            break

    if target_hwnd:
        safe_restore_and_move(target_hwnd, wx, wy, half_w, half_h, topmost=False)
        log_callback(f"[詩歌同步] 雲端歌詞瀏覽器已自動就位至左上格 ({half_w}x{half_h})，不遮蔽主程式！")

        # 同步將中控台主程式提至前景，確保同工操作視野完全通透
        if app_root and hasattr(app_root, "lift"):
            try:
                app_root.after(80, lambda: app_root.lift())
                app_root.after(140, lambda: app_root.focus_force())
            except Exception:
                pass
        return True

    return False
