from spacepy import pycdf
import json
from sys import argv
import persistcdf as pcdf
from ecef2plh import *
from time import time

db = pcdf.Database('base.db')

for cdfname in argv[1:]:
    try:
        cdf = pycdf.CDF(cdfname)
    except pycdf.CDFError:
        print "ERROR: no se pudo abrir el archivo " + cdfname
        print "    Probando con el siguiente..."
        continue
    print "INFO: Procesando el archivo " + cdfname

    t_ini = time()
    count = cdf['Epoch'].shape[0]

    #f = open('output.json','w')
    if "FEDO_Energy" in cdf.keys():
        fedo_descs = []
        for j in xrange(len(cdf['FEDO_Energy'][...])):
            fd = pcdf.FEDODesc()
            fd.energy= cdf['FEDO_Energy'][j].item()
            fd.label = cdf['FEDO_LABL_1'][j].item()
            fd.crosscalib = cdf['FEDO_Crosscalib'][j].item()
            fedo_descs.append(fd)

        db.session.add_all(fedo_descs)
        db.session.commit()

    feio_descs = []
    for j in xrange(len(cdf['FEIO_Energy'][...])):
        fd = pcdf.FEIODesc()
        fd.energy= cdf['FEIO_Energy'][j].item()
        fd.label = cdf['FEIO_LABL_1'][j].item()
        fd.crosscalib = cdf['FEIO_Crosscalib'][j].item()
        feio_descs.append(fd)

    db.session.add_all(feio_descs)
    db.session.commit()

    fpdo_descs = []
    for j in xrange(len(cdf['FPDO_Energy'][...])):
        fd = pcdf.FPDODesc()
        fd.energy= cdf['FPDO_Energy'][j].item()
        fd.label = cdf['FPDO_LABL_1'][j].item()
        fd.crosscalib = cdf['FPDO_Crosscalib'][j].item()
        fpdo_descs.append(fd)

    db.session.add_all(fpdo_descs)
    db.session.commit()

    fpio_descs = []
    for j in xrange(len(cdf['FPIO_Energy'][...])):
        fd = pcdf.FPIODesc()
        fd.energy= cdf['FPIO_Energy'][j].item()
        fd.label = cdf['FPIO_LABL_1'][j].item()
        fd.crosscalib = cdf['FPIO_Crosscalib'][j].item()
        fpio_descs.append(fd)

    db.session.add_all(fpio_descs)
    db.session.commit()

    for i in xrange(count):
        e = pcdf.Epoch()
        e.epoch = cdf['Epoch'][i]
        e.alpha = cdf['Alpha'][i]
        e.alpha_eq = cdf['Alpha_Eq'][i]
        e.b_calc = cdf['B_Calc'][i]
        e.b_eq = cdf['B_Eq'][i]
        e.i = cdf['I'][i]
        e.l = cdf['L'][i]
        e.l_star = cdf['L_star'][i]
        e.mtl = cdf['MLT'][i]
        e.pos_quality = cdf['Position_Quality'][i]
        e.pos_x = cdf['Position'][i][0].item()
        e.pos_y = cdf['Position'][i][1].item()
        e.pos_z = cdf['Position'][i][2].item()
        e.pos_lat, e.pos_lon, e.pos_alt = ecef2geodetic(cdf['Position'][i][0].item(),
                                                        cdf['Position'][i][1].item(),
                                                        cdf['Position'][i][2].item())

        db.session.add(e)
    #    db.session.commit()

        if "FEDO" in cdf.keys():
            for j in xrange(len(cdf['FEDO_Energy'][...])):
                fd = pcdf.FEDO()
                fd.fedo = cdf['FEDO'][i][j].item()
                fd.fedo_quality = cdf['FEDO_Quality'][i][j].item()
                fd.desc = fedo_descs[j]
                fd.epoch = e
                db.session.add(fd)

        for j in xrange(len(cdf['FEIO_Energy'][...])):
            fd = pcdf.FEIO()
            fd.feio = cdf['FEIO'][i][j].item()
            fd.feio_quality = cdf['FEIO_Quality'][i][j].item()
            fd.desc = feio_descs[j]
            fd.epoch = e
            db.session.add(fd)

        for j in xrange(len(cdf['FPDO_Energy'][...])):
            fd = pcdf.FPDO()
            fd.fpdo = cdf['FPDO'][i][j].item()
            fd.fpdo_quality = cdf['FPDO_Quality'][i][j].item()
            fd.desc = fpdo_descs[j]
            fd.epoch = e
            db.session.add(fd)

        for j in xrange(len(cdf['FPIO_Energy'][...])):
            fd = pcdf.FPIO()
            fd.fpio = cdf['FPIO'][i][j].item()
            fd.fpio_quality = cdf['FPIO_Quality'][i][j].item()
            fd.desc = fpio_descs[j]
            fd.epoch = e
            db.session.add(fd)

        if i % 100 == 0:
            db.session.commit()
            print "INFO: procesando " + cdfname

    db.session.commit()
    t_end = time()
    print "INFO: Archivo [" + cdfname + "] procesado en : " + str(int((t_end - t_ini)/60.0)) +":"+ str(int((t_end - t_ini)%60.0)) + " minutos."
