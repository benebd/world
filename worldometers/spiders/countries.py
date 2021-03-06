from turtle import title
from unicodedata import name
import scrapy
import logging


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    country_name =''

    def parse(self, response):
         
        countries = response.xpath("//td/a")
        for country in countries:
            name = country.xpath(".//text()").get()
            self.country_name = name
            link = country.xpath(".//@href").get()

            yield response.follow(url=link,callback=self.parse_country)

    def parse_country(self,response):
        rows = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")

        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()

            yield{
                'name':self.country_name,
                'year':year,
                'population':population
            }


