FROM python:3.11-slim

# Instala dependencias del sistema necesarias para Scrapy
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libxslt1-dev \
    libxml2-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Copiar el script start.sh y darle permisos de ejecución
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Establecer el comando por defecto para ejecutar el script
CMD ["/start.sh"]

# RUN chmod +x /usr/local/bin/scrapy

# CMD ["scrapy", "runspider", "wikiSpider/spiders/newsmergeSpid.py"]

