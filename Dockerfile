
FROM python:3.14.7-slim-trixie

ENV PYTHONDONTWRITEBYTECODE=1 \ PYTHONUNBUFFERED=1

# Création de l'utilisateur Django et du dossier de l'application
RUN useradd --create-home django \
    && mkdir /app \
    && chown django:django /app

WORKDIR /app

# Installation des dépendances
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copie du projet
COPY --chown=django:django . .

# Utilisation d'un utilisateur non-root
USER django

EXPOSE 8000
ENTRYPOINT ["sh", "docker-entrypoint.sh"]
# Lancement de Django avec Gunicorn
CMD ["gunicorn", "brickmarket.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--access-logfile", "-", "--error-logfile", "-"]

