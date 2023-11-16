import cv2
import numpy as np
import pygame
from pygame.locals import *

# Open video capture
cap = cv2.VideoCapture('drive.mp4')  # Replace 'your_video.mp4' with the path to your video file

# Initialize Pygame
pygame.init()

# Set up Pygame window for green circle display
display_pygame = (800, 600)
pygame.display.set_mode(display_pygame)
pygame.display.set_caption("Pygame Window")

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

    # Display green circles using OpenCV
    for circle in circles:
        x, y, radius = circle
        cv2.circle(frame, (x, y), radius, (0, 255, 0), 2)

    # Display the frame with circles using OpenCV
    cv2.imshow('Frame with Circles', frame)

    # Display green circles using Pygame
    pygame_screen = pygame.display.get_surface()
    pygame_screen.fill((0, 0, 0))  # Clear the screen
    for circle in circles:
        x, y, radius = circle
        pygame.draw.circle(pygame_screen, (0, 255, 0), (x, y), radius, 2)

    pygame.display.flip()

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

# Release the video capture object
cap.release()
cv2.destroyAllWindows()

