import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import CzuniItem
from itemloaders.processors import TakeFirst
import datetime
pattern = r'(\xa0)?'
base = 'https://www.unicreditbank.cz/cs/o-bance/tiskove-centrum/tiskove-zpravy.html#2021'

class CzuniSpider(scrapy.Spider):
	# now = datetime.datetime.now()
	# year = now.year
	name = 'czuni'
	start_urls = ['https://www.unicreditbank.cz/cs/o-bance/tiskove-centrum/tiskove-zpravy.html#2021']

	def parse(self, response):
		yield response.follow(response.url, self.parse_post)

		# if self.year >= 2015:
		# 	self.year -= 1
		# 	yield response.follow(base.format(self.year), self.parse)


	def parse_post(self, response):
		articles = response.xpath('//div[@class="accordion-header js-expandmore"]')
		for index in range(len(articles)):
			item = ItemLoader(item=CzuniItem(), response=response)
			item.default_output_processor = TakeFirst()

			date = response.xpath(f'(//div[@class="text"]/span[@class="font-title-4"])[{index+1}]/text()').get().split(' - ')[0]
			# date = re.findall(r'\d+\.\d+\.\d+',date)
			try:
				title = response.xpath(f'(//div[@class="text"]/span[@class="font-title-4"])[{index+1}]//text()').get().split(' - ')[1]
			except IndexError:
				title = response.xpath(f'(//div[@class="text"]/span[@class="font-title-4"])[{index + 1}]/text()').get()
			content = response.xpath(f'(//div[@class="accordion-body js-to_expand "])[{index+1}]//text()').getall()
			content = [p.strip() for p in content if p.strip()]
			content = re.sub(pattern, "",' '.join(content))

			item.add_value('title', title)
			item.add_value('link', response.url)
			item.add_value('content', content)
			item.add_value('date', date)

			yield item.load_item()
