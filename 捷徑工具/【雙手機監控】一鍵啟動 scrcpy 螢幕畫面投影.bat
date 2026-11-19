@echo off
chcp 65001 >nul
set "PATH=E:\Antigravity_Data\五常教會直播設置\scrcpy;C:\Program Files (x86)\Iriun Webcam;%PATH%"
title 【雙手機監控】一鍵啟動 scrcpy 螢幕畫面投影
cd /d "%~dp0"

echo ======================================================================
echo  正在啟動雙機 scrcpy 畫面監控...
echo ======================================================================
echo.

echo [1/2] 正在開啟 ASUS (會眾全景)...
start "scrcpy_ASUS" scrcpy -s M8AIB760S073JRK --port=27183:27184 --window-title "會眾全景 ASUS (USB有線)"

timeout /t 2 >nul

echo.
echo [2/2] 正在開啟 Samsung Galaxy A27 (正面主鏡)...
start "scrcpy_A27" scrcpy -s R5GL91YT4BT --port=27185:27186 --window-title "正面主鏡 A27 (USB有線)"

echo.
echo ======================================================================
echo  [完成] 兩台手機投影視窗已全部啟動！
echo ======================================================================
timeout /t 3
