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

    # Use HoughCircles to detect circles in the edges
    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=50, param2=30, minRadius=10, maxRadius=50)

    if circles is not None:
        # Convert circle coordinates to integer
        circles = np.round(circles[0, :]).astype("int")

        # Draw green circles around the detected edges
        for (x, y, r) in circles:
            cv2.circle(frame, (x, y), r, (0, 255, 0), 4)

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

