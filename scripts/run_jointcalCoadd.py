#!/usr/bin/env python

import numpy as N
import libRun as LR

def build_cmd(patches, config, filt, input, output):
    cmd = "jointcalCoadd.py %s --output %s " % (input, output) + " @"  + patches + " @" + \
          filt + ".list" + " --configfile " + config + " --doraise"
    print "\nCMD:", cmd
    return cmd

if __name__ == "__main__":

    filters = "ugriz"

    usage = """%prog [option]"""

    description = """Run jointcalCoadd.py for a given list of filters and patches."""

    opts, args = LR.standard_options(usage=usage, description=description, filters=filters)

    # overwrite the -m option to force it to be 5
    opts.mod = 5

    # Loop over filters
    for filt in opts.filters:

        config = LR.select_config(opts.configs, filt)

        # Get the list of patches

        # default options
        opts.input = "pardir/output"
        opts.output = "pardir/output"

        # Build the command line and other things
        cmd = build_cmd("patches_" + filt + ".txt", config, filt, opts.input, opts.output)

        # Only submit the job if asked
        prefix = "patches_%s_script" % filt
        LR.submit(cmd, prefix, filt, autosubmit=opts.autosubmit, queue=opts.queue,
                  ct=6000, vmem=opts.vmem, system=opts.system, from_slac=opts.fromslac)

    if not opts.autosubmit:
        print "\nINFO: Use option --autosubmit to submit the jobs"

