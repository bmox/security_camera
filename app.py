from body_finder import find_human
import cv2
import streamlit as st
import time
import datetime
import os


icon = cv2.imread("./icon.png", cv2.IMREAD_UNCHANGED)
icon=cv2.resize(icon,(100,100))
def overlay_transparent(background, overlay, x, y):

    background_width = background.shape[1]
    background_height = background.shape[0]

    if x >= background_width or y >= background_height:
        return background

    h, w = overlay.shape[0], overlay.shape[1]

    if x + w > background_width:
        w = background_width - x
        overlay = overlay[:, :w]

    if y + h > background_height:
        h = background_height - y
        overlay = overlay[:h]

    if overlay.shape[2] < 4:
        overlay = np.concatenate(
            [
                overlay,
                np.ones((overlay.shape[0], overlay.shape[1], 1), dtype=overlay.dtype)
                * 255,
            ],
            axis=2,
        )

    overlay_image = overlay[..., :3]
    mask = overlay[..., 3:] / 255.0

    background[y : y + h, x : x + w] = (1.0 - mask) * background[
        y : y + h, x : x + w
    ] + mask * overlay_image

    return background





camera = st.selectbox("Camera ",("Default","IP Cam"))
if camera=="Default":
    cap=cv2.VideoCapture(0)
if camera=="IP Cam":
    address = st.text_input('Enter your ip') 
    cap=cv2.VideoCapture(str(address))
    which_cam = st.selectbox("Select Which camere you are using",("Front","Back"))
selfie = st.selectbox("Selfi Mirror ",("ON","OFF"))


if st.button("Start"):
    image_placeholder = st.empty()
    detection = False
    detection_stopped_time = None
    timer_started = False
    SECONDS_TO_RECORD_AFTER_DETECTION = 5

    frame_size = (int(cap.get(3)), int(cap.get(4)))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    try:
        os.mkdir("temp")
    except:
        pass
    while True:
        
        success,frame=cap.read()
        if camera=="IP Cam":
            if which_cam=="Front":
                frame = cv2.rotate(frame, cv2.cv2.ROTATE_90_CLOCKWISE)
                frame = cv2.rotate(frame, cv2.cv2.ROTATE_90_CLOCKWISE)
                frame = cv2.rotate(frame, cv2.cv2.ROTATE_90_CLOCKWISE)
            if which_cam=="Back":
                frame = cv2.rotate(frame, cv2.cv2.ROTATE_90_CLOCKWISE)
        if selfie=="ON":
            frame=cv2.flip(frame,1) 
        frame,body_parts =find_human(frame,draw=False)
        if  len(body_parts)!=1:
            if detection:
                timer_started = False
            else:
                detection = True
                current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
                out = cv2.VideoWriter(
                    f"./temp/{current_time}.mp4", fourcc, 20, frame_size)
                print("Started Recording!")
        elif detection:
            if timer_started:
                if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                    detection = False
                    timer_started = False
                    out.release()
                    print('Stop Recording!')
            else:
                timer_started = True
                detection_stopped_time = time.time()
        # frame=cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        if detection:
            out.write(frame)
            frame=overlay_transparent(frame, icon, 10, 5)
        image_placeholder.image(frame, channels="BGR")
        time.sleep(0.01)