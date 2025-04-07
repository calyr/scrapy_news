import scrapy
import hashlib
import re
from wikiSpider.items import NewsItem
from wikiSpider.spiders.data_web import ALLOWED_DOMAINS, BASE_URLS, HEADERS
class NewsMergeSpidSpider(scrapy.Spider):
    name = "newsmergepider"
    allowed_domains = ALLOWED_DOMAINS 
    start_urls = []
    custom_settings = HEADERS

    def start_requests(self):
        """Generate initial requests with proper user agent header """
        for base in BASE_URLS:
            yield scrapy.Request(
                    url = base["URL"],
                    callback=self.parse,
                    headers=HEADERS,
                    meta={'max_page_load': base["MAX_PAGE_LOAD"]}
            )


    def parse(self, response):

        if response.status != 200:
            self.logger.warning(f"Failed to fetch {response.url}: {response.status}")
            return
        
        url_site = response.url
        max_page_load = response.meta.get('max_page_load', 1)  # Valor por defecto = 1

        if 'thenextweb' in url_site:
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
                
                if next_page_number <= max_page_load:
                    yield response.follow(next_page_url, callback=self.parse)
        else:
            news = response.css(".summary-list__item")
            for new in news:
                news_url = new.css("a::attr(href)").get()

                if news_url:
                    news_url = response.urljoin(news_url)
                    yield response.follow(news_url, callback=self.parse_specific)
                else:
                    self.logger.warning(f"Found a newsitem with no URL: {news_url}")
            
            next_page_url = response.css('a[data-section-title="Next Page"]::attr(href)').get()

            if next_page_url:
                page_number = next_page_url.split('=')[-1]
                if page_number.isdigit() and int(page_number) <= max_page_load:
                    next_page_url = response.urljoin(next_page_url)  # Obtener la URL completa
                    yield response.follow(next_page_url, callback=self.parse)
    
    def parse_specific(self, response):
        url_site = response.url
        if 'thenextweb' in url_site:

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
            newsItem['url'] = response.url
            yield newsItem
        else:
            header_css_content = response.css(".main-content")
            tag = header_css_content.css(".rubric__name::text").get(default='N/A')
            header = header_css_content.css(".kctZMs::text").get(default='No header').strip()
            intro = response.css(".dJrDEb::text").get(default='No intro').strip()
            date = header_css_content.css("time::attr(datetime)").get(default='No date')
            body_text = header_css_content.xpath("//div[@class='body__inner-container']//text()").getall()
            body = " ".join(body_text).strip()

            if header != 'No header' and date != 'No date':
                unique_string = f"{header}-{date}"
                unique_id = hashlib.sha256(unique_string.encode()).hexdigest()
                newsItem = NewsItem()
                newsItem['id'] = unique_id
                newsItem['tag'] = tag
                newsItem['header'] = header
                newsItem['intro'] = intro
                newsItem['date'] = date
                newsItem['body'] = body
                newsItem['url'] = response.url
                yield newsItem
    

