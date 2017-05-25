#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  6 10:27:42 2017

@author: take
"""
from ExifInfo import ExifInfo
import os
import shutil
from tqdm import tqdm
class Images():
    def __init__(self,image_directory_full_path,dist_root_dir):
        #️画像があるディレクトリを受け取って画像を検索して画像ファイル名リストを作成する
        self.image_files = {}
        self.error_log = {}
        self.src_dir = image_directory_full_path
        for root,dirs,files in os.walk(image_directory_full_path):
            for file in files:
                name,ext = os.path.splitext(file)            
                if ext.lower() == ".jpg".lower():
                    info = {}
                    image_file = os.path.join(root,file)
                    info["date"] = ExifInfo(image_file).get_day_date()
                    info["dist_dir"] = self.get_dist_dir(dist_root_dir,info["date"])
                    info["file_name"] = os.path.basename(image_file)
                    info["copy_name"] = ""
                    self.image_files[image_file] = info
            self.input_file_num = len(self.image_files)
            self.copy_file_num = 0
            
    def disp_info(self):
        for name,info in self.image_files.items():
            print(name,info)
    
    def get_dist_dir(self,root_dir,day_date):
        #保存先を作成する root + 日付にする
        return root_dir + day_date[:4] + "/" + day_date[:4] + day_date[5:7] + day_date[8:10] + "/"
        
    def create_copy_file_list(self):
        src_files = []
        dist_files = []

        #コピーファイルリストを作成する.
        for name,info in self.image_files.items():
            src_name = name
            dist_name = info["dist_dir"]+info["file_name"]

            if self.is_same_file(src_name,dist_name):
                self.error_log[src_name] = "SAME FILE1"
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
                    self.error_log[src_name] = "SAME FILE2"
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

        print("1.Make Directory")
        #ディレクトリが存在しなければ作成する
        for name,info in self.image_files.items():
            if not os.path.isdir(info["dist_dir"]):
                os.makedirs(info["dist_dir"])
                
        print("2.Create Copy List")
        src_files,dist_files = self.create_copy_file_list()
        
        print("3.Copying","...")
        prog_bar = tqdm(total = len(src_files))
        for src,dist in zip(src_files,dist_files):
            try:
                shutil.copy2(src,dist)
                #DEBUG
                #print(src,dist)
                self.image_files[src]["copy_name"] = dist
                self.copy_file_num+=1
                prog_bar.update(1)

            except shutil.SameFileError as err:
                self.error_log[src] = "SAME PATH"
                prog_bar.update(1)
                continue

        prog_bar.close()
        print(self.copy_file_num,"Files Finished")
        
    def write_log_file(self):
        fout = open(self.src_dir+"log.txt","wt")
        print("Result Summary----------------------------------",file=fout)
        print("Summary",file=fout)
        print("Target Files         :",self.input_file_num,file=fout)
        print("Copy Successful      :",self.copy_file_num,file=fout)
        print("Error Files          :",len(self.error_log),file=fout)
        print("Error Type SAME FILE1:",list(self.error_log.values()).count("SAME FILE1"),file=fout)
        print("Error Type SAME FILE2:",list(self.error_log.values()).count("SAME FILE2"),file=fout)
        print("Error Type SAME PATH :",list(self.error_log.values()).count("SAME PATH"),file=fout)
        print("Result to Copy Image Files----------------------",file=fout)
        for name,info in self.image_files.items():
            print(name," -> ",info["copy_name"],file=fout)
            
        fout.close()
        