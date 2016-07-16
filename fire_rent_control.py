#read rent_control.geojson
#we want percent of fires that are rent control

########################### CURRENT TASKS ########################### 
# 1. Get percentage of fires that are rent-controlled w/ loss-thresh#
# 2. Get percentage of fires that are rent-controlled w/ zipcode ####
# 3. Create graphs of threshold vs. percentage of rent-controlled ###
# 4. TODO (DONE): get all zipcodes and find percentages of r-controll
# led fires for each one given a specific threshold #################
# 5. TODO: 
#####################################################################

import json
from sets import Set
import csv
import matplotlib.pyplot as plt
import numpy as np

rent_control = '/home/husayn/Projects/eviction_mapping/data/rent_control.geojson'
fire_map = '/home/husayn/Projects/eviction_mapping/data/fire_map_2016_good.csv'

#get all the rent-control apartments
with open(rent_control) as f:
    data = json.load(f)

#get all the fire data and put it in the set fire_addresses
unique_zips = []
with open(fire_map, 'rb') as f:
    reader = csv.DictReader(f)
    fire_addresses = []
    for i,row in enumerate(reader):
        if i>=1:
            if (len(row['losses']) > 1):
                if (int(row['losses'][1:].replace(',',''))>1000):
                    fire_addresses.append(row['address'])
                    if (row['zip'] not in unique_zips):
                        unique_zips.append(row['zip'])
print("unique zip length: ", len(unique_zips))
print("fire addresses length: ", len(fire_addresses))

#returns fire_addresses array for differeent loss_thresh's --> TODO: shouldn't this take in addresses and then filter those instead of the entire file? --> actually nevermind, for this to get the entire dataset, just pass 0. THIS NEEDS TO RETURN THE ROW ALSO, NOT JUST THE ADDRESS!!
def populate_addresses(loss_thresh):
    with open(fire_map, 'rb') as f:
        reader = csv.DictReader(f)
        fire_addresses = []
        for i,row in enumerate(reader):
            if i>=1:
                if (len(row['losses']) > 1):
                    if (int(row['losses'][1:].replace(',',''))>loss_thresh):
                        fire_addresses.append(row['address'])
    return fire_addresses

#returns fire addresses within these zipcodes --> can intersect fires with this -->overloads populate_addresses so that we can have specific zipcodes and not just all of them. this should also take a list of zipcodes not just one
def zipcode_restrict(zipcode_spec, loss_thresh):
    with open(fire_map, 'rb') as f:
        reader = csv.DictReader(f)
        zip_restrict = []
        for i,row in enumerate(reader):
            if i>=1:
                if (len(row['losses']) > 1):
                    if (int(row['losses'][1:].replace(',',''))>loss_thresh and zipcode_spec == row['zip']):
                        zip_restrict.append(row['address'])
    return zip_restrict

#parsing the geojson data
rent_addresses = []
total_addresses = 0
blk_lot = []
for (i,feature) in enumerate(data['features']):
    #for key in feature['properties'].keys():
    #    print key
    #print feature
    if i==1:
        print feature['properties'].keys()
    if all(x in feature['properties'].keys() for x in ['latitude', 'longitude']):
            #rent_addresses.add(feature['properties']['address']) --> this is for sets
            rent_addresses.append(feature['properties']['address'])

intersection = list(set(fire_addresses).intersection(rent_addresses))
print('length of intersection is ', len(intersection))
percentage = float(float(len(intersection))/len(fire_addresses))
print(percentage)

#this generates percentages based off of loss_threshold for *all* of SF
"""
xs = []
ys = []
for i in range(100):
    fire_addresses_cb = populate_addresses(i*100)
    intersection_2 = list(set(fire_addresses_cb).intersection(rent_addresses))
    ys.append(float(float(len(intersection_2))/len(fire_addresses_cb)))
    xs.append(i*100)
print ys
plt.plot(xs, ys)
plt.show()

print xs[:20]
print ys[:20]
"""

#this generates percentages for each zipcode in SF. It also happens to run extremely fucking slowly
for (y,zip) in enumerate(unique_zips):
    print zip
    xs = []
    ys = []
    for i in range(100):
        fire_addresses_cb = zipcode_restrict(zip, i*100)
        intersection_2 = list(set(fire_addresses_cb).intersection(rent_addresses))
        if (len(fire_addresses_cb) == 0):
            ys.append(0)
        else:
            ys.append(float(float(len(intersection_2))/len(fire_addresses_cb)))
        xs.append(i*100)
    #print ys
    plt.plot(xs, ys)
    filename = '/home/husayn/Projects/eviction_mapping/correlation_mapping/fire/figures/' + str(zip)
    plt.savefig(filename)
    plt.clf()
    
print 'goodbye'
