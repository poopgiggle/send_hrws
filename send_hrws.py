#!/usr/bin/env python3

import socket
import struct
import sys
import time

if(len(sys.argv) < 2):
    print('''USAGE: %s <interface>''' % sys.argv[0])
    sys.exit(-1)
else:
    interface = sys.argv[1]

try:
    s = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
    s.bind((interface,))
except:
    print("Could not setup a CAN interface on %s." % interface)

can_frame_fmt = "=IB3x8s"

def build_can_frame(can_id, data):
    can_dlc = len(data)
    data = data.ljust(8, b'\x00')
    return struct.pack(can_frame_fmt, can_id, can_dlc, data)

pgn = 0x80FE6E00
src = 0x0b #TBD

def pack_speed(speed):
    return struct.pack("HHHH", *[speed]*4)

def create_speed_message(speed):
    return struct.pack(can_frame_fmt, pgn | src, 8, pack_speed(speed))

speed = 25600
while True:
    if speed == 0:
        speed = 25600
    for i in range(50):
        s.send(create_speed_message(speed))#parameter resolution: 1/256 KM/hr per bit
        time.sleep(.001 * 20)
    speed -= 1

#    for i in range(1250):
#        s.send(create_speed_message(17920))
#        time.sleep(.001 * 20)
