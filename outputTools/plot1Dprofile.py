import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Function to read CSV and plot
def plot_1d_function_paraviewOutput(csv_file, fig=None, offset=0.0):
    if fig==None:
        fig= go.Figure()
    # Read the data from the CSV file
    df = pd.read_csv(csv_file)

    # Extract X and Y values
    x_values = df['arc_length'].values*1000.0 #convert to [mm]
    y_values = df['heat flux'].values / 1e6 #convert to [MW]

    # Add the line plot
    fig.add_trace(go.Scatter(x=x_values + offset, y=y_values, mode='lines', 
                             marker_symbol='square',  marker_size=8, name='HEAT Output'))


    return fig

# Function to read CSV and plot
def plot_1d_function_DIAGOutput(file, fig=None):
    if fig==None:
        fig= go.Figure()
    # Read the data from the CSV file
    data = np.genfromtxt(file, delimiter=' ').T
    # Extract X and Y values
    x_values = data[:,0]
    y_values = data[:,1]

    # Add the line plot
    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines+markers', 
                             marker_symbol='cross',  marker_size=8, name='IR Fit Function'))


    return fig



# Usage example
PVpath = '/home/tlooby/results/AUGvalidation/39231/HEAToutput/1D_temp_fRadDiv64_elmer.csv'  # Replace with your CSV file path
DIAGpath = '/home/tlooby/results/AUGvalidation/39231/diagnosticData/q_39231.txt'

offset = -16.167
fig = go.Figure()
fig = plot_1d_function_DIAGOutput(DIAGpath, fig)
fig = plot_1d_function_paraviewOutput(PVpath, fig, offset)

# Add labels and titles
fig.update_layout(
    title='1D Function Plot',
    xaxis_title='S [m]',
    yaxis_title='$MW/m^2$',
    font=dict(
        family="Arial",
        size=20,
        color="Black"
    ),
)
# Show plot
fig.show()

