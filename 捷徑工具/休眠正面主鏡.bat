@echo off
chcp 65001 >nul
set "PATH=C:\Program Files (x86)\Iriun Webcam;%PATH%"
title 休眠正面主鏡 (Sleep - USB A27 [R5GL91YT4BT])
echo 正在強制關閉 Iriun 攝影機程式 (釋放相機鏡頭)...
adb -s R5GL91YT4BT shell am force-stop com.iriun.webcam >nul 2>&1
echo 正在關閉正面主鏡螢幕並進入深層休眠...
adb -s R5GL91YT4BT shell input keyevent 26 >nul 2>&1
echo [成功] 正面主鏡 (R5GL91YT4BT) 已釋放相機並進入黑屏休眠，同工無需起身！
timeout /t 3
