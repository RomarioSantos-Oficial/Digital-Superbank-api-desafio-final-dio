#!/usr/bin/env pwsh
# Script de instalação e execução do Frontend - Digital Superbank

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Digital Superbank - Frontend Setup  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se Node.js está instalado
Write-Host "🔍 Verificando Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js instalado: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js não encontrado!" -ForegroundColor Red
    Write-Host "   Por favor, instale o Node.js 16+ de https://nodejs.org" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Verificar se npm está instalado
Write-Host "🔍 Verificando npm..." -ForegroundColor Yellow
try {
    $npmVersion = npm --version
    Write-Host "✅ npm instalado: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ npm não encontrado!" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Perguntar se deseja instalar dependências
Write-Host "📦 Deseja instalar as dependências? (S/N)" -ForegroundColor Cyan
$install = Read-Host

if ($install -eq 'S' -or $install -eq 's' -or $install -eq 'Y' -or $install -eq 'y') {
    Write-Host ""
    Write-Host "📥 Instalando dependências..." -ForegroundColor Yellow
    npm install
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Dependências instaladas com sucesso!" -ForegroundColor Green
    } else {
        Write-Host "❌ Erro ao instalar dependências!" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""

# Verificar se arquivo .env existe
if (!(Test-Path ".env")) {
    Write-Host "⚙️  Criando arquivo .env..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✅ Arquivo .env criado!" -ForegroundColor Green
} else {
    Write-Host "✅ Arquivo .env já existe!" -ForegroundColor Green
}

Write-Host ""

# Perguntar se deseja iniciar o servidor
Write-Host "🚀 Deseja iniciar o servidor de desenvolvimento? (S/N)" -ForegroundColor Cyan
$start = Read-Host

if ($start -eq 'S' -or $start -eq 's' -or $start -eq 'Y' -or $start -eq 'y') {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  Iniciando Frontend..." -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📍 URL: http://localhost:3000" -ForegroundColor Green
    Write-Host "📍 API: http://localhost:8000" -ForegroundColor Green
    Write-Host ""
    Write-Host "Pressione Ctrl+C para parar o servidor" -ForegroundColor Yellow
    Write-Host ""
    
    npm run dev
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  Instalação concluída!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Para iniciar o servidor, execute:" -ForegroundColor Yellow
    Write-Host "  npm run dev" -ForegroundColor Cyan
    Write-Host ""
}
