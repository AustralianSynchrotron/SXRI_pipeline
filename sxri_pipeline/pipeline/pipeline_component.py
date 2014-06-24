'''
Created on 28/03/2014

@author: Lenneke Jong <lenneke.jong@synchrotron.org.au>

'''
import sxri_data_exchange
from functools import wraps
import logging


def process(f):
    '''
     Decorator to use on the main function that is running a pipeline component
     It will add the correct information, including references, to the
     provenance group and create a correctly named exchange group
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
    
    
    def __init__(self, data_exchange, input_group_name=None, *args, **kwargs):
        '''Constructor'''
        self.data_exchange = data_exchange
        if input_group_name is None:
            if len(self.data_exchange.exchange_groups) == 1:
                self.input_group = self.data_exchange.get_raw_exchange_group()
            else:
                #default to the last group created becoming input group
                self.input_group = self.data_exchange.exchange_groups[-1]
        else:
            in_group = self.data_exchange.find_exchange_group_by_name(input_group_name)
            if isinstance(in_group,sxri_data_exchange.exchange.ProcessedExchange):
                self.input_group = in_group
        self.output_group = data_exchange.create_exchange_group(*args, **kwargs)
    
 
    def run(self):
        '''Method which will be called to run this pipeline component. Must be 
        overridden in subclasses'''
        print 'run method not implemented yet for %s' % self.__class__
        logging.info('running the pipeline')

# this function is an example of a pipeline component. We can use the @process decorator to automatically
# add provenance information to the hdf5 file. 
# The docstring is used to generate the desciption 


