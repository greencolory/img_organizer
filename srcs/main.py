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

#image_directory = "/Users/take/Pictures/flickr/"
image_directory = "/Volumes/photo/temp/"
#dist_directory = "/Users/take/Pictures/flickr/test/"
dist_directory = "/Volumes/photo/"

if __name__ == "__main__":
    start = time.time()
    print("Read Images")
    imgs = Images(image_directory,dist_directory)
    print("Elaped TIme",time.time()-start,"[s]")
    #imgs.disp_info()
    
    print("Copy Images")
    imgs.copy_files_to_dist_dir()
    print("Elaped TIme",time.time()-start,"[s]")

    imgs.write_log_file()
    