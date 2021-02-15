import numpy as np
import cv2
import sys
import time
from datetime import datetime


def capture(num,cap):
    t,frame=cap.read()
    frame=cv2.flip(frame, 1)
    if(num==0):
        return frame
    if(num==1):
        return(cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE))
    if(num==2):
        return(cv2.rotate(frame, cv2.ROTATE_180))
    if(num==3):
        return(cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE))

def antirotate(num,frame):
    if(num==0):
        return frame
    if(num==1):
        return(cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE))
    if(num==2):
        return(cv2.rotate(frame, cv2.ROTATE_180))
    if(num==3):
        return(cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE))

    


def time_warp_function(num):
    cap = cv2.VideoCapture(0)
    k=time.time()
    count=0
    i=0
    frame1=capture(num,cap)
    frame2=capture(num,cap)
    frame2=frame2^frame2
    frame2=[220,0,0]|frame2
    size=len(frame2)
    while(i<size):
        frame = capture(num,cap)
        if(time.time()-k<0.1):
            frame1[i]=frame[i]
            i=i+1
        frame[:i]=frame1[:i]
        frame1=frame
        if(i>=size):
            break
        frame[i]=frame2[0]
        cv2.imshow("original",antirotate(num,frame))
        
        if cv2.waitKey(5) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        k=time.time()
    cap.release()
    cv2.destroyAllWindows()
    return antirotate(num,frame1)

def waterfall_function(num):
    print("press 'q' to quit")
    cap = cv2.VideoCapture(0)
    count=0
    frame1=capture(num,cap)
    size=len(frame1)
    start=(5*size)//8
    for i in range(start,size):
        frame1[i]=frame1[start]
        
    cv2.imshow("original",antirotate(num,frame1))
    while(1):
        frame = capture(num,cap)
        frame[start+1:]=frame1[start:-1]
        frame1=frame
        cv2.imshow("original",antirotate(num,frame))
        
        if cv2.waitKey(5) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
    cap.release()
    cv2.destroyAllWindows()
    return antirotate(num,frame1)

def timewarp(mode="v",orientation=-1):
    if( mode!="v" and mode!="h"):
        raise Exception("mode is not defined please enter 'v' or 'h' as mode")
    if( orientation!=-1 and orientation!=1):
        raise Exception("orientation is not defined please enter 1 or -1 as orientation")
    orientation=orientation+1
    if(mode=="h"):
        orientation=orientation+1
    img=time_warp_function(orientation)
    cv2.imshow("timewarp_picture",img)
    return img

def waterfall(mode="v",orientation=-1):
    if( mode!="v" and mode!="h"):
        raise Exception("mode is not defined please enter 'v' or 'h' as mode")
    if( orientation!=-1 and orientation!=1):
        raise Exception("orientation is not defined please enter 1 or -1 as orientation")
    orientation=orientation+1
    if(mode=="h"):
        orientation=orientation+1
    img=waterfall_function(orientation)
    cv2.imshow("waterfall_picture",img)
    return img

def dimension_converter(image):
    thresh=10
    imLeft = image
    imRight=image
    imRight[:,thresh:,0]=imLeft[:,:-thresh,0]
    imRight[:,thresh:,1]=imLeft[:,:-thresh,1]
    imRight=imRight[:,thresh:,:]
    cv2.imshow("3D-Video",imRight)

def Video_3d():
    print("press 'q' to quit")
    cap=cv2.VideoCapture(0)
    while(1):
        t,frame=cap.read()
        frame=cv2.flip(frame, 1)
        dimension_converter(frame)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

timewarp()      
