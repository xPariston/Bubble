from fbcrawl.spiders import fbcrawl
from scrapy.crawler import CrawlerProcess
import scrapy


def scrapefb(time,mail,password,page,max):
    process = CrawlerProcess({ 'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    process.crawl('fb',date=time,email=mail,password = password,page=page,max=max)
    process.start()