# -*- coding: utf-8 -*-
#!/usr/bin/python

import cv2
import numpy as np

class Capture():
    def cap(self):
        cap = cv2.VideoCapture(0)
        count = 0
        while(True):
            # フレームをキャプチャする
            ret, frame = cap.read()

            # 画面に表示する
            #cv2.imshow('frame',frame)

            # キーボード入力待ち
            key = cv2.waitKey(1) & 0xFF
            count += 1
            # qが押された場合は終了する
            if key == ord('q'):
                break
            # sが押された場合は保存する
            if count % 100 == 0:
                path = "/home/ubuntu/catkin_ws/src/vv_kuwamai/vv_kuwamai_apps/scripts/media_upload/photo.jpg"
                cv2.imwrite(path,frame)
                flag = 1
                return flag
                break
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    gi = Capture()
    gi.cap()
