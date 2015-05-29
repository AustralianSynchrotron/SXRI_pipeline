.. _sxri_data_exchange_root:

***************
SXRI implementation of the data exchange format
***************

The sxri_data_exchange module provides a wrapper around a hdf5 file that provides a way of interacting with the file and
perform operations that conform to the DataExchange format specified in the APS document, and to enforce the structure
and conventions the SXR-I beamline at the Australian Synchrotron have chosen to implement this standard with the data
collected at their beamline.

The modules extend from the h5py module which provides a python interface to the hdf5 file and methods for creating and
accessing groups and datasets. The sxri_data_exchange module seeks to further constrain the file structure so that it is
    1. standardised over beamline data collections
    2. Able to be used in an automated processing pipeline which expects a certain data format.

