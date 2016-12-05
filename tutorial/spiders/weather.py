# -*- coding: utf-8 -*-
import scrapy
import datetime
import time
import re
import json
from voice import Voice 
from scrapy.http import Request

class WeatherSpider(scrapy.Spider):
    name = "weather"
    allowed_domains = ["www.weather.com.cn"]
    start_urls = (
        'http://www.weather.com.cn/weather1d/101280601.shtml',
    )
    
    dingzhi_url = "http://d1.weather.com.cn/dingzhi/101280601.html?_=%d" #今日天气 %s 参数为 毫秒时间戳
    headers_dingzhi = {
        "Host": "d1.weather.com.cn",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": "http://www.weather.com.cn/weather1d/101280601.shtml",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
    }
    
    sk2d_url = "http://d1.weather.com.cn/sk_2d/101280601.html?_=%d"
    headers_sk2d = {
        "Host": "d1.weather.com.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0",
        "Accept": "*/*",
        "Upgrade-Insecure-Requests": "1",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "http://www.weather.com.cn/weather1d/101280601.shtml",
        "Connection": "keep-alive"
    }
    
    weather1d_url = "http://www.weather.com.cn/weather1d/101280601.shtml"
    headers_weather1d = {
        "Host": "www.weather.com.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "http://www.weather.com.cn/",
        "Connection": "keep-alive"
    }
    time = ""
    dingzhi = ""
    sk2d = ""
    liveStr = ""
    
    weatherStr = ""
    
    
    def start_requests(self):
        requests = []
        now = datetime.datetime.now()
        self.time = "现在时刻，北京时间：" + now.strftime('%Y-%m-%d %H:%M:%S') + "。"
        
        timeTs = int(time.time())* 1000
        dingzhi_url = self.dingzhi_url  % (timeTs)
        #print dingzhi_url
        requests.append(Request(dingzhi_url,headers=self.headers_dingzhi, callback = self.parse_dingzhi))
        
        sk2d_url = self.sk2d_url  % (timeTs)
        #print sk2d_url
        requests.append(Request(sk2d_url,headers=self.headers_sk2d, callback = self.parse_sk2d))
        
        weather1d_url = self.weather1d_url
        #print weather1d_url
        requests.append(Request(weather1d_url,headers=self.headers_weather1d, callback = self.parse))
        
        return requests
    
    #var cityDZ101280601 ={"weatherinfo":{"city":"101280601","cityname":"深圳","temp":"26℃","tempn":"18℃","weather":"多云","wd":"无持续风向","ws":"微风","weathercode":"d1","weathercoden":"n1","fctime":"20161205080000"}};var alarmDZ101280601 ={"w":[]}
    def parse_dingzhi(self,response):
        jsStr = response.body
        pattern = re.compile(r"(\{.*\});")
        match = pattern.search(jsStr) 
        jsonStr = match.group(1)
        arr = json.loads(jsonStr)
        weatherinfo = arr['weatherinfo']
        dingzhi = "今天最高气温，" + weatherinfo['temp'] + "，最低气温，" +  weatherinfo['tempn'] + "、"+ weatherinfo['weather'] + "、" + weatherinfo['ws'] + "。"
        self.dingzhi = dingzhi
    
    #var dataSK = {"nameen":"shenzhen","cityname":"深圳","city":"101280601","temp":"24","tempf":"75","WD":"北风","wde":"N ","WS":"2级","wse":"&lt;12km/h","SD":"63%","time":"18:30","weather":"多云","weathere":"Cloudy","weathercode":"n01","qy":"1011","njd":"暂无实况","sd":"63%","rain":"0","rain24h":"0","aqi":"80","limitnumber":"","aqi_pm25":"80","date":"12月05日(星期一)"}    
    def parse_sk2d(self,response):
        jsStr = response.body
        pattern = re.compile(r"(\{.*\})")
        match = pattern.search(jsStr) 
        jsonStr = match.group(1)
        weatherinfo = json.loads(jsonStr)
        sk2d = "当前温度，" + weatherinfo['temp'] + "℃，"+ weatherinfo['weather'] + "，相对湿度，" + weatherinfo['sd'] + "，风力，" + weatherinfo['WD'] + "，" + weatherinfo['WS'] + "，pm2.5 " + weatherinfo['aqi_pm25'] + "。"
        self.sk2d = sk2d
    
    def parse(self, response):
        liveStr = u"生活指数。"
        for li in response.xpath('//div[@class="livezs"]/ul[@class="clearfix"]/li'): #.extract_first().encode('utf-8')
            #print live
            li1_span = li.xpath('span/text()').extract_first() #.encode('utf-8')
            if li1_span is None:
                li1_span = li.xpath('a/span/text()').extract_first() #.encode('utf-8')
                li1_em = li.xpath('a/em/text()').extract_first() #.encode('utf-8')
                li1_p = li.xpath('a/p/text()').extract_first() #.encode('utf-8')
            else:
                li1_em = li.xpath('em/text()').extract_first() #.encode('utf-8')
                li1_p = li.xpath('p/text()').extract_first() #.encode('utf-8')
            
            liveStr = liveStr + li1_em + "，" + li1_span + "，" + li1_p
        self.liveStr = liveStr
        
    def closed(self, reason):
        self.weatherStr = self.time + self.dingzhi + self.sk2d + self.liveStr
        print self.weatherStr
        voice = Voice()
        access_token = voice.getAccessToken()
        print access_token
        txt = self.weatherStr
        voiceFile = voice.text2audio(access_token,txt)
        voice.playVoice(voiceFile)
        
