import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
cap = cv2.VideoCapture(0)
pose=mp_pose.Pose(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7)
def find_human(image,draw=True):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = pose.process(image)
    body_parts=[]
    if results.pose_landmarks:
        for id, lm in enumerate(results.pose_landmarks.landmark):
                    h, w, c = image.shape
                    # print(id, lm)
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    body_parts.append([id,cx,cy]) 
    else:
        body_parts.append("None")
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if draw:
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    return image, body_parts      


# while cap.isOpened():
#     success, image = cap.read()
#     image = cv2.flip(image, 1)
#     image,body_parts =find_human(image,draw=True)
#     if len(body_parts)>0:
#         print(len(body_parts))
#     cv2.imshow('MediaPipe Pose', image )
#     if cv2.waitKey(5) & 0xFF == 27:
#         break
# cap.release()