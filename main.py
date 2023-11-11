'''
Author: DBin_K DBinKv1@Gmail.com
Date: 2023-11-11 22:26:43
LastEditors: DBin_K DBinKv1@Gmail.com
LastEditTime: 2023-11-11 22:37:49
FilePath: \Link-Purify\main.py
Description: 
'''
import requests

def expand_short_url(short_url):
    try:
        response = requests.head(short_url, allow_redirects=True)
        expanded_url = response.url
        return expanded_url
    except requests.exceptions.RequestException as e:
        print("发生错误：", e)
        return None

# 测试代码
short_url = "https://b23.tv/qovBl9q"
expanded_url = expand_short_url(short_url)
if expanded_url:
    print("展开后的链接：", expanded_url)

