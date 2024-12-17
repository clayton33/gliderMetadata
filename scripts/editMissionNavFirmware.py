import io
import operator
import numpy as np
import pandas as pd
import re
from gliderMetadataApp import models
from scripts import fn_readMissionFile as rmf

def convert_date(date):
    return pd.to_datetime(date.apply(lambda d: str(d)[0:8]), errors='coerce')

df = rmf.readMissionFile()

df = df[df['Navfirmware'] =='3.6.1-r backseat']
for row in df.itertuples():
    gliderSerial = re.sub('SEA(\\d+)', '\\1', getattr(row, 'Glider'))
    gliderSerial = '"' + gliderSerial + '"'
    platformNameQ = models.PlatformName.objects.filter(platform_serial=gliderSerial).first()
    missionQ = models.Mission.objects.filter(mission_platformName=platformNameQ.pk,
                                             mission_number=getattr(row, 'missionNumber')).first()
    # get nav firmware pk
    navFirmQ = models.PlatformNavigationFirmware.objects.filter(platform_navFirmwareVersion='v3.6.1-r').first()
    missionQ.mission_platformNavFirmware=navFirmQ
    missionQ.save()