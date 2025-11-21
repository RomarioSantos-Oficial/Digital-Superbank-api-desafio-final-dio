# Script para iniciar Backend e Frontend simultaneamente
# Digital Superbank - Start Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Digital Superbank - Inicializador   " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$rootPath = $PSScriptRoot
$backendPath = Join-Path $rootPath "Backend"
$frontendPath = Join-Path $rootPath "Frontend"

# Verificar se os diretorios existem
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

# Função para verificar Node.js
function Test-NodeJs {
    try {
        $nodeVersion = node --version 2>$null
        return $true
    } catch {
        return $false
    }
}

# Função para verificar Python
function Test-Python {
    try {
        $pythonVersion = python --version 2>$null
        return $true
    } catch {
        return $false
    }
}

# Verificar dependencias
Write-Host "[*] Verificando dependencias..." -ForegroundColor Yellow
Write-Host ""

# Verificar Python
if (Test-Python) {
    $pythonVersion = python --version
    Write-Host "[OK] Python instalado: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "[X] Python nao encontrado!" -ForegroundColor Red
    Write-Host "    Instale Python 3.8+ de https://python.org" -ForegroundColor Yellow
    exit 1
}

# Verificar Node.js
if (Test-NodeJs) {
    $nodeVersion = node --version
    Write-Host "[OK] Node.js instalado: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "[X] Node.js nao encontrado!" -ForegroundColor Red
    Write-Host "    Instale Node.js 16+ de https://nodejs.org" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Verificar se as dependencias do Frontend estao instaladas
$nodeModulesPath = Join-Path $frontendPath "node_modules"
if (!(Test-Path $nodeModulesPath)) {
    Write-Host "[!] Dependencias do Frontend nao instaladas!" -ForegroundColor Yellow
    Write-Host "[*] Instalando dependencias do Frontend..." -ForegroundColor Yellow
    Push-Location $frontendPath
    npm install
    Pop-Location
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Dependencias do Frontend instaladas!" -ForegroundColor Green
    } else {
        Write-Host "[X] Erro ao instalar dependencias do Frontend!" -ForegroundColor Red
        exit 1
    }
    Write-Host ""
}

# Verificar se o ambiente virtual do Backend existe
$venvPath = Join-Path $backendPath ".venv"
if (!(Test-Path $venvPath)) {
    Write-Host "[!] Ambiente virtual do Backend nao encontrado!" -ForegroundColor Yellow
    Write-Host "[*] Por favor, configure o Backend primeiro executando:" -ForegroundColor Yellow
    Write-Host "    cd Backend" -ForegroundColor Cyan
    Write-Host "    python -m venv .venv" -ForegroundColor Cyan
    Write-Host "    .\.venv\Scripts\Activate.ps1" -ForegroundColor Cyan
    Write-Host "    pip install -r requirements.txt" -ForegroundColor Cyan
    Write-Host ""
    
    $createVenv = Read-Host "Deseja criar o ambiente virtual agora? (S/N)"
    if ($createVenv -eq 'S' -or $createVenv -eq 's' -or $createVenv -eq 'Y' -or $createVenv -eq 'y') {
        Write-Host "[*] Criando ambiente virtual..." -ForegroundColor Yellow
        Push-Location $backendPath
        python -m venv .venv
        
        Write-Host "[*] Instalando dependencias do Backend..." -ForegroundColor Yellow
        & ".\.venv\Scripts\Activate.ps1"
        pip install -r requirements.txt
        Pop-Location
        
        Write-Host "[OK] Ambiente virtual criado e dependencias instaladas!" -ForegroundColor Green
        Write-Host ""
    } else {
        exit 1
    }
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Iniciando Servicos..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Criar jobs para executar Backend, Simulador e Frontend em paralelo
Write-Host "[*] Iniciando Backend (Python/FastAPI)..." -ForegroundColor Yellow
Write-Host "[>] URL: http://localhost:8000" -ForegroundColor Green
Write-Host ""

$backendJob = Start-Job -ScriptBlock {
    param($path)
    Set-Location $path
    & ".\.venv\Scripts\Activate.ps1"
    python main.py
} -ArgumentList $backendPath

# Aguardar alguns segundos para o backend iniciar
Start-Sleep -Seconds 3

Write-Host "[*] Iniciando Simulador de Mercado..." -ForegroundColor Yellow
Write-Host "[>] Atualizando preços a cada 5 segundos" -ForegroundColor Green
Write-Host ""

$simulatorJob = Start-Job -ScriptBlock {
    param($path)
    Set-Location $path
    & ".\.venv\Scripts\Activate.ps1"
    python scripts/market_simulator.py --interval 5
} -ArgumentList $backendPath

# Aguardar alguns segundos
Start-Sleep -Seconds 2

Write-Host "[*] Iniciando Frontend (React/Vite)..." -ForegroundColor Yellow
Write-Host "[>] URL: http://localhost:3000" -ForegroundColor Green
Write-Host ""

$frontendJob = Start-Job -ScriptBlock {
    param($path)
    Set-Location $path
    npm run dev
} -ArgumentList $frontendPath

# Aguardar alguns segundos
Start-Sleep -Seconds 2

Write-Host "========================================" -ForegroundColor Green
Write-Host "   [OK] Servicos Iniciados!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "[WEB] Backend:   http://localhost:8000" -ForegroundColor Cyan
Write-Host "[WEB] Frontend:  http://localhost:3000" -ForegroundColor Cyan
Write-Host "[DOC] API Docs:  http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "[SIM] Mercado:   Atualizando a cada 5 segundos" -ForegroundColor Green
Write-Host ""
Write-Host "[!] Pressione Ctrl+C para parar todos os servicos" -ForegroundColor Yellow
Write-Host ""
Write-Host "[LOG] Logs dos servicos:" -ForegroundColor White
Write-Host "----------------------------------------" -ForegroundColor Gray

# Função para exibir logs
function Show-Logs {
    param($job, $name, $color)
    
    while ($true) {
        $output = Receive-Job -Job $job
        if ($output) {
            foreach ($line in $output) {
                Write-Host "[$name] " -ForegroundColor $color -NoNewline
                Write-Host $line
            }
        }
        Start-Sleep -Milliseconds 100
    }
}

# Monitorar jobs e exibir logs
try {
    while ($true) {
        # Verificar se os jobs ainda estao rodando
        if ($backendJob.State -ne "Running" -and $frontendJob.State -ne "Running" -and $simulatorJob.State -ne "Running") {
            Write-Host ""
            Write-Host "[!] Todos os servicos pararam!" -ForegroundColor Yellow
            break
        }
        
        # Exibir logs do backend
        $backendOutput = Receive-Job -Job $backendJob -ErrorAction SilentlyContinue
        if ($backendOutput) {
            foreach ($line in $backendOutput) {
                Write-Host "[BACKEND] " -ForegroundColor Magenta -NoNewline
                Write-Host $line
            }
        }
        
        # Exibir logs do simulador
        $simulatorOutput = Receive-Job -Job $simulatorJob -ErrorAction SilentlyContinue
        if ($simulatorOutput) {
            foreach ($line in $simulatorOutput) {
                Write-Host "[MARKET] " -ForegroundColor Yellow -NoNewline
                Write-Host $line
            }
        }
        
        # Exibir logs do frontend
        $frontendOutput = Receive-Job -Job $frontendJob -ErrorAction SilentlyContinue
        if ($frontendOutput) {
            foreach ($line in $frontendOutput) {
                Write-Host "[FRONTEND] " -ForegroundColor Cyan -NoNewline
                Write-Host $line
            }
        }
        
        Start-Sleep -Milliseconds 200
    }
} finally {
    # Cleanup ao sair (Ctrl+C ou erro)
    Write-Host ""
    Write-Host "[*] Parando servicos..." -ForegroundColor Yellow
    
    Stop-Job -Job $backendJob -ErrorAction SilentlyContinue
    Stop-Job -Job $simulatorJob -ErrorAction SilentlyContinue
    Stop-Job -Job $frontendJob -ErrorAction SilentlyContinue
    
    Remove-Job -Job $backendJob -Force -ErrorAction SilentlyContinue
    Remove-Job -Job $simulatorJob -Force -ErrorAction SilentlyContinue
    Remove-Job -Job $frontendJob -Force -ErrorAction SilentlyContinue
    
    Write-Host "[OK] Servicos parados!" -ForegroundColor Green
    Write-Host ""
}
