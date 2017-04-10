#!/usr/bin/env python

"""
.. _get_astrometry:

Get needed astrometry data
==========================
"""

import pyfits
import subprocess
import re
import glob
import os
import numpy as N
from optparse import OptionParser

__author__ = 'Nicolas Chotard <nchotard@in2p3.fr>'
__version__ = '$Revision: 1.0 $'

if __name__ == "__main__":

    description = "Get the astrometry catalogue from a list of exposures"
    usage = """usage: %prog [options] datadir

    datadir: absolute path to the directory containing the calibrated data (.fits.fz)"""

    parser = OptionParser(usage=usage, description=description)
    parser.add_option("-r", "--radius", dest="radius",
                      help="Radius in degree givne to the search-index program [%default]",
                      default=0.14)
    parser.add_option("--astromdir", default='/sps/lsst/data/astrometry_net_data/sdss-dr9/',
                      help="Absolute path to an astrometry data catalogue")
    parser.add_option("--config", default='andConfig.py',
                      help="Name of the config file that will be created")
    parser.add_option("--setup", action='store_true', default=False,
                      help="Use this option to automatically declare the package to eups and run"
                      "the setup")
    
    options, args = parser.parse_args()
    
    if len(args) != 1 or not(os.path.exists(args[0])):
        raise IOError("Program argument must be the absolute path pointing to the calibrated data")
    if not options.astromdir.endswith('/'):
        options.astromdir += '/'
    if not len(glob.glob(options.astromdir + '*.fits')):
        raise IOError("No fits file found in the given astrometry directory")
        
    datadir = args[0]
    
    
    # Get the list of input files
    fits_files = glob.glob(datadir + '*.fits.fz')
    
    # Loop on the file to get their corresponding astrometry reference file
    healpixes, ras, decs = [], [], []
    print " %16s %11s %10s %8s" % ("Name", "RA", "DEC", "HEALPIX")
    for i, f in enumerate(fits_files):
    
        # Open the fits file to get the coordinates
        ff = pyfits.open(f)
        ra, dec = ff[0].header['RA_DEG'], ff[0].header['DEC_DEG']
        # Run get-healpix to get the corresponding ID file in the SDSS DR9 catalog
        out=subprocess.check_output('get-healpix -N8 %f -- %f' % (ra, dec),
                                    shell=True)
        r = re.search("Healpix=\d*", out)
        healpix = r.group().split('=')[1]
        print " %16s %11f %10f %8s  %3i/%i" % (f.split('/')[-1], ra, dec,
                                               healpix, i+1, len(fits_files))
        healpixes.append(healpix)
        ras.append(ra)
        decs.append(dec)
        
    print "INFO: %i reference numbers found:" % len(set(healpixes)), \
        ','.join(sorted(set(healpixes)))
    
    # Get the corresponding absloute path (at CC in2p3)
    astrometry = []
    for hp in set(healpixes):
        astrometry.extend(glob.glob(options.astromdir + '*_%i_*.fits' % int(hp)))
    print "\n%i astrometry reference files found:" % len(set(astrometry))
    for af in sorted(astrometry):
        print " - %s" % af
    
    # Copy them localy
    print "\nINFO: Copying the files locally"
    for af in astrometry:
        print " cp %s ." % af
        subprocess.call("cp -f %s ." % af, shell=True)
    
    # Check if there are reference stars
    astrometry = glob.glob("*.fits")
    print "\nInfo: Number os stars found in eahc reference"
    fastrometry = []
    for af in astrometry:
        out = subprocess.check_output('search-index -r %f -d %f -R %f %s' % \
                                      (N.mean(ras), N.mean(decs), options.radius, af),
                                      shell=True)
        r = re.search("Found \d* stars", out)
        nstars = r.group().split()[1]
        if int(nstars) != 0:
            print " - %30s: %3i - OK" % (af, int(nstars))
            fastrometry.append(af)
        else:
            print " - %30s: %3i - Removed from list of reference" % (af, int(nstars))
        
        
    # Create the config file using the list of astrometry files
    f = open(options.config, 'w')
    f.write('filters = "ugriz"\n')
    f.write('root.magColumnMap = dict([(f,f) for f in filters])\n')
    f.write('root.magErrorColumnMap = dict([(f, f + "_err") for f in filters])\n')
    f.write('root.indexFiles = [%s]'%', '.join(['"%s"' % af for af in fastrometry]))
    f.close()
    print "\nINFO: Config file saved in %s, and contains %i astrometry files" % \
        (options.config, len(fastrometry))
    
    # Print some info on what to do next (or do it) to declare the package in eups and run the setup
    declare = "eups declare -m none -r . astrometry_net_data CLUSTERNAME"
    setup = "setup astrometry_net_data CLUSTERNAME"
    if options.setup:
        print "\nINFO: Running '%s'"
        subprocess.call(declare, shell=True)
        print "INFO: Running '%s'"
        subprocess.call(setup, shell=True)
    else:
        print "\nINFO: You should now run (change the user name is needed)"
        print "       $ %s" % declare
        print "       $ %s" % setup

