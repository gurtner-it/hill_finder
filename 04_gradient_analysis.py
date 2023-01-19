# https://betterdatascience.com/data-science-for-cycling-gradient-ranges/

# import required module
import os
import config
import gpxpy
import gpxpy.gpx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import haversine as hs
import plotly.graph_objects as go
import plotly.offline as pyo

plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False
plt.rcParams['figure.figsize'] = (16, 6)

# delete old plots
for filename in os.listdir(config.plot_export_dir+'04_gradient_analysis'):
    file_path = os.path.join(config.plot_export_dir+'04_gradient_analysis', filename)
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

            #print(route_df['gradient'].describe())

            # create gradient bins
            bins = pd.IntervalIndex.from_tuples([
                (-30, -2),
                (-2, 2), 
                (2, 5), 
                (5, 10), 
                (10, 15), 
                (15, 20), 
                (20, 100)
            ], closed='left')

            route_df['gradient_range'] = pd.cut(route_df['gradient'], bins=bins)
            route_df.head()


            # round
            route_df = route_df.round({'gradient_range': 3})

            #print(bins)




            gradient_details = []

            # For each unique gradient range
            for gr_range in route_df['gradient_range'].unique():
                # Keep that subset only
                subset = route_df[route_df['gradient_range'] == gr_range]
                
                # Statistics
                total_distance = subset['distance'].sum()
                pct_of_total_ride = (subset['distance'].sum() / route_df['distance'].sum()) * 100
                elevation_gain = subset[subset['elevation_diff'] > 0]['elevation_diff'].sum()
                elevation_lost = subset[subset['elevation_diff'] < 0]['elevation_diff'].sum()
                
                # Save results
                gradient_details.append({
                    'gradient_range': gr_range,
                    'total_distance': np.round(total_distance, 2),
                    'pct_of_total_ride': np.round(pct_of_total_ride, 2),
                    'elevation_gain': np.round(elevation_gain, 2),
                    'elevation_lost': np.round(np.abs(elevation_lost), 2)
                })



            gradient_details_df = pd.DataFrame(gradient_details).sort_values(by='gradient_range').reset_index(drop=True)


            # Statistics for each gradient range
            print(gradient_details_df)


            # round
            gradient_details_df = gradient_details_df.round(3)





            #plot
            colors = [
                '#0d46a0', '#2f3e9e', '#2195f2', '#4fc2f7',
                '#a5d6a7', '#66bb6a', '#fff59d', '#ffee58',
                '#ffca28', '#ffa000', '#ff6f00', '#f4511e', '#bf360c'
            ]

            custom_text = [f'''<b>{gr}%</b> - {dst}km''' for gr, dst in zip(
                gradient_details_df['gradient_range'].astype('str'),
                gradient_details_df['total_distance'].apply(lambda x: round(x / 1000, 2))
            )]

            fig = go.Figure(
                data=[go.Bar(
                    x=gradient_details_df['gradient_range'].astype(str),
                    y=gradient_details_df['total_distance'].apply(lambda x: round(x / 1000, 2)),
                    marker_color=colors,
                    text=custom_text
                )],
                layout=go.Layout(
                    bargap=0,
                    title='Gradient profile of a route',
                    xaxis_title='Gradient range (%)',
                    yaxis_title='Distance covered (km)',
                    autosize=False,
                    width=1440,
                    height=800,
                    template='simple_white'
                )
            )

            if config.save_plot:
                fig.write_image('plot_export/04_gradient_analysis/'+filename_no_ext+'.png')

            if config.show_plot:
                fig.show()

        except:
            print("An exception occurred:"+filename)
            traceback.print_exc()
