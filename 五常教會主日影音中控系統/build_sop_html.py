# -*- coding: utf-8 -*-
import os
import base64

def b64(path):
    if not os.path.exists(path):
        return ''
    with open(path, 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode('utf-8')

img1_gui = b64(r'C:\Users\admin\.gemini\antigravity\brain\735c6a92-27b2-4e75-85bf-b53c5e5c4885\.user_uploaded\media_1793163183149_a630c140.png')
img2_yt = b64(r'C:\Users\admin\.gemini\antigravity\brain\735c6a92-27b2-4e75-85bf-b53c5e5c4885\.user_uploaded\media_1793163243940_e6cf13e4.png')
img3_lyrics = b64(r'C:\Users\admin\.gemini\antigravity\brain\735c6a92-27b2-4e75-85bf-b53c5e5c4885\.user_uploaded\media_1793163259494_d6b0010d.png')
img4_nav = b64(r'C:\Users\admin\.gemini\antigravity\brain\735c6a92-27b2-4e75-85bf-b53c5e5c4885\.user_uploaded\media_1793163282189_1d62e9f6.png')
img5_check = b64(r'C:\Users\admin\.gemini\antigravity\brain\735c6a92-27b2-4e75-85bf-b53c5e5c4885\.user_uploaded\media_1793163307846_773ad5cc.png')
img6_live = b64(r'C:\Users\admin\.gemini\antigravity\brain\735c6a92-27b2-4e75-85bf-b53c5e5c4885\.user_uploaded\media_1793185268656_865f31fd.png')

logo_path = r'E:\Antigravity_Data\五常教會直播設置\五常教會主日影音中控系統\assets\church_logo.png'
logo_b64 = b64(logo_path)

html_content = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>五常基督長老教會 • 主日影音直播新手不求人 SOP 指南</title>
    <style>
        :root {{
            --primary: #0D9488;
            --primary-dark: #0F766E;
            --primary-light: #F0FDFA;
            --secondary: #1E3A8A;
            --accent: #2563EB;
            --danger: #E11D48;
            --warning: #D97706;
            --success: #059669;
            --text-main: #0F172A;
            --text-muted: #64748B;
            --bg-page: #F8FAFC;
            --bg-card: #FFFFFF;
            --border-color: #E2E8F0;
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
            padding: 24px;
        }}

        .container {{
            max-width: 1040px;
            margin: 0 auto;
            background: var(--bg-card);
            border-radius: 18px;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.07);
            border: 1px solid var(--border-color);
            overflow: hidden;
        }}

        /* 頁首 Header */
        .sop-header {{
            background: linear-gradient(135deg, #0F766E 0%, #0D9488 50%, #1E3A8A 100%);
            color: white;
            padding: 36px 40px;
            position: relative;
        }}

        .sop-header-content {{
            display: flex;
            align-items: center;
            gap: 20px;
        }}

        .sop-header img.logo {{
            width: 76px;
            height: 76px;
            background: white;
            padding: 5px;
            border-radius: 18px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.2);
            flex-shrink: 0;
        }}

        .sop-header h1 {{
            font-size: 26px;
            font-weight: 800;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }}

        .sop-header p.sub {{
            font-size: 15px;
            color: #CCFBF1;
            font-weight: 500;
        }}

        .sop-badges {{
            margin-top: 16px;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}

        .badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 12.5px;
            font-weight: 700;
            background: rgba(255, 255, 255, 0.22);
            backdrop-filter: blur(4px);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.35);
        }}

        /* 核心宣言 Callout */
        .intro-box {{
            margin: 28px 40px 10px 40px;
            background: #F0FDF4;
            border-left: 5px solid #16A34A;
            padding: 20px 24px;
            border-radius: 0 12px 12px 0;
        }}

        .intro-box h2 {{
            font-size: 18px;
            color: #166534;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .intro-box p {{
            font-size: 14.5px;
            color: #14532D;
            line-height: 1.65;
        }}

        /* 內容章節 */
        .section {{
            padding: 30px 40px;
            border-bottom: 1px solid var(--border-color);
        }}

        .section:last-child {{
            border-bottom: none;
        }}

        .section-title {{
            font-size: 21px;
            font-weight: 800;
            color: var(--secondary);
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .section-title .step-num {{
            background: var(--primary);
            color: white;
            width: 34px;
            height: 34px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 800;
            flex-shrink: 0;
            box-shadow: 0 2px 6px rgba(13, 148, 136, 0.3);
        }}

        /* 口語化速查步驟大卡片 */
        .step-list {{
            display: flex;
            flex-direction: column;
            gap: 14px;
            margin: 20px 0;
        }}

        .step-card {{
            background: white;
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 16px 20px;
            display: flex;
            align-items: flex-start;
            gap: 16px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.03);
            transition: all 0.2s;
        }}

        .step-card:hover {{
            border-color: var(--primary);
            box-shadow: 0 4px 12px rgba(13, 148, 136, 0.1);
        }}

        .step-card .num-badge {{
            background: #E0F2FE;
            color: #0369A1;
            font-size: 16px;
            font-weight: 800;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            margin-top: 2px;
        }}

        .step-card-content h4 {{
            font-size: 16px;
            color: var(--text-main);
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .step-card-content p {{
            font-size: 14px;
            color: #475569;
            line-height: 1.6;
        }}

        .step-card-content .action-tag {{
            display: inline-block;
            background: #FEF3C7;
            color: #92400E;
            font-size: 12px;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 6px;
            margin-top: 6px;
        }}

        /* 講道模式專屬特寫卡片 */
        .sermon-hero-card {{
            background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 50%, #0D9488 100%);
            color: white;
            border-radius: 16px;
            padding: 24px 28px;
            margin: 22px 0;
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.2);
        }}

        .sermon-hero-card h3 {{
            font-size: 19px;
            font-weight: 800;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .sermon-hero-card p {{
            font-size: 14.5px;
            color: #E0F2FE;
            line-height: 1.65;
            margin-bottom: 14px;
        }}

        .sermon-feature-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 14px;
            margin-top: 14px;
        }}

        .sermon-feature-item {{
            background: rgba(255, 255, 255, 0.12);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.25);
            border-radius: 12px;
            padding: 14px 16px;
        }}

        .sermon-feature-item h5 {{
            font-size: 15px;
            font-weight: 700;
            color: #FACC15;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .sermon-feature-item p {{
            font-size: 13.5px;
            color: white;
            line-height: 1.55;
            margin: 0;
        }}

        /* 比較表格 (前後省略動作) */
        .diff-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 13.5px;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid var(--border-color);
        }}

        .diff-table th {{
            background: #F1F5F9;
            color: #334155;
            padding: 14px 16px;
            text-align: left;
            font-weight: 800;
            border-bottom: 2px solid var(--border-color);
        }}

        .diff-table td {{
            padding: 14px 16px;
            border-bottom: 1px solid #F1F5F9;
            vertical-align: top;
            line-height: 1.6;
        }}

        .diff-table tr:hover td {{
            background: #F8FAFC;
        }}

        .tag-manual {{
            display: inline-block;
            background: #FEE2E2;
            color: #991B1B;
            padding: 2px 8px;
            border-radius: 6px;
            font-size: 11.5px;
            font-weight: 700;
            margin-bottom: 4px;
        }}

        .tag-sop {{
            display: inline-block;
            background: #DCFCE7;
            color: #166534;
            padding: 2px 8px;
            border-radius: 6px;
            font-size: 11.5px;
            font-weight: 700;
            margin-bottom: 4px;
        }}

        .diff-saved {{
            font-weight: 800;
            color: var(--primary-dark);
        }}

        /* 統計卡片 */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin: 20px 0;
        }}

        .stat-card {{
            background: var(--bg-page);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
        }}

        .stat-card .val {{
            font-size: 26px;
            font-weight: 900;
            color: var(--primary);
            margin: 4px 0;
        }}

        .stat-card .lbl {{
            font-size: 12.5px;
            color: var(--text-muted);
            font-weight: 600;
        }}

        /* 圖文說明卡片 */
        .guide-card {{
            background: white;
            border: 1px solid var(--border-color);
            border-radius: 14px;
            overflow: hidden;
            margin: 22px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }}

        .guide-card .img-box {{
            background: #0F172A;
            text-align: center;
            padding: 14px;
            border-bottom: 1px solid var(--border-color);
        }}

        .guide-card .img-box img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.3);
            display: inline-block;
        }}

        .guide-card .desc {{
            padding: 20px 24px;
            background: #FFFFFF;
        }}

        .guide-card .desc h4 {{
            font-size: 16.5px;
            color: var(--secondary);
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .guide-card .desc p, .guide-card .desc ul {{
            font-size: 14.5px;
            color: #334155;
            line-height: 1.65;
        }}

        .guide-card .desc ul {{
            padding-left: 22px;
            margin-top: 8px;
        }}

        .guide-card .desc li {{
            margin-bottom: 6px;
        }}

        /* 警示與注意 Box */
        .alert-box {{
            background: #FFFBEB;
            border-left: 5px solid #F59E0B;
            padding: 16px 20px;
            border-radius: 0 10px 10px 0;
            margin: 16px 0;
            font-size: 14px;
            color: #92400E;
            line-height: 1.6;
        }}

        .alert-box strong {{
            color: #78350F;
        }}

        .checklist-box {{
            background: #F8FAFC;
            border: 1px solid #CBD5E1;
            border-radius: 12px;
            padding: 18px 22px;
            margin: 16px 0;
        }}

        .checklist-item {{
            display: flex;
            align-items: flex-start;
            gap: 12px;
            margin-bottom: 14px;
            font-size: 14px;
        }}

        .checklist-item:last-child {{
            margin-bottom: 0;
        }}

        .checklist-icon {{
            background: var(--primary);
            color: white;
            border-radius: 50%;
            width: 24px;
            height: 24px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 13px;
            font-weight: 800;
            flex-shrink: 0;
            margin-top: 2px;
        }}

        /* 頁尾 */
        .sop-footer {{
            background: #F1F5F9;
            padding: 24px 40px;
            text-align: center;
            color: var(--text-muted);
            font-size: 13px;
            border-top: 1px solid var(--border-color);
        }}

        @media print {{
            body {{
                padding: 0;
                background: white;
            }}
            .container {{
                box-shadow: none;
                border: none;
                max-width: 100%;
            }}
            .section {{
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>

<div class="container">

    <!-- 頂部形象 Header -->
    <div class="sop-header">
        <div class="sop-header-content">
            <img class="logo" src="{logo_b64}" alt="五常長老教會 Logo">
            <div>
                <h1>台灣基督長老教會 五常教會</h1>
                <p class="sub">主日影音與直播總控標準作業程序 (SOP) • 口語化同工操作全指南</p>
                <div class="sop-badges">
                    <span class="badge">🛡️ 新手上路不怕出包</span>
                    <span class="badge">🚀 免手動打字/免拉視窗 (省80+動作)</span>
                    <span class="badge">📐 四象限排版一秒歸位</span>
                    <span class="badge">🎵 敬拜詩歌數字鍵直達</span>
                    <span class="badge">🎙️ 講道經文自動滿版 + 80s 輪運鏡</span>
                </div>
            </div>
        </div>
    </div>

    <!-- 核心價值宣言 -->
    <div class="intro-box">
        <h2>👋 給親愛的影音同工：為什麼要有這套中控 SOP？</h2>
        <p>
            以前主日直播最容易讓人心驚膽跳的，就是<b>「換不同人輪值，操作習慣不一樣，直播品質就變來變去」</b>——
            有的同工忘記開麥克風取消靜音、有的視窗拉太大擋住投影片備忘稿、有的在詩歌跳唱時找不到投影片慌成一團，或是手機相機忘了熄屏發燙當機...<br><br>
            現在有了這套<b>「五常教會主日影音中控系統」</b>與已設定好的 OBS 自動化，我們把過去所有繁複的手動動作通通自動化！
            不管是經驗豐富的老手，還是第一次輪值的新人，只要照著順序操作，<b>大家的直播品質就能 100% 一模一樣，既輕鬆又專業！</b>
        </p>
    </div>

    <!-- 口語化速查核心步驟 -->
    <div class="section">
        <div class="section-title">
            <span class="step-num">★</span>
            <h3>主日服事一鍵上手：7 大核心操作步驟 (白話速查)</h3>
        </div>
        <p style="font-size: 14.5px; color: #475569; margin-bottom: 12px;">
            主日到了控制台，雙擊打開桌面的<b>「五常教會主日影音中控系統.exe」</b>，照著下面這 7 步點一點就搞定：
        </p>

        <div class="step-list">
            <div class="step-card">
                <div class="num-badge">1</div>
                <div class="step-card-content">
                    <h4>點【📥 下載主日附件】</h4>
                    <p><b>免手動登入開啟 Gmail！</b>系統會自己連到專屬信箱，智能下載本週最新 PPT，並自動下載與對照 <code>config.txt</code> 詩歌設定檔。</p>
                    <span class="action-tag">💡 省去：開瀏覽器 ➔ 登入 Gmail ➔ 找信件 ➔ 手動下載 ➔ 複製檔案</span>
                </div>
            </div>

            <div class="step-card">
                <div class="num-badge">2</div>
                <div class="step-card-content">
                    <h4>點【📋 複製】➔ 點【🌐 開啟後台】</h4>
                    <p>系統已經自動從下載檔案中抓出當週的<b>「講道題目」</b>與<b>「講員牧師」</b>並組好標準標題；點開啟後台後，直接在 YouTube 直播標題按 <code>Ctrl + V</code> 貼上即可！</p>
                    <span class="action-tag">💡 省去：手動打字 120 字 ➔ 來回切換視窗 ➔ 避免打錯講道題目或牧師名字</span>
                </div>
            </div>

            <div class="step-card">
                <div class="num-badge">3</div>
                <div class="step-card-content">
                    <h4>點選【🖥️ 全螢幕投影主日 PPT】</h4>
                    <p><b>免手動找檔案、免自己按 F5！</b>系統會直接打開本週 PPT，並自動強制把投影片全螢幕放映延伸到會堂大螢幕（Monitor 2），操作螢幕則自動進入簡報者檢視。</p>
                    <span class="action-tag">💡 省去：雙擊檔案 ➔ 找功能表 ➔ 檢查延伸螢幕 ➔ 避免不小心把投影片放映在操作螢幕</span>
                </div>
            </div>

            <div class="step-card">
                <div class="num-badge">4</div>
                <div class="step-card-content">
                    <h4>點選【🌐 開啟雲端歌詞】</h4>
                    <p><b>免手動選身分！</b>系統會打開雲端歌詞網頁，並自動跳過身分選擇頁，直接鎖定進入「副唱 / 鋼琴 / 螢幕 (顯示端)」模式，與台前敬拜團無縫連線。</p>
                    <span class="action-tag">💡 省去：開網頁 ➔ 點選手機顯示模式 ➔ 避免選錯身分進到控制端</span>
                </div>
            </div>

            <div class="step-card">
                <div class="num-badge">5</div>
                <div class="step-card-content">
                    <h4>點選【🚀 懸浮導航】</h4>
                    <p>桌面上會出現一個漂亮白框圓角的「歌詞數字鍵提示小視窗」，隨時置頂在最上層，大字提醒跳頁號碼。</p>
                    <span class="action-tag">💡 效果：置頂浮動小卡片，隨時告訴你敬拜團現在唱到哪裡</span>
                </div>
            </div>

            <div class="step-card">
                <div class="num-badge">6</div>
                <div class="step-card-content">
                    <h4>點選中控台【📐 一鍵自動排版】</h4>
                    <p><b>全自動四象限固定＋背景大掃除！</b>系統會先彈出開場 3 道檢核清單（<b>強烈提醒確認 OBS 取消靜音</b>、檢查鏡頭序號），按下確認後，<b>所有其他無關的雜七雜八視窗通通自動最小化</b>，使用的四個工作視窗像素級精準定位！</p>
                    <span class="action-tag">💡 省去：手動滑鼠拖曳 45 次視窗 ➔ 桌面雜訊一秒清空 ➔ 徹底消除 PPT 編輯視窗遮擋</span>
                </div>
            </div>

            <div class="step-card">
                <div class="num-badge">7</div>
                <div class="step-card-content">
                    <h4>點選【🚀 懸浮導航】裡面的三首詩歌快捷鈕</h4>
                    <p><b>點歌秒級直達＋焦點自動鎖定！</b>點選懸浮導航裡的「🎵 首 1、首 2、首 3」，PPT 會瞬間自動跳到該首詩歌起始頁；<b>最厲害的是：系統會自動把鍵盤焦點鎖定回 PPT</b>，你可以直接輸入數字跳頁或按空白鍵/方向鍵下一頁，<b>完全不用拿滑鼠再去點一下 PPT！</b></p>
                    <span class="action-tag">💡 超大福音：消除「切換歌曲後投影片失焦按不下去」的困擾，翻頁 100% 零延遲</span>
                </div>
            </div>
        </div>
    </div>

    <!-- 講道專用：智慧運鏡與經文自動滿版 (使用者重點功能) -->
    <div class="section">
        <div class="section-title">
            <span class="step-num">🎙️</span>
            <h3>敬拜後無縫接軌：講道「自動經文滿版 ＋ 80 秒智慧運鏡」</h3>
        </div>
        <p style="font-size: 14.5px; color: #475569; margin-bottom: 8px;">
            詩歌敬拜結束、牧師準備上台證道時，同工最怕什麼？<b>最怕「牧師念經文時，同工忘記把直播畫面切到投影片」</b>，導致線上會眾只能看到牧師遠遠的影子，卻看不到經文重點！
        </p>

        <!-- 專題解說卡片 -->
        <div class="sermon-hero-card">
            <h3>🎉 好消息：現在只要在敬拜後「切換講道一次」，後面通通不用管！</h3>
            <p>
                教會 OBS 已經設定好整套智慧連動邏輯！詩歌敬拜結束時，同工<b>只要在 OBS 切換到【講道】場景一次</b>，整場講道的運鏡與投影片展示就由系統完全自動接手：
            </p>

            <div class="sermon-feature-grid">
                <div class="sermon-feature-item">
                    <h5>📖 1. 簡報跳頁讀經文 ➔ OBS 自動切到 PPT 滿版！</h5>
                    <p>牧師講道時只要按簡報筆翻頁（讀聖經經文或講道大綱），系統偵測到投影片跳頁，<b>OBS 就會「全自動」瞬間切換到【PPT滿版】全螢幕畫面！</b>同工完全不需要緊張去按切換鍵，徹底杜絕忘記切經文的失誤！</p>
                </div>

                <div class="sermon-feature-item">
                    <h5>🎥 2. 講道畫面維持 80 秒 ➔ 智慧隨機輪播多視角！</h5>
                    <p>講員主畫面維持 80 秒後，OBS 會自動隨機切換視角，讓直播畫面活潑生動：<br>
                    • <b>80% 機率</b> ➔ 自動跳至<b>【側畫面】</b>(iPhone X 側面特寫)<br>
                    • <b>20% 機率</b> ➔ 自動跳至<b>【會眾畫面】</b>(ASUS 會眾全景)<br>
                    運鏡流暢有電影感，同工可以端坐專心聽講道！</p>
                </div>
            </div>
        </div>

        <div class="alert-box" style="background: #EFF6FF; border-left-color: #2563EB; color: #1E3A8A;">
            <strong>✨ 同工省心總整理：</strong><br>
            敬拜完 ➔ OBS 切一次「講道」 ➔ 雙手放開！牧師翻頁念經文會自動切投影片滿版，講道畫面每隔 80 秒會自動跳側鏡特寫或會眾全景，整場講道同工零負擔，再也不用手忙腳亂切鏡頭！
        </div>
    </div>

    <!-- 省略動作對比剖析 -->
    <div class="section">
        <div class="section-title">
            <span class="step-num">⚡</span>
            <h3>動作省多少？「以前手動 vs 現在中控」超真實對比</h3>
        </div>
        <p style="font-size: 14.5px; color: #475569; margin-bottom: 12px;">
            看數據就知道差別有多大！中控系統幫同工省下了幾十次緊張容易點錯的動作：
        </p>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="lbl">省去滑鼠拖放拉伸</div>
                <div class="val">45+ 次</div>
                <div class="lbl">一鍵四象限排好排滿</div>
            </div>
            <div class="stat-card">
                <div class="lbl">省去手動打字更名</div>
                <div class="val">120+ 字</div>
                <div class="lbl">講道標題全自動解析</div>
            </div>
            <div class="stat-card">
                <div class="lbl">講道經文手動切換</div>
                <div class="val">0 次</div>
                <div class="lbl">翻頁自動切 PPT 滿版</div>
            </div>
            <div class="stat-card">
                <div class="lbl">敬拜詩歌跳頁時間</div>
                <div class="val">0.3 秒</div>
                <div class="lbl">由 3~5 秒找頁變成直覺跳</div>
            </div>
        </div>

        <table class="diff-table">
            <thead>
                <tr>
                    <th style="width: 18%;">主日工作階段</th>
                    <th style="width: 38%;">以前舊做法 (手忙腳亂、容易出錯)</th>
                    <th style="width: 44%;">現在中控 SOP (優雅輕鬆、品質一致)</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><b>1. 主日資料與標題</b></td>
                    <td>
                        <span class="tag-manual">手動點 20 幾次</span><br>
                        開瀏覽器 ➔ 登入 Gmail ➔ 找信件 ➔ 點下載 ➔ 改檔名 ➔ 開 YouTube ➔ 貼標題 ➔ 常常字打錯或格式不合。
                    </td>
                    <td>
                        <span class="tag-sop">只要點 2 下</span> <span class="diff-saved">(省 18 次點擊 + 0 打字)</span><br>
                        點<b>【下載附件】</b>自動抓檔案兼解析，點<b>【複製】</b>點<b>【開啟後台】</b>直接貼上，零錯字！
                    </td>
                </tr>
                <tr>
                    <td><b>2. 手機相機開機防燙</b></td>
                    <td>
                        <span class="tag-manual">走來走去按開關</span><br>
                        走到講台跟後方腳架按電源鍵解鎖 ➔ 手動開相機 ➔ 常常忘了關閉螢幕，手機發燙當機掉格。
                    </td>
                    <td>
                        <span class="tag-sop">坐在椅子上點 1 下</span> <span class="diff-saved">(遠端全自動)</span><br>
                        點<b>【喚醒手機】</b>遠端隔空開機；點<b>【操控】</b>螢幕保持黑屏熄屏，持續直播好幾個小時都不發燙！
                    </td>
                </tr>
                <tr>
                    <td><b>3. PPT 雙螢幕放映</b></td>
                    <td>
                        <span class="tag-manual">手動點 8 次選單</span><br>
                        打開 PPT ➔ 設定延伸螢幕 ➔ 按 F5 ➔ 常常放映跑到操作螢幕，主畫面還留著好大一個編輯視窗擋路。
                    </td>
                    <td>
                        <span class="tag-sop">只要點 1 下</span> <span class="diff-saved">(系統強制送對螢幕)</span><br>
                        點<b>【全螢幕投影主日 PPT】</b>，會堂大螢幕自動全螢幕放映，操作螢幕直接變簡報者檢視。
                    </td>
                </tr>
                <tr>
                    <td><b>4. 桌面四象限排版</b></td>
                    <td>
                        <span class="tag-manual">滑鼠手動拖曳 45 次 (耗時5分鐘)</span><br>
                        桌上一堆視窗 ➔ 用滑鼠一個一個拉視窗大小 ➔ 擺不整齊、互相遮擋，不同人排版完全不一樣。
                    </td>
                    <td>
                        <span class="tag-sop">只要點 1 下</span> <span class="diff-saved">(0.5 秒瞬間定位)</span><br>
                        點<b>【一鍵自動排版】</b>，<b>其他無關視窗全部縮小</b>，四象限視窗像素級對齊，中控台自動收合，極致乾淨！
                    </td>
                </tr>
                <tr>
                    <td><b>5. 敬拜詩歌跳頁</b></td>
                    <td>
                        <span class="tag-manual">緊張滾輪找投影片 (滾30幾次)</span><br>
                        主領歌手突然重唱副歌或跳歌 ➔ 同工慌張在縮圖裡上下滾動找頁數 ➔ 容易切錯頁甚至黑畫面，延遲 3 秒才翻頁。
                    </td>
                    <td>
                        <span class="tag-sop">看數字按鍵盤</span> <span class="diff-saved">(直覺跳頁、零延遲)</span><br>
                        懸浮窗顯示「請輸入：7」，直接按數字鍵 7 就切過去！點歌曲鈕自動跳起始頁，<b>完全不用滑鼠點回 PPT！</b>
                    </td>
                </tr>
                <tr>
                    <td><b>6. 講道經文與運鏡</b></td>
                    <td>
                        <span class="tag-manual">全程精神緊繃手動切換</span><br>
                        同工要一直盯著牧師講到哪、有沒有念經文，常常忘記切投影片，鏡頭切換單調乏味。
                    </td>
                    <td>
                        <span class="tag-sop">敬拜後切一次講道即可</span> <span class="diff-saved">(經文自動滿版 + 80s 隨機輪播)</span><br>
                        只要敬拜結束切換到「講道」一次！牧師跳頁自動切 PPT 滿版，講道畫面維持 80 秒後 80% 跳側畫面、20% 跳會眾畫面，全自動運作！
                    </td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- 詳細圖文解說章節 -->
    <div class="section">
        <div class="section-title">
            <span class="step-num">📷</span>
            <h3>圖文詳解：中控介面與操作畫面實戰導覽</h3>
        </div>

        <!-- 實戰桌面全景圖 -->
        <div class="guide-card">
            <div class="img-box">
                <img src="{img6_live}" alt="主日四象限實戰桌面全景">
            </div>
            <div class="desc">
                <h4>🌟 主日現場標準四象限工作桌面 (點排版後的極致境界！)</h4>
                <p>如上圖實拍照所示，按下「一鍵自動排版」後，桌面呈現最完美標準狀態：</p>
                <ul>
                    <li><b>👉 右半側 (50% 寬)</b>：PowerPoint 簡報者檢視畫面，投影片進度、備忘稿與大時鐘一覽無遺。</li>
                    <li><b>👉 左上格 (25%)</b>：雲端歌詞副唱顯示端，清晰顯示主歌/副歌大字。</li>
                    <li><b>👉 左下格 (25%)</b>：Iriun Webcam 視訊視窗，即時監看講台主鏡畫面。</li>
                    <li><b>👉 左下格右上方</b>：現代純白圓角<b>「懸浮導航視窗」</b>置頂常駐，大字顯示跳頁指示！</li>
                </ul>
            </div>
        </div>

        <div class="guide-card">
            <div class="img-box">
                <img src="{img1_gui}" alt="主日影音中控系統介面全景">
            </div>
            <div class="desc">
                <h4>🖥️ 1. 中控系統主視窗 (一切功能的指揮中心)</h4>
                <p>視窗最上方是<b>「硬體連線狀態列」</b>，能即時看到 A27 主鏡、ASUS 全景與 PPT 的連線狀態；下方則是精心設計的步驟 1 到步驟 4，依序操作即可。</p>
            </div>
        </div>

        <div class="guide-card">
            <div class="img-box">
                <img src="{img2_yt}" alt="YouTube Studio 標題更新">
            </div>
            <div class="desc">
                <h4>🌐 2. YouTube 直播後台 (點複製後直接貼上)</h4>
                <p>中控台已經自動組合好包含日期、講道題目、講員的標準文字（例如 <code>10/25「人生說明書」施貞同牧師 「五常教會主日」</code>），貼上去就對了，完全免手打！</p>
            </div>
        </div>

        <div class="guide-card">
            <div class="img-box">
                <img src="{img3_lyrics}" alt="雲端歌詞副唱顯示端">
            </div>
            <div class="desc">
                <h4>🎵 3. 雲端歌詞顯示端 (副唱同步模式)</h4>
                <p>點選「開啟雲端歌詞」後，系統會自動跳過所有選單，直接進入大字歌詞顯示端，台前敬拜團按哪裡，這裡就同步到哪裡！</p>
            </div>
        </div>

        <div class="guide-card">
            <div class="img-box">
                <img src="{img4_nav}" alt="歌詞懸浮導航視窗">
            </div>
            <div class="desc">
                <h4>🚀 4. 置頂懸浮導航小視窗 (翻頁大救星)</h4>
                <ul>
                    <li><b>超大字跳頁提示</b>：隨時以大字顯示「請輸入：7」，看到幾號直接在鍵盤按幾號，投影片秒跳！</li>
                    <li><b>首1、首2、首3 直達鈕</b>：點選任意首歌曲，PPT 會自動跳到該首詩歌主歌頁面，而且<b>鍵盤焦點自動留在 PPT</b>，不用再拿滑鼠點投影片一下！</li>
                </ul>
            </div>
        </div>

        <div class="guide-card">
            <div class="img-box">
                <img src="{img5_check}" alt="開場檢核清單彈出視窗">
            </div>
            <div class="desc">
                <h4>📋 5. 開場 3 大核心防呆檢核清單 (按下排版時自動彈出)</h4>
                <p>按下排版時會強制彈出這個檢核框，就像飛機起飛前的 Checklist，目視確認這三項：</p>
                <div class="checklist-box">
                    <div class="checklist-item">
                        <span class="checklist-icon">1</span>
                        <div><b>OBS 與 YouTube 直播已開始</b>：確認 OBS 綠燈穩定連線、YouTube 呈現「正在直播」。</div>
                    </div>
                    <div class="checklist-item">
                        <span class="checklist-icon">2</span>
                        <div><b>Iriun 鏡頭通道對應確認</b>：1. A27 正面主鏡 ➔ 2. iPhone X 側面副鏡 ➔ 3. ASUS 會眾全景。</div>
                    </div>
                </div>
                <p style="margin-top: 10px;">
                    確認沒問題後，按 <b>Enter（確認全部就緒，開始排版）</b>，四象限排版瞬間就位！
                </p>
            </div>
        </div>
    </div>

    <!-- 主日常見狀況排除 FAQ -->
    <div class="section">
        <div class="section-title">
            <span class="step-num">Q&A</span>
            <h3>主日突發狀況快問快答 (FAQ)</h3>
        </div>
        <div style="font-size: 14.5px; color: #334155; line-height: 1.7;">
            <p><b>Q1：如果敬拜時滑鼠不小心把視窗移亂了，怎麼辦？</b><br>
            👉 <b>別慌！隨時按鍵盤上的 <code>F12</code></b>（或懸浮導航上的 <code>📐 歸位</code>），所有視窗在 0.5 秒內會再次整整齊齊自動歸位！</p>
            <br>
            <p><b>Q2：講道時同工到底要做什麼？</b><br>
            👉 <b>只要在敬拜結束後，在 OBS 切換到【講道】一次即可！</b>後續牧師念經文自動切 PPT 滿版，每隔 80 秒會自動跳側鏡或會眾鏡頭，同工可以端坐專心聽道，完全不用手動切換！</p>
            <br>
            <p><b>Q3：為什麼散會時只要按「休眠」，不要按「關機」？</b><br>
            👉 因為按<b>【休眠手機】</b>，手機相機關閉黑屏待機，下週主日可以直接「遠端喚醒」；如果按徹底關機，手機就會斷電，下週同工就要自己走到腳架旁手動按實體鍵開機囉！</p>
            <br>
            <p><b>Q4：如果某一首詩歌臨時要重唱副歌，怎麼切換最快？</b><br>
            👉 直接看懸浮導航視窗顯示的數字（例如 8），直接在鍵盤按數字 <code>8</code>，投影片就會秒切到副歌，比用滑鼠去縮圖裡找快上 10 倍！</p>
        </div>
    </div>

    <!-- 頁尾 -->
    <div class="sop-footer">
        <p>台灣基督長老教會 五常教會 • 主日影音直播服事團隊 謹製</p>
        <p style="margin-top: 4px;">系統版本：v3.0 現代精簡排版高畫質版 • 文件更新日期：2026 年 10 月</p>
    </div>

</div>

</body>
</html>
'''

# 儲存至 Artifacts, Project, 以及 Desktop
paths = [
    r'C:\Users\admin\.gemini\antigravity\brain\735c6a92-27b2-4e75-85bf-b53c5e5c4885\五常教會主日影音與直播總控SOP操作手冊.html',
    r'E:\Antigravity_Data\五常教會直播設置\五常教會主日影音中控系統\五常教會主日影音與直播總控SOP操作手冊.html',
    os.path.join(os.path.expanduser('~'), 'Desktop', '五常教會主日影音與直播總控SOP操作手冊.html')
]

for p in paths:
    with open(p, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f'[OK] 已產出最新講道連動 SOP 文件: {p} ({len(html_content)} bytes)')
