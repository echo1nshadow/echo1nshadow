#!/usr/bin/python3
# coding:utf-8
from PIL import Image
import numpy
import os
import sys
import getopt

def open_pic(argv):
    im=Image.open(argv);
    return im

def load_pic(im):
    return numpy.array(im)

def print_pic(im):
    arr=load_pic(im);
    i = 0;
    j = 0;
    while( i < im.height):
        j = 0
        while( j < im.width):
            print(arr[i,j])
            j+=1
        i += 1

def color_pic(arr,x,y,block,color):
    i = x;
    j = y;
    while( i < x+block ):
        j = y;
        while( j < y+block ):
            arr[i,j] = color;
            j += 1
        i += 1
    return arr

def get_average_color(arr,x,y,block):
    r = g = b = 0;
    i = x;
    j = y;
    while( i < x+block ):
        j = y;
        while( j < y+block ):
            r += arr[i,j][0]
            g += arr[i,j][1]
            b += arr[i,j][2]
            j += 1
        i += 1
    r = round(r / ( block * block))
    g = round(g / ( block * block))
    b = round(b / ( block * block))
    return tuple((r,g,b))

def save_pic(arr,dest_name):
    Image.fromarray(arr).save(dest_name)

def pixelated_pic(im,block):
    arr=load_pic(im);
    i = 0;
    j = 0;
    while( i < im.height ):
        j = 0;
        while( j < im.width ):
            color_tuple = get_average_color(arr,i,j,block)
            new_arr = color_pic(arr,i,j,block,color_tuple)
            j += block
        i += block
    return new_arr


def main(argv):
    block = 1
    src_name = ""
    dest_name = ""
    try:
        opts,args = getopt.getopt(argv,"b:i:o:",["block="])
    except getopt.GetoptError:
        print("parse argv error")
    for opt,arg in opts:
        if opt == '-b':
            block = int(arg)
            print("block:%d"%block)
        elif opt == '-o':
            dest_name = arg
            print(dest_name)
        elif opt == '-i':
            src_name = arg
            print(src_name)

    im=open_pic(src_name)
    arr = load_pic(im)
    new_arr = pixelated_pic(im,block)
    save_pic(new_arr,dest_name)


if __name__=="__main__":
    main(sys.argv[1:])

