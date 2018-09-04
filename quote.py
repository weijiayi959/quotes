# -*- coding: utf-8 -*-
import scrapy

import quotetutorial.items


class QuoteSpider(scrapy.Spider):
    name = 'quote'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        item = quotetutorial.items.QuoteItem()
        quotes = response.xpath('//div[@class="quote"]')
        for quote in quotes:
            text = quote.xpath('./span[contains(@class,"text") and @itemprop="text"]/text()').extract_first().replace('"','')
            author = quote.xpath('.//small[contains(@class,"author") and @itemprop="author"]/text()').extract_first()
            tags = quote.xpath('.//a[@class="tag"]/text()').extract()
            item['text'] = text
            item['author'] = author
            item['tags'] = tags
            yield item

        next = response.xpath('//li[@class="next"]/a/@href').extract_first()
        url = response.urljoin(next)
        yield scrapy.Request(url=url, callback=self.parse)
