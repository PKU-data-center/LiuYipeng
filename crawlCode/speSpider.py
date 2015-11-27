from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from lyptest.items import specialItem, movieItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

count_special = 0
count_movie = 0

class specialSpider(CrawlSpider):
        name = 'specialSpider'
        allowed_domains = ['163.com']
        start_urls = ['http://open.163.com/ocw', 'http://open.163.com/cuvocw','http://open.163.com/appreciation', 'http://open.163.com/ted']
        rules = [Rule(SgmlLinkExtractor(allow=['special/']), 'parse_special'),
		 Rule(SgmlLinkExtractor(allow=['movie/']), 'parse_movie')]
        def parse_special(self, response):
		global count_special
                x = Selector(response)
                special = specialItem()
		special['type'] = 'special'
                special['url'] =response.url
		count_special = count_special + 1
		special['count'] = count_special
                div = x.xpath("//div[@class ='m-cdes']")
                nameList = div.xpath("//h2/text()").extract()
		special['name'] = nameList[0]
		introduceList =  div.xpath("//p/text()").extract()
                special['introduce'] = introduceList[0:3]
		div2 = x.xpath("//table[@class ='m-clist']")
		listurl = div2.xpath(".//a/@href").extract()
		index = 0
		listUrl = []
		for i in listurl:
			index = index + 1
			if index % 2 == 1:
				listUrl.append(i)
		special['listUrl'] = listUrl
		listname = div2.xpath(".//a/text()").extract()
		index = 0
		listName = []
		for i in listname:
			index = index + 1
			if index % 2 == 1:
				listName.append(i)
		special['listName'] = listName
		return special

	def parse_movie(self, response):
		global count_movie
		x = Selector(response)
                movie = movieItem()
		movie['type'] = 'movie'
		movie['url'] = response.url
		count_movie = count_movie + 1
		movie['count'] = count_movie
		#div1 = x.xpath("//div[@class = 'f-fl nav']")
		#nameList = div1.xpath("//a/text()").extract()
		#movie['name'] = nameList[1]
		div = x.xpath("//div[@class = 'g-sd']")
		nameList = div.xpath(".//h3/text()").extract()
		movie['name'] = nameList
		div2 = div.xpath("//div[@class = 'u-ptl-c f-c6']")
		introduceList =  div2.xpath(".//p/text()").extract()
		movie['introduce'] = introduceList
		return movie
