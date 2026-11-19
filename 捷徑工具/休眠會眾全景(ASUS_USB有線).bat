@echo off
chcp 65001 >nul
set "PATH=C:\Program Files (x86)\Iriun Webcam;%PATH%"
title 休眠會眾全景 (Sleep - ASUS [M8AIB760S073JRK] - USB 有線)
cd /d "%~dp0"

echo 正在強制關閉 ASUS 會眾全景 Iriun 攝影機程式...
adb -s M8AIB760S073JRK shell am force-stop com.iriun.webcam >nul 2>&1

echo 正在關閉 ASUS 螢幕進入深層休眠...
adb -s M8AIB760S073JRK shell input keyevent 26 >nul 2>&1

echo.
echo ======================================================================
echo  [成功] 會眾全景 ASUS 手機 (M8AIB760S073JRK) 已黑屏深層休眠！
echo  鏡頭完全關閉、停止發熱、耗電降至最低，下週可一鍵直接喚醒！
echo ======================================================================
timeout /t 3
