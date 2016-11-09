#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
#import MySQLdb

from scrapy.mail import MailSender
from scrapy.utils.project import get_project_settings

class QiushiSpider(scrapy.Spider):
    name = 'qiushi'
    allowed_domains = ['qiushibaike.com']
    start_urls = ["http://www.qiushibaike.com/text/page/3/"] #"http://www.qiushibaike.com/text/",,"http://www.qiushibaike.com/text/page/3/"
    web_data_list = []

    def parse(self,response):
        for sel in response.xpath('//div[contains(@class,"article block untagged mb15")]'):
            #用户信息域
            user_info = sel.xpath('div[contains(@class,"author clearfix")]')
            #用户编号
            userid = user_info.xpath('a/@href').re(r'/users/(.*)/')[0].encode('utf-8')
            #print userid
            author = user_info.xpath('a/h2/text()').extract_first(default=u'匿名用户').encode('utf-8')
            #print author
            head_img = user_info.xpath('a/img/@src').extract_first().encode('utf-8')
            #print head_img
            age = user_info.xpath('div/text()').extract_first().encode('utf-8')
            #print age
            sex = user_info.xpath('div/@class').re(r'articleGender (.*)Icon')[0].encode('utf-8') #.encode('utf-8')
            #print sex
            #糗事内容
            content_arr = sel.xpath('a[contains(@class,"contentHerf")]/div/span/text()').extract() #.encode('utf-8') #.encode('utf-8')span/
            content = ""
            for i_str in content_arr:
                content = content + i_str.encode('utf-8')
            #print content
            #糗事id
            contentid = sel.xpath('@id').re(r'qiushi_tag_(.*)')[0].encode('utf-8')
            #print contentid
            #投票数
            stats_vote = sel.xpath('div[contains(@class,"stats")]/span[contains(@class,"stats-vote")]/i/text()').extract_first().encode('utf-8')
            #print stats_vote
            item = {"userid":userid,"author":author,"head_img":head_img,"age":age,"sex":sex,"content":content,"stats_vote":stats_vote,"contentid":contentid}
            self.web_data_list.append(item)
            #print ctime
            #print author,content,stats_vote
    def closed(self,reason):
        str = ''
        #conn = MySQLdb.connect(host='127.0.0.1',user='spider_user',passwd='spider_user!@#',port=3306,db='db_spider',charset='utf8')
        #cur = conn.cursor()

        for index,item in enumerate(self.web_data_list):
    	    tmp = 'index:%d, userid:%s, author:%s,head_img:%s \n,age:%s,sex:%s, vote:%s,contentid:%s\n[%s]\n\n' % (index,item['userid'],item['author'],item['head_img'],item['age'],item['sex'],item['stats_vote'],item['contentid'],item['content'])
            str = str + tmp
            author=item['author']
            content=item['content']
            stats_vote = item['stats_vote']
            contentid=item['contentid']
            #sql="insert ignore into t_qiushi(author,content,vote,content_id) values('%s','%s','%s','%s')" % (author,content,stats_vote,contentid)
            #cur.execute(sql)
        #print str
        #conn.commit()
        #cur.close()
        #conn.close()
        
        settings = get_project_settings()
        mailer = MailSender.from_settings(settings)
        mailer.send(to=['1053995075@qq.com','jeremy.h@foxmail.com'],subject='qiushibaike',body=str,cc=None,mimetype='text/plain;charset="utf-8"')
