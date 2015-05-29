'''
Created on 28/03/2014

@author: Lenneke Jong <lenneke.jong@synchrotron.org.au>

This module provides the basic pipeline component class and process decorator for the SXRI processing pipeline.


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
        input_refs, output_ref = f(self, data_exchange, *args, **kwargs)
        _process.input_data = input_refs
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
        self.input_group_refs=[]
        self.input_groups=[]
        if input_group_name is None:
            if len(self.data_exchange.exchange_groups) == 1:
                self.input_groups.append(self.data_exchange.get_raw_exchange_group())
                self.input_group_refs.append(self.data_exchange.get_raw_exchange_group().ref)
            else:
                #default to the last group created becoming input group
                self.input_groups.append(self.data_exchange.exchange_groups[-1])
                self.input_group_refs.append(self.data_exchange.exchange_groups[-1].ref)
        else:
            in_group = self.data_exchange.find_exchange_group_by_name(input_group_name)
            if isinstance(in_group,sxri_data_exchange.exchange.ProcessedExchange):
                self.input_groups.append(in_group)
                self.input_group_refs.append(in_group.ref)
        self.input_group=self.input_groups[0] #most components only have 1 input group so we'll default to that
        self.output_group = data_exchange.create_exchange_group(*args, **kwargs)
    
 
    def run(self):
        '''Method which will be called to run this pipeline component. Must be 
        overridden in subclasses'''
        print 'run method not implemented yet for %s' % self.__class__
        logging.info('running the pipeline')




