@echo off
color 2
echo Auto opener starts!
msg /time:2 * Auto opener starts!
:loop
timeout /t 20
taskkill /im chrome.exe /f
echo Program starting!
msg /time:2 * Program starting!
timeout /t 1
start chrome.exe
cd C:\Users\Lukáš\Desktop
cd C:\Program Files (x86)\Microsoft\Edge\Application
start msedge https://trigger.macrodroid.com
timeout /t 3
taskkill /im msedge.exe /f
goto loop
exit
