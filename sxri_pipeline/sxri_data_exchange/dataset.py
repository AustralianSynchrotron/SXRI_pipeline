'''
Created on 07/10/2013

@author: Lenneke Jong <lenneke.jong@synchrotron.org.au>
'''
import h5py
import numpy as np

class Dataset(object):
    '''
    classdocs
    '''


    def __init__(self, h5dataset, **kwargs):
        '''
        Constructor
        '''
        if isinstance(h5dataset, h5py.Dataset):
            self.h5dataset = h5dataset
            self.shape = self.h5dataset.shape
        else:
            pass 
    
    def get_array(self):
        return self.h5dataset
    
        
    def add_array(self, subarr, dtype, axis, index=None):
        # add a subarray into the existing array (in position?)
        # first need to determine the shape of a slice subarray along the specified axis
        # and need to check that subarr has the same shape
        # resize the numpy array 
        # append/insert the subarray
        # save the dataset
        if subarr.shape != self.h5dataset[axis].shape:
            print "cannot add different shaped arrays"
            
    def add_attribute(self, name, value):
        self.h5dataset.attrs.create(name, value)
            
    def get_attribute(self, name):
        return self.h5dataset.attrs.get(name)
