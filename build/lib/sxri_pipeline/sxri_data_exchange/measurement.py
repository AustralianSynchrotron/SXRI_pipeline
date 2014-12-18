'''
Created on 07/10/2013

@author: Lenneke Jong
'''
from sxri_pipeline.sxri_data_exchange.group import Group
from sxri_pipeline.sxri_data_exchange.instrument import Instrument, Detector, Monochromator
import numpy

class MeasurementGroup(Group):
    '''
    classdocs
    '''


    def __init__(self, h5group, name, *args, **kwargs):
        '''
        Constructor
        '''
        super(MeasurementGroup, self).__init__(h5group, name, *args, **kwargs)


    @property
    def instrument(self):
        return Instrument(self.h5group['instrument'])

    @property
    def sample(self):
        return Instrument(self.h5group['sample'])

    @property
    def wavelength(self):
        energy = self.h5group['instrument']['source']['energy'][0]
        return 1.24e-6 / energy

    @property
    def focal_sample_distance(self):
        '''Helper method to calculate zone plate to sample distances for all positions

        @return a numpy array
        '''
        translation_group = self.instrument.detector.geometry.translation
        return numpy.linalg.norm(numpy.subtract(translation_group['SAM'], translation_group['ZP']), axis=3)

    @property
    def focal_detector_distance(self):
        '''Helper method to calculate zone plate to detector distances for all positions

        @return a numpy array'''
        translation_group = self.instrument.detector.geometry.translation
        return numpy.linalg.norm(numpy.subtract(translation_group['DM'], translation_group['ZP']), axis=3)

    @property
    def pixel_size(self):
        '''Helper method to get pixel size
        '''
        return self.instrument.detector.x_pixel_size[0]

class Sample(Group):
    '''sample class'''

    def __init__(self, h5group, name, *args, **kwargs):
        '''
        Constructor for Sample group
        '''
        super(Sample, self).__init__(h5group, name, *args, **kwargs)

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
    def environment(self):
        '''Environment dataset'''
        return self.get_dataset("environment")

    @environment.setter
    def environment(self, value):
        self.set_dataset("environment", value)

    @property
    def mass(self):
        return self.get_dataset("mass")

    @mass.setter
    def mass(self, value):
        m = self.set_dataset("mass", value)
        m.attrs['units'] = 'g'

    @property
    def preparation_date(self):
        return self.get_dataset("preparation_date")

    @preparation_date.setter
    def preparation_date(self, value):
        self.set_dataset("preparation_date", value)

    @property
    def temperature(self):
        return self.get_dataset("temperature")

    @temperature.setter
    def temperature(self, value):
        t = self.set_dataset("temperature", value)
        t.attrs['units'] = 'Celsius'

    @property
    def temperature_set(self):
        return self.get_dataset("temperature_set")

    @temperature_set.setter
    def temperature_set(self, value):
        ts = self.set_dataset("temperature_set", value)
        ts.attrs['units'] = 'Celsius'

    @property
    def experiment(self):
        return Experiment(self.h5group['experiment'])

    @property
    def experimenter(self):
        return Experimenter(self.h5group['experimenter'])

class Experiment(Group):
    '''
    Wrapper class for the Experiment subgroup
    '''

    def __init__(self, h5group, *args, **kwargs):
        '''
        Constructor for Experiment group
        '''
        super(Experiment, self).__init__(h5group, *args, **kwargs)

    @property
    def activity(self):
        return self.get_dataset("activity")

    @activity.setter
    def activity(self, value):
        self.set_dataset("activity", value)

    @property
    def proposal(self):
        return self.get_dataset("proposal")

    @proposal.setter
    def proposal(self, value):
        self.set_dataset("proposal", value)

    @property
    def safety(self):
        return self.get_dataset("safety")

    @safety.setter
    def safety(self, value):
        self.set_dataset("safety", value)

class Experimenter(Group):
    '''
    Wrapper class for the Experimenter subgroup
    '''

    def __init__(self, h5group, *args, **kwargs):
        '''
        Constructor for Experimenter group
        '''
        super(Experimenter, self).__init__(h5group, *args, **kwargs)

    @property
    def name(self):
        return self.get_dataset("name")

    @name.setter
    def name(self, value):
        self.set_dataset("name", value)

    @property
    def role(self):
        return self.get_dataset("role")

    @role.setter
    def role(self, value):
        self.set_dataset("role", value)

    @property
    def affiliation(self):
        return self.get_dataset("affiliation")

    @affiliation.setter
    def affiliation(self, value):
        self.set_dataset("affiliation", value)

    @property
    def address(self):
        return self.get_dataset("address")

    @address.setter
    def address(self, value):
        self.set_dataset("address", value)

    @property
    def phone(self):
        return self.get_dataset("phone")

    @phone.setter
    def phone(self, value):
        self.set_dataset("phone", value)

    @property
    def email(self):
        return self.get_dataset("email")

    @email.setter
    def email(self, value):
        self.set_dataset("email", value)

    @property
    def facility_user_id(self):
        return self.get_dataset("facility_user_id")

    @facility_user_id.setter
    def facility_user_id(self, value):
        self.set_dataset("facility_user_id", value)


