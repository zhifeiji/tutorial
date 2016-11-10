# -*- coding: utf-8 -*-
import scrapy
import json
import re
import base64
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from cookielib import CookieJar

class LoginSpider(CrawlSpider):
    name = "login"
    allowed_domains = ["qiushibaike.com"]
    start_urls = (
        'http://www.qiushibaike.com/text/',
    )
    index_url = "http://www.qiushibaike.com/"
    login_url = "http://www.qiushibaike.com/new4/session"
    voting_url = "http://www.qiushibaike.com/new3/vote/"
    
    headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
    "Connection": "keep-alive",
    #"Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    "Referer": "http://www.qiushibaike.com/",
    "X-Requested-With":"XMLHttpRequest"
    }
    
    def start_requests(self):
        return [Request(self.index_url,meta = {'cookiejar' : 1}, callback = self.post_login)] 
        

    def post_login(self, response):
        # here you would extract links to follow and return Requests for
        # each of them, with another callback
        print "preparing login"
        #xsrf = response.xpath('//input[@name="_xsrf"]/@value').extract_first()
        #print xsrf
        headers = str(response.headers)
        t = re.search("_xsrf=([\w|]*)",headers)
        xsrf2 = t.group(1)
        print xsrf2
        return [scrapy.FormRequest(self.login_url, 
                            meta = {'cookiejar' : response.meta['cookiejar']},
                            headers = self.headers,
                            formdata = {
                            '_xsrf': xsrf2,
                            'login': 'jeremy.h@foxmail.com',
                            'password': 'a779812560',
                            'remember_me':'checked',
                            'duration':'6437925',
                            },
                            callback = self.after_login,
                            dont_filter = True
                            )]
    def after_login(self, response) :
        for url in self.start_urls :
            yield Request(url,meta = {'cookiejar' : response.meta['cookiejar']},headers = self.headers,callback=self.parse)

    def parse(self, response):
        #print response
        #pass
        for sel in response.xpath('//div[contains(@class,"article block untagged mb15")]'):
            #糗事id
            contentid = sel.xpath('@id').re(r'qiushi_tag_(.*)')[0].encode('utf-8')
            #self.voting(contentid,response)
            userid = '13479418';
            str = "%s+%s" % (contentid , userid)
            a = base64.b64encode(str)
            voteurl = "%s%s" %(self.voting_url,a)
            print voteurl
            yield Request(voteurl,meta = {'cookiejar' : response.meta['cookiejar']},headers = self.headers,callback=self.parse_voting)
            
    #投票，+1        
    def voting(self,contentid,response):
        pass
        
    def parse_voting(self,response):
        pass
            
            
