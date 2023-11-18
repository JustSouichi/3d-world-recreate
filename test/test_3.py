import cv2
import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Function to draw green circles in 3D using PyOpenGL
def draw_green_circles_3d(circles):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluPerspective(45, (display_pygame[0] / display_pygame[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    for circle in circles:
        x, y, radius = circle
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(0, 1, 0)  # Green color
        for i in range(100):
            theta = 2.0 * np.pi * float(i) / float(100)
            dx = radius * np.cos(theta)
            dy = radius * np.sin(theta)
            glVertex3f(x + dx, y + dy, 0)
        glEnd()

    pygame.display.flip()

# Open video capture
cap = cv2.VideoCapture('drive.mp4')  # Replace 'your_video.mp4' with the path to your video file

# Initialize Pygame
pygame.init()

# Set up Pygame window for 3D green circle display
display_pygame = (800, 600)
pygame.display.set_mode(display_pygame, DOUBLEBUF | OPENGL)
pygame.display.set_caption("3D Pygame Window")

gluPerspective(45, (display_pygame[0] / display_pygame[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and help edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use the Canny edge detector
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours in the edges
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Extract the centers and radii of circles from contours
    circles = []
    for contour in contours:
        if cv2.contourArea(contour) > 10:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            center = (int(x), int(y))
            radius = max(1, int(radius) - 2)
            circles.append((center[0], center[1], radius))

    # Display green circles in 3D using PyOpenGL
    draw_green_circles_3d(circles)

    # Display the frame with circles using OpenCV
    cv2.imshow('Frame with Circles', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

    # Handle Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            pygame.quit()
            cv2.destroyAllWindows()
            quit()

pygame.quit()
cv2.destroyAllWindows()

