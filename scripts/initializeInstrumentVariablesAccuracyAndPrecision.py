import io
import re
import pandas as pd
from gliderMetadataApp import models

# included all vars, but commented out ones that I haven't been able to find values for
# first is platformVariable
# second is accuracy
# third is precision
m = [['GPCTD_CONDUCTIVITY', 0.0003, ''],
     ['GPCTD_TEMPERATURE', 0.002, ''],
     # ['GPCTD_PRESSURE', '', ''],
     # ['GPCTD_DOF', '', ''],
     #['FLBBCD_CHL_COUNT', ''],
     # ['FLBBCD_CHL_SCALED', '', ''],
     #['FLBBCD_BB_700_COUNT', ''],
     # ['FLBBCD_BB_700_SCALED', '', ''],
     #['FLBBCD_CDOM_COUNT', '', ''],
     # ['FLBBCD_CDOM_SCALED', '', ''],
     #['MFLUV1_V1_COUNT', ''],
     #['MFLUV1_V2_COUNT', ''],
     #['MFLUV1_V3_COUNT', ''],
     #['MFLUV1_V4_COUNT', ''],
     #['MFLUV1_TMP', ''],
     #['MFLUV1_TRY_SCALED', ''],
     #['MFLUV1_PHE_SCALED', ''],
     #['MFLUV1_NAPH_SCALED', ''],
     ['AROD_FT_TEMP', 0.01, ''],
     ['AROD_FT_DO', 2.0, ''],
     #['PORPOISE_STATUS', ''],
     #['PORPOISE_EVTS', ''],
     #['PORPOISE_DISK_MOUNTED', ''],
     #['PORPOISE_DISKS_USAGE', ''],
     #['PORPOISE_DISKS_FULL', ''],
     #['PORPOISE_SAMPLING_STATUS', ''],
     #['PORPOISE_ACOUSTIC_RECORDING', '', ''],
     ['LEGATO_CONDUCTIVITY', 0.003, ''],
     ['LEGATO_TEMPERATURE', 0.002, ''],
     # ['LEGATO_PRESSURE', '', ''],
     # ['LEGATO_SALINITY', '', '']
     ]

for var in m:
    print(f"Getting variable {var[0]}")
    x = models.InstrumentVariable.objects.get(instrument_variableSourceName = var[0])
    if not (len(str(var[1])) == 0):
        print(f"Adding accuracy.")
        x.instrument_accuracy = var[1]
        x.save()
    if not (len(str(var[2])) == 0):
        print(f"Adding precision.")
        x.instrument_precision = var[2]
        x.save()