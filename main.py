import sys 
import os
import cv2
import numpy as np

def add_circles_to_edges(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
      if cv2.contourArea(contour) > 0.0:
        (x, y), radius = cv2.minEnclosingCircle(contour)
        center = (int(x), int(y))
        radius = 1
        cv2.circle(frame, center, radius, (0, 255, 0), 2)

try:
  video_path = sys.argv[1]
  video_path = "drive.mp4"
  if os.path.exists(video_path):
     cap = cv2.VideoCapture(video_path)
     if (cap.isOpened() == False):
        print("No video selected") 
     while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
          W = 700
          H = 400
          add_circles_to_edges(frame)
          cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
          cv2.resizeWindow('Frame', (W, H))
          cv2.imshow('Frame', frame)
          if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        else:
          break
     cap.release()
     cv2.destroyAllWindows()
  else:
    print("error: incorrent video path")
except:
 print("error: no path video insert")
