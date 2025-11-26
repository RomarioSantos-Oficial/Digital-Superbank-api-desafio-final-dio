# Script CORRIGIDO para iniciar Backend e Frontend
# Usa Start-Process em vez de Jobs para evitar problemas de ativação

param(
    [switch]$InitSetup = $false, # Se true, força a execução de setup inicial (venv, pip install, npm, populate_all)
    [switch]$RunCandles = $false, # Se true, roda geração de candles (via populate_all -RunCandles)
    [int]$CandlesDays = 7,       # Número de dias para geração de candles
    [switch]$ContinueOnError = $false,
    [switch]$NoInit = $false,     # Se true, não fará o setup automático mesmo que .venv esteja ausente
    [switch]$ExcludeChatbot = $false, # Se true, não popula o banco do chatbot
    [switch]$IncludeInteractiveChatbot = $false # Se true, popula a base interativa (populate_chatbot.py)
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Digital Superbank - Inicializador   " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "[Use] Start this script with -InitSetup to configure first-run (create venv, install requirements, npm install, populate DB)" -ForegroundColor Gray
Write-Host "[Options] -InitSetup -RunCandles -CandlesDays -ContinueOnError" -ForegroundColor Gray

$rootPath = $PSScriptRoot
$backendPath = Join-Path $rootPath "Backend"
$frontendPath = Join-Path $rootPath "Frontend"

# Verificar diretorios
if (!(Test-Path $backendPath)) {
    Write-Host "[X] Diretorio Backend nao encontrado!" -ForegroundColor Red
    exit 1
}

if (!(Test-Path $frontendPath)) {
    Write-Host "[X] Diretorio Frontend nao encontrado!" -ForegroundColor Red
    exit 1
}

Write-Host "[>] Backend: $backendPath" -ForegroundColor Gray
Write-Host "[>] Frontend: $frontendPath" -ForegroundColor Gray
Write-Host ""

# Verificar Python
try {
    $pythonVersion = python --version 2>$null
    Write-Host "[OK] Python: $pythonVersion" -ForegroundColor Green

# Forçar UTF-8 nas execuções do Python no Windows
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
} catch {
    Write-Host "[X] Python nao encontrado!" -ForegroundColor Red
    exit 1
}

# Verificar Node.js
try {
    $nodeVersion = node --version 2>$null
    Write-Host "[OK] Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "[X] Node.js nao encontrado!" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Verificar ambiente virtual
$venvPath = Join-Path $backendPath ".venv"
$venvPython = Join-Path $venvPath "Scripts\python.exe"
if (!(Test-Path $venvPath)) {
    if ($NoInit) {
        Write-Host "[X] Ambiente virtual não encontrado em $venvPath, e -NoInit foi especificado. Abortando." -ForegroundColor Red
        exit 1
    }

    Write-Host "[>] Ambiente virtual não encontrado: criando .venv automaticamente..." -ForegroundColor Yellow
    Push-Location $backendPath
    try {
        python -m venv .venv
    } catch {
        Write-Host "[X] Falha ao criar .venv com python -m venv: $_" -ForegroundColor Red
        Pop-Location
        exit 1
    }
    Pop-Location
    if (Test-Path $venvPath) { Write-Host "[OK] .venv criado" -ForegroundColor Green } else { Write-Host "[X] Falha ao criar .venv" -ForegroundColor Red; exit 1 }
    # Atualiza variável
    $venvPath = Join-Path $backendPath ".venv"; $venvPython = Join-Path $venvPath "Scripts\python.exe"
    # também força o InitSetup para instalar dependências e popular DB
    $InitSetup = $true
}

$venvPip = $venvPython

# Verificar node_modules
$nodeModulesPath = Join-Path $frontendPath "node_modules"
if (!(Test-Path $nodeModulesPath)) {
    Write-Host "[!] Instalando dependencias do Frontend..." -ForegroundColor Yellow
    Push-Location $frontendPath
    npm install
    Pop-Location
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Iniciando Servicos..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Se InitSetup estiver ativo (ou venv foi criado agora), instalar dependências e popular DB
if ($InitSetup) {
    Write-Host "[>] Modo InitSetup - instalando dependências e popular DB..." -ForegroundColor Cyan
    Set-Location $backendPath
    Write-Host "[>] Instalando requisitos do Backend via venv..." -ForegroundColor Gray
        & $venvPython -X utf8 -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) { Write-Host "[X] Falha ao instalar dependências do Backend" -ForegroundColor Red; if (-not $ContinueOnError) { exit 1 } }

    # Instalar dependências do frontend se falta (recheck)
    if (!(Test-Path $nodeModulesPath)) {
        Write-Host "[>] Instalando dependências do Frontend..." -ForegroundColor Gray
        Push-Location $frontendPath
        npm install
        Pop-Location
    }

    # Chamar populate_all.ps1 no root para popular DBs
    $populateScript = Join-Path $PSScriptRoot 'populate_all.ps1'
    if (!(Test-Path $populateScript)) {
        Write-Host "[X] populate_all.ps1 não encontrado: $populateScript" -ForegroundColor Red
    } else {
        Write-Host "[>] Executando populate_all.ps1 para popular o banco..." -ForegroundColor Gray
        $args = @()
        $args += '-InstallDeps'
        if ($RunCandles) { $args += '-RunCandles'; $args += "-Days $CandlesDays" }
        if ($ExcludeChatbot) { $args += '-ExcludeChatbot' }
        if ($IncludeInteractiveChatbot) { $args += '-IncludeInteractiveChatbot' }
        if ($ContinueOnError) { $args += '-ContinueOnError' }
        $argLine = $args -join ' '
        Set-Location $PSScriptRoot
        iex "& `"$populateScript`" $argLine"
        Set-Location $backendPath
    }
}

# Script para Backend
$backendScript = @"
Set-Location '$backendPath'
& '.\.venv\Scripts\Activate.ps1'
python main.py
"@

# Script para Frontend
$frontendScript = @"
Set-Location '$frontendPath'
npm run dev
"@

# Salvar scripts temporarios
$backendScriptPath = Join-Path $env:TEMP "backend_start.ps1"
$frontendScriptPath = Join-Path $env:TEMP "frontend_start.ps1"

$backendScript | Out-File -FilePath $backendScriptPath -Encoding UTF8
$frontendScript | Out-File -FilePath $frontendScriptPath -Encoding UTF8

# Iniciar Backend (que já inclui o simulador integrado)
Write-Host "[*] Iniciando Backend (com simulador integrado)..." -ForegroundColor Yellow
Write-Host "[>] URL: http://localhost:8000" -ForegroundColor Green
Write-Host "[>] Simulador de velas: Ativado automaticamente" -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-File", $backendScriptPath

Start-Sleep -Seconds 5

# Iniciar Frontend
Write-Host "[*] Iniciando Frontend..." -ForegroundColor Yellow
Write-Host "[>] URL: http://localhost:3000" -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-File", $frontendScriptPath

Start-Sleep -Seconds 2

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   [OK] Servicos Iniciados!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "[WEB] Backend:   http://localhost:8000" -ForegroundColor Cyan
Write-Host "[WEB] Frontend:  http://localhost:3000" -ForegroundColor Cyan
Write-Host "[DOC] API Docs:  http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "[SIM] Simulador: Integrado no Backend (velas a cada 1s)" -ForegroundColor Green
Write-Host ""
Write-Host "[!] 2 janelas PowerShell foram abertas:" -ForegroundColor Yellow
Write-Host "    1. Backend (porta 8000 + Simulador integrado)" -ForegroundColor White
Write-Host "    2. Frontend (porta 3000)" -ForegroundColor White
Write-Host ""
Write-Host "[!] Feche as janelas para parar os servicos" -ForegroundColor Yellow
Write-Host ""
Write-Host "Pressione qualquer tecla para continuar..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
