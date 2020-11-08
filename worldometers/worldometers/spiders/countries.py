# -*- coding: utf-8 -*-
import scrapy
import logging


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['http://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        countries = response.xpath("//td/a")
        for country in countries:
            country_name = country.xpath(".//text()").get()
            country_link = country.xpath(".//@href").get()

            yield response.follow(url=country_link, callback=self.parse_country, meta={'country_name': country_name})

    def parse_country(self, response):
        rows = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[position()=1]/tbody/tr")
        for row in rows:
            country_name = response.request.meta['country_name']
            year = row.xpath(".//td[position()=1]/text()").get()
            population = row.xpath(".//td[position()=2]/strong/text()").get()

            yield {
                'country_name': country_name,
                'year': year,
                'population': population
            }