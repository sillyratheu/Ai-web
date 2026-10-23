FROM python:3.10-slim

# System level-e Firefox-esr install kora hocche
RUN apt-get update && apt-get install -y \
    firefox-esr \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
