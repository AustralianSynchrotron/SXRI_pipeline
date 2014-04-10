'''
Created on 07/10/2013

@author: Lenneke Jong
'''
import h5py

from sxri_data_exchange.exchange import ProcessedExchange, RawExchange
from sxri_data_exchange.measurement import MeasurementGroup
from sxri_data_exchange.provenance import ProvenanceGroup
import re


class SXRIDataExchange(h5py.File):
    '''
    class that maps to the DataExchange format from aps to a h5 file
    '''
    
    
    def __init__(self, filename):
        '''
        This file wraps a hdf5 file containing raw scan data, created by the SXR-I beamline at the AS
        It follows the conventions of the APS DataExchange document.
        '''
        super(SXRIDataExchange, self).__init__(filename,'a')
        self.exchange_groups = [self.wrap_existing_exchange_group(self[k],k) for k in self.keys() if re.findall('exchange', k)]
        self.measurement_groups = [MeasurementGroup(self[k],k) for k in self.keys() if re.findall('measurement', k)]
        self.provenance_group = self.create_provenance_group()
        self.nx = self['exchange']['data'].shape[-1] 
        self.ny = self['exchange']['data'].shape[-2]
        self.implements=self['implements']
        
    def wrap_existing_exchange_group(self,h5group,name,**kwargs):
        '''create ExchangeGroup objects for any groups that already exist in the hdf5 file. The first one is always 
        to be the raw data taken from the detector'''
        if name == 'exchange':
            wrapped = RawExchange(h5group)
        else:
            wrapped=ProcessedExchange(h5group)
        return wrapped
        
    def create_exchange_group(self, title, **kwargs):
        '''
        Create a wrapped exchange group in the root level group of the hdf5 file
        '''
        n = len(self.exchange_groups)
        name="exchange"
        if n > 0:
            new_exchange_group = ProcessedExchange(self.create_group("%s_%s" % (name,n)),title=title)
        else:
            new_exchange_group = RawExchange(self.create_group(name))
        self.exchange_groups.append(new_exchange_group)
        return new_exchange_group
    
    def create_provenance_group(self, **kwargs):
        '''
        Create a wrapped provenance group in the root level group of the hdf5 file
        '''
        if 'provenance' in self.keys():
            print "already have a provenance group, let's wrap it'"
            self.provenance_group=ProvenanceGroup(self['provenance'])
        else:
            self.provenance_group = ProvenanceGroup(self.create_group("provenance"))
            self.implements=self.implements+":provenance"
        return self.provenance_group
    
    def get_provenance_group(self,**kwargs):
        '''
        Get the wrapped provenance group
        '''
        if not self.provenance_group:
            return create_provenance_group()
        else:
            return self.provenance_group
    
    def create_measurement_group(self, **kwargs):
        '''
        Create a wrapped measurement group in the root level group of the hdf5 file
        '''
        n = len(self.measurement_groups)
        if n > 0:
            new_measurement_group = MeasurementGroup(self.create_group("measurement_%s" % n))
        else:
            new_measurement_group = MeasurementGroup(self.create_group("measurement"))
        self.measurement_groups.append(new_measurement_group)
        return new_measurement_group
                                           
    
    def get_raw_exchange_group(self):
        '''
        The raw data collected at the beam line is always contained the zeroth exhange group
        '''
        for eg in self.exchange_groups:
            if isinstance(eg,RawExchange):
                return eg
    
    def add_process(self,name,description):
        '''Add a processing step to the provenance group'''
        return self.provenance_group.create_process(name,description)
    

    def print_groups(self):
        '''
        A method mostly useful for testing that just prints out the names of the top level groups in the file
        '''
        for key in self.keys():
            print key
            print self[key].name
