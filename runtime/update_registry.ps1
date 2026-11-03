schtasks /create `
 /tn "AI-LAB Registry Update" `
 /sc minute `
 /mo 15 `
 /tr "powershell.exe -ExecutionPolicy Bypass -File E:\AI-Server\runtime\build_registry.ps1" `
 /f