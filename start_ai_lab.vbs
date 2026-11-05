Option Explicit

Dim sh
Set sh = CreateObject("WScript.Shell")

sh.Run "cmd /c E:\AI-Server\START_AI_LAB.bat", 0, False
