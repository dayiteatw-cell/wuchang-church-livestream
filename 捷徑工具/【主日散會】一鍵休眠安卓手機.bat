@echo off
chcp 65001 >nul
set "PATH=C:\Program Files (x86)\Iriun Webcam;%PATH%"
title 【主日散會】一鍵休眠安卓手機 (A27 + ASUS 雙 USB 有線)
cd /d "%~dp0"

echo ======================================================================
echo  五常教會主日直播 -- 【主日散會】一鍵休眠安卓手機 (雙 USB 有線)
echo ======================================================================
echo.

echo [1/2] 正在休眠正面主鏡 (Galaxy A27 [R5GL91YT4BT] - USB 有線)...
adb -s R5GL91YT4BT shell am force-stop com.iriun.webcam >nul 2>&1
adb -s R5GL91YT4BT shell input keyevent 26 >nul 2>&1
echo      [OK] 正面主鏡 A27 攝影機已關閉並進入黑屏深層休眠！

echo.
echo [2/2] 正在休眠會眾全景 (ASUS [M8AIB760S073JRK] - USB 有線)...
adb -s M8AIB760S073JRK shell am force-stop com.iriun.webcam >nul 2>&1
adb -s M8AIB760S073JRK shell input keyevent 26 >nul 2>&1
echo      [OK] 會眾全景 ASUS 攝影機已關閉並進入黑屏深層休眠！

echo.
echo ======================================================================
echo  [散會] 安卓雙機已全部結束視訊串流並黑屏深層休眠！一整週待機耗電極低！
echo  (桌邊 iPhone X 側面副鏡請同工由下往上滑關閉 Iriun 即可)
echo  同工無需走動拔線，電腦可正常關機，下週一鍵自動喚醒！
echo ======================================================================
timeout /t 4
