'''
Created on 28/03/2014

@author: Lenneke Jong <lenneke.jong@synchrotron.org.au>

'''
import sxri_data_exchange 
import numpy as np
from functools import wraps
import logging


def process(f):
    '''
     Decorator to use on the main function that is running a pipeline component
     It will add the correct information, including references, to the provenance group and create a correctly named exchange group
    '''
    @wraps(f)
    def wrapper(self, data_exchange, *args, **kwargs):
        _process = data_exchange.add_process(f.__name__, f.__doc__)
        input_ref, output_ref = f(self, data_exchange, *args, **kwargs)
        _process.input_data = input_ref
        _process.output_data = output_ref
        return
    return wrapper


class PipelineComponent(object):
    '''
    Base object for pipeline components to inherit from.
    '''
    
    
    def __init__(self, data_exchange, *args, **kwargs):
        '''Constructor'''
        self.data_exchange = data_exchange
        self.input_group = data_exchange.get_raw_exchange_group()
        self.output_group = data_exchange.create_exchange_group(*args, **kwargs)
    
 
    def run(self):
        '''Method which will be called to run this pipeline component. Must be overridden in subclasses'''
        print 'run method not implemented yet for %s' % self.__class__
        logging.info('running the pipeline')

# this function is an example of a pipeline component. We can use the @process decorator to automatically
# add provenance information to the hdf5 file. 
# The docstring is used to generate the desciption 

class DataAverager(PipelineComponent):
    '''
    This class implements averaging over a number of exposures across the darkfields, whitefields and the diffraction data
    '''

    def __init__(self, data_exchange, *args, **kwargs):
        super(DataAverager, self).__init__(data_exchange, title='processed, darkfields, whitefields and data averaged', 
                                           *args, **kwargs)
       
    
        
    def run(self):
        '''
        The method called by the pipeline from outside of this class
        '''
        self.average_raw_data(self.data_exchange)
        
    @process
    def average_raw_data(self, data_exchange, *args, **kwargs):
        '''
        Averages the raw data
        '''
        self.average_raw_darkfields(*args, **kwargs)
        self.average_raw_whitefields(*args, **kwargs)
        self.average_raw_diffraction_images(*args, **kwargs)
        return self.input_group.ref, self.output_group.ref
    
    
    def average_raw_darkfields(self, *args, **kwargs):
        ''' Process raw darkfields
        '''
        raw_darkfields = self.input_group.get_raw_darkfields()
        av = np.average(np.dstack(raw_darkfields), axis=2)
        self.output_group.create_dataset(av, name='data_dark_averaged')
        
    def average_raw_whitefields(self, *args, **kwargs):
        ''' Process raw whitefields
        '''
        raw_whitefields = self.input_group.get_raw_whitefields()
        av = np.average(np.dstack(raw_whitefields), axis=2)
        self.output_group.create_dataset(av, name='data_white_averaged')
        
    def average_raw_diffraction_images(self, *args, **kwargs):
        '''
        average the exposures of diffraction images at each position
        '''
        raw_data = self.input_group.get_raw_dataset().get_array()
        x_positions, y_positions, nx, ny = raw_data.shape[0], raw_data.shape[1], raw_data.shape[3], raw_data.shape[4]
        av_data = np.empty((x_positions, y_positions, nx, ny))  # don't hard code these dimensions
        for x in range(0, x_positions):
            for y in range(0, y_positions):
                av_data[x][y] = np.average(np.dstack(raw_data[x][y]), axis=2)
        self.output_group.create_dataset(av_data, name='data')
    
