from java.util import HashMap

def runscripts():
    import glob, os
    scripts = glob.glob(WORK_DIR + "/02-processccd/scripts/*/*.sh")
    if not len(scripts):
        raise("ERROR: no file found")
    else:
        raise("GREAT: %i file found" % len(scripts))
    for i, script in enumerate(scripts):
        print "%2d" % i, script
        vars = MashMap()
        vars.put("CUR_SCRIPT", script)
        pipeline.createSubstream("processFilter", i, vars)
