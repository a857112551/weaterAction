#!/usr/bin/python3
#coding=utf-8
import time

import requests, json
import os

CITYCODE=os.environ.get('CITYCODE') #itboy地区码
KEY=os.environ.get('KEY') #tianapikey

def get_iciba_everyday():
    icbapi = 'http://open.iciba.com/dsapi/'
    eed = requests.get(icbapi)
    bee = eed.json()  #返回的数据
    english = bee['content']
    zh_CN = bee['note']
    str = '【奇怪的知识】\n' + english + '\n' + zh_CN
    return str

def ServerPush(info):
    cur_path = os.path.abspath(os.path.dirname(__file__))
    if os.path.exists(cur_path + "/notify.py"):
        try:
            from notify import send
        except:
            print("加载通知服务失败~")
        else:
            send('今日份提醒', info)
            print("加载通知服务成功~")

def main():
    try:
        api = 'http://t.weather.itboy.net/api/weather/city/'             #API地址，必须配合城市代码使用
        city_code = CITYCODE   #进入https://where.heweather.com/index.html查询你的城市代码
        tqurl = api + city_code
        response = requests.get(tqurl)
        d = response.json()         #将数据以json形式返回，这个d就是返回的json数据
        if(d['status'] == 200):     #当返回状态码为200，输出天气状况
            parent = d["cityInfo"]["parent"] #省
            city = d["cityInfo"]["city"] #市
            update_time = d["time"] #更新时间
            date = d["data"]["forecast"][0]["ymd"] #日期
            week = d["data"]["forecast"][0]["week"] #星期
            weather_type = d["data"]["forecast"][0]["type"] # 天气
            wendu_high = d["data"]["forecast"][0]["high"] #最高温度
            wendu_low = d["data"]["forecast"][0]["low"] #最低温度
            shidu = d["data"]["shidu"] #湿度
            pm25 = str(d["data"]["pm25"]) #PM2.5
            pm10 = str(d["data"]["pm10"]) #PM10
            quality = d["data"]["quality"] #天气质量
            fx = d["data"]["forecast"][0]["fx"] #风向
            fl = d["data"]["forecast"][0]["fl"] #风力
            ganmao = d["data"]["ganmao"] #感冒指数
            tips = d["data"]["forecast"][0]["notice"] #温馨提示
            # 天气提示内容
            tdwt = "【今日份天气】\n城市： " + parent + city + \
                   "\n日期： " + date + \
                   "\n星期: " + week + \
                   "\n天气: " + weather_type + \
                   "\n温度: " + wendu_high + " / "+ wendu_low + \
                   "\n湿度: " + shidu + \
                   "\nPM25: " + pm25 + \
                   "\n空气质量: " + quality + \
                   "\n风力风向: " + fx + fl + \
                   "\n感冒指数: "  + ganmao
            # 黄历
            api = 'http://api.tianapi.com/txapi/lunar/index?key='
            key_code=KEY
            tqurl = api + key_code
            response = requests.get(tqurl)
            d = response.json()
            if(d['code'] == 200):
                yinli=d['newslist'][0]['lubarmonth']+d['newslist'][0]['lunarday']
                yi=d['newslist'][0]['fitness']
                ji=d['newslist'][0]['taboo']
                tdwt=tdwt+"\n【今日黄历】"+ \
                     "\n阴历："+yinli+ \
                     "\n宜："+yi+ \
                     "\n忌："+ji
            if(d['newslist'][0]['lunarday']=="初一" or d['newslist'][0]['lunarday']=="十五"):
                tdwt=tdwt+"\n今天是"+d['newslist'][0]['lunarday']+"哦，别忘了烧香拜佛呀"

            # requests.post(cpurl,tdwt.encode('utf-8'))         #把天气数据转换成UTF-8格式，不然要报错。
            tdwt=tdwt+"\n更新时间：" + update_time + \
                 "\n✁✁✁✁✁✁✁✁✁✁✁✁✁✁✁✁✁✁✁✁✁✁✁✁\n" + get_iciba_everyday()
            print(tdwt)
            ServerPush(tdwt)
    except Exception:
        error = '【出现错误】\n　　今日天气推送错误，请检查服务或网络状态！'
        print(error)
        print(Exception)

if __name__ == '__main__':
    main()
    
