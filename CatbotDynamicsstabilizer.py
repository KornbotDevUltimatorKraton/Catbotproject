#!/usr/bin/python
import smbus
import math
import time  
import pyfirmata 
# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
AngleDegX  = 0 
AngleDegY = 0 
AngleDegZ = 0 
  # First serial harcware body control serial connection 
try:
  hardware = pyfirmata.ArduinoMega("/dev/ttyACM0")
  print("Catbot hardware serial connection successfully!")
except: 
  print("Hardware serial connection error trying to reconnect...")
  try: 
    hardware =pyfirmata.ArduinoMega("/dev/ttyACM1")
    print("Rerouting first serial successfully!")
  except: 
    print("Hardware serial error please checking physical hardware this time!")
  # Seccond hardware control serial connection 
try:
  hardware2 = pyfirmata.ArduinoMega("/dev/ttyUSB0")
  print("Catbot hardware serial connection successfully!")
except: 
  print("Seccond Hardware serial connection error trying to reconnect...")
  try: 
    hardware2 =pyfirmata.ArduinoMega("/dev/ttyUSB1")
    print("Rerouting seccond serial successfully!")
  except: 
    print("Seccond Hardware serial error please checking physical hardware this time!")
#Hardware pins connection with the pinmap micro controller 


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                     # X axis Gyrocontrol 

#Shoulder X - Left
Shoulder2Left = hardware.get_pin('d:6:s')
#Shoulder X-Right 
Shoulder2Right = hardware.get_pin('d:12:s')
#Abduct X - left 
AbductLeft  = hardware2.get_pin('d:5:s')
#Abduct X - right 
AbductRight = hardware2.get_pin('d:6:s')

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                    # Y axis  Gyrocontrol 
#Head 
Head = hardware.get_pin('d:8:s')
#Shoulder Y - Left
ShoulderLeft = hardware.get_pin('d:4:s')
#Shoulder Y - left 
ShoulderRight = hardware.get_pin('d:5:s')
#Hip Y - Left 
HipLeft = hardware.get_pin('d:3:s')
#Hip Y - Right
HipRight = hardware.get_pin('d:2:s') 
#Elbow Y - left 
ElbowLeft = hardware.get_pin('d:14:s')
#Elbow Y - Right
ElbowRight = hardware.get_pin('d:11:s')
#Abduct knee Y - Left 
#Abductknee3Left = hardware.get_pin('d:7:s') 
#Abductknee2Left = hardware2.get_pin('d:4:s')
#Abduct Knee Y - Right 
#Abductknee3Right = hardware2.get_pin('d:7:s')
#Abductknee2Right = hardware2.get_pin('d:8:s')
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                   # Z axis  Gyrocontrol 
#Headz = hardware.get_pin('d:15:s')


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
 
bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect
 
# Aktivieren, um das Modul ansprechen zu koennen
bus.write_byte_data(address, power_mgmt_1, 0)
 
print("Gyroskop")
print("--------")
 
gyroskop_xout = read_word_2c(0x43)
gyroskop_yout = read_word_2c(0x45)
gyroskop_zout = read_word_2c(0x47)

def ActuatorsXcontrol(AngleDegX): 
    if AngleDegX == 4.196468226055834: 
        Shoulder2Left.write(175)
        Shoulder2Right.write(5)
        AbductLeft.write(0)
        AbductRight.write(180)

    if AngleDegX > 4.196468226055834:
        Shoulder2Left.write(175 + abs(AngleDegX))
        Shoulder2Right.write(abs(AngleDegX + 8))
        AbductLeft.write(abs(AngleDegX))
        AbductRight.write(180 - abs(AngleDegX))   
    if AngleDegX < 4.196468226055834:
        Shoulder2Left.write(175 - abs(AngleDegX))
        Shoulder2Right.write(abs(AngleDegX + 8))
        AbductLeft.write(abs(AngleDegX))
        AbductRight.write(180 - abs(AngleDegX))   

def ActuatorsYcontrol(AngleDegY):
    Head.write(140 + AngleDegY)    
    if AngleDegY == 0.9511994645726558: 
        ShoulderLeft.write(120)
        ShoulderRight.write(50)
        ElbowLeft.write(50)
        ElbowRight.write(100)
        Abductknee2Right.write(170)
        HipLeft.write(160)
        HipRight.write(20)

    if AngleDegY > 0.9511994645726558:
        ShoulderLeft.write(120 - AngleDegY)
        ShoulderRight.write(50 + AngleDegY)
        ElbowLeft.write(50 - AngleDegY)
        ElbowRight.write(120 + AngleDegY)

        HipLeft.write(160 - abs(AngleDegX))
        HipRight.write(20 + abs(AngleDegX))

    if AngleDegY < 0.9511994645726558:
        ShoulderLeft.write(120 - AngleDegY)
        ShoulderRight.write(50 + AngleDegY )
        ElbowLeft.write(50 + AngleDegY)
        ElbowRight.write(120 - AngleDegY)
        HipLeft.write(160 + abs(AngleDegX))
        HipRight.write(20 - abs(AngleDegX))

while True:
#   print("gyroskop_xout: ", ("%5d" % gyroskop_xout), " skaliert: ", (gyroskop_xout / 131))
 #  print("gyroskop_yout: ", ("%5d" % gyroskop_yout), " skaliert: ", (gyroskop_yout / 131))
  # print("gyroskop_zout: ", ("%5d" % gyroskop_zout), " skaliert: ", (gyroskop_zout / 131))
 
   print("Catbot Gyroscope")
   print("---------------------")
 
   beschleunigung_xout = read_word_2c(0x3b)
   beschleunigung_yout = read_word_2c(0x3d)
   beschleunigung_zout = read_word_2c(0x3f)
 
   beschleunigung_xout_skaliert = beschleunigung_xout / 16384.0
   beschleunigung_yout_skaliert = beschleunigung_yout / 16384.0
   beschleunigung_zout_skaliert = beschleunigung_zout / 16384.0
   AngleDegX = math.degrees(beschleunigung_xout_skaliert)
   AngleDegY = math.degrees(beschleunigung_yout_skaliert)
   AngleDegZ = math.degrees(beschleunigung_zout_skaliert)
   print("AngleDegX",(AngleDegX))
   print("AngleDegY",(AngleDegY))
   print("AngleDegZ",(AngleDegZ))
   ActuatorsXcontrol(AngleDegY)
   ActuatorsYcontrol(AngleDegX)
   #ActuatorsZcontrol(AngleDegZ)
   #print("beschleunigung_xout: ", ("%6d" % beschleunigung_xout), " skaliert: ", beschleunigung_xout_skal$
   #print("beschleunigung_yout: ", ("%6d" % beschleunigung_yout), " skaliert: ", beschleunigung_yout_skal$
   #print("beschleunigung_zout: ", ("%6d" % beschleunigung_zout), " skaliert: ", beschleunigung_zout_skal$
   #print("X Rotation: " , get_x_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, bes$
   #print("Y Rotation: " , get_y_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, bes$
   time.sleep(0.2)
