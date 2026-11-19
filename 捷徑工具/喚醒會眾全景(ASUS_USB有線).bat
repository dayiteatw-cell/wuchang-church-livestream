@echo off
chcp 65001 >nul
set "PATH=C:\Program Files (x86)\Iriun Webcam;%PATH%"
title 喚醒會眾全景 (Wake Up - ASUS [M8AIB760S073JRK] - USB 有線)
cd /d "%~dp0"

echo 正在喚醒會眾全景 (ASUS [M8AIB760S073JRK] - USB 有線)...
adb -s M8AIB760S073JRK shell input keyevent 26 >nul 2>&1
adb -s M8AIB760S073JRK shell input keyevent 82 >nul 2>&1

echo 正在啟動 Iriun Webcam App...
adb -s M8AIB760S073JRK shell monkey -p com.iriun.webcam -c android.intent.category.LAUNCHER 1 >nul 2>&1

echo.
echo ======================================================================
echo  [成功] 會眾全景 ASUS 手機已點亮並自動開啟 Iriun！
echo  OBS 來源【Asus會眾全景】(Iriun #2) 立即連線就緒！
echo ======================================================================
timeout /t 3
