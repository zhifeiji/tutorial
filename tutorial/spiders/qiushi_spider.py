#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
#import MySQLdb

from scrapy.mail import MailSender
from scrapy.utils.project import get_project_settings
from scrapy.http import Request
from pymongo import *

class QiushiSpider(scrapy.Spider):
    name = 'qiushi'
    allowed_domains = ['qiushibaike.com']
    #http://www.qiushibaike.com/history/ 糗事百科，穿越入口
    start_urls = ["http://www.qiushibaike.com/history/"] #"http://www.qiushibaike.com/text/",,"http://www.qiushibaike.com/text/page/3/"
    web_data_list = []
    client = MongoClient("mongodb://10.10.30.107:27117/")
    db = client.test
    collection = db.test_collection
    
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url)
    
    def parse(self,response):
        for sel in response.xpath('//div[contains(@class,"article block untagged mb15")]'):
            #用户信息域
            user_info = sel.xpath('div[contains(@class,"author clearfix")]')
            #用户编号
            userids = user_info.xpath('a/@href').re(r'/users/(.*)/')   #[0].encode('utf-8')
            if len(userids) > 0 :
                userid = userids[0].encode('utf-8')
                #print userid
                author = user_info.xpath('a/h2/text()').extract_first(default=u'匿名用户').encode('utf-8')
                #print author
                head_img = user_info.xpath('a/img/@src').extract_first().encode('utf-8')
                #print head_img
                age = user_info.xpath('div/text()').extract_first().encode('utf-8')
                #print age
                sex = user_info.xpath('div/@class').re(r'articleGender (.*)Icon')[0].encode('utf-8') #.encode('utf-8')
            else:
                userid = 0
                author = (u'匿名用户').encode('utf-8')
                head_img = ''
                age = 0
                sex = ''
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
            
            item['_id'] = item['contentid']
            item['stats_vote'] = int(item['stats_vote'])
            print item['stats_vote']
            self.collection.insert(item)
            
            #print ctime
            #print author,content,stats_vote
        change = response.xpath('//div[contains(@class,"history-nv mb15 clearfix")]')
        random = change.xpath('//a[contains(@class,"random")]/@href').extract_first().encode('utf-8')
        #date = change.xpath('//span[contains(@class,"date")]/text()').extract_first().encode('utf-8')
        #下一个穿越的url入口
        curr_url = response.urljoin(random)
        for i in range(2,21):
            nextpage = "%spage/%d/" % (curr_url,i)
            print nextpage    
            #yield Request(nextpage)
            
    def closed(self,reason):
        str = ''
        #conn = MySQLdb.connect(host='127.0.0.1',user='spider_user',passwd='spider_user!@#',port=3306,db='db_spider',charset='utf8')
        #cur = conn.cursor()
        
        #mydict = {"name":"Lucy", "sex":"female","job":"nurse"}
        

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
        
        #将爬取的数据发送邮件
        settings = get_project_settings()
        mailer = MailSender.from_settings(settings)
        #mailer.send(to=['1053995075@qq.com','jeremy.h@foxmail.com'],subject='qiushibaike',body=str,cc=None,mimetype='text/plain;charset="utf-8"')
