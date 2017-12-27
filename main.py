# -*- coding:utf-8 -*-

from settings import *
import sys
import requests
from requests.auth import HTTPBasicAuth

reload(sys)
sys.setdefaultencoding('utf-8')
COOKIE = None

global NAME
global PASSWORD
global GITNAME
global GITPASSWORD


class Gitstar():
    def __init__(self, name, password, git_name, git_password):
        self.NAME = name
        self.PASSWORD = password
        self.GITNAME = git_name
        self.GITPASSWORD = git_password

        self.cookie = None

    def login_gitstar(self):
        r = requests.post("http://gitstar.top:88/api/user/login",
                          params={'username': self.NAME, 'password': self.PASSWORD})
        self.cookie = r.headers['Set-Cookie']

    def get_gitstar_follow_recommend(self):
        self.login_gitstar()
        url = "http://gitstar.top:88/api/users/%s/status/follow-recommend" % self.NAME
        response = requests.get(url, headers={'Accept': 'application/json', 'Cookie': self.cookie})
        jsn = response.json()
        list = []
        for obj in jsn:
            list.append(obj['User'])
        return list

    def follow(self, url):
        AUTH = HTTPBasicAuth(self.GITNAME, self.GITPASSWORD)
        requests.put("https://api.github.com/user/following/" + url
                     , headers={'Content-Length': '0'}
                     , auth=AUTH)

    def update_gitstar(self):
        url = "http://gitstar.top:88/follow_update"
        res = requests.get(url, headers={'Accept': 'application/json', 'Cookie': self.cookie})
        print "update:" + str(res.status_code == 200)


G = Gitstar(NAME, PASSWORD, GITNAME, GITPASSWORD)
FollowList = G.get_gitstar_follow_recommend()
t = len(FollowList)
print "need follow : %d" % t
i = 1
for url in FollowList:
    G.follow(url)
    print "[%d/%d]Followed! -->%s" % (i, t, url)
    i = i + 1

if t > 0:
    G.update_gitstar()
