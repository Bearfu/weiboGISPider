from bs4 import BeautifulSoup

path = '/Users/fuzhe/PycharmProjects/weiboGISPider/Demo.html'
htmlfile = open(path, 'r', encoding='utf-8')
htmlhandle = htmlfile.read()

soup = BeautifulSoup(htmlhandle, 'lxml')
con_L = soup.find_all("div", "card-wrap")
for a in con_L:
    userInfo = a.find('a')
    if userInfo:
        print(userInfo.get('href'))
        txt = a.find('p','txt')
        if txt:
            print("content = ", txt.text)
        print("-------------------------------------------------------------------------------------------------------")
