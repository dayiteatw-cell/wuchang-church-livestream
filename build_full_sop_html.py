# -*- coding: utf-8 -*-
"""
五常基督長老教會 主日同工影音投影與直播全流程操作手冊 (SOP) HTML 生成腳本
更新內容：
1. 移除步驟 1 的【延伸螢幕確認】提示框。
2. 移除步驟 2 的【實測免喚醒特性】提示框。
3. 截圖 20 說明修改為：「畫面中紅色圓角框為相機的「🔍 操控」按鈕。同工點擊此按鈕即可透過電腦遠端開啟安卓手機操作視窗！」
4. 2-2 標題改為：「2-2：開啟手機 Iriun Webcam（iPhone 則手輕觸螢幕開啟）」
   - iPhone: 側面副鏡 iPhone X：由同工手輕觸螢幕點擊開啟 Iriun Webcam App 圖示（如下圖）：
   - 安卓: 安卓手機由【截圖 01】A27 電腦操控手機螢幕和【截圖 02】ASUS 電腦操控手機螢幕，從電腦操控打開 Iriun Webcam
   - 截圖 01 & 02 描述改為：「點擊 Iriun Webcam 圖示」
5. 全文語言風格極致簡潔、口語化、精準無贅字。
"""

import os
import base64

BASE_DIR = r"E:\Antigravity_Data\五常教會直播設置"
ASSETS_DIR = os.path.join(BASE_DIR, "照片素材")
OUTPUT_HTML = os.path.join(BASE_DIR, "五常教會主日同工投影與直播教學手冊.html")
OUTPUT_HTML_SYS = os.path.join(BASE_DIR, "五常教會主日影音中控系統", "五常教會主日同工投影與直播教學手冊.html")
LOGO_PATH = os.path.join(BASE_DIR, "五常教會主日影音中控系統", "assets", "church_logo.png")

IMAGES_INFO = [
    ("01_A27_手機桌面.png", "【截圖 01】A27 電腦操控手機螢幕", "點擊 Iriun Webcam 圖示"),
    ("02_ASUS_手機桌面.png", "【截圖 02】ASUS 電腦操控手機螢幕", "點擊 Iriun Webcam 圖示"),
    ("03_A27_多工切換.png", "A27 多工切換預覽 Iriun Webcam", "Iriun Webcam 於背景執行"),
    ("04_A27_Iriun等待連線提示.png", "A27 Iriun 橫向等待連線提示", "提示 Waiting for the connection 正在握手"),
    ("05_A27_Iriun即時畫面_講台十字架.png", "正面主鏡 A27 即時畫面（講台十字架）", "講台正面平視，十字架居中"),
    ("06_ASUS_多工預覽.png", "ASUS 多工直立預覽 Iriun Webcam", "ASUS 機身準備好 Iriun 應用"),
    ("07_A27_Iriun連線提示重整.png", "A27 橫向 Iriun 重新連線提示", "自動重連提示"),
    ("08_ASUS_多工預覽狀態.png", "ASUS 多工預覽狀態確認", "確保 Iriun 處於待命狀態"),
    ("09_ASUS_Iriun已連線會眾全景.png", "會眾全景 ASUS 即時畫面（全場俯拍）", "後方高處俯拍會眾席全景"),
    ("10_Iriun電腦端_Camera1_A27.png", "Iriun 電腦端 Camera 1 鎖定 Samsung SM-A2760 [USB]", "【關鍵鎖定】Camera 1 必須為 Galaxy A27"),
    ("11_Iriun電腦端_Camera2_iPhoneX.png", "Iriun 電腦端 Camera 2 鎖定 iPhone [USB] 側面講台", "【關鍵鎖定】Camera 2 必須為桌邊 iPhone X"),
    ("12_Iriun電腦端_Camera3_ASUS.png", "Iriun 電腦端 Camera 3 鎖定 Asus ASUS_I006D [USB] 會眾全景", "【關鍵鎖定】Camera 3 必須為 ASUS"),
    ("13_OBS介面_主日敬拜正面主鏡.png", "OBS 33.0 正面主鏡預覽與台標跑馬燈", "左下五常台標與跑馬燈，維持 60.00 FPS"),
    ("14_OBS場景清單_下半段_F1至F4快捷鍵.png", "OBS 快捷鍵鏡頭清單（F1~F4、PPT滿版）", "F1 主鏡、F2 PPT、F3 側鏡、F4 全景"),
    ("15_OBS場景清單_上半段_畫面與鏡頭庫.png", "OBS 場景上半段（禮拜即將開始圖卡）", "禮拜即將開始待機字卡"),
    ("16_OBS音效混音器_音訊軌道.png", "OBS 音效混音器（預設紅色靜音）", "輸出音效 2、麥克風/輸入音效 1"),
    ("17_OBS_點擊開始串流按鈕.png", "【截圖 17】點擊開始串流", "勾選排程後，點擊紅框「開始串流」按鈕正式推流直播"),
    ("17_OBS控制項面板_開始串流與直播管理.png", "OBS 控制項面板（開始串流、開始錄製）", "管理直播與開始串流推流"),
    ("18_OBS未設定直播提示視窗.png", "OBS 未設定直播防呆提示視窗", "未綁定直播時的防呆提示"),
    ("19_OBS_YouTube直播設定與排程選擇.png", "OBS 選擇現有 YouTube 排程直播", "勾選當週主日活動並套用"),
    ("20_五常總控台_完整主介面.png", "總控台主介面（紅圈標註【🔍 操控】）", "畫面中紅色圓角框為相機的「🔍 操控」按鈕。同工點擊此按鈕即可透過電腦遠端開啟安卓手機操作視窗！"),
    ("21_五常中控系統_桌面捷徑圖示.png", "中控系統桌面捷徑圖示", "雙擊桌面捷徑啟動中控系統"),
    ("22_雲端同步歌詞_瀏覽器顯示頁.png", "雲端同步歌詞顯示頁（主歌/副歌自動切換）", "網址 sync-lyrics-app.onrender.com"),
    ("23_詩歌PPT懸浮導航視窗.png", "詩歌 PPT 懸浮導航視窗（歌詞同步中 [1_V]）", "置頂小視窗，提示下一張投影片編號"),
    ("24_五常總控台_步驟1至步驟4操作區.png", "總控台核心步驟 1～4 操作面板", "相機、標題、PPT放映、歌詞導航與視窗排版"),
    ("25_主日開場檢核清單對話框.png", "主日開場檢核清單對話框", "確認直播與相機後按 Enter 啟動排版"),
    ("26_YouTube頻道直播管理後台.png", "YouTube Studio 頻道直播管理後台", "核對當週主日排程活動"),
    ("27_YouTube影片詳細資料_直播標題設定.png", "YouTube Studio 貼上直播標題", "貼上中控系統複製之標準標題"),
    ("28_主日直播多視窗黃金四分割工作配置.png", "主日同工黃金四分割工作台標準螢幕配置", "左上歌詞、左下相機導航、右半演講者檢視"),
    ("29_手機多工向上滑動關閉Iriun.png", "【截圖 29】手機多工滑動關閉 Iriun Webcam", "重新以電腦操控安卓手機，滑鼠向上滑動關閉 Iriun Webcam App；iPhone 輕觸畫面向上滑關閉"),
    ("30_Iriun_三橫線解析度調整選單.png", "【Iriun 選單】三橫線解析度切換", "點擊左上角三橫線選單切換解析度以重整傳輸流")
]

NEW_IMAGES_INFO = [
    ("00_天花板USB面板_充電與訊號切換.jpg", "天花板 USB 面板插孔對照", "紅記號為【充電】，無記號為【連接電腦訊號】"),
    ("00_Iriun_App圖示.png", "Iriun Webcam 手機端 App 圖示", "iPhone 側面副鏡請同工手輕觸此圖示開啟")
]

def load_b64(filepath):
    if not os.path.exists(filepath):
        print(f"[警告] 找不到檔案: {filepath}")
        return ""
    with open(filepath, "rb") as f:
        data = f.read()
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".png":
        mime = "image/png"
    elif ext in [".jpg", ".jpeg"]:
        mime = "image/jpeg"
    else:
        mime = "application/octet-stream"
    return f"data:{mime};base64," + base64.b64encode(data).decode("utf-8")

def main():
    print("正在編碼截圖與素材為 Base64...")
    b64_map = {}
    for filename, title, desc in IMAGES_INFO:
        p = os.path.join(ASSETS_DIR, filename)
        b64_map[filename] = load_b64(p)
    
    for filename, title, desc in NEW_IMAGES_INFO:
        p = os.path.join(ASSETS_DIR, filename)
        b64_map[filename] = load_b64(p)

    logo_b64 = load_b64(LOGO_PATH)

    print("正在組合極簡口語化 SOP HTML...")

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>五常基督長老教會・主日同工影音投影與直播全流程操作手冊 (SOP)</title>
    <style>
        :root {{
            --primary: #0D9488;
            --primary-dark: #0F766E;
            --primary-light: #F0FDFA;
            --secondary: #1E3A8A;
            --secondary-dark: #172554;
            --secondary-light: #EFF6FF;
            --accent: #2563EB;
            --danger: #E11D48;
            --danger-light: #FFF1F2;
            --warning: #D97706;
            --warning-light: #FEF3C7;
            --success: #059669;
            --success-light: #ECFDF5;
            --text-main: #0F172A;
            --text-sub: #334155;
            --text-muted: #64748B;
            --bg-page: #F8FAFC;
            --bg-card: #FFFFFF;
            --border-color: #E2E8F0;
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.05);
            --shadow-md: 0 4px 16px rgba(0,0,0,0.07);
            --shadow-lg: 0 10px 30px rgba(0,0,0,0.12);
            --radius-sm: 8px;
            --radius-md: 14px;
            --radius-lg: 20px;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft JhengHei", 微軟正黑體, Roboto, sans-serif;
            background-color: var(--bg-page);
            color: var(--text-main);
            line-height: 1.7;
            padding: 24px 16px 80px 16px;
            -webkit-font-smoothing: antialiased;
        }}

        .wrapper {{
            max-width: 1140px;
            margin: 0 auto;
        }}

        /* 頁頂橫幅 Hero Header */
        .hero-header {{
            background: linear-gradient(135deg, #0F766E 0%, #0D9488 45%, #1E3A8A 100%);
            color: white;
            border-radius: var(--radius-lg);
            padding: 36px 44px;
            box-shadow: var(--shadow-lg);
            position: relative;
            overflow: hidden;
            margin-bottom: 24px;
        }}

        .header-top {{
            display: flex;
            align-items: center;
            gap: 20px;
            flex-wrap: wrap;
        }}

        .header-logo {{
            width: 80px;
            height: 80px;
            background: white;
            padding: 6px;
            border-radius: 18px;
            box-shadow: 0 6px 16px rgba(0,0,0,0.2);
            flex-shrink: 0;
        }}

        .header-text h1 {{
            font-size: 26px;
            font-weight: 800;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }}

        .header-text p.sub {{
            font-size: 15px;
            color: #CCFBF1;
            font-weight: 500;
        }}

        .header-badges {{
            display: flex;
            gap: 10px;
            margin-top: 18px;
            flex-wrap: wrap;
        }}

        .badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(255,255,255,0.2);
            backdrop-filter: blur(8px);
            padding: 5px 13px;
            border-radius: 30px;
            font-size: 13px;
            font-weight: 600;
            border: 1px solid rgba(255,255,255,0.3);
        }}

        /* 導航列 */
        .sticky-nav {{
            position: sticky;
            top: 12px;
            z-index: 99;
            background: rgba(255, 255, 255, 0.96);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border-color);
            border-radius: 50px;
            box-shadow: var(--shadow-md);
            padding: 8px 16px;
            margin-bottom: 28px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            overflow-x: auto;
            gap: 6px;
        }}

        .nav-links {{
            display: flex;
            gap: 4px;
            white-space: nowrap;
        }}

        .nav-link {{
            padding: 6px 13px;
            border-radius: 20px;
            text-decoration: none;
            color: var(--text-sub);
            font-size: 13px;
            font-weight: 700;
            transition: all 0.2s ease;
        }}

        .nav-link:hover, .nav-link.active {{
            background: var(--primary);
            color: white;
        }}

        .btn-action {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 14px;
            background: var(--secondary);
            color: white;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            border: none;
            cursor: pointer;
            text-decoration: none;
            transition: opacity 0.2s ease;
            white-space: nowrap;
        }}

        .btn-action:hover {{
            opacity: 0.9;
        }}

        /* 章節卡片 */
        .section-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-md);
            padding: 32px 36px;
            margin-bottom: 28px;
        }}

        .section-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 2px solid var(--primary-light);
            padding-bottom: 14px;
            margin-bottom: 20px;
            flex-wrap: wrap;
            gap: 12px;
        }}

        .section-title-wrap {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .step-num {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 19px;
            font-weight: 800;
            flex-shrink: 0;
        }}

        .section-title {{
            font-size: 21px;
            font-weight: 800;
            color: var(--secondary-dark);
        }}

        .section-tag {{
            background: var(--secondary-light);
            color: var(--secondary);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 800;
            border: 1px solid #BFDBFE;
        }}

        .step-block {{
            margin-bottom: 28px;
        }}

        .step-block h4 {{
            font-size: 16.5px;
            font-weight: 700;
            color: var(--text-main);
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .step-block h4::before {{
            content: "";
            display: inline-block;
            width: 6px;
            height: 15px;
            background: var(--primary);
            border-radius: 3px;
        }}

        /* 圖片卡片 */
        .image-card {{
            background: #F1F5F9;
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            overflow: hidden;
            box-shadow: var(--shadow-sm);
            margin: 14px 0 20px 0;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}

        .image-card:hover {{
            box-shadow: var(--shadow-md);
        }}

        .image-card-header {{
            background: white;
            padding: 9px 15px;
            font-size: 13.5px;
            font-weight: 700;
            color: var(--text-sub);
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .image-card-header .img-tag {{
            background: var(--primary-light);
            color: var(--primary-dark);
            padding: 2px 8px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 800;
        }}

        .image-card-body {{
            position: relative;
            background: #0F172A;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: zoom-in;
            min-height: 180px;
            overflow: hidden;
        }}

        .image-card-body img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 0 auto;
            transition: transform 0.2s ease;
        }}

        .image-card-body:hover img {{
            transform: scale(1.015);
        }}

        .image-card-body::after {{
            content: "🔍 點擊放大查看細節";
            position: absolute;
            bottom: 8px;
            right: 12px;
            background: rgba(0,0,0,0.7);
            color: white;
            font-size: 11px;
            padding: 3px 9px;
            border-radius: 20px;
            opacity: 0;
            transition: opacity 0.2s ease;
            pointer-events: none;
        }}

        .image-card-body:hover::after {{
            opacity: 1;
        }}

        .image-card-desc {{
            background: white;
            padding: 11px 16px;
            font-size: 13.5px;
            color: var(--text-sub);
            border-top: 1px solid var(--border-color);
            line-height: 1.6;
        }}

        .grid-2 {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(440px, 1fr));
            gap: 18px;
        }}

        .grid-3 {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(310px, 1fr));
            gap: 16px;
        }}

        kbd {{
            display: inline-block;
            background: #F1F5F9;
            border: 1px solid #CBD5E1;
            border-bottom: 2px solid #94A3B8;
            border-radius: 5px;
            padding: 2px 7px;
            font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
            font-size: 12px;
            font-weight: 700;
            color: var(--secondary-dark);
        }}

        table.sop-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 14px 0 20px 0;
            font-size: 13.5px;
        }}

        table.sop-table th, table.sop-table td {{
            padding: 10px 14px;
            border: 1px solid var(--border-color);
            text-align: left;
        }}

        table.sop-table th {{
            background: #F8FAFC;
            color: var(--secondary-dark);
            font-weight: 700;
        }}

        table.sop-table tr:nth-child(even) {{
            background: #F8FAFC;
        }}

        .alert-warning {{
            background: var(--warning-light);
            border-left: 4px solid var(--warning);
            color: #92400E;
            padding: 14px 18px;
            border-radius: var(--radius-md);
            margin: 16px 0;
            font-size: 14px;
        }}

        /* 圖片放大燈箱 */
        .modal {{
            display: none;
            position: fixed;
            z-index: 9999;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.88);
            backdrop-filter: blur(6px);
            align-items: center;
            justify-content: center;
            flex-direction: column;
            padding: 24px;
        }}

        .modal.active {{
            display: flex;
        }}

        .modal-img-wrap {{
            max-width: 95%;
            max-height: 85%;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }}

        .modal-img-wrap img {{
            max-width: 100%;
            max-height: 85vh;
            border-radius: 8px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
            object-fit: contain;
        }}

        .modal-caption {{
            color: #F8FAFC;
            margin-top: 14px;
            font-size: 15px;
            font-weight: 600;
            text-align: center;
            max-width: 800px;
        }}

        .modal-close {{
            position: absolute;
            top: 20px;
            right: 28px;
            color: white;
            font-size: 36px;
            font-weight: 300;
            cursor: pointer;
            line-height: 1;
        }}

        .modal-close:hover {{
            color: #5EEAD4;
        }}

        @media (max-width: 768px) {{
            .hero-header {{
                padding: 24px 20px;
            }}
            .section-card {{
                padding: 20px 16px;
            }}
            .grid-2, .grid-3 {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>

<div class="wrapper">

    <!-- 頁頂橫幅 -->
    <header class="hero-header">
        <div class="header-top">
            <img class="header-logo" src="{logo_b64}" alt="五常教會 LOGO">
            <div class="header-text">
                <h1>五常基督長老教會・主日同工影音投影與直播全流程操作手冊 (SOP)</h1>
                <p class="sub">線源改插訊號 ➔ 啟動電腦桌面中控相機 ➔ 一鍵下載主日附件與主日標題設定 ➔ OBS串流 ➔ PPT大投影 ➔ 四分割視窗工作台 ➔ 崇拜實戰切換 ➔ 散會休眠</p>
            </div>
        </div>
        <!-- 給服事同工的話 -->
        <div class="workers-message-box" style="margin-top: 18px; max-width: 960px; margin-left: auto; margin-right: auto; background: rgba(255, 255, 255, 0.15); backdrop-filter: blur(8px); border: 1.5px solid rgba(255, 255, 255, 0.35); border-radius: 12px; padding: 18px 24px; text-align: left; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);">

            <p style="font-size: 14.5px; line-height: 1.85; color: #FFFFFF; margin: 0; text-shadow: 0 1px 2px rgba(0,0,0,0.2);">
                親愛的影音同工平安！為維持每週主日直播一致的標準作業流程（SOP），並確保線上禮拜的影音最高品質，我們特別將中控系統全面自動化，精簡了各項繁雜的操作步驟（如自動下載主日附件、OBS 場景依翻頁與計時計數自動切換，避免手動切換遺漏），且天花板相機鏡頭已全面固定定位避免誤觸移位。期盼同工們服事前能完整瀏覽並熟悉這份教學 SOP，讓我們同心合意、安心順暢地服事神與眾弟兄姊妹！
            </p>
        </div>
    </header>

    <!-- 導航列 -->
    <nav class="sticky-nav">
        <div class="nav-links">
            <a href="#step-1" class="nav-link">步驟 1. 線源改插訊號孔</a>
            <a href="#step-2" class="nav-link">步驟 2. 中控操控相機</a>
            <a href="#step-3" class="nav-link">步驟 3. 複製主日標題</a>
            <a href="#step-4" class="nav-link">步驟 4. 貼上後台標題</a>
            <a href="#step-5" class="nav-link">步驟 5. PPT放映與雲端歌詞</a>
            <a href="#step-6" class="nav-link">步驟 6. 四分割工作台</a>
            <a href="#step-7" class="nav-link">步驟 7. OBS排程與串流</a>
            <a href="#step-8" class="nav-link">步驟 8. 崇拜實戰鏡頭切換</a>
            <a href="#step-9" class="nav-link">步驟 9. 散會休眠關機</a>
            <a href="#step-faq" class="nav-link">故障排除 FAQ</a>
        </div>
        <button class="btn-action" onclick="window.print()">🖨️ 列印 / 另存 PDF</button>
    </nav>

    <!-- 步驟一：線源由充電改插連接電腦訊號線 -->
    <section id="step-1" class="section-card">
        <div class="section-header">
            <div class="section-title-wrap">
                <span class="step-num">1</span>
                <h2 class="section-title">將二隻安卓手機的線源，由充電改插連接電腦訊號線，紅色記號的插孔為充電，無記號為連接電腦訊號</h2>
            </div>
            <span class="section-tag">硬體線源切換</span>
        </div>

        <p style="font-size: 15px; margin-bottom: 12px; font-weight: 600;">
            將二隻安卓手機的線源，由充電改插連接電腦訊號線，紅色記號的插孔為充電，無記號為連接電腦訊號。
        </p>

        <div style="background: #FEF2F2; border: 1.5px solid #FCA5A5; border-radius: 8px; padding: 10px 16px; margin-bottom: 14px; color: #991B1B; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 8px;">
            <span>⚠️</span>
            <span>【重要提醒】切換線源僅在「面板端」插拔，請勿插拔或拉扯手機端線路，以避免相機移位與視角跑掉！</span>
        </div>

        <div class="image-card" style="max-width: 600px; margin: 16px auto;">
            <div class="image-card-header">
                <span>【實機面板】天花板 USB 面板插孔對照</span>
                <span class="img-tag" style="background:#FEE2E2; color:#B91C1C;">重要插孔識別</span>
            </div>
            <div class="image-card-body" onclick="openModal('{b64_map['00_天花板USB面板_充電與訊號切換.jpg']}', '【實機面板】天花板 USB 面板：紅色記號為充電，無記號為連接電腦訊號')">
                <img src="{b64_map['00_天花板USB面板_充電與訊號切換.jpg']}" alt="天花板 USB 面板插孔對照">
            </div>
            <div class="image-card-desc">
                🔴 <strong>紅色記號插孔</strong>：為<strong>【平日獨立充電】</strong>（平日插在此孔維持電力）。<br>
                ⚪ <strong>無記號插孔</strong>：為<strong>【連接電腦訊號】</strong>（主日聚會專用，直通音控電腦傳輸視訊）。<br>
                👉 <strong>動作</strong>：將正面主鏡 (A27) 與會眾全景 (ASUS) 的線，從紅色充電孔拔下，<strong>改插到下方的「無記號電腦訊號孔」</strong>！<br>
                🚫 <strong>請勿插拔手機端線路</strong>：切換時僅插拔此面板插孔，請勿觸碰或拉扯手機端接線，以防相機機位移位。
            </div>
        </div>
    </section>

    <!-- 步驟二：啟動中控系統・操控相機與通道鎖定 -->
    <section id="step-2" class="section-card">
        <div class="section-header">
            <div class="section-title-wrap">
                <span class="step-num">2</span>
                <h2 class="section-title">啟動中控系統・操控相機與通道鎖定</h2>
            </div>
            <span class="section-tag">相機操控與鎖定</span>
        </div>

        <div class="step-block">
            <h4>2-1：開啟桌面中控台</h4>
            <div class="grid-2">
                <div class="image-card">
                    <div class="image-card-header">
                        <span>【截圖 21】桌面中控系統圖示</span>
                        <span class="img-tag">桌面啟動</span>
                    </div>
                    <div class="image-card-body" onclick="openModal('{b64_map['21_五常中控系統_桌面捷徑圖示.png']}', '【截圖 21】五常教會主日影音中控系統.exe 桌面捷徑')">
                        <img src="{b64_map['21_五常中控系統_桌面捷徑圖示.png']}" alt="桌面中控圖示">
                    </div>
                    <div class="image-card-desc">
                        在電腦桌面雙擊<strong>「五常教會主日影音中控系統」</strong>捷徑。
                    </div>
                </div>
                <div class="image-card">
                    <div class="image-card-header">
                        <span>【截圖 20】總控台主介面</span>
                        <span class="img-tag" style="background:#FEE2E2; color:#B91C1C;">紅圈標註</span>
                    </div>
                    <div class="image-card-body" onclick="openModal('{b64_map['20_五常總控台_完整主介面.png']}', '【截圖 20】總控台主介面：畫面中紅色圓角框為相機的「🔍 操控」按鈕。同工點擊此按鈕即可透過電腦遠端開啟安卓手機操作視窗！')">
                        <img src="{b64_map['20_五常總控台_完整主介面.png']}" alt="總控台主介面標註">
                    </div>
                    <div class="image-card-desc">
                        畫面中紅色圓角框為相機的「🔍 操控」按鈕。同工點擊此按鈕即可透過電腦遠端開啟安卓手機操作視窗！
                    </div>
                </div>
            </div>
        </div>

        <div class="step-block">
            <h4>2-2：開啟手機 Iriun Webcam（iPhone 則手輕觸螢幕開啟）</h4>
            <p style="font-size: 14.5px; margin-bottom: 8px; font-weight: 600;">
                側面副鏡 iPhone X：由同工手輕觸螢幕點擊開啟 Iriun Webcam App 圖示（如下圖）：
            </p>

            <div class="image-card" style="max-width: 320px; margin: 12px auto;">
                <div class="image-card-header">
                    <span>【圖 2】Iriun Webcam 手機 App 圖示</span>
                    <span class="img-tag" style="background:#DBEAFE; color:#1E40AF;">iPhone 輕觸開啟</span>
                </div>
                <div class="image-card-body" style="background:#1E293B;" onclick="openModal('{b64_map['00_Iriun_App圖示.png']}', '【圖 2】iPhone 側面副鏡請同工手輕觸此藍色 Iriun Webcam 圖示開啟')">
                    <img src="{b64_map['00_Iriun_App圖示.png']}" alt="Iriun App 圖示" style="max-width: 100px; padding: 16px;">
                </div>
                <div class="image-card-desc" style="text-align: center;">
                    輕觸此藍色圓形相機圖示開啟 Iriun Webcam。
                </div>
            </div>

            <p style="font-size: 14.5px; margin: 16px 0 8px 0;">
                <strong>安卓手機由【截圖 01】A27 電腦操控手機螢幕和【截圖 02】ASUS 電腦操控手機螢幕，從電腦操控打開 Iriun Webcam：</strong>
            </p>
            <div class="grid-2">
                <div class="image-card">
                    <div class="image-card-header">
                        <span>【截圖 01】A27 電腦操控手機螢幕</span>
                        <span class="img-tag">A27 手機螢幕</span>
                    </div>
                    <div class="image-card-body" onclick="openModal('{b64_map['01_A27_手機桌面.png']}', '【截圖 01】A27 電腦操控手機螢幕：點擊 Iriun Webcam 圖示')">
                        <img src="{b64_map['01_A27_手機桌面.png']}" alt="A27 手機桌面">
                    </div>
                    <div class="image-card-desc">
                        點擊 Iriun Webcam 圖示
                    </div>
                </div>

                <div class="image-card">
                    <div class="image-card-header">
                        <span>【截圖 02】ASUS 電腦操控手機螢幕</span>
                        <span class="img-tag">ASUS 手機螢幕</span>
                    </div>
                    <div class="image-card-body" onclick="openModal('{b64_map['02_ASUS_手機桌面.png']}', '【截圖 02】ASUS 電腦操控手機螢幕：點擊 Iriun Webcam 圖示')">
                        <img src="{b64_map['02_ASUS_手機桌面.png']}" alt="ASUS 手機桌面">
                    </div>
                    <div class="image-card-desc">
                        點擊 Iriun Webcam 圖示
                    </div>
                </div>
            </div>

            <div class="grid-2" style="margin-top: 16px;">
                <div class="image-card">
                    <div class="image-card-header">
                        <span>【截圖 05】正面主鏡 A27 即時畫面連線成功</span>
                        <span class="img-tag">正面主鏡就緒</span>
                    </div>
                    <div class="image-card-body" onclick="openModal('{b64_map['05_A27_Iriun即時畫面_講台十字架.png']}', '【截圖 05】正面主鏡即時畫面：講台十字架正面平視')">
                        <img src="{b64_map['05_A27_Iriun即時畫面_講台十字架.png']}" alt="正面主鏡連線成功">
                    </div>
                    <div class="image-card-desc">
                        講台正面平視，十字架居中。
                    </div>
                </div>
                <div class="image-card">
                    <div class="image-card-header">
                        <span>【截圖 09】會眾全景 ASUS 即時畫面連線成功</span>
                        <span class="img-tag">會眾全景就緒</span>
                    </div>
                    <div class="image-card-body" onclick="openModal('{b64_map['09_ASUS_Iriun已連線會眾全景.png']}', '【截圖 09】會眾全景即時畫面：後方高處俯拍座椅全景')">
                        <img src="{b64_map['09_ASUS_Iriun已連線會眾全景.png']}" alt="會眾全景連線成功">
                    </div>
                    <div class="image-card-desc">
                        後方高處俯拍會眾席全景。
                    </div>
                </div>
            </div>
        </div>

        <div class="step-block">
            <h4>2-3：電腦端 Iriun Webcam 視窗核對通道（重要！）</h4>
            <div class="grid-3">
                <div class="image-card">
                    <div class="image-card-header">
                        <span>【截圖 10】Camera #1</span>
                        <span class="img-tag">通道 #1</span>
                    </div>
                    <div class="image-card-body" onclick="openModal('{b64_map['10_Iriun電腦端_Camera1_A27.png']}', '【截圖 10】Camera 1 必須為 Samsung SM-A2760 [USB]')">
                        <img src="{b64_map['10_Iriun電腦端_Camera1_A27.png']}" alt="Camera 1 A27">
                    </div>
                    <div class="image-card-desc">
                        <strong>必須鎖定：</strong><code>Samsung SM-A2760 [USB]</code><br>正面主鏡講台。
                    </div>
                </div>
                <div class="image-card">
                    <div class="image-card-header">
                        <span>【截圖 11】Camera #2</span>
                        <span class="img-tag">通道 #2</span>
                    </div>
                    <div class="image-card-body" onclick="openModal('{b64_map['11_Iriun電腦端_Camera2_iPhoneX.png']}', '【截圖 11】Camera 2 必須為 iPhone [USB]')">
                        <img src="{b64_map['11_Iriun電腦端_Camera2_iPhoneX.png']}" alt="Camera 2 iPhoneX">
                    </div>
                    <div class="image-card-desc">
                        <strong>必須鎖定：</strong><code>iPhone [USB]</code><br>桌邊 iPhone X 側面特寫。
                    </div>
                </div>
                <div class="image-card">
                    <div class="image-card-header">
                        <span>【截圖 12】Camera #3</span>
                        <span class="img-tag">通道 #3</span>
                    </div>
                    <div class="image-card-body" onclick="openModal('{b64_map['12_Iriun電腦端_Camera3_ASUS.png']}', '【截圖 12】Camera 3 必須為 Asus ASUS_I006D [USB]')">
                        <img src="{b64_map['12_Iriun電腦端_Camera3_ASUS.png']}" alt="Camera 3 ASUS">
                    </div>
                    <div class="image-card-desc">
                        <strong>必須鎖定：</strong><code>Asus ASUS_I006D [USB]</code><br>後方 ASUS 會眾全景。
                    </div>
                </div>
            </div>
            <p style="font-size: 14.5px; margin-top: 14px; color: var(--secondary-dark); font-weight: 700;">
                👉 順序可由中間框起來下拉調整順序。
            </p>
        </div>


    </section>

    <!-- 步驟三：下載主日附件與複製標題 -->
    <section id="step-3" class="section-card">
        <div class="section-header">
            <div class="section-title-wrap">
                <span class="step-num">3</span>
                <h2 class="section-title">下載主日附件，並自動生成標題，一鍵複製 ➔ 貼上 YouTube 直播標題</h2>
            </div>
            <span class="section-tag">附件下載與標題複製</span>
        </div>

        <p style="font-size: 15px; margin-bottom: 14px; font-weight: 600; color: var(--secondary-dark);">
            先確認主日日期是否為當日（可手動更改），無誤後點擊<strong>【下載主日附件】</strong>（圖示紅框）。系統自動生成標題後，點擊<strong>【複製】</strong>，再點擊<strong>【開啟後台】</strong>（紅框標註）。
        </p>
        <div class="image-card">
            <div class="image-card-header">
                <span>【截圖 24】總控台步驟 2 操作面板</span>
                <span class="img-tag" style="background:#FEE2E2; color:#B91C1C;">紅框標註操作</span>
            </div>
            <div class="image-card-body" onclick="openModal('{b64_map['24_五常總控台_步驟1至步驟4操作區.png']}', '【截圖 24】總控台步驟 2 面板：先確認日期，點擊下載主日附件；確認自動生成標題，點擊複製與開啟後台')">
                <img src="{b64_map['24_五常總控台_步驟1至步驟4操作區.png']}" alt="步驟 2 面板">
            </div>
            <div class="image-card-desc">
                確認日期無誤 ➔ 點擊紅框<strong>【下載主日附件】</strong> ➔ 自動生成標題 ➔ 點擊紅框<strong>【複製】</strong> ➔ 點擊紅框<strong>【開啟後台】</strong>。
            </div>
        </div>
    </section>

    <!-- 步驟四：自動開啟 YouTube 直播後台 ➔ 編輯貼上當日主日標題 ➔ 儲存 -->
    <section id="step-4" class="section-card">
        <div class="section-header">
            <div class="section-title-wrap">
                <span class="step-num">4</span>
                <h2 class="section-title">自動開啟 YouTube 直播後台 ➔ 編輯貼上當日主日標題 ➔ 儲存</h2>
            </div>
            <span class="section-tag">後台標題設定</span>
        </div>

        <div class="step-block">
            <div class="grid-2">
                <div class="image-card">
                    <div class="image-card-header">
                        <span>【截圖 26】YouTube 直播管理頁</span>
                        <span class="img-tag" style="background:#FEE2E2; color:#B91C1C;">紅框點擊編輯</span>
                    </div>
                    <div class="image-card-body" onclick="openModal('{b64_map['26_YouTube頻道直播管理後台.png']}', '【截圖 26】自動開啟 YouTube 直播管理後台：點擊紅框「✏️ 編輯」圖示')">
                        <img src="{b64_map['26_YouTube頻道直播管理後台.png']}" alt="YouTube 直播管理頁">
                    </div>
                    <div class="image-card-desc">
                        自動開啟 YouTube 直播管理後台，點擊當日主日活動的<strong>「✏️ 編輯」</strong>圖示（紅框處）。
                    </div>
                </div>
                <div class="image-card">
                    <div class="image-card-header">
                        <span>【截圖 27】貼上標題並儲存</span>
                        <span class="img-tag" style="background:#FEE2E2; color:#B91C1C;">紅框貼上與儲存</span>
                    </div>
                    <div class="image-card-body" onclick="openModal('{b64_map['27_YouTube影片詳細資料_直播標題設定.png']}', '【截圖 27】紅框標題欄貼上標題，確認後點擊右上角紅框「儲存」')">
                        <img src="{b64_map['27_YouTube影片詳細資料_直播標題設定.png']}" alt="YouTube 標題設定">
                    </div>
                    <div class="image-card-desc">
                        在<strong>「標題」</strong>欄位（紅框處）貼上複製的當日主日標題，無誤後點擊右上角<strong>「儲存」</strong>按鈕（紅框處）。
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- 步驟五：PPT 大投影放映 ➔ 啟動雲端歌詞與懸浮導航 ➔ 工作視窗排版 -->
    <section id="step-5" class="section-card">
        <div class="section-header">
            <div class="section-title-wrap">
                <span class="step-num">5</span>
                <h2 class="section-title">PPT 大投影放映 ➔ 啟動雲端歌詞與懸浮導航 ➔ 工作視窗排版</h2>
            </div>
            <span class="section-tag">大投影與歌詞導航</span>
        </div>

        <ol style="font-size: 15px; line-height: 1.8; margin-bottom: 18px; padding-left: 20px;">
            <li><strong>點擊【步驟 3】「開啟 PPT (大投影放映)」</strong>：會堂大投影機滿版放映，主螢幕進入演講者檢視。</li>
            <li><strong>點擊【步驟 4】「開啟雲端歌詞」與「懸浮導航」，接著按「視窗排版」</strong>。</li>
            <li><strong>懸浮導航操作說明（重要備註）</strong>：
                <ul style="margin-top: 6px; padding-left: 18px;">
                    <li>每唱完一首詩歌，用滑鼠點擊<strong>首 1、2、3</strong>，PPT 會自動跳到那首（紅框標註）。</li>
                    <li>接著依照敬拜主領操作的跳段，依照<strong>數字鍵再按 ENTER</strong> 後 PPT 跳頁（紅框標註）。</li>
                </ul>
            </li>
        </ol>

        <div class="grid-2">
            <div class="image-card">
                <div class="image-card-header">
                    <span>【截圖 23】詩歌 PPT 懸浮導航視窗</span>
                    <span class="img-tag" style="background:#FEE2E2; color:#B91C1C;">紅框操作</span>
                </div>
                <div class="image-card-body" onclick="openModal('{b64_map['23_詩歌PPT懸浮導航視窗.png']}', '【截圖 23】懸浮導航：紅框點擊首 1、2、3 切歌；紅框中央依照提示輸入數字鍵+Enter跳頁')">
                    <img src="{b64_map['23_詩歌PPT懸浮導航視窗.png']}" alt="懸浮導航視窗">
                </div>
                <div class="image-card-desc">
                    點擊紅框<strong>【首 1、2、3】</strong>切換詩歌；照紅框提示按<strong>【數字鍵 ➔ Enter】</strong>跳頁。
                </div>
            </div>
            <div class="image-card">
                <div class="image-card-header">
                    <span>【截圖 22】雲端同步歌詞頁面</span>
                    <span class="img-tag">雲端歌詞</span>
                </div>
                <div class="image-card-body" onclick="openModal('{b64_map['22_雲端同步歌詞_瀏覽器顯示頁.png']}', '【截圖 22】自動開啟之雲端同步歌詞頁面')">
                    <img src="{b64_map['22_雲端同步歌詞_瀏覽器顯示頁.png']}" alt="雲端同步歌詞頁面">
                </div>
                <div class="image-card-desc">
                    即時顯示目前歌詞段落，便於同工對照敬拜主領進度。
                </div>
            </div>
        </div>
    </section>

    <!-- 步驟六：開場檢核確認 ➔ 一鍵生成「排版四分割工作台」 -->
    <section id="step-6" class="section-card">
        <div class="section-header">
            <div class="section-title-wrap">
                <span class="step-num">6</span>
                <h2 class="section-title">開場檢核確認 ➔ 一鍵生成「排版四分割工作台」</h2>
            </div>
            <span class="section-tag">四分割工作台</span>
        </div>

        <p style="font-size: 15px; margin-bottom: 12px; font-weight: 600; color: var(--secondary-dark);">
            按下「視窗排版」後跳出檢核對話框，確認無誤後點擊右下角紅框<strong>【確認全部就緒，開始排版 (Enter)】</strong>（或按 Enter 鍵）：
        </p>

        <ul style="font-size: 14.5px; line-height: 1.8; margin-bottom: 16px; padding-left: 20px;">
            <li><strong>左上</strong>：雲端同步歌詞頁面</li>
            <li><strong>左下</strong>：相機畫面 ＋ 詩歌懸浮導航（依翻頁提示輸入數字換頁）</li>
            <li><strong>右半</strong>：PowerPoint 演講者檢視</li>
        </ul>

        <div class="grid-2">
            <div class="image-card">
                <div class="image-card-header">
                    <span>【截圖 25】主日開場檢核清單</span>
                    <span class="img-tag" style="background:#FEE2E2; color:#B91C1C;">紅框點擊開始排版</span>
                </div>
                <div class="image-card-body" onclick="openModal('{b64_map['25_主日開場檢核清單對話框.png']}', '【截圖 25】開場檢核清單：點擊右下角紅框【確認全部就緒，開始排版 (Enter)】')">
                    <img src="{b64_map['25_主日開場檢核清單對話框.png']}" alt="開場檢核清單">
                </div>
                <div class="image-card-desc">
                    彈窗確認後，點擊右下角紅框<strong>【確認全部就緒，開始排版 (Enter)】</strong>按鈕。<br>
                    <strong style="color: #DC2626; font-size: 13.5px;">👉 請確定 YouTube 已發送直播！</strong>
                </div>
            </div>
            <div class="image-card">
                <div class="image-card-header">
                    <span>【截圖 28】多視窗四分割工作台</span>
                    <span class="img-tag">終端核心畫面</span>
                </div>
                <div class="image-card-body" onclick="openModal('{b64_map['28_主日直播多視窗黃金四分割工作配置.png']}', '【截圖 28】四分割工作配置：左下相機導航、右半演講者檢視')">
                    <img src="{b64_map['28_主日直播多視窗黃金四分割工作配置.png']}" alt="四分割工作台">
                </div>
                <div class="image-card-desc">
                    • <strong>左上</strong>：雲端同步歌詞頁面<br>
                    • <strong>左下</strong>：相機畫面 ＋ 詩歌懸浮導航（依翻頁提示輸入數字換頁）<br>
                    • <strong>右半</strong>：PowerPoint 演講者檢視
                </div>
            </div>
        </div>
    </section>

    <!-- 步驟七：OBS Studio 綁定排程並開始串流 -->
    <section id="step-7" class="section-card">
        <div class="section-header">
            <div class="section-title-wrap">
                <span class="step-num">7</span>
                <h2 class="section-title">OBS Studio 綁定排程並開始串流</h2>
            </div>
            <span class="section-tag">串流推流與錄製</span>
        </div>

        <p style="font-size: 15px; margin-bottom: 14px; font-weight: 600; color: var(--secondary-dark);">
            進行 OBS 串流綁定與啟動推流，正式進入主日直播：
        </p>

        <div class="image-card" style="margin-bottom: 20px;">
            <div class="image-card-header">
                <span>【截圖 13】OBS 33.0 正面主鏡畫面</span>
                <span class="img-tag">OBS 監控</span>
            </div>
            <div class="image-card-body" onclick="openModal('{b64_map['13_OBS介面_主日敬拜正面主鏡.png']}', '【截圖 13】OBS 主畫面：正面主鏡預覽、左下五常台標與跑馬燈、60.00 FPS')">
                <img src="{b64_map['13_OBS介面_主日敬拜正面主鏡.png']}" alt="OBS 正面主鏡預覽">
            </div>
            <div class="image-card-desc">
                OBS 畫面左下角帶有五常台標與跑馬燈，確認幀率維持 60.00 FPS。
            </div>
        </div>

        <div class="grid-2">
            <div class="image-card">
                <div class="image-card-header">
                    <span>【截圖 19】選擇現有 YouTube 排程直播</span>
                    <span class="img-tag">排程綁定</span>
                </div>
                <div class="image-card-body" onclick="openModal('{b64_map['19_OBS_YouTube直播設定與排程選擇.png']}', '【截圖 19】點管理直播，選擇現有直播分頁中勾選當週活動')">
                    <img src="{b64_map['19_OBS_YouTube直播設定與排程選擇.png']}" alt="選擇現有直播">
                </div>
                <div class="image-card-desc">
                    點 OBS「管理直播」➔「選擇現有直播」勾選當週主日活動並套用。
                </div>
            </div>
            <div class="image-card">
                <div class="image-card-header">
                    <span>【截圖 17】點擊開始串流</span>
                    <span class="img-tag">推流直播</span>
                </div>
                <div class="image-card-body" onclick="openModal('{b64_map['17_OBS_點擊開始串流按鈕.png']}', '【截圖 17】點擊紅框【開始串流】按鈕正式推流')">
                    <img src="{b64_map['17_OBS_點擊開始串流按鈕.png']}" alt="點擊開始串流按鈕" style="max-height: 120px; object-fit: contain;">
                </div>
                <div class="image-card-desc">
                    點擊紅框<strong>「開始串流」</strong>按鈕，正式進入主日直播推流。
                </div>
            </div>
        </div>
    </section>

    <!-- 步驟八：主日崇拜實戰切換 SOP -->
    <section id="step-8" class="section-card">
        <div class="section-header">
            <div class="section-title-wrap">
                <span class="step-num">8</span>
                <h2 class="section-title">主日崇拜實戰——看投影翻頁、歌詞同步與鏡頭切換</h2>
            </div>
            <span class="section-tag">崇拜進行實戰</span>
        </div>

        <!-- 全自動化說明 -->
        <div style="background: #F0FDF4; border: 1.5px solid #86EFAC; border-radius: 10px; padding: 16px 20px; margin-bottom: 16px;">
            <div style="display: flex; align-items: center; gap: 8px; font-weight: 700; color: #166534; font-size: 15.5px; margin-bottom: 8px;">
                <span>✨</span>
                <span>OBS 已經設置全自動化運行（皆不需要手動 OBS）：</span>
            </div>
            <ol style="margin: 0; padding-left: 22px; color: #15803D; font-size: 14.5px; line-height: 1.8;">
                <li>OBS 已經設置自動化，開啟時為靜音模式，<strong>主日早上 10 點自動開啟聲音</strong>。</li>
                <li>直播過程中，當 PPT 有換頁，OBS 場景<strong>自動跳到【主日 PPT 滿版】，停留 28 秒後自動跳回主鏡頭，當切換下一頁自動歸 0 計數</strong>。</li>
                <li>正面主鏡於停留 90 秒後，會<strong>自動跳到側面副鏡 iPhone X 停留 18 秒</strong>，之後再<strong>自動跳回正面主鏡</strong>。</li>
            </ol>
            <p style="margin: 8px 0 0 0; font-size: 14px; font-weight: 700; color: #166534;">
                👉 以上為全自動化，皆不需要手動操作 OBS。
            </p>
        </div>

        <!-- 甚麼時候需要切換 OBS -->
        <div style="background: #FFFBEB; border: 1.5px solid #FDE68A; border-radius: 10px; padding: 16px 20px; margin-bottom: 20px;">
            <div style="display: flex; align-items: center; gap: 8px; font-weight: 700; color: #B45309; font-size: 15.5px; margin-bottom: 8px;">
                <span>🎯</span>
                <span>甚麼時候需要切換 OBS：</span>
            </div>
            <ul style="margin: 0; padding-left: 20px; color: #92400E; font-size: 14.5px; line-height: 1.8;">
                <li><strong>當敬拜剛上台還沒唱詩歌及主領禱告時</strong>（通常在詩歌換首時） ➔ <strong>按 <kbd>F1</kbd></strong>（視情況動作）</li>
                <li><strong>牧師離開講台太遠脫離主鏡頭</strong> ➔ <strong>按 <kbd>F1</kbd> 或 <kbd>F2</kbd></strong>（視情況動作）</li>
                <li><strong>牧師介紹來賓鏡頭切到會眾</strong> ➔ <strong>按 <kbd>F3</kbd></strong>（視情況動作）</li>
            </ul>
        </div>

        <table class="sop-table">
            <thead>
                <tr>
                    <th style="width: 12%;">快捷鍵</th>
                    <th style="width: 25%;">切換目標畫面</th>
                    <th style="width: 43%;">適用時機</th>
                    <th style="width: 20%;">主要畫面來源</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><kbd>F1</kbd></td>
                    <td><strong>正面主鏡（牧師講道）</strong></td>
                    <td>
                        1. 當敬拜剛上台還沒唱詩歌及主領禱告時（通常在詩歌換首時）按 F1（視情況動作）<br>
                        2. 牧師離開講台太遠脫離主鏡頭（按 F1 或 F2，視情況動作）
                    </td>
                    <td>Galaxy A27 (1080p 60fps)</td>
                </tr>
                <tr>
                    <td><kbd>F2</kbd></td>
                    <td><strong>側面副鏡（講台特寫）</strong></td>
                    <td>牧師離開講台太遠脫離主鏡頭（按 F1 或 F2，視情況動作）</td>
                    <td>iPhone X 特寫機位</td>
                </tr>
                <tr>
                    <td><kbd>F3</kbd></td>
                    <td><strong>會眾全景（會堂大景）</strong></td>
                    <td>牧師介紹來賓鏡頭切到會眾（按 F3，視情況動作）</td>
                    <td>ASUS 後方高處俯拍機位</td>
                </tr>
                <tr>
                    <td><kbd>F4</kbd></td>
                    <td><strong>主日 PPT 滿版</strong></td>
                    <td>視情況動作（註：換頁時系統已自動切換滿版，同工亦可手動切換）</td>
                    <td>會堂投影 PPT 數位擷取</td>
                </tr>
            </tbody>
        </table>

        <div class="image-card" style="margin-top: 18px; max-width: 600px; margin-left: auto; margin-right: auto;">
            <div class="image-card-header">
                <span>【截圖 14】OBS 快捷鍵鏡頭場景列表</span>
                <span class="img-tag">快捷鍵對照</span>
            </div>
            <div class="image-card-body" onclick="openModal('{b64_map['14_OBS場景清單_下半段_F1至F4快捷鍵.png']}', '【截圖 14】快捷鍵鏡頭列表：F1主鏡、F2副鏡、F3全景、F4 PPT滿版')">
                <img src="{b64_map['14_OBS場景清單_下半段_F1至F4快捷鍵.png']}" alt="快捷鍵場景列表">
            </div>
            <div class="image-card-desc">
                場景列表清晰標註 F1 正面主鏡、F2 側面副鏡、F3 會眾全景、F4 主日 PPT 滿版。
            </div>
        </div>
    </section>

    <!-- 步驟九：主日散會與安全休眠關機流程 -->
    <section id="step-9" class="section-card">
        <div class="section-header">
            <div class="section-title-wrap">
                <span class="step-num">9</span>
                <h2 class="section-title">主日散會與安全休眠關機流程</h2>
            </div>
            <span class="section-tag">散會復原關機</span>
        </div>

        <ol style="font-size: 14.5px; line-height: 1.8; margin-left: 20px; margin-bottom: 20px;">
            <li><strong>停止直播與錄製</strong>：OBS 控制面板點擊<strong>【停止串流】</strong>與<strong>【停止YOUTUBE直播】</strong>。</li>
            <li><strong>相機休眠</strong>：重新以電腦「🔍 操控」安卓手機，<strong>滑鼠向上滑動關閉 Iriun Webcam App</strong>；iPhone <strong>輕觸畫面向上滑關閉</strong>。</li>
            <li><strong>線源插回充電孔</strong>：至天花板面板，將 A27 與 ASUS 的線<strong>由無記號訊號孔拔下，插回紅色充電孔</strong>，供週間補充電力。</li>
            <li><strong>關閉電源</strong>：關閉投影機與電腦主機電源，主日服事圓滿完成！</li>
        </ol>

        <div class="image-card" style="max-width: 480px; margin: 0 auto;">
            <div class="image-card-header">
                <span>【截圖 29】手機多工滑動關閉 Iriun Webcam App</span>
                <span class="img-tag">相機休眠關閉</span>
            </div>
            <div class="image-card-body" onclick="openModal('{b64_map['29_手機多工向上滑動關閉Iriun.png']}', '【截圖 29】多工畫面中滑鼠向上滑動關閉 Iriun Webcam App；iPhone 輕觸畫面向上滑關閉')">
                <img src="{b64_map['29_手機多工向上滑動關閉Iriun.png']}" alt="向上滑動關閉Iriun" style="max-height: 420px; object-fit: contain;">
            </div>
            <div class="image-card-desc">
                在安卓手機操控視窗中，點多工鍵後<strong>滑鼠向上滑動關閉 Iriun Webcam App</strong>；桌邊 iPhone 輕觸螢幕向上滑動關閉。
            </div>
        </div>
    </section>

    <!-- 常見狀況快速排錯指南 (Troubleshooting FAQ) -->
    <section id="step-faq" class="section-card">
        <div class="section-header">
            <div class="section-title-wrap">
                <span class="step-num">!</span>
                <h2 class="section-title">常見狀況快速排錯指南 (Troubleshooting FAQ)</h2>
            </div>
            <span class="section-tag">故障排除</span>
        </div>

        <div style="background: #F8FAFC; border: 1.5px solid #E2E8F0; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
            <h4 style="color: #DC2626; font-size: 16px; margin-bottom: 10px; display: flex; align-items: center; gap: 8px;">
                <span>⚠️</span>
                <span>Q1: 為什麼直播正面主鏡 A27 會卡頓/掉幀？</span>
            </h4>
            <div style="display: flex; gap: 20px; align-items: flex-start; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 280px; font-size: 14.5px; line-height: 1.85; color: var(--text-main);">
                    <strong>A:</strong> 操控手機的畫面於執行後可關閉（關閉多餘影像傳輸）；<br>
                    若畫面依然出現卡頓，請在<strong>【截圖 10】Camera #1</strong> 點那<strong>「三橫線」</strong>（如下圖），先選擇其他像素再調回 <strong>1920×1080</strong>（重新整理傳輸流）。
                </div>
                <div class="image-card" style="width: 140px; margin: 0; flex-shrink: 0;">
                    <div class="image-card-header" style="padding: 6px 10px; font-size: 12px;">
                        <span>三橫線選單</span>
                        <span class="img-tag" style="background: #FEE2E2; color: #DC2626;">圖 1</span>
                    </div>
                    <div class="image-card-body" style="padding: 6px;" onclick="openModal('{b64_map['30_Iriun_三橫線解析度調整選單.png']}', '【Iriun 選單】點擊左上角三橫線選單先選其他像素再調回 1920×1080')">
                        <img src="{b64_map['30_Iriun_三橫線解析度調整選單.png']}" alt="三橫線選單" style="max-height: 90px; object-fit: contain;">
                    </div>
                    <div class="image-card-desc" style="padding: 6px 8px; font-size: 11.5px;">
                        點擊紅框三橫線切換像素
                    </div>
                </div>
            </div>
        </div>

        <div style="background: #F8FAFC; border: 1.5px solid #E2E8F0; border-radius: 12px; padding: 20px;">
            <h4 style="color: #0284C7; font-size: 16px; margin-bottom: 10px; display: flex; align-items: center; gap: 8px;">
                <span>🖥️</span>
                <span>Q2: 視窗排版跑位了？</span>
            </h4>
            <p style="font-size: 14.5px; line-height: 1.85; color: var(--text-main); margin: 0;">
                <strong>A:</strong> 隨時在中控台重按<strong>【步驟 4：視窗排版】</strong>，即可自動還原黃金四分割工作台！
            </p>
        </div>
    </section>

</div>

<!-- 圖片放大燈箱 Lightbox Modal -->
<div id="imageModal" class="modal" onclick="closeModal()">
    <span class="modal-close" onclick="closeModal()">&times;</span>
    <div class="modal-img-wrap" onclick="event.stopPropagation()">
        <img id="modalImg" src="" alt="放大預覽">
    </div>
    <div id="modalCaption" class="modal-caption" onclick="event.stopPropagation()"></div>
</div>

<script>
    function openModal(src, caption) {{
        const modal = document.getElementById('imageModal');
        const img = document.getElementById('modalImg');
        const cap = document.getElementById('modalCaption');
        img.src = src;
        cap.innerText = caption;
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }}

    function closeModal() {{
        const modal = document.getElementById('imageModal');
        modal.classList.remove('active');
        document.body.style.overflow = 'auto';
    }}

    document.addEventListener('keydown', function(e) {{
        if (e.key === 'Escape') {{
            closeModal();
        }}
    }});
</script>

</body>
</html>
"""

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"成功生成極簡 SOP 手冊: {OUTPUT_HTML} (大小: {os.path.getsize(OUTPUT_HTML) // 1024} KB)")

    if os.path.exists(os.path.dirname(OUTPUT_HTML_SYS)):
        with open(OUTPUT_HTML_SYS, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"成功備份至中控系統資料夾: {OUTPUT_HTML_SYS}")

if __name__ == "__main__":
    main()
