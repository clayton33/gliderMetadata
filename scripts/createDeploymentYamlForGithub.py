import os
import re
import pandas as pd
from gliderMetadataApp import models
from scripts import createPygliderIOOSyaml as d
# not good, but it's fine for these tests
path='C:/Users/laytonc/Documents/GitHub/deploymentYaml'
# create a deployment yaml for every glider mission
# query from database to get
# serialNumber (for fn)
# missionNumber (for fn)
# and cruiseNumber (for filename)
m = models.Mission.objects.all()
serialNumber = []
missionNumber = []
cruiseNumber = []
for item in m.iterator():
    serialNumber.append(item.mission_platformName.platform_serial)
    missionNumber.append(item.mission_number)
    cruiseNumber.append(item.mission_cruiseNumber)

# change cruiseNumber to match with repo name in BIODataSvc SRC
# e.g. 'GLI2020SEA019M78'
cnStart = [re.sub("(\\w+)\\_(\\w+)\\_(\\w+)", "\\1", k) for k in cruiseNumber]
cnGld = [re.sub("(\\w+)\\_(\\w+)\\_(\\w+)", "\\2", k) for k in cruiseNumber]
cnMission = [re.sub("(\\w+)\\_(\\w+)\\_(\\w+)", "\\3", k) for k in cruiseNumber]
cnMissionNum = [int(k) for k in cnMission]
filename = []
for k in range(len(cnStart)):
    x = cnStart[k] + cnGld[k] + 'M' + str(cnMissionNum[k]) + '.yaml'
    filename.append(x)

mdf = pd.DataFrame(
    {
        'serialNumber':serialNumber,
        'missionNumber':missionNumber,
        'filename':filename
    }
)
for row in mdf.itertuples():
    print(f"Creating deployment yaml for glider {getattr(row, 'serialNumber')} and mission {getattr(row, 'missionNumber')}")
    destFile = path + '/' + getattr(row, 'filename')
    timebase_sourceVariable = 'NAV_LATITUDE'
    d.createPygliderIOOSyaml(platform_company='Alseamar',
                             platform_model='SeaExplorer',
                             platform_serial=getattr(row, 'serialNumber'),
                             mission_number=getattr(row, 'missionNumber'),
                             timebase_sourceVariable=timebase_sourceVariable,
                             interpolate=False,
                             add_keep_variables=True,
                             filename=destFile)