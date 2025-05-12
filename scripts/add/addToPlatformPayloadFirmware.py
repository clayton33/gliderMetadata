import io
import pandas as pd
from gliderMetadataApp import models

data = {'platformPayloadFirmware':['2.24.2-r', '2.25.1-r'],
        'platformPayloadFirmwareComments':['', '']}
df = pd.DataFrame(data)
# file = io.FileIO(file=r".\initializationData\platform\platformPayloadFirmware02.csv", mode="r")
# df = pd.read_csv(file)
for row in df.itertuples():
    print(f"Getting firmware version {getattr(row, 'platformPayloadFirmware')} "
          f"with comment {getattr(row, 'platformPayloadFirmwareComments')}")
    # check to see if data already added
    ippfQ = models.PlatformPayloadFirmware.objects.filter(platform_payloadFirmwareVersion=getattr(row, "platformPayloadFirmware"))
    if ippfQ.first() is None:
        print('Adding ...')
        ppf = models.PlatformPayloadFirmware(platform_payloadFirmwareVersion=getattr(row, "platformPayloadFirmware"),
                                             platform_payloadFirmwareVersionComments=getattr(row, "platformPayloadFirmwareComments"))
        ppf.save()
    else:
        print("Already in database.")