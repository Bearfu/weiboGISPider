import  requests
source_url = "https://s.weibo.com/weibo/%E5%8C%97%E4%BA%AC%E5%A4%A7%E9%9B%A8?q=%E5%8C%97%E4%BA%AC%E6%9A%B4%E9%9B%A8&region=custom:11:6&typeall=1&haslink=1&timescope=custom:2012-07-01-0:2012-08-11-16&Refer=g&page=2"
url = "http://t.cn/zWK0sZW"
response = requests.request("GET", url)
print(response.headers)
print(response.headers['Set-Cookie'])



# 这一串里面有真实的经纬度 你看一下逻辑 怎么取出来
"M_WEIBOCN_PARAMS=fid%3D100101116.26561_39.882278%26uicode%3D10000011"
