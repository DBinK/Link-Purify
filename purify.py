'''
Author: DBin_K DBinKv1@Gmail.com
Date: 2023-11-12 01:09:06
LastEditors: DBin_K DBinKv1@Gmail.com
LastEditTime: 2023-11-13 01:44:12
FilePath: \Link-Purify\purify.py
Description: 
'''
import re
import yaml
import requests

url = ""                    # 初始化URL
config_file = './rule.yml'    # 配置文件地址
# 短链接列表

# 从配置文件中加载规则
with open(config_file, 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)


def process_url(text):
    """
    主要功能, 提取文字中的域名, 如果是短链接则将其扩展

    参数: 
        text, 任意带链接的文字输入

    返回:
        url, 文字中的链接
    """
    global origin_text 

    origin_text = text

    print(f'原始text: {origin_text}\n')

    url = extract_url(text)
    domain = extract_domain(url)
    short_url_domains = [
        'b23.tv',
        'xhslink.com']

    for short_url_domain in short_url_domains:
        if short_url_domain == domain:
            url = expand_short_url(url)
    
    url = remove_tracking_params(url)
    return url
    

def extract_domain(url):
    """
    提取文字中的域名

    参数: 
        url: 链接

    返回: 
        域名，或 `None`
    """

    # 匹配域名的正则表达式
    regex = r"(https?://)?(www\.)?(\w+(?:\.\w+)+)"

    # 提取域名
    match = re.match(regex, url)
    if match:
        return match.group(3)
    else:
        return None
    
    
def extract_url(text):
    """
    提取文本中的链接并返回。

    参数: 
    - text: 要提取链接的文本

    返回: 
    - url: 链接列表
    """
    # 定义链接的正则表达式模式
    pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    
    # 使用正则表达式模式匹配文本中的链接
    match = re.search(pattern, text)
    
    if match:
        link = match.group(0)
        return link
    else:
        return "未找到链接"

def expand_short_url(short_url):
    """
    展开短链接并返回完整的URL。

    参数: 
    - short_url: 要展开的短链接

    返回: 
    - expanded_url: 展开后的完整URL，如果展开失败则返回None
    """
    try:
        
        response = requests.head(
            short_url,
            allow_redirects=True,
            verify=False)
        expanded_url = response.url
        return expanded_url
    except requests.exceptions.RequestException as e:
        print("发生错误: ", e)
        return None

def remove_tracking_params(url):
    """
    根据给定的规则列表，清除URL中的跟踪参数并返回净化后的URL。

    参数: 
    - url: 要清除跟踪参数的URL

    返回: 
    - url: 清除跟踪参数后的净化URL
    """
    global config #使用全局配置文件

    print(f'原始url: {url}\n')

    # 获取全局配置中的 provider
    providers = config['providers']
    
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
    print(f'净化url: {url}\n')
    return url

def replace_url(origin_text, url):
    """
    将文本中的链接替换为指定的URL。

    参数:
    - text: 要处理的文本
    - url: 替换链接的目标URL

    返回:
    - replaced_text: 替换后的文本
    """
    # 使用正则表达式匹配文本中的链接
    pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    replaced_text = re.sub(pattern, url, origin_text)
    return replaced_text
