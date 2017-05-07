#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  6 10:23:50 2017

@author: take
"""
#import os
#os.path.append("./")
from Images import Images

if __name__ == "__main__":
    image_directory = "/Users/take/Pictures/flickr/"
    imgs = Images(image_directory)
    imgs.disp_info()
