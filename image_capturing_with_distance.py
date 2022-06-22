from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import distance
import serial
from datetime import datetime


try:
# initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (1920, 1080)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(1920, 1080))
    # allow the camera to warmup
    time.sleep(0.1)
    # capture frames from the camera
except Exception as e:
    print(e)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    
# grab the raw NumPy array representing the image, then initialize the timestamp
# and occupied/unoccupied text
    
    image = frame.array
    try:
        ser = serial.Serial("/dev/ttyAMA0", 115200, bytesize=8, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE)
    except Exception as e:
        print(e)
    if ser.is_open == False: ser.open()
    try:
        distance_ = distance.getTFminiData()
    except Exception as e:
        print(e)
        distance_ = -1

    
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y-%H-%M-%S-%f.jpg")
    try:
        
        image = cv2.putText(image, f"Distance: {distance_} cm", (20,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0) , 2, cv2.LINE_AA)
    except Exception as e:
        print(e)
    
    ser.close()
    #cv2.imshow("Frame", image)
    try:
        cv2.imwrite(timestampStr, image)
    except Exception as e:
        print(e)
    
    time.sleep(0.3)
    key = cv2.waitKey(1) & 0xFF
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
            

