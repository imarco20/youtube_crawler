from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import pymysql

engine = create_engine("mysql+pymysql://root:mysql@localhost/youtube_crawler", echo=True)
engine.connect()
