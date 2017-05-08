#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  6 10:23:50 2017

@author: take
"""
#import os
#os.path.append("./")
from Images import Images
import time

if __name__ == "__main__":
    image_directory = "/Users/take/Pictures/flickr/"
    start = time.time()
    print("Read Images")
    imgs = Images(image_directory)
    print("Elaped TIme",time.time()-start,"[s]")
    #imgs.disp_info()
    
    print("Copy Images")
    imgs.copy_files_to_dist_dir()
    print("Elaped TIme",time.time()-start,"[s]")
