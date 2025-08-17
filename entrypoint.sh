#!/bin/sh

# Arrêter le script si une commande échoue
set -e

echo "📌 Attente de la base de données PostgreSQL..."
until nc -z db 5432; do
  echo "⏳ Postgres n'est pas encore disponible - attente..."
  sleep 2
done

echo "✅ Base de données prête."

# Appliquer les migrations
echo "📌 Application des migrations..."
python manage.py makemigrations profils authentification
python manage.py migrate --noinput
./populate.sh
# Collecter les fichiers statiques
echo "📌 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Lancer Gunicorn
echo "🚀 Démarrage de Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 --workers=3 plateformeynno.wsgi:application
