# Proyecto Scraping and Data Lake

## Table of Contents
- [Requirements](#requirements)
- [Configuration](#configuration)
- [Installations](#installations)
- [FAQ](#faq)
- [Maintainers](#maintainer)
- [Authors](#authors)

## Requirements
1. Python3
2. Docker
3. Docker Desktop for( Window/Mac Os)


## Configuration

1. Debes crear el archivo .env
2. Este archivo tendra las variables de conexion a la base de datos de posgres
3. Al estar utilizando docker compose, estas variables las puedes obtener del archivo docker-compose.yml 
-- .env (file)
```sh
DB_HOST=postgres
DB_USER=root
DB_PASSWORD=root
DB_DATABASE=scraper
```

-- docker-compose.yml (file)
```sh
services:
  postgres:
    image: postgres
    restart: always
    # set shared memory limit when using docker-compose
    shm_size: 128mb
    environment:
      POSTGRES_USER: root
      POSTGRES_PASSWORD: root
      POSTGRES_DB: scraper
    volumes:
      - ./data:/var/lib/postgresql/data
    networks:
      - can-network

   and editors
```


## Installations

Instalación de librerias necesarias en el proyecto
```sh
pip install -r requirements.txt
```

## Architecture
El proyecto utiliza una patron de arquitectura recomendado por scrapy para la ETL desde el scraping hasta la creación del datalake.


## Configuración de respuesta.

The data is saved as json 
```json
[{"id": "8734eb9b74a3bd9b012cd787b275fd5be698c56f21bab4392a519135239b4847", "tag": "Ecosystems", "header": "TNW Conference unveils plan to unleash the next big things in tech", "intro": "Our new event agenda is designed to elevate Europe's tech ecosystem", "date": "March 14, 2025 - 10:13 am"},...]
```

## Roadmap

- [x] Feature craper 
- [x] Feature merge project
- [x] Final Project 

## Versioning
This project uses [SemVer](https://semver.org) for versioning. For the versiones available, see the [tags on this repository](https://github.com/calyr/scrapy_news)

## Authors

*Initial work* - [Roberto Carlos Callisaya](https://github.com/calyr)




# scheduler wired and news merged
## Steps

## create a image scraper
```sh
docker build -t scraper:latest .
```
## up the container using docker compose
```sh
docker compose up --build
```

# scheduler wired and news
## 2 times a day

```sh
python scrapy_scheduler_merge.py
```


# scheduler wired and news
## Steps
In your terminal execute the next command
```sh
python scrapy_scheduler_wired.py
python scrapy_scheduler_news.py
```
## Individual scrapy thenextweb.com
```sh
scrapy runspider spiders/newsSpid.py -O thenextweb.json
```

## Individual scrapy wired.com
```sh
scrapy runspider spiders/wiredSpid.py -O wired.json
```

# scheduler wired and news
## 2 times a day

```sh
python scrapy_scheduler_news.py
```

```sh
python scrapy_scheduler_wired.py
```

# If you prefer test in your computer: please use venv
## Steps

```sh
python3 -m venv venv
```


```sh
source ../venv/bin/activate
```


```sh
pip install -r requirements.txt
```
