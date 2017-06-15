#!/usr/bin/env python

"""
.. _libRun:

Tools to run cluster analysis
=============================
"""

import os
import sys
import re
import time
import numpy as np
from optparse import OptionParser

__author__ = 'Nicolas Chotard <nchotard@in2p3.fr>'
__version__ = '$Revision: 1.0 $'

SCRIPTS = {1: 'processCcd',
           2: 'makeCoaddTempExp',
           3: 'assembleCoadd',
           4: 'detectCoaddSources',
           5: 'mergeCoaddDetections',
           6: 'measureCoaddSources',
           7: 'mergeCoaddMeasurements',
           8: 'forcedPhotCcd',
           9: 'forcedPhotCoadd'}

def build_cmd(script_number, items, config, filt, **kwargs):
    """
    Build the command line to run for a set of script:
     - 1. processCcd.py
     - 2. makeCoaddTempExp.py
     - 3. assembleCoadd.py
     - 4. detectCoaddSources.py
     - 5. mergeCoaddDetections.py
     - 6. measureCoaddSources.py
     - 7. mergeCoaddMeasurements.py
     - 8. forcedPhotCcd.py
     - 9. forcedPhotCoadd.py
    """
    script = SCRIPTS[script_number]

    # 1
    if script == 'processCcd':
        filename = "scripts/" + filt + "/" + items + ".list"        
        cmd = "processCcd.py pardir/input --output pardir/output @" + \
              filename + " --configfile " + config + " --clobber-config"
    # 2
    elif script == 'makeCoaddTempExp':
        filename = filt+'.list'
        cmd = "makeCoaddTempExp.py pardir/output --output pardir/output/coadd_dir " + items + " @" + filename + " --configfile " + config
    # 3
    elif script == 'assembleCoadd':
        # h_vmem=8G
        patchList, runList, configFile, filt
        prefix = makeFileName(patchList)
        cmd = "assembleCoadd.py pardir/output/coadd_dir " + patchList + " @" + runList + " --configfile " + configFile + " --clobber-config"
    # 4
    elif script == 'detectCoaddSources':
        print "WARNING: No implemented yet. Quit."
        sys.exit()
    # 5
    elif script == 'mergeCoaddDetections':
        print "WARNING: No implemented yet. Quit."
        sys.exit()
    # 6
    elif script == 'measureCoaddSources':
        print "WARNING: No implemented yet. Quit."
        sys.exit()
    # 7
    elif script == 'mergeCoaddMeasurements':
        print "WARNING: No implemented yet. Quit."
        sys.exit()
    # 8
    elif script == 'forcedPhotCcd':
        print "WARNING: No implemented yet. Quit."
        sys.exit()
    # 9
    elif script == 'forcedPhotCoadd':
        print "WARNING: No implemented yet. Quit."
        sys.exit()

    print "\nCMD: ", cmd
    return cmd

def makeFileName(patchList) :
    s = re.split('--', patchList)
    name = ""
    for i in range(1,len(s)) :
        field = []
        t = re.split(" ", s[i])
        for j in range(1,4) :
            field.append(re.split("=",t[j])[1])
        if i > 1 :
            name = name + "_"
        name = name + field[0] + "_" + field[1] + "_" + field[2]
    return name.replace(",","-")
    
def submit(cmd, prefix, config, filt, autosubmit=False, ct=60000, vmem='4G'):
    """
    cmd: command line to run
    prefix: used for the .log and .sh file names
    config: name of the config file, which must be in the local directory
    filt: name of the current filter
    autosubmit: if True, the job will be created and submited automatically
    """
    if not os.path.isdir("scripts/" + filt):
        os.makedirs("scripts/" + filt)
    cwd = os.getcwd()
    dirLog = cwd + "/log/" + filt
    if not os.path.isdir(dirLog):
        os.makedirs(dirLog)
    log = dirLog + "/" + prefix + ".log"
    print "LOG: ", log
    qsub = "qsub -P P_lsst -l sps=1,ct=%i,h_vmem=%s -j y -o " % (ct, vmem) \
                                   + log + " <<EOF"
    scriptname = "scripts/" + filt + "/" + prefix + ".sh"
    script = open(scriptname, "w")
    script.write(qsub + "\n")
    script.write("#!/usr/local/bin/bash\n")
    script.write(" cd " + cwd + "\n")
    script.write(" source pardir/setup.sh\n")
    script.write(" " + cmd + "\n")
    script.write("EOF" + "\n")
    script.close()
    os.system("chmod +x " + scriptname)
    if opts.autosubmit:
        os.system("./"+scriptname)
        time.sleep(1)

def job_number(items, max_item, max_job):
    """
    How many jobs should we be running (and how many items in each?)?
    """
    assert max_item > 0, "max_item must be > 0"
    assert max_job > 1, "max_job must be > 0"
    njobs = int(np.ceil(float(len(items))/max_item))
    if njobs > max_job:
        print "WARNING: number of jobs exceed the maximum. More items will be put in each job."
        njobs = max_job
    return njobs

def organize_items(items, njobs):
    items = np.array_split(sorted(items), njobs)
    print "INFO: Items sub-divided as followed in %i jobs:" % njobs
    for it in items:
        print " -", "_".join(np.array(it, dtype='string'))
    return items     
        
if __name__ == "__main__":

    filters = "ugriz"
    
    usage = """%prog [option]\n"""
    usage += """\n To run all filters, you can do something like"""
    usage += """\n%prog -s script_number -f ugriz -m 1 -c processConfig.py,processConfig_u.py -a\n Possible scripts_number are:"""
    for s in sorted(SCRIPTS):
        usage += "\n - %s: %s" % (s, SCRIPTS[s])
    
    description = """This script will run one of the script for a given list of filters. The 
    default if to use f.list files (where 'f' is a filter in ugriz), and launch processCcd in 
    several batch jobs. You thus need to be running it at CC-IN2P3 to make it work."""
    
    parser = OptionParser(description=description, usage=usage)
    parser.add_option("-s", "--script", type="int", default=None,
                      help="Script number. Can be any number corresponding to a script from the list "
                      "shown above.")
    parser.add_option("-f", "--filters", type="string", default="ugriz",
                      help="Filter(s) [%default]. Can also be a ist of filter ('ugriz')")
    parser.add_option("-c", "--configs", type="string", default="processConfig.py",
                      help="Configuration file [%default]. Several files (and filters with option -f) "
                      "can be given if a filter needs its own config file. In that case, include"
                      " '_f' in the name of the file. e.g.: processConfig.py,processConfig_u.py if you"
                      " want the 'u' filter to use a different configuration file. The default config"
                      " must be the first one.")
    parser.add_option("-m", "--mod", type="int", default=4,
                      help="Nbr. of visits per job [%default]")
    parser.add_option("-M", "--max", type="int", default=999,
                      help="Max nbr of jobs to be submitted [%default]")
    parser.add_option("-a", "--autosubmit", action='store_true', default=False,
                      help="Submit the jobs automatically")
    opts, args = parser.parse_args()
    
    if opts.script not in SCRIPTS:
        raise IOError("option script must be used and must be a number from the lsit of script (-h)")
    print "\nINFO: Selected script (%s) will be run" % SCRIPTS[opts.script]

    print "INFO: We will run of the following filter(s)", opts.filters
    configs = opts.configs.split(',')
    
    # Check the input filter
    for filt in opts.filters:
        if filt not in filters:
            print "Unknown filter: " + filt
            continue

        # look for a specific config file
        if "_"+filt+".py" in opts.configs:                
            config = [c for c in configs if "_"+filt in c][0]
        else:
            config = configs[0] # default configuration file is the first of the list            

        if scripts_number in [1]: # work on visits
            # Get the list of visits
            visits = [v.split('=')[1] for v in np.loadtxt(filt+".list",
                                                          dtype='string', unpack=True)[1]]
            print "INFO: %i visits loaded: " % len(visits), visits
            
            # Get the number of jobs
            njobs = job_number(visits, opts.mod, opts.max)
        
            # Reorganize the list of items (visits, patches) in consequence
            visits = organize_items(visits, njobs)
        elif script_number in [2]: # work on patches
            # Get the list of patches
            patches = np.loadtxt("patches_"+filt+".txt", dtype='string')
            print "INFO: %i patches loaded" % len(patches)
            
            # Get the number of jobs
            njobs = job_number(visits, 1, opts.max)
        
            # Reorganize the list of items (visits, patches) in consequence
            visits = organize_items(patches, njobs)
            
        
        # Loop over the visit sub lists
        for it in items:
            if scripts_number in [1]:
                # This is what we will write in the sub list file
                sub_items = ["--id visit=%s ccd=0..35" % i for i in it]
                np.savetxt(sub_visit, filename)
                kwargs = {'filename': }

            # Only submit if asked, and only create the list and .sh file otherwise
            items = "_".join(vs)
            cmd = build_cmd(opts.script, items, config, filt, **kwargs)
            prefix = items
            submit(cmd, prefix, config, filt, autosubmit=False)
            #submit("_".join(vs), towrite, config, filt, opts)
        
        if not opts.autosubmit:
            print "\nINFO: Use option --autosubmit to submit the jobs"
        
