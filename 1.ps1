# Script CORRIGIDO e AUTÔNOMO para iniciar Backend e Frontend
# Usa Start-Process para abrir janelas separadas para cada serviço.

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Digital Superbank - Inicializador   " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$rootPath = $PSScriptRoot
$backendPath = Join-Path $rootPath "Backend"
$frontendPath = Join-Path $rootPath "Frontend"

# ====================================================================
# 1. VERIFICAÇÕES INICIAIS
# ====================================================================

# Verificar diretorios
if (!(Test-Path $backendPath)) {
    Write-Host "[X] Diretorio Backend nao encontrado! Caminho esperado: $backendPath" -ForegroundColor Red
    exit 1
}

if (!(Test-Path $frontendPath)) {
    Write-Host "[X] Diretorio Frontend nao encontrado! Caminho esperado: $frontendPath" -ForegroundColor Red
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
    Write-Host "[X] Python nao encontrado! Certifique-se de que esta instalado e no PATH." -ForegroundColor Red
    exit 1
}

# Verificar Node.js
try {
    $nodeVersion = node --version 2>$null
    Write-Host "[OK] Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "[X] Node.js nao encontrado! Certifique-se de que esta instalado e no PATH." -ForegroundColor Red
    exit 1
}

Write-Host ""

# ====================================================================
# 2. CONFIGURAÇÃO DO BACKEND (PYTHON) - Criação e Instalação Sequencial
# ====================================================================

$venvPath = Join-Path $backendPath ".venv"
$backendRequirements = Join-Path $backendPath "requirements.txt"
$rootRequirements = Join-Path $rootPath "requirements.txt" # Arquivo na raiz

# A. Criar/Verificar Ambiente Virtual
if (!(Test-Path $venvPath)) {
    Write-Host "[!] Ambiente virtual (.venv) nao encontrado. Criando e configurando..." -ForegroundColor Yellow
    Push-Location $backendPath
    
    # Cria o ambiente virtual
    Write-Host "[*] Criando .venv..." -ForegroundColor Gray
    python -m venv .venv
    
    Pop-Location
    Write-Host "[OK] Ambiente virtual criado." -ForegroundColor Green
}

# B. Instalar dependências do Backend
if (Test-Path $backendRequirements) {
    Write-Host "[!] Instalando/Atualizando dependencias do Backend..." -ForegroundColor Yellow
    
    # Usa o pip dentro do venv para garantir a instalacao no ambiente correto
    & "$venvPath\Scripts\pip" install -r $backendRequirements
    
    Write-Host "[OK] Dependencias do Backend instaladas." -ForegroundColor Green
} else {
    Write-Host "[>] requirements.txt do Backend nao encontrado. Ignorando instalacao de dependencias Python." -ForegroundColor Gray
}

# C. Instalar dependências da Raiz (usando o ambiente virtual)
if (Test-Path $rootRequirements) {
    Write-Host "[!] Instalando/Atualizando dependencias da Raiz do Projeto..." -ForegroundColor Yellow
    
    # Usa o pip dentro do venv para a instalacao
    & "$venvPath\Scripts\pip" install -r $rootRequirements
    
    Write-Host "[OK] Dependencias da Raiz instaladas." -ForegroundColor Green
} else {
    Write-Host "[>] requirements.txt na Raiz nao encontrado. Ignorando instalacao extra." -ForegroundColor Gray
}

Write-Host ""

# ====================================================================
# 3. CONFIGURAÇÃO DO FRONTEND (NODE.JS) - Instalação de node_modules
# ====================================================================

$nodeModulesPath = Join-Path $frontendPath "node_modules"
if (!(Test-Path $nodeModulesPath)) {
    Write-Host "[!] node_modules nao encontrado. Instalando dependencias do Frontend (npm install)..." -ForegroundColor Yellow
    Push-Location $frontendPath
    npm install
    Pop-Location
    Write-Host "[OK] Dependencias do Frontend instaladas." -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Iniciando Servicos..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ====================================================================
# 4. INICIALIZAÇÃO DOS SERVIÇOS
# ====================================================================

# Script para Backend (Ativa o venv e roda o main.py)
$backendScript = @"
Set-Location '$backendPath'
& '$venvPath\Scripts\Activate.ps1'
python main.py
"@

# Script para Frontend (Roda o npm run dev)
$frontendScript = @"
Set-Location '$frontendPath'
npm run dev
"@

# Salvar scripts temporarios para execucao no Start-Process
$backendScriptPath = Join-Path $env:TEMP "backend_start.ps1"
$frontendScriptPath = Join-Path $env:TEMP "frontend_start.ps1"

$backendScript | Out-File -FilePath $backendScriptPath -Encoding UTF8
$frontendScript | Out-File -FilePath $frontendScriptPath -Encoding UTF8

# Iniciar Backend (que já inclui o simulador integrado)
Write-Host "[*] Iniciando Backend (com simulador integrado)..." -ForegroundColor Yellow
Write-Host "[>] URL: http://localhost:8000" -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-File", $backendScriptPath

Start-Sleep -Seconds 5 # Espera um pouco para o backend subir antes do frontend

# Iniciar Frontend
Write-Host "[*] Iniciando Frontend..." -ForegroundColor Yellow
Write-Host "[>] URL: http://localhost:3000" -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-File", $frontendScriptPath

Start-Sleep -Seconds 2

# ====================================================================
# 5. MENSAGEM FINAL
# ====================================================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Green

Write-Host "   [OK] Servicos Iniciados com Sucesso!  " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "[WEB] Backend:   http://localhost:8000" -ForegroundColor Cyan
Write-Host "[WEB] Frontend:  http://localhost:3000" -ForegroundColor Cyan
Write-Host "[DOC] API Docs:  http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "[SIM] Simulador: Integrado no Backend (velas a cada 1s)" -ForegroundColor Green
Write-Host ""
Write-Host "[!] Duas janelas PowerShell foram abertas. Feche-as para parar os servicos." -ForegroundColor Yellow
Write-Host ""
Write-Host "Pressione qualquer tecla para fechar esta janela do iniciador..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")