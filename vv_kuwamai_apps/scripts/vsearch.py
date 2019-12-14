#/usr/bin/python
# -*- coding: utf-8 -*-

#---------------------------------------------------
#Name : vsearch.py
#Author : s-shibata
#Created : 2019 / 10 / 01
#Last Date : 2019 / 11 / 25
#Note : Related to read_master.py and gene_image.py
#---------------------------------------------------

import os
import shutil
import json
import sys
import gene_image
from requests_oauthlib import OAuth1Session
from hashlib import md5
import datetime
import vv_print
import keys
import rospy

tweet_text = []
sto = []

class Search():
    def kuwamai(self):

        gi = gene_image.GenerateImage()
        gi.gene_blank_image()

        #API認証情報
        CK = keys.CK
        CS = keys.CS
        AT = keys.AT
        ATS = keys.ATS
        twitter = OAuth1Session(CK,CS,AT,ATS)
        #API取得
        search = "https://api.twitter.com/1.1/search/tweets.json"

        def md5hex(str):
            a = md5()
            a.update(str)
            print a
            return a.hexdigest()

        folder = '/home/ubuntu/catkin_ws/src/vv_kuwamai/vv_kuwamai_apps/scripts/data/'
        path = os.path.exists(folder)

        if not path:
            os.mkdir(folder)

        #number aquire
        num = 1

        path_w = '/home/ubuntu/catkin_ws/src/vv_kuwamai/vv_kuwamai_apps/scripts/memory.txt'

        print "---------------------------------------"

        #serch keyword
        keyword = "#vv_kuwamai"
        params = {'q' : keyword, 'count' : num}
        req = twitter.get(search, params = params)
        flag = 0
        flg = 0
        count = 1
        if req.status_code == 200:
            search_timeline = json.loads(req.content)
            rospy.loginfo("search_timeline")
            rospy.loginfo(len(search_timeline['statuses']))
            #timeline search
            for tweet in search_timeline['statuses']:
                with open(path_w) as f:
                    line = str(f.readlines())
                    print line

                if str(tweet['id']) in line:
                    rospy.loginfo("same tweet")
                    rospy.loginfo(tweet['id'])
                    break
                    rospy.loginfo("not break0")
                #if it was media
                rospy.loginfo("not break1")
                user_name = tweet['user']['name'].encode('utf-8').decode('utf-8')
                if 'media' in tweet['entities']:
                    sto.append(tweet['id'])
                    urls = tweet['entities']['media']
                    media_urls = urls[0]['media_url']
                    downloads = twitter.get(media_urls).content
                    print "\r" + media_urls + " " + str([count])
                    flag += 1
                #if it was sentence
                else:
                    rospy.loginfo("test1")
                    sto.append(tweet['id'])
                    #print sto
                    #print tweet['user']['name']
                    #user_name = tweet['user']['name']
                    a = tweet['text']

                    #encode to utf-8
                    c = a.encode('utf-8').decode('utf-8')
                    #cut "#vv_kuwamai"
                    d = c[:-12]

                    rospy.loginfo("vsearch test")

                    #rospy.loginfo(d)
                    tweet_text.append(d)
                    flag += 1
                    #pass d and flag to gene_image/write_to_image
                    gi.write_to_image(d,flag,user_name)
                    print tweet['created_at']
                    print '----------------------------------------------------'
                    with open(path_w, mode='a') as f:
                        f.write(str(sto))
                        rospy.loginfo("add")
                    continue
                #dt_now = datetime.datetime.now()
                #filename = 'gene_image' +  str(dt_now) + '.jpg'# % md5hex(urls[0]['media_url'])
                filename = 'gene_image' +  str(flg) + '.jpg'# % md5hex(urls[0]['media_url'])
                filepath = '%s/%s' % (folder, filename)
                images = open(filepath, 'wb')
                #save image
                images.write(downloads)
                #vp = vv_print.VVPrint()
                #vp.test_print(filepath)
                print filepath
                images.close()
                #new_path = shutil.move('/Users/shiba/vv_kuwamai1/data/' + filename, '/Users/shiba/vv_kuwamai1/data1')
                count += 1
                flg += 1
                #return filepath
                with open(path_w, mode='a') as f:
                    f.write(str(sto))
                    rospy.loginfo("add sto")

        else:
            print "ERROR: %d" % req.status_code
        print sto
if __name__ == '__main__':
    Search().kuwamai()
