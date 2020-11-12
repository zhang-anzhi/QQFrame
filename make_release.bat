@echo off
set name=QQFrame
mkdir release
echo set a version: 
set /p ver=

mkdir release\%name%-%ver%

REM 扫地
rd /s /q utils\__pycache__
rd /s /q utils\parser\__pycache__

REM Readme, requirements, LICENSE
copy readme.md release\%name%-%ver%\readme.md
copy requirements.txt release\%name%-%ver%\requirements.txt
copy LICENSE release\%name%-%ver%\LICENSE

REM Main file
copy QQFrame.py release\%name%-%ver%\QQFrame.py
xcopy /e /y /q /i utils release\%name%-%ver%\utils
xcopy /e /y /q /i lang release\%name%-%ver%\lang

REM Zip
cd release
zip -r -q %name%-%ver%.zip %name%-%ver%
rd /s /q %name%-%ver%
cd ..

echo =========== Finish ===========
pause
