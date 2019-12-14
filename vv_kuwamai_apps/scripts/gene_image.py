#!/usr/bin/python
# -*- coding: utf-8 -*-

#---------------------------------------------------
#Name : gene_image.py
#Author : s-shibata
#Created : 2019 / 10 / 01
#Last Date : 2019 / 11 / 25
#Note : with YusukeKato
#Note : Related to read_master.py and gene_image.py
#---------------------------------------------------

import cv2 as cv
import numpy as np
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import vv_print
import datetime
import rospy
class GenerateImage():
    def __init__(self):
        # image size
        self.height = 707
        self.width = 500

        # setting fonts
        self.fontPath = "~/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"
        #self.fontPath = "~/usr/System/Fonts/ヒラギノ明朝 ProN.ttc"
        self.fontSize_text = 40
        self.fontSize_text_kyoka = 50
        self.textFont = ImageFont.truetype(self.fontPath, self.fontSize_text)
        self.textFont_kyoka = ImageFont.truetype(self.fontPath, self.fontSize_text_kyoka)

        print "--- end init ---"

    def gene_blank_image(self):
        # image array
        blank = np.zeros((self.height, self.width, 3))
        blank += 255

        # generate image
        cv.imwrite('/home/ubuntu/catkin_ws/src/vv_kuwamai/vv_kuwamai_apps/scripts/blank.png', blank)

        print "--- end gene_blank_image ---"

    def write_to_image(self, input_text,count,user_name):
        # read image
        drawImg = Image.open("/home/ubuntu/catkin_ws/src/vv_kuwamai/vv_kuwamai_apps/scripts/blank.png")
        rospy.loginfo("write start")

        # instanse
        draw = ImageDraw.Draw(drawImg)

        # setting line
        h = (self.height / 2) - 150
        leftSide = self.width - (self.width-20)
        rightSide = self.width - 20

        #seal space
        len_input_text = len(input_text)

        # write string
        leftSide_str = self.width - (self.width-40)
        rightSide_str = self.width - 40
        h_str = self.height / 2 + 8

        #sentence_line
        first_line_h = h_str - 120
        second_line_h = h_str - 50
        third_line_h = h_str + 20
        fourth_line_h = h_str + 90
        fifth_line_h = h_str + 160
        width = leftSide_str + 40

        kyoka = u"〜許可証〜"

        draw.text((140, 130), kyoka, fill=(0,0,0), font=self.textFont_kyoka)

        user = user_name + u" 殿"
        draw.text((50, 230), user, fill=(0,0,0), font=self.textFont)

        #count new_line
        n = input_text.count("\n")

        #split new_line
        v = input_text.split("\n")


        draw.ellipse((40, 323, 50, 333), fill=(0, 0, 0), outline=(1, 1, 1))
        draw.text((leftSide_str + 20, second_line_h), v[0][0:11], fill=(0,0,0), font=self.textFont)
        draw.text((leftSide_str + 20, third_line_h), v[0][11:22], fill=(0,0,0), font=self.textFont)

        if len_input_text > 22:
            draw.text((leftSide_str + 20, fourth_line_h), v[0][22:33], fill=(0,0,0), font=self.textFont)
            if len_input_text > 33:
                draw.text((leftSide_str + 20, fifth_line_h), v[0][33:44], fill=(0,0,0), font=self.textFont)

        if len(v) > 1 and len(v[0]) < 11 and len(v[1]) > 3:
            draw.ellipse((40, 393, 50, 413), fill=(0, 0, 0), outline=(1, 1, 1))
            draw.text((leftSide_str + 20, third_line_h), v[1][0:11], fill=(0,0,0), font=self.textFont)
            if len_input_text > 11:
                draw.text((leftSide_str + 20, fourth_line_h), v[1][11:22], fill=(0,0,0), font=self.textFont)
                if len_input_text > 22:
                    draw.text((leftSide_str + 20, fifth_line_h), v[1][22:33], fill=(0,0,0), font=self.textFont)

        sen = u"上記内容を許可します。"
        draw.text((50, 580), sen, fill=(0,0,0), font=self.textFont)
        shomei = u"クワマイ"
        draw.text((260, 660), shomei, fill=(0,0,0), font=self.textFont)
        draw.line((50, 560, 450, 560), fill=(0, 0, 0), width=2)

        # save image
        dt_now = datetime.datetime.now()
        drawImg.save("/home/ubuntu/catkin_ws/src/vv_kuwamai/vv_kuwamai_apps/scripts/data/gene_image" + str(count) + ".jpg")
        print "--- end write_to_image  ---"

if __name__ == '__main__':
    gi = GenerateImage()
    gi.gene_blank_image()
    s="aaa"
    count=1
    user_name="aaa"
    gi.write_to_image(s,count,user_name)
