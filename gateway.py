import serial.tools.list_ports
import random
import time
import  sys
from connect import *
from  Adafruit_IO import  MQTTClient

# import mysql.connector

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="",
#   database="sfarm"
# )

# mycursor = mydb.cursor()
INSERT INTO `temp_record` (`T_ID`, `Date`, `Time`, `Tempdata`, `A_ID`) VALUES (NULL, CURDATE(), CURTIME(), '30', '1');

# sql = "INSERT INTO `temp_record` (`T_ID`, `Date`, `Time`, `Tempdata`, `A_ID`) VALUES (NULL, CURDATE(), CURTIME(), %s, '1');"
# val = ()
# mycursor.execute(sql, val)

# mydb.commit()

# sql = "INSERT INTO `light_record` (`T_ID`, `Date`, `Time`, `Lightdata`, `A_ID`) VALUES (NULL, CURDATE(), CURTIME(), %s, '1');"
# val = ()
# mycursor.execute(sql, val)

# mydb.commit()

# sql = "INSERT INTO `moist_record` (`T_ID`, `Date`, `Time`, `Moistdata`, `A_ID`) VALUES (NULL, CURDATE(), CURTIME(), %s, '1');"
# val = ()
# mycursor.execute(sql, val)

# mydb.commit()


AIO_FEED_ID = "dadn-pump"

AIO_USERNAME = "khoinguyen3923"
AIO_KEY = "aio_dhWy65egcAicAWwbIuG3Gzw1Nym5"

def  connected(client):
    print("Ket noi thanh cong...")
    client.subscribe(AIO_FEED_ID)

def  subscribe(client , userdata , mid , granted_qos):
    print("Subcribe thanh cong...")

def  disconnected(client):
    print("Ngat ket noi...")
    sys.exit (1)

def  message(client , feed_id , payload):
    print("Nhan du lieu: " + payload)
    if isYolobitConnected:
        ser.write((str(payload) + "#").encode())

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB Serial Device" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort

isYolobitConnected = False
if getPort() != "None":
    ser = serial.Serial( port=getPort(), baudrate=115200)
    isYolobitConnected = True


while True:
    time.sleep(1)