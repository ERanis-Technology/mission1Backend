# Utilise une image Python légère
FROM python:3.11-slim

# Empêche Python de générer des fichiers .pyc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Définir le dossier de travail
WORKDIR /app

# Installer dépendances système
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Installer dépendances Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copier le projet
COPY . .

# Collecte des fichiers statiques
RUN python manage.py collectstatic --noinput

# Commande de démarrage avec Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "plateformeynno.wsgi:application"]
