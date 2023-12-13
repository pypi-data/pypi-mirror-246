# coding = utf-8
import crawles
l = []
for page in range(1, 6):
    url = 'https://match.yuanrenxue.cn/match/13'

    cookies = {
        'Hm_lpvt_9bcbda9cbf86757998a2339a0437208e': '1702370772',
        'Hm_lpvt_c99546cf032aaa5a679230de9a95c7db': '1702372083',
        'Hm_lvt_9bcbda9cbf86757998a2339a0437208e': '1702370772',
        'Hm_lvt_c99546cf032aaa5a679230de9a95c7db': '1702370754',
        'no-alert3': 'true',
        'qpfccr': 'true',
        'sessionid': 'ybwnsiiifc00tyhhzkxtdak761e45600',
        'tk': '-1040984292813191015',
        'yuanrenxue_cookie': '1702372078|EO3qdi3iHnNAmAvdUVilp67JZc0Nhl01j9PLNx17SuirdKaVDRkttzMj0Gy1bpbYcG3QsV9irY9XjNS4UtWtIKaSn0uDp1FRNlNCXPV3wqZUQfZx44xx1hz0FqRqT6W1jmZmX5fb11Um',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'authority': 'match.yuanrenxue.cn',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://match.yuanrenxue.cn/match/13',
        'sec-ch-ua': '\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '\"Windows\"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    params = {
    }

    # 当前时间戳: 1702372251.4653976
    response = crawles.session_get(url, headers=headers, params=params, cookies=cookies)
    print(response.text)
    data = ''.join(response.findall(r"\('(.*?)'\)")).split('=')


    url = 'https://match.yuanrenxue.cn/api/match/13'

    cookies = {
        data[0]: data[1]
    }

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'authority': 'match.yuanrenxue.cn',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://match.yuanrenxue.cn/match/13',
        'sec-ch-ua': '\"Microsoft Edge\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '\"Windows\"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'page': page,
    }


    # 当前时间戳: 1702371736.1471784
    response = crawles.session_get(url, headers=headers, params=params, cookies=cookies)
    print(response.text)
    print(response.cookies)

    for i in response.json()['data']:
        l.append(i['value'])

print(sum(l))
