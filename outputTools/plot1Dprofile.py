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
    #y_values = df['$MW/m^2$'].values #convert to [MW]

    # Add the line plot
    fig.add_trace(go.Scatter(x=x_values + offset, y=y_values, mode='lines', 
                             marker_symbol='square',  marker_size=8, name='HEAT Output'))


    return fig

# Function to read CSV and plot
def plot_1d_function_DIAGOutput(file, fig=None, qBG = 0.0):
    if fig==None:
        fig= go.Figure()
    # Read the data from the CSV file
    data = np.genfromtxt(file, delimiter=' ').T
    # Extract X and Y values
    x_values = data[:,0]
    y_values = data[:,1] + qBG

    # Add the line plot
    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines+markers', 
                             marker_symbol='cross',  marker_size=8, name='AUG IR Chord'))


    return fig



# Usage example
#PVpath = '/home/tlooby/results/AUGvalidation/40240/HEAToutput/1D_HF_v3.csv'  # Replace with your CSV file path
#DIAGpath = '/home/tlooby/results/AUGvalidation/40240/diagnosticData/q_40240.txt'
PVpath = '/home/tlooby/results/AUGvalidation/39231/HEAToutput/1D_HF_v4.csv'  # Replace with your CSV file path
DIAGpath = '/home/tlooby/results/AUGvalidation/39231/diagnosticData/q_39231.txt'




offset = -40.223 #[mm]
qBG = 0.1 #[MW/m2]


fig = go.Figure()
fig = plot_1d_function_DIAGOutput(DIAGpath, fig, qBG)
fig = plot_1d_function_paraviewOutput(PVpath, fig, offset)

# Add labels and titles
fig.update_layout(
    title='1D Function Plot',
    xaxis_title='S [mm]',
    yaxis_title='$MW/m^2$',
    font=dict(
        family="Arial",
        size=20,
        color="Black"
    ),
    legend=dict(
        orientation="v",
        yanchor="auto",
        y=1,
        xanchor="right", 
        x=1.0
    )
)


# Show plot
fig.show()

