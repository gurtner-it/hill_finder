# https://towardsdatascience.com/data-science-for-cycling-how-to-read-gpx-strava-routes-with-python-e45714d5da23

# import required module
import os
import config
import gpxpy
import gpxpy.gpx
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False
 
# iterate over files in
for filename in os.listdir(config.directory):
    file = os.path.join(config.directory, filename)
    # checking if it is a file
    if os.path.isfile(file) and filename != '.DS_Store':
        #print(filename)

        filename_no_ext = os.path.splitext(filename)[0]

        #gpx_open_path = 'gpx_source/'+config.gpx_filename+'.gpx'
        #csv_export_path = 'csv_export/'+config.gpx_filename+'.csv'
        #plot_export_path = 'plot_export/'+config.gpx_filename+'__track.png'

        gpx_open_path = file
        csv_export_path = 'csv_export/'+filename_no_ext+'.csv'
        plot_export_path = 'plot_export/track/'+filename_no_ext+'.png'

        try:
            with open(gpx_open_path, 'r') as gpx_file:
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
            route_df.head()

            print(route_df)

            # convert to csv
            route_df.to_csv(csv_export_path, index=False)



            # plot a route
            plt.figure(figsize=(14, 8))
            plt.scatter(route_df['longitude'], route_df['latitude'], color='#101010')
            plt.title('Route latitude and longitude points', size=20);

            if config.save_plot:
                plt.savefig(plot_export_path)

            if config.show_plot:
                plt.show()

        except:
            print("An exception occurred")
