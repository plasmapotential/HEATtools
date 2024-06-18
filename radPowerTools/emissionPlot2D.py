import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.interpolate import griddata


#radPath = '/home/tlooby/HEATruns/AUG/validation39231_Tom_v2/aug/'
radPath = '/home/tlooby/HEATruns/AUG/validation40240_Tom_v1/aug/'

#f = radPath + 'P_RZ_39231_interpolated_1600pts_box.csv'
#f = radPath + 'P_RZ_39231_interpolated_485pts_box_1.65MW.csv'
#f = radPath + '39231_RZpower.csv'
f = radPath + '40240_RZpower.csv'
#f = radPath + 'input_rad_39231.csv'
# Read the data from the CSV file
df = pd.read_csv(f)

# Ensure the CSV file has columns named 'R', 'Z', and 'P'
R = df['# R[m]'].values
Z = df['Z[m]'].values * -1.0
P = df['P[MW]'].values

#if you want to eliminate noise floor points, use this line
noise = np.where(P<0)
P[noise] = 0.0


print("Total power before Normalizing = {:f}[MW]".format(np.sum(P)))

P/=np.sum(P)

print("Total power after normalizing = {:f}[MW]".format(np.sum(P)))

## Create grid values first
#grid_x, grid_y = np.mgrid[min(R):max(R):100j, min(Z):max(Z):100j]
## Interpolate unstructured D-dimensional data.
#grid_z = griddata((R, Z), P, (grid_x, grid_y), method='linear')


# Create the 2D plot using Plotly
fig = go.Figure(data =
    go.Contour(
        z = P,
        x = R,
        y = Z,
        colorscale='plasma',
        line_width=0,
    )
)

# Add labels and titles
fig.update_layout(
    title='Emission Profile',
    xaxis_title='R [m]',
    yaxis_title='Z [m]',
)

fig.update_yaxes(scaleanchor="x",scaleratio=1,)
# Show plot
fig.show()