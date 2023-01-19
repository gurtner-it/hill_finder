# https://betterdatascience.com/data-science-for-cycling-calculate-route-gradients-from-strava-gpx

import config
import gpxpy
import gpxpy.gpx

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import haversine as hs

import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False


plt.rcParams['figure.figsize'] = (16, 6)
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False



def haversine_distance(lat1, lon1, lat2, lon2) -> float:
    distance = hs.haversine(
        point1=(lat1, lon1),
        point2=(lat2, lon2),
        unit=hs.Unit.METERS
    )
    return np.round(distance, 2)



with open('gpx_source/'+config.gpx_filename+'.gpx', 'r') as gpx_file:
    gpx = gpxpy.parse(gpx_file)


#print(gpx.get_uphill_downhill())

#print(gpx.get_elevation_extremes())

#print(gpx.get_track_points_no())

#print(gpx.tracks[0].segments[0].points[:10])

route_info = []

for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            route_info.append({
                'latitude': point.latitude,
                'longitude': point.longitude,
                'elevation': point.elevation
            })

#print(route_info)

# convert into panda df
route_df = pd.DataFrame(route_info)
route_df['elevation_diff'] = route_df['elevation'].diff()

distances = [np.nan]
for i in range(len(route_df)):
    if i == 0:
        continue
    else:
        distances.append(haversine_distance(
            lat1=route_df.iloc[i - 1]['latitude'],
            lon1=route_df.iloc[i - 1]['longitude'],
            lat2=route_df.iloc[i]['latitude'],
            lon2=route_df.iloc[i]['longitude']
        ))
        
route_df['distance'] = distances

route_df['cum_elevation'] = route_df['elevation_diff'].cumsum() 
route_df['cum_distance'] = route_df['distance'].cumsum() 

route_df = route_df.fillna(0)

# round
route_df = route_df.round({'elevation_diff': 3, 'distance': 3, 'cum_elevation': 3, 'cum_distance': 3})

route_df.head()

print(route_df)


route_df.to_csv('csv_export/'+config.gpx_filename+'.csv', index=False)


plt.plot(route_df['cum_distance'], route_df['cum_elevation'], color='#101010', lw=3)
plt.title('Route elevation profile', size=20)
plt.xlabel('Distance in meters', size=14)
plt.ylabel('Elevation in meters', size=14);

if config.save_plot:
    plt.savefig('plot_export/'+config.gpx_filename+'__elevation.png')

if config.show_plot:
    plt.show()
