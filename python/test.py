#!/usr/bin/python3
# coding:utf-8
from PIL import Image
import numpy
import os
import sys

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

def black_pic(im,dest_pic_name):
    arr=load_pic(im);
    i = 0;
    j = 0;
    while( i < im.height):
        j = 0
        while( j < im.width):
            arr[i,j]=(0,0,0)
            j+=1
        i += 1

    new_im=Image.fromarray(arr)
    new_im.save(dest_pic_name)


if __name__=="__main__":
    im=open_pic(sys.argv[1])
    black_pic(im,sys.argv[2])


