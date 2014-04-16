'''
Created on 25/09/2013

@author: Lenneke Jong <lenneke.jong@synchrotron.org.au>
'''
import os
os.environ["LD_RUN_PATH"] = '../../lib'
from sxri_data_exchange.dataexchange import SXRIDataExchange
import pipeline_component
import logging
# from pre_processing import average_frameset, subtract_darkfield
# from pyNADIA.double2d import PyDouble2D
# from pyNADIA.complex2d import PyComplex2D

class Pipeline(object):
    '''
    Main class of the data processing pipeline for the SXR-Imaging beamline at the Australian Synchrotron.
    '''
 
    
    def __init__(self, filepath):
        '''Constructor
            Get the pipeline variables from the hdf5 file itself, but for now lets just do some hardcoded setup
        '''
        self.data_exchange = SXRIDataExchange(filepath)
        self.test_setup(filepath)
        logging.basicConfig(filename='sxri_pipeline_testing.log',level=logging.DEBUG)
        logging.debug('a debug message')
        
    def test_setup(self, filepath):
        '''
        Some hardcoded values for development and testing of the pipeline. All these values should be included in the 
        hdf5 file itself or derived from such values.
        '''
        logging.info('running the test setup')
        self.beam_wavelenth = 4.892e-10
        self.zone_focal_length = 16.353e-3
        self.focal_detector_length = 0.909513 - 16.353e-3
        self.pixel_size = 13.5e-6
        self.wf_support = 163e-6
        self.wf_initial_estimate = 0
        self.components = ['process_raw_darkfields']  # this is a list of component names that we will call for this particular pipeline
    
    def setup_h5py(self):
        '''This function checks that we have the correct data present and will
        report back errors that will mean the pipeline cannot run. 
        '''
        self.check_exchange_data()
        self.check_geometry()
        
    
    
    def check_exchange_data(self):
        '''
        check that there exists an exchange group which contains one dataset called data and at least
        one of each data_dark and data_white.
        '''
        pass
    
    def check_geometry(self):
        '''
        Checks that there are attributes that describe the geometry of the experiment. 
        '''
        pass
    

    def run(self, *args, **kwargs):
        ''' Run the pipeline
        '''
        averager = pipeline_component.DataAverager(self.data_exchange)
        averager.run()
        self.cleanup()
        print 'done'
        
    def cleanup(self):
        '''
        Close the hdf5 file and other cleaning up.
        '''
        self.data_exchange.close()
        
        
def main():
    p = Pipeline('/home/jongl/SXRI/sxri-test.h5')
    p.run()

        
if __name__ == "__main__":
    main()
