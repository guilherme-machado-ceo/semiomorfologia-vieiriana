# setup_windows.ps1
# Script de instalação automatizado para Windows 11 + PowerShell
# Requisitos: Python 3.10+ instalado e disponível no PATH

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Semiomorfologia Vieiriana - Setup" -ForegroundColor Cyan
Write-Host "  Windows 11 | PowerShell | 8GB RAM" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Verificar Python
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Error "Python não encontrado. Instale Python 3.10+ e adicione ao PATH."
    exit 1
}

$version = & python --version 2>&1
Write-Host "✓ Python detectado: $version" -ForegroundColor Green

# Criar ambiente virtual
if (Test-Path "venv") {
    Write-Host "⚠ Ambiente virtual já existe. Removendo..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force "venv"
}

Write-Host "→ Criando ambiente virtual..." -ForegroundColor Blue
python -m venv venv

# Ativar
Write-Host "→ Ativando ambiente virtual..." -ForegroundColor Blue
& .\venv\Scripts\Activate.ps1

# Instalar dependências
Write-Host "→ Instalando dependências (numpy + matplotlib + pytest)..." -ForegroundColor Blue
pip install --upgrade pip
pip install -r requirements.txt

# Verificar instalação
Write-Host "→ Verificando instalação..." -ForegroundColor Blue
python -c "from semiomorfologia.core.ontologia import Morfema; print('OK')"

# Executar testes
Write-Host "→ Executando testes..." -ForegroundColor Blue
python -m pytest tests/ -v --tb=short

# Executar demo simples
Write-Host "→ Executando demonstração..." -ForegroundColor Blue
python examples/demo_simples.py

Write-Host "" 
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Setup concluído com sucesso!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Comandos úteis:" -ForegroundColor Cyan
Write-Host "  .\venv\Scripts\Activate.ps1    # Ativar ambiente"
Write-Host "  python examples/demo_completo.py  # Demo completa"
Write-Host "  python -m pytest tests/ -v    # Executar testes"
Write-Host ""
