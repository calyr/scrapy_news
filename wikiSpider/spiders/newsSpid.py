import scrapy
import hashlib
import re

from wikiSpider.items import NewsItem
class NewsSpidSpider(scrapy.Spider):
    name = "newsSpid"
    allowed_domains = ["thenextweb.com"]
    start_urls = ["https://thenextweb.com/latest"]
    max_page_load = 6
    # Configurar un User-Agent para evitar bloqueos
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    def parse(self, response):
        news = response.css("article")
        for new in news:
            news_url = new.css("a::attr(href)").get()
            yield response.follow(news_url, callback=self.parse_specific)
        
        next_page_url = response.css('a[rel="next"]::attr(href)').get()
        if next_page_url:
            match = re.search(r"/page/(\d+)", next_page_url)
            if match:
                next_page_number = int(match.group(1))  # Extrae el número de la URL (Ej: "/page/3" -> 3)
            else:
                next_page_number = 2 
            
            if next_page_number <= self.max_page_load:
                yield response.follow(next_page_url, callback=self.parse)
    def parse_specific(self, response):

        header_css_content = response.css(".c-header__text")
        body_css_contet = response.css(".c-article__main *::text").getall()
        tag = header_css_content.css(".c-article-leadtag::text").get()
        header = header_css_content.css(".c-header__heading::text").get().strip()
        intro = header_css_content.css(".c-header__intro::text").get().strip()
        date = header_css_content.css("time::attr(datetime)").get()
        
        body = " ".join(body_css_contet).strip()

        # Generar un ID único basado en el header y la fecha
        unique_string = f"{header}-{date}"
        unique_id = hashlib.sha256(unique_string.encode()).hexdigest()
        newsItem = NewsItem()
    
        newsItem['id'] = unique_id
        newsItem['tag'] = tag
        newsItem['header'] = header
        newsItem['intro'] = intro
        newsItem['date'] = date
        newsItem['body'] = body

        yield newsItem
    

