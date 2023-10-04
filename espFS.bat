
set "folder_path=%cd%"  
:: 当前文件夹路径
for %%F in ("%folder_path%\*.bin") do (
    move %%~nxF ./history_bin/%%~nxF
)


set h=%time:~0,2%
set h=%h: =0%
::补全小时中的空格
set file_name=SPIFFS_%date:~0,4%-%date:~5,2%-%date:~8,2%-%h%%time:~3,2%-%time:~6,2%.bin


::以4M3M为例
%~dp0mkspiffs -c %~dp0data -b 8192 -p 256 -s 0x2FA000 %~dp0%file_name%
%~dp0esptool.exe --chip esp8266 --baud 115200 write_flash -z 0x100000 %~dp0%file_name%

pause