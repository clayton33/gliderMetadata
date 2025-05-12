import io
import pandas as pd
from gliderMetadataApp import models

data = {'platformNavigationFirmware':['v3.8.2-r'],
        'platformNavigationFirmwareNotes':['humidity']}
df = pd.DataFrame(data)
# file = io.FileIO(file=r".\initializationData\platform\platformNavigationFirmware03.csv", mode="r")
# df = pd.read_csv(file)
for row in df.itertuples():
    print(f"Getting firmware version {getattr(row, 'platformNavigationFirmware')} "
          f"with comment {getattr(row, 'platformNavigationFirmwareNotes')}")
    # check to see if data already added
    ipnfQ = models.PlatformNavigationFirmware.objects.filter(platform_navFirmwareVersion=getattr(row, "platformNavigationFirmware"))
    if ipnfQ.first() is None:
        print('Adding ...')
        pnf = models.PlatformNavigationFirmware(platform_navFirmwareVersion=getattr(row, "platformNavigationFirmware"),
                                                platform_navFirmwareComments=getattr(row, "platformNavigationFirmwareNotes"))
        pnf.save()
    else:
        print("Already in database.")


