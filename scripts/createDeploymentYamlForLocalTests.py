import os
import re

import pandas as pd
from scripts import createPygliderIOOSyaml as d

# get list of directories in local test directory
# not good, but it's fine for these tests
path='C:/Users/laytonc/Documents/requests/laytonChantelle/20240705testGliderBatchProcessing'
nonHiddenDir = [f for f in os.listdir(path) if not f.startswith('.')]
gldDir = [f for f in nonHiddenDir if os.path.isdir(os.path.join(path, f))]
gldPath = [path + '/' + k for k in gldDir]
# get glider serial number and mission from directory name (kind of fragile)
gldSerial = [re.sub("GLD(\\d+)SEA(\\d+)M(\\d+)", "\\2", k) for k in gldDir]
gldMission = [re.sub("GLD(\\d+)SEA(\\d+)M(\\d+)", "\\3", k) for k in gldDir]
# add "" around gldSerial
gldSerial = ['"' + k + '"' for k in gldSerial]
# create dataframe to pass along to fn to create .yml file
mdf = pd.DataFrame(
    {
        'serialNumber': gldSerial,
        'missionNumber': gldMission,
        'path': gldPath
    })

for row in mdf.itertuples():
    print(f"Creating deployment yaml for glider {getattr(row, 'serialNumber')} and mission {getattr(row, 'missionNumber')}")
    # create filename since i'm doing a bulk creation (and not putting them in a good spot)
    # filename = 'deployment' + '_' + \
    #            'SEA' + getattr(row, 'serialNumber').strip('\"') + 'M00' + str(getattr(row, 'missionNumber')) + \
    #             '.yml'
    filename = getattr(row, 'path') + '/' + 'deployment.yml'
    # snCheck = getattr(row, 'serialNumber') == '"032"'
    # mnCheck = getattr(row, 'missionNumber') in [65, 60]
    # if snCheck & mnCheck:
    #     timebase_sourceVariable = 'LEGATO_TEMPERATURE'  # not sure ?
    # else:
    #     timebase_sourceVariable = 'GPCTD_TEMPERATURE'
    timebase_sourceVariable = 'NAV_LATITUDE'
    d.createPygliderIOOSyaml(platform_company='Alseamar',
                             platform_model='SeaExplorer',
                             platform_serial=getattr(row, 'serialNumber'),
                             mission_number=getattr(row, 'missionNumber'),
                             timebase_sourceVariable=timebase_sourceVariable,
                             interpolate=False,
                             add_keep_variables=True,
                             filename=filename)

