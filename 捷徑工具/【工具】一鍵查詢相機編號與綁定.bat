@echo off
chcp 65001 >nul
set "PATH=C:\Program Files (x86)\Iriun Webcam;%PATH%"
title 【相機檢測與序號綁定工具】(A27 + ASUS 雙 USB 有線)
cd /d "%~dp0"

echo ======================================================================
echo  五常教會主日直播 -- 【雙手機 USB 有線序號檢測工具】
echo ======================================================================
echo  目前五常教會雙手機皆採用 USB 實體有線連接：
echo    1. Galaxy A27 (正面主鏡) : 序號 R5GL91YT4BT
echo    2. ASUS (會眾全景)       : 序號 M8AIB760S073JRK
echo ======================================================================
echo.

echo 正在掃描 USB 已連線的 Android 設備...
echo ----------------------------------------------------------------------
adb devices -l
echo ----------------------------------------------------------------------
echo.

echo 正在檢測正面主鏡 (R5GL91YT4BT)...
adb -s R5GL91YT4BT get-state >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo   [OK] 正面主鏡 Galaxy A27 (R5GL91YT4BT): USB 連線正常！
) else (
    echo   [!] 正面主鏡 Galaxy A27 (R5GL91YT4BT): 未連線，請檢查 USB 傳輸線或 USB 偵錯。
)

echo.
echo 正在檢測會眾全景 (M8AIB760S073JRK)...
adb -s M8AIB760S073JRK get-state >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo   [OK] 會眾全景 ASUS (M8AIB760S073JRK): USB 連線正常！
) else (
    echo   [!] 會眾全景 ASUS (M8AIB760S073JRK): 未連線，請檢查 USB 傳輸線或 USB 偵錯。
)

echo.
echo ======================================================================
echo  【USB 有線雙機綁定機制說明】
echo   * 雙機皆走實體 USB 傳輸，無 Wi-Fi 斷線、干擾或延遲問題。
echo   * 所有 BAT 腳本皆已嚴格綁定各自實體硬體序號 (-s 參數)。
echo   * 開機時序：A27 先點亮搶佔 Iriun #1，ASUS 接續點亮鎖定 Iriun #2。
echo ======================================================================
echo.
pause
