'''
Created on 25/09/2013

@author: Lenneke Jong <lenneke.jong@synchrotron.org.au>
'''

from sxri_data_exchange.dataexchange import SXRIDataExchange
from pipeline.pre_processing import run_preprocessing
from pipeline.fresnel_reconstruction import fresnel_whitefield_reco2, fresnel_ptyco_reco
import logging
import traceback
import argparse



class Pipeline(object):
    '''
    Main class of the data processing pipeline for the SXR-Imaging beamline at
    the Australian Synchrotron.
    '''


    def __init__(self, filepath):
        '''Constructor
            Get the pipeline variables from the hdf5 file itself, but for now
            lets just do some hardcoded setup
        '''
        self.data_exchange = SXRIDataExchange(filepath)
        logging.basicConfig(filename='sxri_pipeline_testing.log',
                            level=logging.DEBUG)
        logging.debug('a debug message')


    def setup_h5py(self):
        '''This function checks that we have the correct data present and will
        report back errors that will mean the pipeline cannot run.
        '''
        self.check_exchange_data()
        self.check_geometry()



    def check_exchange_data(self):
        '''
        Check that there exists an exchange group which contains one dataset
        called data and at least one of each data_dark and data_white.
        '''

        if 'exchange' in self.data_exchange.keys():
            datasets = ['data', 'data_dark', 'data_white']
            if all(x in self.data_exchange.keys() for x in datasets):
                return
            else:
                raise Exception("raw data exchange group for raw data requires \
                    at least datasets named data, data_dark and data_white")
        else: 
            raise Exception('no raw data exchange group found')



    def check_geometry(self):
        '''
        Checks that there are attributes that describe the geometry of the experiment. Not yet implemented
        '''
        pass

    def run(self, *args, **kwargs):
        ''' Run the pipeline, This is the main method in the pipeline class where the separate pipeline modules
            and put together. Some methods here have been commented out for ease with testing, so that steps don't need
            to be rerun. The self.data_exchange argument for each of the methods is required
        '''
        try:
            #self.setup_h5py()
            #run_preprocessing(self.data_exchange)
            # next_input_group_name="/exchange_1"
            #fresnel_whitefield_reco(self.data_exchange, next_input_group_name)
            #fresnel_whitefield_reco2(self.data_exchange)
            #self.data_exchange.print_groups()
            fresnel_ptyco_reco(self.data_exchange)
            self.data_exchange.print_groups()
        except Exception as ex:
            print ex.message
            tb = traceback.format_exc()
            print tb
        finally:
            self.cleanup()


    def cleanup(self):
        '''
        Close the hdf5 file and other cleaning up.
        '''
        self.data_exchange.flush()
        self.data_exchange.close()


def main():
    '''
    Run the pipeline from the command line. pass a hdf as the argument
    '''
    parser = argparse.ArgumentParser(description="Run the SXRI processing pipeline.")
    parser.add_argument('filename', metavar='filename', help='full path of the hdf5 file')
    args = parser.parse_args()
    if args.filename:
        p = Pipeline(args.filename)
        p.run()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
