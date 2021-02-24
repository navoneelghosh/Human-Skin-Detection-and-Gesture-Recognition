#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 23:16:00 2021

"""
import cv2
import numpy as np
import sys, os
import glob
# import imutils
from VideoGet import VideoGet
from VideoShow import VideoShow
import time


#Skin Detection using HSV color space
# Returns the detected skin frame
def skinDetectionHSV(img):
    '''
    Parameters
    ----------
    img: color image
    '''
    image = np.array(img)
    imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    skinMaskHSV = cv2.bitwise_or((cv2.inRange(imageHSV, (0, 25, 80), (50, 255, 255))),(cv2.inRange(imageHSV, (150, 25, 80), (255, 255, 255))))
    skinHSV = cv2.bitwise_and(image, image, mask = skinMaskHSV)
    return skinHSV

def matchTemplate(img, templates, titles, method=cv2.TM_CCORR_NORMED):
    ''' 
    Parameters
    ----------
    img : grayscale image
    template : grayscale image
    method: matching method, an integer, 
            'cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED'

    Returns
    -------
    bounding box.

    '''

    found = None
    # loop over the scales of the image
    for scale in np.linspace(0.2, 1.0, 20)[::-1]:
        resized = cv2.resize(img, (int(img.shape[1] * scale),int(img.shape[0] * scale)))
        r = img.shape[1] / float(resized.shape[1])
        # edged = cv2.Canny(resized, 40, 90)
        edged=resized
        # cv2.imshow('frame', edged)
        for template, t in zip(templates,titles):
            tH, tW = template.shape[:2]
            if resized.shape[0] < tH or resized.shape[1] < tW:
                break
            # cv2.imshow("Template", template)

            result = cv2.matchTemplate(edged, template, method)
            (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
            # if we have found a new maximum correlation value, then update
            # the bookkeeping variable
            if found is None or maxVal > found[0]:
                found = (maxVal, maxLoc, r, t)
            
 	# unpack the bookkeeping variable and compute the (x, y) coordinates
 	# of the bounding box based on the resized ratio
    (maxVal, maxLoc, r, t) = found
    (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
    (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
    
    return maxVal, t, startX, startY, endX, endY



if __name__ == "__main__":
    
    # read templates from folder
    templates = glob.glob("templates/*.png")

    # templates_gray = [ cv2.Canny(cv2.imread(template,0), 40,90) for template in templates ]
    templates_gray = [cv2.imread(template, 0) for template in templates]
    names = [(name.split("/")[-1]).split(".")[0] for name in templates]
    # for n,t in zip(names,templates_gray):
    #     cv2.imshow(n,t)
    # print([tplt.shape for tplt in templates_gray])

    # cap = cv2.VideoCapture(0)
    # # if not successful, exit program
    # if not cap.isOpened():
    #     print("Cannot open the video cam")
    #     sys.exit()
    
    fW = 640
    fH = 480
    video_getter = VideoGet(0,fW,fH).start()
    # video_shower = VideoShow(video_getter.frame).start()
    
    cv2.namedWindow("MyVideo", cv2.WINDOW_AUTOSIZE)
    fgbg = cv2.createBackgroundSubtractorKNN()
    
    fourcc = cv2.VideoWriter_fourcc(*'MPEG')
    out = cv2.VideoWriter('output.avi', fourcc, 9.0, (640, 480))

    while(True):
        start = int(round(time.time() * 1000))
        # # Capture frame-by-frame
        # ret, frame = cap.read()
        # if not ret:
        #     print("Cannot read a frame from video stream")
        #     break
        
        frame = video_getter.frame
        # frame = cv2.resize(frame, (0,0), fx=0.8, fy=0.8)
        # video_shower.frame = frameq
        
        fgmask = fgbg.apply(frame)
        fgmask = cv2.medianBlur(fgmask, 3)
        fgmask = cv2.blur(fgmask,(3,3))
        fgmask = cv2.dilate(fgmask,np.ones((7,7)))
        fgmask = ((fgmask>0)*255).astype(np.uint8)
        skinMatching = skinDetectionHSV(frame)
        skinMatching = cv2.medianBlur(skinMatching,5)
        skinMatching = cv2.cvtColor(skinMatching, cv2.COLOR_BGR2GRAY)
        skinMatching = ((skinMatching>0)*255).astype(np.uint8)
        fgmask = cv2.bitwise_and(skinMatching,fgmask)
        # fgmask = cv2.blur(fgmask,(5,5))
        tt = np.zeros_like(fgmask)
        contours, hierarchy = cv2.findContours(fgmask,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours)!=0:
            maxCont = max(contours, key=cv2.contourArea)
            blankImage=np.zeros_like(fgmask)
            cv2.drawContours(blankImage,[maxCont],-1,(255,255,255),thickness=cv2.FILLED)
            maxVal,name,startX,startY,endX,endY = matchTemplate(blankImage,templates_gray,names)
            print(maxVal,name,startX,startY,endX,endY)
            if maxVal > 0.7:
                box = [(startX, startY), (endX, endY)]
                cv2.putText(frame,name,(40,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
                cv2.rectangle(frame,box[0],box[1],(255,255,255),2)
                # cv2.imshow("mask", blankImage)
                idx = names.index(name)
                fH, fW = fgmask.shape[:2]
                tH, tW = templates_gray[idx].shape[:2]
                tt = cv2.copyMakeBorder(templates_gray[idx], 50, fH-tH-50, 50, fW-tW-50, cv2.BORDER_CONSTANT,value=0)
            v_comb = np.vstack([blankImage, tt])
        else:
            v_comb = np.vstack([fgmask, tt])
        # cv2.imshow('merged', fgmask)
        v_comb = cv2.resize(v_comb, (0,0), fx=0.5, fy=0.5)
        v_comb = cv2.cvtColor(v_comb, cv2.COLOR_GRAY2BGR)
        combined = np.hstack([frame, v_comb])
        
        cv2.imshow("MyVideo", combined)
        # video_shower.frame = combined
        out.write(frame)
        end=int(round(time.time() * 1000)) - start
        print("FPS=",(1000.0/end))
        if cv2.waitKey(1) & 0xFF == ord('q') or video_getter.stopped:
            video_getter.stop()
            # video_shower.stop()
            cv2.imwrite('skinDetection.png', blankImage)
            break
    

    # When everything done, release the capture
    cv2.destroyAllWindows()


