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
    # halifax line (HL) and passive acoustic monitoring in emerald basin (PAM EB)
    if getattr(row, 'Missiontype') in ['HL', 'PAM EB']:
        contributingInstitution=['Bedford Institute of Oceanography', 'Bedford Institute of Oceanography']
        contributingInstitutionVocab=['https://edmo.seadatanet.org/report/1811','https://edmo.seadatanet.org/report/1811']
        contributingInstitutionRole=['Operator', 'PI']
        contributingInstitutionRoleVocab=['https://vocab.nerc.ac.uk/collection/W08/current/CONT0003/', 'https://vocab.nerc.ac.uk/collection/W08/current/CONT0004/']
    # bonavista (BBL)
    if getattr(row, 'Missiontype') in ['BBL']:
        contributingInstitution = ['Bedford Institute of Oceanography', 'Northwest Atlantic Fisheries Centre', 'Northwest Atlantic Fisheries Centre']
        contributingInstitutionVocab = ['https://edmo.seadatanet.org/report/1811', 'https://edmo.seadatanet.org/report/4157', 'https://edmo.seadatanet.org/report/4157']
        contributingInstitutionRole = ['Operator', 'Operator', 'PI']
        contributingInstitutionRoleVocab = ['https://vocab.nerc.ac.uk/collection/W08/current/CONT0003/', 'https://vocab.nerc.ac.uk/collection/W08/current/CONT0003/', 'https://vocab.nerc.ac.uk/collection/W08/current/CONT0004/']
    im.mission_contributingInstitutions=', '.join(contributingInstitution)
    im.mission_contributingInstitutionVocabulary=', '.join(contributingInstitutionVocab)
    im.mission_contributingInstitutionsRole=', '.join(contributingInstitutionRole)
    im.mission_contributingInstitutionsRoleVocabulary=', '.join(contributingInstitutionRoleVocab)
    im.save()