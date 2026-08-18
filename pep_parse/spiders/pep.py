import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        pep_list = response.css(
            'a[href^="pep-"]::attr(href)'
        ).getall()
        for pep_link in pep_list:
            pep_url = response.urljoin(pep_link + '/')
            yield response.follow(pep_url, callback=self.parse_pep)

    def parse_pep(self, response):
        data = {
            'number': response.css(
                'h1.page-title::text'
            ).get().strip().split()[1],
            'name': response.css(
                'h1.page-title::text'
            ).get().strip(),
            'status': response.css(
                'dt:contains("Status") + dd abbr::text'
            ).get().strip(),
        }
        yield PepParseItem(data)
