#!/usr/bin/env python
# coding: utf-8
import json
from requests_oauthlib import OAuth1Session
import camera
import cv2 as cv
import time
import keys

import rospy
from std_srvs.srv import Empty
from std_srvs.srv import EmptyResponse

#API認証
CK = keys.CK
CS = keys.CS
AT = keys.AT
ATS = keys.ATS

#API取得
url_media = "https://upload.twitter.com/1.1/media/upload.json"
url_text = "https://api.twitter.com/1.1/statuses/update.json"

# OAuth認証 セッションを開始
twitter = OAuth1Session(CK, CS, AT, ATS)

class Upload():

    def handle_service(self, req):
        rospy.loginfo("Upload to Twitter!")
        # カメラから写真を取得
        rospy.loginfo("camera!")
        gi = camera.Capture()
        gi.cap()
        # 休憩
        rospy.loginfo("kyuukei!")
        time.sleep(2.0)
        # アップロード
        rospy.loginfo("upload!")
        self.Up()
        # 空を返す
        #return EmptyResponse()

    def service_server(self):
        rospy.init_node('service_server')
        self.s = rospy.Service('call_me', Empty, self.handle_service)
        print "Ready to serve."
        rospy.spin()

    def Up(self):
        image_path = '/home/ubuntu/catkin_ws/src/vv_kuwamai/vv_kuwamai_apps/scripts/media_upload/photo.jpg'
        img = cv.imread(image_path)
        img = cv.rotate(img, cv.ROTATE_90_COUNTERCLOCKWISE)
        cv.imwrite("/home/ubuntu/catkin_ws/src/vv_kuwamai/vv_kuwamai_apps/scripts/media_upload/photo.jpg", img)
        # 画像投稿
        files = {"media" : open('/home/ubuntu/catkin_ws/src/vv_kuwamai/vv_kuwamai_apps/scripts/media_upload/photo.jpg', 'rb')}
        req_media = twitter.post(url_media, files = files)

        # レスポンスを確認
        if req_media.status_code != 200:
            print "画像アップロード失敗: %s", req_media.text
            exit()

        # Media ID を取得
        media_id = json.loads(req_media.text)['media_id']
        print "Media ID: %d" % media_id

        # Media ID を付加してテキストを投稿
        params = {'status': '#vv_print', "media_ids": [media_id]}
        req_media = twitter.post(url_text, params = params)

        # 再びレスポンスを確認
        if req_media.status_code != 200:
            print "テキストアップロード失敗: %s", req_text.text
            exit()
        print ("OK")

if __name__ == '__main__':
    ul = Upload()
    ul.service_server()
