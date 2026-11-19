@echo off
chcp 65001 >nul
set "PATH=E:\Antigravity_Data\五常教會直播設置\scrcpy;C:\Program Files (x86)\Iriun Webcam;%PATH%"
title 正面主鏡遠端操控 (Scrcpy - USB A27 [R5GL91YT4BT])
echo 正在啟動正面主鏡遠端操控視窗 (Galaxy A27 [R5GL91YT4BT] - USB 有線)...
echo 提示：
echo 1. 滑鼠滾輪：可直接縮放鏡頭 (Zoom In / Out)
echo 2. 滑鼠左鍵長按：可對焦並鎖定曝光 (AE/AF Lock)
echo 3. 手機實體螢幕已自動熄滅，手機完全不發熱！
echo.
scrcpy -s R5GL91YT4BT --port=27185:27186 --window-title "正面主鏡 A27 (USB有線 / 滑鼠變焦與對焦)" --turn-screen-off --stay-awake
