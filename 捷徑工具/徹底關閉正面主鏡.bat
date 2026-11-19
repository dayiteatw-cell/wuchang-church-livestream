@echo off
chcp 65001 >nul
set "PATH=C:\Program Files (x86)\Iriun Webcam;%PATH%"
title 徹底關閉正面主鏡 (Power Off - USB A27 [R5GL91YT4BT])
echo ======================================================================
echo  【正面主鏡徹底關機 (Galaxy A27 [R5GL91YT4BT] - USB 有線)】
echo  注意：手機徹底關機後，無法透過電腦遠端開機。
echo  下次使用時，請走至講台前腳架旁按手機實體電源鍵開機。
echo ======================================================================
echo.
set /p confirm=確定要徹底關閉正面主鏡手機電源嗎？(請輸入 Y 確定，其他鍵取消): 
if /i "%confirm%"=="Y" (
    echo 正在執行關機...
    adb -s R5GL91YT4BT reboot -p
    echo [成功] 正面主鏡手機已安全存檔並完全關閉電源。
) else (
    echo [已取消] 未執行關機。
)
timeout /t 5
