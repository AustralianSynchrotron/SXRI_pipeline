'''
Created on 17/04/2014

@author: Lenneke Jong
'''

from pipeline.pipeline_component import PipelineComponent, process
from pyNADIA.fresnelcdiwf import PyFresnelCDIWF
from pyNADIA.complex2d import PyComplex2D
from pyNADIA.double2d import PyDouble2D

import numpy
# import pyNADIA.fresnelcdi
# import pyNADIA.phasediversecdi

class FresnelWhitefieldRecoTask(PipelineComponent):
    '''
    classdocs
    '''


    def __init__(self, sxri_data_exchange, num_iterations=25, normalisation=1.0
                 , *args, **kwargs):
        '''
        Constructor
        '''
        super(FresnelWhitefieldRecoTask, self).__init__(sxri_data_exchange, 
                                                        input_group_name=None,
                                                        title='Fresnel whitefield reconstruction',
                                                        *args, **kwargs)
        print "initialising FresnelWhitefieldRecoTask"
        self.fsd = sxri_data_exchange.measurement_groups[0].focal_sample_distance
        self.ftd = sxri_data_exchange.measurement_groups[0].focal_detector_distance
        self.pixel_size = sxri_data_exchange.measurement_groups[0].pixel_size
        self.wavelength = sxri_data_exchange.measurement_groups[0].wavelength
        # self.whitefield_data = sxri_data_exchange.get_processed_whitefields()
#        self.zpfd = zone plate to focal distance
        self.num_positions = self.data_exchange.x_positions * self.data_exchange.y_positions
        self.normalisation = normalisation
        self.num_iterations = num_iterations  # set a default?
        self.reco_objects = {}
        self.whitefield_recos = self.init_whitefield_recos()
        self.object_estimates = {}


    def run(self):
        '''
        Run the fresnel whitefield reconstruction task
        '''
        self.initial_intensities = self.get_input_data()
        self.fresnel_whitefield_reconstruction(self.data_exchange)

    def get_input_data(self):
        '''
        Read the input data from the hdf5 file and create a dictionary of 
        PyDouble2D objects corresponding to the initial data for each position.
        '''
        initial_array = self.input_group.get_dataset('data_white_averaged').get_array()
        print(initial_array.shape)
        initial_dict = {}
        for x in range(0, self.data_exchange.x_positions):
            for y in range(0, self.data_exchange.y_positions):
                input_array = initial_array.copy()
                pydub2d = PyDouble2D()
                pydub2d.set_array_ptr(input_array)
                initial_dict[x * self.data_exchange.y_positions + y] = pydub2d
        return initial_dict

    def init_whitefield_recos(self):
        '''
        Creates a dictionary numpy arrays corresponding to the complex 2d array obtained by
        reconstruction routine. We pass the pointer to the underlying data to a PyComplex2D object which 
        is then passed to the PyFresnelCDIWF object. This array holds the final result of the reconstructions.
        The next step is to see if it is possible to use the 1 multi-dimensional array and use memory views, 
        but the underlying array may not be contiguous then, depending on how we specify it. 
        '''
        wf_recos = {}
        for x in range(self.data_exchange.x_positions):
            for y in range(self.data_exchange.y_positions):
                reco = numpy.zeros([self.data_exchange.nx, self.data_exchange.ny], dtype=numpy.complex)
                wf_recos[x * self.data_exchange.y_positions + y] = reco
        return wf_recos


    @process
    def fresnel_whitefield_reconstruction(self, data_exchange, *args, **kwargs):
        '''
        Fresnel whitefield reconstruction
        '''
        # set up the numpy array for reconstructions
     #   self.whitefield_recos = numpy.zeros([self.data_exchange.x_positions, self.data_exchange.y_positions, self.data_exchange.nx, self.data_exchange.ny], dtype=numpy.complex_t)
        self.initialise_reconstructions(self.data_exchange.x_positions, self.data_exchange.y_positions)
        for x in range(0, self.data_exchange.x_positions):
            for y in range(0, self.data_exchange.y_positions):
                self.fresnel_whitefield_iteration(x * self.data_exchange.y_positions + y, self.num_iterations) 
        print "done the recos"
        self.output_group.create_dataset(self.whitefield_recos_to_numpy(), "whitefield_reconstructions")
        print "written to file"
        return self.input_group.ref, self.output_group.ref


    def initialise_reconstructions(self, x_positions, y_positions):
        '''
        Set up the PyFresnelCDIWF objects and do initial steps 
        '''
        for x in range(0, x_positions):
            for y in range(0, y_positions):
                i = x * y_positions + y
                # need to pass in a PyComplex2D, not just a 2D array
                object_estimate = PyComplex2D(self.data_exchange.nx, self.data_exchange.ny)
                object_estimate.set_array_ptr(self.whitefield_recos[i])
                self.object_estimates[i] = object_estimate
                ftd = self.ftd[x][y][0]
                fsd = self.fsd[x][y][0]
                reco_object = PyFresnelCDIWF(object_estimate, self.wavelength, ftd, fsd, self.pixel_size, self.normalisation)
                reco_object.initialiseEstimate(0)
                reco_object.setSupport(163e-6)
                reco_object.setIntensity(self.initial_intensities[i])  # need to create a PyDouble2D object here
                self.reco_objects[i] = reco_object

    def whitefield_recos_to_numpy(self):
        '''
        Copy the individual reconstructed whitefield numpy arrays into a larger one to store in the
        hdf5 file. This is not ideal and if it is possible to use a larger numpy array for all of these and slice according
        it may not be necessary.
        '''
        # need to figure out a way to efficiently reconstruct the "datacube" for the whitefield recos
        wfs = numpy.empty([self.data_exchange.x_positions, self.data_exchange.y_positions, self.data_exchange.nx, self.data_exchange.ny], dtype=numpy.complex_)
        for x in range(self.data_exchange.x_positions):
            for y in range(self.data_exchange.y_positions):
                wfs[x][y] = self.whitefield_recos[x * self.data_exchange.x_positions + y].copy()
        return wfs

    def fresnel_whitefield_iteration(self, i, num_iterations):
        '''
        Do num_iterations on object with index i
        '''
        for ni in range(0, num_iterations):
            success = self.reco_objects[i].iterate()

def fresnel_whitefield_reco(data_exchange, input_group_name):
    '''
        Do a Fresnel whitefield reconstruction on processed frames,
        giving an input group name for a given data_exchange file
    '''
    fwfreco = FresnelWhitefieldRecoTask(data_exchange, input_group_name)
    fwfreco.run()
    print "done"

def fresnel_whitefield_reco2(data_exchange):
    '''
        Do a Fresnel whitefield reconstruction on processed frames 
        for a given data_exchange file
    '''
    fwfreco = FresnelWhitefieldRecoTask(data_exchange)
    fwfreco.run()
    print "done2"

def fresnel_ptyco_reco(data_exchange):
    pass
