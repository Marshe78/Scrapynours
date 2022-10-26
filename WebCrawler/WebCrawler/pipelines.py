# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector

class WebcrawlerPipeline:
    def process_item(self, item, spider):
        return item

class Database:
    def connectDb():
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
        )
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS reviews")

    def createTable():
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="reviews"
        )
        mycursor = mydb.cursor()
        mycursor.execute("CREATE TABLE IF NOT EXISTS movie (title VARCHAR(255), img VARCHAR(255), author VARCHAR(255), time VARCHAR(255), genre VARCHAR(255), score VARCHAR(255), description TEXT(50000), releaseDate VARCHAR(255))")
        mycursor.execute("CREATE TABLE IF NOT EXISTS boursorama (indexStockExchange VARCHAR(255), stockAction VARCHAR(255), variation VARCHAR(255), vMax VARCHAR(255), vMin VARCHAR(255), vOpen VARCHAR(255), dateCollect DATE)")

    def addRow(item):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="reviews"
        )
        mycursor = mydb.cursor()
        sql = "INSERT INTO movie (title, img, author, time, genre, score, description, releaseDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (item['title'], item['img'], item['author'], item['time'], item['genre'], item['score'], item['desc'], item['release'])
        mycursor.execute(sql, val)
        mydb.commit()
        # print("Title :" , type(item['title']) , "Img :" , type(item['img']) , "Author :" , type(item['author']) , "Time :" , type(item['time']) , "Genre :" , type(item['genre']) , "Score :" , type(item['score']) , "Description :" , type(item['desc']) , "Release Date :" , type(item['release']))

    def addRowBoursorama(item):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="reviews"
        )
        mycursor = mydb.cursor()
        sql = "INSERT INTO boursorama (indexStockExchange, stockAction, variation, vMax, vMin, vOpen, dateCollect) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (item['indexStockExchange'], item['stockAction'], item['variation'], item['vMax'], item['vMin'], item['vOpen'], item['dateCollect'])
        mycursor.execute(sql, val)
        mydb.commit()