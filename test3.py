import sys
import os
import cv2

W = 1920
H = 1080

circle_data = []  # List to store circle information [(x, y, radius), ...]

def add_circles_to_edges(frame):
    global circle_data
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
            circle_data.append((center[0], center[1], radius))

def export_to_obj(file_path):
    with open(file_path, 'w') as file:
        for circle in circle_data:
            x, y, radius = circle
            file.write(f"v {x} {y} 0\n")

try:
    video_path = sys.argv[1]
    video_path = "drive.mp4"
    if os.path.exists(video_path):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("No video selected")
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                add_circles_to_edges(frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()

        # Export circle data to obj file
        export_to_obj('circle_data.obj')

    else:
        print("error: incorrect video path")
except Exception as e:
    print(e)
except:
    print("error: no video path inserted")

