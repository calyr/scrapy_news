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