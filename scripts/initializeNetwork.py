import io
import operator
import pandas as pd
import re
from gliderMetadataApp import models
from scripts import fn_readMissionFile as rmf

def convert_date(date):
    return pd.to_datetime(date.apply(lambda d: str(d)[0:8]), errors='coerce')

df = rmf.readMissionFile()

# Doing the 'BBL' missions, so subset df to those missions
#df = df[df['Missiontype'] == 'BBL']

# get pk value of the platform to find mission pk
# mission_platformName
# reformat df['Glider'] to be able to match it with database
gliderSerial = [re.sub('SEA(\\d+)', '\\1', x) for x in df['Glider']]
gliderSerial = ['"' + x + '"' for x in gliderSerial]
# get pk from models.PlatformName
platformNamePk = []
for i in gliderSerial:
    platformNameQ = models.PlatformName.objects.filter(platform_serial=i).first()
    if platformNameQ is None:
        print(f"Unable to find primary key value for glider with serial number {i}")
        platformNamePk.append(None)
    else:
        platformNamePk.append(platformNameQ.pk)

# add platformNamePk to df
df['platformNamePk'] = platformNamePk

for row in df.itertuples():
    missionQ = models.Mission.objects.filter(mission_platformName=getattr(row, 'platformNamePk'),
                                             mission_number=getattr(row, 'missionNumber')).first()
    im = models.Mission.objects.get(pk=missionQ.pk) # not sure if this is redundant
    # define contributingInstitution, contributingInstitutionVocabulary, contributingInstitutionRole,
    #   contributingInstitutionRoleVocabulary
    # halifax line (HL) and bonavista (BBL)
    if getattr(row, 'Missiontype') in ['HL', 'BBL']:
        network = 'OceanGliders > BOON > Northwest Atlantic Ocean > Atlantic Zone Monitoring Program'
    else:
        network = 'OceanGliders > BOON > Northwest Atlantic Ocean'
    im.mission_network = network
    im.save()