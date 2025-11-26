<#
Populate All - PowerShell Script

Descrição:
  Executa os scripts de inicialização e populamento do banco de dados
  a partir da pasta `Backend` em ordem segura.

Parâmetros:
  -InstallDeps: instala dependências do arquivo `Backend/requirements.txt` antes de executar
  -RunCandles:   executa a geração de velas históricas (padrão: $false)
  -Days:         número de dias para gerar velas (padrão: 7)
  -ContinueOnError: continua para o próximo script em caso de erro (padrão: $false)

Uso exemplo:
  .\populate_all.ps1 -InstallDeps -RunCandles -Days 7
#>
param (
    [switch]$InstallDeps = $false,
    [switch]$RunCandles = $false,
    [int]$Days = 7,
    [switch]$ExcludeChatbot = $false,
    [switch]$IncludeInteractiveChatbot = $false,
    [switch]$ContinueOnError = $false
)

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$ts] [$Level] $Message"
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

# Forçar UTF-8 no Python no Windows (para evitar erros com emojis e símbolos)
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

function Run-Script {
    param(
        [string]$ScriptPath,
        [string]$Arguments = ""
    )

    $fullCmd = "& $pythonCmd -X utf8 `"$ScriptPath`" $Arguments"
    Write-Log "Executando: $fullCmd"

    try {
        # Executa no contexto atual. Poderíamos usar Start-Process se preferir separar o processo.
        iex $fullCmd
        if (!$LASTEXITCODE -or $LASTEXITCODE -eq 0) {
            Write-Log "Sucesso: $ScriptPath"
            return $true
        } else {
            Write-Log "Falha (exit code $LASTEXITCODE): $ScriptPath" "ERROR"
            if (-not $ContinueOnError) { exit $LASTEXITCODE }
            return $false
        }
    } catch {
        Write-Log "Exceção ao executar $ScriptPath - $_" "ERROR"
        if (-not $ContinueOnError) { exit 1 }
        return $false
    }
}

# Passo opcional: instalar dependências
if ($InstallDeps) {
    Write-Log "Instalando dependências do Backend/requirements.txt..."
    $reqFile = Join-Path $BackendDir 'requirements.txt'
    if (Test-Path $reqFile) {
        iex "& $pythonCmd -X utf8 -m pip install -r `"$reqFile`""
        if (!$LASTEXITCODE -or $LASTEXITCODE -eq 0) {
            Write-Log "Dependências instaladas com sucesso."
        } else {
            Write-Log "Falha ao instalar dependências com exit code $LASTEXITCODE" "ERROR"
            if (-not $ContinueOnError) { exit $LASTEXITCODE }
        }
    } else {
        Write-Log "Arquivo de requirements não encontrado: $reqFile" "WARN"
    }
}

# Ordem recomendada de execução
$jobs = @(
    @{ script = '.\scripts\init_db.py'; args = '' },
    @{ script = '.\scripts\generate_stocks.py'; args = '' },
    @{ script = '.\scripts\generate_funds.py'; args = '' },
    @{ script = '.\scripts\add_fixed_income_assets.py'; args = '' },
    @{ script = '.\scripts\generate_demo_users.py'; args = '' },
    @{ script = '.\scripts\generate_varied_users.py'; args = '' }
)

# Adiciona chatbot por padrão, mas permite desabilitar com -ExcludeChatbot
if (-not $ExcludeChatbot) {
    $jobs += @{ script = '.\scripts\update_chatbot_db.py'; args = '' }
    $jobs += @{ script = '.\scripts\populate_chatbot_full.py'; args = '' }
    # Opcional: executar também a versão interativa (populate_chatbot.py)
    if ($IncludeInteractiveChatbot) { $jobs += @{ script = '.\scripts\populate_chatbot.py'; args = '' } }
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
