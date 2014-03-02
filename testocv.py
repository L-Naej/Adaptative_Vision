#!/usr/bin/python

# Face Detection using OpenCV. Based on sample code by Roman Stanchak
# Nirav Patel http://eclecti.cc 5/20/2008

import sys, os
import cv
	
def detectObject(image):
  grayscale = cv.CreateImage(cv.CvSize(640, 480), 8, 1)
  cv.CvtColor(image, grayscale, CV_BGR2GRAY)
  storage = cv.CreateMemStorage(0)
  cv.ClearMemStorage(storage)
  cv.EqualizeHist(grayscale, grayscale)
  cascade = cv.LoadHaarClassifierCascade('haarcascade_frontalface_alt.xml',
                                        cv.CvSize(1,1))
  faces = cv.HaarDetectObjects(grayscale, cascade, storage, 1.2, 2, 
                              CV_HAAR_DO_CANNY_PRUNING, cv.Size(100,100))
  
  if faces:
    for i in faces:
      cv.Rectangle(image, cv.Point( int(i.x), int(i.y)),
                  cv.Point(int(i.x+i.width), int(i.y+i.height)),
                  CV_RGB(0,255,0), 3, 8, 0)
  
def displayObject(image):
  cv.NamedWindow("face", 1)
  cv.ShowImage("face", image)
  cv.WaitKey(0)
  cv.DestroyWindow("face")
  
def main():
  # Uses xawtv. Gstreamer can be used instead, but I found it much slower
  os.system("v4lctl snap jpeg 640x480 face.jpg")
  image = cv.LoadImage("face.jpg")
  detectObject(image)
  displayObject(image)
  cv.SaveImage("face.jpg", image)

if __name__ == "__main__":
  main()