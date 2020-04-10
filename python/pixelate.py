#!/usr/bin/python3
# coding:utf-8
from PIL import Image
import numpy
import os
import sys
import getopt

def open_pic(argv):
    im=Image.open(argv)
    return im

def load_pic(im):
    return numpy.array(im)

def print_pic(im):
    arr=load_pic(im)
    i = 0
    j = 0
    while( i < im.height):
        j = 0
        while( j < im.width):
            print(arr[i,j])
            j+=1
        i += 1

def color_pic(arr,x,y,value,color):
    i = x
    j = y
    while( i < x+value ):
        j = y
        while( j < y+value ):
            arr[i,j] = color
            j += 1
        i += 1
    return arr

def get_average_color(arr,x,y,value):
    r = g = b = 0
    i = x
    j = y
    while( i < x+value ):
        j = y
        while( j < y+value ):
            r += arr[i,j][0]
            g += arr[i,j][1]
            b += arr[i,j][2]
            j += 1
        i += 1
    r = round(r / ( value * value))
    g = round(g / ( value * value))
    b = round(b / ( value * value))
    return tuple((r,g,b))


def pixelated_pic(im):
    global value
    arr=load_pic(im)
    i = 0
    j = 0
    while( i < im.height ):
        j = 0
        while( j < im.width ):
            color_tuple = get_average_color(arr,i,j,value)
            new_arr = color_pic(arr,i,j,value,color_tuple)
            j += value
        i += value
    return new_arr

def lighten_pic(im):
    arr = load_pic(im)
    i = 0
    j = 0
    while ( i < im.height ):
        j = 0
        while( j < im.width ):
            arr[i,j] = (arr[i,j][0]+10, arr[i,j][1]+10, arr[i,j][2]+10)
            j += 1
        i += 1
    return arr

def save_pic(arr,dest_name):
    Image.fromarray(arr).save(dest_name)

def process_pic(im,proc):
    return proc(im)

def main(argv):
    global value
    src_name = ""
    dest_name = ""
    try:
        opts,args = getopt.getopt(argv,"plv:i:o:",["value="])
    except getopt.GetoptError:
        print("parse argv error")
    for opt,arg in opts:
        if opt == '-v':
            value = int(arg)
            print("value:%d"%value)
        elif opt == '-o':
            dest_name = arg
            print(dest_name)
        elif opt == '-l':
            proc = lighten_pic
        elif opt == '-p':
            proc = pixelated_pic
        elif opt == '-i':
            src_name = arg
            print(src_name)

    im=open_pic(src_name)
    arr = load_pic(im)
    new_arr = process_pic(im,proc)
    save_pic(new_arr,dest_name)


value = 1

if __name__=="__main__":
    main(sys.argv[1:])

