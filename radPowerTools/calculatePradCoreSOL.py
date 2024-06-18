#calculates radiation power outside of separatrix from EQ and an emission profile (R,Z)
#Engineer:      T Looby
#Date:          20240617

import sys
import shutil
import numpy as np
import scipy.interpolate as interp
from shapely.geometry import Point, Polygon
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

EFITPath = '/home/tlooby/source'
HEATPath = '/home/tlooby/source/HEAT/github/source'
sys.path.append(EFITPath)
sys.path.append(HEATPath)


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
NR = len(R)
NZ = len(Z)


#if you want to eliminate noise floor points, use this line
noise = np.where(P<0)
P[noise] = 0.0
#Normalize to 1
#P /= np.sum(P)

#if we want to only include points within the rlim,zlim from a GEQDSK, 
#set this flag to true
limBound = True
if limBound == True:
    import MHDClass
    gFile = '/home/tlooby/HEATruns/AUG/validation39231_Tom_v2/aug/39231_3.000.eqdsk'
    MHD = MHDClass.setupForTerminalUse(gFile=gFile)
    ep = MHD.ep

    # Create a Polygon object from the contour points
    contour_polygon = Polygon(ep.g['lcfs'])

    # Define the distance threshold in [m]
    dist_threshold = 0.004

    points = np.stack((R.flatten(), Z.flatten())).T

    # Check if points in the pointcloud are inside the contour and calculate distances
    #to the contour.  only include points inside the contour and points that are further
    #than dist_threshold from the contour.
    valid_points = []
    for point in points:
        p = Point(point)
        inside = contour_polygon.contains(p)
        distance = contour_polygon.exterior.distance(p)
        valid_points.append(inside and distance > dist_threshold)

    inside = np.array(valid_points)

else:
    inside= np.ones((NZ*NR))*True

coreUse = np.where(inside == True)[0]
SOLuse = np.where(inside == False)[0]
print(len(SOLuse))
print(len(R))


#Total power
P_rad = np.sum(P)

#calculate power outside separatrix
P_rad_core = np.sum(P[coreUse])

#power radiated in core
P_rad_SOL = P_rad - P_rad_core

print("Total Radiated Power: {:f} [MW]".format(P_rad))
print("SOL Radiated Power: {:f} [MW]".format(P_rad_SOL))
print("Core Radiated Power: {:f} [MW]".format(P_rad_core))


#if you want to calculate the power in a bounding box
#define bounding box [m]
rMin = 1.1
rMax = 1.65
zMin = -1.2
zMax = -0.7
boxR = np.where(np.logical_and(R>rMin, R<rMax))[0]
boxZ = np.where(np.logical_and(Z>zMin, Z<zMax))[0]
boxUse = np.intersect1d(boxR, boxZ)
P_rad_box = np.sum(P[boxUse])
print("Total Box Power: {:f}".format(np.sum(P[boxUse])))



fig = make_subplots(rows=1, cols=3, subplot_titles=("Core: {:0.2f}".format(P_rad_core), 
                                                    "SOL: {:0.2f}".format(P_rad_SOL), 
                                                    "Box: {:0.2f}".format(P_rad_box)))

# Calculate the bounds
x_min = min(R.min(), R.min())
x_max = max(R.max(), R.max())
y_min = min(Z.min(), Z.min())
y_max = max(Z.max(), Z.max())

# Inside Contour plot
fig.add_trace(
    go.Scatter(
        x=R[coreUse],
        y=Z[coreUse],
        mode='markers',
        marker=dict(
            size=10,
            color=P[coreUse],
            colorscale='jet',
            colorbar=dict(title='P [MW]'),
        ),
        name='Inside Core'
    ),
    row=1, col=1
)

# Outside Contour plot
fig.add_trace(
    go.Scatter(
        x=R[SOLuse],
        y=Z[SOLuse],
        mode='markers',
        marker=dict(
            size=10,
            color=P[SOLuse],
            colorscale='jet',
            colorbar=dict(title='P [MW]'),
        ),
        name='Outside Core'
    ),
    row=1, col=2
)

fig.add_trace(
    go.Scatter(
        x=R[boxUse],
        y=Z[boxUse],
        mode='markers',
        marker=dict(
            size=10,
            color=P[boxUse],
            colorscale='jet',
            colorbar=dict(title='P [MW]'),
        ),
        name='Box'
    ),
    row=1, col=3
)


# Update layout for the plots
fig.update_layout(
    showlegend=False,
    #title='Emission Profile Inside and Outside Core',
    #paper_bgcolor='rgba(0,0,0,0)',
    #plot_bgcolor='rgba(0,0,0,0)'
)
# Update axes with the same range
fig.update_xaxes(title_text="R [m]", range=[x_min, x_max], row=1, col=1)
fig.update_yaxes(title_text="Z [m]", range=[y_min, y_max], row=1, col=1, )

fig.update_xaxes(title_text="R [m]", range=[x_min, x_max], row=1, col=2)
fig.update_yaxes(title_text="Z [m]", range=[y_min, y_max], row=1, col=2,)

fig.update_xaxes(title_text="R [m]", range=[x_min, x_max], row=1, col=3)
fig.update_yaxes(title_text="Z [m]", range=[y_min, y_max], row=1, col=3,)



# Show plot
fig.show()