# WeatherBot妹 - LINE Messaging for Weather Request

### English Version
This is a LineBot for user can check the local weather by specifying the location. Weather data comes from the Central Weather Bureau (CWB). 

To access weather data from CWB, you must get the access token from the account of [CWB](http://www.cwb.gov.tw/V7/index.htm). For more information, please refers to the [OPEN DATA of Taiwan](http://opendata.cwb.gov.tw/usages)

For Line channel secret and access token, you can get them from Line developers page.

### 中文版本
此為使用LineBot API所建置的天氣查詢機器人，可供查詢台灣各地區天氣。天氣資料來源：中央氣象局

如果要存取氣象局的天氣資料，必須在[中央氣象局](http://www.cwb.gov.tw/V7/index.htm)辦帳號後取得授權碼。詳細資料請查閱：[OPEN DATA of Taiwan](http://opendata.cwb.gov.tw/usages)

此外若要設置Line channel secret和access token，請到Line developer頁面取得


## Starting by setting local env

```
$ export LINE_CHANNEL_SECRET=YOUR_LINE_CHANNEL_SECRET
$ export LINE_CHANNEL_ACCESS_TOKEN=YOUR_LINE_CHANNEL_ACCESS_TOKEN
$ export WEATHER_CENTER_BUREAU_KEY=YOUR_WEATHER_CENTER_BUREAU_KEY

$ pip install -r requirements.txt
```

Run sample

```
$ python app.py
```

## Getting started with Heroku

### heroku button

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/MakrisHuang/WeatherBot_Sample)

then set Webhook URL in your line developer page: `https://{YOUR_APP}.herokuapp.com/callback`

### deploy by yourself

```
heroku create
heroku info # then set Webhook URL: https://{YOUR_APP}.herokuapp.com/callback
heroku config:set LINE_CHANNEL_SECRET="..."
heroku config:set LINE_CHANNEL_ACCESS_TOKEN="..."
heroky config:set WEATHER_CENTER_BUREAU_KEY="..."
git push heroku master
heroku logs
```
