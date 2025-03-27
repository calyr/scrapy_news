import scrapy
import hashlib
import re

from wikiSpider.items import NewsItem

class WiredSpidSpider(scrapy.Spider):
    name = "wiredSpid"
    allowed_domains = ["www.wired.com"]
    start_urls = ["https://www.wired.com/category/politics"]
    max_page_load = 2

    def parse(self, response):
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
            if page_number.isdigit() and int(page_number) <= self.max_page_load:
                next_page_url = response.urljoin(next_page_url)  # Obtener la URL completa
                yield response.follow(next_page_url, callback=self.parse)

    def parse_specific(self, response):

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
            newsItem['url'] = "url"

            yield newsItem

