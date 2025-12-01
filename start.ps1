<#
.SYNOPSIS
    Digital Superbank - Instalador e Inicializador Completo

.DESCRIPTION
    Script interativo para primeira instala??o e execu??o do Digital Superbank.
    Verifica depend?ncias, instala bibliotecas, cria banco de dados e popula dados.

.PARAMETER SkipInteractive
    Pula o modo interativo e usa configura??es padr?o

.PARAMETER NoData
    N?o popula dados (a??es, fundos, usu?rios)

.EXAMPLE
    .\start.ps1
    Modo interativo completo (recomendado para primeira vez)

.EXAMPLE
    .\start.ps1 -SkipInteractive
    Instala??o autom?tica com configura??es padr?o
#>

param(
    [switch]$SkipInteractive = $false,
    [switch]$NoData = $false
)

# ============================================================================
# FUN??ES AUXILIARES
# ============================================================================

function Write-Step {
    param([string]$Message, [string]$Status = "INFO")
    $colors = @{
        "INFO" = "Cyan"
        "SUCCESS" = "Green"
        "WARNING" = "Yellow"
        "ERROR" = "Red"
        "QUESTION" = "Magenta"
    }
    $icons = @{
        "INFO" = "[*]"
        "SUCCESS" = "[OK]"
        "WARNING" = "[!]"
        "ERROR" = "[X]"
        "QUESTION" = "[?]"
    }
    Write-Host "$($icons[$Status]) $Message" -ForegroundColor $colors[$Status]
}

function Test-Command {
    param([string]$Command)
    try {
        $null = Get-Command $Command -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

function Show-Banner {
    Clear-Host
    Write-Host ""
    Write-Host "??????????????????????????????????????????????????????????????????" -ForegroundColor Cyan
    Write-Host "?                                                                ?" -ForegroundColor Cyan
    Write-Host "?              DIGITAL SUPERBANK - INSTALADOR                    ?" -ForegroundColor Cyan
    Write-Host "?                                                                ?" -ForegroundColor Cyan
    Write-Host "?          Sistema Bancario Completo com Investimentos           ?" -ForegroundColor Cyan
    Write-Host "?                                                                ?" -ForegroundColor Cyan
    Write-Host "??????????????????????????????????????????????????????????????????" -ForegroundColor Cyan
    Write-Host ""
}

function Get-UserChoice {
    param(
        [string]$Question,
        [string]$Default = "S"
    )
    
    $choice = Read-Host "$Question (S/N) [Padr?o: $Default]"
    if ([string]::IsNullOrWhiteSpace($choice)) {
        $choice = $Default
    }
    return $choice.ToUpper() -eq "S"
}

# ============================================================================
# IN?CIO DO SCRIPT
# ============================================================================

Show-Banner

# ============================================================================
# ETAPA 1: VERIFICA??O DE ESTRUTURA E DEPEND?NCIAS
# ============================================================================

Write-Host "??????????????????????????????????????????????????????????????????" -ForegroundColor White
Write-Host "?  ETAPA 1: Verificando Estrutura e Depend?ncias                ?" -ForegroundColor White
Write-Host "??????????????????????????????????????????????????????????????????" -ForegroundColor White
Write-Host ""

$rootPath = $PSScriptRoot
$backendPath = Join-Path $rootPath "Backend"
$frontendPath = Join-Path $rootPath "Frontend"
$dbPath = Join-Path $backendPath "src\database\data\digital_superbank.db"

# Verificar estrutura de diret?rios
Write-Step "Verificando estrutura de diret?rios..." "INFO"

if (!(Test-Path $backendPath)) {
    Write-Step "Diret?rio Backend n?o encontrado!" "ERROR"
    Write-Host "   Certifique-se de estar executando o script na raiz do projeto." -ForegroundColor Red
    exit 1
}

if (!(Test-Path $frontendPath)) {
    Write-Step "Diret?rio Frontend n?o encontrado!" "ERROR"
    Write-Host "   Certifique-se de estar executando o script na raiz do projeto." -ForegroundColor Red
    exit 1
}

Write-Step "Estrutura de diret?rios OK" "SUCCESS"
Write-Host "   Backend:  $backendPath" -ForegroundColor Gray
Write-Host "   Frontend: $frontendPath" -ForegroundColor Gray
Write-Host ""

# Verificar Python
Write-Step "Verificando Python..." "INFO"
if (Test-Command "python") {
    $pythonVersion = python --version 2>&1
    Write-Step "Python instalado: $pythonVersion" "SUCCESS"
} else {
    Write-Step "Python N?O encontrado!" "ERROR"
    Write-Host ""
    Write-Host "   Por favor, instale Python 3.10 ou superior:" -ForegroundColor Yellow
    Write-Host "   https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}
Write-Host ""

# Verificar Node.js
Write-Step "Verificando Node.js..." "INFO"
if (Test-Command "node") {
    $nodeVersion = node --version 2>&1
    Write-Step "Node.js instalado: $nodeVersion" "SUCCESS"
} else {
    Write-Step "Node.js N?O encontrado!" "ERROR"
    Write-Host ""
    Write-Host "   Por favor, instale Node.js:" -ForegroundColor Yellow
    Write-Host "   https://nodejs.org/" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}
Write-Host ""

# Verificar se ? primeira instala??o
$isFirstInstall = $false
$venvPath = Join-Path $backendPath ".venv"

if (!(Test-Path $venvPath)) {
    $isFirstInstall = $true
    Write-Step "PRIMEIRA INSTALA??O DETECTADA" "WARNING"
    Write-Host "   Ambiente virtual Python n?o encontrado." -ForegroundColor Yellow
    Write-Host ""
} elseif (!(Test-Path $dbPath)) {
    $isFirstInstall = $true
    Write-Step "BANCO DE DADOS N?O ENCONTRADO" "WARNING"
    Write-Host "   Ser? necess?rio criar e popular o banco." -ForegroundColor Yellow
    Write-Host ""
}

# ============================================================================
# ETAPA 2: CONFIGURA??O DO AMBIENTE PYTHON
# ============================================================================

Write-Host "??????????????????????????????????????????????????????????????????" -ForegroundColor White
Write-Host "?  ETAPA 2: Configurando Ambiente Python                        ?" -ForegroundColor White
Write-Host "??????????????????????????????????????????????????????????????????" -ForegroundColor White
Write-Host ""

$venvPython = Join-Path $venvPath "Scripts\python.exe"

# Criar ambiente virtual se n?o existir
if (!(Test-Path $venvPath)) {
    Write-Step "Criando ambiente virtual Python..." "INFO"
    Set-Location $backendPath
    
    try {
        python -m venv .venv
        Write-Step "Ambiente virtual criado com sucesso!" "SUCCESS"
    } catch {
        Write-Step "Erro ao criar ambiente virtual" "ERROR"
        Write-Host "   Detalhes: $_" -ForegroundColor Red
        exit 1
    }
    
    $venvPython = Join-Path $venvPath "Scripts\python.exe"
} else {
    Write-Step "Ambiente virtual j? existe" "SUCCESS"
}
Write-Host ""

# Instalar/Atualizar depend?ncias do Backend
Write-Step "Verificando depend?ncias do Backend..." "INFO"
$requirementsPath = Join-Path $backendPath "requirements.txt"

if ($isFirstInstall -or $SkipInteractive -eq $false) {
    Write-Host "   Instalando bibliotecas Python (isso pode demorar)..." -ForegroundColor Yellow
    Set-Location $backendPath
    
    & $venvPython -m pip install --upgrade pip | Out-Null
    & $venvPython -m pip install -r $requirementsPath
    
    if ($LASTEXITCODE -eq 0) {
        Write-Step "Depend?ncias do Backend instaladas!" "SUCCESS"
    } else {
        Write-Step "Erro ao instalar depend?ncias" "ERROR"
        exit 1
    }
} else {
    Write-Step "Depend?ncias do Backend OK" "SUCCESS"
}
Write-Host ""

# ============================================================================
# ETAPA 3: CONFIGURA??O DO FRONTEND
# ============================================================================

Write-Host "??????????????????????????????????????????????????????????????????" -ForegroundColor White
Write-Host "?  ETAPA 3: Configurando Frontend                                ?" -ForegroundColor White
Write-Host "??????????????????????????????????????????????????????????????????" -ForegroundColor White
Write-Host ""

$nodeModulesPath = Join-Path $frontendPath "node_modules"

if (!(Test-Path $nodeModulesPath)) {
    Write-Step "Instalando depend?ncias do Frontend..." "INFO"
    Set-Location $frontendPath
    
    npm install
    
    if ($LASTEXITCODE -eq 0) {
        Write-Step "Depend?ncias do Frontend instaladas!" "SUCCESS"
    } else {
        Write-Step "Erro ao instalar depend?ncias do Frontend" "ERROR"
        exit 1
    }
} else {
    Write-Step "Depend?ncias do Frontend j? instaladas" "SUCCESS"
}
Write-Host ""

# ============================================================================
# ETAPA 4: CRIA??O E VERIFICA??O DO BANCO DE DADOS
# ============================================================================

Write-Host "??????????????????????????????????????????????????????????????????" -ForegroundColor White
Write-Host "?  ETAPA 4: Configurando Banco de Dados                         ?" -ForegroundColor White
Write-Host "??????????????????????????????????????????????????????????????????" -ForegroundColor White
Write-Host ""

Set-Location $backendPath

# Verificar se banco existe
if (!(Test-Path $dbPath)) {
    Write-Step "Criando estrutura do banco de dados..." "INFO"
    
    # Executa init_db.py para criar tabelas
    & $venvPython scripts\init_db.py
    
    if ($LASTEXITCODE -eq 0 -and (Test-Path $dbPath)) {
        Write-Step "Banco de dados criado com sucesso!" "SUCCESS"
    } else {
        Write-Step "Erro ao criar banco de dados" "ERROR"
        exit 1
    }
} else {
    Write-Step "Banco de dados j? existe" "SUCCESS"
}

# Verificar tabelas do banco
Write-Step "Verificando estrutura das tabelas..." "INFO"

$checkTablesScript = @'
import sqlite3
conn = sqlite3.connect("src/database/data/digital_superbank.db")
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
tables = cursor.fetchall()
print(str(len(tables)) + " tabelas encontradas")
for table in tables:
    print("  - " + table[0])
conn.close()
'@

$checkTablesScript | & $venvPython -

Write-Host ""

# ============================================================================
# ETAPA 5: POPULA??O DE DADOS (INTERATIVO)
# ============================================================================

if (-not $NoData) {
    Write-Host "??????????????????????????????????????????????????????????????????" -ForegroundColor White
    Write-Host "?  ETAPA 5: Populacao de Dados Iniciais                         ?" -ForegroundColor White
    Write-Host "??????????????????????????????????????????????????????????????????" -ForegroundColor White
    Write-Host ""
    
    Write-Host "DADOS PARA INSTALACAO:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "   [OBRIGATORIO] ACOES (30 empresas)" -ForegroundColor Green
    Write-Host "      - Empresas de Tecnologia, Energia, Financas, Saude" -ForegroundColor Gray
    Write-Host "      - Arquivo: demo/acao.txt" -ForegroundColor Gray
    Write-Host ""
    Write-Host "   [OBRIGATORIO] FUNDOS IMOBILIARIOS (25 fundos)" -ForegroundColor Green
    Write-Host "      - Lajes Corporativas, Shopping, Logistica, etc." -ForegroundColor Gray
    Write-Host "      - Arquivo: demo/fundo_investimento.txt" -ForegroundColor Gray
    Write-Host ""
    Write-Host "   [OBRIGATORIO] CHATBOT (40+ perguntas e respostas)" -ForegroundColor Green
    Write-Host "      - Base de conhecimento completa" -ForegroundColor Gray
    Write-Host "      - Arquivo: demo/chatbot_conhecimento.txt" -ForegroundColor Gray
    Write-Host ""
    Write-Host "   [OPCIONAL] USUARIOS DEMO (37 usuarios)" -ForegroundColor Yellow
    Write-Host "      - 20 usuarios com 3 contas cada" -ForegroundColor Gray
    Write-Host "      - 17 usuarios com perfis variados" -ForegroundColor Gray
    Write-Host "      - Arquivo: demo/pessoa.txt" -ForegroundColor Gray
    Write-Host ""
    
    # Acoes, Fundos e Chatbot sao OBRIGATORIOS na primeira instalacao
    $installStocks = $true
    $installFunds = $true
    $installChatbot = $true
    $installUsers = $true
    
    if (-not $SkipInteractive) {
        Write-Host "----------------------------------------------------------------" -ForegroundColor DarkGray
        $installUsers = Get-UserChoice "   [>] Instalar USUARIOS DE DEMONSTRACAO (37 usuarios)?"
        Write-Host "----------------------------------------------------------------" -ForegroundColor DarkGray
        Write-Host ""
    }
    
    # Executar scripts selecionados
    Write-Step "Populando banco de dados..." "INFO"
    Write-Host ""
    
    # 1. OBRIGATORIO: Acoes (sempre instalado)
    Write-Host "   [1/5] Criando acoes..." -ForegroundColor Cyan
    & $venvPython scripts\generate_stocks.py --update 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Step "30 acoes criadas!" "SUCCESS"
    } else {
        Write-Step "Erro ao criar acoes!" "ERROR"
    }
    
    # 2. OBRIGATORIO: Fundos Imobiliarios (sempre instalado)
    Write-Host "   [2/5] Criando fundos imobiliarios..." -ForegroundColor Cyan
    & $venvPython scripts\generate_funds.py --update 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Step "25 fundos criados!" "SUCCESS"
    } else {
        Write-Step "Erro ao criar fundos!" "ERROR"
    }
    
    # 3. OBRIGATORIO: Chatbot (sempre instalado)
    Write-Host "   [3/5] Populando base de conhecimento do chatbot..." -ForegroundColor Cyan
    & $venvPython scripts\populate_chatbot_from_file.py --update 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Step "Chatbot configurado!" "SUCCESS"
    } else {
        Write-Step "Erro ao configurar chatbot!" "ERROR"
    }
    
    # 4. Ativos de renda fixa
    Write-Host "   [4/5] Adicionando ativos de renda fixa..." -ForegroundColor Cyan
    & $venvPython scripts\add_fixed_income_assets.py 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Step "Renda fixa adicionada!" "SUCCESS"
    }
    
    # 5. OPCIONAL: Usuarios de demonstracao
    if ($installUsers) {
        Write-Host "   [5/5] Criando usuarios de demonstracao..." -ForegroundColor Cyan
        & $venvPython scripts\generate_demo_users.py --update 2>&1 | Out-Null
        & $venvPython scripts\generate_varied_users.py 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Step "37 usuarios criados!" "SUCCESS"
        } else {
            Write-Step "Erro ao criar usuarios!" "ERROR"
        }
    } else {
        Write-Host "   [5/5] Usuarios de demonstracao PULADOS (opcao do usuario)" -ForegroundColor Yellow
    }
    
    Write-Host ""
    Write-Step "Populacao de dados concluida!" "SUCCESS"
    Write-Host ""
}

# ============================================================================
# ETAPA 6: VERIFICA??O FINAL E RELAT?RIO
# ============================================================================

Write-Host "??????????????????????????????????????????????????????????????????" -ForegroundColor White
Write-Host "?  ETAPA 6: Verifica??o Final do Sistema                        ?" -ForegroundColor White
Write-Host "??????????????????????????????????????????????????????????????????" -ForegroundColor White
Write-Host ""

Write-Step "Executando verifica??o final..." "INFO"
Write-Host ""

# Verificar banco de dados
$dbExists = Test-Path $dbPath
$venvExists = Test-Path $venvPath
$nodeModulesExists = Test-Path $nodeModulesPath

# Contar registros no banco
if ($dbExists) {
    $statsScript = @'
import sqlite3
conn = sqlite3.connect("src/database/data/digital_superbank.db")
cursor = conn.cursor()

# Contar registros
cursor.execute("SELECT COUNT(*) FROM assets WHERE asset_type='STOCK'")
stocks = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM assets WHERE asset_type='FUND'")
funds = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM users")
users = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM accounts")
accounts = cursor.fetchone()[0]

print("stocks:" + str(stocks))
print("funds:" + str(funds))
print("users:" + str(users))
print("accounts:" + str(accounts))

conn.close()
'@

    $stats = $statsScript | & $venvPython - 2>&1
    $stocksCount = ($stats | Select-String "stocks:(\d+)").Matches.Groups[1].Value
    $fundsCount = ($stats | Select-String "funds:(\d+)").Matches.Groups[1].Value
    $usersCount = ($stats | Select-String "users:(\d+)").Matches.Groups[1].Value
    $accountsCount = ($stats | Select-String "accounts:(\d+)").Matches.Groups[1].Value
}

# Exibir relat?rio
Write-Host "??????????????????????????????????????????????????????????????????" -ForegroundColor Green
Write-Host "?                   RELATORIO DE INSTALACAO                      ?" -ForegroundColor Green
Write-Host "??????????????????????????????????????????????????????????????????" -ForegroundColor Green
Write-Host "?                                                                ?" -ForegroundColor Green

if ($venvExists) {
    Write-Host "?  [OK] Ambiente Python            OK                          ?" -ForegroundColor Green
} else {
    Write-Host "?  [X]  Ambiente Python            ERRO                        ?" -ForegroundColor Red
}

if ($nodeModulesExists) {
    Write-Host "?  [OK] Dependencias Frontend      OK                          ?" -ForegroundColor Green
} else {
    Write-Host "?  [X]  Dependencias Frontend      ERRO                        ?" -ForegroundColor Red
}

if ($dbExists) {
    Write-Host "?  [OK] Banco de Dados             OK                          ?" -ForegroundColor Green
    Write-Host "?                                                                ?" -ForegroundColor Green
    Write-Host "?  DADOS INSTALADOS:                                             ?" -ForegroundColor Green
    Write-Host "?     - Acoes:                     $stocksCount empresas        " -NoNewline -ForegroundColor Green
    Write-Host " " * (30 - $stocksCount.Length) "?" -ForegroundColor Green
    Write-Host "?     - Fundos Imobiliarios:       $fundsCount fundos          " -NoNewline -ForegroundColor Green
    Write-Host " " * (30 - $fundsCount.Length) "?" -ForegroundColor Green
    Write-Host "?     - Usuarios:                  $usersCount usuarios        " -NoNewline -ForegroundColor Green
    Write-Host " " * (30 - $usersCount.Length) "?" -ForegroundColor Green
    Write-Host "?     - Contas Bancarias:          $accountsCount contas       " -NoNewline -ForegroundColor Green
    Write-Host " " * (30 - $accountsCount.Length) "?" -ForegroundColor Green
} else {
    Write-Host "?  [X]  Banco de Dados             ERRO                        ?" -ForegroundColor Red
}

Write-Host "?                                                                ?" -ForegroundColor Green
Write-Host "??????????????????????????????????????????????????????????????????" -ForegroundColor Green
Write-Host ""

if (-not $venvExists -or -not $nodeModulesExists -or -not $dbExists) {
    Write-Step "Instala??o incompleta! Verifique os erros acima." "ERROR"
    exit 1
}

Write-Step "Sistema instalado e verificado com sucesso!" "SUCCESS"
Write-Host ""

# ============================================================================
# ETAPA 7: INICIAR APLICA??O
# ============================================================================

Write-Host "??????????????????????????????????????????????????????????????????" -ForegroundColor White
Write-Host "?  ETAPA 7: Iniciando Aplica??o                                  ?" -ForegroundColor White
Write-Host "??????????????????????????????????????????????????????????????????" -ForegroundColor White
Write-Host ""

if (-not $SkipInteractive) {
    $startNow = Get-UserChoice "   [>] Deseja iniciar o Digital Superbank agora?"
    if (-not $startNow) {
        Write-Host ""
        Write-Step "Instalacao concluida!" "SUCCESS"
        Write-Host ""
        Write-Host "   Para iniciar o sistema posteriormente, execute:" -ForegroundColor Cyan
        Write-Host "   .\start.ps1 -SkipInteractive" -ForegroundColor Yellow
        Write-Host ""
        exit 0
    }
}

Write-Host ""
Write-Step "Iniciando Backend e Frontend..." "INFO"
Write-Host ""
# Criar scripts tempor?rios para Backend e Frontend
$backendScript = @"
Set-Location '$backendPath'
& '.\.venv\Scripts\Activate.ps1'
python main.py
"@

$frontendScript = @"
Set-Location '$frontendPath'
npm run dev
"@

$backendScriptPath = Join-Path $env:TEMP "backend_start.ps1"
$frontendScriptPath = Join-Path $env:TEMP "frontend_start.ps1"

$backendScript | Out-File -FilePath $backendScriptPath -Encoding UTF8
$frontendScript | Out-File -FilePath $frontendScriptPath -Encoding UTF8

# Iniciar Backend
Write-Host "   [>] Iniciando Backend..." -ForegroundColor Cyan
Write-Host "      URL: http://localhost:8000" -ForegroundColor Gray
Write-Host "      Docs: http://localhost:8000/docs" -ForegroundColor Gray
Start-Process powershell -ArgumentList "-NoExit", "-File", $backendScriptPath

Start-Sleep -Seconds 3

# Iniciar Frontend
Write-Host ""
Write-Host "   [>] Iniciando Frontend..." -ForegroundColor Cyan
Write-Host "      URL: http://localhost:3000" -ForegroundColor Gray
Start-Process powershell -ArgumentList "-NoExit", "-File", $frontendScriptPath

Start-Sleep -Seconds 2

# Mensagem final
Write-Host ""
Write-Host ""
Write-Host "??????????????????????????????????????????????????????????????????" -ForegroundColor Green
Write-Host "?                                                                ?" -ForegroundColor Green
Write-Host "?           DIGITAL SUPERBANK INICIADO COM SUCESSO!              ?" -ForegroundColor Green
Write-Host "?                                                                ?" -ForegroundColor Green
Write-Host "??????????????????????????????????????????????????????????????????" -ForegroundColor Green
Write-Host ""
Write-Host "ACESSE O SISTEMA:" -ForegroundColor Cyan
Write-Host ""
Write-Host "   Frontend:     http://localhost:3000" -ForegroundColor Yellow
Write-Host "   Backend API:  http://localhost:8000" -ForegroundColor Yellow
Write-Host "   Documentacao: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host ""
Write-Host "USUARIOS DE TESTE:" -ForegroundColor Cyan
Write-Host ""

if ($usersCount -gt 0) {
    Write-Host "   Email:  joao.silva@superbank.com.br" -ForegroundColor White
    Write-Host "   Senha:  Senha1@2025" -ForegroundColor White
    Write-Host ""
    Write-Host "   Veja todos os usuarios em: pessoa.txt" -ForegroundColor Gray
} else {
    Write-Host "   [!] Nenhum usuario de teste instalado" -ForegroundColor Yellow
    Write-Host "   Execute novamente com dados para criar usuarios" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "INFORMACOES:" -ForegroundColor Cyan
Write-Host ""
Write-Host "   * 2 janelas PowerShell foram abertas:" -ForegroundColor White
Write-Host "     - Backend (porta 8000)" -ForegroundColor Gray
Write-Host "     - Frontend (porta 3000)" -ForegroundColor Gray
Write-Host ""
Write-Host "   * Para parar os servicos:" -ForegroundColor White
Write-Host "     - Feche as janelas PowerShell abertas" -ForegroundColor Gray
Write-Host ""
Write-Host "   * Arquivos de dados criados:" -ForegroundColor White
Write-Host "     [OK] demo/acao.txt (30 acoes)" -ForegroundColor Green
Write-Host "     [OK] demo/fundo_investimento.txt (25 fundos)" -ForegroundColor Green
Write-Host "     [OK] demo/chatbot_conhecimento.txt (40+ perguntas)" -ForegroundColor Green
if ($installUsers) { Write-Host "     [OK] demo/pessoa.txt (37 usuarios)" -ForegroundColor Green }
Write-Host ""
Write-Host "??????????????????????????????????????????????????????????????" -ForegroundColor DarkGray
Write-Host ""
Write-Host "Pressione qualquer tecla para fechar esta janela..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
