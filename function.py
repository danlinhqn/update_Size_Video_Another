import pyautogui
import pyperclip
import win32api
import win32con
import time
import random
import shutil
import webbrowser as wb
import re
import os
import subprocess
from datetime import datetime
from PIL import ImageGrab
from bs4 import BeautifulSoup
import requests
import urllib.parse
from PIL import Image
from io import BytesIO
import numpy as np
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import uuid
import json
import glob
import pydirectinput
import string
from pywinauto import Application
import psycopg2


# Tại đây khai báo để gọi API sửa dụng upload DB UAT
API_TOKEN = 'https://wapi.weallnet.com/api/TOKEN_AccessToken/GetClientAccessToken'
API_SAVE_PHOTOS = 'https://wapi.weallnet.com/api/Photo/Save'
API_SAVE_IMAGES = 'https://wapi.weallnet.com/api/PhotoImage/Save'

# Khai báo Token, để có thể truy cập lên DB
def getToken():
    
    try :
        r = requests.post(API_TOKEN,
                        
            # # UAT => Test      
            # json={
            #     "clientId": "WANBMS",
            #     "clientSecret": "QVFOGGL5ECOTJE3RZPVRR455IWAN01",
            #     "scope": "WANAPI"
            #     }
            
            # PROD
            json={
                "clientId": "WANBMS",
                "clientSecret": "QVFOGGL5ECOTJE3RZPVRR455IWAN01",
                "scope": "WANAPI"
                }
            
            
            )

            

        return r.json().get('access_token')
    except requests.exceptions.HTTPError as err: print(f"Http Error: {err}")

TOKEN = getToken()

# Hàm update lại Code random cho DB Photos
def Update_Code_Random_DB():
    
    list_ID_Photos = []
    
    # Kết nối với DB | Kiểm tra Data sử dụng trước khi chạy chương trình
    def connectDB():
        
        conn = psycopg2.connect(
            
                # Data PROD
                host="172.16.33.100",
                port="5432",
                database="WAN_Data",
                user="wan_data",
                password="fbpSk9MPmjheVzEtR8Ax6Q4NWYa3JnqG"

            )
        
        return(conn)

    def getIDFromDB():

        cur = connectDB().cursor()

        # Hàm hỗ trợ lấy dữ liệu ChannelConfigID + ID video tiktok + thời gian tải lên
        
        cur.execute( 'SELECT "PhotoID" FROM "Photos" ')

        rows = cur.fetchall()

        # Lưu vào Data => Chuẩn bị tới bước tiếp theo phân loại và xóa trash
        for row in rows: 
            list_ID_Photos.append(row[0])

        # Ngắt kết nối khi lấy dữ liệu xong

        cur.close()
        connectDB().close()
        
    # ------------------------------------ /
    # Hàm update lại Code random cho DB Photos
    def updateCodeForPhotoID(photo_id):
        # Tạo kết nối đến cơ sở dữ liệu
        connection = connectDB()
        cur = connection.cursor()

        # Thực hiện lệnh SQL để cập nhật cột "Code"
        cur.execute('UPDATE "Photos" SET "Code" = %s WHERE "PhotoID" = %s', (str(uuid.uuid1()), photo_id))

        # Commit thay đổi vào cơ sở dữ liệu và đóng kết nối
        connection.commit()
        cur.close()
        connection.close()

# Hàm ghi giá trị txt vào file 
def write_Value_To_File_Txt(file_path, values_to_append):

    values_to_append = str(values_to_append)
    # File path to append the values
        
    with open(file_path, 'a', encoding='utf-8') as file:
        file.writelines(values_to_append + "\n")
        
# Hàm tính kích thước của Hình
def get_image_dimensions_from_url(image_url):
    
    try:
        # Tải hình ảnh từ URL
        response = requests.get(image_url)
        response.raise_for_status()
        
        # Đọc hình ảnh từ dữ liệu nhận được
        image = Image.open(BytesIO(response.content))
        
        # Lấy thông tin chiều cao và chiều rộng của hình ảnh
        width, height = image.size
        
        return width, height
    
    except Exception as e:
        print("Error:", str(e))
        return None, None
    
    
