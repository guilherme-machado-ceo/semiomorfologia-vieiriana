# run_tests.ps1
# Executa suite de testes com cobertura

& .\venv\Scripts\Activate.ps1
python -m pytest tests/ -v --cov=src/semiomorfologia --cov-report=html --cov-report=term
