#SOLPSclass.py
#Description:   python interface to SOLPS output
#Engineer:      T Looby
#Date:          20220920

import matplotlib
import matplotlib.cm as cm
import plotly
import plotly.graph_objects as go
import numpy as np
from shapely.geometry import MultiPoint, MultiPolygon, Polygon, LinearRing
import netCDF4 as nc

class SOLPS_NC:
    """
    Class for interfacing to SOLPS output in netCDF (NC) format
    """
    def __init__(self):
        print("Nothing to initialize.  SOLPS class created")
        return

    def readAll(self, cdfFile):
        """
        reads a SOLPS output file in netCDF format
        """
        self.cdfFile = cdfFile
        self.ds = nc.Dataset(self.cdfFile)
        return
    
    def getListOfVars(self):
        """
        returns a list of all variable names in self.ds
        """
        a = []
        for var in self.ds.variables.values():
            a.append(var.name)
        return a

    def getSingleVar(self, var: str):
        """
        returns a single variable's data from the TRANSP data

        var is a string that corresponds to the name of the variable
        """
        try:
            varData = self.ds[var]
        except:
            print("Variable "+var+" not found in list of variables")
            varData = None

        return varData



    def getXYfromGeom(self):
        """
        orders geometry points and saves them in xGrid,yGrid variables for
        plotting.  Note that in xGrid,yGrid the 0th value in each grid cell
        is repeated, resulting in 5 x,y coordinates per grid element, in order
        to generate closed contours in plotly
        """

        self.xGrid = []
        self.yGrid = []

        crx = self.getSingleVar('crx')
        cry = self.getSingleVar('cry')

        #number of grid cells
        Nx = crx.shape[2]
        Ny = crx.shape[1]
        Ncells = Nx*Ny

        #cell ordering of 1,1,1,1...4,4,4,4...
        self.xGrid = [None]*Ncells*6
        self.xGrid[0::6] = crx[0,:,:].flatten()
        self.xGrid[1::6] = crx[1,:,:].flatten()
        self.xGrid[2::6] = crx[3,:,:].flatten() #note that 2 is 3 and 3 is 2
        self.xGrid[3::6] = crx[2,:,:].flatten() #  in ordering of polygons here
        self.xGrid[4::6] = crx[0,:,:].flatten()

        self.yGrid = [None]*Ncells*6
        self.yGrid[0::6] = cry[0,:,:].flatten()
        self.yGrid[1::6] = cry[1,:,:].flatten()
        self.yGrid[2::6] = cry[3,:,:].flatten() #note that 2 is 3 and 3 is 2
        self.yGrid[3::6] = cry[2,:,:].flatten() #  in ordering of polygons here
        self.yGrid[4::6] = cry[0,:,:].flatten()

        self.Ncells = Ncells

        print(self.xGrid[0:6])
        print(self.yGrid[0:6])
        return

    def plot1cell(self, i):
        print(self.xGrid[i:i+6])
        print(self.yGrid[i:i+6])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.xGrid[i:i+6],y=self.yGrid[i:i+6], fill="toself"))
        return fig


    def plotlySingleRadLine(self, z):
        """
        plots line radiation data on the grid as a heatmap

        returns a plotly go.Figure() object
        """
        z = np.abs(z)
        fig = go.Figure()
        zMax = max(z)
        zNorm = z / zMax

        norm = matplotlib.colors.Normalize(vmin=min(z), vmax=max(z), clip=True)
        mapper = cm.ScalarMappable(norm=norm, cmap=cm.hot)

        #fig.add_trace(go.Scatter(x=self.xGrid,y=self.yGrid, fill="toself"))
        for i in range(self.Ncells):
            fc = mapper.to_rgba(z[i])
            fcStr = 'rgba({:f}, {:f}, {:f}, {:f})'.format(fc[0],fc[1],fc[2],fc[3])
            fig.add_trace(go.Scatter(x=self.xGrid[i*6:i*6+4], y=self.yGrid[i*6:i*6+4], mode='lines', fill="toself", fillcolor=fcStr, line=dict(color=fcStr)))


        #add colorbar
        fig.add_trace(go.Scatter(x=[None],y=[None],mode='markers',
                                 marker=dict(colorscale=plotly.colors.sequential.Hot,
                                             cmin=0,cmax=zMax,
                                             colorbar=dict(thickness=15,outlinewidth=0, title="Power [W]")

                                            )
                                 )
                    )

        fig.update_yaxes(scaleanchor = "x",scaleratio = 1,)

        fig.update_layout(
            title = "Line Radiation [W]",
            xaxis_title="R [m]",
            yaxis_title="Z [m]",
            autosize=True,
            #for aspect ratio
            #autosize=False,
            #width=width*1.1,
            #height=height,
            showlegend=False,
            font=dict(
                #family="Courier New",
                size=18,
                #color="#dcdce3"
                ),
            margin=dict(
                l=10,
                r=10,
                b=10,
                t=100,
                pad=4
            )
            )



        return fig


    def plotlyAllRadLines(self, data):
        """
        plots all line radiation profiles superimposed on the grid as a heatmap

        returns a plotly go.Figure() object
        """
        #add up all power for all species
        z = np.zeros((self.Ncells))
        for d in data:
            z += np.array(np.abs(d.flatten()), dtype=float)

        fig = go.Figure()

        zMax = max(z)
        print("Maximum Power: {:f} [W]".format(zMax))
        print("Total power: {:f} []".format(np.sum(z)))
        zNorm = z / zMax

        self.Prad_all = z
        self.Prad_max = zMax
        self.Prad_sum = np.sum(z)
        norm = matplotlib.colors.Normalize(vmin=min(z), vmax=max(z), clip=True)
        mapper = cm.ScalarMappable(norm=norm, cmap=cm.hot)

        #fig.add_trace(go.Scatter(x=self.xGrid,y=self.yGrid, fill="toself"))
        for i in range(self.Ncells):
            fc = mapper.to_rgba(z[i])
            fcStr = 'rgba({:f}, {:f}, {:f}, {:f})'.format(fc[0],fc[1],fc[2],fc[3])
            fig.add_trace(go.Scatter(x=self.xGrid[i*6:i*6+4], y=self.yGrid[i*6:i*6+4], mode='lines', fill="toself", fillcolor=fcStr, line=dict(color=fcStr)))


        #add colorbar
        fig.add_trace(go.Scatter(x=[None],y=[None],mode='markers',
                                 marker=dict(colorscale=plotly.colors.sequential.Hot,
                                             cmin=0,cmax=zMax,
                                             colorbar=dict(thickness=15,outlinewidth=0, title="Power [W]")

                                            )
                                 )
                    )

        fig.update_yaxes(scaleanchor = "x",scaleratio = 1,)

        fig.update_layout(
            title = "Line Radiation [W] for All Lines",
            xaxis_title="R [m]",
            yaxis_title="Z [m]",
            autosize=True,
            #for aspect ratio
            #autosize=False,
            #width=width*1.1,
            #height=height,
            showlegend=False,
            font=dict(
                #family="Courier New",
                size=18,
                #color="#dcdce3"
                ),
            margin=dict(
                l=10,
                r=10,
                b=10,
                t=100,
                pad=4
            )
            )



        return fig

    def addRZcontour(self, fig, contourFile):
        """
        adds an RZ contour to an existing figure

        contourFile should be a csv with the RZ points of the contour

        returns an updated figure
        """
        RZ = np.genfromtxt(contourFile, comments='#', delimiter=',')

        fig.add_trace(go.Scatter(x=RZ[:,0],y=RZ[:,1], mode='lines', line={'color':'blue'}))


        return fig


    def getPolyCentroids(self):
        """
        gets centroids of polygons defined by
        (crx, cry)

        saves into variable self.ctrs
        """
        self.ctrs = np.zeros((self.Ncells,2))
        for i in range(self.Ncells):
            poly = Polygon(np.vstack([self.xGrid[i*6:i*6+4],self.yGrid[i*6:i*6+4]]).T)
            self.ctrs[i,:] = np.array(poly.centroid.coords)[0]
        return

    def createHEATradCSV(self, Prad, file=None, boundBox=None):
        """
        generates a CSV file that can be read by HEAT.  file includes R,Z,Prad
        data that has been taken for a specific species, or for all species,
        as requested by user.

        boundBox is a list of 4 values: (Rmin, Rmax, Zmin, Zmax), which defines
        the region of the SOLPS data that we want to save to CSV.  should be in
        [meters]

        HFscalar is a scalar that will be multiplied by the Prad
        """
        self.getPolyCentroids()


        if boundBox != None:
            test1 = np.logical_and(self.ctrs[:,0]>boundBox[0], self.ctrs[:,0]<boundBox[1])
            test2 = np.logical_and(self.ctrs[:,1]>boundBox[2], self.ctrs[:,1]<boundBox[3])
            use = np.where(np.logical_and(test1,test2)==True)[0]
        else:
            use = np.arange(self.Ncells)

        data = np.vstack([self.ctrs[use,:].T, Prad[use]]).T
        data[:,-1] *= 1e-6 #W to MW
        head = 'R[m], Z[m], P[MW]'
        if len(data) == 0:
            print("\nNo radiation data!  Check your bounding box!")
            print('boundBox should be (Rmin,Rmax,Zmin,Zmax) in [m]')
            print("EXITING WITHOUT WRITING FILE!\n")
        else:
            np.savetxt(file,data,delimiter=',',fmt='%.10f',header=head)
            print('Saved HEAT radiation file to: '+file)

        return



class SOLPS_IO:
    """
    Class for interfacing to SOLPS output
    """
    def __init__(self):
        print("Nothing to initialize.  SOLPS class created")
        return

    def readGeometry(self, geomFile, lastHeader = 0):
        """
        reads a SOLPS geometry file.  saves a new class object called geometry,
        a dictionary whose keys are each of the variables defined in the
        SOLPS geometry file.  Usually these geometry files are named b2fgmtry

        geomFile is full path to file
        lastHeader is the last index of the header in the file (0 indexed)
        """
        #read geometry data (you may need to modify this)
        #0 indexed header lines
        self.geometry = {}

        d={}
        with open(geomFile, 'r') as f:
            for i,line in enumerate(f):
                #skip header lines
                if i<lastHeader+1:
                    continue
                #lines with variable definitions that describe subsequent variables
                elif '*cf:' in line:
                    l = line.strip().split(' ')
                    l = [ x for x in l if x!='']
                    d = {'length':l[-2], 'type':l[-3], 'data':[]}
                    name = l[-1]
                    self.geometry[name] = d
                #lines with variables
                else:
                    if self.geometry[name]['type'] == 'char':
                        self.geometry[name]['data'] = line[:-2] #remove newline
                    else:
                        self.geometry[name]['data'] += self.readNumbers(line, d['type'])

        #generate xGrid,yGrid variables for plotting later
        self.getXYfromGeom()

        print("Read geometry data...")
        return


    def readNumbers(self, data, type):
        """
        reads a line from a SOLPS file, strips it and builds into a list,
        then returns either a list of floats or ints
        """
        l = data.strip().split()
        if type=='int':
            l = [ int(x) for x in l if x!='']
        else:
            l = [ float(x) for x in l if x!='']
        return l


    def readLineRadiation(self, radFile):
        """
        reads line radiation file and saves a lineRad object, which is a list
        containing the line radiation [W] on the SOLPS grid.
        """
        #read radiation data by species
        self.lineRad = {}
        with open(radFile, 'r') as f:
            for i,line in enumerate(f):
                if '#' in line:
                    species = line.strip().split(' ')[-1]
                    self.lineRad[species] = {'power': []}

                else:
                    self.lineRad[species]['power'].append(line.strip().split(' ')[-1])

        print("Read line radiation data...")
        return

    def readAtomRadiation(self, radFile):
        """
        reads atom radiation file and saves a atomRad object, which is a list
        containing the atom radiation [W] on the SOLPS grid.  Atom radiation
        is defined separately from line radiation in SOLPS output
        """
        #read radiation data by species
        self.atomRad = {}
        with open(radFile, 'r') as f:
            for i,line in enumerate(f):
                if '#' in line:
                    species = line.strip().split(' ')[-1]
                    self.atomRad[species] = {'power': []}
                else:
                    self.atomRad[species]['power'].append(line.strip().split(' ')[-1])

        print("Read atom (neutral) radiation data...")
        return



    def readTe(self, TeFile):
        """
        reads line radiation file and saves a lineRad object, which is a list
        containing the line radiation [W] on the SOLPS grid.
        """
        #read radiation data by species
        self.Te = {}
        with open(TeFile, 'r') as f:
            for i,line in enumerate(f):
                if '#' in line:
                    species = line.strip().split(' ')[-1]
                    self.Te = {'Te': []}

                else:
                    self.Te['Te'].append(line.strip().split(' ')[-1])

        print("Read Te data...")
        return




    def getXYfromGeom(self):
        """
        orders geometry points and saves them in xGrid,yGrid variables for
        plotting.  Note that in xGrid,yGrid the 0th value in each grid cell
        is repeated, resulting in 5 x,y coordinates per grid element, in order
        to generate closed contours in plotly
        """
        self.xGrid = []
        self.yGrid = []
        #number of grid cells
        Ncells = int(len(self.geometry['cry']['data']) / 4)

        #cell ordering of 1,1,1,1...4,4,4,4...
        self.xGrid = [None]*Ncells*6
        self.xGrid[0::6] = self.geometry['crx']['data'][:1*Ncells]
        self.xGrid[1::6] = self.geometry['crx']['data'][1*Ncells:2*Ncells]
        self.xGrid[2::6] = self.geometry['crx']['data'][3*Ncells:4*Ncells] #order flipped 2-3
        self.xGrid[3::6] = self.geometry['crx']['data'][2*Ncells:3*Ncells] #order flipped 2-3
        self.xGrid[4::6] = self.geometry['crx']['data'][:1*Ncells]
        self.yGrid = [None]*Ncells*6
        self.yGrid[0::6] = self.geometry['cry']['data'][:1*Ncells]
        self.yGrid[1::6] = self.geometry['cry']['data'][1*Ncells:2*Ncells]
        self.yGrid[2::6] = self.geometry['cry']['data'][3*Ncells:4*Ncells] #order flipped 2-3
        self.yGrid[3::6] = self.geometry['cry']['data'][2*Ncells:3*Ncells] #order flipped 2-3
        self.yGrid[4::6] = self.geometry['cry']['data'][:1*Ncells]

        self.Ncells = Ncells

        print(self.xGrid[0:6])
        print(self.yGrid[0:6])
        return

    def getPolyCentroids(self):
        """
        gets centroids of polygons defined by
        (self.geometry['crx'], self.geometry['cry'])

        saves into variable self.ctrs
        """
        self.ctrs = np.zeros((self.Ncells,2))
        for i in range(self.Ncells):
            poly = Polygon(np.vstack([self.xGrid[i*6:i*6+4],self.yGrid[i*6:i*6+4]]).T)
            self.ctrs[i,:] = np.array(poly.centroid.coords)[0]
        return


    def plotlyMeshPlot(self):
        """
        returns a plotly go.Figure() object that can be plotted in a web browser
        figure is of the SOLPS mesh
        """
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.xGrid,y=self.yGrid, fill="toself"))
        fig.update_yaxes(scaleanchor = "x",scaleratio = 1,)

        fig.update_layout(
            xaxis_title="R [m]",
            yaxis_title="Z [m]",
            autosize=True,
            #for aspect ratio
            #autosize=False,
            #width=width*1.1,
            #height=height,
            showlegend=False,
            font=dict(
                #family="Courier New",
                size=18,
                #color="#dcdce3"
                ),
            margin=dict(
                l=10,
                r=10,
                b=10,
                t=100,
                pad=4
            )
            )


        return fig


    def plotlySingleRadLine(self, species=None):
        """
        plots line radiation data on the grid as a heatmap

        returns a plotly go.Figure() object
        """
        if species==None:
            key = list(self.lineRad.keys())[0]
            print("No key provided.  Available species:")
            print(list(self.lineRad.keys()))
            print("Using species: "+key)
        elif species not in list(self.lineRad.keys()):
            key = list(self.lineRad.keys())[0]
            print("Species not in file.  Available species")
            print(list(self.lineRad.keys()))
            print("Using species: "+key)
        else:
            key=species
            print("Using species: "+key)

        fig = go.Figure()
        z = np.array(self.lineRad[key]['power'], dtype=float)
        zMax = max(z)
        zNorm = z / zMax

        norm = matplotlib.colors.Normalize(vmin=min(z), vmax=max(z), clip=True)
        mapper = cm.ScalarMappable(norm=norm, cmap=cm.hot)

        #fig.add_trace(go.Scatter(x=self.xGrid,y=self.yGrid, fill="toself"))
        for i in range(self.Ncells):
            fc = mapper.to_rgba(z[i])
            fcStr = 'rgba({:f}, {:f}, {:f}, {:f})'.format(fc[0],fc[1],fc[2],fc[3])
            fig.add_trace(go.Scatter(x=self.xGrid[i*6:i*6+4], y=self.yGrid[i*6:i*6+4], mode='lines', fill="toself", fillcolor=fcStr, line=dict(color=fcStr)))


        #add colorbar
        fig.add_trace(go.Scatter(x=[None],y=[None],mode='markers',
                                 marker=dict(colorscale=plotly.colors.sequential.Hot,
                                             cmin=0,cmax=zMax,
                                             colorbar=dict(thickness=15,outlinewidth=0, title="Power [W]")

                                            )
                                 )
                    )

        fig.update_yaxes(scaleanchor = "x",scaleratio = 1,)

        fig.update_layout(
            title = "Line Radiation [W] for "+key,
            xaxis_title="R [m]",
            yaxis_title="Z [m]",
            autosize=True,
            #for aspect ratio
            #autosize=False,
            #width=width*1.1,
            #height=height,
            showlegend=False,
            font=dict(
                #family="Courier New",
                size=18,
                #color="#dcdce3"
                ),
            margin=dict(
                l=10,
                r=10,
                b=10,
                t=100,
                pad=4
            )
            )



        return fig



    def plotlyAllRadLines(self):
        """
        plots all line radiation profiles superimposed on the grid as a heatmap

        returns a plotly go.Figure() object
        """
        #add up all power for all species
        z = np.zeros((self.Ncells))
        for species in list(self.lineRad.keys()):
            z += np.array(self.lineRad[species]['power'], dtype=float)

        fig = go.Figure()

        zMax = max(z)
        print("Maximum Power: {:f} [W]".format(zMax))
        print("Total power: {:f} []".format(np.sum(z)))
        zNorm = z / zMax

        norm = matplotlib.colors.Normalize(vmin=min(z), vmax=max(z), clip=True)
        mapper = cm.ScalarMappable(norm=norm, cmap=cm.hot)

        #fig.add_trace(go.Scatter(x=self.xGrid,y=self.yGrid, fill="toself"))
        for i in range(self.Ncells):
            fc = mapper.to_rgba(z[i])
            fcStr = 'rgba({:f}, {:f}, {:f}, {:f})'.format(fc[0],fc[1],fc[2],fc[3])
            fig.add_trace(go.Scatter(x=self.xGrid[i*6:i*6+4], y=self.yGrid[i*6:i*6+4], mode='lines', fill="toself", fillcolor=fcStr, line=dict(color=fcStr)))


        #add colorbar
        fig.add_trace(go.Scatter(x=[None],y=[None],mode='markers',
                                 marker=dict(colorscale=plotly.colors.sequential.Hot,
                                             cmin=0,cmax=zMax,
                                             colorbar=dict(thickness=15,outlinewidth=0, title="Power [W]")

                                            )
                                 )
                    )

        fig.update_yaxes(scaleanchor = "x",scaleratio = 1,)

        fig.update_layout(
            title = "Line Radiation [W] for All Lines",
            xaxis_title="R [m]",
            yaxis_title="Z [m]",
            autosize=True,
            #for aspect ratio
            #autosize=False,
            #width=width*1.1,
            #height=height,
            showlegend=False,
            font=dict(
                #family="Courier New",
                size=18,
                #color="#dcdce3"
                ),
            margin=dict(
                l=10,
                r=10,
                b=10,
                t=100,
                pad=4
            )
            )



        return fig


    def plotlyAllRad(self):
        """
        plots all line and atom radiation profiles superimposed on the grid as a heatmap

        returns a plotly go.Figure() object
        """
        #add up all power for all species
        z = np.zeros((self.Ncells))
        #line radiation
        for species in list(self.lineRad.keys()):
            z += np.array(self.lineRad[species]['power'], dtype=float)
        #neutral radiation
        for species in list(self.atomRad.keys()):
            z += np.array(self.atomRad[species]['power'], dtype=float)

        fig = go.Figure()

        zMax = max(z)
        print("Maximum Power: {:f} [W]".format(zMax))
        print("Total power: {:f} [W]".format(np.sum(z)))
        zNorm = z / zMax

        norm = matplotlib.colors.Normalize(vmin=min(z), vmax=max(z), clip=True)
        mapper = cm.ScalarMappable(norm=norm, cmap=cm.plasma)

        #fig.add_trace(go.Scatter(x=self.xGrid,y=self.yGrid, fill="toself"))
        for i in range(self.Ncells):
            fc = mapper.to_rgba(z[i])
            fcStr = 'rgba({:f}, {:f}, {:f}, {:f})'.format(fc[0],fc[1],fc[2],fc[3])
            fig.add_trace(go.Scatter(x=self.xGrid[i*6:i*6+4], y=self.yGrid[i*6:i*6+4], mode='lines', fill="toself", fillcolor=fcStr, line=dict(color=fcStr)))


        #add colorbar
        fig.add_trace(go.Scatter(x=[None],y=[None],mode='markers',
                                 marker=dict(colorscale=plotly.colors.sequential.Plasma,
                                             cmin=0,cmax=zMax,
                                             colorbar=dict(thickness=15,outlinewidth=0, title="Power [W]")

                                            )
                                 )
                    )

        fig.update_yaxes(scaleanchor = "x",scaleratio = 1,)

        fig.update_layout(
            title = "Line Radiation + Neutral Atom Radiation [W]",
            xaxis_title="R [m]",
            yaxis_title="Z [m]",
            autosize=True,
            #for aspect ratio
            #autosize=False,
            #width=width*1.1,
            #height=height,
            showlegend=False,
            font=dict(
                #family="Courier New",
                size=18,
                #color="#dcdce3"
                ),
            margin=dict(
                l=10,
                r=10,
                b=10,
                t=100,
                pad=4
            )
            )



        return fig


    def addRZcontour(self, fig, contourFile):
        """
        adds an RZ contour to an existing figure

        contourFile should be a csv with the RZ points of the contour

        returns an updated figure
        """
        RZ = np.genfromtxt(contourFile, comments='#', delimiter=',')

        fig.add_trace(go.Scatter(x=RZ[:,0],y=RZ[:,1], mode='lines', line={'color':'blue'}))


        return fig


    def plotlyTe(self):
        """
        plots line radiation data on the grid as a heatmap

        returns a plotly go.Figure() object
        """
        fig = go.Figure()
        z = np.array(self.Te['Te'], dtype=float)
        zMax = max(z)
        zNorm = z / zMax

        norm = matplotlib.colors.Normalize(vmin=min(z), vmax=max(z), clip=True)
        mapper = cm.ScalarMappable(norm=norm, cmap=cm.viridis)
        #fig.add_trace(go.Scatter(x=self.xGrid,y=self.yGrid, fill="toself"))
        for i in range(self.Ncells):
            fc = mapper.to_rgba(z[i])
            fcStr = 'rgba({:f}, {:f}, {:f}, {:f})'.format(fc[0],fc[1],fc[2],fc[3])
            fig.add_trace(go.Scatter(x=self.xGrid[i*6:i*6+4], y=self.yGrid[i*6:i*6+4],
                            mode='lines', fill="toself", fillcolor=fcStr, line=dict(color=fcStr),
                            hoverinfo='text',
                            text='{:0.2f} eV'.format(z[i])
                            ))


        #add colorbar
        fig.add_trace(go.Scatter(x=[None],y=[None],mode='markers',
                                 marker=dict(colorscale=plotly.colors.sequential.Viridis,
                                             cmin=0,cmax=zMax,
                                             colorbar=dict(thickness=15,outlinewidth=0, title="Te [eV]")

                                            )
                                 )
                    )

        fig.update_yaxes(scaleanchor = "x",scaleratio = 1,)
        fig.update_layout(
            title = "Temperature [eV]",
            xaxis_title="R [m]",
            yaxis_title="Z [m]",
            autosize=True,
            #for aspect ratio
            #autosize=False,
            #width=width*1.1,
            #height=height,
            showlegend=False,
            font=dict(
                #family="Courier New",
                size=18,
                #color="#dcdce3"
                ),
            margin=dict(
                l=10,
                r=10,
                b=10,
                t=100,
                pad=4
            )
            )



        return fig



    def createHEATradCSV(self, file=None, species='all', neutrals=True, boundBox=None):
        """
        generates a CSV file that can be read by HEAT.  file includes R,Z,Prad
        data that has been taken for a specific species, or for all species,
        as requested by user.

        boundBox is a list of 4 values: (Rmin, Rmax, Zmin, Zmax), which defines
        the region of the SOLPS data that we want to save to CSV.  should be in
        [meters]

        """
        #line radiation
        if species in list(self.lineRad.keys()):
            key = species
            print("Using species: "+key)
            Prad = np.array(self.lineRad[key]['power'], dtype=float)
        else:
            #add up all power for all species
            Prad = np.zeros((self.Ncells))
            for species in list(self.lineRad.keys()):
                Prad += np.array(self.lineRad[species]['power'], dtype=float)

        if neutrals==True:
            for species in list(self.atomRad.keys()):
                Prad+=np.array(self.atomRad[species]['power'], dtype=float)

        self.getPolyCentroids()


        if boundBox != None:
            test1 = np.logical_and(self.ctrs[:,0]>boundBox[0], self.ctrs[:,0]<boundBox[1])
            test2 = np.logical_and(self.ctrs[:,1]>boundBox[2], self.ctrs[:,1]<boundBox[3])
            use = np.where(np.logical_and(test1,test2)==True)[0]
        else:
            use = np.arange(self.Ncells)

        data = np.vstack([self.ctrs[use,:].T, Prad[use]]).T
        data[:,-1] *= 1e-6 #W to MW
        head = 'R[m], Z[m], P[MW]'
        if len(data) == 0:
            print("\nNo radiation data!  Check your bounding box!")
            print('boundBox should be (Rmin,Rmax,Zmin,Zmax) in [m]')
            print("EXITING WITHOUT WRITING FILE!\n")
        else:
            np.savetxt(file,data,delimiter=',',fmt='%.10f',header=head)
            print('Saved HEAT radiation file to: '+file)

        return








if __name__ == '__main__':
    print("This script should be called as a class object from a python script")
    print("or a terminal.  Doing nothing...")
