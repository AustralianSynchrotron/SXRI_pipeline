'''
Created on 07/10/2013

@author: Lenneke Jong
'''
from group import Group

class MeasurementGroup(Group):
    '''
    classdocs
    '''


    def __init__(self,h5group,name,*args,**kwargs):
        '''
        Constructor
        '''
        self.h5group=h5group
        self.name=name
        # self.sample=Sample(self.h5group.create_group("sample"))
        # self.measurement=Instrument(self.h5group.create_group("instrument"))
                           
        
        def get_pixel_size(self):
            pass
        
        def get_zp_distance(self):
            pass
        
        
class Sample(Group):
    '''sample class'''
    
    @property
    def name(self):
        return self.get_dataset("name")
        
    @name.setter
    def name(self, value):
        self.set_dataset("name",value)
    
    @property
    def description(self):
        return self.get_dataset("description")
    
    @description.setter
    def description(self,value):
        self.set_dataset("description",value)
    
    @property
    def environment(self):
        return self.get_dataset("environment")
    
    @environment.setter
    def environment(self,value):
        self.set_dataset("environment",value)
    
    @property
    def mass(self):
        return self.get_dataset("mass")

    @mass.setter
    def mass(self,value):
        m=self.set_dataset("mass",value)
        m.attrs['units']='g'

    @property
    def preparation_date(self):
        return self.get_dataset("preparation_date")
    
    @preparation_date.setter
    def preparation_date(self,value):
        self.set_dataset("preparation_date",value)
    
    @property
    def temperature(self):
        return self.get_dataset("temperature")
    
    @temperature.setter
    def temperature(self,value):
        t=self.set_dataset("temperature",value)
        t.attrs['units']='Celsius'
    
    @property
    def temperature_set(self):
        return self.get_dataset("temperature_set")
    
    @temperature_set.setter
    def temperature_set(self,value):
        ts=self.set_dataset("temperature_set",value)
        ts.attrs['units']='Celsius'
        
class Experiment(Group):
    
    @property
    def activity(self):
        return self.get_dataset("activity")
    
    @activity.setter
    def activity(self,value):
        self.set_dataset("activity",value)
        
    @property
    def proposal(self):
        return self.get_dataset("proposal")
    
    @proposal.setter
    def proposal(self,value):
        self.set_dataset("proposal",value)
        
    @property
    def safety(self,value):
        return self.get_dataset("safety")
    
    @safety.setter
    def safety(self,value):
        self.set_dataset("safety",value)

class Experimenter(Group):
    
    @property
    def name(self):
        return self.get_dataset("name")
    
    @name.setter
    def name(self,value):
        self.set_dataset("name",value)
        
    @property
    def role(self):
        return self.get_dataset("role")
    
    @role.setter
    def role(self,value):
        self.set_dataset("role",value)
        
    @property
    def affiliation(self):
        return self.get_dataset("affiliation")
    
    @affiliation.setter
    def affiliation(self,value):
        self.set_dataset("affiliation",value)

    @property
    def address(self):
        return self.get_dataset("address")
    
    @address.setter
    def address(self,value):
        self.set_dataset("address",value)

    @property
    def phone(self):
        return self.get_dataset("phone")
    
    @phone.setter
    def phone(self,value):
        self.set_dataset("phone",value)
        
    @property
    def email(self):
        return self.get_dataset("email")
    
    @email.setter
    def email(self,value):
        self.set_dataset("email",value)
        
    @property
    def facility_user_id(self):
        return self.set_dataset("facility_user_id")
    
    @facility_user_id.setter
    def facility_user_id(self,value):
        self.set_dataset("facility_user_id",value)


    