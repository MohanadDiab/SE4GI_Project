import requests
import json
import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine


# Acquiring the data via HTTP request
response=requests.get('https://five.epicollect.net/api/export/entries/housing-quality-index-crafers-aldgate-stirling?per_page=100')
raw_data=response.text

# Converting the data into a readable JSON fromat
data=json.loads(raw_data)

# Transforming the JSON dataset into a Pandas data frame
df=pd.json_normalize(data['data']['entries'])

# setup db connection (generic connection path to be update with your credentials: 'postgresql://user:password@localhost:5432/mydatabase')
# possible errors happen when the port or the password aren't updated with your laptop/database
# make sure you have a databse called se4g and it has the postgis extension
engine = create_engine('postgresql://postgres:admin@localhost:5432/se4g')

# export the data frame into the databse
df.to_sql('Housing Data', engine,if_exists='replace',index=False)

# import the data frame from the databse
df=pd.read_sql_table('Housing Data',engine)

# create two new columns with numeric coordinate values
df['lat'] = pd.to_numeric(df['1_Location.latitude'], errors='coerce')
df['lon'] =  pd.to_numeric(df['1_Location.longitude'], errors='coerce')

# from Pandas DataFrame to GeoPandas GeoDataFrame
geodf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['lon'], df['lat']))

