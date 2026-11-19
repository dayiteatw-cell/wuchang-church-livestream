# -*- coding: utf-8 -*-
"""
五常教會 主日詩歌連動與 PPT 投影片同步導航模組
支援：
1. 自動同步 Downloads/config.txt 覆蓋 E:/Antigravity_Data/sync-lyrics-app/config.txt
2. 多種文字編碼 (UTF-16LE, UTF-8-SIG, UTF-8, CP950) 解析歌名與段落頁碼 (V, V2, P, C, B, 2, E)
3. 自動開啟雲端歌詞網頁 (https://sync-lyrics-app.onrender.com/)
4. 投影同工切歌：發送 Ctrl+1, Ctrl+2, Ctrl+3 至「同步歌詞」瀏覽器視窗
5. 原生 Python 半透明置頂懸浮導航視窗 (完全取代 AHK 懸浮窗)
"""

import os
import sys
import re
import time
import shutil
import webbrowser
import threading
import tkinter as tk
from datetime import datetime

try:
    import win32gui
    import win32con
    import win32api
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False

# 雲端歌詞服務 URL (預設直接帶入 role=display 副唱/顯示端模式)
CLOUD_URL = "https://sync-lyrics-app.onrender.com/?role=display"
DOWNLOADS_DIR = os.path.join(os.path.expanduser("~"), "Downloads")
DOWNLOADS_CONFIG = os.path.join(DOWNLOADS_DIR, "config.txt")

# 跨電腦相容設定檔目錄 (優先程式所在目錄，相容原開發路徑)
APP_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
LOCAL_CONFIG = os.path.join(APP_DIR, "config.txt")
DEV_SYNC_DIR = r"E:\Antigravity_Data\sync-lyrics-app"
DEV_CONFIG = os.path.join(DEV_SYNC_DIR, "config.txt")

PART_NAME_MAP = {
    "V": "主歌",
    "V2": "主歌2",
    "P": "導歌 (Pre-Chorus)",
    "C": "副歌",
    "B": "橋段",
    "2": "後半 / 特殊段落",
    "E": "尾句 (Outro)"
}

class LyricsSyncManager:
    def __init__(self, log_callback=None):
        self.log_callback = log_callback or print
        self.app_instance = None # 關聯之中控台實例
        self.on_song_changed_callback = None # 歌曲切換回呼
        self.songs = {}          # {1: "向耶和華唱新歌", 2: "每一天我需要祢", 3: "主祢永遠與我同在"}
        self.mapping = {}        # {"1_V": ["2", "3", "4"], "3_V2": ["13"], "3_P": ["14"], ...}
        self.current_song = 1
        self.active_config_path = None
        self.last_sync_info = "尚未同步"
        self.navigator_window = None
        
        # 初始同步載入
        self.sync_and_load_config()

    def log(self, msg):
        try:
            self.log_callback(msg)
        except Exception:
            print(msg)

    def sync_and_load_config(self):
        """檢查 Downloads/config.txt，若存在則同步並載入 (全自動相容任何電腦)"""
        synced_from_downloads = False
        target_file = None

        try:
            if os.path.exists(DOWNLOADS_CONFIG):
                # 優先同步到本機程式目錄
                try:
                    shutil.copy2(DOWNLOADS_CONFIG, LOCAL_CONFIG)
                except Exception:
                    pass
                # 若開發環境目錄存在，同步備份一份
                if os.path.exists(os.path.dirname(DEV_SYNC_DIR)):
                    try:
                        os.makedirs(DEV_SYNC_DIR, exist_ok=True)
                        shutil.copy2(DOWNLOADS_CONFIG, DEV_CONFIG)
                    except Exception:
                        pass
                target_file = DOWNLOADS_CONFIG
                synced_from_downloads = True
                mtime = os.path.getmtime(DOWNLOADS_CONFIG)
                time_str = datetime.fromtimestamp(mtime).strftime("%m/%d %H:%M")
                self.last_sync_info = f"已由 Downloads 自動讀取同步 ({time_str})"
                self.log(f"[詩歌同步] 已從 Downloads 讀取最新 config.txt！({time_str})")
            elif os.path.exists(LOCAL_CONFIG):
                target_file = LOCAL_CONFIG
                mtime = os.path.getmtime(LOCAL_CONFIG)
                time_str = datetime.fromtimestamp(mtime).strftime("%m/%d %H:%M")
                self.last_sync_info = f"使用本機現有 config.txt ({time_str})"
                self.log(f"[詩歌同步] 使用本機現有 config.txt ({time_str})")
            elif os.path.exists(DEV_CONFIG):
                target_file = DEV_CONFIG
                mtime = os.path.getmtime(DEV_CONFIG)
                time_str = datetime.fromtimestamp(mtime).strftime("%m/%d %H:%M")
                self.last_sync_info = f"使用專案既有 config.txt ({time_str})"
                self.log(f"[詩歌同步] 使用專案現有 config.txt ({time_str})")
            else:
                self.last_sync_info = "未找到 config.txt"
                self.log("[詩歌同步] ⚠️ 尚未在 Downloads 或程式目錄找到 config.txt 設定檔。")
                return False
        except Exception as e:
            self.log(f"[詩歌同步] 同步 config.txt 發生例外: {e}")
            target_file = DOWNLOADS_CONFIG if os.path.exists(DOWNLOADS_CONFIG) else None

        self.active_config_path = target_file
        return self._parse_config_file(target_file)

    def _parse_config_file(self, filepath):
        """支援多種編碼讀取 config.txt 並解析歌名與頁碼映射"""
        if not os.path.exists(filepath):
            return False

        encodings = ['utf-16le', 'utf-8-sig', 'utf-8', 'cp950']
        content = ""
        for enc in encodings:
            try:
                with open(filepath, 'r', encoding=enc) as f:
                    c = f.read().strip('\ufeff')
                    if len(c) > 5 and ('_V' in c or '_C' in c or '#' in c):
                        content = c
                        break
            except Exception:
                continue

        if not content:
            return False

        self.songs.clear()
        self.mapping.clear()
        pending_title = None

        for line in content.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith('#'):
                pending_title = line.lstrip('#').strip()
                continue
            parts = [p.strip() for p in line.split(',')]
            if len(parts) >= 2:
                cmd, page = parts[0], parts[1]
                if cmd not in self.mapping:
                    self.mapping[cmd] = []
                self.mapping[cmd].append(page)
                m = re.match(r'^(\d+)_', cmd)
                if m:
                    s_num = int(m.group(1))
                    if pending_title and s_num not in self.songs:
                        self.songs[s_num] = pending_title
                        pending_title = None

        # 輸出歌單日誌
        song_summary = []
        for s_num in sorted(self.songs.keys()):
            song_summary.append(f"第 {s_num} 首: {self.songs[s_num]}")
        
        if song_summary:
            self.log(f"[詩歌歌單] 成功解析 {len(self.songs)} 首歌曲：" + " | ".join(song_summary))
        return True

    def open_web_app(self):
        """開啟雲端歌詞網頁 (預設直接進入副唱顯示端)"""
        try:
            webbrowser.open(CLOUD_URL)
            self.log(f"[詩歌同步] 已在預設瀏覽器開啟雲端歌詞網頁 (直接進入副唱顯示端): {CLOUD_URL}")
            return True
        except Exception as e:
            self.log(f"[詩歌同步] 開啟網頁失敗: {e}")
            return False

    def find_lyrics_window(self):
        """尋找目前標題含有「同步歌詞」的瀏覽器視窗"""
        if not HAS_WIN32:
            return None, ""

        found = []
        def enum_cb(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if "同步歌詞" in title or "sync-lyrics" in title.lower():
                    found.append((hwnd, title))
        win32gui.EnumWindows(enum_cb, None)
        return found[0] if found else (None, "")

    def switch_song(self, song_num):
        """投影同工切換歌曲 (自動跳至該首主歌、更新懸浮窗頁碼提示，並連動 PowerPoint 放映)"""
        song_name = self.songs.get(song_num, "")
        self.current_song = song_num

        # 1. 取得該首歌曲之「主歌 (V)」頁碼
        cmd_verse = f"{song_num}_V"
        pages = self.mapping.get(cmd_verse, [])
        first_page = pages[0] if pages else ""
        page_display = f"{pages[0]} (後續 {', '.join(pages[1:])})" if len(pages) > 1 else (pages[0] if pages else "未設定")

        self.log(f"[切換歌曲] 投影同工切換至：第 {song_num} 首 ({song_name}) ➔ 自動跳至主歌，頁碼: 第 {page_display} 頁")

        # 2. 立刻更新懸浮視窗至該首歌曲的主歌與頁碼
        if self.navigator_window and self.navigator_window.is_alive():
            self.navigator_window.set_song_verse(song_num, song_name, pages)

        # 3. 通知主控台介面同步高亮歌曲按鈕
        if self.on_song_changed_callback:
            try:
                self.on_song_changed_callback(song_num)
            except Exception:
                pass

        # 4. PowerPoint 自動跳至該首主歌放映頁面 (雙重確認，確保 100% 跳頁)
        def _do_jump():
            try:
                from ppt_manager import goto_slide
                if first_page and str(first_page).isdigit():
                    goto_slide(int(first_page), log_callback=self.log)
            except Exception:
                pass

        _do_jump()
        if self.navigator_window and self.navigator_window.is_alive():
            self.navigator_window.win.after(100, _do_jump)

        # 5. 背景通知雲端歌詞網頁切換至該首歌曲 (若瀏覽器已開啟)，完成後立即歸還視窗焦點給 PPT
        if HAS_WIN32:
            hwnd, title = self.find_lyrics_window()
            if hwnd:
                def _sync_browser():
                    try:
                        win32gui.SetForegroundWindow(hwnd)
                        time.sleep(0.04)
                        vk_num = ord(str(song_num))
                        win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
                        win32api.keybd_event(vk_num, 0, 0, 0)
                        time.sleep(0.03)
                        win32api.keybd_event(vk_num, 0, win32con.KEYEVENTF_KEYUP, 0)
                        win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
                        from ppt_manager import focus_slideshow
                        time.sleep(0.02)
                        focus_slideshow(log_callback=self.log)
                    except Exception:
                        pass
                threading.Thread(target=_sync_browser, daemon=True).start()

        return True

    def start_floating_navigator(self, root_tk):
        """啟動或顯示原生半透明置頂懸浮導航視窗"""
        # 啟動前自動刷新最新 config.txt
        self.sync_and_load_config()

        if self.navigator_window and self.navigator_window.is_alive():
            self.navigator_window.show()
            self.log("[懸浮導航] 導航視窗已就緒並置頂顯示。")
            return

        self.navigator_window = FloatingNavigator(root_tk, self)
        self.navigator_window.show()
        self.log("[懸浮導航] 🚀 已啟動原生置頂 PPT 歌詞同步導航視窗 (F9 啟動 / F11 關閉)！")

    def stop_floating_navigator(self):
        """關閉或隱藏懸浮導航視窗"""
        if self.navigator_window and self.navigator_window.is_alive():
            self.navigator_window.hide()
            self.log("[懸浮導航] 已關閉懸浮導航視窗。")

    def launch_ahk_backup(self):
        """一鍵啟動原本的 AHK 腳本 (備用方案)"""
        if not os.path.exists(AHK_EXE_PATH):
            self.log(f"[AHK 備用] 找不到 AutoHotkey 執行檔: {AHK_EXE_PATH}")
            return False
        if not os.path.exists(AHK_SCRIPT_PATH):
            self.log(f"[AHK 備用] 找不到 AHK 腳本: {AHK_SCRIPT_PATH}")
            return False

        try:
            self.sync_and_load_config() # 先更新 config
            subprocess.Popen([AHK_EXE_PATH, AHK_SCRIPT_PATH], cwd=SYNC_APP_DIR)
            self.log(f"[AHK 備用] 🚀 已在背景啟動 ppt_sync.ahk 腳本！")
            return True
        except Exception as e:
            self.log(f"[AHK 備用] 啟動 AHK 失敗: {e}")
            return False


class FloatingNavigator:
    """原生 Python 置頂半透明 PPT 歌詞同步導航懸浮視窗 (完全取代 AHK)"""
    def __init__(self, parent, manager):
        self.parent = parent
        self.manager = manager
        self.win = None
        self.running = False
        self.is_small_mode = False
        self.last_cmd = ""
        self.drag_x = 0
        self.drag_y = 0
        self.user_dragged = False
        self.num_buffer = ""
        self.num_buffer_timer = None

    def is_alive(self):
        return self.win is not None and self.win.winfo_exists()

    def show(self):
        if not self.is_alive():
            self._create_window()
        else:
            if not getattr(self, "user_dragged", False):
                self._ensure_safe_initial_pos()
        self.win.deiconify()
        self.win.lift()
        self.win.attributes("-topmost", True)
        if not self.running:
            self.running = True
            threading.Thread(target=self._monitor_loop, daemon=True).start()

    def hide(self):
        self.running = False
        if self.is_alive():
            self.win.withdraw()

    def _ensure_safe_initial_pos(self):
        """計算安全初始位置：優先排定於中控台右側或安全空曠區域，絕不遮擋【📐 視窗排版】等操作按鈕"""
        try:
            sw = self.win.winfo_screenwidth()
            sh = self.win.winfo_screenheight()
            w = 430 if self.is_small_mode else 480
            h = 148 if self.is_small_mode else 158

            placed = False
            if self.parent and hasattr(self.parent, "winfo_rootx"):
                try:
                    self.parent.update_idletasks()
                    if self.parent.winfo_viewable():
                        px = self.parent.winfo_rootx()
                        py = self.parent.winfo_rooty()
                        pw = self.parent.winfo_width()
                        ph = self.parent.winfo_height()

                        # 策略 1: 若中控台右側有充足空間，緊鄰中控台右側 (留 15px 縫隙)
                        if px + pw + w + 16 <= sw:
                            x = px + pw + 15
                            y = max(10, min(py + 60, sh - h - 40))
                            placed = True
                        # 策略 2: 若中控台左側有足夠空間
                        elif px >= w + 16:
                            x = px - w - 15
                            y = max(10, min(py + 60, sh - h - 40))
                            placed = True
                        # 策略 3: 若中控台下方有空間 (徹底避開 Step 4 按鈕列)
                        elif py + ph + h + 15 <= sh:
                            x = max(10, min(px + 20, sw - w - 12))
                            y = py + ph + 10
                            placed = True
                except Exception:
                    placed = False

            # 備用安全位置：螢幕右側中上方 (避開左側中控台視窗)
            if not placed:
                x = max(10, sw - w - 24)
                y = max(20, (sh - h) // 3)

            self.win.geometry(f"{w}x{h}+{x}+{y}")
        except Exception:
            pass

    def _create_window(self):
        self.win = tk.Toplevel(self.parent)
        self.win.title("PPT_Sync_Navigator")
        self.win.overrideredirect(True)      # 無邊框 (同 AHK -Caption)
        self.win.attributes("-topmost", True) # 永遠置頂 (同 AHK +AlwaysOnTop)
        self.win.attributes("-alpha", 0.94)   # 94% 不透明度
        self.win.configure(bg="#FFFFFF")      # 外部 2px 純白外框底色

        # 計算安全預設位置 (避免遮擋中控台【📐 視窗排版】按鈕)
        self._ensure_safe_initial_pos()

        # 滑鼠拖曳視窗支援
        self.win.bind("<ButtonPress-1>", self._start_drag)
        self.win.bind("<B1-Motion>", self._do_drag)
        self.win.bind("<ButtonRelease-1>", lambda e: self._refocus_ppt())

        # 套用 Windows 懸浮工具列無焦點特性 (WS_EX_NOACTIVATE = 0x08000000)
        # 同時設定在 Tkinter 內部 HWND (wid) 與 Windows 頂層 HWND (parent)
        try:
            self.win.update_idletasks()
            wid = self.win.winfo_id()
            if HAS_WIN32:
                parent = win32gui.GetParent(wid)
                for h in [wid, parent]:
                    if h and win32gui.IsWindow(h):
                        ex_style = win32gui.GetWindowLong(h, win32con.GWL_EXSTYLE)
                        win32gui.SetWindowLong(h, win32con.GWL_EXSTYLE, ex_style | 0x08000000)
        except Exception:
            pass

        # 鍵盤穿透轉發機制：即便焦點落在懸浮窗，鍵盤輸入也能 100% 直達 PowerPoint
        self.win.bind("<Key>", self._on_key_press)

        # 套用四角圓邊 (現代圓角無邊框視窗)
        self.win.after(30, self.apply_rounded_corners)

        # 內部主要容器 (深藍科技黑底，藉由 outer padding 呈現 2px 白色外框)
        self.container = tk.Frame(self.win, bg="#0B132B")
        self.container.pack(fill="both", expand=True, padx=2, pady=2)

        # 頂部小標題列
        hdr = tk.Frame(self.container, bg="#0B132B")
        hdr.pack(fill="x", padx=12, pady=(6, 0))

        self.lbl_conn = tk.Label(
            hdr,
            text="🟢 等待連線 (尋找歌詞視窗)...",
            font=("微軟正黑體", 9, "bold"),
            fg="#34D399",
            bg="#0B132B"
        )
        self.lbl_conn.pack(side="left")

        # 控制小按鈕區 (右上方高亮控制鍵)
        ctrl_box = tk.Frame(hdr, bg="#0B132B")
        ctrl_box.pack(side="right", padx=(0, 4))

        btn_snap = tk.Label(ctrl_box, text="📐 歸位", font=("微軟正黑體", 8, "bold"), fg="#34D399", bg="#0B132B", cursor="hand2")
        btn_snap.pack(side="left", padx=4)
        btn_snap.bind("<Button-1>", lambda e: self._on_snap_clicked())

        btn_master = tk.Label(ctrl_box, text="🎛️ 中控", font=("微軟正黑體", 8, "bold"), fg="#38BDF8", bg="#0B132B", cursor="hand2")
        btn_master.pack(side="left", padx=4)
        btn_master.bind("<Button-1>", lambda e: self._on_master_clicked())

        btn_size = tk.Label(ctrl_box, text="⛶ 大小", font=("微軟正黑體", 8, "bold"), fg="#E2E8F0", bg="#0B132B", cursor="hand2")
        btn_size.pack(side="left", padx=4)
        btn_size.bind("<Button-1>", lambda e: self.toggle_size())

        btn_close = tk.Label(ctrl_box, text="✕ 關閉", font=("微軟正黑體", 8, "bold"), fg="#F87171", bg="#0B132B", cursor="hand2")
        btn_close.pack(side="left", padx=2)
        btn_close.bind("<Button-1>", lambda e: self.hide())

        # 計算初始歌曲與主歌頁碼
        cur_s = self.manager.current_song
        cur_song_name = self.manager.songs.get(cur_s, "")
        cur_pages = self.manager.mapping.get(f"{cur_s}_V", [])
        init_page_text = f"請輸入: {cur_pages[0]}" if cur_pages else "請輸入: 等待信號..."
        init_song_text = f"目前歌曲: 第 {cur_s} 首 (主歌){' - ' + cur_song_name if cur_song_name else ''}"

        # 中央超大字：頁碼指示 (同 AHK StatusText) - 純白超粗體
        self.lbl_page = tk.Label(
            self.container,
            text=init_page_text,
            font=("微軟正黑體", 26 if self.is_small_mode else 32, "bold"),
            fg="#FFFFFF",
            bg="#0B132B"
        )
        self.lbl_page.pack(pady=(2, 0))

        # 下方高亮金黃字：目前歌曲與段落 - 電光金黃
        self.lbl_song = tk.Label(
            self.container,
            text=init_song_text,
            font=("微軟正黑體", 10 if self.is_small_mode else 11, "bold"),
            fg="#FACC15",
            bg="#0B132B"
        )
        self.lbl_song.pack(pady=(1, 5))

        # 底部歌曲切換按鈕列 (與中控台同步，顯示實際歌名與高亮狀態)
        self.btn_row = tk.Frame(self.container, bg="#0B132B")
        self.btn_row.pack(fill="x", padx=10, pady=(0, 8))

        self.song_buttons = {}
        for s_idx in [1, 2, 3]:
            s_name = self.manager.songs.get(s_idx, "")
            display_title = f"🎵 首 {s_idx}: {s_name}" if s_name else f"🎵 第 {s_idx} 首"
            is_active = (s_idx == cur_s)

            btn = tk.Label(
                self.btn_row,
                text=display_title,
                font=("微軟正黑體", 8 if self.is_small_mode else 9, "bold"),
                bg="#6366F1" if is_active else "#1E293B",
                fg="#FFFFFF",
                padx=6 if self.is_small_mode else 8,
                pady=4,
                cursor="hand2"
            )
            btn.pack(side="left", expand=True, fill="x", padx=2)

            def _bind_btn(b, idx):
                b.bind("<Enter>", lambda e: b.config(bg="#334155") if idx != self.manager.current_song else None)
                b.bind("<Leave>", lambda e: b.config(bg="#1E293B") if idx != self.manager.current_song else None)
                def _click(e):
                    self.manager.switch_song(idx)
                    self._refocus_ppt()
                b.bind("<Button-1>", _click)
            _bind_btn(btn, s_idx)
            self.song_buttons[s_idx] = btn

    def _on_key_press(self, event):
        """鍵盤事件直接作用於 PowerPoint，解決同工未點 PPT 畫面也能按鍵切頁與輸數字"""
        keysym = event.keysym
        char = event.char

        # 1. 數字鍵輸入 (0-9)
        if char and char.isdigit():
            self.num_buffer += char
            if self.num_buffer_timer:
                self.parent.after_cancel(self.num_buffer_timer)
            self.num_buffer_timer = self.parent.after(1500, self._clear_num_buffer)
            return

        # 2. Enter / Return 鍵
        if keysym in ["Return", "KP_Enter"]:
            if self.num_buffer:
                target_slide = int(self.num_buffer)
                self.num_buffer = ""
                try:
                    from ppt_manager import goto_slide
                    goto_slide(target_slide, log_callback=self.manager.log)
                except Exception:
                    pass
            else:
                try:
                    from ppt_manager import next_slide
                    next_slide(log_callback=self.manager.log)
                except Exception:
                    pass
            self._refocus_ppt()
            return

        # 3. 下一頁 (空白鍵 / 方向鍵右 / 方向鍵下 / PageDown)
        if keysym in ["space", "Right", "Down", "Next"]:
            self.num_buffer = ""
            try:
                from ppt_manager import next_slide
                next_slide(log_callback=self.manager.log)
            except Exception:
                pass
            self._refocus_ppt()
            return

        # 4. 上一頁 (方向鍵左 / 方向鍵上 / PageUp)
        if keysym in ["Left", "Up", "Prior"]:
            self.num_buffer = ""
            try:
                from ppt_manager import prev_slide
                prev_slide(log_callback=self.manager.log)
            except Exception:
                pass
            self._refocus_ppt()
            return

        self.num_buffer = ""
        self._refocus_ppt()

    def _clear_num_buffer(self):
        self.num_buffer = ""
        self.num_buffer_timer = None

    def _refocus_ppt(self):
        """點擊懸浮窗後立即將鍵盤焦點歸還給 PowerPoint 放映視窗"""
        def _do():
            try:
                from ppt_manager import focus_slideshow
                focus_slideshow(log_callback=self.manager.log)
            except Exception:
                pass
        if self.is_alive():
            self.win.after(50, _do)

    def _start_drag(self, event):
        self.drag_x = event.x
        self.drag_y = event.y

    def _do_drag(self, event):
        if not self.is_alive():
            return
        dx = event.x - self.drag_x
        dy = event.y - self.drag_y
        if abs(dx) > 3 or abs(dy) > 3:
            self.user_dragged = True
        x = self.win.winfo_x() + dx
        y = self.win.winfo_y() + dy
        self.win.geometry(f"+{x}+{y}")

    def _on_snap_clicked(self):
        """點擊懸浮窗上的【📐 歸位】按鈕，先彈出前置檢核清單，確認後執行自動排版"""
        try:
            from window_layout_manager import confirm_preflight_checklist, snap_sunday_layout
            if not confirm_preflight_checklist(parent=self.win):
                self.manager.log("[懸浮導航] 同工已取消排版作業。")
                return

            snap_sunday_layout(app_instance=getattr(self.manager, "app_instance", None), log_callback=self.manager.log, skip_confirm=True)
        except Exception as e:
            self.manager.log(f"[懸浮導航] 排版歸位失敗: {e}")

    def _on_master_clicked(self):
        """點擊懸浮窗上的【🎛️ 中控】按鈕，立刻還原並呼叫中控台主畫面"""
        try:
            if self.parent:
                self.parent.deiconify()
                self.parent.lift()
                self.parent.focus_force()
        except Exception:
            pass

    def apply_rounded_corners(self, radius=26):
        """為懸浮導航視窗四個角建立現代平滑圓邊 (SetWindowRgn)"""
        if not HAS_WIN32 or not self.is_alive():
            return
        try:
            import ctypes
            self.win.update_idletasks()
            w = self.win.winfo_width()
            h = self.win.winfo_height()
            if w <= 1 or h <= 1:
                w = 430 if self.is_small_mode else 480
                h = 148 if self.is_small_mode else 158
            wid = self.win.winfo_id()
            top_h = win32gui.GetParent(wid) or wid
            gdi32 = ctypes.windll.gdi32
            user32 = ctypes.windll.user32
            for hwnd in [wid, top_h]:
                if hwnd and win32gui.IsWindow(hwnd):
                    hrgn = gdi32.CreateRoundRectRgn(0, 0, w + 1, h + 1, int(radius), int(radius))
                    if hrgn:
                        user32.SetWindowRgn(hwnd, hrgn, True)
        except Exception:
            pass

    def snap_to_bottom_left_top_right(self, work_x=0, work_y=0, half_w=853, half_h=456):
        """將懸浮導航視窗精確排定在左下格 (相機畫面) 的右上方，並套用四角圓邊"""
        if not self.is_alive():
            return
        self.user_dragged = False
        w = 430 if self.is_small_mode else 480
        h = 148 if self.is_small_mode else 158
        x = work_x + half_w - w - 12
        y = work_y + half_h + 30
        self.win.geometry(f"{w}x{h}+{x}+{y}")
        self.win.lift()
        self.win.attributes("-topmost", True)
        self.win.after(30, self.apply_rounded_corners)

    def snap_to_top_left(self, work_x=0, work_y=0, half_w=853):
        """將懸浮導航視窗排定在左上格"""
        self.snap_to_bottom_left_top_right(work_x, work_y, half_w)

    def toggle_size(self):
        """切換標準 (480x158) / 緊湊 (430x148) 模式"""
        self.is_small_mode = not self.is_small_mode
        if self.is_alive():
            cur_x = self.win.winfo_x()
            cur_y = self.win.winfo_y()
            w = 430 if self.is_small_mode else 480
            h = 148 if self.is_small_mode else 158
            self.win.geometry(f"{w}x{h}+{cur_x}+{cur_y}")
            self.lbl_page.configure(font=("微軟正黑體", 26 if self.is_small_mode else 32, "bold"))
            self.lbl_song.configure(font=("微軟正黑體", 10 if self.is_small_mode else 11, "bold"))
            for btn in self.song_buttons.values():
                btn.configure(font=("微軟正黑體", 8 if self.is_small_mode else 9, "bold"))
            self.win.after(30, self.apply_rounded_corners)
            self._refocus_ppt()

    def update_song_buttons(self, active_num):
        """更新懸浮窗歌曲按鈕高亮狀態與標題"""
        if not hasattr(self, "song_buttons"):
            return
        for s_idx, btn in self.song_buttons.items():
            s_name = self.manager.songs.get(s_idx, "")
            display_title = f"🎵 首 {s_idx}: {s_name}" if s_name else f"🎵 第 {s_idx} 首"
            if s_idx == active_num:
                btn.configure(text=display_title, bg="#6366F1", fg="#FFFFFF")
            else:
                btn.configure(text=display_title, bg="#1E293B", fg="#F8FAFC")

    def set_song_verse(self, song_num, song_name, pages):
        """切換歌曲時，立即更新懸浮窗為該首「主歌」與對應頁碼"""
        if not self.is_alive():
            return

        self.last_cmd = f"{song_num}_V"
        title_display = f" - {song_name}" if song_name else ""
        self.lbl_song.configure(text=f"目前歌曲: 第 {song_num} 首 (主歌){title_display}")

        if pages:
            self.lbl_page.configure(text=f"請輸入: {pages[0]}")
        else:
            self.lbl_page.configure(text="等待信號...")

        self.lbl_conn.configure(text=f"✅ 已切換至第 {song_num} 首主歌", fg="#10B981")
        self.update_song_buttons(song_num)

    def set_song(self, song_num, song_name):
        self.set_song_verse(song_num, song_name, self.manager.mapping.get(f"{song_num}_V", []))

    def _monitor_loop(self):
        """背景迴圈每 100ms 檢查一次視窗標題的 [CMD:...] 指令"""
        while self.running:
            try:
                if not self.is_alive():
                    break

                hwnd, full_title = self.manager.find_lyrics_window()
                if not hwnd:
                    self.parent.after(0, lambda: self._update_conn_status("❌ 未偵測到視窗 (請點擊開啟雲端歌詞)", "#EF4444"))
                    time.sleep(0.5)
                    continue

                # 擷取 [CMD:...]
                m = re.search(r'\[CMD:(.*?)\]', full_title)
                if m:
                    cmd = m.group(1).strip()
                    self.parent.after(0, lambda t=full_title, c=cmd: self._process_cmd(t, c))
                else:
                    self.parent.after(0, lambda: self._update_conn_status("✅ 歌詞同步已連線", "#10B981"))

                time.sleep(0.1)
            except Exception:
                time.sleep(0.3)

    def _update_conn_status(self, text, color):
        if self.is_alive():
            self.lbl_conn.configure(text=text, fg=color)

    def _process_cmd(self, full_title, cmd):
        if not self.is_alive():
            return

        self.lbl_conn.configure(text=f"✅ 歌詞同步中 [{cmd}]", fg="#10B981")

        if cmd == self.last_cmd:
            return

        # 解析歌曲編號與段落代碼 (例如 "3_V2", "3_P", "1_C")
        m_song = re.match(r'^(\d+)_(.*)', cmd)
        song_num = 1
        part_code = "V"
        if m_song:
            song_num = int(m_song.group(1))
            part_code = m_song.group(2)
        elif re.match(r'^(\d+)', cmd):
            song_num = int(re.match(r'^(\d+)', cmd).group(1))

        # 關鍵防護：若接收到的指令歌曲編號與目前選取的歌曲不符，絕不倒退覆蓋！
        # (換歌曲一律由中控懸浮窗主動切換，避免被瀏覽器殘留的舊歌標題強行拉回第 1 首)
        if song_num != self.manager.current_song:
            return

        self.last_cmd = cmd

        part_name = PART_NAME_MAP.get(part_code, f"({part_code})")
        song_title = self.manager.songs.get(song_num, "")

        # 更新目前歌曲標籤
        title_display = f" - {song_title}" if song_title else ""
        self.lbl_song.configure(text=f"目前歌曲: 第 {song_num} 首 ({part_name}){title_display}")

        # 查閱 config 頁碼
        pages = self.manager.mapping.get(cmd, [])
        if pages:
            self.lbl_page.configure(text=f"請輸入: {pages[0]}")
        else:
            self.lbl_page.configure(text="等待信號...")
