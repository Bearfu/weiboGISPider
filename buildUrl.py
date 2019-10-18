# coding:utf-8
import urllib
import time
import requests
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
    return datetime.datetime.strptime(str_time, '%Y-%m-%d-%H')


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
    for regionnum in RegionnumList:
        Start_time = "2012-07-20-0"  # 起始时间
        while get_timestamp(Start_time) < get_timestamp('2012-07-30-23'):
            End_time = get_next_time(Start_time)
            url = "https://s.weibo.com/weibo/%25E5%258C%2597%25E4%25BA%25AC%25E5%25A4%25A7%25E9%259B%25A8?q=北京大雨" \
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
                'Cookie': "SINAGLOBAL=9567883550528.377.1569808672284; un=chengqigu@wallstreetcn.com; wvr=6; login_sid_t=c730c63997f8c1fbf6960d47c6ae13f4; cross_origin_proto=SSL; _s_tentry=passport.weibo.com; UOR=www.techug.com,widget.weibo.com,localhost; Apache=7701813525170.181.1571381327292; ULV=1571381327313:3:2:1:7701813525170.181.1571381327292:1570617980196; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5yo3qLH_A-Z1xIXjnFVHa35JpX5K2hUgL.Fo-fSKz41hzESKz2dJLoIpRLxK.L1h5L1h.LxKnL1hzLBK2LxK-LB--L1-xW-85t; SSOLoginState=1571381332; ALF=1602917341; SCF=AlKv9XO_kn5oN9LEpTD5dfRHwvgf9Y6efvgGH20icb--QWYVl8lg65e1raabzxIXO6j6gUS1vobM3F5cDcDwekI.; SUB=_2A25wrRAPDeRhGeNL7lAY-CzOzj6IHXVT2wbHrDV8PUNbmtBeLWr4kW9NSOkvckBPXa-UxJetCyMUkttN_iYm6bxR; SUHB=0102xsCr3dUnQr; webim_unReadCount=%7B%22time%22%3A1571381441666%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A98%2C%22msgbox%22%3A0%7D; WBStorage=384d9091c43a87a5|undefined",
                'Host': "s.weibo.com",
                'cache-control': "no-cache"
            }
            response = requests.request("GET", url, headers=headers)
            infoObj = {
                "msg_id": "",
                "address": RegionnumToName.get(str(regionnum)),
                "content": "",
                "msg_time": Start_time,
                "msg_timestamp": get_datettime(Start_time),
                "tools": "",
                "transmi_count": 0,
                "comment_count": 0,
                "praise_count": 0,

            }
            if "抱歉，未找到“北京大雨”相关结果。" not in response.text:
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
                    # 从a标签中获取用户的ID
                    userInfo = a.find('a')
                    if userInfo:
                        result = re.findall(".*m/(.*)\?.*", userInfo.get('href'))
                        if result:
                            # print("UserId = ", result[0])
                            infoObj["msg_id"] = result[0]
                        # 从class为txt 的P标签中获取用户发布的微博内容
                        txt = a.find('p', 'txt')
                        if txt:
                            # print("Content = ", txt.get_text().replace(" ", "").replace("\n", ""))
                            infoObj["content"] = txt.get_text().replace(" ", "").replace("\n", "")
                        # 从class为from 的P标签中获取用户发布的时间和来源
                        fm = a.find('p', 'from')
                        if fm:
                            fms = fm.get_text().replace(" ", "").split("\xa0")
                            if len(fms) > 1:
                                # print("time = ", fms[0].replace(" ", "").replace("\n", ""))
                                # print("source = ", fms[1].replace(" ", "").replace("\n", ""))
                                infoObj["msg_time"] = fms[0].replace(" ", "").replace("\n", "")
                                # infoObj["msg_timestamp"] = txt.get_text().replace(" ", "").replace("\n", "")
                                infoObj["tools"] = fms[0].replace(" ", "").replace("\n", "")

                        # 从class为card-act 的 div 标签中获取点赞等相关信息
                        card_act = a.find('div', 'card-act')
                        if card_act:
                            ul = card_act.find('ul')
                            lis = ul.find_all('li')
                            # infoObj["transmi_count"] = lis[0].get_text().replace("转发")
                            # infoObj["comment_count"] = lis[1].get_text()
                            # infoObj["praise_count"] = lis[2].get_text()
                            # print("收藏 = ", lis[0].get_text())
                            # print("转发 = ", lis[1].get_text())
                            # print("评论 = ", lis[2].get_text())
                            # print("点赞 = ", lis[3].get_text())
                        if infoObj.get('msg_id') != "":
                            # print(infoObj)
                            pymsqlDemo.insertDB(infoObj)


            else:
                print("抱歉，未找到“北京大雨”相关结果")
            time.sleep(random.randint(5, 10))
            Start_time = get_next_time(Start_time)
