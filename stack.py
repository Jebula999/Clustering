from operator import index
import numpy as np
import pandas as pd
import math
import time
import os
import itertools

clusters = []
latarray = np.array([])
longarray = np.array([])
start_time = time.time()
temp_time = time.time()
meters = 10
LatDegPerMeter = 0.000008999
LatDeg = meters*LatDegPerMeter
LongDegPerMeter = 0.000010844
LongDeg = meters*LongDegPerMeter

pokestops = pd.read_csv("pokestops.csv", header=None)
pokestops.columns = ["Lat", "Long"]
LocLatMin = pokestops["Lat"].min()
LocLatMax = pokestops["Lat"].max()
LocLongMin = pokestops["Long"].min()
LocLongMax = pokestops["Long"].max()

latiterations = math.ceil((LocLatMax-LocLatMin)/(LatDeg))
longiterations = math.ceil((LocLongMax-LocLongMin)/(LongDeg))

print("Find all coordinates for the locations df")
print("Total Loops Required: " + str(latiterations*longiterations*len(pokestops)))
locations = pd.DataFrame(itertools.product(np.arange(latiterations)*LatDeg + LocLatMin, np.arange(longiterations)*LongDeg + LocLongMin), columns=["Lat", "Long"])
print("%s seconds" % (time.time() - temp_time))
print("")

locations["Count"] = 0

def haversine_np_matrix(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    lon1 = np.expand_dims(lon1, axis=0)
    lat1 = np.expand_dims(lat1, axis=0)
    lon2 = np.expand_dims(lon2, axis=1)
    lat2 = np.expand_dims(lat2, axis=1)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km
print("Calculating Distance Table")
temp_time = time.time()
distances = haversine_np_matrix(pokestops["Long"],pokestops["Lat"], locations["Long"],locations["Lat"])
print("%s seconds" % (time.time() - temp_time))
print("")

print("Creating Distance Table")
temp_time = time.time()
locations = locations.join(pd.DataFrame(distances))
print("%s seconds" % (time.time() - temp_time))
print("")

print("Removing Distances < 70m")
temp_time = time.time()
locations[locations.iloc[:, 3:] > 0.07] = np.NaN
print("%s seconds" % (time.time() - temp_time))
print("")

print("Counting number of Nearby locations")
temp_time = time.time()
locations["Count"] = locations.iloc[:, 3:].count(axis="columns")
print("%s seconds" % (time.time() - temp_time))
print("")

print("Sorting by location count")
temp_time = time.time()
locations.sort_values("Count", ascending=False, inplace=True)
print("%s seconds" % (time.time() - temp_time))
print("")

print("Saving Top 20 Locations")
temp_time = time.time()
top20 = locations.iloc[0:20, 0:3]
if os.path.exists("Top 20 Locations.txt"):
    os.remove("Top 20 Locations.txt")
with open("Top 20 Locations.txt", 'a') as f:
    dfAsString = top20.to_string(header=True, index=True)
    f.write(dfAsString)
print("%s seconds" % (time.time() - temp_time))
print("")

print("Removing all 0 distance locations from Database")
temp_time = time.time()
locations.drop(locations.index[locations["Count"] == 0], inplace=True)
print("%s seconds" % (time.time() - temp_time))
print("")

print("Running the filtering algorithm")
temp_time = time.time()
while len(locations) > 0:
    #Count number of locations
    locations["Count"] = locations.iloc[:, 3:].count(axis="columns")
    #Remove all 0 locations
    locations.drop(locations.index[locations["Count"] == 0], inplace=True)
    #Sort by count
    locations.sort_values("Count", ascending=False, inplace=True)
    if len(locations) == 0:
        break
    #Add top entry to final clusters array
    clusters = np.append(clusters, locations.iloc[0 , 0:2])
    #Remove all columns that contain pokestops in first row from df
    locations = locations[locations.columns[[True]*3 + list(locations.iloc[0].isna()[3:])]]
    #Remove top entry from df
    locations.drop(index=locations.index[0], axis=0, inplace=True)
print("%s seconds" % (time.time() - temp_time))
print("")

print("Saving Locations to Array")
temp_time = time.time()
clusters = np.reshape(clusters, (-1,2))
print("%s seconds" % (time.time() - temp_time))
print("")

print("Writing final Clustered Spawnpoints to file")
temp_time = time.time()
if os.path.exists("Clustered_Spawnpoints.txt"):
    os.remove("Clustered_Spawnpoints.txt")
np.savetxt("Clustered_Spawnpoints.txt", np.array(clusters), delimiter=',', fmt='%1.8f')
print("%s seconds" % (time.time() - temp_time))
print("")

print("Total Time Taken: %s Seconds" % (time.time() - start_time))