# scheduler wired and news merged
## Steps

## create a image scraper
```sh
docker build -t scraper:latest .
```
## up the container using docker compose
```sh
docker compose up
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
## Table of Contents

- [Authors] Authors

## Requirements

## Installations

```sh
pip install -r requirements.txt
```

## Architecture
The project has a structre recommended to scrapy


## Configuration
The data is saved as json 
```json
[{"id": "8734eb9b74a3bd9b012cd787b275fd5be698c56f21bab4392a519135239b4847", "tag": "Ecosystems", "header": "TNW Conference unveils plan to unleash the next big things in tech", "intro": "Our new event agenda is designed to elevate Europe's tech ecosystem", "date": "March 14, 2025 - 10:13 am"},...]
```

## Roadmap

- [x] Feature craper 
- [x] Feature merge project
- [ ] Final Project 

## Versioning
This project uses [SemVer](https://semver.org) for versioning. For the versiones available, see the [tags on this repository](https://github.com/calyr)

## Authors

*Initial work* - [Roberto Carlos Callisaya](https://github.com/calyr)