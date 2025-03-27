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

