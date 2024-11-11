# Используем официальный образ Python
FROM python:3.10

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем все файлы проекта в контейнер
COPY . /app

# Устанавливаем все зависимости проекта
# (здесь используется файл requirements.txt для установки пакетов)
RUN pip install --no-cache-dir -r requirements.txt

# Определяем команду для запуска приложения
CMD ["python", "main.py"]
