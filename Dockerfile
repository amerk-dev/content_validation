FROM python:3.12

WORKDIR /app

COPY ./app /app

# Обновляем apt-get и устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    cmake \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Обновляем pip
RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r /app/requirements.txt
RUN pip install psycopg2

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]