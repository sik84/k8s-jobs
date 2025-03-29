FROM python:3.9-slim

# Installiere pandas
RUN pip install pandas

# Kopiere das Skript in den Container
COPY transform_csv.py /app/transform_csv.py

# Setze das Arbeitsverzeichnis
WORKDIR /app

# Führe das Skript aus
CMD ["python", "transform_csv.py"]
