from pymongo import MongoClient
import datetime
import json

def create_places_data_states(db):

  places_collection = db.places

  states_list = ['Andhra Pradesh',
  'Arunachal Pradesh',
  'Assam',
  'Bihar',
  'Chhattisgarh',
  'Goa',
  'Gujarat',
  'Haryana',
  'Himachal Pradesh',
  'Jharkhand',
  'Karnataka',
  'Kerala',
  'Madhya Pradesh',
  'Maharashtra',
  'Manipur',
  'Meghalaya',
  'Mizoram',
  'Nagaland',
  'Odisha',
  'Punjab',
  'Rajasthan',
  'Sikkim',
  'Tamil Nadu',
  'Telangana',
  'Tripura',
  'Uttar Pradesh',
  'Uttarakhand',
  'West Bengal']

  states_info = [{'name': state, 'type': 'State', 'attributes': [], 'keywords': []} for state in states_list]

  # states_info_json = json.dumps(states_info, indent=4)

  resp = places_collection.insert_many(states_info)
  print(resp)

  # print(states_info_json)



def create_places_data_ut(db):

  places_collection = db.places

  ut_list = [
    'Andaman and Nicobar Islands',
    'Dadra and Nagar Haveli and Daman and Diu',
    'Chandigarh',
    'Lakshadweep',
    'Puducherry',
    'Delhi',
    'Ladakh',
    'Jammu and Kashmir'
  ]

  ut_info = [{'name': ut, 'type': 'UT', 'attributes': [], 'keywords': []} for ut in ut_list]

  resp = places_collection.insert_many(ut_info)
  print(resp)


if __name__ == '__main__':

  client = MongoClient('mongodb://localhost:27017/')

  db = client.tours_database

  # create_places_data_states(db)
  # create_places_data_ut(db)
