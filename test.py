import cv2
import numpy as np

# Function to add green circles to detected edges
def add_circles_to_edges(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and help edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use the Canny edge detector
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours in the edges
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw green circles around the contours
    for contour in contours:
        # Ignore small contours (adjust the area threshold as needed)
        if cv2.contourArea(contour) > 0.0:
            # Fit a circle to the contour
            (x, y), radius = cv2.minEnclosingCircle(contour)
            center = (int(x), int(y))
            #radius = int(radius)
            radius = 1
            cv2.circle(frame, center, radius, (0, 255, 0), 2)

# Open video capture
cap = cv2.VideoCapture('drive.mp4')  # Replace 'your_video.mp4' with the path to your video file

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    # Add green circles to detected edges
    add_circles_to_edges(frame)

    # Display the frame
    cv2.imshow('Frame with Circles on Edges', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Release the video capture object and close the window
cap.release()
cv2.destroyAllWindows()

