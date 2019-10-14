import requests
import urllib

SelectCode = "北京大雨"  # 关键字

Regionnum = "4"  # 东城区代码
Start_time = "2012-07-21-2"  # 起始时间
End_time = "2012-07-22-23"  # 结束时间
page = 2

# 将传入的关键字进行两次Encode
def doubleEncode(key):
    try:
        return urllib.parse.quote(urllib.parse.quote(key))
    except Exception:
        return ""


URL = "https://s.weibo.com/weibo/{}?q={}&&region=custom:11:{}&typeall=1&suball=1&timescope=custom:{}:{}&Refer=g".format(
    doubleEncode(SelectCode), SelectCode, Regionnum, Start_time, End_time
)




if __name__ == '__main__':
    url = "https://s.weibo.com/weibo/{}?q={}&&region=custom:11:{}&typeall=1&suball=1&timescope=custom:{}:{}&Refer=g&page={}".format(
        doubleEncode(SelectCode), SelectCode, Regionnum, Start_time, End_time,page
    )
    print(url)
    headers = {
        'Connection': "keep-alive",
        'Upgrade-Insecure-Requests': "1",
        'Sec-Fetch-Mode': "navigate",
        'Sec-Fetch-User': "?1",
        'Sec-Fetch-Site': "same-origin",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
        'Cookie': "SINAGLOBAL=9567883550528.377.1569808672284; login_sid_t=de9791f791e69a37a9b20be943761e17; cross_origin_proto=SSL; _s_tentry=www.baidu.com; Apache=5326827333880.572.1570617980182; ULV=1570617980196:2:1:1:5326827333880.572.1570617980182:1569808672294; SSOLoginState=1570617981; un=chengqigu@wallstreetcn.com; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5yo3qLH_A-Z1xIXjnFVHa35JpX5KMhUgL.Fo-fSKz41hzESKz2dJLoIpRLxK.L1h5L1h.LxKnL1hzLBK2LxK-LB--L1-xW-85t; SUHB=0d4Og_CYjdgbhW; ALF=1602584476; SCF=AlKv9XO_kn5oN9LEpTD5dfRHwvgf9Y6efvgGH20icb--RTuX05srXx2AYecaHBr3z1ZHHjCVmaUzWthTfO3_aTU.; SUB=_2A25woDxPDeRhGeNL7lAY-CzOzj6IHXVT1CqHrDV8PUNbmtBeLWbhkW9NSOkvcodneQeizR2Siw80B7BykN5YyxMj; UOR=www.techug.com,widget.weibo.com,login.sina.com.cn; webim_unReadCount=%7B%22time%22%3A1571048489304%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A97%2C%22msgbox%22%3A0%7D; WBStorage=384d9091c43a87a5|undefined",
        'cache-control': "no-cache",
    }

    response = requests.request("GET", url, headers=headers)

    print(response.text)
