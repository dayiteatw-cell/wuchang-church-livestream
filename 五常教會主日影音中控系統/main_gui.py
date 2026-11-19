# -*- coding: utf-8 -*-
"""
五常教會 主日影音直播自動化中控系統
台灣基督長老教會 五常教會 (Wuchang Presbyterian Church)
整合：
1. Gmail 主日附件自動下載 (dayitea.tw)
2. PPT 講道題目與講員自動解析 + YouTube 直播標題複製
3. PowerPoint 雙螢幕延伸投影全螢幕自動放映
4. 安卓雙機 (Samsung Galaxy A27 + ASUS) ADB 時序喚醒、休眠與斷電關機
5. scrcpy 雙機獨立畫面投影監控與遠端縮放對焦
"""

import os
import sys
import threading
import time
import subprocess
import shutil
import re
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from PIL import Image, ImageTk

# 匯入內部模組
from sermon_parser import extract_sermon_info
from gmail_downloader import download_sunday_files, get_recent_sunday
from camera_manager import (
    wake_all_cameras, sleep_all_cameras, repair_camera_order, check_devices, run_adb,
    wake_single_camera, sleep_single_camera, poweroff_single_camera,
    is_iriun_running, launch_iriun_webcam
)
from ppt_manager import start_slideshow, next_slide, prev_slide, exit_slideshow
from lyrics_sync_manager import LyricsSyncManager
from window_layout_manager import snap_sunday_layout

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads")

YOUTUBE_LIVE_URL = "https://studio.youtube.com/channel/UCgWfqXVekyo6KGloR15Hblw/videos/live?filter=%5B%5D&sort=%7B%22columnType%22%3A%22date%22%2C%22sortOrder%22%3A%22DESCENDING%22%7D"

def get_asset_path(filename):
    """尋找 assets 資源路徑 (支援 PyInstaller 單一 EXE 打包與本地開發)"""
    if hasattr(sys, "_MEIPASS"):
        p = os.path.join(sys._MEIPASS, "assets", filename)
        if os.path.exists(p):
            return p
    local_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", filename)
    if os.path.exists(local_p):
        return local_p
    return None

def get_scrcpy_bin():
    """尋找 scrcpy.exe 所在路徑 (支援 PyInstaller 單一 EXE 打包與本地開發)"""
    if hasattr(sys, "_MEIPASS"):
        meipass_scrcpy = os.path.join(sys._MEIPASS, "scrcpy", "scrcpy.exe")
        if os.path.exists(meipass_scrcpy):
            return meipass_scrcpy
        root_scrcpy = os.path.join(sys._MEIPASS, "scrcpy.exe")
        if os.path.exists(root_scrcpy):
            return root_scrcpy

    local_scrcpy = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scrcpy", "scrcpy.exe")
    if os.path.exists(local_scrcpy):
        return local_scrcpy

    shared_scrcpy = r"E:\Antigravity_Data\五常教會直播設置\scrcpy\scrcpy.exe"
    if os.path.exists(shared_scrcpy):
        return shared_scrcpy

    found = shutil.which("scrcpy")
    if found:
        return found
    return "scrcpy"

def make_button(parent, text, bg, fg="white", hover_bg=None, command=None, font=("微軟正黑體", 10, "bold"), padx=12, pady=5):
    """建立現代扁平化按鈕 (附帶滑鼠懸停效果)"""
    btn = tk.Button(
        parent,
        text=text,
        bg=bg,
        fg=fg,
        activebackground=hover_bg or bg,
        activeforeground=fg,
        font=font,
        relief="flat",
        bd=0,
        padx=padx,
        pady=pady,
        cursor="hand2"
    )
    if hover_bg:
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    if command:
        btn.config(command=command)
    return btn


class ChurchAutomationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("五常基督長老教會  主日影音與直播總控系統")
        self.root.geometry("880x700")
        self.root.minsize(840, 640)

        # 設定視窗圖示 (方案 B 現代純白圓角卡片底板)
        icon_path = get_asset_path("app_icon_v3.ico") or get_asset_path("app_icon.ico")
        if icon_path and os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception:
                pass

        # 載入教會 Logo (純白圓角底板徽章，清晰呈現十架與同心圓)
        self.logo_image = None
        self.taskbar_icon = None
        logo_path = get_asset_path("church_logo.png")
        if logo_path and os.path.exists(logo_path):
            try:
                pil_img = Image.open(logo_path).convert("RGBA")
                # 依 1:1 縮放為 48 x 48，於頂部抬頭清晰呈現
                pil_img_resized = pil_img.resize((48, 48), Image.Resampling.LANCZOS)
                self.logo_image = ImageTk.PhotoImage(pil_img_resized)
            except Exception:
                self.logo_image = None

        # 設定 Windows 工作列圖示 (採用帶純白外框卡片之正方形圖標，深淺主題皆清晰奪目)
        app_icon_png = get_asset_path("app_icon_v3.png") or get_asset_path("app_icon.png") or logo_path
        if app_icon_png and os.path.exists(app_icon_png):
            try:
                t_img = Image.open(app_icon_png).convert("RGBA")
                self.taskbar_icon = ImageTk.PhotoImage(t_img.resize((64, 64), Image.Resampling.LANCZOS))
                self.root.iconphoto(False, self.taskbar_icon)
            except Exception:
                pass

        self.current_pptx_path = None
        self.current_title_info = None
        self.current_sunday_date = get_recent_sunday()

        # 詩歌連動與 PPT 導航管理器
        self.lyrics_mgr = LyricsSyncManager(log_callback=self.log)
        self.lyrics_mgr.app_instance = self
        self.lyrics_mgr.on_song_changed_callback = self.update_active_song_button

        # 樣式定義
        self.setup_styles()
        self.create_widgets()

        # 更新詩歌 UI 標籤
        self.update_lyrics_ui_labels()

        # 綁定全域/視窗快捷鍵 (F9 懸浮導航、F11 關閉、F12 一鍵排版歸位)
        self.root.bind("<F9>", lambda e: self.btn_start_lyrics_nav())
        self.root.bind("<F11>", lambda e: self.btn_stop_lyrics_nav())
        self.root.bind("<F12>", lambda e: self.btn_snap_layout_clicked())

        # 啟動時自動掃描 Downloads 資料夾中的最新 PPT
        self.root.after(400, self.auto_check_existing_files)

        # 啟動時自動檢查並執行電腦端 Iriun Webcam (若尚未開啟)
        self.root.after(800, self.auto_start_iriun)

    def setup_styles(self):
        # 現代雅緻配色 (參考五常教會 Logo 綠色與質感灰)
        self.c_bg = "#F8FAFC"         # 背景 Slate 50
        self.c_card = "#FFFFFF"       # 卡片底色純白
        self.c_border = "#E2E8F0"     # 細邊框灰
        self.c_teal = "#0D9488"       # 教會品牌湖水綠
        self.c_teal_hover = "#0F766E" # 懸停深綠
        self.c_teal_light = "#F0FDFA" # 淺綠高亮底色
        self.c_emerald = "#059669"    # 成功翡翠綠
        self.c_blue = "#2563EB"       # 科技藍
        self.c_rose = "#E11D48"       # 警示紅
        self.c_text = "#0F172A"       # 深黑字體
        self.c_muted = "#64748B"      # 次要文字灰

        self.root.configure(bg=self.c_bg)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=self.c_bg)
        style.configure("Card.TFrame", background=self.c_card)
        style.configure("TLabel", background=self.c_bg, foreground=self.c_text, font=("微軟正黑體", 10))
        style.configure("Card.TLabel", background=self.c_card, foreground=self.c_text, font=("微軟正黑體", 10))

    def create_widgets(self):
        # ==================== [頂部] 教會品牌形象標題列 ====================
        header_card = tk.Frame(self.root, bg="#FFFFFF", highlightbackground=self.c_border, highlightthickness=1)
        header_card.pack(fill="x", padx=16, pady=(12, 6))

        header_content = tk.Frame(header_card, bg="#FFFFFF")
        header_content.pack(fill="x", padx=16, pady=10)

        # 左側: Logo 與 標題
        left_box = tk.Frame(header_content, bg="#FFFFFF")
        left_box.pack(side="left")

        if self.logo_image:
            lbl_logo = tk.Label(left_box, image=self.logo_image, bg="#FFFFFF")
            lbl_logo.pack(side="left", padx=(0, 14))

        title_vbox = tk.Frame(left_box, bg="#FFFFFF")
        title_vbox.pack(side="left")

        title_lbl = tk.Label(
            title_vbox,
            text="台灣基督長老教會  五常教會",
            font=("微軟正黑體", 15, "bold"),
            fg=self.c_text,
            bg="#FFFFFF"
        )
        title_lbl.pack(anchor="w")

        sub_lbl = tk.Label(
            title_vbox,
            text="主日影音與直播總控系統  •  Wuchang Presbyterian Church",
            font=("微軟正黑體", 9, "bold"),
            fg=self.c_teal,
            bg="#FFFFFF"
        )
        sub_lbl.pack(anchor="w", pady=(2, 0))

        # 右側: 即時主日資訊與就緒徽章
        right_box = tk.Frame(header_content, bg="#FFFFFF")
        right_box.pack(side="right")

        self.date_badge = tk.Frame(right_box, bg="#F0FDFA", highlightbackground="#99F6E4", highlightthickness=1)
        self.date_badge.pack(side="left", padx=6)
        self.lbl_head_date = tk.Label(
            self.date_badge,
            text=f"📅 主日日期: {self.current_sunday_date}",
            font=("微軟正黑體", 9, "bold"),
            fg=self.c_teal,
            bg="#F0FDFA",
            padx=10,
            pady=4
        )
        self.lbl_head_date.pack()

        sys_badge = tk.Frame(right_box, bg="#F0FDF4", highlightbackground="#BBF7D0", highlightthickness=1)
        sys_badge.pack(side="left", padx=6)
        tk.Label(
            sys_badge,
            text="● 系統就緒",
            font=("微軟正黑體", 9, "bold"),
            fg="#16A34A",
            bg="#F0FDF4",
            padx=10,
            pady=4
        ).pack()

        # 【📐 一鍵自動排版歸位】主快捷按鈕 (已移除多餘 F12 提示)
        btn_snap_head = make_button(
            right_box,
            text="📐 一鍵自動排版",
            bg=self.c_teal,
            fg="white",
            hover_bg=self.c_teal_hover,
            font=("微軟正黑體", 9, "bold"),
            padx=12,
            pady=4,
            command=self.btn_snap_layout_clicked
        )
        btn_snap_head.pack(side="left", padx=(6, 0))

        # ==================== [設備狀態列] 現代標籤式燈號 + 右上角控制 ====================
        status_card = tk.Frame(self.root, bg="#FFFFFF", highlightbackground=self.c_border, highlightthickness=1)
        status_card.pack(fill="x", padx=16, pady=(0, 6))

        stat_inner = tk.Frame(status_card, bg="#FFFFFF")
        stat_inner.pack(fill="x", padx=12, pady=5)

        tk.Label(stat_inner, text="硬體連線:", font=("微軟正黑體", 9, "bold"), fg=self.c_muted, bg="#FFFFFF").pack(side="left", padx=(0, 6))

        # A27 Badge
        self.f_stat_a27 = tk.Frame(stat_inner, bg="#F1F5F9", highlightbackground="#CBD5E1", highlightthickness=1)
        self.f_stat_a27.pack(side="left", padx=3)
        self.lbl_stat_a27 = tk.Label(self.f_stat_a27, text="● A27 主鏡: 偵測中", bg="#F1F5F9", fg=self.c_muted, font=("微軟正黑體", 8, "bold"), padx=6, pady=2)
        self.lbl_stat_a27.pack()

        # ASUS Badge
        self.f_stat_asus = tk.Frame(stat_inner, bg="#F1F5F9", highlightbackground="#CBD5E1", highlightthickness=1)
        self.f_stat_asus.pack(side="left", padx=3)
        self.lbl_stat_asus = tk.Label(self.f_stat_asus, text="● ASUS 全景: 偵測中", bg="#F1F5F9", fg=self.c_muted, font=("微軟正黑體", 8, "bold"), padx=6, pady=2)
        self.lbl_stat_asus.pack()

        # PPT Badge
        self.f_stat_ppt = tk.Frame(stat_inner, bg="#F1F5F9", highlightbackground="#CBD5E1", highlightthickness=1)
        self.f_stat_ppt.pack(side="left", padx=3)
        self.lbl_stat_ppt = tk.Label(self.f_stat_ppt, text="● 主日 PPT: 掃描中", bg="#F1F5F9", fg=self.c_muted, font=("微軟正黑體", 8, "bold"), padx=6, pady=2)
        self.lbl_stat_ppt.pack()

        # 右側控制：重新整理連線狀態
        btn_refresh_stat = make_button(
            stat_inner,
            text="🔄 重新整理",
            bg="#F1F5F9",
            fg="#334155",
            hover_bg="#E2E8F0",
            font=("微軟正黑體", 8, "bold"),
            padx=10,
            pady=3,
            command=self.refresh_devices_status
        )
        btn_refresh_stat.pack(side="right")

        # ==================== [主工作區] 上半雙欄 + 下半滿版 ====================
        main_work_area = tk.Frame(self.root, bg=self.c_bg)
        main_work_area.pack(fill="x", padx=16, pady=2)

        # 上半部：左右雙欄 (左欄: 步驟 1 相機總控，右欄: 步驟 2 主日附件 + 步驟 3 PPT 放映)
        top_split = tk.Frame(main_work_area, bg=self.c_bg)
        top_split.pack(fill="x", pady=(0, 6))

        left_col = tk.Frame(top_split, bg=self.c_bg)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 4))

        right_col = tk.Frame(top_split, bg=self.c_bg)
        right_col.pack(side="right", fill="both", expand=True, padx=(4, 0))

        # -------------------- [左欄] 【步驟 1】相機總控 (A27 + ASUS 雙機) --------------------
        step1_card = tk.Frame(left_col, bg="#FFFFFF", highlightbackground=self.c_border, highlightthickness=1)
        step1_card.pack(fill="both", expand=True, pady=0, ipady=4)

        s1_head = tk.Frame(step1_card, bg="#FFFFFF")
        s1_head.pack(fill="x", padx=12, pady=(8, 4))
        tk.Frame(s1_head, bg=self.c_blue, width=4, height=16).pack(side="left", padx=(0, 6))
        tk.Label(s1_head, text="【步驟 1】相機總控 (A27 + ASUS 雙機)", font=("微軟正黑體", 10, "bold"), fg="#1E3A8A", bg="#FFFFFF").pack(side="left")

        # 雙機喚醒與休眠主按鈕 (橫向對半分，填滿整行)
        cam_main_row = tk.Frame(step1_card, bg="#FFFFFF")
        cam_main_row.pack(fill="x", padx=12, pady=3)

        btn_wake = make_button(
            cam_main_row,
            text="🚀 【開機】喚醒手機",
            bg=self.c_blue,
            fg="white",
            hover_bg="#1D4ED8",
            font=("微軟正黑體", 9, "bold"),
            padx=8,
            pady=5,
            command=self.btn_wake_clicked
        )
        btn_wake.pack(side="left", fill="x", expand=True, padx=(0, 3))

        btn_sleep = make_button(
            cam_main_row,
            text="🌙 【散會】休眠手機",
            bg=self.c_rose,
            fg="white",
            hover_bg="#BE123C",
            font=("微軟正黑體", 9, "bold"),
            padx=8,
            pady=5,
            command=self.btn_sleep_clicked
        )
        btn_sleep.pack(side="left", fill="x", expand=True, padx=(3, 0))

        # 畫面投影監控 (scrcpy)
        cam_mon_row = tk.Frame(step1_card, bg="#FFFFFF")
        cam_mon_row.pack(fill="x", padx=12, pady=3)

        btn_scrcpy_a27 = make_button(
            cam_mon_row,
            text="📱 監控 A27",
            bg="#F1F5F9",
            fg="#0F172A",
            hover_bg="#E2E8F0",
            font=("微軟正黑體", 8, "bold"),
            padx=6,
            pady=3,
            command=self.btn_scrcpy_a27_clicked
        )
        btn_scrcpy_a27.pack(side="left", fill="x", expand=True, padx=(0, 2))

        btn_scrcpy_asus = make_button(
            cam_mon_row,
            text="📱 監控 ASUS",
            bg="#F1F5F9",
            fg="#0F172A",
            hover_bg="#E2E8F0",
            font=("微軟正黑體", 8, "bold"),
            padx=6,
            pady=3,
            command=self.btn_scrcpy_asus_clicked
        )
        btn_scrcpy_asus.pack(side="left", fill="x", expand=True, padx=2)

        btn_scrcpy_dual = make_button(
            cam_mon_row,
            text="🖥️ 雙機投影",
            bg="#F0FDFA",
            fg=self.c_teal,
            hover_bg="#CCFBF1",
            font=("微軟正黑體", 8, "bold"),
            padx=6,
            pady=3,
            command=self.btn_scrcpy_dual_clicked
        )
        btn_scrcpy_dual.pack(side="left", fill="x", expand=True, padx=(2, 0))

        # 分隔線
        tk.Frame(step1_card, bg=self.c_border, height=1).pack(fill="x", padx=12, pady=(4, 3))

        # 單機小指令附屬區
        a27_sub = tk.Frame(step1_card, bg="#FFFFFF")
        a27_sub.pack(fill="x", padx=12, pady=2)
        tk.Label(a27_sub, text="正面主鏡 A27:", font=("微軟正黑體", 8, "bold"), fg=self.c_text, bg="#FFFFFF", width=11, anchor="w").pack(side="left")

        make_button(a27_sub, "🔆 喚醒", bg="#F8FAFC", fg="#1E293B", hover_bg="#E2E8F0", font=("微軟正黑體", 8), padx=4, pady=2, command=lambda: self.sub_wake_camera("a27")).pack(side="left", fill="x", expand=True, padx=1)
        make_button(a27_sub, "💤 休眠", bg="#F8FAFC", fg="#1E293B", hover_bg="#E2E8F0", font=("微軟正黑體", 8), padx=4, pady=2, command=lambda: self.sub_sleep_camera("a27")).pack(side="left", fill="x", expand=True, padx=1)
        make_button(a27_sub, "🔍 操控", bg="#F0FDFA", fg=self.c_teal, hover_bg="#CCFBF1", font=("微軟正黑體", 8), padx=4, pady=2, command=lambda: self.sub_scrcpy_camera("a27")).pack(side="left", fill="x", expand=True, padx=1)
        make_button(a27_sub, "🔌 關機", bg="#FEF2F2", fg=self.c_rose, hover_bg="#FEE2E2", font=("微軟正黑體", 8), padx=4, pady=2, command=lambda: self.sub_poweroff_camera("a27")).pack(side="left", fill="x", expand=True, padx=1)

        asus_sub = tk.Frame(step1_card, bg="#FFFFFF")
        asus_sub.pack(fill="x", padx=12, pady=(2, 4))
        tk.Label(asus_sub, text="會眾全景 ASUS:", font=("微軟正黑體", 8, "bold"), fg=self.c_text, bg="#FFFFFF", width=11, anchor="w").pack(side="left")

        make_button(asus_sub, "🔆 喚醒", bg="#F8FAFC", fg="#1E293B", hover_bg="#E2E8F0", font=("微軟正黑體", 8), padx=4, pady=2, command=lambda: self.sub_wake_camera("asus")).pack(side="left", fill="x", expand=True, padx=1)
        make_button(asus_sub, "💤 休眠", bg="#F8FAFC", fg="#1E293B", hover_bg="#E2E8F0", font=("微軟正黑體", 8), padx=4, pady=2, command=lambda: self.sub_sleep_camera("asus")).pack(side="left", fill="x", expand=True, padx=1)
        make_button(asus_sub, "🔍 操控", bg="#F0FDFA", fg=self.c_teal, hover_bg="#CCFBF1", font=("微軟正黑體", 8), padx=4, pady=2, command=lambda: self.sub_scrcpy_camera("asus")).pack(side="left", fill="x", expand=True, padx=1)
        make_button(asus_sub, "🔌 關機", bg="#FEF2F2", fg=self.c_rose, hover_bg="#FEE2E2", font=("微軟正黑體", 8), padx=4, pady=2, command=lambda: self.sub_poweroff_camera("asus")).pack(side="left", fill="x", expand=True, padx=1)

        # 【📷 開啟 Iriun Webcam】橫向滿版展開
        iriun_row = tk.Frame(step1_card, bg="#FFFFFF")
        iriun_row.pack(fill="x", padx=12, pady=(2, 4))

        make_button(
            iriun_row,
            text="📷 開啟 Iriun Webcam (電腦端視訊驅動)",
            bg=self.c_teal,
            fg="white",
            hover_bg=self.c_teal_hover,
            font=("微軟正黑體", 8, "bold"),
            padx=10,
            pady=4,
            command=self.btn_iriun_clicked
        ).pack(fill="x", expand=True)

        # -------------------- [右欄 1] 【步驟 2】主日附件備便 & 直播標題 --------------------
        step2_card = tk.Frame(right_col, bg="#FFFFFF", highlightbackground=self.c_border, highlightthickness=1)
        step2_card.pack(fill="x", pady=(0, 6), ipady=3)

        # 區塊標題列
        s2_head = tk.Frame(step2_card, bg="#FFFFFF")
        s2_head.pack(fill="x", padx=12, pady=(8, 4))
        tk.Frame(s2_head, bg=self.c_teal, width=4, height=16).pack(side="left", padx=(0, 6))
        tk.Label(s2_head, text="【步驟 2】主日附件備便 & 直播標題", font=("微軟正黑體", 10, "bold"), fg="#1E3A8A", bg="#FFFFFF").pack(side="left")

        # 日期輸入與下載按鈕
        dl_row = tk.Frame(step2_card, bg="#FFFFFF")
        dl_row.pack(fill="x", padx=12, pady=(1, 4))

        tk.Label(dl_row, text="主日日期:", font=("微軟正黑體", 9, "bold"), fg=self.c_text, bg="#FFFFFF").pack(side="left")
        self.ent_date = ttk.Entry(dl_row, width=10, font=("Consolas", 9, "bold"))
        self.ent_date.insert(0, self.current_sunday_date)
        self.ent_date.pack(side="left", padx=(6, 8))

        btn_dl = make_button(
            dl_row,
            text="📥 下載主日附件",
            bg=self.c_teal,
            fg="white",
            hover_bg=self.c_teal_hover,
            font=("微軟正黑體", 9, "bold"),
            padx=12,
            pady=3,
            command=self.btn_download_clicked
        )
        btn_dl.pack(side="left")

        # 解析之講道資訊
        info_row = tk.Frame(step2_card, bg="#F8FAFC", highlightbackground=self.c_border, highlightthickness=1)
        info_row.pack(fill="x", padx=12, pady=(2, 5))

        info_inner = tk.Frame(info_row, bg="#F8FAFC")
        info_inner.pack(fill="x", padx=8, pady=4)

        tk.Label(info_inner, text="講道題目:", font=("微軟正黑體", 8, "bold"), fg=self.c_muted, bg="#F8FAFC").grid(row=0, column=0, sticky="w", pady=1)
        self.lbl_sermon_title = tk.Label(info_inner, text="尚未解析", font=("微軟正黑體", 9, "bold"), fg=self.c_teal, bg="#F8FAFC")
        self.lbl_sermon_title.grid(row=0, column=1, sticky="w", padx=4, pady=1)

        tk.Label(info_inner, text="講員牧師:", font=("微軟正黑體", 8, "bold"), fg=self.c_muted, bg="#F8FAFC").grid(row=0, column=2, sticky="w", padx=(10, 0), pady=1)
        self.lbl_preacher = tk.Label(info_inner, text="尚未解析", font=("微軟正黑體", 9, "bold"), fg=self.c_emerald, bg="#F8FAFC")
        self.lbl_preacher.grid(row=0, column=3, sticky="w", padx=4, pady=1)

        # YouTube 標題複製
        yt_row = tk.Frame(step2_card, bg="#FFFFFF")
        yt_row.pack(fill="x", padx=12, pady=(0, 6))

        yt_box = tk.Frame(yt_row, bg="#FFFFFF")
        yt_box.pack(fill="x")

        self.ent_yt_title = ttk.Entry(yt_box, font=("微軟正黑體", 9))
        self.ent_yt_title.pack(side="left", fill="x", expand=True, padx=(0, 4))

        btn_copy = make_button(
            yt_box,
            text="📋 複製",
            bg=self.c_emerald,
            fg="white",
            hover_bg="#047857",
            font=("微軟正黑體", 8, "bold"),
            padx=8,
            pady=3,
            command=self.btn_copy_title_clicked
        )
        btn_copy.pack(side="left", padx=2)

        btn_yt = make_button(
            yt_box,
            text="🌐 開啟後台",
            bg="#334155",
            fg="white",
            hover_bg="#1E293B",
            font=("微軟正黑體", 8, "bold"),
            padx=8,
            pady=3,
            command=self.btn_open_yt_clicked
        )
        btn_yt.pack(side="left", padx=2)

        # -------------------- [右欄 2] 【步驟 3】PPT 雙螢幕大投影 --------------------
        step3_card = tk.Frame(right_col, bg="#FFFFFF", highlightbackground=self.c_border, highlightthickness=1)
        step3_card.pack(fill="x", pady=0, ipady=3)

        s3_head = tk.Frame(step3_card, bg="#FFFFFF")
        s3_head.pack(fill="x", padx=12, pady=(8, 4))
        tk.Frame(s3_head, bg=self.c_emerald, width=4, height=16).pack(side="left", padx=(0, 6))
        tk.Label(s3_head, text="【步驟 3】PPT 雙螢幕大投影", font=("微軟正黑體", 10, "bold"), fg="#1E3A8A", bg="#FFFFFF").pack(side="left")

        ppt_btn_row = tk.Frame(step3_card, bg="#FFFFFF")
        ppt_btn_row.pack(fill="x", padx=12, pady=(2, 6))

        btn_run_ppt = make_button(
            ppt_btn_row,
            text="🖥️ 全螢幕投影主日 PPT (自動延伸雙螢幕放映)",
            bg="#10B981",
            fg="white",
            hover_bg="#059669",
            font=("微軟正黑體", 9, "bold"),
            padx=12,
            pady=6,
            command=self.btn_run_ppt_clicked
        )
        btn_run_ppt.pack(fill="x", expand=True)

        # ==================== [下半部 滿版卡片] 【步驟 4】主日詩歌連動與 PPT 懸浮導航 ====================
        step4_card = tk.Frame(main_work_area, bg="#FFFFFF", highlightbackground=self.c_border, highlightthickness=1)
        step4_card.pack(fill="x", pady=(0, 4), ipady=3)

        s4_head = tk.Frame(step4_card, bg="#FFFFFF")
        s4_head.pack(fill="x", padx=12, pady=(6, 3))
        tk.Frame(s4_head, bg="#8B5CF6", width=4, height=16).pack(side="left", padx=(0, 6))
        tk.Label(s4_head, text="【步驟 4】主日詩歌連動與 PPT 懸浮導航", font=("微軟正黑體", 10, "bold"), fg="#1E3A8A", bg="#FFFFFF").pack(side="left")

        self.lbl_lyrics_sync_stat = tk.Label(s4_head, text=self.lyrics_mgr.last_sync_info, font=("微軟正黑體", 8), fg=self.c_muted, bg="#FFFFFF")
        self.lbl_lyrics_sync_stat.pack(side="right")

        # 本週詩歌清單卡片 (滿版橫向展開)
        song_info_card = tk.Frame(step4_card, bg="#F8FAFC", highlightbackground=self.c_border, highlightthickness=1)
        song_info_card.pack(fill="x", padx=12, pady=2)

        self.lbl_song_list = tk.Label(
            song_info_card,
            text=self.get_song_list_display(),
            font=("微軟正黑體", 8, "bold"),
            fg="#4338CA",
            bg="#F8FAFC",
            justify="left",
            anchor="w"
        )
        self.lbl_song_list.pack(fill="x", padx=8, pady=3)

        # 操作工具列：導航操作群 + 切換歌曲群 (整齊滿版橫排)
        tools_row = tk.Frame(step4_card, bg="#FFFFFF")
        tools_row.pack(fill="x", padx=12, pady=(3, 6))

        # 左側：導航按鈕 (已拿掉 F? 提示，更加清爽)
        make_button(tools_row, text="🌐 開啟雲端歌詞", bg=self.c_teal, fg="white", hover_bg=self.c_teal_hover, font=("微軟正黑體", 8, "bold"), padx=8, pady=4, command=self.btn_open_lyrics_web).pack(side="left", padx=(0, 3))
        make_button(tools_row, text="🚀 懸浮導航", bg="#2563EB", fg="white", hover_bg="#1D4ED8", font=("微軟正黑體", 8, "bold"), padx=8, pady=4, command=self.btn_start_lyrics_nav).pack(side="left", padx=2)
        make_button(tools_row, text="⏹ 關閉導航", bg="#64748B", fg="white", hover_bg="#475569", font=("微軟正黑體", 8, "bold"), padx=8, pady=4, command=self.btn_stop_lyrics_nav).pack(side="left", padx=2)
        make_button(tools_row, text="📐 視窗排版", bg="#0D9488", fg="white", hover_bg="#0F766E", font=("微軟正黑體", 8, "bold"), padx=8, pady=4, command=self.btn_snap_layout_clicked).pack(side="left", padx=2)
        make_button(tools_row, text="🔄 重載設定", bg="#F1F5F9", fg="#334155", hover_bg="#E2E8F0", font=("微軟正黑體", 8, "bold"), padx=6, pady=4, command=self.btn_reload_lyrics_config).pack(side="left", padx=2)

        # 右側：歌曲切換快捷鈕
        self.btn_song3 = make_button(tools_row, text="🎵 首 3", bg="#EEF2FF", fg="#3730A3", hover_bg="#E0E7FF", font=("微軟正黑體", 8, "bold"), padx=8, pady=3, command=lambda: self.switch_lyrics_song(3))
        self.btn_song3.pack(side="right", padx=2)

        self.btn_song2 = make_button(tools_row, text="🎵 首 2", bg="#EEF2FF", fg="#3730A3", hover_bg="#E0E7FF", font=("微軟正黑體", 8, "bold"), padx=8, pady=3, command=lambda: self.switch_lyrics_song(2))
        self.btn_song2.pack(side="right", padx=2)

        self.btn_song1 = make_button(tools_row, text="🎵 首 1", bg="#EEF2FF", fg="#3730A3", hover_bg="#E0E7FF", font=("微軟正黑體", 8, "bold"), padx=8, pady=3, command=lambda: self.switch_lyrics_song(1))
        self.btn_song1.pack(side="right", padx=2)

        tk.Label(tools_row, text="切換歌曲:", font=("微軟正黑體", 8, "bold"), fg=self.c_text, bg="#FFFFFF").pack(side="right", padx=(6, 4))

        # ==================== [底部] 即時日誌視窗 ====================
        log_frame = tk.Frame(self.root, bg=self.c_bg)
        log_frame.pack(fill="both", expand=True, padx=16, pady=(0, 8))

        log_head = tk.Frame(log_frame, bg=self.c_bg)
        log_head.pack(fill="x", pady=(0, 2))
        tk.Label(log_head, text="📜 即時系統日誌與同工提示:", font=("微軟正黑體", 8, "bold"), fg=self.c_text, bg=self.c_bg).pack(side="left")

        btn_clear_log = make_button(log_head, text="清空日誌", bg="#E2E8F0", fg="#334155", hover_bg="#CBD5E1", font=("微軟正黑體", 8), padx=6, pady=1, command=self.clear_log)
        btn_clear_log.pack(side="right")

        self.txt_log = tk.Text(
            log_frame,
            bg="#0F172A",
            fg="#F8FAFC",
            insertbackground="white",
            font=("Consolas", 8),
            height=6,
            relief="flat",
            bd=1,
            highlightbackground="#334155",
            highlightthickness=1
        )
        self.txt_log.pack(fill="both", expand=True)

        self.log("五常教會主日影音中控系統已啟動就緒。")

    def log(self, message):
        """寫入日誌訊息"""
        def _append():
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.txt_log.insert("end", f"[{timestamp}] {message}\n")
            self.txt_log.see("end")
        self.root.after(0, _append)

    def clear_log(self):
        self.txt_log.delete("1.0", "end")

    def auto_check_existing_files(self):
        """掃描 Downloads 資料夾中的最新 PPT 並自動解析講道題目"""
        self.log(f"正在掃描 {DOWNLOAD_DIR} 目錄中的最新主日檔案...")
        if not os.path.exists(DOWNLOAD_DIR):
            return

        pptx_candidates = []
        for f in os.listdir(DOWNLOAD_DIR):
            if f.endswith(".pptx") and not f.startswith("~$"):
                full_p = os.path.join(DOWNLOAD_DIR, f)
                pptx_candidates.append((full_p, os.path.getmtime(full_p)))

        if pptx_candidates:
            pptx_candidates.sort(key=lambda x: x[1], reverse=True)
            latest_pptx = pptx_candidates[0][0]
            self.current_pptx_path = latest_pptx
            fname = os.path.basename(latest_pptx)
            self.lbl_stat_ppt.config(text=f"● 主日 PPT: {fname}", fg="#16A34A")
            self.f_stat_ppt.config(bg="#F0FDF4", highlightbackground="#BBF7D0")
            self.lbl_stat_ppt.config(bg="#F0FDF4")
            self.log(f"已定位最新主日簡報: {fname}")

            # 解析講道題目與講員
            info = extract_sermon_info(latest_pptx)
            if info:
                self.current_title_info = info
                self.lbl_sermon_title.config(text=info["sermon_title"])
                self.lbl_preacher.config(text=info["preacher"])
                self.ent_yt_title.delete(0, "end")
                self.ent_yt_title.insert(0, info["youtube_title"])
                self.log(f"【成功解析】題目:「{info['sermon_title']}」 | 講員: {info['preacher']}")
                self.log(f"【直播建議標題】{info['youtube_title']}")

            m_date = re.search(r"(\d{8})", fname)
            if m_date:
                self.current_sunday_date = m_date.group(1)
                self.ent_date.delete(0, "end")
                self.ent_date.insert(0, self.current_sunday_date)
                self.lbl_head_date.config(text=f"📅 主日日期: {self.current_sunday_date}")
        else:
            self.lbl_stat_ppt.config(text="● 主日 PPT: 未發現", fg="#DC2626")
            self.f_stat_ppt.config(bg="#FEF2F2", highlightbackground="#FECACA")
            self.lbl_stat_ppt.config(bg="#FEF2F2")

        # 同步檢查並載入最新詩歌 config.txt
        if hasattr(self, "lyrics_mgr"):
            self.lyrics_mgr.sync_and_load_config()
            self.update_lyrics_ui_labels()

        self.refresh_devices_status()

    def refresh_devices_status(self):
        """重新整理手機與相機狀態"""
        def _worker():
            stat = check_devices()
            def _update():
                if stat.get("a27_usb"):
                    self.lbl_stat_a27.config(text="● 正面主鏡 A27: 已連線", fg="#16A34A", bg="#F0FDF4")
                    self.f_stat_a27.config(bg="#F0FDF4", highlightbackground="#BBF7D0")
                else:
                    self.lbl_stat_a27.config(text="● 正面主鏡 A27: 未連線", fg="#DC2626", bg="#FEF2F2")
                    self.f_stat_a27.config(bg="#FEF2F2", highlightbackground="#FECACA")

                if stat.get("asus_usb"):
                    self.lbl_stat_asus.config(text="● 會眾全景 ASUS: 已連線", fg="#16A34A", bg="#F0FDF4")
                    self.f_stat_asus.config(bg="#F0FDF4", highlightbackground="#BBF7D0")
                else:
                    self.lbl_stat_asus.config(text="● 會眾全景 ASUS: 未連線", fg="#DC2626", bg="#FEF2F2")
                    self.f_stat_asus.config(bg="#FEF2F2", highlightbackground="#FECACA")
            self.root.after(0, _update)

        threading.Thread(target=_worker, daemon=True).start()

    # ==================== 按鈕事件處理 ====================

    def btn_download_clicked(self):
        target_date = self.ent_date.get().strip() or None

        def _worker():
            self.log("="*60)
            if target_date:
                self.log(f"開始執行下載主日 ({target_date}) 附件 (來源: dayitea.tw@gmail.com)...")
            else:
                self.log("開始執行「下載最新主日附件」(來源: dayitea.tw@gmail.com)...")

            ok, files, actual_date = download_sunday_files(target_date=target_date, save_dir=DOWNLOAD_DIR, log_callback=self.log)
            if ok:
                self.log(f"主日資料備便成功 (日期: {actual_date})！")
                if actual_date:
                    self.current_sunday_date = actual_date
                    def _update_date():
                        self.ent_date.delete(0, "end")
                        self.ent_date.insert(0, actual_date)
                        self.lbl_head_date.config(text=f"📅 主日日期: {actual_date}")
                    self.root.after(0, _update_date)

                self.root.after(500, self.auto_check_existing_files)
                messagebox.showinfo("成功", f"已成功從 wang 取得主日 ({actual_date}) 檔案！\n共 {len(files)} 個檔案已儲存至 {DOWNLOAD_DIR}。\n系統已自動解析講道題目與講員。")
            else:
                self.log("[錯誤] 下載失敗，請檢查網路或郵件備份。")
                messagebox.showerror("下載失敗", "未能在寄件備份中找到 wang 寄出的主日信件！")

        threading.Thread(target=_worker, daemon=True).start()

    def btn_copy_title_clicked(self):
        title_text = self.ent_yt_title.get().strip()
        if not title_text:
            messagebox.showwarning("提示", "目前沒有直播標題可複製！")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(title_text)
        self.log(f"已複製直播標題至剪貼簿: {title_text}")
        messagebox.showinfo("複製成功", f"直播標題已成功複製到剪貼簿：\n\n{title_text}\n\n請直接至 YouTube 直播管理頁面貼上 (Ctrl+V)！")

    def btn_open_yt_clicked(self):
        self.log("正在開啟五常教會 YouTube 直播後台管理頁面...")
        webbrowser.open(YOUTUBE_LIVE_URL)

    def btn_run_ppt_clicked(self):
        if not self.current_pptx_path or not os.path.exists(self.current_pptx_path):
            messagebox.showwarning("提示", "找不到主日 PPT 檔案！請先執行步驟 2 下載或指定簡報檔案。")
            return

        def _worker():
            self.log("="*60)
            self.log(f"正在全螢幕啟動簡報放映: {os.path.basename(self.current_pptx_path)} ...")
            ok = start_slideshow(self.current_pptx_path, log_callback=self.log)
            if ok:
                # 自動將跳出的 PPT 簡報者檢視畫面移至螢幕右半側 50%，徹底解除全螢幕最大化，絕不蓋住中控台主程式
                try:
                    from window_layout_manager import dock_presenter_view_to_right
                    dock_presenter_view_to_right(log_callback=self.log, app_root=self.root)
                except Exception as e:
                    self.log(f"[PPT 投影] 檢視畫面自動定位提示: {e}")

        threading.Thread(target=_worker, daemon=True).start()

    # -------------------- 詩歌連動與 PPT 導航處理 --------------------
    def get_song_list_display(self):
        s1 = self.lyrics_mgr.songs.get(1, "未設定")
        s2 = self.lyrics_mgr.songs.get(2, "未設定")
        s3 = self.lyrics_mgr.songs.get(3, "未設定")
        return f"首 1: {s1}  |  首 2: {s2}  |  首 3: {s3}"

    def update_lyrics_ui_labels(self):
        if hasattr(self, "lbl_song_list"):
            self.lbl_song_list.config(text=self.get_song_list_display())
        if hasattr(self, "lbl_lyrics_sync_stat"):
            self.lbl_lyrics_sync_stat.config(text=self.lyrics_mgr.last_sync_info)
        s1 = self.lyrics_mgr.songs.get(1, "")
        s2 = self.lyrics_mgr.songs.get(2, "")
        s3 = self.lyrics_mgr.songs.get(3, "")
        if hasattr(self, "btn_song1"):
            t1 = f"🎵 首 1: {s1[:6]}" if s1 else "🎵 第 1 首"
            self.btn_song1.config(text=t1)
        if hasattr(self, "btn_song2"):
            t2 = f"🎵 首 2: {s2[:6]}" if s2 else "🎵 第 2 首"
            self.btn_song2.config(text=t2)
        if hasattr(self, "btn_song3"):
            t3 = f"🎵 首 3: {s3[:6]}" if s3 else "🎵 第 3 首"
            self.btn_song3.config(text=t3)
        self.update_active_song_button(self.lyrics_mgr.current_song)

    def update_active_song_button(self, active_num):
        btns = {1: getattr(self, "btn_song1", None), 2: getattr(self, "btn_song2", None), 3: getattr(self, "btn_song3", None)}
        for s_idx, b in btns.items():
            if b:
                if s_idx == active_num:
                    b.config(bg="#4338CA", fg="white")
                else:
                    b.config(bg="#EEF2FF", fg="#3730A3")

    def btn_open_lyrics_web(self):
        self.lyrics_mgr.sync_and_load_config()
        self.update_lyrics_ui_labels()
        self.lyrics_mgr.open_web_app()

        # 自動將開啟的雲端歌詞瀏覽器移至左上格 (50% 寬 x 50% 高)，解除最大化狀態，絕不蓋住中控台主程式
        def _dock_worker():
            try:
                from window_layout_manager import dock_lyrics_view_to_top_left
                dock_lyrics_view_to_top_left(log_callback=self.log, app_root=self.root)
            except Exception as e:
                self.log(f"[詩歌同步] 歌詞視窗定位提示: {e}")

        threading.Thread(target=_dock_worker, daemon=True).start()

    def btn_start_lyrics_nav(self):
        self.lyrics_mgr.start_floating_navigator(self.root)
        self.update_lyrics_ui_labels()

    def btn_stop_lyrics_nav(self):
        self.lyrics_mgr.stop_floating_navigator()

    def btn_snap_layout_clicked(self):
        """一鍵自動排版歸位 (點擊排版時與「開啟 Iriun Webcam」按鈕完全一致：直接執行路徑呼叫跳出桌面，確認鏡頭排序後一鍵歸位)"""
        from window_layout_manager import confirm_preflight_checklist, snap_sunday_layout

        # 1. 點擊排版按鈕時，與手動點擊「開啟 Iriun Webcam」按鈕完全相同：直接執行路徑呼叫！
        self.btn_iriun_clicked()

        # 2. 彈出前置作業檢核清單 (同工可一邊檢視桌面上的 Iriun 視窗與鏡頭排序，一邊核對清單)
        if not confirm_preflight_checklist(parent=self.root):
            self.log("[排版歸位] 同工已取消排版作業。")
            return

        # 3. 待同工檢查確認全部就緒後，開始執行四象限自動排版歸位
        def _worker():
            snap_sunday_layout(app_instance=self, log_callback=self.log, skip_confirm=True)
        threading.Thread(target=_worker, daemon=True).start()

    def btn_reload_lyrics_config(self):
        self.lyrics_mgr.sync_and_load_config()
        self.update_lyrics_ui_labels()
        self.log(f"[詩歌同步] 已手動重新整理設定檔！{self.lyrics_mgr.last_sync_info}")

    def switch_lyrics_song(self, song_num):
        self.lyrics_mgr.switch_song(song_num)
        self.update_active_song_button(song_num)
        try:
            from ppt_manager import focus_slideshow
            self.root.after(50, lambda: focus_slideshow(log_callback=self.log))
        except Exception:
            pass

    def btn_wake_clicked(self):
        def _worker():
            self.log("="*60)
            wake_all_cameras(log_callback=self.log)
            self.root.after(1000, self.refresh_devices_status)

        threading.Thread(target=_worker, daemon=True).start()

    def btn_sleep_clicked(self):
        if not messagebox.askyesno("確認休眠", "確定要讓正面主鏡與 ASUS 會眾機（安卓雙機）全部黑屏休眠嗎？\n(相機將完全關閉並停止發熱，後續可遠端直接喚醒)"):
            return

        def _worker():
            self.log("="*60)
            sleep_all_cameras(log_callback=self.log)
            self.root.after(1000, self.refresh_devices_status)

        threading.Thread(target=_worker, daemon=True).start()

    def auto_start_iriun(self):
        """啟動中控系統時，自動檢查並開啟電腦端 Iriun Webcam (若未在背景執行)"""
        if not is_iriun_running():
            self.log("偵測到電腦端 Iriun Webcam 尚未啟動，自動開啟中...")
            launch_iriun_webcam(log_callback=self.log)
        else:
            self.log("電腦端 Iriun Webcam 視訊服務已在背景正常執行。")

    def btn_iriun_clicked(self):
        self.log("="*60)
        self.log("正在開啟電腦端 Iriun Webcam 視窗...")
        launch_iriun_webcam(log_callback=self.log)

    def launch_scrcpy_instance(self, serial, port, title, extra_args=None):
        """啟動單一 scrcpy 實例 (自動定位打包路徑與配置通訊埠)"""
        scrcpy_bin = get_scrcpy_bin()
        scrcpy_dir = os.path.dirname(scrcpy_bin) if os.path.isabs(scrcpy_bin) else None

        cmd = [scrcpy_bin, "-s", serial, f"--port={port}", "--window-title", title]
        if extra_args:
            cmd.extend(extra_args)
        self.log(f"執行指令: {' '.join(cmd)}")

        env = os.environ.copy()
        path_dirs = []
        if scrcpy_dir and os.path.exists(scrcpy_dir):
            path_dirs.append(scrcpy_dir)
        path_dirs.append(r"C:\Program Files (x86)\Iriun Webcam")
        if "PATH" in env:
            path_dirs.append(env["PATH"])
        env["PATH"] = ";".join(path_dirs)

        try:
            proc = subprocess.Popen(
                cmd,
                cwd=scrcpy_dir if (scrcpy_dir and os.path.exists(scrcpy_dir)) else None,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
                text=True,
                encoding="utf-8",
                errors="replace"
            )

            def _monitor():
                for line in proc.stdout:
                    txt = line.strip()
                    if txt and ("ERROR" in txt or "WARN" in txt or "Device" in txt or "Connected" in txt):
                        self.log(f"[{title}] {txt}")
            threading.Thread(target=_monitor, daemon=True).start()

        except Exception as e:
            self.log(f"[啟動失敗] 無法啟動 scrcpy: {e}")
            messagebox.showerror("啟動失敗", f"無法啟動 scrcpy 投影視窗：\n{e}\n\n請確認手機已用 USB 線接上電腦並開啟 USB 偵錯。")

    def sub_wake_camera(self, target):
        def _worker():
            self.log("="*60)
            wake_single_camera(target, log_callback=self.log)
            self.root.after(1000, self.refresh_devices_status)
        threading.Thread(target=_worker, daemon=True).start()

    def sub_sleep_camera(self, target):
        name = "正面主鏡 A27" if target == "a27" else "會眾全景 ASUS"
        if not messagebox.askyesno("確認休眠", f"確定要讓【{name}】進入黑屏休眠嗎？\n(相機將完全關閉釋放、停止發熱，後續可單獨喚醒)"):
            return
        def _worker():
            self.log("="*60)
            sleep_single_camera(target, log_callback=self.log)
            self.root.after(1000, self.refresh_devices_status)
        threading.Thread(target=_worker, daemon=True).start()

    def sub_poweroff_camera(self, target):
        name = "正面主鏡 A27" if target == "a27" else "會眾全景 ASUS"
        if not messagebox.askyesno("確認徹底關機", f"【注意警語】\n確定要讓【{name}】手機徹底關閉電源嗎？\n\n手機關機（斷電）後無法透過電腦遠端開機，下次使用前同工必須走到腳架旁按手機實體開機鍵！\n\n(平常主日散會建議點選「休眠」即可，下週能遠端直接喚醒)"):
            return
        def _worker():
            self.log("="*60)
            poweroff_single_camera(target, log_callback=self.log)
            self.root.after(1500, self.refresh_devices_status)
        threading.Thread(target=_worker, daemon=True).start()

    def sub_scrcpy_camera(self, target):
        if target == "a27":
            self.log("="*60)
            self.log("正在啟動 A27 正面主鏡 (滾輪縮放 + 手機熄屏) 遠端操控視窗...")
            self.launch_scrcpy_instance(
                serial="R5GL91YT4BT",
                port="27185:27186",
                title="正面主鏡 A27 (滾輪變焦+熄屏防燙)",
                extra_args=["--turn-screen-off", "--stay-awake"]
            )
        else:
            self.log("="*60)
            self.log("正在啟動 ASUS 會眾全景 (滑鼠對焦 + 手機熄屏) 遠端操控視窗...")
            self.launch_scrcpy_instance(
                serial="M8AIB760S073JRK",
                port="27183:27184",
                title="會眾全景 ASUS (滑鼠對焦+熄屏防燙)",
                extra_args=["--turn-screen-off", "--stay-awake"]
            )

    def btn_scrcpy_a27_clicked(self):
        self.log("="*60)
        self.log("正在啟動 Samsung Galaxy A27 (正面主鏡) 螢幕畫面監控...")
        self.launch_scrcpy_instance(
            serial="R5GL91YT4BT",
            port="27185:27186",
            title="正面主鏡 Galaxy A27 (USB有線)"
        )

    def btn_scrcpy_asus_clicked(self):
        self.log("="*60)
        self.log("正在啟動 ASUS (會眾全景) 螢幕畫面監控...")
        self.launch_scrcpy_instance(
            serial="M8AIB760S073JRK",
            port="27183:27184",
            title="會眾全景 ASUS (USB有線)"
        )

    def btn_scrcpy_dual_clicked(self):
        def _worker():
            self.log("="*60)
            self.log("【雙手機監控】正在啟動雙機 scrcpy 畫面監控...")
            self.log("[1/2] 正在開啟 ASUS (會眾全景)...")
            self.launch_scrcpy_instance(
                serial="M8AIB760S073JRK",
                port="27183:27184",
                title="會眾全景 ASUS (USB有線)"
            )
            time.sleep(2)
            self.log("[2/2] 正在開啟 Samsung Galaxy A27 (正面主鏡)...")
            self.launch_scrcpy_instance(
                serial="R5GL91YT4BT",
                port="27185:27186",
                title="正面主鏡 Galaxy A27 (USB有線)"
            )
            time.sleep(1)
            self.log("="*60)
            self.log("[完成] 兩台手機投影視窗已全部啟動！")
        threading.Thread(target=_worker, daemon=True).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = ChurchAutomationApp(root)
    root.mainloop()
