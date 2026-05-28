import pickle
import pandas as pd

with open('search_df.pkl', 'rb') as f:
    search_df = pickle.load(f)

print(f"Loaded search_df with {len(search_df)} rows")

def search_location(user_input, limit=10):
    
    query = user_input.strip().lower()
    

    if len(query) == 0:
        return []
    

    #find the query from the search df
    mask = search_df['search_term'].str.startswith(query, na=False)
    results = search_df[mask].copy()
    
    if len(results) == 0:
        return []
    
    # deop suplicate locations with same geo id
    results = results.drop_duplicates(subset='geonameid')
    results = results.sort_values('population', ascending=False, na_position='last')
    
    output = []
    for i in range(len(results.head(limit))):
        row = results.iloc[i]
        
        if row['entity_type'] == 'state':
            entry = {
                
                'entity_type': 'state',
                'entity_name': row['entity_name'],
                'latitude':    row['latitude'],
                'longitude':   row['longitude']
            }
        
        elif row['entity_type'] == 'city':
            entry = {
                'entity_type': 'city',
                'entity_name': str(row['entity_name']) + ', ' + str(row['state']),
                'latitude':    row['latitude'],
                'longitude':   row['longitude'],
                'normalized': {
                    'geoId':     str(row['geonameid']),
                    'city':      row['city'],
                    'state':     row['state'],
                    'latitude':  row['latitude'],
                    'longitude': row['longitude']
                }
            }
        
        elif row['entity_type'] == 'pincode':
            entry = {
                'entity_type': 'pincode',
                'entity_name': row['pincode'],
                'latitude':    row['latitude'],
                'longitude':   row['longitude'],
                'normalized': {
                    'geoId':     None,
                    'city':      row['city'],
                    'state':     row['state'],
                    'pincode':   row['pincode'],
                    'latitude':  row['latitude'],
                    'longitude': row['longitude']
                }
            }
        
        output.append(entry)
    
    return output

import json
print("\n test pincode ")
print(json.dumps(search_location("208"), indent=2, default=str))

# print("\n test city")
# print(json.dumps(search_location("mumb"), indent=2, default=str))

# print("\n test state")
# print(json.dumps(search_location("west b"), indent=2, default=str))