import scrapy
class BookSpidSpider(scrapy.Spider):
    name = "bookSpid"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ['https://books.toscrape.com']

    def parse(self, response):
        books = response.css("article.product_pod")
        for book in books:
            # tmp_url = book.css("h3 a").attrib["href"]
            relative_url = book.css("h3 a::attr(href)").get()
           
            yield response.follow(relative_url, callback=self.parse_specific)

        next_page = response.css('li.next a::attr(href)').get()
        next_page = response.urljoin(next_page)
        yield response.follow(next_page, callback=self.parse)

    def parse_specific(self, response):
        table_rows = response.css("table tr")
        yield {
            'title': response.css("div.product_main h1::text").get(),
            'rating' : response.css("div.product_main p.star-rating").attrib["class"],
            'available' : table_rows[5].css("td::text").get(),
            'description' : response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
            'category' : response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
            'product_type' : table_rows[1].css("td::text").get()
        }