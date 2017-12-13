#!/usr/bin/env python

"""
.. _cacd_query:

Tools to run cluster analysis
=============================
"""


from __future__ import print_function
import os
import warnings
from io import StringIO
from optparse import OptionParser
from astroquery.ned import Ned
from astropy.io import votable
from astropy.table import Table
from datetime import datetime
import requests


def cfht_megacam_tap_query(ra_deg=180.0, dec_deg=0.0, radius=0.01666666):
    """Do a query of the CADC Megacam table.
    Get all observations inside a radius around a target
    @rtype : Table
    @param ra_deg: center of search region, in degrees
    @param dec_deg: center of search region in degrees
    @param radius: : radisu in degree, from the center
    """

    query = ("SELECT "
             "COORD1(CENTROID(Plane.position_bounds)) AS RAJ2000,"
             "COORD2(CENTROID(Plane.position_bounds)) AS DEJ2000,"
             "Plane.productID AS ProductID,"
             "target_name "
             "FROM "
             "caom2.Observation as o "
             "JOIN caom2.Plane as Plane on o.obsID=Plane.obsID "
             "WHERE o.collection = 'CFHT' "
             "AND Plane.dataProductType = 'image' "
             "AND Plane.calibrationLevel = '2' "
             "AND Plane.energy_emBand = 'Optical' "
             "AND Plane.time_exposure >= '180' "
             "AND o.instrument_name = 'MegaPrime' "
             "AND o.type = 'OBJECT' "
             "AND INTERSECTS( CIRCLE('ICRS', %f, %f, %f), Plane.position_bounds ) = 1 "
             "AND ( Plane.quality_flag IS NULL OR Plane.quality_flag != 'junk' ) ")

    query = query % (ra_deg, dec_deg, radius)
    query += "AND Plane.dataRelease <= '%s' " % datetime.now().isoformat().split("T")[0]
    query += "AND Plane.energy_bandpassName LIKE '_.MP%' "
    data = {"QUERY": query,
            "REQUEST": "doQuery",
            "LANG": "ADQL",
            "FORMAT": "votable"}

    lurl = "http://www.cadc.hia.nrc.gc.ca/tap/sync"

    warnings.simplefilter('ignore')
    ff = StringIO(requests.get(lurl, params=data).content)
    ff.seek(0)
    return votable.parse(ff).get_first_table().to_table()


if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option('-T', '--target', type='string', help="Target name")
    parser.add_option('-P', '--paper', type='string', help="Paper reference")
    parser.add_option('--ra', type=float,
                      help="RA (in degrees) of the centre of the search area.")
    parser.add_option('--dec', type=float,
                      help="DEC (in degrees) of the centre of the search area.")
    parser.add_option('--radius', type=float, default=0.4,
                      help="radius (in degrees) of the search area. [%default-")
    parser.add_option('-o', '--output', type='string', default='cadcUrlList.txt',
                      help="Name of the output file which will contain the list"
                      " of fits to download [%default]")
    parser.add_option('-d', '--dir', type='string', default=None,
                      help="Directory where data will be downloaded. Default is target name.")
    parser.add_option('-D', '--download', action='store_true', default=False,
                      help="Automatic download of the fits files found (could take a while...)")

    opts, args = parser.parse_args()

    if opts.target is not None:
        print("INFO: Target is", opts.target)
        obj = Ned.query_object(opts.target)
        ras, decs = [obj['RA(deg)'].item()], [obj['DEC(deg)'].item()]
        objs = [opts.target]
    elif opts.paper is not None:
        print("INFO: look for all target in paper: %s" % opts.paper)
        objects = Ned.query_refcode(opts.paper) # for WTGI : 2014MNRAS.439....2V
        ras = objects['RA(deg)']
        decs = objects['DEC(deg)']
        objs = [obj.replace(" ", "") for obj in objects['Object Name']]
        print("INFO: %i targets found" % len(objs))
    elif opts.ra is None or opts.dec is None:
        raise IOError("You must give a target name (--target) or its coordinates (--ra, --dec)")

    for obj, ra, dec in zip(objs, ras, decs):
        table = cfht_megacam_tap_query(ra, dec, opts.radius)
        assert isinstance(table, Table)
        if not len(table):
            print("WARNING: No data for\n", obj)
            continue
        print("INFO: Target info")
        print(" - Name: ", obj)
        print(" - RA (deg):", ra)
        print(" - DEC (deg):", dec)
        print("INFO: Found %i files" % len(table))
        webpath = 'http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/data/pub/CFHT/'

        urls = [webpath+pid for pid in table['ProductID']]

        if opts.dir is None:
            if not os.path.exists(obj):
                os.mkdir(obj)
            opts.dir = obj
        else:
            if not os.path.exists(opts.dir):
                os.mkdir(opts.dir)
        os.chdir(opts.dir)

        outfile = open(opts.output, 'w')
        for pid in urls[::-1]:
            outfile.write("%s\n" % pid)
        outfile.close()
        print("INFO: list of files saved in %s/%s" % (obj, opts.output))
        if not opts.download:
            print("Run the follwing command to download them:")
            print("\n   wget --content-disposition -N -i %s\n" % opts.output)
        else:
            try:
                import wget
                wget = wget.download
            except:
                print("WARNING: Install the 'wget' package (will use the wget system for now)")
                wget = lambda url: os.system("wget -N %s" % url)
            for url in urls:
                print("\nDownloading", url)
                wget(url)
                os.rename(url.split('/')[-1], url.split('/')[-1] + '.fits.fz')
        if opts.dir not in [None, '.', './']:
            os.chdir("..")
