# Utilise une image Python légère
FROM python:3.11-slim

# Empêche Python de générer des fichiers .pyc et force logs non-bufferisés
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Définir le dossier de travail
WORKDIR /app

# Installer dépendances système (Postgres + Pillow)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Installer dépendances Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copier le projet
COPY . .

# On laisse la commande à entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
