from java.util import MashMap

def runscripts():
    import glob, os
    workdir = os.getenv("WORK_DIR")[0] + "/02-processccd/"
    scripts = glob.glob(workdir + "scripts/*/*.sh")
    for i, script in enumerate(scripts):
        print "%2d" % i, script
        vars = MashMap()
        vars.put("CUR_SCRIPT", script)
        pipeline.createSubstream("processFilter", i, vars)
