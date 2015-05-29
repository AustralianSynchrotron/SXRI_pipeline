'''
Created on 17/04/2014

@author: Lenneke Jong <lenneke.jong@synchrotron.org.au>
'''
from pipeline.pipeline_component import PipelineComponent, process
import numpy as np

#def run_data_averager(data_exchange):
#    '''
#    create the DataAverager object and run it.
 #   '''
 #   averager = DataAverager(data_exchange)
 #   averager.run()
#    return averager.output_group.get_name()



def run_preprocessing(data_exchange):
    '''
    Run a multi-step preprocessing routine
    '''
    preprocessor = Preprocessor(data_exchange)
    preprocessor.run()


# this class is an example of a pipeline component. We can use the @process decorator to automatically
# add provenance information to the hdf5 file. 
# The docstring is used to generate the description 

class Preprocessor(PipelineComponent):
    '''
    This class implements averaging over a number of exposures across the darkfields, whitefields and the diffraction data
    as well as assorted other preprocessing steps.
    '''

    def __init__(self, data_exchange, *args, **kwargs):
        '''
        Constructor
        '''
        super(Preprocessor, self).__init__(data_exchange, title='processed, darkfields, whitefields and data averaged', 
                                           *args, **kwargs)

    
        
    def run(self):
        '''
        The method called by the pipeline from outside of this class
        '''
        self.process_raw_data(self.data_exchange)
        
        
    @process
    def process_raw_data(self, data_exchange, *args, **kwargs):
        ''' Processes the raw data
        '''
        self.average_raw_darkfields(*args, **kwargs)
        self.average_raw_whitefields(*args, **kwargs)
        self.average_raw_diffraction_images(*args, **kwargs)
        self.subtract_averaged_darkfields(*args,**kwargs)
        self.calculate_and_apply_threshold(*args,**kwargs)
        return self.input_group.ref, self.output_group.ref

    def average_raw_darkfields(self, *args, **kwargs):
        ''' Average all the raw darkfields and create a new dataset in the output group
        '''
        raw_darkfields = self.input_group.get_raw_darkfields()
        av = np.average(np.dstack(raw_darkfields), axis=2)
        self.output_group.create_dataset(av, name='data_dark_averaged')

    def average_raw_whitefields(self, *args, **kwargs):
        ''' Average all the raw whitefields and create a new dataset in the output groupww
        '''
        raw_whitefields = self.input_group.get_raw_whitefields()
        av = np.average(np.dstack(raw_whitefields), axis=2)
        self.output_group.create_dataset(av, name='data_white_averaged')

    def average_raw_diffraction_images(self, *args, **kwargs):
        ''' average the exposures of diffraction images at each position
            - 15/07/14 now also subtracts the averaged darkfield.
        '''
        raw_data = self.input_group.get_raw_dataset().get_array()
        x_positions, y_positions, nx, ny = raw_data.shape[0], raw_data.shape[1], raw_data.shape[3], raw_data.shape[4]
        av_data = np.empty((x_positions, y_positions, nx, ny))  
        #av_darkfield=self.output_group.get_dataset('data_dark_averaged').get_array() # av_darkfield is one image
        for x in range(x_positions):
            for y in range(y_positions):
                av_data[x][y] = np.average(np.dstack(raw_data[x][y]), axis=2)
        self.output_group.create_dataset(av_data, name='data_averaged')


    def subtract_averaged_darkfields(self,*args, **kwargs):
        '''
        Subtract the averaged darkfield frames from the averaged data and whitefield frames
        '''
        av_darkfield=self.output_group.get_dataset('data_dark_averaged').get_array() # av_darkfield is one image
        av_data = self.output_group.get_dataset('data_averaged').get_array()
        av_whitefield = self.output_group.get_dataset('data_dark_averaged').get_array() 
        
        av_data_sub_dark = av_data - av_darkfield
        av_data_sub_dark.clip(0)
        av_whitefield_sub_dark = av_whitefield - av_darkfield
        av_whitefield_sub_dark.clip(0)
        self.output_group.create_dataset(av_data_sub_dark,name="data_averaged_sub_dark")
        self.output_group.create_dataset(av_whitefield_sub_dark,name="data_white_sub_dark")
    
    def calculate_and_apply_threshold(self,*args,**kwargs):
        '''
        Calculate the threshold from a corner from a whitefield image.
        '''
        whitefield_corner = self.output_group.get_dataset('data_white_sub_dark').get_array()[5:10,5:10]
        thresh = (np.mean(whitefield_corner)-np.max(whitefield_corner))/2
        data_thresholded = self.output_group.get_dataset('data_averaged_sub_dark').get_array() - thresh# apply threshold
        data_thresholded.clip(0)
        data_white_thresholded = self.output_group.get_dataset('data_white_sub_dark').get_array() -thresh
        data_white_thresholded.clip(0)
        self.output_group.create_dataset(data_thresholded,name="data_averaged_sub_dark_threshold")
        self.output_group.create_dataset(data_white_thresholded,name="data_white_sub_dark_threshold")