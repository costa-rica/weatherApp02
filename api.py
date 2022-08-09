from flask import Flask, request
import json
from models import sess, Users, Locations

app = Flask(__name__)

with open(r'C:\Users\captian2020\Documents\config_files\config_weatherPlatform02.json') as config_file:
    config = json.load(config_file)

class ConfigDev:
    DEBUG = True
    SECRET_KEY = config.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = config.get('SQL_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WEATHER_API_KEY = config.get('WEATHER_API_KEY')

app.config.from_object(ConfigDev())

@app.route('/add_user', methods = ['GET', 'POST'])
def add_user():
    request_data = request.get_json()
    min_loc_distance_difference = 1000

    users = sess.query(Users).all()

    for user in users:
        if request_data.get('username') == user.username:
            return 'User already exists'
    
    try:
        add_user_dict = {}
        add_user_dict['username'] = request_data.get('username')
        add_user_dict['lat'] = request_data.get('lat')
        add_user_dict['lon'] = request_data.get('lon')
        add_user_dict['location_id'] = ''
        new_user = Users(**add_user_dict)
        sess.add(new_user)
        sess.commit()

    except:
        return f"Something is wrong with the data you tried to add to the database."

    # Check Locations table to see if user's location already exists
    locations_unique_list = sess.query(Locations).all()
    for loc in locations_unique_list:
        lat_diff = abs(float(request_data.get('lat')) - loc.lat)
        lon_diff = abs(float(request_data.get('lon')) - loc.lon)
        loc_dist_diff = lat_diff + lon_diff

        if loc_dist_diff < min_loc_distance_difference:
            min_loc_distance_difference = loc_dist_diff
            location_id = loc.id
        
    if min_loc_distance_difference < .1:
        new_user = sess.query(Users).filter_by(username = request_data.get('username')).first()
        new_user.location_id = location_id
        sess.commit()
        return f"{request_data.get('username')} added succesfully!"

    else:
    # coordinates not found in Location and add coordinates as new location
        new_loc_dict = {}
        new_loc_dict['city'] = request_data.get('city')
        new_loc_dict['region'] = request_data.get('region')
        new_loc_dict['country'] = request_data.get('country')
        new_loc_dict['lat'] = request_data.get('lat')
        new_loc_dict['lon'] = request_data.get('lon')

        new_location = Locations(**new_loc_dict)
        sess.add(new_location)
        sess.commit()

        just_added_location = sess.query(Locations).filter_by(lat = request_data.get('lat'),
            lon = request_data.get('lon')).first()

        new_user = sess.query(Users).filter_by(username = request_data.get('username')).first()
        new_user.location_id = just_added_location.id
        sess.commit()

        return f"{request_data.get('username')} and new location added succesfully!"


if __name__ == '__main__':
    app.run()