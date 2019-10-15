from bs4 import BeautifulSoup
import re

# BeautifulSoup 文档地址
# https://beautifulsoup.readthedocs.io/zh_CN/v4.4.0/#id28

path = '/Users/fuzhe/PycharmProjects/weiboGISPider/Demo.html'
htmlfile = open(path, 'r', encoding='utf-8')
htmlhandle = htmlfile.read()
# html文件转为SOUP对象
soup = BeautifulSoup(htmlhandle, 'lxml')
# 获取用户微博列表
con_L = soup.find_all("div", "card-wrap")
# 轮询列表中的微博
for a in con_L:
    # 从a标签中获取用户的ID
    userInfo = a.find('a')
    if userInfo:
        result = re.findall(".*m/(.*)\?.*", userInfo.get('href'))
        if result:
            print("UserId = ", result[0])
        # 从class为txt 的P标签中获取用户发布的微博内容
        txt = a.find('p', 'txt')
        if txt:
            print("Content = ", txt.get_text().replace(" ", "").replace("\n", ""))
        # 从class为from 的P标签中获取用户发布的时间和来源
        fm = a.find('p', 'from')
        if fm:
            fms = fm.get_text().replace(" ", "").split("\xa0")
            if len(fms) > 1:
                print("time = ", fms[0].replace(" ", "").replace("\n", ""))
                print("source = ", fms[1].replace(" ", "").replace("\n", ""))
        # 从class为card-act 的 div 标签中获取点赞等相关信息
        card_act = a.find('div','card-act')
        if card_act:
            ul = card_act.find('ul')
            lis = ul.find_all('li')
            print("收藏 = ", lis[0].get_text())
            print("转发 = ", lis[1].get_text())
            print("评论 = ", lis[2].get_text())
            print("点赞 = ", lis[3].get_text())

        print("-------------------------------------------------------------------------------------------------------")
