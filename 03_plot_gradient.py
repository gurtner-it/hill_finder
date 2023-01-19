# https://betterdatascience.com/data-science-for-cycling-calculate-route-gradients-from-strava-gpx

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
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False



route_df = pd.read_csv('csv_export/'+config.gpx_filename+'.csv')
route_df.head()

#print(route_df)

gradients = [np.nan]

for ind, row in route_df.iterrows(): 
    if ind == 0:
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
route_df = route_df.clip(lower=lower, upper=upper)

#smoothing gradient
route_df['gradient'] = route_df['gradient'].rolling(100, min_periods=1).mean()


# plot
plt.title('Terrain gradient on the route', size=20)
plt.xlabel('Data point', size=14)
plt.ylabel('Gradient (%)', size=14)
plt.plot(np.arange(len(route_df)), route_df['gradient'], lw=1, color='#101010');


if config.save_plot:
    plt.savefig('plot_export/'+config.gpx_filename+'__gradient.png')

if config.show_plot:
    plt.show()

route_df.to_csv('csv_export/'+config.gpx_filename+'.csv', index=False)


