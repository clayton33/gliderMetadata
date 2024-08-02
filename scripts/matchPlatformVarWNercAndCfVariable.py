import io
import re
import pandas as pd
from gliderMetadataApp import models

m = [['Timestamp', 'TIME', ''],
     #['NavState', '', ''],
     #['SecurityLevel', '', ''],
     ['Heading', 'GLIDER_HEADING', ''],
     #['Declination', '', ''],
     ['Pitch', 'GLIDER_PITCH', 'platform_pitch'],
     ['Roll', 'GLIDER_ROLL', 'platform_roll'],
     #['Depth', '', ''],
     #['Temperature', '', ''],
     #['Pa', '', ''],
     #['Lon', '', ''],
     #['Lat', '', ''],
     #['DeadReckoning', '', ''],
     #['DesiredH', '', ''],
     #['BallastCmd', '', ''],
     #['BallastPos', '', ''],
     #['LinCmd', '', ''],
     #['AngCmd', '', ''],
     #['AngPos', '', ''],
     #['Voltage', '', ''],
     ['Altitude', 'ALTITUDE', ''],
     #['NAV_RESOURCE', '', ''],
     #['NAV_MISSIONID', '', ''],
     #['NAV_NUMBEROFYO', '', ''],
     ['NAV_LONGITUDE', 'LONGITUDE', 'longitude'],
     ['NAV_LATITUDE', 'LATITUDE', 'latitude'],
     #['NAV_DEPTH', '', '']
     ]

for var in m:
    x = models.PlatformVariable.objects.get(platform_variableSourceName = var[0])
    if not (len(var[1]) == 0):
        y = models.VariableNERCStandard.objects.get(variable_nerc_variableName=var[1])
        if not y is None:
            x.platform_nercVariable = y
            x.save()
    if not (len(var[2]) == 0):
        z = models.VariableCFStandard.objects.get(variable_standardName=var[2])
        if not z is None:
            x.platform_cfVariable = z
            x.save()