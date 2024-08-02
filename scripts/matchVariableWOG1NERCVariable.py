import io
import re
import pandas as pd
from gliderMetadataApp import models

# included all vars, but commented out ones that don't have a match
# first is platformVariable
# second is NERC
# third is CF
m = [['GPCTD_CONDUCTIVITY', 'CNDC', 'sea_water_electrical_conductivity'],
     ['GPCTD_TEMPERATURE', 'TEMP', 'sea_water_temperature'],
     ['GPCTD_PRESSURE', 'PRES', 'sea_water_pressure'],
     ['GPCTD_DOF', 'FREQUENCY_DOXY', ''],
     #['FLBBCD_CHL_COUNT', ''],
     ['FLBBCD_CHL_SCALED', 'FLUORESCENCE_CHLA', 'concentration_of_chlorophyll_in_sea_water'],
     #['FLBBCD_BB_700_COUNT', ''],
     ['FLBBCD_BB_700_SCALED', 'BBP700', ''],
     #['FLBBCD_CDOM_COUNT', '', ''],
     ['FLBBCD_CDOM_SCALED', 'CDOM', ''],
     #['MFLUV1_V1_COUNT', ''],
     #['MFLUV1_V2_COUNT', ''],
     #['MFLUV1_V3_COUNT', ''],
     #['MFLUV1_V4_COUNT', ''],
     #['MFLUV1_TMP', ''],
     #['MFLUV1_TRY_SCALED', ''],
     #['MFLUV1_PHE_SCALED', ''],
     #['MFLUV1_NAPH_SCALED', ''],
     ['AROD_FT_TEMP', 'TEMP_DOXY', 'temperature_of_sensor_for_oxygen_in_sea_water'],
     ['AROD_FT_DO', 'DOXY', 'mole_concentration_of_dissolved_molecular_oxygen_in_sea_water'],
     #['PORPOISE_STATUS', ''],
     #['PORPOISE_EVTS', ''],
     #['PORPOISE_DISK_MOUNTED', ''],
     #['PORPOISE_DISKS_USAGE', ''],
     #['PORPOISE_DISKS_FULL', ''],
     #['PORPOISE_SAMPLING_STATUS', ''],
     #['PORPOISE_ACOUSTIC_RECORDING', '', ''],
     ['LEGATO_CONDUCTIVITY', 'CNDC', 'sea_water_electrical_conductivity'],
     ['LEGATO_TEMPERATURE', 'TEMP', 'sea_water_temperature'],
     ['LEGATO_PRESSURE', 'PRES', 'sea_water_pressure'],
     ['LEGATO_SALINITY', 'PSAL', 'sea_water_salinity']
     ]

for var in m:
    x = models.InstrumentVariable.objects.get(instrument_variableSourceName = var[0])
    if not (len(var[1]) == 0):
        y = models.VariableNERCStandard.objects.get(variable_nerc_variableName=var[1])
        if not y is None:
            x.instrument_nercVariable = y
            x.save()
    if not (len(var[2]) == 0):
        z = models.VariableCFStandard.objects.get(variable_standardName=var[2])
        if not z is None:
            x.instrument_cfVariable = z
            x.save()


