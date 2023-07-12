import io
import pandas as pd
from gliderMetadataApp import models

def initiate_InstrumentSerialNumber():
    file = io.FileIO(file=r".\initializationData\instrument\instrumentSerialNumber02.csv", mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        isn = models.InstrumentSerialNumber(instrument_serialNumberModel=models.InstrumentModel.objects.get(pk=getattr(row, "instrumentModel_id")),
                                            instrument_originalPlatform=models.PlatformName.objects.get(pk=getattr(row, "instrument_originalPlatform")),
                                            instrument_serialNumber=getattr(row, "instrument_serialNumber"))
        isn.save()

initiate_InstrumentSerialNumber()