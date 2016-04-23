#!/usr/bin/env python
import scrapy
from scrapy.mail import MailSender
from scrapy.utils.project import get_project_settings

class QiushiSpider(scrapy.Spider):
	name = 'qiushi'
	allowed_domains = ['qiushibaike.com']
	start_urls = ["http://www.qiushibaike.com/text/"]
	web_data_list = []

	def parse(self,response):
		for sel in response.xpath('//div[contains(@class,"article block untagged mb15")]'):

			author = sel.xpath('div[contains(@class,"author clearfix")]/a/h2/text()').extract()[0].encode('utf-8')
			content = sel.xpath('div[contains(@class,"content")]/text()').extract()[0].encode('utf-8')
			stats_vote = sel.xpath('div[contains(@class,"stats")]/span[contains(@class,"stats-vote")]/i/text()').extract()[0].encode('utf-8')
			item = {"author":author,"content":content.strip(),"stats_vote":stats_vote}
			self.web_data_list.append(item)
			#print author,content,stats_vote
	def closed(self,reason):
		str = ''
		for index,item in enumerate(self.web_data_list):
			tmp = 'index:%d, author:%s, vote:%s\n[%s]\n\n' % (index,item['author'],item['stats_vote'],item['content'])
			str = str + tmp
		print str
		settings = get_project_settings()
		mailer = MailSender.from_settings(settings)
		mailer.send(to='jeremy.h@foxmail.com',subject='qiushibaike',body=str,mimetype='text/plain;charset="utf-8"')
