#!/usr/bin/env python

import numpy as N
import libRun as LR

def build_cmd(patches, config, filt):
    cmd = "makeCoaddTempExp.py pardir/output --output pardir/output/coadd_dir " + patches + " @" + \
          filt + ".list" + " --configfile " + config
    print "\nCMD:", cmd
    return cmd

if __name__ == "__main__":

    filters = "ugriz"
    
    usage = """%prog [option]"""
    
    description = """This script will run makeCoaddTempExp for a given list of filters and patches. 
    The  default if to use f.list files (where 'f' is a filter in ugriz) and patches_f.txt, 
    and launch processCcd in several batch jobs. You thus need to be running it at CC-IN2P3 to make 
    it work. To run all  filters, you can do something like 
    %prog -f ugriz -m 1 -c makeCoaddTempExpConfig.py -a"""

    opts, args = LR.standard_options(usage=usage, description=description, filters=filters)

    # overwrite the -m option to force it to be 1
    opts.mod = 1

    # Loop over filters
    for filt in opts.filters:

        config = LR.select_config(opts.configs, filt)

        # Get the list of patches
        patches = [" ".join(p) for p in N.loadtxt("patches_" + filt + ".txt", dtype='string')]
        print "INFO: %i patches loaded: " % len(patches)

        # How many jobs should we be running (and how many visit in each?)?
        njobs = LR.job_number(patches, opts.mod, opts.max)

        # Reorganize the visit list in consequence
        patches = LR.organize_items(patches, njobs)

        # Loop over the patches sub lists
        for ps in patches:

            # Build the command line and other things
            cmd = build_cmd(ps[0], config, filt)

            # Only submit the job if asked
            prefix = LR.makeFileName(ps[0])
            LR.submit(cmd, prefix, filt, autosubmit=opts.autosubmit,
                      ct=1000, queue='long', system=opts.system)

    if not opts.autosubmit:
        print "\nINFO: Use option --autosubmit to submit the jobs"

