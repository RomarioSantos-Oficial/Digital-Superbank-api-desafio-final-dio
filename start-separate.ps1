#!/usr/bin/env pwsh
# Script simplificado para iniciar Backend e Frontend
# Digital Superbank - Quick Start

Write-Host ""
Write-Host "🏦 Digital Superbank - Quick Start" -ForegroundColor Cyan
Write-Host ""

$rootPath = $PSScriptRoot
$backendPath = Join-Path $rootPath "Backend"
$frontendPath = Join-Path $rootPath "Frontend"

# Iniciar Backend em nova janela
Write-Host "🚀 Iniciando Backend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; Write-Host '🔵 BACKEND - FastAPI' -ForegroundColor Cyan; Write-Host ''; if (Test-Path '.venv') { .\.venv\Scripts\Activate.ps1 }; python main.py"

# Aguardar 2 segundos
Start-Sleep -Seconds 2

# Iniciar Frontend em nova janela
Write-Host "🚀 Iniciando Frontend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; Write-Host '🟢 FRONTEND - React + Vite' -ForegroundColor Green; Write-Host ''; npm run dev"

Write-Host ""
Write-Host "✅ Serviços iniciados em janelas separadas!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "🌐 Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Feche as janelas do PowerShell para parar os serviços" -ForegroundColor Yellow
Write-Host ""
