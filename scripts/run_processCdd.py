#!/usr/bin/env python

"""
.. _run_processCdd:

Run processCdd.py for a list of visits
======================================
"""

from __future__ import print_function
import os
import numpy as N
import libRun as LR


__author__ = 'Nicolas Chotard <nchotard@in2p3.fr>'
__version__ = '$Revision: 1.0 $'


def build_cmd(visits, config, filt, input='pardir/input', output='pardir/output'):

    if not os.path.isdir("scripts/" + filt):
        os.makedirs("scripts/" + filt)

    # Create and save a sub list of visit
    filename = "scripts/" + filt + "/" + "_".join(visits) + ".list"
    N.savetxt(filename, ["--id visit=%s ccd=0..35" % visit for visit in visits], fmt="%s")

    # Create the command line
    cmd = "processCcd.py %s --output %s @" % (input, output) + \
          filename + " --configfile " + config
    if opts.multicore:
        cmd += " -j 8 --timeout 999999999"
    print("\nCMD: ", cmd)

    return cmd

    
if __name__ == "__main__":

    usage = """%prog [option]"""

    description = """This script will run processCcd for a given list of filters and visits. The 
    default if to use f.list files (where 'f' is a filter in ugriz), and launch processCcd in 
    several batch jobs. You thus need to be running it at CC-IN2P3 to make it work. To run all 
    filters, you can do something like %prog -f ugriz -m 1 -c processConfig.py,processConfig_u.py -a
    """

    opts, args = LR.standard_options(usage=usage, description=description)

    # Loop over filters
    for filt in opts.filters:

        config = LR.select_config(opts.configs, filt)

        # Get the list of visits
        visits = [visit.split('=')[1].strip("'")
                  for visit in N.loadtxt(filt+".list", dtype='str', unpack=True)[1]]
        print("INFO: %i visits loaded: " % len(visits), visits)

        # How many jobs should we be running (and how many visit in each?)?
        opts.mod = 1  # one job per visit to be faster
        njobs = LR.job_number(visits, opts.mod, opts.max)

        # Reorganize the visit list in consequence
        visits = LR.organize_items(visits, njobs)

        # specific options for processCcd
        opts.ct = 259200
        opts.vmem = "32G"
        opts.queue = "huge"
        if opts.multicore:
            opts.queue = "mc_huge"
            opts.otheroptions = "-pe multicores 8"

        # Loop over the visit sub lists
        for i, vs in enumerate(visits):

            # Build the command line and other things
            cmd = build_cmd(vs, config, filt, opts.input, opts.output)

            # Only submit the job if asked
            prefix = "visit_%03d_script" % (i + 1)
            #prefix = "%i_" % (i + 1) + "_".join(vs)
            LR.submit(cmd, prefix, filt, autosubmit=opts.autosubmit,
                      ct=opts.ct, vmem=opts.vmem, queue=opts.queue,
                      system=opts.system, otheroptions=opts.otheroptions,
                      from_slac=opts.fromslac)

    if not opts.autosubmit:
        print("\nINFO: Use option --autosubmit to submit the jobs")
