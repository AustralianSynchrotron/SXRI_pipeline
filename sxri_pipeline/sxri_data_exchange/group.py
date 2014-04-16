'''
Created on 07/10/2013

@author: Lenneke Jong
'''
import h5py
from sxri_data_exchange.dataset import Dataset
import re

class Group(object):
    '''
    Super class for all the group objects in our file.
    '''


    def __init__(self, h5group, name=None):
        '''
        Constructor
        '''
        if isinstance(h5group, h5py.Group):
            self.h5group = h5group
            if name is not None and self.h5group.name is None:
                self.h5group.name = name
            self.dataset_names = self.get_dataset_names()
            self.ref = self.h5group.ref
        else:
            pass 
            # throw some exception here?
    def create_string_dataset(self, name, data, *args, **kwargs):
        ''' creates a resizable string dataset useful for descritions, titles etc'''
        self.h5group.create_dataset(name, data=data, dtype=h5py.special_dtype(vlen=bytes))
        
    def set_dataset(self, name, data, **kwargs):
        '''set a dataset'''
        if name in self.h5group.keys() and isinstance(h5py.Dataset, self.h5group.get(name)):
            self.h5group[name] = data
        else:
            self.create_dataset(name, data)
        
    def create_dataset(self, data, name='data', chunks=True, *args, **kwargs):
        '''creates a dataset for this group enforcing naming and attribute conventions
            @param  data a numpy array 
            @param name for the dataset, default:"data"
        '''
        # first count if there are other datasets
        if name in self.dataset_names:
            name = 'data_' + len(self.dataset_names)
        dset = Dataset(self.h5group.create_dataset(name, data=data))
        if dset:
            self.dataset_names.append(name)
        return dset
        
    def get_dataset(self, name):
        '''Get a dataset by name'''
        if isinstance(self.h5group.get(name), h5py.Dataset):
            return Dataset(self.h5group[name])
        else:
            raise Exception('no dataset of name ' + name + 'in this group')
        
    def add_attribute(self, key, value):
        '''Add an attribute to the group'''
        self.h5group.attrs[key] = value
    
    def get_attributes(self):
        '''get all the attributes of this group'''
        return self.h5group.attrs
        
    def get_dataset_names(self):
        names = []
        
        def isDataset(name, obj):
            if isinstance(obj, h5py.Dataset) and obj.dtype == 'uint':
                names.append(name)
        
        self.h5group.visititems(isDataset)
        return names    
    
    def get_dataset_names_like(self, pattern):
        '''
        returns a list of dataset names that match a regular expression
        '''
        match_names = []
        for name in self.h5group.keys():
            if re.match(pattern, name):
                match_names.append(name)
        return match_names 
    
    def get_num_arr_datasets(self):
        '''return the number of numpy-like datasets in the group'''
        return len(self.dataset_names)
