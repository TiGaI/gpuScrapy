# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter
from pathlib import Path
import os
import csv

class GpubenchmarkPipeline(object):
	def __init__(self):
	   print("*"*50 + 10*"\n" + str(os.getcwd()) + 10*"\n" + 50*"*")
	   self.filename = 'GPUBenchmark.csv'
	# open the csv and begin to use CsvItemExporter object and start exporting
	def open_spider(self, spider):
		if not os.path.exists(Path("data")):
			os.makedirs(Path("data"))
		self.csvfile = open(Path("data",self.filename), mode='w+b')
		self.exporter = CsvItemExporter(self.csvfile)
		self.exporter.start_exporting()
	# finish exporting then close csv
	def close_spider(self, spider):
		self.exporter.finish_exporting()
		self.csvfile.close()
		with open(Path("data",self.filename), 'r') as f:
			reader = csv.reader(f)
			original_list = list(reader)
			cleaned_list = list(filter(None,original_list))

		with open(Path("data", self.filename), 'w', newline='') as output_file:
			wr = csv.writer(output_file, dialect='excel')
			for data in cleaned_list:
				wr.writerow(data)
	# handles each item object that was yielded in the scraper
	def process_item(self, item, spider):
	   self.exporter.export_item(item)
	   return item
