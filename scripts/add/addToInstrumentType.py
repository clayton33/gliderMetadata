import io
import pandas as pd
from gliderMetadataApp import models

def initiate_InstrumentType():
    file = io.FileIO(file=r".\initializationData\instrument\instrumentType02.csv", mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        it = models.InstrumentType(instrument_type=getattr(row, "instrument_type"))
        it.save()

initiate_InstrumentType()