'''
Created on 17/04/2014

@author: Lenneke Jong

This module contains classes for fresnel whitefield reconstruction tasks as well as the full fresnel reconstruction task.
'''
import os,sys


from pipeline.pipeline_component import PipelineComponent, process
from pyNADIA.fresnelcdiwf import PyFresnelCDIWF
from pyNADIA.fresnelcdi import PyFresnelCDI
from pyNADIA.complex2d import PyComplex2D
from pyNADIA.double2d import PyDouble2D
from pyNADIA.phasediversecdi import PyPhaseDiverseCDI,CROSSCORRELATION,MINIMUMERROR

import numpy


class FresnelWhitefieldRecoTask(PipelineComponent):
    '''
    This class provides methods for the fresnel whitefield reconstruction tasks
    '''


    def __init__(self, sxri_data_exchange, num_iterations=25, normalisation=1.0
                 , *args, **kwargs):
        '''
        Constructor
        Sets up the various group objects (in superclass) and attributes for reconstruction parameters.
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
                pydub2d = PyDouble2D(self.data_exchange.nx,self.data_exchange.ny)
               # input_array = initial_array.copy()
                #pydub2d = PyDouble2D()
                #pydub2d.set_array_ptr(input_array)
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

class FresnelRecoTask(PipelineComponent):
    
    
    def __init__(self, sxri_data_exchange, input_group_name=None, num_iterations=25, normalisation=1.0
                 , *args, **kwargs):
        '''
        Constructor
        '''
        super(FresnelRecoTask, self).__init__(sxri_data_exchange, 
                                                        input_group_name=input_group_name,
                                                        title='Fresnel ptycography reconstruction',
                                                        *args, **kwargs)
        print "initialising FresnelRecoTask"
        self.fsd = numpy.average(sxri_data_exchange.measurement_groups[0].focal_sample_distance, axis=2)
        self.ftd = numpy.average(sxri_data_exchange.measurement_groups[0].focal_detector_distance, axis=2)
        self.pixel_size = sxri_data_exchange.measurement_groups[0].pixel_size
        self.wavelength = sxri_data_exchange.measurement_groups[0].wavelength
        # self.whitefield_data = sxri_data_exchange.get_processed_whitefields()
#        self.zpfd = zone plate to focal distance
        self.num_positions = self.data_exchange.x_positions * self.data_exchange.y_positions
        self.normalisation = normalisation
        self.num_iterations = num_iterations  # set a default?
        self.reco_objects = {}
        self.recos = self.init_numpy_reco_objects()
        self.whitefield_recos=self.get_reconstructed_whitefield()
        self.initial_intensities=self.get_input_data()
        self.object_estimates = {}
        self.pd = PyPhaseDiverseCDI()
        self.result_array=numpy.zeros([self.data_exchange.nx, self.data_exchange.ny], dtype=numpy.complex)
        print "init done"

    def init_numpy_reco_objects(self):
        '''
        Creates a dictionary numpy arrays corresponding to the complex 2d array obtained by
        reconstruction routine. We pass the pointer to the underlying data to a PyComplex2D object which 
        is then passed to the PyFresnelCDI object. This array holds the final result of the reconstructions.
        The next step is to see if it is possible to use the 1 multi-dimensional array and use memory views, 
        but the underlying array may not be contiguous then, depending on how we specify it. 
        '''
        self.main_object=numpy.zeros([self.data_exchange.nx, self.data_exchange.ny], dtype=numpy.complex)
        recos = {}
        for x in range(self.data_exchange.x_positions):
            for y in range(self.data_exchange.y_positions):
                reco = numpy.zeros([self.data_exchange.nx, self.data_exchange.ny], dtype=numpy.complex)
                recos[x * self.data_exchange.y_positions + y] = reco
        print "initialised numpy reco objects"
        return recos

    def get_input_data(self):
        '''Read the input data from the hdf5 file and create a dictionary of 
        PyDouble2D objects corresponding to the initial data for each position.
        '''
        initial_array = self.input_group.get_dataset('data_averaged_sub_dark_threshold').get_array()
        print initial_array.shape
        initial_dict = {}
        for x in range(0, self.data_exchange.x_positions):
            for y in range(0, self.data_exchange.y_positions):
                input_array = initial_array[x,y]
                pydub2d = PyDouble2D()
                pydub2d.set_array_ptr(input_array)
                initial_dict[x * self.data_exchange.y_positions + y] = pydub2d
        print "got the input data"
        return initial_dict

    def get_reconstructed_whitefield(self):
        '''Get the reconstructed whitefield'''
        whitefield_recos_group = self.data_exchange.find_exchange_group_by_title('Fresnel whitefield reconstruction')
        dset = whitefield_recos_group.get_dataset('whitefield_reconstructions')
        whitefields_dict ={}
        big_array=dset.get_array()
        if len(dset.shape)>2: #if there are more than one reconstructed whitefields to use loop over them for all positions
            for x in range(self.data_exchange.x_positions):
                for y in range(self.data_exchange.y_positions):
                    wf_array=big_array[x][y].copy()
                    wf=PyComplex2D()
                    wf.set_array_ptr(wf_array)
                    whitefields_dict[x * self.data_exchange.y_positions + y] = wf
        else: #use only the one whitefield, will need to check if this is ok later
            wf=PyComplex2D()
            wf_array=dset.copy()
            wf.set_array_ptr(wf_array)
            for i in range(self.data_exchange.x_positions*self.data_exchange.y_positions):
                whitefields_dict[i]=wf
        self.input_groups.append(whitefield_recos_group)
        self.input_group_refs.append(whitefield_recos_group.ref)
        print "got reconstructed whitefields"
        return whitefields_dict

    def create_support(self, nx, ny, default=163e-6):
        '''
        create a support object, either from a function or the default
        '''
        from math import sqrt
        support = PyDouble2D(nx,ny)
        beam_fraction=0.5
        i0=(nx-1)/2.0
        j0=(ny-1)/2.0

        for i in range(0,nx):
            for j in range(0,ny):
                if sqrt((i-i0)*(i-i0)+(j-j0)*(j-j0)) < beam_fraction*sqrt(j0*j0+i0*i0):
                    support.set(i,j,100)
                else:
                    support.set(i,j,0)
        return support

    def initialise_reconstructions(self, x_positions, y_positions):
        '''
        Set up the PyFresnelCDI objects and do initial steps 
        '''
        for x in range(0, x_positions):
            for y in range(0, y_positions):
                i = x * y_positions + y
                # need to pass in a PyComplex2D, not just a 2D array
                object_estimate = PyComplex2D(self.data_exchange.nx, self.data_exchange.ny)
                object_estimate.set_array_ptr(self.recos[i])
                self.object_estimates[i] = object_estimate
                print self.object_estimates[i].getSizeX()
                print self.whitefield_recos[i].getSizeY()
                reco_object = PyFresnelCDI(self.object_estimates[i], self.whitefield_recos[i], self.wavelength, self.ftd[x][y], self.fsd[x][y], self.pixel_size, self.normalisation)
                reco_object.initialiseEstimate()
                reco_object.setSupport(self.create_support(self.data_exchange.nx,self.data_exchange.ny))
                reco_object.setIntensity(self.initial_intensities[i])
                if self.complex_constraint:
                    reco_object.setComplexConstraint(self.complex_constraint)
                self.reco_objects[i] = reco_object
                self.pd.addNewPosition(reco_object, x,y)

    @process
    def fresnel_reconstruction(self, data_exchange, *args, **kwargs):
        '''
        Fresnel reconstruction
        '''
        #temp_result = PyDouble2D()
        self.initialise_reconstructions(self.data_exchange.x_positions, self.data_exchange.y_positions)
        result = PyComplex2D()
        result.set_array_ptr(self.result_array)
        self.pd.initialiseEstimate()
        for i in range(0,self.num_iterations):
            if i==0:
                self.pd.adjustPositions(CROSSCORRELATION)
            if i==10:
                self.pd.adjustPositions(MINIMUMERROR)
            self.pd.iterate()
            # shrinkwrap?
        result = self.pd.getTransmissionFunction()
        self.output_group.create_dataset(self.result_array, "fresnel ptycographic result")
        return self.input_group_refs, self.output_group.ref
    
    @process    
    def test(self,data_exchange, *args, **kwargs):
        '''testing multiple input groups'''
        self.get_reconstructed_whitefield()
        print self.input_group_refs
        return self.input_group_refs,self.output_group.ref
        
    def run(self):
        '''
        Run the fresnel reconstruction
        '''
        self.fresnel_reconstruction(self.data_exchange)
        
        
        
#     # run the reconstruction
#     for i in range(0, 20):
#         print "iteration %d" % i
# 
#         # apply the iterations  
#         proj.iterate(); 
#         print "Error: %f" % proj.getError()
# 
#         if i % 5 == 0:
#             # output the current estimate of the object
#             result = object_estimate.get2dMAG()
#             temp_str = "fcdi_example_iter_%d.ppm" % i
#             result.write_ppm(temp_str)
#     
#             # apply the shrinkwrap algorithm
#             proj.applyShrinkwrap(2, 0.1);
# 
#        
#        
# 
#     # output results
#     print "done iterating"
#     trans = PyComplex2D(nx, ny)
#     trans = proj.getTransmissionFunction()
# 
#    # result=trans.get2dMAG()
#     result = proj.getTransmissionFunction().get2dMAG()
# 
#     result.write_ppm("fcdi_example_trans_mag.ppm", log_scale=True)
# 
#     result = trans.get2dPHASE()
#     result.write_ppm("fcdi_example_trans_phase.ppm")
# 
#     print "done!"
    
    
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
    '''
    do a full ptycographic fresnel reco
    '''
    fpreco=FresnelRecoTask(data_exchange,"/exchange_1")
    fpreco.run()
    print "done3"
