import sys 
import os
import cv2
import numpy as np
import pygame
from pygame.locals import *

W = 1920  
H = 1080 

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
    video_path = "drive.mp4"  # Assuming you want to use the default video path
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
                add_circles_to_edges(frame)
                cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
                cv2.resizeWindow('Frame', (W, H))
                cv2.imshow('Frame', frame)
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
                
                # Calculate the maximum radius to determine the scaling factor
                max_radius = max(circle[2] for circle in circles)
                scaling_factor = min(W / (2 * max_radius), H / (2 * max_radius))
                
                # Draw circles on the scaled Pygame window
                for circle in circles:
                    x, y, radius = circle
                    scaled_radius = int(radius * scaling_factor)
                    pygame.draw.circle(pygame_screen, (0, 255, 0), (int(x * scaling_factor), int(y * scaling_factor)), scaled_radius, 2)
                
                pygame.display.flip()
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        cap.release()
                        pygame.quit()
                        cv2.destroyAllWindows()
                        quit()
            else:
                break
        cap.release()
        cv2.destroyAllWindows()
    else:
        print("error: incorrect video path")
except Exception as e:
    print(e)
except:
    print("error: no video path inserted")

