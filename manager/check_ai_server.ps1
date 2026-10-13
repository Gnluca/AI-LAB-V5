Write-Host ""
Write-Host "=== AI LAB V2 CHECK ===" -ForegroundColor Cyan
Write-Host ""

# FastAPI

Write-Host "Controllo FastAPI..." -ForegroundColor Yellow

try {
    $status = Invoke-RestMethod `
        -Uri "http://127.0.0.1:8000/status" `
        -TimeoutSec 5

    Write-Host "[OK] FastAPI Online" -ForegroundColor Green
    Write-Host "Modello: $($status.model)"
    Write-Host "Ollama : $($status.ollama)"
}
catch {
    Write-Host "[ERRORE] FastAPI Offline" -ForegroundColor Red
}

Write-Host ""

# Ollama

Write-Host "Controllo Ollama..." -ForegroundColor Yellow

$ollama = netstat -ano | findstr "11434"

if ($ollama) {
    Write-Host "[OK] Ollama sulla porta 11434" -ForegroundColor Green
}
else {
    Write-Host "[ERRORE] Ollama non trovato" -ForegroundColor Red
}

Write-Host ""

# Database

Write-Host ""
Write-Host "Controllo Database..." -ForegroundColor Yellow

if (Test-Path "E:\AI-Server\database\chat.db")
{
    $db = Get-Item "E:\AI-Server\database\chat.db"

$size = [math]::Round(($db.Length / 1024), 2)


    Write-Host "[OK] chat.db presente ($size KB)" -ForegroundColor Green
}
else
{
    Write-Host "[ERRORE] chat.db mancante" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== CHECK COMPLETATO ===" -ForegroundColor Cyan