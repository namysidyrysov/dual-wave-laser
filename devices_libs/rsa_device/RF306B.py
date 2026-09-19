from devices_libs.rsa_device.rsa_api_full_N import search_connect,config_spectrum,acquire_spectrum,create_frequency_array
import numpy as np
from ctypes import *
rsa = cdll.LoadLibrary(r"C:\Tektronix\RSA_API\lib\x64\RSA_API.dll")
KILO=1e+3
GIGA=1e+9

# Tektronix RSA306B
class RF306B():
    MIN_FREQ = 9*KILO
    MAX_FREQ = 6.2*GIGA
    DEFAULT_TRACE_POINTS = 8001
    
    def __init__(self):
        search_connect()
        self.cf = 2.4453*GIGA
        self.refLevel = -20
        self.span = 6.2*GIGA
        self.rbw = 10*KILO
        self.start = self.MIN_FREQ
        self.stop = self.MAX_FREQ
        self.trace_points = self.DEFAULT_TRACE_POINTS
        

    
        self.specSet = config_spectrum(self.cf, self.refLevel, self.span, self.rbw, self.start, self.stop, self.trace_points)
        print(self.__class__.__name__, 'inited!')

        

    def __del__(self):
        rsa.DEVICE_Disconnect()
        
    def set_cf(self, val):
        self.cf = val
        self.specSet = config_spectrum(self.cf, self.refLevel, self.span, self.rbw, self.start, self.stop, self.trace_points)

    def set_refLevel(self, val):
        self.refLevel = val
        self.specSet = config_spectrum(self.cf, self.refLevel, self.span, self.rbw, self.start, self.stop, self.trace_points)

    def set_span(self, val):
        self.span = val
        self.specSet = config_spectrum(self.cf, self.refLevel, self.span, self.rbw, self.start, self.stop, self.trace_points)

    def set_rbw(self, val):
        self.rbw = val
        self.specSet = config_spectrum(self.cf, self.refLevel, self.span, self.rbw, self.start, self.stop, self.trace_points)

    def set_start(self, val):
        self.start = val
        self.specSet = config_spectrum(self.cf, self.refLevel, self.span, self.rbw, self.start, self.stop, self.trace_points)

    def set_stop(self, val):
        self.stop = val
        self.specSet = config_spectrum(self.cf, self.refLevel, self.span, self.rbw, self.start, self.stop, self.trace_points)

    def set_trace_points(self, val):
        self.trace_points = val
        self.specSet = config_spectrum(self.cf, self.refLevel, self.span, self.rbw, self.start, self.stop, self.trace_points)

    def get_rf_spectrum(self):
        ''' Возвращает X и Y отдельно в виде числовых массивов'''
        powers = acquire_spectrum(self.specSet)
        freqs = create_frequency_array(self.specSet)
        return freqs, powers


    def config_param(self, cf, refLevel, span, rbw, start, stop, trace_points):
        self.cf = cf
        self.refLevel = refLevel
        self.span = span
        self.rbw = rbw
        self.start = start
        self.stop = stop
        self.trace_points = trace_points
        self.specSet = config_spectrum(self.cf, self.refLevel, self.span, self.rbw, self.start, self.stop,self.trace_points)
    
