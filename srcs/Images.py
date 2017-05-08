#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  6 10:27:42 2017

@author: take
"""
from ExifInfo import ExifInfo
import os
import shutil

class Images():
    def __init__(self,image_directory_full_path):
        #️画像があるディレクトリを受け取って画像を検索して画像ファイル名リストを作成する
        self.image_files = {}
        for root,dirs,files in os.walk(image_directory_full_path):
            #TODO 保存先ディレクトリ設定
            dist_root_dir = image_directory_full_path + "test/"
            for file in files:
                name,ext = os.path.splitext(file)            
                if ext.lower() == ".jpg".lower():
                    info = {}
                    image_file = os.path.join(root,file)
                    info["date"] = ExifInfo(image_file).get_day_date()
                    info["dist_dir"] = self.get_dist_dir(dist_root_dir,info["date"])
                    info["file_name"] = os.path.basename(image_file)
                    self.image_files[image_file] = info

    def disp_info(self):
        for name,info in self.image_files.items():
            print(name,info)
    
    def get_dist_dir(self,root_dir,day_date):
        #保存先を作成する root + 日付にする
        return root_dir + day_date[:4] + day_date[5:7] + day_date[8:10] + "/"
        
    def copy_files_to_dist_dir(self):
        #保存先にファイルをコピーする
        #同じファイルはコピーしない.
        print("Copy Start",len(self.image_files),"Files ...")
        count = 0
        for name,info in self.image_files.items():
            #ディレクトリが存在しなければ作成する
            if not os.path.isdir(info["dist_dir"]):
                os.makedirs(info["dist_dir"])
            
            #同じファイルがあれば、サイズが異なる場合のみ別名でコピーする.
            dist_name = info["dist_dir"]+info["file_name"]

            if os.path.exists(dist_name):
                #サイズが同じ場合、コピーしない.
                if os.path.getsize(dist_name) == os.path.getsize(name):
                    continue
                else:
                    #サイズが異なる場合、別名で保存する.
                    #TODO コピー後のファイルもチェックする必要あり
                    name_no_ext,ext = os.path.splitext(dist_name)            
                    dist_name = name_no_ext + "(2)" + ext

            try:
                shutil.copy2(name,dist_name)
                count+=1

            except shutil.SameFileError as err:
                continue
            
            
        print(count,"Files Finished")
        