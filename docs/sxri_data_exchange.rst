.. _sxri_data_exchange_root:

***********************************************
SXRI implementation of the data exchange format
***********************************************

The sxri_data_exchange module provides a wrapper around a hdf5 file that provides a way of interacting with the file and
perform operations that conform to the DataExchange format specified in the APS document, and to enforce the structure
and conventions the SXR-I beamline at the Australian Synchrotron have chosen to implement this standard with the data
collected at their beamline.

The modules extend from the h5py module which provides a python interface to the hdf5 file and methods for creating and
accessing groups and datasets. The sxri_data_exchange module seeks to further constrain the file structure so that it is
    1) standardised over beamline data collections
    2) Able to be used in an automated processing pipeline which expects a certain data format.

A new SXRIDataExchange object is created using the filename as an argument to the constructor. The __init__ function
automatically takes care of wrapping the existing groups and datasets into one RawExchange class to refer to the exchange
group containing the raw experimental data, and ProcessedExchange groups which mostly are created by the processing
pipeline. The Measurement and Provenance groups are also created which contain much of the information about the
experimental setup used to take the data, and details of the pipeline component steps performed on the data respectively.


