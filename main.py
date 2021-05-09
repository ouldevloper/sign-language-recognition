# @Author: Абделлах Улахияне
# @Date:   2021-04-17 23:54:50
# @Last Modified by:   Абделлах Улахияне
# @Last Modified time: 2021-04-18 06:52:12
import numpy as np
from keras.models import model_from_json
import operator
import cv2
import sys
import os
import time
from config import *

if not os.path.isdir("modeles") or  \
   not os.path.isfile("modeles/model.json") or  \
   not os.path.isfile("modeles/model.h5"):
        print("Exiting : Training first")
        exit(1)

###############[Loaded model from disk]#####################
# Loading the model
json_file = open("modeles/model.json", "r")
model_json = json_file.read()
json_file.close()
model = model_from_json(model_json)
# load weights into new model
model.load_weights("modeles/model.h5")
print("Loaded model from disk")
###############[end of Loaded model from disk]##############
###############[capture video]##############################
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
        imageToSave = frame[y1:y2+60, x1:x2]
        imageToSave = cv2.resize(imageToSave, image_size)
        grayImage = cv2.cvtColor(imageToSave,cv2.COLOR_RGB2GRAY)
        grayImage = cv2.resize(grayImage,image_size)
        bgrImage = cv2.cvtColor(imageToSave,cv2.COLOR_RGB2BGR)
        bgrImage = cv2.resize(bgrImage,image_size)
        _,black = cv2.threshold(grayImage,80,160,  cv2.THRESH_OTSU)
        
    
        # Batch of 1
        result = model.predict(black.reshape(1,image_size[0], image_size[1],1))
        lst = list(result[0])
        prediction = {v:result[0][k] for k,v in enumerate(sorted(os.listdir("./data/training")))}
        #print(prediction)
        prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
        sorted(prediction)
        
        if list(result[0]).count(1)>0:
                cv2.putText(frame, f"We Got : {prediction[0][0]}", 
                                org, cv2.FONT_HERSHEY_SIMPLEX, 
                                fontScale, color, thickness, cv2.LINE_AA)
                #if list(result[0]).index(1)==0:
                #        cv2.putText(frame, f"We Got : No thing", 
                #                org, cv2.FONT_HERSHEY_SIMPLEX, 
                #                fontScale, color, thickness, cv2.LINE_AA)
                #else:
                #        cv2.putText(frame, f"We Got : {prediction[0][0]}", 
                #                org, cv2.FONT_HERSHEY_SIMPLEX, 
                #                fontScale, color, thickness, cv2.LINE_AA)
        else:
                cv2.putText(frame, f"We Got : No thing", 
                        org, cv2.FONT_HERSHEY_SIMPLEX, 
                        fontScale, color, thickness, cv2.LINE_AA)
        cv2.imshow("Main Video !",frame)
        cv2.imshow("black Video !",black)

        
    interrupt = cv2.waitKey(10)
    if interrupt & 0xFF == 27: # esc key
        break
        
 
capture.release()
cv2.destroyAllWindows()