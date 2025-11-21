# Script simplificado para iniciar Backend e Frontend
# Abre cada serviço em uma janela separada

$ErrorActionPreference = "Stop"

# Caminhos
$rootPath = $PSScriptRoot
$backendPath = Join-Path $rootPath "Backend"
$frontendPath = Join-Path $rootPath "Frontend"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Digital Superbank - Inicializador   " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar diretorios
if (!(Test-Path $backendPath)) {
    Write-Host "[X] Diretorio Backend nao encontrado!" -ForegroundColor Red
    exit 1
}

if (!(Test-Path $frontendPath)) {
    Write-Host "[X] Diretorio Frontend nao encontrado!" -ForegroundColor Red
    exit 1
}

Write-Host "[*] Iniciando Backend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; .\.venv\Scripts\Activate.ps1; python main.py"

Start-Sleep -Seconds 2

Write-Host "[*] Iniciando Frontend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; npm run dev"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   [OK] Servicos Iniciados!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "[WEB] Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "[WEB] Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "[DOC] API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "[INFO] Duas janelas foram abertas:" -ForegroundColor White
Write-Host "  - Backend (Python/FastAPI)" -ForegroundColor Gray
Write-Host "  - Frontend (React/Vite)" -ForegroundColor Gray
Write-Host ""
Write-Host "[!] Para parar os servicos, feche as janelas ou use Ctrl+C em cada uma" -ForegroundColor Yellow
Write-Host ""
