# https://towardsdatascience.com/data-science-for-cycling-how-to-read-gpx-strava-routes-with-python-e45714d5da23

# import required module
import os
import config
import gpxpy
import gpxpy.gpx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False
 




# delete old files in csv folder
for filename in os.listdir(config.csv_dir):
    file_path = os.path.join(config.csv_dir, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))


# delete old plots
for filename in os.listdir(config.plot_export_dir+'01_track'):
    file_path = os.path.join(config.plot_export_dir+'01_track', filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))








# iterate over files in
for filename in os.listdir(config.gpx_dir):
    file = os.path.join(config.gpx_dir, filename)
    # checking if it is a file
    if os.path.isfile(file) and filename != '.DS_Store':
        

        filename_no_ext = os.path.splitext(filename)[0]

        gpx_open_path = file
        csv_export_path = 'csv_export/'+filename_no_ext+'.csv'
        plot_export_path = config.plot_export_dir+'01_track/'+filename_no_ext+'.png'

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
            #exit(0)










            # convert into panda df
            route_df = pd.DataFrame(route_info)
            route_df['elevation_diff'] = route_df['elevation'].diff()



            # calculate elevation & distance
            distances = [np.nan]
            for i in range(len(route_df)):
                if i == 0:
                    continue
                else:
                    distances.append(config.haversine_distance(
                        lat1=route_df.iloc[i - 1]['latitude'],
                        lon1=route_df.iloc[i - 1]['longitude'],
                        lat2=route_df.iloc[i]['latitude'],
                        lon2=route_df.iloc[i]['longitude']
                    ))
                    
            route_df['distance'] = distances

            route_df['cum_elevation'] = route_df['elevation_diff'].cumsum() 
            route_df['cum_distance'] = route_df['distance'].cumsum() 

            route_df = route_df.fillna(0)










            # calc gradients
            gradients = [np.nan]

            for ind, row in route_df.iterrows(): 
                if ind == 0 or row['distance'] == 0:
                    continue
                    
                grade = (row['elevation_diff'] / row['distance']) * 100
                
                if grade > 30:
                    gradients.append(np.nan)
                else:
                    gradients.append(np.round(grade, 1))



            route_df['gradient'] = gradients
            route_df['gradient'] = route_df['gradient'].interpolate().fillna(0)

            # round
            route_df = route_df.round({'gradient': 3})

            # exclude outliers
            lower = route_df.gradient.quantile(.05)
            upper = route_df.gradient.quantile(.95)
            route_df['gradient'] = route_df['gradient'].clip(lower=lower, upper=upper)

            #smoothing gradient
            route_df['gradient'] = route_df['gradient'].rolling(100, min_periods=1).mean()



            # round
            route_df = route_df.round({'elevation_diff': 3, 'distance': 3, 'cum_elevation': 3, 'cum_distance': 3, 'gradient': 3})


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

            plt.close()
            
            print(filename + ' done')

        except Exception:
            pass
            #print("An exception occurred:"+filename)
            #traceback.print_exc()
