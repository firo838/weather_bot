#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urllib.request, urllib.error
import json
import re
from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ

def open_id():
    ld = open("./id_list.txt", "r", encoding="utf-8")
    lines = ld.readlines()
    ld.close()
    return lines

def find_cityname(citycode, lines):
    for line in lines:
        if line.find(citycode) >= 0:
            #print line[:-1]
            citylist = line[:-1].split(" ")
            cityname = citylist[0].split("\"")
            #print cityname[1]
            return cityname

def find_citycode(cityname, lines):
    for line in lines:
        if line.find(cityname) >= 0:
            #print line[:-1]
            citylist = line[:-1].split(" ")
            citycode = citylist[1].split("\"")
            #print cityname[1]
            return citycode[1]

def find_city(text, lines):
    for line in lines:
        citylist = line[:-1].split(" ")
        c = citylist[0].split("\"")
        c = ''.join(c)
        if re.search(c, text):
            print("call c")
            return c
    print("call empty")
    return ''

def print_weather(res, cityname):
    print(u'今日から3日間の' + cityname[1] + 'の天気')
    for forecast in res['forecasts']:
        print('*******************************')
        print(forecast['dateLabel']+'('+forecast['date']+')').encode('utf-8')
        print(forecast['telop']).encode('utf-8')
    print('*******************************')

def printbot_weather(res, cityname, message):
    msg0 = '今日から3日間の' + cityname[1] + 'の天気'
    message.send(msg0)
    msg1 = '*******************************'
    for forecast in res['forecasts']:
        msg2 = (forecast['dateLabel']+'('+forecast['date']+')').encode('utf-8')
        msg3 = (forecast['telop']).encode('utf-8')
        message.send(msg1)
        message.send(msg2)
        message.send(msg3)
    message.send(msg1)

def printbot_weather2(res, cityname, message):
    msg = '今日から3日間の' + cityname[1] + 'の天気\n'.encode('utf-8')
    msg1 = '*******************************\n'.encode('utf-8')
    msg = msg + msg
    for forecast in res['forecasts']:
        msg2 = (forecast['dateLabel']+'('+forecast['date']+')').encode('utf-8')
        msg3 = (forecast['telop']).encode('utf-8')
        msg = msg + msg1 + msg2 + msg3
    msg = msg + msg1
    message.send(msg)

def printbot_weather3(res, cityname, message):
    msg0 = '今日から3日間の' + cityname[1] + 'の天気'
    msg1 = '*******************************'
    msgj = msg0 + '\n' #+ msg1 + '\n'
    for forecast in res['forecasts']:
        msg2 = forecast['dateLabel'] + '(' + forecast['date'] + ')'
        msg3 = (forecast['telop'])
        msgj = msgj + msg1 + '\n' + msg2 + '\n' + msg3 + '\n'
    msgj = msgj + msg1 + '\n'
    msg = json.loads("[]")
    text = json.loads("{}")
    text["text"] = msgj
    msg.append(text)
    message.send_webapi('', json.dumps(msg))

def print_area(message, lines):
    msg0 = '***検索可能なすべての地域***' + '\n'
    for line in lines:
        citylist = line[:-1].split(" ")
        c = citylist[0].split("\"")
        msg0 = msg0 + ''.join(c) + '\n'
    msg = json.loads("[]")
    text = json.loads("{}")
    text["text"] = msg0
    msg.append(text)
    message.send_webapi('', json.dumps(msg))

def weather_reply(message):
    citycode = '130010' # デフォルトエリア : 東京
    
    res = urllib.request.urlopen(url='http://weather.livedoor.com/forecast/webservice/json/v1?city=%s'%citycode).read()
    
    # 読み込んだJSONデータをディクショナリ型に変換
    res = json.loads(res)
    cityname = find_cityname(citycode, open_id())
    #print_weather(res, cityname)
    printbot_weather3(res, cityname, message)

def weather_reply2(message):
    text = message.body['text']     # メッセージを取り出す
    citycode = '130010'
    lines = open_id()
    if find_city(text, lines) is '':
        citycode = find_citycode(find_city(text, lines), lines)
        url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city=' + citycode
        res = urllib.request.urlopen(url=url).read()

        # 読み込んだJSONデータをディクショナリ型に変換
        res = json.loads(res)
        cityname = find_cityname(citycode, lines)
        #print_weather(res, cityname)
        printbot_weather3(res, cityname, message)
    else:
        default_respond(message)

def default_respond(message):
    msg = 'そんな都市ねーです。'
    message.reply(msg)

def area_reply(message):
    print_area(message, open_id())

# bot宛のメッセージ
@respond_to(r'天気')
def mention_func(message):
    weather_reply2(message)

@respond_to(r'地域')
def respond_area(message):
    area_reply(message)

## チャンネル内のbot宛以外の投稿
#@listen_to(r'天気')
#def listen_func(message):
#    weather_reply2(message)
#
#@listen_to(r'地域')
#def listen_area(message):
#    area_reply(message)
