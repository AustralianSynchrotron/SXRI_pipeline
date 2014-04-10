'''
Created on 28/03/2014

@author: Lenneke Jong <lenneke.jong@synchrotron.org.au>

'''
import sxri_data_exchange 
import numpy as np
from functools import wraps

def process(f):
    @wraps(f)
    def wrapper(data_exchange,logfile,*args,**kwargs):
        process=data_exchange.add_process(f.__name__,f.__doc__)
        input_ref,output_ref=f(data_exchange,logfile,*args,**kwargs)
        process.input_data=input_ref
        process.output_data=output_ref
        return
    return wrapper

# this function is an example of a pipeline component. We can use the @process decorator to automatically
# add provenance information to the hdf5 file. 
# The docstring is used to generate the desciption 
@process
def process_raw_darkfields(data_exchange,logfile,*args,**kwargs):
    ''' Process raw darkfields
    '''
    input_group=data_exchange.get_raw_exchange_group()
    raw_darkfields = input_group.get_raw_darkfields()
    av=np.average(np.dstack(raw_darkfields),axis=2)
    output_group=data_exchange.create_exchange_group('processed, darkfields averaged')
    output_data=output_group.create_dataset(av)
    return raw_darkfields.ref,output_data.ref