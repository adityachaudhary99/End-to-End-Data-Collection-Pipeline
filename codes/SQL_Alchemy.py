import configparser
import sqlalchemy
import pymysql
from Weather_API_Data import weather_df
from Demographic_Data import cities_df
from Flight_Airport_Codes import flights_df

config = configparser.ConfigParser()
config.read('config.ini')
password = config['secret']['passwpord']

schema = "Gans_support_data"  # the database created in MySQL
host = "127.0.0.1"
user = "root"
password = password
port = 3306
con = f'mysql+pymysql://{user}:{password}@{host}:{port}/{schema}'

weather_df.to_sql('weather',  # name of the table
                  if_exists='replace',
                  con=con,
                  index=False)

cities_df.to_sql('cities',  # name of the table
                 if_exists='replace',
                 con=con,
                 index=False)

flights_df.to_sql('flight',  # name of the table
                  if_exists='replace',
                  con=con,
                  index=False)
