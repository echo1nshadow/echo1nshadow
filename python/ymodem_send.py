#!/usr/bin/python3
# coding:utf-8

import pdb
import serial
import sys
import time
import binascii

SOH = 0x01
STH = 0x02
ACK = 0x06
C   = 'C'

def open_serial(com):
    return serial.Serial(com,115200,timeout=0.5)

def send_msg(ser,msg):
    ser.write(msg.encode())

def crc_ymodem(buff,len):
    wCRCin = 0x0000
    wCPoly = 0x1021
    wChar  = 0
    i = 0
    while(len):
        wChar = buff[i]
        wCRCin ^= (wChar << 8);
        i += 1

        j = 0
        while( j < 8 ):
            if (wCRCin & 0x8000):
                wCRCin = (wCRCin << 1) ^ wCPoly;
            else:
                wCRCin = wCRCin << 1;
            j += 1
            
        len -= 1
    return wCRCin

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
    file = [0] * 133
    i = 0
    while(1):
        file[0] = SOH
        file[1] = i
        file[2] = ~i
        ret = fd.read(128)
        j = 0
        len = ret.__len__()
        while( j < len ):
            file[i] = ret[j]
            j += 1
            i += 1
        
        while( j < 128 ):
            file[i] = 0xff
            j += 1
            i += 1


        
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
