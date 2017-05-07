#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  6 11:05:31 2017

@author: take
"""
from PIL import Image
from PIL.ExifTags  import TAGS 

class ExifInfo():
    def __init__(self,image_name):
        self.file_name = image_name
    
    def get_day_date(self):
        img = Image.open(self.file_name)
        date = ""
        try:
            exif = img._getexif()
            for id,val in exif.items():
                tg = TAGS.get(id,id)
                if tg == "DateTimeOriginal":
                    date = val
        except AttributeError:
            pass
        
        img.close()
        return date

