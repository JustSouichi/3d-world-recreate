import sys 
import os
import cv2
import numpy as np
import pygame
from pygame.locals import *



W = 1920  
H = 1080 

def add_circles_to_edges(frame, circle_list):
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
        circle_list.append((center[0], center[1], radius))

try:
  circle_list = []
  obj_file = []
  video_path = sys.argv[1]
  video_path = "drive.mp4"
  pygame.init()
  display_pygame = (W, H)
  pygame.display.set_mode(display_pygame)
  pygame.display.set_caption("Pygame window")
  if os.path.exists(video_path):
     cap = cv2.VideoCapture(video_path)
     if (cap.isOpened() == False):
        print("No video selected") 
     while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
          #add_circles_to_edges(frame)
          add_circles_to_edges(frame, circle_list)
          cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
          cv2.resizeWindow('Frame', (W, H))
          cv2.imshow('Frame', frame)
          print(frame)
          pygame_screen = pygame.display.get_surface()
          pygame_screen.fill((0, 0, 0))
          circles = []
          gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
          blurred = cv2.GaussianBlur(gray, (5, 5), 0)
          edges = cv2.Canny(blurred, 50, 150)
          contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
          for contour in contours:
            if cv2.contourArea(contour) > 0.0:
              (x, y), radius = cv2.minEnclosingCircle(contour)
              center = (int(x), int(y))
              radius = 1
              circles.append((center[0], center[1], radius))
          pygame_screen = pygame.display.get_surface()
          pygame.fill = ((0, 0, 0))
          for circle in circles:
            x, y, radius = circle
            pygame.draw.circle(pygame_screen, (0, 255, 0), (x, y), radius, 2)
          pygame.display.flip()
          if cv2.waitKey(25) & 0xFF == ord('q'):
            break
          for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                cv2.detroyAllWindows()
                quit()
        else:
          break
     cap.release()
     cv2.destroyAllWindows()
     output_file_path = "circle_data.obj"
     with open(output_file_path, 'w') as obj_file:
      for circle in circle_list:
        x, y, radius = circle
        obj_file.write(f"v {x} {y} 0\n")
        for i in range(32):
          theta = i * (2 * 3.14159) / 32
          obj_file.write(f"v {x + radius * np.cos(theta)} {y + radius * np.sin(theta)} 0\n")
          for i in range(32):
            obj_file.write(f"f {i+1} {i+2} {33}\n")
  else:
    print("error: incorrent video path")
except Exception as e:
  print(e)
except:
 print("error: no path video insert")
