'''
Author: DBin_K DBinKv1@Gmail.com
Date: 2023-11-12 01:09:06
LastEditors: DBin_K DBinKv1@Gmail.com
LastEditTime: 2023-11-12 11:16:08
FilePath: \Link-Purify\purify.py
Description: 
'''
import re
import yaml
import requests

url = ""                    # 初始化URL
config_file = './rule.yml'    # 配置文件地址

# 从配置文件中加载规则
with open(config_file, 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)


def expand_short_url(short_url):
    """
    展开短链接并返回完整的URL。

    参数：
    - short_url：要展开的短链接

    返回：
    - expanded_url：展开后的完整URL，如果展开失败则返回None
    """
    try:
        response = requests.head(short_url, allow_redirects=True)
        expanded_url = response.url
        return expanded_url
    except requests.exceptions.RequestException as e:
        print("发生错误：", e)
        return None

def remove_tracking_params(url, rules):
    """
    根据给定的规则列表，清除URL中的跟踪参数并返回净化后的URL。

    参数：
    - url：要清除跟踪参数的URL
    - rules：跟踪参数的规则列表

    返回：
    - url：清除跟踪参数后的净化URL
    """
    for rule in rules:
        pattern = r'(\?|&){0}=[^&]*'.format(rule)
        url = re.sub(pattern, '', url)
    return url

def remove_tracking_params_by_config(url, config):
    """
    根据配置文件中的规则，清除URL中的跟踪参数并返回净化后的URL。

    参数：
    - url：要清除跟踪参数的URL
    - config：配置文件的字典表示

    返回：
    - url：清除跟踪参数后的净化URL
    """
    for provider, provider_config in config['providers'].items():
        pattern = provider_config['urlPattern']
        if re.match(pattern, url):
            rules = provider_config['rules']
            url = remove_tracking_params(url, rules)
            break
    return url


# 示例用法

#url = 'https://www.bilibili.com/video/BV1R7411K7aF?spm_id_from=333.334.b_63686965665f7265636f6d6d656e64.1'

# 测试代码
"""short_url = "https://b23.tv/qovBl9q"

expanded_url = expand_short_url(short_url)
url = expanded_url

if expanded_url:
    print("展开后的链接：", expanded_url)

clean_url = remove_tracking_params_by_config(url, config)

print("净化后的链接：", clean_url)"""