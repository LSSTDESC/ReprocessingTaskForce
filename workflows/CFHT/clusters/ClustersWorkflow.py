def runscripts():
    import glob, os
    workdir = os.getenv("WORK_DIR")[0] + "/02-processccd/"
    files = glob.glob(workdir + "scripts/*/*.sh")
    for f in files:
        pipeline.createSubstream("processFilter"; f)
