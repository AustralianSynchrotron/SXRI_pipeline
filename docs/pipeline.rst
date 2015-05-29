.. _pipeline_root:

************************
SXRI Processing Pipeline
************************


The pipeline module provides classes and methods to construct a processing pipeline.
The PipelineComponent class provides the base class for creating new components so that all new components follow
convention on how they are accessed.

The pipeline_main provides the main Pipeline class which in instantiated and run by calling its "run" method from either
the command line or the __main__ method in pipeline main.
This classes main purpose is to hold a reference to an SXRIDataExchange object which wraps the hdf5 file used by the pipeline.
This class and the other classes in the sxri_data_exchange package provide methods to access the groups and datasets in the
hdf5 file and ensures the conventions specified by the data exchange format are followed.

The @process decorator forms an important part of the way the pipeline keeps track of data provenance. When an
SXRIDataExchange object is instantiated it creates further objects that wrap around the various groups

The fresnel_reconstruction module makes use of the Python bindings to the NADIA library
https://github.com/AustralianSynchrotron/nadia-coecxs and utilises it's routines for
fresnel whitefield reconstruction and the full fresnel_reconstruction. However, the pipeline framework is designed so
that different routines could be used for reconstruction steps. The only requirement is that the new pipeline components
can handle any further manipulation of data from the numpy arrays returned by the sxri_data_exchange methods
into whatever form it needs.

