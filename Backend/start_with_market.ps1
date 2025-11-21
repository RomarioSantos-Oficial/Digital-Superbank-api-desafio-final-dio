# Script PowerShell para iniciar o Backend + Simulador de Mercado
# Usa: .\start_with_market.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 DIGITAL SUPERBANK - INICIALIZADOR" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verifica se está no diretório correto
if (-Not (Test-Path "main.py")) {
    Write-Host "❌ Erro: Execute este script do diretório Backend/" -ForegroundColor Red
    exit 1
}

Write-Host "🔧 Iniciando serviços..." -ForegroundColor Yellow
Write-Host ""

# Inicia o backend FastAPI em background
Write-Host "📡 Iniciando API Backend (porta 8000)..." -ForegroundColor Green
$backend = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python main.py" -PassThru

# Aguarda 3 segundos para o backend iniciar
Start-Sleep -Seconds 3

# Inicia o simulador de mercado em background
Write-Host "📈 Iniciando Simulador de Mercado (atualização a cada 10s)..." -ForegroundColor Green
$simulator = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python scripts/market_simulator.py --interval 10" -PassThru

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ SERVIÇOS INICIADOS COM SUCESSO!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📡 Backend API:      http://localhost:8000" -ForegroundColor White
Write-Host "📊 Docs (Swagger):   http://localhost:8000/docs" -ForegroundColor White
Write-Host "📈 Simulador:        Rodando (10s de intervalo)" -ForegroundColor White
Write-Host ""
Write-Host "Para alterar intervalo do simulador:" -ForegroundColor Yellow
Write-Host "  - Feche a janela do simulador" -ForegroundColor Yellow
Write-Host "  - Execute: python scripts/market_simulator.py --interval <segundos>" -ForegroundColor Yellow
Write-Host ""
Write-Host "Para parar os serviços:" -ForegroundColor Yellow
Write-Host "  - Feche ambas as janelas do PowerShell" -ForegroundColor Yellow
Write-Host "  - Ou pressione Ctrl+C em cada janela" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Pressione qualquer tecla para sair deste script..." -ForegroundColor Gray
Write-Host "(Os serviços continuarão rodando em outras janelas)" -ForegroundColor Gray
Write-Host "========================================" -ForegroundColor Cyan

$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
