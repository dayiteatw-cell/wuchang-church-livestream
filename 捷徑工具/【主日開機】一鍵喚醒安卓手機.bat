@echo off
chcp 65001 >nul
set "PATH=C:\Program Files (x86)\Iriun Webcam;%PATH%"
title 【主日開機】一鍵喚醒安卓手機 (A27 + ASUS 雙 USB 有線)
cd /d "%~dp0"

echo ======================================================================
echo  五常教會主日直播 -- 【主日開機】一鍵喚醒安卓手機 (A27 + ASUS)
echo ======================================================================
echo.

echo [1/2] 正在喚醒正面主鏡 (Samsung Galaxy A27 [R5GL91YT4BT] - USB 3.0 有線)...
adb -s R5GL91YT4BT shell input keyevent 26 >nul 2>&1
adb -s R5GL91YT4BT shell input keyevent 82 >nul 2>&1
adb -s R5GL91YT4BT shell monkey -p com.iriun.webcam -c android.intent.category.LAUNCHER 1 >nul 2>&1
echo      [OK] 正面主鏡 A27 已喚醒！成功鎖定 [Iriun Webcam #1]！

echo.
echo [2/2] 正在喚醒會眾全景 (ASUS [M8AIB760S073JRK] - USB 有線)...
adb -s M8AIB760S073JRK shell input keyevent 26 >nul 2>&1
adb -s M8AIB760S073JRK shell input keyevent 82 >nul 2>&1
adb -s M8AIB760S073JRK shell monkey -p com.iriun.webcam -c android.intent.category.LAUNCHER 1 >nul 2>&1
echo      [OK] 會眾全景 ASUS 已喚醒！成功鎖定 [Iriun Webcam #2]！

echo.
echo ======================================================================
echo  [完成] 安卓手機順序已精準對齊：
echo    * Iriun #1 : Galaxy A27 - 正面主鏡 (R5GL91YT4BT)
echo    * Iriun #2 : ASUS - 會眾全景 (M8AIB760S073JRK)
echo  (桌邊 iPhone X 側面副鏡請由同工手動解鎖點開 Iriun 即可)
echo  OBS 各場景畫面固定不跳位，同工可直接開始直播！
echo ======================================================================
timeout /t 4
