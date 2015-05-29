.. _introduction_root:

***************
Introduction to the SXRI Processing Pipeline
***************

These docs describe the Python modules for the data processing pipeline developed for the Soft X-Ray Imaging beamline at
the Australian Synchrotron. The pipeline consists of two modules: the pipeline logic itself and wrappers around the
HDF5 file that is used as the basis for data storage. The pipeline is heavily dependent on the format of this HDF5 file
which follows the conventions described in the Data Exchange format developed by the Advanced Photon Source
http://www.aps.anl.gov/DataExchange/

The pipeline is designed to allow for the easy addition of modules to perform new processing tasks. Preprocessing steps


