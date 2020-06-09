#!/usr/bin/python3
# coding:utf-8

import serial
import sys
import time

def open_serial(com):
    return serial.Serial(com,9600,timeout=0.5)

def send_msg(ser,msg):
    ser.write(msg.encode())

if __name__ =="__main__":
    ser = open_serial(sys.argv[1]);
    i = 0;
    send_msg(ser,"/1ZR\r\n");
    time.sleep(3);
    while( i < int(sys.argv[2])):
        print(i)
        send_msg(ser,"/1IA1500OA0R\r\n");
        time.sleep(3.5);
        i += 1
