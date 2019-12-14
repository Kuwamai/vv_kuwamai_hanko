#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import sys
from requests_oauthlib import OAuth1Session
import keys

#API認証情報
CK = keys.CK
CS = keys.CS
AT = keys.AT
ATS = keys.ATS
# OAuth認証 セッションを開始
twitter = OAuth1Session(CK, CS, AT, ATS)
#API取得
#url = "https://api.twitter.com/1.1/statuses/update.json"
search = "https://api.twitter.com/1.1/search/tweets.json"
#TL = "https://api.twitter.com/1.1/statuses/user_timeline.json"

num = 1
print "---------------------------------------"
keyword = u"#vv_kuwamai"
params = {'q' : keyword, 'count' : num}
req = twitter.get(search, params = params)


if req.status_code == 200:
    search_timeline = json.loads(req.text)
    print len(search_timeline['statuses'])
    for tweet in search_timeline['statuses']:
        print tweet['user']['name']+'::'+tweet['text']
        print tweet['created_at']
        print '----------------------------------------------------'
else:
    print "ERROR: %d" % req.status_code
