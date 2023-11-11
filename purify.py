
import re
import yaml
import requests

with open('rule.yml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

url = ""

def expand_short_url(short_url):
    try:
        response = requests.head(short_url, allow_redirects=True)
        expanded_url = response.url
        return expanded_url
    except requests.exceptions.RequestException as e:
        print("发生错误：", e)
        return None

def remove_tracking_params(url, rules):
    for rule in rules:
        pattern = r'(\?|&){0}=[^&]*'.format(rule)
        url = re.sub(pattern, '', url)
    return url

def remove_tracking_params_by_config(url, config):
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