'''
Created on 17/03/2014

@author: jongl
'''
from group import Group

class Process(Group):
    '''
    classdocs
    '''

    

    def __init__(self, params):
        '''
        Constructor
        '''
        
        
    
    @property
    def name(self):
        return self.get_dataset("name")
        
    @name.setter
    def name(self, value):
        self.set_dataset("name", value)
    
    @property
    def description(self):
        return self.get_dataset("description")
    
    @description.setter
    def description(self, value):
        self.set_dataset("description", value)
    
    @property
    def version(self):
        return self.get_dataset("version")
    
    @version.setter
    def version(self, value):
        self.set_dataset("version", value)
        
    @property
    def input(self):
        return self.get_dataset("input_data")
    
    @input.setter
    def input(self, value):
        self.set_dataset("input", value)
        
    @property
    def output(self):
        return self.get_dataset("output")
    
    @output.setter
    def output(self, value):
        self.set_dataset("output", value)
        
    def add_other_property(self, propname, value):
        property(self.get_dataset(propname), self.set_dataset(propname, value))
        
        
        
        
        
