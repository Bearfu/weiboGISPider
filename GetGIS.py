
import requests
import RadomGIS
from bs4 import BeautifulSoup

import random

source_url = "https://s.weibo.com/weibo/%E5%8C%97%E4%BA%AC%E5%A4%A7%E9%9B%A8?q=%E5%8C%97%E4%BA%AC%E6%9A%B4%E9%9B%A8&region=custom:11:6&typeall=1&haslink=1&timescope=custom:2012-07-01-0:2012-08-11-16&Refer=g&page=2"
# url = "http://t.cn/zWK0sZW"
# response = requests.request("GET", url)
# print(response.headers)
# print(response.headers['Set-Cookie'])


# 这一串里面有真实的经纬度 你看一下逻辑 怎么取出来
# s = "MLOGIN=0; expires=Thu, 31-Oct-2019 07:47:59 GMT; Max-Age=3600; path=/; domain=.weibo.cn, _T_WM=13368055335; expires=Sun, 10-Nov-2019 06:47:59 GMT; Max-Age=864000; path=/; domain=.weibo.cn, XSRF-TOKEN=deleted; expires=Thu, 01-Jan-1970 00:00:01 GMT; Max-Age=0; path=/; domain=.weibo.cn, XSRF-TOKEN=ef62e2; expires=Thu, 31-Oct-2019 07:07:59 GMT; Max-Age=1200; path=/; domain=m.weibo.cn, WEIBOCN_FROM=1110006030; path=/; domain=.weibo.cn; HttpOnly, M_WEIBOCN_PARAMS=fid%3D100101116.26561_39.882278%26uicode%3D10000011; expires=Thu, 31-Oct-2019 06:57:59 GMT; Max-Age=600; path=/; domain=.weibo.cn; HttpOnly"
# "M_WEIBOCN_PARAMS=fid%3D100101116.26561_39.882278%26uicode%3D10000011"
# a = s.split(";")
# print(a[-6])
#
# for b in a:
#     print(b)

url = "https://s.weibo.com/weibo/%25E5%258C%2597%25E4%25BA%25AC%25E5%25A4%25A7%25E9%259B%25A8?q=北京暴雨&region=custom:11:1&typeall=1&suball=1&timescope=custom:2012-07-24-08:2012-07-24-18&Refer=g"

headers = {
    'Connection': "keep-alive",
    'Cache-Control': "max-age=0",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
    'Sec-Fetch-Mode': "navigate",
    'Sec-Fetch-User': "?1",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    'Sec-Fetch-Site': "none",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
    'Cookie': "SINAGLOBAL=9567883550528.377.1569808672284; un=chengqigu@wallstreetcn.com; UOR=www.techug.com,widget.weibo.com,link.zhihu.com; login_sid_t=8d38d4567ba520550ee2c4b3522624b1; cross_origin_proto=SSL; _ga=GA1.2.1846032271.1572514968; _gid=GA1.2.1623070641.1572514968; _s_tentry=-; __gads=Test; Apache=4919063187151.969.1572514972843; ULV=1572514972878:4:3:1:4919063187151.969.1572514972843:1571381327313; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5yo3qLH_A-Z1xIXjnFVHa35JpX5K2hUgL.Fo-fSKz41hzESKz2dJLoIpRLxK.L1h5L1h.LxKnL1hzLBK2LxK-LB--L1-xW-85t; ALF=1604050975; SSOLoginState=1572514977; SCF=AlKv9XO_kn5oN9LEpTD5dfRHwvgf9Y6efvgGH20icb--GpUEpivtjBNMTUa09x9aBFJ3lzICRXyDaHAD9EgR_NQ.; SUB=_2A25wvtzxDeRhGeNL7lAY-CzOzj6IHXVTykk5rDV8PUNbmtBeLWqikW9NSOkvcjkcWl5fFzHNljsMmGlxHgO0QDK5; SUHB=0ElqGJmXeh3aG2; WBStorage=384d9091c43a87a5|undefined; webim_unReadCount=%7B%22time%22%3A1572515285195%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D",
    'Host': "s.weibo.com",
    'cache-control': "no-cache"
}
try:
    response = requests.request("GET", url, headers=headers)
except:
    pass
if "抱歉，未找到“北京暴雨”相关结果。" not in response.text:
    # html文件转为SOUP对象
    soup = BeautifulSoup(response.text, 'lxml')
    # 获取本次搜索结果能翻页页数
    try:
        m_page = soup.find("div", "m-page")
        li = m_page.find_all("li")
        print("总页数 = ", len(li))
    except:
        print("总页数 = 1")
    # 获取用户微博列表
    con_L = soup.find_all("div", "card-wrap")
    # 轮询列表中的微博
    for a in con_L:
        userInfo = a.find('a')
        if userInfo:
            txt = a.find('p', 'txt')
            if txt:
                try:
                    a_o = txt.find('a').find('i')
                    if a_o.get_text() == '2':
                        response = requests.request("GET", txt.find('a')['href'])
                        SC = response.headers['Set-Cookie']
                        print()
                except:
                    pass