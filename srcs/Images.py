#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  6 10:27:42 2017

@author: take
"""
import glob as gb
from ExifInfo import ExifInfo
import os

class Images():
    def __init__(self,image_directory_full_path):
        #️画像があるディレクトリを受け取って画像を検索して画像ファイル名リストを作成する
        self.image_files = {}
        for root,dirs,files in os.walk(image_directory_full_path):
            
            for file in files:
                name,ext = os.path.splitext(file)            
                if ext.lower() == ".jpg".lower():
                    image_file = os.path.join(root,file)
                    date = ExifInfo(image_file).get_day_date()
                    self.image_files[image_file] = date

    def disp_info(self):
        for name,date in self.image_files.items():
            print(date,name)
        