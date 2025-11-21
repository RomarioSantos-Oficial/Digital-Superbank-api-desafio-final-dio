# Script PowerShell para executar testes da API

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " TESTE COMPLETO - Digital Superbank API" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se servidor está rodando
Write-Host "[1/3] Verificando servidor..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/docs" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
    Write-Host "✓ Servidor rodando na porta 8000" -ForegroundColor Green
} catch {
    Write-Host "✗ Servidor NÃO está rodando!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Iniciando servidor..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; uvicorn main:app --reload"
    Write-Host "Aguardando 10 segundos para o servidor inicializar..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10
}

# Configurar encoding UTF-8
$env:PYTHONIOENCODING = "utf-8"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Executar testes
Write-Host ""
Write-Host "[2/3] Executando testes..." -ForegroundColor Yellow
Write-Host ""
python tests/test_all_services.py

# Finalizar
Write-Host ""
Write-Host "[3/3] Testes concluídos!" -ForegroundColor Green
Write-Host ""
Write-Host "Pressione qualquer tecla para sair..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
