# https://betterdatascience.com/data-science-for-cycling-calculate-route-gradients-from-strava-gpx

# import required module
import os
import config
import gpxpy
import gpxpy.gpx
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False
plt.rcParams['figure.figsize'] = (16, 6)


# delete old plots
for filename in os.listdir(config.plot_export_dir+'02_elevation'):
    file_path = os.path.join(config.plot_export_dir+'02_elevation', filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))



# iterate over files in
for filename in os.listdir(config.csv_dir):
    file = os.path.join(config.csv_dir, filename)
    # checking if it is a file
    if os.path.isfile(file) and filename != '.DS_Store':
        #print(filename)

        filename_no_ext = os.path.splitext(filename)[0]

        gpx_open_path = file
        csv_export_path = 'csv_export/'+filename_no_ext+'.csv'
        plot_export_path = 'plot_export/track/'+filename_no_ext+'.png'

        try:

            route_df = pd.read_csv(file)
            route_df.head()

            plt.plot(route_df['cum_distance'], route_df['cum_elevation'], color='#101010', lw=3)
            plt.title('Route elevation profile', size=20)
            plt.xlabel('Distance in meters', size=14)
            plt.ylabel('Elevation in meters', size=14);

            if config.save_plot:
                plt.savefig('plot_export/02_elevation/'+filename_no_ext+'.png')

            if config.show_plot:
                plt.show()
            
            plt.close()

        except:
            print("An exception occurred:"+filename)
            traceback.print_exc()
