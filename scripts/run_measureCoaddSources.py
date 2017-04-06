#!/usr/bin/env python

import os
import time
import re
import glob
from optparse import OptionParser
import libRun as LR

def build_cmd(patch, configFile, filt, input, output):
    if not os.path.isdir("scripts/" + filt) :
        os.makedirs("scripts/" + filt)
        
    cmd = "mv "+ patch + " scripts/" + filt
    os.system(cmd)

    cmd = "measureCoaddSources.py %s --output %s" % (input, output) + \
          " @scripts/" + filt + "/" + patch + " --configfile " + configFile + " --clobber-config --clobber-versions"
    print cmd
    return cmd
    
if __name__ == "__main__":

    filters = "ugriz"
    
    usage = """%prog [option]"""
    
    description = """This script will run measureCoaddSources for a given list of filters and visits. 
    The default if to use f.list files (where 'f' is a filter in ugriz), and launch it in 
    several batch jobs. You thus need to be running it at CC-IN2P3 to make it work. To run all 
    filters, you can do something like %prog -f ugriz -m 1 -c processConfig.py,processConfig_u.py -a"""
    
    opts, args = LR.standard_options(usage=usage, description=description, filters=filters)

    for filt in opts.filters:
        if filt not in filters :
            sys.exit("Unknown filter : " + filt)
        
        filePatch = "patches_" + filt + ".txt"
        
        cmd = "split -l " + str(opts.mod) + " -d " + filePatch + " _" + filePatch
        print cmd
        os.system(cmd)
        
        patchList = glob.glob("_patches_" + filt + "*")
        
        for patch in patchList :
            print patch
            cmd = build_cmd(patch, opts.configs, filt, opts.input, opts.output)
            LR.submit(cmd, patch, filt, autosubmit=opts.autosubmit, system='cl7')
