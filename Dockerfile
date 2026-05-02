FROM public.ecr.aws/docker/library/python:3.12-slim-bookworm

# Reszta kodu pozostaje bez zmian
COPY --from=public.ecr.aws/astral-sh/uv:latest /uv /uvx /bin/

# Ustawiamy katalog roboczy
WORKDIR /app

# Kopiujemy pliki definiujące zależności
COPY pyproject.toml uv.lock ./

# Instalujemy zależności (uv sync automatycznie utworzy venv wewnątrz kontenera)
RUN uv sync --frozen

# Kopiujemy resztę plików projektu (w tym bridge.dxf)
COPY . .

# Uruchamiamy skrypt
CMD ["uv", "run", "main.py"]