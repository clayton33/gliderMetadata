import io
import operator
import pandas as pd
import re
from gliderMetadataApp import models
# read in file
file = io.FileIO(file=r".\initializationData\instrument\instrumentSerialNumberUpdate.csv", mode="r")
df = pd.read_csv(file)
for row in df.itertuples():
    # get the instrument model pk
    imQ = models.InstrumentModel.objects.get(instrument_model = getattr(row, 'instrumentModel'))
    # get instrument serial number
    isn = models.InstrumentSerialNumber(instrument_serialNumberModel = imQ,
                                        instrument_serialNumber = getattr(row, 'instrument_serialNumber'))
    isn.save()