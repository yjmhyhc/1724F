import plotly.figure_factory as ff
import geopandas as gpd
from geopy.distance import geodesic

def haversine_distance(la1, lo1, la2, lo2):
    cor_point1 = la1, lo1
    cor_point2 = la2, lo2
    return geodesic(cor_point1, cor_point2).meters

def within_range(haversine_distance):
    return haversine_distance <= 10000

def should_discard(row):
    x = row['geometry'].x
    y = row['geometry'].y
    return  within_range(haversine_distance(43.7906646, -79.3028889, y, x))

#gain the hexagonal binning map of traffic accidents reported around a certain point

# Import polygons for Canadian provinces and concatenate to traffic statistics
# Define the raw URL
url = "https://raw.githubusercontent.com/yjmhyhc/1724F/main/residential.geojson"

# Read the GeoJSON into a GeoDataFrame
ksi = gpd.read_file(url)

#data washing (exclude points that are outside the range)
filtered_ksi = ksi[ksi.apply(should_discard, axis=1)]

# define the center
center = (43.7906646,-79.3028889)

# use create_hexbin_mapbox to create Hexbin Mapbox
fig = ff.create_hexbin_mapbox(
    data_frame=filtered_ksi,
    lat=filtered_ksi['geometry'].y,
    lon=filtered_ksi['geometry'].x,
    nx_hexagon=10,
    opacity=0.5,
    min_count=1,
    labels={'color': 'Residence Number'},
    color_continuous_scale='turbo'
)

fig.update_layout(
    mapbox_style="stamen-terrain",
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    mapbox={'center': {'lat': center[0], 'lon': center[1]}, 'zoom': 13}
)
fig.show()
