# Semiomorfologia Vieiriana — API REST (modo leve)
# Imagem para Cloud Run (ou qualquer runtime de contêiner).
# Modo leve: sem PyTorch/sentence-transformers e sem qiskit,
# para caber em 512 MB de memória com cold start curto.

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Dependências travadas com hashes (requirements-docker.lock, gerado de
# requirements-docker.in com: uv pip compile requirements-docker.in
# --python-version 3.12 --generate-hashes -o requirements-docker.lock).
# requests e sparqlwrapper ficam fora: só as rotas experimentais os usam.
COPY requirements-docker.lock ./
RUN pip install --require-hashes -r requirements-docker.lock

# Código do framework
COPY setup.py pyproject.toml README.md LICENSE ./
COPY src ./src
RUN pip install --no-deps .

# Usuário sem privilégios
RUN useradd --create-home --uid 10001 appuser
USER appuser

# Cloud Run injeta a porta em $PORT (padrão 8080)
ENV PORT=8080
EXPOSE 8080

CMD ["sh", "-c", "uvicorn semiomorfologia.api.app:app --host 0.0.0.0 --port ${PORT}"]
