#!/usr/bin/python3
# coding:utf-8

import pdb
import serial
import sys
import time
import binascii

def open_serial(com):
    return serial.Serial(com,115200,timeout=0.5)

def send_msg(ser,msg):
    ser.write(msg.encode())

def open_file(file,mode):
    try:
        fd = open(file,mode)
    except OSError:
        print("can not open this file")
        input()
        quit()
    return fd

def ymodem_transfer(ser):
    print("transfer start")
    fd = open_file("test.txt","r")
    while(1):
        time.sleep(1)
'''
def recv_msg(ser):
    print(ser.readline())
'''
if __name__ =="__main__":
    ser = open_serial(sys.argv[1]);
    i = 0;
    send_msg(ser,"update\r\n");
    print(ser.readline())
    time.sleep(1);
    while(1):
        ch = ser.read()
        if( ch == b'C' ):
            ymodem_transfer(ser)
        
    '''
    while( i < int(sys.argv[2])):
        print(i)
        send_msg(ser,"/1IA1500OA0R\r\n");
        time.sleep(3.5);
        i += 1
    '''
