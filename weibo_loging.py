# coding: utf-8
import base64
import random
import re
import requests
import rsa
import time
import urllib
import binascii
from vc import Chaoren
from config import get_mysql_connection
import logging


class WeiboLogin(object):

    def __init__(self, username, password):
        self.s = requests.Session()
        self.username = username
        self.password = password
        self.passport_headers = {
            "Referer": "https://weibo.com/",
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:64.0) Gecko/20100101 Firefox/64.0',
        }

    # 获取cookie
    def get_cookie(self):
        # self.s.cookies是CookieJar的类型，进行解包得到cookie字符串
        cookie = ""
        for c in self.s.cookies:
            cookie = cookie + c.name + "=" + c.value + "; "
        return cookie

    # 在输入用户名的时候又一次加载，对用户名加密，且返回相关的参数
    def login_ago(self):
        _ = time.time() * 1000
        su = base64.b64encode(urllib.request.quote(self.username).encode())
        params = {
            'entry': 'weibo',
            # 'callback': 'sinaSSOController.preloginCallBack',
            'su': su,
            'rsakt': 'mod',
            'client': 'ssologin.js(v1.4.19)',
            '_': _
        }
        url = "https://login.sina.com.cn/sso/prelogin.php"
        web_data = self.s.get(url, params=params)

        js_web_data = web_data.json()

        # 输入用户名之后就会弹出验证码
        #  添加验证码操作
        v_url = "https://login.sina.com.cn/cgi/pin.php?r={0}&s=0&p={1}".format(str(random.randint(1000000, 99999999)),
                                                                               js_web_data.get("pcid"))
        r = requests.get(v_url, headers=self.passport_headers)
        with open("v.jpg", "wb") as f:
            f.write(r.content)
        # 请求验证码打码平台
        cr = Chaoren()
        js_web_data['cap'] = cr.get_captcha()
        return js_web_data

    # 带着所有的参数进行登录
    def login(self, username):
        data = self.login_ago()
        cap = data['cap']

        servertime = data['servertime']
        nonce = data['nonce']
        pubkey = data['pubkey']  # 用来生成sp
        rsakv = data['rsakv']

        pcid = data['pcid']
        su = base64.b64encode(urllib.request.quote(self.username).encode())
        message_password = str(servertime) + "\t" + str(nonce) + "\n" + str(self.password)
        # 生成sp
        rsapubkey = int(pubkey, 16)
        key = rsa.PublicKey(rsapubkey, 65537)
        sp = binascii.b2a_hex(rsa.encrypt(message_password.encode('utf-8'), key))
        post_data = {

            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'qrcode_flag': 'false',
            'useticket': '1',
            'pagerefer': '',

            "wsseretry": "servertime_error",
            "pcid": pcid,
            "door": cap,

            'vsnf': '1',
            'su': su,
            'service': 'miniblog',
            'servertime': servertime,
            'nonce': nonce,
            'pwencode': 'rsa2',
            'rsakv': rsakv,
            'sp': sp,
            'sr': '1440 * 900',
            'encoding': 'UTF-8',
            'prelt': '42',
            'url': 'https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META',
        }

        # 在登陆的时候，会重定向进行新浪通行验证
        url_login_php = "https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)&_=" + str(
            time.time() * 1000)
        web_data = self.s.post(url_login_php, data=post_data, headers=self.passport_headers)
        # print(web_data.content.decode('GBK'))

        # 这里才是最终的登陆入口
        try:
            redirect_url1 = re.search('location.replace\("(.*?)"\);', web_data.text, re.S).group(1)
            redirect_login1 = self.s.get(redirect_url1, headers=self.passport_headers)

            redirect_url2 = re.search("location.replace\('(.*?)'\);", redirect_login1.text).group(1)
            self.s.get(redirect_url2, headers=self.passport_headers)
            print("=" * 20 + username + "=" * 20 + "模拟登陆成功: " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            return self.get_cookie(), username
        except:
            self.login(username)

    def update_cookie(self, username, cookie):
        conn = get_mysql_connection()
        update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        with conn.cursor() as cursor:
            sql = "update weibo_cookie set cookie='%s', update_time='%s' where username='%s'" % (
            cookie, update_time, username)
            cursor.execute(sql)
            conn.commit()


if __name__ == "__main__":
    username = "18516315182"
    password = "kankan185"
    weibo = WeiboLogin(username, password)

    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)

    while True:
        print("更新cookie: ")
        try:
            cookie, username = weibo.login(username)
            logger.warning(cookie)
            weibo.update_cookie(username, cookie)
            print("更新完成")
        except:
            cookie, username = weibo.login(username)
            logger.warning(cookie)
            weibo.update_cookie(username, cookie)
            print("更新完成")
        time.sleep(15 * 60)
