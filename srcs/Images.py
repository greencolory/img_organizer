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

    def create_copy_file_list(self):
        src_files = []
        dist_files = []

        #コピーファイルリストを作成する.
        for name,info in self.image_files.items():
            src_name = name
            dist_name = info["dist_dir"]+info["file_name"]

            if self.is_same_file(src_name,dist_name):
                continue

            src_files.append(src_name)
            dist_files.append(dist_name)
        
        #コピーファイルリストのうち、同じ名前のものをリネームする.
        #リネームした後のファイル名がかぶらない用にリネーム後listの最後に追加して再チェックする
        is_check = True
        
        while is_check:
            is_check = False
            for src_name,dist_name in zip(src_files,dist_files):

                if self.is_same_file(src_name,dist_name):
                    #リネームしたファイルで同じものがある場合は、削除する.
                    src_files.remove(src_name)
                    dist_files.remove(dist_name)
                else:
                    if os.path.exists(dist_name):
                        #元のファイルをリストから削除してリネームしてlistの最後に追加する
                        name_no_ext,ext = os.path.splitext(dist_name)            
        
                        src_files.remove(src_name)
                        dist_files.remove(dist_name)
                        
                        dist_name = name_no_ext + "(2)" + ext
                        src_files.append(src_name)
                        dist_files.append(dist_name)
                        is_check = True
                    else:
                        continue
                    
        
        return src_files,dist_files
        
    def is_same_file(self,src,dist):
        is_same = False
        if os.path.exists(dist):
            #サイズが同じ
            if os.path.getsize(dist) == os.path.getsize(src):
                is_same = True
        return is_same
        
    def copy_files_to_dist_dir(self):
        #保存先にファイルをコピーする
        #同じファイルはコピーしない.
        print("Copy Start",len(self.image_files),"Files ...")
        count = 0

        #ディレクトリが存在しなければ作成する
        for name,info in self.image_files.items():
            if not os.path.isdir(info["dist_dir"]):
                os.makedirs(info["dist_dir"])
                
        src_files,dist_files = self.create_copy_file_list()
        
        for src,dist in zip(src_files,dist_files):
            try:
                shutil.copy2(src,dist)
                #DEBUG
                #print(src,dist)
                count+=1

            except shutil.SameFileError as err:
                continue

        print(count,"Files Finished")
        