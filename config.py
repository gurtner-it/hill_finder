import haversine as hs
import numpy as np

# assign directory
gpx_dir = '/Users/beatgurtner/Downloads/rides/'
#gpx_dir = '/Applications/MAMP/htdocs/hill_finder/gpx_source/'
csv_dir = '/Applications/MAMP/htdocs/hill_finder/csv_export/'
plot_export_dir = '/Applications/MAMP/htdocs/hill_finder/plot_export/'


show_plot = False
save_plot = True

def haversine_distance(lat1, lon1, lat2, lon2) -> float:
    distance = hs.haversine(
        point1=(lat1, lon1),
        point2=(lat2, lon2),
        unit=hs.Unit.METERS
    )
    return np.round(distance, 2)