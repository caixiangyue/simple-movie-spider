import scrapy
import js2xml
import pymongo
class QuotesSpider(scrapy.Spider):
    name = "movie"

    def start_requests(self):
        urls = []
        for i in range(1,50):
            urls.append('http://www.haiduomi.com/type/1-'+str(i)+'.html')
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        hrefs = response.css('li.fed-list-item a.fed-list-pic::attr(href)').extract()
        for href in hrefs:
            yield scrapy.Request(response.urljoin(href),callback=self.parse_href_1)

    def parse_href_1(self,response):
        href = response.css('a.fed-btn::attr(href)').extract_first()
        yield scrapy.Request(response.urljoin(href),callback=self.parse_href_2)

    def parse_href_2(self,response):
        js_code = response.xpath("//script[contains(.,'iframe.src')]/text()").extract_first()
        parsed_js = js2xml.parse(js_code)
        js_selector = scrapy.Selector(root=parsed_js)
        movie_link = js_selector.xpath("//program/assign[@operator='=']/right/string/text()").extract_first()
        title = response.css('h3.fed-elip a::text').extract_first()
        role = response.css('ul.fed-rows li.fed-elip a::text').extract()
        extra = response.css('li.fed-col-xs6 a::text').extract()
        
        movie = {
            'title':title,
            'link':movie_link,
            'main_role':role[:-2],
            'direct':role[-1],
            'type':extra[0],
            'area':extra[1],
            'date':extra[2]
        }
        client = pymongo.MongoClient(host='localhost',port=27017)
        db = client.movie
        movies = db.movies
        result = movies.insert_one(movie)
        print(result)
