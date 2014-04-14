'''
Created on 07/10/2013

@author: Lenneke Jong
'''
from sxri_data_exchange.group import Group

class ExchangeGroup(Group):
    '''
    ExchangeGroup class wraps a h5py.Group class and enforces some 
    conventions in the DataExchange specification as implemented by the SXR-I branch line at the Australian Synchrotron
    '''


    def __init__(self, h5group, name, *args, **kwargs):
        '''
        Constructor
        '''
        super(ExchangeGroup, self).__init__(h5group, name)
        # self.h5group.require_dataset('data')
        
    def set_title(self, title):
        '''set the "title" dataset, creating it if it doesn't exist. Dataset is a string representing the name of this exchange group'''
        if 'title' not in self.h5group.keys():
            self.create_string_dataset('title', data=title)
        else:
            self.h5group['title'].data = title
        
        
    

class RawExchange(ExchangeGroup):
    '''
    The raw data variant of the exchange group. In this group we expect one data
    set called 'data' containing all the diffraction data frames Data is an
    a*b*c*2048*2048 numpy array with a= number of frames on each position, b and
    c the 'x' and 'y' coordinates of each scan position We also have
    data_white_n and data_dark_n datasets containing the whitefiled and
    darkfields which correspond to each frame these will be of size 2048*2048
    Attributes of the 'data' dataset called 'white_field' and 'dark_field' map a
    reference to a dark field frame and white field frame for each data frame.
    This should actually be a read-only group for us
    '''
    
    def __init__(self, h5group, name="exchange", title='raw data', *args, **kwargs):
        '''
        Constructor
        '''
        super(RawExchange, self).__init__(h5group, name, *args, **kwargs)
        self.set_title(title)
    
    
    def get_raw_dataset(self):
        '''
        Get's the dataset with the title 'data' which contains all the raw data
        '''
        try:
            return self.get_dataset('data')
        except:
            raise Exception('no dataset')
    
    def get_raw_darkfields(self):
        darkfield_names = self.get_dataset_names_like('data_dark')
        darkfields = []
        for d in darkfield_names:
            dset = self.get_dataset(d)
            darkfields.append(dset.get_array())
        return darkfields
    
    def get_raw_whitefields(self):
        whitefield_names = self.get_dataset_names_like('data_white')
        whitefields = []
        for d in whitefield_names:
            dset = self.get_dataset(d)
            whitefields.append(dset.get_array())
        return whitefields  
    
      
    def get_white_field_list(self):
        ''' get the white field attribute which is an array of references to where the 
        white field corresponding to each frame in the raw data exists'''
        raw_data = self.get_raw_dataset()
        return raw_data.get_attribute('white_field')
    
    def get_dark_field_list(self):
        ''' get the dark field attribute which is an array of references to where the 
        dark field corresponding to each frame in the raw data exists'''
        return self.h5group.get_attribute('dark_field')
    
    
    
class ProcessedExchange(ExchangeGroup):
    '''This variant of the exchange group is the for processed data'''
    
    def __init__(self, h5group, title='processed data', *args, **kwargs):
        '''
        Constructor
        '''
        super(ProcessedExchange, self).__init__(h5group, title, *args, **kwargs)
        self.set_title(title)
    
    def create_dataset(self, data, name="data", units='counts', **kwargs):
        '''creates a dataset for this group enforcing naming and attribute 
            conventions
            
            @param  data a numpy array 
            @param title name for the dataset, default:"data"
            @param description default:"transmission"
            @param units default:"counts"
        '''
        # first count if there are other datasets
        if self.h5group.get(name):
            raise Exception("Dataset named %s already exists" % name)
            # append a number to the end of the title by selecting all datasets that match the pattern title_%d? not sure how to do that
        similar_dset_names = self.get_dataset_names_like(name)
        if len(similar_dset_names) > 0:
            name = name + '_' + str(len(similar_dset_names))
        dset = self.h5group.create_dataset(name, data=data, **kwargs)
        # dset.attrs['description']=description
        dset.attrs['units'] = units   


