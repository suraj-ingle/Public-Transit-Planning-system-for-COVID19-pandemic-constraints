# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 16:25:13 2020

@author: DELL
"""


import cv2
import sys


bodyCascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
video_capture = cv2.VideoCapture("bus.mp4")


total_frames = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
print(total_frames)


pre_frame = 0;
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    body = bodyCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
      
    )
    
    for (x, y, w, h) in body:
        
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cur = video_capture.get(cv2.CAP_PROP_POS_FRAMES);
        tt_inframe = cur - pre_frame;
        print(f'toatal time object in frame: {tt_inframe}')
        print(cur)
        pre_frame = cur
       
    
    
    cv2.imshow('Video', frame)
    
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


video_capture.release()
cv2.destroyAllWindows()
