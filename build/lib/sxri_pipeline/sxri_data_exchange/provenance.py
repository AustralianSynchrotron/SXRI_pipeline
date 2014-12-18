'''
Created on 07/10/2013

@author: Lenneke Jong
'''

import re
import h5py
from sxri_pipeline.sxri_data_exchange.group import Group


class ProvenanceGroup(Group):
    '''
    ProvenanceGroup wraps the 'provenance' group sitting in the root of the hdf5 file. 
    '''
    

    def __init__(self, h5group, *args, **kwargs):
        '''
        Constructor
        '''
        super(ProvenanceGroup, self).__init__(h5group, *args, **kwargs)
        self.process_groups = [self.h5group[k] for k in self.h5group.keys() if re.findall('process', k)]
       

    def create_process(self, name, description):
        ''''create a process group containing a name and description'''
        n = len(self.process_groups)
        group_name = "process"
        if n > 0:
            new_process_group = ProcessGroup(self.h5group.create_group("%s_%s" % (group_name, n)))
        else:
            new_process_group = ProcessGroup(self.h5group.create_group(group_name))
        self.process_groups.append(new_process_group)
        new_process_group.process_name = name
        new_process_group.description = description
        return new_process_group


    def add_process(self, actor, start_time, status, message, reference, description):
        if not actor in self.processes:
            return "Process not recognised"
        else:
            pg = ProcessGroup(self.h5group.create_group(actor))
            # create an entry in the process table
            return pg


class ProcessGroup(Group):
    '''
    ProcessGroup wraps a 'process' subgroup which contains information describing each 
    processing step that happens to in the data pipeline. It contains references to the input 
    output data used.
    '''
    
    def __init__(self, h5group):
        super(ProcessGroup, self).__init__(h5group)
        
    
    @property
    def process_name(self):
        return self.h5group["process_name"]
    
    @process_name.setter
    def process_name(self, value):
        if 'process_name' in self.h5group.keys():
            self.h5group['process_name'] = value
        else:
            self.create_string_dataset('process_name', data=value)
        
    @property
    def description(self):
        return self.h5group["description"]
    
    @description.setter
    def description(self, value):
        if 'description' in self.h5group.keys():
            self.h5group['description'] = value
        else:
            self.create_string_dataset('description', data=value)
        
    @property
    def input_data(self):
        return self.h5group['input_data']
    
    @input_data.setter
    def input_data(self, value):
        if 'input_data' in self.h5group.keys():
            self.h5group['input_data'] = value
        else:
            self.h5group.create_dataset('input_data', data=value, dtype=h5py.special_dtype(ref=h5py.Reference))
        
    @property
    def output_data(self):
        return self.h5group['output_data']
    
    @output_data.setter
    def output_data(self, value):
        if 'output_data' in self.h5group.keys():
            self.h5group['output_data'] = value
        else:
            self.h5group.create_dataset('output_data', data=value, dtype=h5py.special_dtype(ref=h5py.Reference))

    
