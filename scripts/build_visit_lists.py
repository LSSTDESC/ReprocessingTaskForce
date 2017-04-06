#!/usr/bin/env python

"""
.. _build_visit_lists:

Build the list of visit for a given cluster
===========================================
"""

import os
import glob
from optparse import OptionParser

__author__ = 'Nicolas Chotard <nchotard@in2p3.fr>'
__version__ = '$Revision: 1.0 $'

RERUN = []

def read_log(log):
    complete_log = False
    f = open(log, 'r')
    d = {}
    for l in f:
        if l.startswith("processCcd: Processing"):
            sd = eval(l.split("processCcd: Processing ")[1])
            if sd['visit'] not in d:
                d[sd['visit']] = {}
            d[sd['visit']][sd['ccd']] = sd
        if l.startswith("processCcd.calibrate.astrometry: Matched and fit WCS"):
            ll=l.split()
            ast={'iterations': ll[6], 'matches': ll[9],
                'scatter': ll[14], 'scatter_sgm': ll[16], 'unit': ll[17]}
            d[sd['visit']][sd['ccd']].update(ast)
            if float(ast['scatter']) == 0:
                print "WARNING: WSC scatter is 0 for visit %s, ccd %s" % (sd['visit'], sd['ccd'])
        elif l.startswith("processCcd.calibrate.astrometry: Astrometric scatter"):
            ll=l.split()
            ast={'matches': ll[8], 'scatter': ll[3], 'unit': ll[4], 'rejected': ll[10]}
            d[sd['visit']][sd['ccd']].update(ast)
        if l.startswith("*   maxvmem:"):
            complete_log = True
    f.close()
    if not complete_log:
        print "WARNING: The following log is not complete:", log
        RERUN.append(". %s" % log.replace("log/", "scripts/").replace('.log', '.sh'))
    return d

def get_logs(logs):
    loglist = []
    for l in logs.split(','):
        loglist.extend(glob.glob(l))
    print "INFO: %i logs loaded" % len(loglist)
    d = {}
    for i, log in enumerate(loglist):
        ld = read_log(log)
        for v in ld:
            if v in d:
                d[v].update(ld[v])
            else:
                d[v] = ld[v]
    return d

def create_list(f, d, r):
    ff = open("%s.list" % f, 'w')
    for v in sorted(d[f]):
        ccd = "^".join(str(i) for i in range(36) if i not in r[f][v])
        ff.write("--selectId visit=%i ccd=%s\n" % (v, ccd))
    ff.close()

if __name__ == "__main__":

    description = "Build the list of visit for a given cluster for all available filters"
    usage = """usage: %prog [options] datadir

    datadir: absolute path to the directory containing the calibrated data (.fits.fz)"""

    parser = OptionParser(usage=usage, description=description)
    parser.add_option("-i", "--input", help="Directory conting the input fits files.")
    parser.add_option("--idopt", help="id option to put in fron of the visit "
                      "name. Could be 'selectId' or 'id' [%default]",
                      default='id', type='string')
    parser.add_option("-l", "--logs", type="string", help="Logs select ccd (coma separated for "
                      "several logs, or \*.log for multiple log in the same dir.")
    parser.add_option("-r", "--scatter_range", type="string", default="0.02,0.1",
                      help="Astrometric scatter range in which a ccd has to be [%default]")
    parser.add_option("-x", "--exclude", type="string",
                      help="List of visit/ccd to exclude. Format is the same as in the output file"
                      ", e.g visit=850760 ccd=11^16")
    options, args = parser.parse_args()

    if options.input is None:
        raise IOError("Please use the input option")
    if not os.path.exists(options.input):
        raise IOError("Input directory does not exists")
    if not options.input.endswith('/'):
        options.input += '/'
    if options.idopt not in ['selectId', 'id']:
        raise IOError("Option idopt must be 'selectid' or 'id'")
    
    fits = glob.glob(options.input+'raw/*/*/*/*/*.fz')
    if len(fits) == 0:
        raise IOError("No fits file found while lokking for %s/raw/*/*/*/*/*.fz" % options.input)
    else:
        print "INFO: %i visists found" % len(fits)
    filters = set([f.split('/')[-2] for f in fits])
    visits = [f.split('/')[-1].split('p.fits.fz')[0] for f in fits]
    f_visits = {f: [v for i, v in enumerate(visits) if '/'+f+'/' in fits[i]]
                for f in filters}
    print "INFO: %i filters found" % len(f_visits)

    # Do we select CCD based on the astrometric scatter?
    if options.logs is not None:
        ii = 0
        min_scatter, max_scatter = map(float, options.scatter_range.split(','))
        logs = get_logs(options.logs) # Read the logs, get the data
        d = {f: {} for f in filters} # orgize the visit per filter
        for v in logs:
            f = logs[v][logs[v].keys()[0]]['filter']
            d[f][v] = logs[v]
        rejected = {f: {int(v): [] for v in f_visits[f]} for f in filters}
        for f in filters:
            for v in sorted(d[f]):
                for ccd in sorted(d[f][v]):
                    if 'scatter' in d[f][v][ccd]:
                        scatter = float(d[f][v][ccd]['scatter'])
                        if scatter < min_scatter or scatter > max_scatter:
                            print "Scatter < %.2f or > %.2f for " % (min_scatter, max_scatter), \
                                f, v, ccd, scatter
                            rejected[f][v].append(int(ccd))
                    else:
                        print "No astrometric scatter (processCcd crashed) for", f, v, ccd
                        rejected[f][v].append(int(ccd))
                        ii += 1
            print sum([len(rejected[f][v]) for v in rejected[f]]), \
                "/ %i CCDs rejected for filter %s (actually %i ccds)\n" % \
                (sum([36*len(d[f])]), f, sum([len(d[f][v]) for v in d[f]]))

    # Do we have an input exlcude list?
    exclude = {v: [] for f in f_visits for v in f_visits[f]}
    if options.exclude is not None:
        el = N.loadtxt(options.exclude, dtype='str', unpack=True)
        for v, ccds in zip(el[0], el[1]):
            exclude[v.split('=')[1]] = ccds.split('=')[1].split('^')
            
    # Write and save the list, including the ccd selection if needed
    for f in f_visits:
        vf = "%s.list" % f
        ff = open(vf, 'w')
        for v in f_visits[f]:
            ccd = "^".join(str(i) for i in range(36) if i not in rejected[f][int(v)]
                           and str(i) not in exclude[v])
            if len(ccd):
                ff.write("--%s visit=%s ccd=%s\n" % (options.idopt, v, ccd))
            else:
                ff.write("--%s visit=%s\n" % (options.idopt, v))
        ff.close()
        print " - %s: %i visits -> %s" %(f, len(f_visits[f]), vf)
