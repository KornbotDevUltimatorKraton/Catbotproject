#Author: Mr.Chanapai Chuadchum Project name: Catbot Project
#description: This project was devlop to be the robot that cooperating
#with human in the family be a part of daily life and learn from human
#date developing: 28/5/2019 - Now
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera # processing image
import cv2 #image processing function
import time #timing control function
import pyfirmata #hardware interface pyfirmata protocol official verison import math
from nanpy import(ArduinoApi,SerialManager) # Nanpy protocol hardware interface for prototype version
from nanpy import Servo
import speech_recognition as sr 
import pyttsx3
import smbus
import math
import datetime
import serial # For the GPS UART serial communication system
times = datetime.datetime.now()
camera = PiCamera()
camera.resolution = (384, 288)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(384, 288))
#/hardware = pyfirmata.ArduinoMega("/dev/ttyACM0")
display_window = cv2.namedWindow("Catbot vision system")

face_cascade = cv2.CascadeClassifier('/usr/share/opencv/opencv/data/haarcascades/haarcascade_frontalface_alt.xml')
cat_cascade = cv2.CascadeClassifier('/usr/share/opencv/opencv/data/haarcascades/haarcascade_frontalcatface.xml')
emotion_cascade = cv2.CascadeClassifier('/usr/share/opencv/opencv/data/Faceemo/cascade.xml')
dog_cascade = cv2.CascadeClassifier('/usr/share/opencv/opencv/data/Dogcascade-/cascade.xml')
kuvars_cascade = cv2.CascadeClassifier('/usr/share/opencv/opencv/data/kuvarsdogCascade/cascade.xml')
Goldenr_cascade = cv2.CascadeClassifier('/usr/share/opencv/opencv/data/Goldenretrievercascade-/cascade.xml')
car_cascade = cv2.CascadeClassifier('/usr/share/opencv/opencv/data/Carcascade-/cascade.xml')
time.sleep(1)
r = 0

 # 3D space angle convert function radians to degrees
angleDegX = 0
angleDegY = 0
angleDegZ = 0
c = 0
  # Gyro scope address
# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
 # Gyro sensor calculation function on the body dynamic
def read_byte(reg):
    return bus.read_byte_data(address, reg)

def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value

def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def Calculatedeep(w,h):
      d = w*h
      r = 226*(d/52441)
      return r
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
 #Gyroscope sensor
bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect
         # Aktivieren, um das Modul ansprechen zu koennen
bus.write_byte_data(address, power_mgmt_1, 0)
print("Gyroscope")
print("--------")
gyroskop_xout = read_word_2c(0x43)
gyroskop_yout = read_word_2c(0x45)
gyroskop_zout = read_word_2c(0x47)
 # Audio
engine = pyttsx3.init()
engine.setProperty('rate',150)
engine.setProperty('volume',0.4)

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
try:
  hardware = pyfirmata.ArduinoMega("/dev/ttyACM0")
  print("Body hardware connection successfully !")
except:
  print("Hardware body disconnect please reconnect !")
 # try:
   # print("Nanpy firmware accessing ....")
  # connection = SerialManager()
  #  Hardware = ArduinoApi(connection=connection)
 # except:
#     print("Non of body hardware control found !")
   # Actuator neck setting
ServoX = hardware.get_pin('d:10:s')
ServoY1 = hardware.get_pin('d:8:s')
ServoY2 = hardware.get_pin('d:9:s')
#ServoX.write(80)
#ServoY2.write(120)
#try:
 #  ServoXn = Servo(9)
  # ServoYn = Servo(8)
#except:
#   print("Hardware control wrong type on of them found")
#ServoY1 = hardware.get_pin('d:8:s')
#ServoY2 = hardware.get_pin('d:10:s')
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    image = frame.array

    #FACE DETECTION STUFF
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
         # Gyro scope running value
    print("gyroscope_xout: ", ("%5d" % gyroskop_xout), " radian x : ", (gyroskop_xout /131))
    print("gyroscope_yout: ", ("%5d" % gyroskop_yout), " radian y: ", (gyroskop_yout /131))
    print( "gyroscope_zout: ", ("%5d" % gyroskop_zout), "radian z: ", (gyroskop_zout/131))
    print("Conversion sensor")
    print("---------------------")
    beschleunigung_xout = read_word_2c(0x3b)
    beschleunigung_yout = read_word_2c(0x3d)
    beschleunigung_zout = read_word_2c(0x3f)
    beschleunigung_xout_skaliert = beschleunigung_xout / 16384.0
    beschleunigung_yout_skaliert = beschleunigung_yout / 16384.0
    beschleunigung_zout_skaliert = beschleunigung_zout / 16384.0
           # Angle calculation function convert to degrees
    angleDegX = math.degrees(beschleunigung_xout_skaliert)
    angleDegY = math.degrees(beschleunigung_yout_skaliert)
    angleDegZ = math.degrees(beschleunigung_zout_skaliert)
    print("AngleDegX",(angleDegX))  # Angle X
    print("AngleDegY",(angleDegY))  # Angle Y
    print("AngleDegZ",(angleDegZ))  # Angle Z
    print(times) # Time function
#    ServoX.write(80)
 #   ServoY2.write(120)
    cv2.putText(image,'time'+str(times),(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.2,(0,255,0),1,-1)
    cv2.putText(image,'Gyroscope',(10,200),cv2.FONT_HERSHEY_SIMPLEX,0.2,(0,0,255),1,-1)
    cv2.putText(image,'X-axis \t'+ str(angleDegX),(10,220),cv2.FONT_HERSHEY_SIMPLEX,0.2,(255,0,0),1,-1)
    cv2.putText(image,'Y-axis \t'+ str(angleDegY),(10,240),cv2.FONT_HERSHEY_SIMPLEX,0.2,(255,0,0),1,-1)
    cv2.putText(image,'Z-axis \t'+ str(angleDegZ),(10,260),cv2.FONT_HERSHEY_SIMPLEX,0.2,(255,0,0),1,-1)
    cv2.putText(image,'Accelerometer',(110,200),cv2.FONT_HERSHEY_SIMPLEX,0.2,(0,0,255),1,-1)
    cv2.putText(image,'X-axis \t'+ str(beschleunigung_xout_skaliert),(130,220),cv2.FONT_HERSHEY_SIMPLEX,0.2,(255,0,0),1,-1)
    cv2.putText(image,'Y-axis \t'+ str(beschleunigung_yout_skaliert),(130,240),cv2.FONT_HERSHEY_SIMPLEX,0.2,(255,0,0),1,-1)
    cv2.putText(image,'Z-axis \t'+ str(beschleunigung_zout_skaliert),(130,260),cv2.FONT_HERSHEY_SIMPLEX,0.2,(255,0,0),1,-1)
    for (x,y,w,h) in faces:
       # font = cv2.FONT_HERSHEY_SIMPLEX
        engine.say("Hello human")
        engine.runAndWait()
       # ServoX.write(abs((x/384)*180))
       # ServoY1.write(abs((y/288)*160))
        #ServoY2.write(abs((y/288)*160))
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.putText(image,'Human face',(x-w,y-h),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),1,-1)
       # cv2.putText(image,'Human face',(x-w,y-h))
        ServoX.write(abs(((x-(h/2))/384)*180))
        ServoY1.write(abs(160-(y/288)*160))
       # ServoY2.write(abs((y/288)*160))
        time.sleep(0.02)
        print(x,y,w,h)
        print("Calculate deep of picture detected:")
        print(Calculatedeep(w,h))
        print("cm.")

    cats = cat_cascade.detectMultiScale(gray,1.1, 5)
    for(x,y,w,h) in cats:
            #font = cv2.FONT_HERSHEY_SIMPLEX
            engine.say("Hello cat meaw meaw")
            engine.runAndWait()
            cv2.rectangle(image,(x,y),(x+w,y+h),(54,255,255),2)
            cv2.putText(image,'Cat face',(x-w,y-h),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),1,-1)
            try:
              ServoX.write(abs(((x- (h/2))/384)*180))
              ServoY1.write(abs(160-(y/288)*160))
              #ServoY2.write(abs((y/288)*160))
              time.sleep(0.02)
            except:
            print("Some servo might broken or short circuit  please recheck need repairment")
            print("Cat detected")
#    emotion = emotion_cascade.detectMultiScale(gray, 1.1, 5)
 #   for(x,y,w,h) in emotion:
  #          cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
   #         print("Emotion detected")
    dogs = dog_cascade.detectMultiScale(gray, 1.1, 5)
    for(x,y,w,h) in dogs:
        #    font = cv2.FONT_HERSHEY_SIMPLEX
            engine.say("Hello dog hong hong")
            engine.runAndWait()
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
            cv2.putText(image,'Siberian husky',(x-w,y-h),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),1,-1)
         #   cv2.puText(image,'Seiberian husky',(x-w,y-h))
            try:
              ServoX.write(abs(((x- (h/2))/384)*180))
              ServoY1.write(abs((y/288)*160))
              #ServoY2.write(abs((y/288)*160))
              time.sleep(0.02)
            except:
                 print("Some servo might broken or short circuit  please recheck need repairment")
            print("Dog species siberien husky")
    cv2.imshow("Catbot vision system", image)
    key = cv2.waitKey(1)

    rawCapture.truncate(0)

    if key == 27:
        camera.close()
        cv2.destroyAllWindows()
        break