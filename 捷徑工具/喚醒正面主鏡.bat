@echo off
chcp 65001 >nul
set "PATH=C:\Program Files (x86)\Iriun Webcam;%PATH%"
title 喚醒正面主鏡 (Wake Up - USB A27 [R5GL91YT4BT])
echo 正在喚醒正面主鏡 (Galaxy A27 [R5GL91YT4BT] - USB 有線)...
adb -s R5GL91YT4BT shell input keyevent 26 >nul 2>&1
adb -s R5GL91YT4BT shell input keyevent 82 >nul 2>&1
echo 正在啟動 Iriun Webcam App...
adb -s R5GL91YT4BT shell monkey -p com.iriun.webcam -c android.intent.category.LAUNCHER 1 >nul 2>&1
echo [成功] 正面主鏡已點亮並自動開啟 Iriun，鎖定 [Iriun Webcam #1]！
timeout /t 3
