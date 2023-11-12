'''
Author: DBin_K DBinKv1@Gmail.com
Date: 2023-11-12 01:09:06
LastEditors: DBin_K DBinKv1@Gmail.com
LastEditTime: 2023-11-12 12:18:20
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

print(config)

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

def remove_tracking_params(url):
    """
    根据给定的规则列表，清除URL中的跟踪参数并返回净化后的URL。

    参数：
    - url：要清除跟踪参数的URL

    返回：
    - url：清除跟踪参数后的净化URL
    """
    global config
    print(config)
    # 获取全局配置中的提供者配置信息
    providers = config['providers']
    print(providers)
    for provider, provider_config in providers.items():
        # 获取当前提供者的URL匹配域名
        pattern = provider_config['urlPattern']
        # 如果URL匹配当前提供者的域名，则执行跟踪参数清除操作
        if re.match(pattern, url):
            # 获取当前提供者的规则列表
            rules = provider_config['rules']
            # 遍历规则列表，逐个清除URL中的跟踪参数
            for rule in rules:
                # 构建匹配规则的正则表达式
                pattern = r'(\?|&){0}=[^&]*'.format(rule)
                # 使用正则表达式替换URL中的匹配项为空字符串，实现参数清除
                url = re.sub(pattern, '', url)
            break
    # 返回净化后的URL
    return url

# 示例用法

#url = 'https://www.bilibili.com/video/BV1R7411K7aF?spm_id_from=333.334.b_63686965665f72656f6d6d656e64.1'

# http://xhslink.com/YhhEpw

# 测试代码
"""short_url = "https://b23.tv/qovBl9q"

expanded_url = expand_short_url(short_url)
url = expanded_url

if expanded_url:
    print("展开后的链接：", expanded_url)

clean_url = remove_tracking_params_by_config(url, config)

print("净化后的链接：", clean_url)"""