@echo off
chcp 65001 >nul
set "PATH=C:\Program Files (x86)\Iriun Webcam;%PATH%"
title 徹底關閉會眾全景 (Power Off - ASUS [M8AIB760S073JRK] - USB 有線)
cd /d "%~dp0"

echo ======================================================================
echo  【會眾全景徹底關機 (ASUS [M8AIB760S073JRK] - USB 有線)】
echo.
echo  [注意] 警語：
echo  手機一旦徹底關機（斷電），無法透過電腦遠端開機。
echo  下次聚會前同工必須走到腳架旁按實體電源鍵開機。
echo  平常主日散會建議使用【休眠會眾全景.bat】即可一鍵喚醒！
echo ======================================================================
echo.
set /p confirm=確定要讓 ASUS 會眾機徹底關閉電源嗎？(請輸入 Y 確定，其他鍵取消): 

if /i "%confirm%"=="Y" (
    echo.
    echo 正在發送關機指令...
    adb -s M8AIB760S073JRK reboot -p
    echo.
    echo [成功] ASUS 會眾全景手機已完全關閉電源。
) else (
    echo [已取消] 未執行關機。
)
timeout /t 5
