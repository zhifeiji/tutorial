#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
import MySQLdb

from scrapy.mail import MailSender
from scrapy.utils.project import get_project_settings

class QiushiSpider(scrapy.Spider):
    name = 'qiushi'
    allowed_domains = ['qiushibaike.com']
    start_urls = ["http://www.qiushibaike.com/text/","http://www.qiushibaike.com/text/page/2/","http://www.qiushibaike.com/text/page/3/"]
    web_data_list = []

    def parse(self,response):
        for sel in response.xpath('//div[contains(@class,"article block untagged mb15")]'):
            author = sel.xpath('div[contains(@class,"author clearfix")]/a/h2/text()').extract_first(default=u'匿名用户').encode('utf-8')
            content = sel.xpath('div[contains(@class,"content")]/text()').extract_first().encode('utf-8')
            contentid = sel.xpath('@id').re(r'qiushi_tag_(.*)')[0].encode('utf-8')
            stats_vote = sel.xpath('div[contains(@class,"stats")]/span[contains(@class,"stats-vote")]/i/text()').extract_first().encode('utf-8')
            item = {"author":author,"content":content.strip(),"stats_vote":stats_vote,"contentid":contentid}
            self.web_data_list.append(item)
			#print ctime
			#print author,content,stats_vote
    def closed(self,reason):
        str = ''
        conn = MySQLdb.connect(host='127.0.0.1',user='spider_user',passwd='spider_user!@#',port=3306,db='db_spider',charset='utf8')
        cur = conn.cursor()

        for index,item in enumerate(self.web_data_list):
    	    tmp = 'index:%d, author:%s, vote:%s,contentid:%s\n[%s]\n\n' % (index,item['author'],item['stats_vote'],item['contentid'],item['content'])
            str = str + tmp
            author=item['author']
            content=item['content']
            stats_vote = item['stats_vote']
            contentid=item['contentid']
            sql="insert ignore into t_qiushi(author,content,vote,content_id) values('%s','%s','%s','%s')" % (author,content,stats_vote,contentid)
            cur.execute(sql)
        print str
        conn.commit()
        cur.close()
        conn.close()
        
		#settings = get_project_settings()
		#mailer = MailSender.from_settings(settings)
		#mailer.send(to='jeremy.h@foxmail.com',subject='qiushibaike',body=str,mimetype='text/plain;charset="utf-8"')
