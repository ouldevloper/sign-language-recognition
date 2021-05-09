# @Author: Абделлах Улахияне
# @Date:   2021-03-30 14:22:33
# @Last Modified by:   Абделлах Улахияне
# @Last Modified time: 2021-04-18 23:12:58

import numpy as np
import cv2
import imutils
import os
import sys
import signal
import threading
from threading import Thread
from random import randint


path       = "data/training"  
validation = "data/validation"  
testing    = "data/testing"

classname    = []
classnamestr = []
tmp=False

os.mkdir("data/") if not os.path.isdir("data/") else print(end="")
os.mkdir(path) if not os.path.isdir(path) else print(end="")
os.mkdir(validation) if not os.path.isdir(validation) else print(end="")
os.mkdir(testing) if not os.path.isdir(testing) else print(end="")


capture = cv2.VideoCapture(0)
while capture.isOpened():
    isCaptured, frame = capture.read()
    if isCaptured:
        frame = cv2.flip(frame,1)
        frame = cv2.resize(frame,(920,620))
        x1 = int(0.5*frame.shape[1])
        y1 = 10
        x2 = frame.shape[1]-10
        y2 = int(0.5*frame.shape[1])
        #drow cyrcle on targeted Image
        #cv2.rectangle(frame, (x1-1, y1-1), (x2-1, y2+100), (0,0,0) ,1)
        #Exctract Image from Main Video
        imageToSave = frame[y1:y2+60, x1:x2]
        imageToSave = cv2.resize(imageToSave, (200, 200))
        #Convert Image To GRAY
        grayImage = cv2.cvtColor(imageToSave,cv2.COLOR_RGB2GRAY)
        grayImage = cv2.resize(grayImage,(200,200))
        #Convert Iage To BGR
        bgrImage = cv2.cvtColor(imageToSave,cv2.COLOR_RGB2BGR)
        bgrImage = cv2.resize(bgrImage,(200,200))

        thresh,black = cv2.threshold(grayImage,80,160,  cv2.THRESH_OTSU)
        cv2.imshow("Main Video !",frame)
        cv2.imshow("black Video !",black)
        #cv2.imshow("Original Image To Save for Training!",imageToSave)
        #cv2.imshow("Gray Image To Save for Training!",grayImage)
        #cv2.imshow("BGR Image To Save for Training!",bgrImage)
        
        key = cv2.waitKey(1)
        if key == 27:
            break    
        else:
            if key != -1:
                if tmp == True:
                    if key == 13:
                        print("Save Photos for this new classname : ",classnamestr)
                        fullpath = f"{path}{os.sep}{classnamestr}"
                        if not os.path.isdir(fullpath):
                            os.mkdir(fullpath)
                        if not os.path.isdir(f"{testing}{os.sep}{classnamestr}"):
                            os.mkdir(f"{testing}{os.sep}{classnamestr}")
                           
                        filename = f"{classnamestr}_{randint(999999999,999999999999999999)}.png"
                        while filename  in os.listdir(fullpath):
                            filename = f"{classnamestr}_{randint(999999999,999999999999999999)}.png"
                        cv2.imwrite(f"{fullpath}{os.sep}{filename}",black)
                        #filename = f"{classnamestr}_{randint(999999999,999999999999999999)}.png"
                        #while filename  in os.listdir(fullpath):
                        #    filename = f"{classnamestr}_{randint(999999999,999999999999999999)}.png"
                        #cv2.imwrite(f"{fullpath}{os.sep}{filename}",imageToSave)
                        #filename = f"{classnamestr}_{randint(999999999,999999999999999999)}.png"
                        #while filename  in os.listdir(fullpath):
                        #    filename = f"{classnamestr}_{randint(999999999,999999999999999999)}.png"
                        #cv2.imwrite(f"{fullpath}{os.sep}{filename}",grayImage)
                        #filename = f"{classnamestr}_{randint(999999999,999999999999999999)}.png"
                        #while filename  in os.listdir(fullpath):
                        #    filename = f"{classnamestr}_{randint(999999999,999999999999999999)}.png"
                        #cv2.imwrite(f"{fullpath}{os.sep}{filename}",bgrImage)
                    else:
                        tmp=False
                        classname=[]
                elif len(classname)>0:
                    if  key == 13:
                        print("Generate New Photo classname : ","".join(list(map(lambda x:chr(x) if x>0 else "",classname))))
                        classnamestr = "".join(list(map(lambda x:chr(x) if x>0 else "",classname)))
                        classname=list()
                        tmp=True
                    else:
                        classname.append(key)
                else:
                    if key  != 13:
                        classname.append(key)
    else:
        break
                   
capture.release()
cv2.destroyAllWindows()


