<#
Populate All - PowerShell Script Interativo

Descrição:
  Script INTERATIVO para popular bancos de dados específicos.
  Permite escolher quais dados adicionar: ações, fundos, pessoas ou chatbot.

Parâmetros:
  -All:          Popula todos os bancos de dados (não interativo)
  -InstallDeps:  Instala dependências antes de executar
  -RunCandles:   Executa a geração de velas históricas (padrão: $false)
  -Days:         Número de dias para gerar velas (padrão: 7)

Uso exemplo:
  .\populate_all.ps1              (Modo interativo - RECOMENDADO)
  .\populate_all.ps1 -All         (Popula tudo automaticamente)
#>
param (
    [switch]$All = $false,
    [switch]$InstallDeps = $false,
    [switch]$RunCandles = $false,
    [int]$Days = 7
)

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$ts] [$Level] $Message"
}

function Show-Banner {
    Clear-Host
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host "       DIGITAL SUPERBANK - POPULADOR DE DADOS INTERATIVO" -ForegroundColor Cyan
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host ""
}

function Get-UserChoice {
    param([string]$Question)
    $choice = Read-Host "$Question (S/N)"
    return $choice.ToUpper() -eq "S"
}

# Determina o diretório raiz do repositório (onde o script .ps1 está)
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
$BackendDir = Join-Path $ScriptRoot 'Backend'

Write-Log "Root do projeto: $ScriptRoot"
Write-Log "Pasta Backend: $BackendDir"

if (!(Test-Path $BackendDir)) {
    Write-Log "Pasta Backend não encontrada: $BackendDir" "ERROR"
    exit 1
}

Set-Location $BackendDir

# Tenta localizar python (fallback para "py")
$pythonCmd = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $pythonCmd) {
    $pythonCmd = (Get-Command py -ErrorAction SilentlyContinue).Source
}

if (-not $pythonCmd) {
    Write-Log "Nenhum interpretador Python encontrado no PATH (procure por 'python' ou 'py')." "ERROR"
    exit 1
}

Write-Log "Usando comando Python: $pythonCmd"

function Run-Script {
    param(
        [string]$ScriptPath,
        [string]$Arguments = ""
    )

    $fullCmd = "& $pythonCmd `"$ScriptPath`" $Arguments"
    Write-Log "Executando: $fullCmd"

    try {
        # Força Python a usar UTF-8 para evitar UnicodeEncodeError no Windows consoles
        $oldPythonIO = $env:PYTHONIOENCODING
        $oldPythonUTF8 = $env:PYTHONUTF8
        $env:PYTHONIOENCODING = 'utf-8'
        $env:PYTHONUTF8 = '1'

        # Executa explicitamente e escreve saída para log (UTF-8)
        $scriptNameSafe = ([IO.Path]::GetFileName($ScriptPath)).Replace(' ', '_')
        $logFilePath = Join-Path $BackendDir "logs\$scriptNameSafe.log"
        if (!(Test-Path (Split-Path $logFilePath))) { New-Item -Path (Split-Path $logFilePath) -ItemType Directory -Force | Out-Null }
        Write-Log "Executando e gravando log: $logFilePath"
        & $pythonCmd $ScriptPath $Arguments *>&1 | Out-File -FilePath $logFilePath -Encoding utf8 -Append
        if (!$LASTEXITCODE -or $LASTEXITCODE -eq 0) {
            Write-Log "Sucesso: $ScriptPath"
            return $true
# Passo opcional: instalar dependências
if ($InstallDeps) {
    Write-Log "Instalando dependências do Backend/requirements.txt..."
    $reqFile = Join-Path $BackendDir 'requirements.txt'
    if (Test-Path $reqFile) {
        iex "& $pythonCmd -m pip install -r `"$reqFile`""
        if (!$LASTEXITCODE -or $LASTEXITCODE -eq 0) {
            Write-Log "Dependências instaladas com sucesso."
        } else {
            Write-Log "Falha ao instalar dependências com exit code $LASTEXITCODE" "ERROR"
            exit $LASTEXITCODE
        }
    } else {
        Write-Log "Arquivo de requirements não encontrado: $reqFile" "WARN"
    }
}

# Modo interativo ou automático
if (-not $All) {
    Show-Banner
    
    Write-Host "Este script permite adicionar novos dados ao banco de dados." -ForegroundColor Yellow
    Write-Host "Escolha quais dados você deseja popular:" -ForegroundColor Yellow
    Write-Host ""
    
    # Perguntar sobre cada tipo de dado
    $populateStocks = Get-UserChoice "Deseja adicionar/atualizar ACOES"
    $populateFunds = Get-UserChoice "Deseja adicionar/atualizar FUNDOS IMOBILIARIOS"
    $populateFixedIncome = Get-UserChoice "Deseja adicionar/atualizar RENDA FIXA"
    $populateUsers = Get-UserChoice "Deseja adicionar/atualizar USUARIOS (demo e variados)"
    $populateChatbot = Get-UserChoice "Deseja adicionar/atualizar CHATBOT (base de conhecimento)"
    $generateCandles = Get-UserChoice "Deseja gerar VELAS HISTORICAS (pode demorar)"
    
    if ($generateCandles) {
        $Days = Read-Host "Quantos dias de historico deseja gerar? [Padrao: 7]"
        if ([string]::IsNullOrWhiteSpace($Days)) { $Days = 7 }
    }
    
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Green
    Write-Host "INICIANDO POPULACAO DOS DADOS SELECIONADOS..." -ForegroundColor Green
    Write-Host "================================================================" -ForegroundColor Green
    Write-Host ""
    
} else {
    # Modo automático (-All)
    Write-Log "Modo automatico: populando TODOS os dados..."
    $populateStocks = $true
    $populateFunds = $true
    $populateFixedIncome = $true
    $populateUsers = $true
    $populateChatbot = $true
    $generateCandles = $false
}

# Sempre inicializa o banco
# Gerar velas históricas se solicitado
if ($generateCandles -or $RunCandles) {
    Write-Log "Gerando velas históricas em $Days dias (isso pode demorar)..."
    $ok = Run-Script -ScriptPath '.\scripts\generate_historical_candles.py' -Arguments "--days $Days"
    if (-not $ok) {
        Write-Log "AVISO: Falha ao gerar velas históricas" "WARN"
    }
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Green
Write-Host "POPULACAO CONCLUIDA COM SUCESSO!" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""

# Mostrar resumo do que foi populado
Write-Host "RESUMO:" -ForegroundColor Cyan
if ($populateStocks) { Write-Host "  [OK] Acoes populadas" -ForegroundColor Green }
if ($populateFunds) { Write-Host "  [OK] Fundos imobiliarios populados" -ForegroundColor Green }
if ($populateFixedIncome) { Write-Host "  [OK] Renda fixa populada" -ForegroundColor Green }
if ($populateUsers) { Write-Host "  [OK] Usuarios populados" -ForegroundColor Green }
if ($populateChatbot) { Write-Host "  [OK] Chatbot populado" -ForegroundColor Green }
if ($generateCandles -or $RunCandles) { Write-Host "  [OK] Velas historicas geradas" -ForegroundColor Green }

Write-Host ""
Write-Host "Verifique os arquivos em demo/ para ver os dados criados." -ForegroundColor Yellow
Write-Host ""

exit 0
if ($populateFunds) {
    $jobsToRun += @{ script = '.\scripts\generate_funds.py'; args = '' }
}

if ($populateFixedIncome) {
    $jobsToRun += @{ script = '.\scripts\add_fixed_income_assets.py'; args = '' }
}

if ($populateUsers) {
    $jobsToRun += @{ script = '.\scripts\generate_demo_users.py'; args = '' }
    $jobsToRun += @{ script = '.\scripts\generate_varied_users.py'; args = '' }
}

if ($populateChatbot) {
    $jobsToRun += @{ script = '.\scripts\populate_chatbot_from_file.py'; args = '--update' }
}

# Executar jobs selecionados
foreach ($job in $jobsToRun) {
    $ok = Run-Script -ScriptPath $job.script -Arguments $job.args
    if (-not $ok) {
        Write-Log "AVISO: Falha em $($job.script) - continuando..." "WARN"
    }
}   @{ script = '.\scripts\generate_varied_users.py'; args = '' }
)

# Adiciona chatbot por padrão, mas permite desabilitar com -ExcludeChatbot
if (-not $ExcludeChatbot) {
    $jobs += @{ script = '.\scripts\populate_chatbot_from_file.py'; args = '--update' }
}

# Roda em sequência
foreach ($job in $jobs) {
    $ok = Run-Script -ScriptPath $job.script -Arguments $job.args
    if (-not $ok -and -not $ContinueOnError) {
        Write-Log "Abortando sequência devido a erro em $($job.script)" "ERROR"
        exit 1
    }
}

# Gerar velas históricas somente se solicitado
if ($RunCandles) {
    Write-Log "Gerando velas históricas em $Days dias (isso pode demorar)..."
    $ok = Run-Script -ScriptPath '.\scripts\generate_historical_candles.py' -Arguments "--days $Days"
    if (-not $ok -and -not $ContinueOnError) {
        Write-Log "Abortando após erro em geração de velas" "ERROR"
        exit 1
    }
}

Write-Log "Todos os scripts executados (ou pulados) conforme parâmetro." "INFO"
Write-Log "Concluído."

exit 0
