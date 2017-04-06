#!/usr/bin/env python

import os
import glob
import libRun as LR

def build_cmd(patch, configFile, input, output) :

    if not os.path.isdir("scripts") :
        os.makedirs("scripts")
        
    cmd = "mv "+ patch + " scripts"
    os.system(cmd)

    cmd = "mergeCoaddMeasurements.py %s --output %s"  % (input, output) + " @scripts/" + \
          patch + " --configfile " + configFile + " --clobber-config --clobber-versions"
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

    configFile = opts.configs

    filePatch = "patches.txt"

    modularity = opts.mod
    maxPatch = opts.max 
    
    cmd = "split -l " + str(modularity) + " -d " + filePatch + " _" + filePatch
    print cmd
    os.system(cmd)

    patchList = glob.glob("_patches*")
    
    for patch in sorted(patchList):
        print patch
        cmd = build_cmd(patch, configFile, opts.input, opts.output)
        LR.submit(cmd, patch, autosubmit=opts.autosubmit)
