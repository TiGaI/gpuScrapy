from scrapy import Spider
from gpuBenchmark.items import GpubenchmarkItem
import re
from scrapy.http.request import Request
from scrapy_splash import SplashRequest
import pandas as pd

class gpubenchmark(Spider):
	name = 'gpubenchmark'
	allowed_urls = ['https://www.videocardbenchmark.net']
	start_urls = ['https://www.videocardbenchmark.net']
	
	def parse(self, response):
		yield SplashRequest('https://www.videocardbenchmark.net/high_end_gpus.html', self.highendvideocards, endpoint='render.html', magic_response=True, meta={'handle_httpstatus_all': True}, args={'wait':0.5, 'http_method': 'GET'})
		

	def highendvideocards(self, response):
		data = GpubenchmarkItem()
		rows = response.xpath('//tr')
		# print("this is the rows", rows[5:])
		# print(rows[5])
		# print(rows[5].xpath('td[1]/a/text()').extract())
		# print(rows[5].xpath('td[2]/div/text()').extract())
		for row in rows[5:]:
			try:
				name = row.xpath('td[1]/a/text()').extract()[0]
				number = row.xpath('td[2]/div/text()').extract()[0]
			except:
				break

			data['brand'], data['benchmark'] = name, number
			yield data


		yield SplashRequest('https://www.videocardbenchmark.net/mid_range_gpus.html', self.midtohighvideocards, endpoint='render.html', magic_response=True, meta={'handle_httpstatus_all': True}, args={'wait':0.5, 'http_method': 'GET'})


	def midtohighvideocards(self, response):
		rows = response.xpath('//tr')
		data = GpubenchmarkItem()
	
		for row in rows[5:]:
			try:
				name = row.xpath('td[1]/a/text()').extract()[0]
				number = row.xpath('td[2]/div/text()').extract()[0]
			except:
				break
			data['brand'], data['benchmark'] = name, number
			yield data

		yield SplashRequest('https://www.videocardbenchmark.net/midlow_range_gpus.html', self.lowtomidvideocards, endpoint='render.html', magic_response=True, meta={'handle_httpstatus_all': True}, args={'wait':0.5, 'http_method': 'GET'})
	
	def lowtomidvideocards(self, response):
		
		rows = response.xpath('//tr')
		data = GpubenchmarkItem()

		for row in rows[5:]:
			try:
				name = row.xpath('td[1]/a/text()').extract()[0]
				number = row.xpath('td[2]/div/text()').extract()[0]
			except:
				break
			data['brand'], data['benchmark'] = name, number
			yield data

		yield SplashRequest('https://www.videocardbenchmark.net/low_end_gpus.html', self.lowvideocards, endpoint='render.html', magic_response=True, meta={'handle_httpstatus_all': True}, args={'wait':0.5, 'http_method': 'GET'})

	def lowvideocards(self, response):
		rows = response.xpath('//tr')
		data = GpubenchmarkItem()
	
		for row in rows[5:]:
			try:
				name = row.xpath('td[1]/a/text()').extract()[0]
				number = row.xpath('td[2]/div/text()').extract()[0]
			except:
				break
			data['brand'], data['benchmark'] = name, number
			yield data