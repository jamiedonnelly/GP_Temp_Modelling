import netCDF4 as nc 
import os 
import numpy as np 
import pandas as pd
import geopandas as gpd
import json

### Processing the tmax data to extract locations of interest 

# Show all files
root = './data/tmax/'
files = sorted([os.path.join(root,file) for file in os.listdir(root)])

# Extract first file 
testf = files[0]
test = nc.Dataset(testf)

## Data is structure such that many cells remain null/empty
## These cells always have a value of 1e+20
## Extract locations with non-null value 
## Extracts (i,j) indices for cells of interes
data = np.array(test['tasmax'][:])[0][::-1]
indices = []
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        if data[i,j]!=1e+20:
            indices.append((i,j))

## Lat/Long coords of whole domain
latvals = np.array(test['latitude'][:])[::-1] # [::-1] is added to orient the data correctly - it begins incorrectly oriented
lonvals = np.array(test['longitude'][:])[::-1]

## Extract coordinates of cells we care about 
latlong = []
for ix in indices:
    latlong.append([latvals[ix[0],ix[1]],lonvals[ix[0],ix[1]]])

## values in dataframe containing index, array indices and lat/long coords
locs_df = pd.DataFrame(index=[i for i in range(len(latlong))],columns=['x','y','latitude','longitude'])
for i,ll in enumerate(latlong):
    locs_df.loc[i,:] = [indices[i][0],indices[i][1],np.round(ll[0],3),np.round(ll[1],3)]

## Create dictionary mapping from (i,j) array indices to latlong
colnum_to_latlong = {}
for i, ix in enumerate(indices):
    colnum_to_latlong[str(i)] = [ix[0],ix[1]]
with open("./data/colnum_to_latlong.json","wb") as f:
    json.dump(colnum_to_latlong,f)

## Use geopands to create shapefile highlighting these locations 
gdf = gdf.GeoDataFrame(geometry=gpd.points_from_xy(locs_df.longitude,locs_df.latitude))
gdf.set_crs('epsg:4326',inplace=True)

## Save to .shp 
shp_fname = './data/qgis/uk_grid_points.shp'
gdf.to_file(shp_fname,driver="ESRI Shapefile")

