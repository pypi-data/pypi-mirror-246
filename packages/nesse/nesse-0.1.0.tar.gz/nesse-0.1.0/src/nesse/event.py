import numpy as np
from .constants import *
from scipy.interpolate import interp1d
from tqdm import tqdm
import pickle

##########
# 

##########

class Event:
    '''
    The Event class contains all information about a single particle event in the detector. 
    This starts with information of energy depositions imported from Geant4 (pos,dE,times). 
    Electron and hole drift paths are stored and used to determine the signal on a detector. 

    Currently this only works for a single contact, but we plan to extend to all contacts.
    '''
    def __init__(self, _id, _pos, _dE, _times):
        self.ID = _id
        self.pos = _pos
        self.dE = _dE
        self.times = _times

        self.dQ = []
        self.dI = {}
        self.dt = {}

        self.quasiparticles = []
        
        self.signal_I = {}
        self.signal_times = {}

    def shift_pos(self,new_pos=[0,0,0]):
        shift = np.array(new_pos) - self.pos[0]
        self.pos = self.pos + shift
        return None
        
    def convolveElectronicResponse(self, electronicResponse, contact=0):
        func_I = interp1d(self.dt[contact], self.dI[contact], bounds_error=False, fill_value=0)
        temp_times = electronicResponse["times"]
        dt = np.diff(temp_times)[0]
        
        self.signal_I[contact] = np.convolve(func_I(temp_times),electronicResponse["step"])
        self.signal_times[contact] = np.arange(0,len(self.signal_I[contact])*dt, dt)
        
        return None
        
    def addGaussianNoise(self, sigma=1, SNR=None):
        if SNR is not None:
            sigma = np.max(np.abs(self.signal_I))/SNR
        self.signal_I += np.random.normal(0, sigma , len(self.signal_I))   
        
    def convertUnits(self, energyConversionFactor, lengthConversionFactor, timeConversionFactor):
        self.dE *= energyConversionFactor
        self.pos *= lengthConversionFactor
        self.times *= timeConversionFactor
        return None
        
    def calculateInducedCurrent(self, dt, WF_interp, contact=0):
        weightingFieldx_interp, weightingFieldy_interp, weightingFieldz_interp, weightingFieldMag_interp = WF_interp
        
        max_time = max([o.time[-1] for o in self.quasiparticles])
        start_time = min([o.time[0] for o in self.quasiparticles])
        times_I = np.arange(start_time,max_time,dt)
        
        induced_I = np.zeros(len(times_I))

        for i in range(len(self.quasiparticles)):
            o = self.quasiparticles[i]
            Is = [o.q*np.dot(o.vel[j],
                        [weightingFieldx_interp(o.pos[j]),
                         weightingFieldy_interp(o.pos[j]),
                         weightingFieldz_interp(o.pos[j])]) for j in range(len(o.pos))]

            if len(Is) > 0:
                func_I = interp1d(o.time, Is, bounds_error=False, fill_value=0)
                induced_I += func_I(times_I)

        '''for i in tqdm(range(len(self.vel_drift_e))):
            if interp3d:
                Is = [-qe_SI*np.dot(self.vel_drift_e[i][j], 
                        [weightingFieldx_interp(self.pos_drift_e[i][j]),
                         weightingFieldy_interp(self.pos_drift_e[i][j]),
                         weightingFieldz_interp(self.pos_drift_e[i][j])]) for j in range(len(self.vel_drift_e[i]))]
                         
            else:
                Is = [-qe_SI*np.dot(self.vel_drift_e[i][j], 
                        [weightingFieldx_interp(self.pos_drift_e[i][j]),
                         weightingFieldy_interp(self.pos_drift_e[i][j]),
                         weightingFieldz_interp(self.pos_drift_e[i][j])])[0] for j in range(len(self.vel_drift_e[i]))]

            times = self.times_drift_e[i][:-1]

            if len(Is)>1:
                func_I = interp1d(times, Is, bounds_error=False, fill_value=0)
                induced_I += func_I(times_I)
                
        for i in tqdm(range(len(self.vel_drift_h))):
            if interp3d:
                Is = [qe_SI*np.dot(self.vel_drift_h[i][j], 
                        [weightingFieldx_interp(self.pos_drift_h[i][j]),
                         weightingFieldy_interp(self.pos_drift_h[i][j]),
                         weightingFieldz_interp(self.pos_drift_h[i][j])]) for j in range(len(self.vel_drift_h[i]))]
                         
            else:
                Is = [qe_SI*np.dot(self.vel_drift_h[i][j], 
                        [weightingFieldx_interp(self.pos_drift_h[i][j]),
                         weightingFieldy_interp(self.pos_drift_h[i][j]),
                         weightingFieldz_interp(self.pos_drift_h[i][j])])[0] for j in range(len(self.vel_drift_h[i]))]
            times = self.times_drift_h[i][:-1]

            if len(Is)>1:
                func_I = interp1d(times, Is, bounds_error=False, fill_value=0)
                induced_I += func_I(times_I)'''
        
        self.dI[contact] = induced_I
        self.dt[contact]=times_I-start_time
        
        return None    
    
    def sample(self, dt,length=None, contact=0):
        '''
        Samples the induced current of an event to larger timesteps so that it is the same format as nab data. 
        There is some question as to the proper way to do this; for now we simply take the value at the exact time sampled.
        '''
        step = int(dt/(self.signal_times[contact][1]-self.signal_times[contact][0])) 
        signal = self.signal_I[contact][::step].copy()
        if length==None:
            return signal
        else:
            return np.pad(signal, (round(length/2),round(length/2)-len(signal)),"edge")

def eventsFromG4root(filename, pixel=None):
    import uproot
    import pandas

    file = uproot.open(filename)
    tree = file["ntuple/hits"]

    try:
        df = tree.arrays(["eventID", "trackID", "x", "y", "z", "time", "eDep", "pixelNumber"], 
                         library="pd")
        if pixel is not None:
            df = df[df["pixelNumber"]==pixel]
    
        gdf = df.groupby("eventID")
    except:
        #old formatting exception
        df = tree.arrays(["iD", "x", "y", "z", "time", "eDep"], library="pd")
        gdf = df.groupby("iD")

    events = []
    for eID, group in gdf:
        event = Event(eID, group[["x", "y", "z"]].to_numpy(), group["eDep"].to_numpy(), group["time"].to_numpy())
        event.convertUnits(1e3,1e-3,1e-9)
        events.append(event)
    return events
    
#convert events to nabPy form, and save optionally save pickle file if filename is given. dt is time sampling in ns, which is 4ns for current nab daq
def saveEventsNabPy(events, filename=None, dt=4e-9, length=7000, contact=0):
    new_events =np.array([event.sample(dt,length, contact) for event in events])
    if filename is not None:
        with open(filename+".pkl", "wb") as file:
            pickle.dump(new_events, file)
    
    return new_events
    
def loadEventsNabPy(filename):
    with open(filename, "rb") as file:
        events = pickle.load(file)
    
    return events
    
    
#save complete event object, for example if you want to be able to re-downsample, apply a different convolution, etc.
def saveEvents(events, filename):
    with open(filename+".pkl", "wb") as file:
        pickle.dump(events, file)
    return
    
def loadEvents(filename):
    with open(filename+".pkl", "rb") as file:
        events = pickle.load(file)
    return events
    
