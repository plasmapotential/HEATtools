import numpy as np
import plotly.graph_objects as go
import pandas as pd

# Define the impulse response function (assumed to be an exponential decay)
def impulse_response_exp(t, RC):
    return np.exp(-t / RC)

def impulse_response_poly(t, coeffs):
    return np.polynomial.polynomial.polyval(t,coeffs)

# Time step and time vector
dt = 0.001
t = np.arange(0, 0.095, dt)

# Example arbitrary heat flux signal q(t)
#q_t =1e6 * np.sin(0.5 * np.pi * t) * np.exp(-0.1 * t)
q_t = np.zeros((len(t)))
q_t[1:11] = 400


# Impulse response with a given RC value
RC = 0.017255  # Replace with the derived RC value
T0 = 300.0 #[K] initial temperature
#h_t = impulse_response_exp(t, RC) + T0

cFile = '/home/tlooby/source/tomTest/impulse/coeffs.csv'
coeffs = np.genfromtxt(cFile, delimiter=',')
h_t = impulse_response_poly(t, coeffs)

# Convolve the impulse response with the heat flux signal
Tpeak = np.convolve(q_t, h_t, mode='full') * dt
Tpeak = Tpeak[:len(t)]

# Adjust time vector for the convolution result
t_conv = np.arange(0, len(Tpeak) * dt, dt)

# Create a plot using Plotly
fig = go.Figure()

#fig.add_trace(go.Scatter(x=t, y=q_t, mode='lines', name='q(t)'))
#fig.add_trace(go.Scatter(x=t, y=h_t, mode='lines', name='Impulse Response'))
fig.add_trace(go.Scatter(x=t_conv, y=Tpeak, mode='lines', name='T_model'))

#name of each PFC
pfc1 = '/home/tlooby/HEAT/data/sparc_000001_impulseResponse/openFoam/heatFoam/T006'
files = [pfc1]
#nombres = ['Quadratic80ms', 'Triangle']
nombres = ['T_HEAT']

data = []
maxTs = []
namesWithTag = []
for i,f in enumerate(files):
#    if tag in name:
    outfile = f + '/postProcessing/fieldMinMax1/0/fieldMinMax.dat' #peak at any point
    tmp = pd.read_csv(outfile, header=1, delimiter="\t")
    tmp.columns = tmp.columns.str.strip()
    tmp = tmp.sort_values('field')
    tmp['field'] = tmp['field'].str.strip()
    use = tmp['field']=='T'
    maxTs.append(max(tmp[use]['max'].values))
    data.append(tmp)
    namesWithTag.append(nombres[i])


#print(maxTs)
idxMax = np.argmax(maxTs)
#print("Maximum T occurs on PFC: " + nombres[idxMax])


for i,df in enumerate(data):
    mask = df['field'] == 'T'
    t_orig = df[mask].sort_values('# Time')['# Time'].values
    varMax = df[mask].sort_values('# Time')['max'].values
    varMax = np.insert(varMax, 0, 300.0)
    t = np.insert(t, 0, 0.0)


    fig.add_trace(go.Scatter(x=t_orig, y=varMax, name=nombres[i], line=dict(width=4,),
                         mode='lines', marker_size=4,))



fig.update_yaxes(title_text="<b>Maximum PFC Temperature [K]</b>")
fig.update_xaxes(title_text="<b>Time [s]</b>")



fig.show()



print(np.max(Tpeak))