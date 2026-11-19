@echo off
chcp 65001 >nul
set "PATH=E:\Antigravity_Data\五常教會直播設置\scrcpy;C:\Program Files (x86)\Iriun Webcam;%PATH%"
title 會眾全景遠端操控 (Scrcpy - ASUS [M8AIB760S073JRK] - USB 有線)
cd /d "%~dp0"

echo 正在啟動會眾全景遠端操控視窗 (ASUS [M8AIB760S073JRK] - USB 有線)...
echo 提示：
echo 1. 滑鼠左鍵長按：可對焦並鎖定曝光
echo 2. 獨立通訊埠：27183:27184 (避免與正面主鏡衝突)
echo.
scrcpy -s M8AIB760S073JRK --port=27183:27184 --window-title "會眾全景 ASUS (USB有線 / 畫面監控與對焦)" --turn-screen-off --stay-awake
