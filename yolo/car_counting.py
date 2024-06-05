import cv2
from ultralytics import YOLO, solutions

model = YOLO("model/yolov8n.pt")
cap = cv2.VideoCapture("data/car_1.mp4")
assert cap.isOpened(), "Error reading video file"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

print(w,h)
# Define line points
line_pts = [(0, 800), (1920, 800)]

region_points = [(0, 500),(1920, 500),(1920,800),(0, 800)]

# Video writer
video_writer = cv2.VideoWriter("object_counting_output1.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

# Init Object Counter
counter = solutions.ObjectCounter(
    view_img=True,
    reg_pts=region_points,
    classes_names=model.names,
    draw_tracks=False,
    line_thickness=4,
    count_bg_color=(0, 255, 0),
)

while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        print("Video frame is empty or video processing has been successfully completed.")
        break
    tracks = model.track(im0, persist=True, conf=0.5, iou=0.45, show=False)

    im0 = counter.start_counting(im0, tracks)
    video_writer.write(im0)

cap.release()
video_writer.release()
cv2.destroyAllWindows()