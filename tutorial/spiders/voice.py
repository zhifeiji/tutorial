#!/usr/bin/env python
# -*- coding: utf-8 -*-
# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import urllib 
import urllib2
import json
import sys 
import os

#reload(sys)  
#sys.setdefaultencoding('utf8')   

__author__ = "hdq"
__date__ = "$2016-11-18 19:52:20$"
class Voice:
    #获取百度平台的token
    def getAccessToken(self):
        url = u"https://openapi.baidu.com/oauth/2.0/token"
        grant_type = u'client_credentials'                   #必须参数，固定为“client_credentials”；
        client_id = '0wSpuwt9jg7NjpEfIGPz9tDB'              #必须参数，应用的 API Key；
        client_secret = '226f666122b92687e8a0b91e5887c311'  #必须参数，应用的 Secret Key;

        realurl = "%s?grant_type=%s&client_id=%s&client_secret=%s" % \
                    (url,grant_type,client_id,client_secret)
        print realurl
        req = urllib2.Request(realurl)
        #print req
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        print res
        data = json.loads(res)
        return data['access_token']

    #文本转换为mp3
    def text2audio(self,access_token,text):
        url = u'http://tsn.baidu.com/text2audio' #语音合成接口支持 POST 和 GET两种方式
        tex = text   #合成的文本，使用UTF-8编码，请注意文本长度必须小于1024字节
        lan = 'zh'   #语言选择,填写zh
        tok = access_token     #开放平台获取到的开发者 access_token
        ctp = '1'    #客户端类型选择，web端填写1
        cuid = '1'   #用户唯一标识，用来区分用户，填写机器 MAC 地址或 IMEI 码，长度为60以内
        spd = '5'    #语速，取值0-9，默认为5中语速
        pit = '5'    #音调，取值0-9，默认为5中语调
        vol = '5'    #音量，取值0-9，默认为5中音量
        per = '0'    #发音人选择，取值0-1, 0为女声，1为男声，默认为女声

        params = urllib.urlencode({'tex':tex,'lan':lan,'tok':tok,'ctp':ctp,'cuid':cuid,'spd':spd,'pit':pit,'vol':vol,'per':per}) 
        print params
        #错误码	含义
        #500	不支持输入
        #501	输入参数不正确
        #502	token验证失败
        #503	合成后端错误

        realurl = u"%s?%s" % (url,params)
        print realurl
        req = urllib2.Request(realurl)
        #print req
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        #print res
        voice_file = 'voice.mp3'
        with open(voice_file, "wb") as code:     
            code.write(res)   
        print "downloading with requests"

        return voice_file

    #播放声音
    def playVoice(self,voiceFile):
        os.system(voiceFile)

    def audio2text(self,voiceFile):
        url = 'http://vop.baidu.com/server_api'

    

if __name__ == "__main__":
    print "Hello World"
    voice = Voice()
    access_token = voice.getAccessToken()
    print access_token
    txt = u"现在时刻，北京时间：2016-12-05 20:35:34。今天最高气温17℃，最低气温23℃、多云、微风。当前温度，24℃，多云，相对湿度，65%，风力，东北风，1级，pm2.5 80。生活指数。紫外线指数，弱，辐射较弱，涂擦SPF12-15、PA+护肤品。感冒指数，较易发，降温幅度较大，预防感冒。穿衣指数，较舒适，建议穿薄外套或牛仔裤等服装。洗车指数，较适宜，无雨且风力较小，易保持清洁度。运动指数，较适宜，户外运动请注意防晒。空气污染扩散指数，较差，气象条件较不利于空气污染物扩散。"
    voiceFile = voice.text2audio(access_token,txt)
    voice.playVoice(voiceFile)
