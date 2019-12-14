# coding:utf-8

import printer
from PIL import Image, ImageFilter, ImageOps, ImageChops
import cv2 as cv
import numpy as np
from time import sleep

class VVPrint():
    def test_print(self, image_path):
        # プリンタ準備
        p = printer.ThermalPrinter(heatingDots=0, heatTime=255, heatInterval=255)

        # resize
        img = cv.imread(image_path)
        #ih,iw,ic = img.shape[:3]
        #new_h = ih*(iw/384)
        #img = cv.resize(img,dsize=(384,new_h))
        img = cv.resize(img,dsize=(384,537))
        img = cv.rotate(img, cv.ROTATE_180)
        cv.imwrite("tmp.jpg", img)

        #i = Image.open("tmp.jpg").convert('1')
        i = Image.open("tmp.jpg")

		# edge only
        #i1 = i.convert('L')
        #i2 = i1.filter(ImageFilter.MaxFilter(5))
        #i3 = ImageChops.difference(i1,i2)
        #output_image = ImageOps.invert(i3)

        #i = ImageOps.equalize(i)
        #i = i.convert('1')

        #output_image = i.convert('L')
        output_image = i.convert('1')
        output_image.save("./tmp.jpg")

        data = list(output_image.getdata())
        w, h = output_image.size
        p.set_param()
        p.print_bitmap(data, w, h)

        # 少し紙送り
        p.linefeed(3)


if __name__ == '__main__':
	vp = VVPrint()
	#image_path = "./gene_image1.png"
	#image_path = "./data1/gene_image2019-11-25 06:58:51.341539.jpg"
	#image_path = "./data1/test_image.jpg"
	image_path = "./data1/gene_image.jpg"
	#image_path = "./Astronaut_scaled.jpg"
	vp.test_print(image_path)
