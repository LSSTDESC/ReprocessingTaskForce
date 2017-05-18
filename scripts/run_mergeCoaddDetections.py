#!/usr/bin/env python

import os
import time
import re
import glob
from optparse import OptionParser
import libRun as LR

def build_cmd(patch, configFile, input, output):

    if not os.path.isdir("scripts"):
        os.makedirs("scripts")

    cmd = "mergeCoaddDetections.py %s --output %s"  % (input, output) + \
          " @" + patch + " --configfile " + configFile

    return cmd

if __name__ == "__main__":

    usage = """%prog [option]"""

    description = """This script will run mergeCoaddDetections for a given list of filters and patches. 
    The  default if to use f.list files (where 'f' is a filter in ugriz) and patches_f.txt, 
    and launch detectCoadSources in several batch jobs. You thus need to be running it at CC-IN2P3 
    to make it work. To run all  filters, you can do something like 
    %prog -f ugriz -m 1 -c detectCoaddSources.py -a"""

    opts, args = LR.standard_options(usage=usage, description=description)

    # overwrite some options
    opts.mod = 20
    opts.input = "_parent/output/coadd_dir"
    opts.output = "_parent/output/coadd_dir"
    file_patch = "patches_all.txt"

    cmd = "split -l " + str(opts.mod) + " -d " + file_patch + " " + file_patch + "_"
    os.system(cmd)
    patch_list = sorted(glob.glob(file_patch + "_*"))
    print patch_list

    for patch in sorted(patch_list):
        print "\n", patch
        # Only submit the job if asked
        cmd = build_cmd(patch, opts.configs, opts.input, opts.output)
        LR.submit(cmd, patch, None, autosubmit=opts.autosubmit, ct=1000, vmem='4G',
                  from_slac=opts.fromslac)
