'''
Created on 15/04/2014

@author: Lenneke Jong <Lenneke.Jong@synchrotron.org.au>
'''
from sxri_pipeline.sxri_data_exchange.group import Group

class Instrument(Group):
    '''
    classdocs
    '''


    def __init__(self, h5group, *args, **kwargs):
        '''
        Constructor
        '''
        super(Instrument, self).__init__(h5group, *args, **kwargs)
        
    @property
    def detector(self):
        return Detector(self.h5group['detector'])
        
class Detector(Group):
    '''
    classdocs
    '''


    def __init__(self, h5group, *args, **kwargs):
        '''
        Constructor
        '''
        super(Detector, self).__init__(h5group, *args, **kwargs)

    @property
    def x_pixel_size(self):
        return self.h5group['x_pixel_size']

    @property
    def y_pixel_size(self):
        return self.h5group['y_pixel_size']

    @property  
    def geometry(self):
        return Geometry(self.h5group['geometry'])



class Geometry(Group):
    '''
    classdocs
    '''

    def __init__(self, h5group, name=None, *args, **kwargs):
        '''
        Constructor
        '''
        super(Geometry, self).__init__(h5group, name, *args, **kwargs)

    @property
    def translation(self):
        '''
        Returns a dictionary containing all the named datasets in the translation group
        '''
        return self.h5group['translation']
#        transdict={}
#        translation_group=self.h5group['translation']
#        for k in translation_group.keys():
#            if isinstance(h5py.Dataset,translation_group[k]):
#                transdict[k]=translation_group[k]
#        return transdict

class Monochromator(Group):
    '''
    classdocs
    '''

    def __init__(self, h5group, name=None):
        '''
        Constructor
        '''
        super(Monochromator, self).__init__(h5group, name)  #

    @property
    def energy(self):
        return self.get_dataset('energy')

    @property
    def energy_error(self):
        return self.get_dataset('energy_error')

    @property
    def type(self):
        return self.h5group['type']
