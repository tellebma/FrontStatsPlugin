FROM python:3.9-slim
WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

VOLUME /app/mmr_database.db
VOLUME /app/player_database.db

EXPOSE 5000

CMD ["python", "app.py"]