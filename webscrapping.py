import requests
import pandas as pd
from bs4 import BeautifulSoup
import sqlalchemy
from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


url = 'https://www.flipkart.com/search?q=mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
response = requests.get(url)
soup = BeautifulSoup(response.content,'html.parser')

mobiles_data = []
name=soup.find_all('div',class_='KzDlHZ')
names=[]
for i in name[0:10]:
    d=i.get_text()
    names.append(d)
# print(names)

price=soup.find_all('div',class_='Nx9bqj _4b5DiR')
prices=[]
for i in price[0:10]:
    d=i.get_text()
    prices.append(d[1:])
# print(prices)

rating=soup.find_all('div',class_='XQDdHH')
ratings=[]
for i in rating[0:10]:
    d=i.get_text()
    ratings.append(d)
# print(ratings)

image=soup.find_all('img',class_='DByuf4')
images=[]
for i in image[0:10]:
    d=i['src']
    images.append(d)

df = pd.DataFrame()
df['mobiles_Names']= names
df['mobiles_prices']=prices
df['mobiles_ratings']=ratings
df['mobiles_images']=images
df.to_csv('mobiles_data.csv', index=False)
# print(df)

# Define the SQLite database
DATABASE_URL = 'sqlite:///mobiles_data.db'
Base = sqlalchemy.orm.declarative_base()

# Define the mobiles_data model
class Data(Base):
    __tablename__ = 'mobiles_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    names = Column(String)
    prices = Column(String)
    ratings= Column(String)
    images=Column(String)
   

# Create the database and table
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Insert the data into the database
for data in mobiles_data:
    data_record = Data(names=data['names'], prices=data['prices'],ratings=data['ratings'],images=data['images'])
    session.add(data_record)

# Commit the session
session.commit()










