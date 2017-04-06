#!/usr/bin/env python

"""
.. _rereun_locked:

Tools to run cluster analysis
=============================
"""

from glob import glob
from optparse import OptionParser

if __name__ == '__main__':
    
    parser = OptionParser()
    parser.add_option('-r', '--rerun', action='store_true', default=False,
                      help="If not set, only print what will be rerun")
    opts, args = parser.parse_args()

    rerun = []
    logs = glob("log/*/*.log")
    print "INFO: %i log files found" % len(logs)
    for log in sorted(logs):
        f = open(log)
        for l in f:
            if '.lockDir' in l:
              rerun.append(log)
              break
        f.close()
    print "INFO: %i logs will a .lockDir found" % len(rerun)
    for r in rerun:
        script = r.replace("log/", "script/").replace('.log', '.sh')
        print "Re-running:", script
        if opts.rerun:
            os.system(". %s" % script)
