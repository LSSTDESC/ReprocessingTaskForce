#!/usr/bin/env python

import os
import time
import glob
import libRun as LR

def build_cmd(patch, configFile, filt, input, output):
    if not os.path.isdir("scripts/" + filt) :
        os.makedirs("scripts/" + filt)
        
    cmd = "mv "+ patch + " scripts/" + filt
    os.system(cmd)

    cmd = "detectCoaddSources.py %s --output %s" % (input, output) + " @scripts/" + filt + "/" + patch + " --configfile " + configFile + " --clobber-config --clobber-versions"
    print cmd

    return cmd
    
if __name__ == "__main__":

    filters = "ugriz"
    
    usage = """%prog [option]"""
    
    description = """This script will run detectCoadSources for a given list of filters and patches. 
    The  default if to use f.list files (where 'f' is a filter in ugriz) and patches_f.txt, 
    and launch detectCoadSources in several batch jobs. You thus need to be running it at CC-IN2P3 
    to make it work. To run all  filters, you can do something like 
    %prog -f ugriz -m 1 -c detectCoaddSources.py -a"""
    
    opts, args = LR.standard_options(usage=usage, description=description, filters=filters)

    # overwrite the -m option to force it to be 1 (this is a fast step)
    opts.mod = 100
    
    # Loop over filters
    for filt in opts.filters:

        config = LR.select_config(opts.configs, filt)

        filePatch = "patches_" + filt + ".txt"
        
        cmd = "split -l " + str(opts.mod) + " -d " + filePatch + " _" + filePatch
        print cmd
        os.system(cmd)
        
        patchList = glob.glob("_patches_" + filt + "*")
        
        for patch in patchList :
            print patch

            # Build the command line and other things
            cmd = build_cmd(patch, config, filt, opts.input, opts.output)
            
            # Only submit the job if asked
            prefix = patch
            LR.submit(cmd, prefix, filt, autosubmit=opts.autosubmit, ct=5000, vmem='4G')

    if not opts.autosubmit:
        print "\nINFO: Use option --autosubmit to submit the jobs"
