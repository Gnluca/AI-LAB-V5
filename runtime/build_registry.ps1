# ==========================================================
# AI-LAB V7
# Resource Discovery & Registry Builder
# ==========================================================

$Root = "E:\AI-Server"
$Registry = "E:\AI-Server\registry"

New-Item -ItemType Directory -Force -Path $Registry | Out-Null

Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host " AI-LAB RESOURCE DISCOVERY ENGINE"
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# ==========================================================
# NODE DISCOVERY
# ==========================================================

$Nodes = @{}

foreach ($Node in @(
    @{Name="node41"; IP="192.168.1.41"; Role="primary"},
    @{Name="node56"; IP="192.168.1.56"; Role="worker"}
))
{
    try {

        $Status = Invoke-RestMethod `
            "http://$($Node.IP):8000/status" `
            -TimeoutSec 5

        $Nodes[$Node.Name] = @{
            ip     = $Node.IP
            role   = $Node.Role
            status = "online"
        }

    }
    catch {

        $Nodes[$Node.Name] = @{
            ip     = $Node.IP
            role   = $Node.Role
            status = "offline"
        }

    }
}

$Nodes | ConvertTo-Json -Depth 10 |
    Set-Content "$Registry\nodes_registry.json"

Write-Host "[OK] Nodes Registry"

# ==========================================================
# PROJECT DISCOVERY
# ==========================================================

$Projects = @()

$ProjectRoot = "$Root\projects"

if(Test-Path $ProjectRoot)
{
    Get-ChildItem $ProjectRoot -Directory |
    ForEach-Object {

        $Projects += @{
            name   = $_.Name
            path   = $_.FullName
            node   = "node56"
            status = "detected"
        }

    }
}

# AI-Learning-Studio

if(Test-Path "E:\AI-Learning-Studio")
{
    $Projects += @{
        name   = "AI-Learning-Studio"
        path   = "E:\AI-Learning-Studio"
        node   = "node56"
        status = "detected"
    }
}

# SocialAI

if(Test-Path "E:\SocialAI")
{
    $Projects += @{
        name   = "SocialAI"
        path   = "E:\SocialAI"
        node   = "node56"
        status = "detected"
    }
}

@{
    generated = (Get-Date)
    projects  = $Projects
} | ConvertTo-Json -Depth 10 |
Set-Content "$Registry\projects_registry.json"

Write-Host "[OK] Projects Registry"

# ==========================================================
# PASSPORTS
# ==========================================================

$PassportDir = "$Registry\passports"

New-Item `
    -ItemType Directory `
    -Force `
    -Path $PassportDir | Out-Null

foreach($Project in $Projects)
{
    $Passport = @{
        name       = $Project.name
        type       = "application"
        owner      = "AI-LAB"
        node       = $Project.node
        path       = $Project.path
        status     = "online"
        registered = (Get-Date)
    }

    $Passport |
    ConvertTo-Json -Depth 10 |
    Set-Content (
        "$PassportDir\" +
        $Project.name +
        "_passport.json"
    )
}

Write-Host "[OK] Resource Passports"

# ==========================================================
# OLLAMA DISCOVERY
# ==========================================================

$Models = @{}

try {

    $Ollama =
        Invoke-RestMethod `
        "http://127.0.0.1:11434/api/tags"

    foreach($Model in $Ollama.models)
    {
        $Models[$Model.name] = @{
            status = "installed"
        }
    }

}
catch {

    $Models["ollama"] = @{
        status = "offline"
    }

}

$Models |
ConvertTo-Json -Depth 10 |
Set-Content "$Registry\models_registry.json"

Write-Host "[OK] Models Registry"

# ==========================================================
# WINDOWS SERVICES
# ==========================================================

$ServiceNames = @(
    "Schedule",
    "EventLog",
    "WinRM"
)

$Services = @()

foreach($Svc in $ServiceNames)
{
    try {

        $Obj = Get-Service $Svc

        $Services += @{
            name   = $Obj.Name
            status = $Obj.Status.ToString()
        }

    }
    catch {

        $Services += @{
            name   = $Svc
            status = "not_found"
        }

    }

}

$Services |
ConvertTo-Json -Depth 10 |
Set-Content "$Registry\services_registry.json"

Write-Host "[OK] Services Registry"

# ==========================================================
# STORAGE
# ==========================================================

$Drives = Get-PSDrive -PSProvider FileSystem |
ForEach-Object {

    @{
        drive    = $_.Name
        free_gb  = [math]::Round($_.Free / 1GB,2)
        used_gb  = [math]::Round(
            ($_.Used / 1GB),
            2
        )
    }
}

$Drives |
ConvertTo-Json -Depth 10 |
Set-Content "$Registry\storage_registry.json"

Write-Host "[OK] Storage Registry"

# ==========================================================
# HEALTH
# ==========================================================

$Health = @{
    timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    runtime   = "online"
    projects  = $Projects.Count
    models    = $Models.Count
    nodes     = $Nodes.Count
    score     = 100
    status    = "healthy"
}

$Health |
ConvertTo-Json -Depth 10 |
Set-Content "$Registry\health_registry.json"

Write-Host "[OK] Health Registry"

# ==========================================================
# SUMMARY
# ==========================================================

Write-Host ""
Write-Host "====================================" -ForegroundColor Green
Write-Host " DISCOVERY COMPLETED"
Write-Host "====================================" -ForegroundColor Green
Write-Host ""

$Health

Write-Host ""
Write-Host "Registry Path:"
Write-Host $Registry