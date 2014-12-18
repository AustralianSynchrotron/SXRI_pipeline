'''
Created on 17/04/2014

@author: Lenneke Jong <lenneke.jong@synchrotron.org.au>
'''
from sxri_pipeline.pipeline.pipeline_component import PipelineComponent, process
import numpy as np

def run_data_averager(data_exchange):
    '''
    create the DataAverager object and run it.
    '''
    averager = DataAverager(data_exchange)
    averager.run()
    return averager.output_group.get_name()

def run_darkfield_subtractor(data_exchange):
    '''
    create the DarkfieldSubtractor object and run it.
    '''
    subtractor = DarkfieldSubtractor(data_exchange)
    subtractor.run()



# this class is an example of a pipeline component. We can use the @process decorator to automatically
# add provenance information to the hdf5 file. 
# The docstring is used to generate the description 

class DataAverager(PipelineComponent):
    '''
    This class implements averaging over a number of exposures across the darkfields, whitefields and the diffraction data
    '''

    def __init__(self, data_exchange, *args, **kwargs):
        '''
        Constructor
        '''
        super(DataAverager, self).__init__(data_exchange, title='processed, darkfields, whitefields and data averaged', 
                                           *args, **kwargs)
       
    
        
    def run(self):
        '''
        The method called by the pipeline from outside of this class
        '''
        self.average_raw_data(self.data_exchange)
        
    @process
    def average_raw_data(self, data_exchange, *args, **kwargs):
        ''' Averages the raw data
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
        ''' average the exposures of diffraction images at each position
        '''
        raw_data = self.input_group.get_raw_dataset().get_array()
        x_positions, y_positions, nx, ny = raw_data.shape[0], raw_data.shape[1], raw_data.shape[3], raw_data.shape[4]
        av_data = np.empty((x_positions, y_positions, nx, ny))  # don't hard code these dimensions
        for x in range(0, x_positions):
            for y in range(0, y_positions):
                av_data[x][y] = np.average(np.dstack(raw_data[x][y]), axis=2)
        self.output_group.create_dataset(av_data, name='data')


class DarkfieldSubtractor(PipelineComponent):
    '''
    This class implements removing the averaged darkfield from the averaged diffraction images
    '''

    def __init__(self, data_exchange, *args, **kwargs):
        super(DarkfieldSubtractor, self).__init__(data_exchange, title='subtracts average darkfield from the averaged diffraction images', 
                                           *args, **kwargs)

    def run(self):
        '''
        The method called by the pipeline from outside of this class
        '''
        pass

