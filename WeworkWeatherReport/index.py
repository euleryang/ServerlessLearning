##!/usr/bin/env python3
# -*- coding:utf-8 _*-
"""
@author: edsion
@file: index.py
@time: 2019/06/28
@contact: edsion@21kunpeng.com

"""
import os
import json
import urllib3

X = os.getenv('X', '121.6544')  # 要获取天气信息的经度
Y = os.getenv('Y', '25.1552')   # 要获取天气信息的纬度

SKYCON = {
    'CLEAR_DAY': "晴（白天）",
    'CLEAR_NIGHT': "晴（夜间）",
    'PARTLY_CLOUDY_DAY': '多云（白天）',
    'PARTLY_CLOUDY_NIGHT': '多云（夜间）',
    'CLOUDY': '阴',
    'WIND': '大风',
    'HAZE': '雾霾',
    'RAIN': '雨',
    'SNOW': '雪',
    'Unknown': '其它'
}
COMFORT = {
    -1: '未知',
    0: '闷热',
    1: '酷热',
    2: '很热',
    3: '热',
    4: '温暖',
    5: '舒适',
    6: '凉爽',
    7: '冷',
    8: '很冷',
    9: '寒冷',
    10: '极冷',
    11: '刺骨的冷',
    12: '湿冷',
    13: '干冷',
}


def translate_aqi(n):
    if 0 < n <= 50:
        return f'<font color="info">{n}-优</font>'
    elif 50 < n <= 100:
        return f'<font color="info">{n}-良</font>'
    elif 100 < n <= 150:
        return f'<font color="warning">{n}-轻度污染</font>'
    elif 150 < n <= 200:
        return f'<font color="warning">{n}-中度污染</font>'
    elif 200 < n <= 300:
        return f'<font color="warning">{n}-重度污染</font>'
    elif n > 300:
        return f'<font color="warning">{n}-严重污染</font>'
    else:
        return f'<font color="comment">{n}-未知</font>'


def template_string(**kwargs):
    return """当前《公司》位置天气<font color="warning">{skycon}</font>
> 气温：{temperature:.2f}摄氏度(℃)
> 气压：{pres:.2f}千帕(kPa)
> 相对湿度：{humidity:.0f}%
> 风向：{wind_direction:.0f}(从北顺时针0~360°)
> 风速：{wind_speed}公里/小时(km/h)
> 能见度：{visibility}公里(km)
> pm2.5：{pm25}μg/m³
> AQI（国标）：{aqi}
> 最近的降水带：<font color="warning">{precipitation}</font>公里(km)
> 舒适度：{comfort}
""".format(**kwargs)


def main_handler(event, context):
    http = urllib3.PoolManager()
    r = http.request(
        method='GET',
        url=f'https://api.caiyunapp.com/v2/TAkhjf8d1nlSlspN/{X},{Y}/realtime.json?lang=zh_CN&unit=metric&tzshift=28800')
    print(f'API Response:{r.data}')

    res = json.loads(r.data)
    assert res.get('status') == 'ok'

    result = res.get('result')
    assert result
    assert result.get('status') == 'ok'
    
    content = template_string(
        skycon=SKYCON.get(result.get('skycon', 'Unknown')),
        temperature=result.get('temperature', 'Unknown'),
        pres=result.get('pres', 0) / 1000,
        humidity=result.get('humidity', 0) * 100,
        wind_direction=result.get('wind', {}).get('direction', 'Unknown'),
        wind_speed=result.get('wind', {}).get('speed', 'Unknown'),
        precipitation=result.get('precipitation', {}).get('nearest', {}).get('distance', 'Unknown'),
        visibility=result.get('visibility', 'Unknown'),
        pm25=result.get('pm25', 'Unknown'),
        aqi=translate_aqi(result.get('aqi', -1)),
        comfort=COMFORT.get(result.get('comfort', {}).get('index', -1)),
    )
    encoded_data = json.dumps({"msgtype": "markdown", "markdown": {'content': content}}).encode('utf-8')
    rr = http.request(method='POST', url=os.getenv('WEBHOOK_URL'), body=encoded_data,
                      headers={'Content-Type': 'application/json'})
    print(f'webhook response:{rr.data}')
    #assert json.loads(rr.data).get('errcode') == 0
    return r.status


if __name__ == '__main__':
    main_handler(None, None)