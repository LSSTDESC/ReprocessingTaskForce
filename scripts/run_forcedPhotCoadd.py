#!/usr/bin/env python

import os
import time
import re
import glob
import libRun as LR

def build_cmd(patch, configFile, filt, input, output):
    if not os.path.isdir("scripts/" + filt) :
        os.makedirs("scripts/" + filt)
        
    cmd = "mv "+ patch + " scripts/" + filt
    os.system(cmd)

    cmd = "forcedPhotCoadd.py %s --output %s"  % (input, output) + " @scripts/" + \
          filt + "/" + patch + " --configfile " + configFile + " --clobber-config --clobber-versions"
    print cmd
    return cmd

if __name__ == "__main__":

    filters = "ugriz"
    
    usage = """%prog [option]"""
    
    description = """This script will run forcedPhotCoadd for a given list of filters and patches. 
    The  default if to use f.list files (where 'f' is a filter in ugriz) and patches_f.txt, 
    and launch forcedPhotCoadd in several batch jobs. You thus need to be running it at CC-IN2P3 
    to make it work. To run all  filters, you can do something like 
    %prog -f ugriz -m 1 -c YOURCONFIGFILE -a"""
    
    opts, args = LR.standard_options(usage=usage, description=description, filters=filters)

    for filt in opts.filters:
        if filt not in filters:
            sys.exit("Unknown filter : " + filt)

        filePatch = "patches_" + filt + ".txt"    
        cmd = "split -l " + str(opts.mod) + " -d " + filePatch + " _" + filePatch
        print cmd
        os.system(cmd)
    
        patchList = glob.glob("_patches_" + filt + "*")
    
        for patch in sorted(patchList):
            print patch
            cmd = build_cmd(patch, opts.configs, filt, opts.input, opts.output)
            LR.submit(cmd, patch, filt, autosubmit=opts.autosubmit, ct=60000,
                      vmem='8G', queue='huge')
