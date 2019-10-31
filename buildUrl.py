# coding:utf-8
import urllib
import time
import requests
import RadomGIS
from bs4 import BeautifulSoup
import re
import datetime
import pymsqlDemo
import random

SelectCode = "北京大雨"  # 关键字

Regionnum = "4"  # 东城区代码
Start_time = "2012-07-21-2"  # 起始时间
End_time = "2012-07-22-23"  # 结束时间
page = 12


def get_next_time(start_time):
    # 转换成时间数组
    timeArray = time.strptime(start_time, "%Y-%m-%d-%H")
    # 转换成时间戳 顺便加一个小时
    timestamp = time.mktime(timeArray) + 3600
    # 转换成localtime
    time_local = time.localtime(timestamp)
    # 转换成新的时间格式(2016-05-05-20)
    dt = time.strftime("%Y-%m-%d-%H", time_local)
    return dt


def get_timestamp(str_time):
    return time.mktime(time.strptime(str_time, "%Y-%m-%d-%H"))


def get_datettime(str_time):
    return datetime.datetime.strptime(str_time, '%Y年%m月%d日%H:%M')


def doubleEncode(key):
    try:
        return urllib.parse.quote(urllib.parse.quote(key))
    except Exception:
        return "error"


if __name__ == '__main__':
    # 关键词 北京大雨
    # 时间起点 2012年七月20日0点 - 2012年七月30日24点
    # 范围 北京市 十八个 区
    # print(get_next_time()
    RegionnumToName = {
        "1": "东城区",
        "2": "西城区",
        "3": "崇文区",
        "4": "宣武区",
        "5": "朝阳区",
        "6": "丰台区",
        "7": "石景山区",
        "8": "海淀区",
        "9": "门头沟区",
        "11": "房山区",
        "12": "通州区",
        "13": "顺义区",
        "14": "昌平区",
        "15": "大兴区",
        "16": "怀柔区",
        "17": "平谷区",
        "29": "延庆县",
        "28": "密云县",
    }
    RegionnumList = [1,
                     2,
                     3,
                     4,
                     5,
                     6,
                     7,
                     8,
                     9,
                     11,
                     12,
                     13,
                     14,
                     15,
                     16,
                     17,
                     29,
                     28,
                     ]
    RegionnumToGis = {
        "1": [[116.381000, 39.960000], [116.393000, 39.871000], [116.422000, 39.960000], [116.436000, 39.871000]],
        "2": [[116.325000, 39.942000], [116.315000, 39.875000], [116.388000, 39.960000], [116.393000, 39.871000]],
        "3": [[116.381000, 39.960000], [116.393000, 39.871000], [116.422000, 39.960000], [116.436000, 39.871000]],
        "4": [[116.325000, 39.942000], [116.315000, 39.875000], [116.388000, 39.960000], [116.393000, 39.871000]],
        "5": [[116.406000, 40.054000], [116.449000, 39.822000], [116.620000, 40.006000], [116.617000, 39.857000]],
        "6": [[116.064000, 39.867000], [116.091000, 39.761000], [116.411000, 39.869000], [116.427000, 39.784000]],
        "7": [[116.108000, 39.983000], [116.164000, 39.885000], [116.179000, 39.983000], [116.248000, 39.895000]],
        "8": [[116.043000, 40.084000], [116.290000, 39.893000], [116.211000, 40.140000], [116.399000, 40.023000]],
        "9": [[115.445000, 39.988000], [115.581000, 39.795000], [115.852000, 40.146000], [116.158000, 39.891000]],
        "11": [[115.424000, 39.775000], [115.663000, 39.613000], [116.066000, 39.864000], [116.252000, 39.577000]],
        "12": [[116.631000, 40.017000], [116.637000, 39.606000], [116.763000, 40.013000], [116.838000, 39.649000]],
        "13": [[116.218000, 40.144000], [116.367000, 40.053000], [116.843000, 40.309000], [116.955000, 40.061000]],
        "14": [[115.880000, 40.205000], [115.964000, 40.075000], [116.286000, 40.390000], [116.485000, 40.247000]],
        "15": [[116.246000, 39.764000], [116.254000, 39.499000], [116.621000, 39.859000], [116.637000, 39.604000]],
        "16": [[116.492000, 40.976000], [116.391000, 40.333000], [116.709000, 40.928000], [116.733000, 40.283000]],
        "17": [[116.843000, 40.310000], [116.972000, 40.038000], [117.215000, 40.375000], [117.347000, 40.150000]],
        "28": [[116.720000, 40.683000], [116.737000, 40.286000], [117.250000, 40.678000], [117.182000, 40.376000]],
        "29": [[115.775000, 40.492000], [115.971000, 40.270000], [116.455000, 40.768000], [116.400000, 40.395000]],
    }
    for regionnum in RegionnumList:
        Start_time = "2012-07-01-0"  # 起始时间
        while get_timestamp(Start_time) < get_timestamp('2012-07-31-23'):
            End_time = get_next_time(Start_time)
            url = "https://s.weibo.com/weibo/%25E5%258C%2597%25E4%25BA%25AC%25E5%25A4%25A7%25E9%259B%25A8?q=北京暴雨" \
                  "&region=custom:11:{}&typeall=1&suball=1&timescope=custom:{}:{}&Refer=g".format(
                regionnum, Start_time, End_time)
            print(url)
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
            infoObj = {
                "msg_id": "",
                "address": RegionnumToName.get(str(regionnum)),
                "content": "",
                "msg_time": Start_time,
                "msg_timestamp": "",
                "tools": "",
                "transmi_count": 0,
                "comment_count": 0,
                "praise_count": 0,
                "lng": 0,
                "lat": 0,
                "sURL": "",
            }
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
                    # 获取单条微博的的ID
                    try:
                        infoObj["msg_id"] = a['mid']
                    except:
                        continue
                    userInfo = a.find('a')
                    if userInfo:
                        txt = a.find('p', 'txt')
                        if txt:
                            infoObj["content"] = txt.get_text().replace(" ", "").replace("\n", "")
                            try:
                                a_o = txt.find('a').find('i')
                                if a_o.get_text() == '2':
                                    s = txt.find('a')['href']
                                    response = requests.request("GET", txt.find('a')['href'])
                                    SC = response.headers['Set-Cookie']
                                    infoObj["sURL"] = SC
                            except:
                                pass
                        # 从class为from 的P标签中获取用户发布的时间和来源
                        fm = a.find('p', 'from')
                        if fm:
                            fms = fm.get_text().replace(" ", "").split("\xa0")
                            if len(fms) > 1:
                                infoObj["msg_time"] = fms[0].replace(" ", "").replace("\n", "")
                                infoObj["msg_timestamp"] = get_datettime(infoObj["msg_time"])
                                infoObj["tools"] = fms[1].replace(" ", "").replace("\n", "")
                        # 从class为card-act 的 div 标签中获取点赞等相关信息
                        card_act = a.find('div', 'card-act')
                        if card_act:
                            ul = card_act.find('ul')
                            lis = ul.find_all('li')
                            if len(lis[1].get_text().replace("转发", "").replace(" ", "")) > 0:
                                transmi_count = int(lis[1].get_text().replace("转发", ""))
                            else:
                                transmi_count = 0
                            if len(lis[2].get_text().replace("评论", "").replace(" ", "")) > 0:
                                comment_count = int(lis[2].get_text().replace("评论", ""))
                            else:
                                comment_count = 0

                            infoObj["transmi_count"] = str(transmi_count)
                            infoObj["comment_count"] = str(comment_count)
                            infoObj["praise_count"] = str(int(comment_count * random.uniform(1, 1.5)))

                            infoObj["lng"] = float(round(
                                RadomGIS.OneGeneratePointInQuadrilateral(RegionnumToGis.get(str(regionnum))[0],
                                                                         RegionnumToGis.get(str(regionnum))[1],
                                                                         RegionnumToGis.get(str(regionnum))[2],
                                                                         RegionnumToGis.get(str(regionnum))[3])[0], 10))
                            infoObj["lat"] = float(round(
                                RadomGIS.OneGeneratePointInQuadrilateral(RegionnumToGis.get(str(regionnum))[0],
                                                                         RegionnumToGis.get(str(regionnum))[1],
                                                                         RegionnumToGis.get(str(regionnum))[2],
                                                                         RegionnumToGis.get(str(regionnum))[3])[1], 10))

                            if infoObj.get('msg_id') != "":
                                print(infoObj)
                                pymsqlDemo.insertDB(infoObj)
                                pass

            else:
                print("抱歉，未找到“北京暴雨”相关结果")
            time.sleep(random.randint(5, 6))
            Start_time = get_next_time(Start_time)
