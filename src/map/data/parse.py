import json
from src.definitions import SETTINGS, ROOT_PATH

region_path = ROOT_PATH / "map/data/census_subdivisions.geojson"

with open(region_path) as region_geojson:
    census_subdivisions = json.load(region_geojson)
    region_geojson.close()

out_list = []

for feature in census_subdivisions["features"]:
    if feature["properties"]["PRNAME"] == "British Columbia / Colombie-Britannique":
        out_list.append(feature)

census_subdivisions["features"] = out_list

with open('census_subdivisions3.geojson', 'w') as outfile:
    json.dump(census_subdivisions, outfile)
    outfile.close()

# import geopandas as gpd
#
# data = gpd.read_file("census_subdivisions3.geojson").copy()
# print(data.crs)
# data.set_crs("+proj=lcc +lat_1=50 +lat_2=70 +lat_0=40 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +units=m no_defs", inplace=True, allow_override=True)
# print(data.crs)
# data.to_crs(epsg=4269, inplace=True)
# print(data.crs)
# data.to_file("census_subdivisions4.geojson", driver="GeoJSON")




