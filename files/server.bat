@echo off
setlocal enabledelayedexpansion

REM Get local IP address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| find "IPv4 Address"') do (
    set "local_ip=%%a"
)

REM Remove leading and trailing spaces
set "local_ip=!local_ip:~1!"

echo Starting PHP server on !local_ip!:80...

CMD /K "php artisan serve --host=!local_ip! --port=80"
