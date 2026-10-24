# ============================================
# AI-Learning-Studio Backup Script
# AI LAB V6.2
# ============================================

$ProjectName = "AI-Learning-Studio"

# Percorso progetto
$SourcePath = "E:\AI-Server\projects\$ProjectName"

# Cartella backup
$BackupRoot = "E:\Backup"

# Data e ora
$DateStamp = Get-Date -Format "yyyy-MM-dd_HHmmss"

# Nome archivio
$ZipFile = Join-Path $BackupRoot "$ProjectName`_$DateStamp.zip"

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host " AI-Learning-Studio Backup Utility"
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Verifica esistenza progetto
if (!(Test-Path $SourcePath))
{
    Write-Host "ERRORE: Progetto non trovato." -ForegroundColor Red
    Write-Host $SourcePath
    exit
}

# Crea cartella backup se assente
if (!(Test-Path $BackupRoot))
{
    New-Item -ItemType Directory -Path $BackupRoot -Force | Out-Null
}

Write-Host "Progetto :" $ProjectName -ForegroundColor Yellow
Write-Host "Origine  :" $SourcePath
Write-Host "Backup   :" $ZipFile
Write-Host ""

try
{
    Compress-Archive `
        -Path "$SourcePath\*" `
        -DestinationPath $ZipFile `
        -Force

    $SizeMB = [math]::Round((Get-Item $ZipFile).Length / 1MB, 2)

    Write-Host ""
    Write-Host "Backup completato con successo!" -ForegroundColor Green
    Write-Host "File :" $ZipFile
    Write-Host "Dimensione :" $SizeMB "MB"
}
catch
{
    Write-Host ""
    Write-Host "Backup fallito:" -ForegroundColor Red
    Write-Host $_.Exception.Message
}

Write-Host ""
Pause