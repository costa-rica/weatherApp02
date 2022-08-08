from sqlalchemy import create_engine, inspect
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
import json
from datetime import datetime

with open(r'C:\Users\captian2020\Documents\config_files\config_weatherPlatform02.json') as config_file:
    config = json.load(config_file)


Base = declarative_base()
engine = create_engine(config.get('SQL_URI'), echo = True)
Session = sessionmaker(bind = engine)
sess = Session()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    username = Column(Text)
    lat = Column(Float)
    lon = Column(Float)
    location_id = Column(Integer, ForeignKey('locations.id'),nullable = False)#one
    time_stamp_utc = Column(DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f'Users(id: {self.id}, usernam: {self.username}, city_name: {self.city_name})'


class Locations(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key = True)
    city = Column(Text)
    region = Column(Text)
    country = Column(Text)
    lat = Column(Float)
    lon = Column(Float)
    users = relationship('Users', backref = 'location', lazy = True)
    time_stamp_utc = Column(DateTime, nullable = False, default = datetime.utcnow)

# class Weather(db.Model):
class Weather(Base):
    __tablename__ = 'weather'
    id = Column(Integer, primary_key = True)
    time_stamp_utc = Column(DateTime, nullable=False, default=datetime.utcnow)
    lat = Column(Float)
    lon = Column(Float)
    city_location_name = Column(Text)
    region_name = Column(Text)
    country_name = Column(Text)
    tz_id = Column(Text)
    localtime_epoch = Column(Integer)
    localtime = Column(Text)

# Air Quality Endpoint
    co = Column(Float)# Carbon Monoxide (μg/m3)
    o3 = Column(Float)# Ozone (μg/m3)
    no2 = Column(Float)# Nitrogen dioxide (μg/m3)
    so2 = Column(Float)# Sulphur dioxide (μg/m3)
    pm2_5 = Column(Float)# PM2.5 (μg/m3)
    pm10 = Column(Float)# PM10 (μg/m3)
    us_epa_index = Column(Integer)#  	US - EPA standard. 
    gb_defra_index = Column(Integer)# UK Defra Index

# Realtime API i.e. this is the weather
    last_updated = Column(Text)
    last_updated_epoch = Column(Text)
    temp_c = Column(Float)
    temp_f = Column(Float)
    feelslike_c = Column(Float)
    feelslike_f = Column(Float)
    condition_text = Column(Text)
    condition_icon = Column(Text)
    condition_code = Column(Integer)
    wind_mph = Column(Float)
    wind_kph = Column(Float)
    wind_degree = Column(Integer)
    wind_dir = Column(String)
    pressure_mb = Column(Float)
    pressure_in = Column(Float)
    precip_mm = Column(Float)
    precip_in = Column(Float)
    humidity = Column(Integer)
    cloud = Column(Integer)
    is_day = Column(Integer)
    uv = Column(Float)
    gust_mph = Column(Float)
    gust_kph = Column(Float)

# Astronomy API
    sunrise = Column(Text)
    sunset = Column(Text)
    moonrise = Column(Text)
    moonset = Column(Text)
    moon_phase = Column(Text)
    moon_illumination = Column(Integer)

    note = Column(Text)
    
    def __repr__(self):
        return f"Weather(id: {self.id}, " \
            f"city_location_name: {self.city_location_name}, temp_c: {self.temp_c})"
