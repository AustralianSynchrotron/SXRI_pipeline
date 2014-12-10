.. _pipeline_root:

*************************
SXRI Processing Pipeline
*************************

Entry point into the pipeline is in pipeline_main.

current assumptions for pipeline
- each component in a pipeline will produce a new exchange group for the processed data
- 
- up to the individual components to figure out what their input group should be
- currently no re-entry if any error happens, the pipeline will exit & data file may be left in a corrupt state. May need to find a way to roll back?
 
