# Étape 1 : Construire l'image pour le backend Flask
FROM python:3.9-slim

# Créer et définir le répertoire de travail
WORKDIR /app

# Copier les dépendances Python
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier les fichiers source du backend Flask
COPY . .

# Exposer le port 5000 pour Flask
EXPOSE 5000

# Démarrer l'application Flask
CMD ["python", "app.py"]