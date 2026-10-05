@echo off
chcp 65001 >nul
title AGT 客户端

cd /d "%~dp0CLIENT\agt-app"
if not exist "package.json" (
    echo [错误] 没找到客户端目录: %~dp0CLIENT\agt-app
    echo        请把这个文件放在 AGT 项目根目录下再运行。
    pause
    exit /b 1
)

netstat -ano | findstr ":5091" | findstr "LISTENING" >nul
if errorlevel 1 (
    echo [警告] 后端服务似乎没有在运行 ^(端口 5091 未监听^)。
    echo        请先在另一个 PowerShell 窗口里执行:
    echo            cd /d %~dp0
    echo            .\start-local.ps1
    echo        否则客户端启动后会连不上后端。
    echo.
    pause
)

echo 正在启动 AGT 客户端, 请稍候...
echo 关闭本窗口即可退出客户端。
echo.

call npm run dev

echo.
echo 客户端已退出。
pause
