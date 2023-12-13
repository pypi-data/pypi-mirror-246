# coding = utf-8
import requests

url = 'https://movie.douban.com/review/best/'

cookies = {
    '__utma': '223695111.1694651962.1694087402.1701854009.1701860339.9',
    '__utmb': '223695111.0.10.1701860339',
    '__utmc': '223695111',
    '__utmz': '223695111.1701854009.8.5.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
    '__yadk_uid': 'IsdE7yT1rpurinPSuIdtxHCk5L31pJYL',
    '_pk_id.100001.4cf6': '5113a7a4827f0ceb.1694087402.',
    '_pk_ref.100001.4cf6': '%5B%22%22%2C%22%22%2C1701860339%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D',
    '_pk_ses.100001.4cf6': '1',
    '_vwo_uuid_v2': 'D63E59A4B800BF45066982B8C74641605|02c6e1371ccf08df5a468ed21aa5326a',
    'ap_v': '0,6.0',
    'bid': 'arLwbuDr9tw',
    'll': '\"118267\"',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://movie.douban.com/review/best/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'sec-ch-ua': '\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '\"Windows\"',
}

params = {
    'start': '20',
}

# 当前时间戳: 1701860402.240319
response = requests.get(url, headers=headers, params=params, cookies=cookies)
print(response.text)
