# https://towardsdatascience.com/data-science-for-cycling-how-to-read-gpx-strava-routes-with-python-e45714d5da23

import config
import gpxpy
import gpxpy.gpx

import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

with open('gpx_source/'+config.gpx_filename+'.gpx', 'r') as gpx_file:
	gpx = gpxpy.parse(gpx_file)


print(gpx.get_uphill_downhill())

print(gpx.get_elevation_extremes())

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
route_df.head()

print(route_df)

# convert to csv
route_df.to_csv('csv_export/'+config.gpx_filename+'.csv', index=False)



# plot a route

plt.figure(figsize=(14, 8))
plt.scatter(route_df['longitude'], route_df['latitude'], color='#101010')
plt.title('Route latitude and longitude points', size=20);

if config.save_plot:
    plt.savefig('plot_export/'+config.gpx_filename+'__track.png')

if config.show_plot:
    plt.show()
