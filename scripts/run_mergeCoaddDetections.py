#!/usr/bin/env python

import os
import time
import re
import glob
from optparse import OptionParser
import libRun as LR

def build_cmd(patch, configFile, input, output):

    if not os.path.isdir("scripts") :
        os.makedirs("scripts")
        
    cmd = "mv "+ patch + " scripts"
    os.system(cmd)

    cmd = "mergeCoaddDetections.py %s --output %s"  % (input, output) + \
          " @scripts/" + patch + " --configfile " + configFile + " --clobber-config --clobber-versions"
    print cmd

    return cmd

def submit(cmd, patch, autosubmit=False):

    if not os.path.isdir("scripts") :
        os.makedirs("scripts")

        
    cwd = os.getcwd()
    
    dirLog = cwd + "/log"
    if not os.path.isdir(dirLog) :
        os.makedirs(dirLog)
    log = dirLog + "/" + patch + ".log"
 
    qsub = "qsub -P P_lsst -l sps=1,ct=60000,h_vmem=4G -j y -o "+ log + " <<EOF"
    scriptName = "scripts/" + patch + ".sh"
    script = open(scriptName,"w")
    script.write(qsub + "\n")
    script.write("#!/usr/local/bin/bash\n")
    script.write(" cd " + cwd + "\n")
    script.write(" source _parent/setup.sh\n")
    script.write(" " + cmd + "\n")
    script.write("EOF" + "\n")
    script.close()
    os.system("chmod +x " + scriptName)

    if autosubmit:
        os.system("./"+scriptName)        
        time.sleep(0.2)

if __name__ == "__main__":
    filters = "ugriz"
    
    usage = """%prog [option]"""
    
    description = """This script will run mergeCoaddDetections for a given list of filters and patches. 
    The  default if to use f.list files (where 'f' is a filter in ugriz) and patches_f.txt, 
    and launch detectCoadSources in several batch jobs. You thus need to be running it at CC-IN2P3 
    to make it work. To run all  filters, you can do something like 
    %prog -f ugriz -m 1 -c detectCoaddSources.py -a"""

    opts, args = LR.standard_options(usage=usage, description=description, filters=filters)

    configFile = opts.configs

    filePatch = "patches.txt"

    modularity = opts.mod
    maxPatch = opts.max 
    print modularity
    cmd = "split -l " + str(modularity) + " -d " + filePatch + " _" + filePatch
    print cmd
    os.system(cmd)
    
    patchList = glob.glob("_patches*")
    
    for patch in sorted(patchList):
        print "\n", patch
        cmd = build_cmd(patch, configFile, opts.input, opts.output)
        submit(cmd, patch, autosubmit=opts.autosubmit)
