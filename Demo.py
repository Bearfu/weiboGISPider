import requests
import urllib

SelectCode = "北京大雨"  # 关键字

Regionnum = "4"  # 东城区代码
Start_time = "2012-07-21-2"  # 起始时间
End_time = "2012-07-22-23"  # 结束时间
page = 12

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
        doubleEncode(SelectCode), SelectCode, Regionnum, Start_time, End_time, page
    )
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
    url = "https://s.weibo.com/weibo/%25E5%258C%2597%25E4%25BA%25AC%25E5%25A4%25A7%25E9%259B%25A8?q=北京大雨&region=custom:11:1&typeall=1&suball=1&timescope=custom:2012-07-20-10:2012-07-20-20&Refer=g"
    print(url)
    response = requests.request("GET", url, headers=headers)

    print(response.text)
