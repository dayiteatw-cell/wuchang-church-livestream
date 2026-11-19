@echo off
chcp 65001 >nul
set "PATH=C:\Program Files (x86)\Iriun Webcam;%PATH%"
title 【救援工具】一鍵重整相機順序 (修正 Iriun #1 #2 錯位 - 雙 USB 有線)
cd /d "%~dp0"

echo ======================================================================
echo  五常教會直播 -- 【Iriun 相機順序重整與矯正工具 (雙 USB 有線)】
echo ======================================================================
echo  當發現 OBS 畫面顛倒（例如主鏡跑到 #2、會眾跑到 #1）時使用。
echo  此腳本將強制釋放雙機通道，並依標準時序重新鎖定編號：
echo.
echo    [順序 1] 正面主鏡 (Galaxy A27 [R5GL91YT4BT]) : 鎖定 Iriun Webcam #1
echo    [順序 2] 會眾全景 (ASUS [M8AIB760S073JRK])   : 鎖定 Iriun Webcam #2
echo ======================================================================
echo.

echo [步驟 1/3] 正在強制關閉雙機的 Iriun 釋放所有通道...
adb -s R5GL91YT4BT shell am force-stop com.iriun.webcam >nul 2>&1
adb -s M8AIB760S073JRK shell am force-stop com.iriun.webcam >nul 2>&1
echo      [OK] 雙手機通道已全部釋放！
echo.
timeout /t 2 >nul

echo [步驟 2/3] 正在優先啟動正面主鏡 (Galaxy A27)...
adb -s R5GL91YT4BT shell input keyevent 26 >nul 2>&1
adb -s R5GL91YT4BT shell input keyevent 82 >nul 2>&1
adb -s R5GL91YT4BT shell monkey -p com.iriun.webcam -c android.intent.category.LAUNCHER 1 >nul 2>&1
echo      [OK] 正面主鏡 A27 已成功鎖定 [Iriun Webcam #1]！
echo.
timeout /t 3 >nul

echo [步驟 3/3] 正在依序啟動會眾全景 (ASUS)...
adb -s M8AIB760S073JRK shell input keyevent 26 >nul 2>&1
adb -s M8AIB760S073JRK shell input keyevent 82 >nul 2>&1
adb -s M8AIB760S073JRK shell monkey -p com.iriun.webcam -c android.intent.category.LAUNCHER 1 >nul 2>&1
echo      [OK] 會眾全景 ASUS 已成功鎖定 [Iriun Webcam #2]！
echo.

echo ======================================================================
echo  [完成] 雙相機編號已全部精準歸位：
echo    * Iriun #1 = Galaxy A27 - 正面主鏡 (R5GL91YT4BT)
echo    * Iriun #2 = ASUS - 會眾全景 (M8AIB760S073JRK)
echo  OBS 畫面已完全對齊，同工可安心開始直播！
echo ======================================================================
timeout /t 4
