#!/usr/bin/env python

"""
.. _run_processCdd:

Run processCdd.py for a list of visits
======================================
"""

import libRun as LR

__author__ = 'Nicolas Chotard <nchotard@in2p3.fr>'
__version__ = '$Revision: 1.0 $'

if __name__ == "__main__":

    filters = "ugriz"

    usage = """%prog [option]"""

    description = """Run jointcal for a given list of filters"""

    opts, args = LR.standard_options(usage=usage, description=description, filters=filters)

    input = "_parent/output"
    output = "_parent/output/coadd_dir"
    config = "jointcalConfig.py"

    # Loop over filters
    for filt in opts.filters:
        cmd = "jointcal.py %s --output %s @%s.list --configfile %s" % \
              (input, output, filt, config)
        # Only submit the job if asked
        prefix = "jointcal_%s" % filt
        LR.submit(cmd, prefix, filt, autosubmit=opts.autosubmit,
                  ct=opts.ct, vmem=opts.vmem, queue=opts.queue,
                  system=opts.system, otheroptions=opts.otheroptions,
                  from_slac=opts.fromslac)

    if not opts.autosubmit:
        print "\nINFO: Use option --autosubmit to submit the jobs"
