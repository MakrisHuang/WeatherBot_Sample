# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import sys
import time
import json, requests

from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
weatherCenterBureauKey = os.getenv('WEATHER_CENTER_BUREAU_KEY', None)

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)
if weatherCenterBureauKey is None:
    print('Specify WEATHER_CENTER_BUREAU_KEY as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

def analyzeLocation(userMsg):
    locations = [
        u"宜蘭",
        u"花蓮",
        u"臺東",
        u"台東",
        u"澎湖",
        u"金門",
        u"連江",
        u"臺北",
        u"台北",
        u"新北",
        u"桃園",
        u"臺中",
        u"台中",
        u"臺南",
        u"台南",
        u"高雄",
        u"基隆",
        u"新竹",
        u"苗栗",
        u"彰化",
        u"南投",
        u"雲林",
        u"嘉義",
        u"屏東"
    ]

    location = ""
    wordIndex = 0
    for county in locations:
        if userMsg.find(county) != -1:
            wordIndex = userMsg.find(county)

            location = userMsg[wordIndex: wordIndex + 2]
            if location[0] == u'台':
                location = u'臺' + location[1]
    if isinstance(location, unicode):
        print 'location is unicode'
    # print 'get location: ' + location

    # 加上縣
    if len(location) > 0:
        if (location == u"宜蘭" or location == u"花蓮" or
        location ==  u"臺東" or location == u"澎湖" or
        location == u"金門" or location == u"連江" or
        location == u"彰化" or location == u"南投" or
        location == u"雲林" or location == u"屏東"):
            location += u"縣"

    # 處理有「縣」和「市」的
    if location == u"苗栗" or location == u"嘉義" or \
    location == u"新竹":
        countyLevel = userMsg[wordIndex + 2: wordIndex + 3]
        if countyLevel == u"縣" or countyLevel == u"市":
            # 採用使用者輸入的縣或市
            location += countyLevel
        else:
            # 使用者未輸入，預設採用「市」
            location += u"市"

    # 加入市
    if (location == u"臺北" or location == u"新北" or
    location == u"桃園" or location == u"臺中" or
    location == u"臺南" or location == u"高雄" or
    location == u"基隆"):
        location += u"市"

    return location

def getWeatherResponse(cityName, key):
    rootUrl = "http://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001"
    headers = {'Authorization': key}

    # Wx: 天氣簡短報告 ex. 陰短暫雨 26度
    # PoP: 降雨機率 ex. 60%
    # MinT: 最低溫度
    # CI: 體感 ex. 稍有寒意
    # MaxT: 最高溫度
    requestUrl = rootUrl + '?locationName=' + cityName + '&elementName=Wx' + '&sort=time'
    r = requests.get(requestUrl, headers=headers)
    print 'weather request status code: ' + str(r.status_code)
    if r.status_code == 200:
        return r.json()
    else:
        return None

def getAllWeathers(result):
    weatherStates = []
    weatherElements = result['records']['location'][0]['weatherElement'][0]['time']
    for weather in weatherElements:
        startTime = weather['startTime']
        endTime = weather['endTime']
        msg = u'從' + startTime + u'\n到' + endTime \
        + u'\n天氣情況: ' + weather['parameter']['paramterName'] + u'\n\n'
        weatherStates.append(msg)
    return weatherStates

def getCurrentWeather(result):
    location = result['records']['location'][0]['locationName']
    currWeather = result['records']['location'][0]['weatherElement'][0]['time'][0]
    msg = u'現在' + location + u'天氣: ' + currWeather['parameter']['paramterName']
    return msg

def getReplyMsg(allWeathers, currWeather):
    msg = u"未來36小時預報\n"
    for weatherMsg in allWeathers:
        msg += weatherMsg
    return msg + currWeather

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    replyMsg = ""
    userMsg = event.message.text
    locationName = analyzeLocation(userMsg)
    if len(locationName) != 0:
        weatherResult = getWeatherResponse(locationName, weatherCenterBureauKey)
        allWeathers = getAllWeathers(weatherResult)
        currWea = getCurrentWeather(weatherResult)
        replyMsg = getReplyMsg(allWeathers, currWea)
    else:
        replyMsg = "無法判定您要查詢的天氣位置，請輸入縣市名。如：今天台中市天氣如何？"
    line_bot_api.reply_message(
      event.reply_token,
      TextSendMessage(text=replyMsg))

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
