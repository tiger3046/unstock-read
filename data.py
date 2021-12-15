import sqlite3
from PIL import Image
import sys
import pyocr
import pyocr.builders
import cv2
import requests
import os
import glob
import json


# SQLiteを操作するためのカーソルを作成
#cur = sqlite3.connect('db.sqlite3').cursor()
#cur.execute('SELECT * FROM timeline_post').fetchone()

#画の絶対パス入手
#if row[4]=='':
#    continue
#pic="/home/ec2-user/environment/media/"+row[4]
#print(pic)
#print(os.path.isfile(pic))

img = cv2.imread(r'/home/ec2-user/environment/media/images/isbn5_6.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite(r'/home/ec2-user/environment/book_serch/New Folder\grayscale.jpg', gray)
img_grayscale_pass = r'/home/ec2-user/environment/book_serch/New Folder\grayscale.jpg'

    
pyocr.tesseract.TESSERACT_CMD = r'/usr/bin/tesseract'

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
tool = tools[0]

result = tool.image_to_string(
    Image.open(img_grayscale_pass),
    lang="jpn+eng",
    builder=pyocr.builders.TextBuilder()
)
#確認用
#print(result)

#ISBNという文字列の位置を探す
index = result.find("ISBN")
result_list = list(result) #文字列を1文字ずつ配列に代入
isbn_list = []
for i in range(index+4,index+21):
    isbn_list.append(result_list[i])
isbn_number = ''.join(isbn_list)





#ISBN番号確認
#print('ISBN_Number:'+isbn_number)

#GoogleBooksAPI
url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:'
def main(isbn):
    req_url = url + isbn
    response = requests.get(req_url)
    return response.json()
ISBN_JSON = main(isbn_number)
book_name = ISBN_JSON["items"][0]["volumeInfo"]["title"]
authors_list=ISBN_JSON["items"][0]["volumeInfo"]["authors"]
authors = authors_list[0]
print(authors)
isbn_number = isbn_number.replace('-',"")
#isbn_number = int(isbn_number)
#print(type(isbn_number))

filepath = os.path.abspath("../db.sqlite3")
con = sqlite3.connect(filepath)
cur = con.cursor()
userID = 6
cur.execute("INSERT INTO case_booklist(\"isbn\",\"bookname\",\"writer\",userid_id) VALUES({},\"{}\",\"{}\",{});".format(isbn_number,book_name,authors,userID))
cur.close()
con.commit()
con.close()