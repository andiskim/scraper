from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose

from amazon.items import AmazonItem

class MySpider(BaseSpider):
	name = "amazon"
	allowed_domains = ["http://www.amazon.com"]
	start_urls = ["http://www.amazon.com/s?ie=UTF8&page=1&rh=i%3Aaps%2Ck%3Asalt%20lamp"]

	view = '//a[contains(@class, "a-link-normal s-access-detail-page  a-text-normal")]'
	item_fields = {
		'title': './/@title',
		'link': './/@href'
	}
	def parse(self, response):
		selector = response.selector.xpath(view)

		#iterate over titles
		for page in selector.select(self.view):
			loader = ItemLoader(AmazonItem(), page)

			#define processors
			loader.default_input_processor = MapCompose(unicode.strip)
			loader.default_output_processor = Join()

			#iterate over fields and add xpaths to the loader
			for field, xpath in self.iem_fields.iteritems():
				loader.add_xpath(field, xpath)
			return loader.load_item()