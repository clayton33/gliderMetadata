import pandas as pd
from scripts import createPygliderIOOSyaml as d
# list of lists of missions
missions = [['"032"', 79],
            ['"021"', 69],
            ['"019"', 84],
            ['"032"', 65],
            ['"032"', 60],
            ['"024"', 72],
            ['"024"', 67],
            ['"024"', 45],
            ['"024"', 67],
            ['"024"', 69],
            ['"019"', 49],
            ['"032"', 51],
            ['"022"', 88],
            ['"022"', 91],
            ['"021"', 71]]
mdf = pd.DataFrame(missions,
                   columns = ['serialNumber', 'missionNumber'])

for row in mdf.itertuples():
    print(f"Creating deployment yaml for glider {getattr(row, 'serialNumber')} and mission {getattr(row, 'missionNumber')}")
    # create filename since i'm doing a bulk creation (and not putting them in a good spot)
    filename = 'deployment' + '_' + \
               'SEA' + getattr(row, 'serialNumber').strip('\"') + 'M00' + str(getattr(row, 'missionNumber')) + \
                '.yml'
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