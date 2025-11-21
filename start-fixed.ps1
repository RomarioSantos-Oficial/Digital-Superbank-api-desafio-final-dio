# Script CORRIGIDO para iniciar Backend e Frontend
# Usa Start-Process em vez de Jobs para evitar problemas de ativação

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Digital Superbank - Inicializador   " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

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
if (!(Test-Path $venvPath)) {
    Write-Host "[X] Ambiente virtual nao encontrado em $venvPath" -ForegroundColor Red
    Write-Host "[*] Execute: cd Backend; python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

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
