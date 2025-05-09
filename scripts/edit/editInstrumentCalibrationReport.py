import io
import operator
import pandas as pd
import re
from gliderMetadataApp import models
# read in file
file = io.FileIO(file=r".\initializationData\instrument\instrumentCalibrationFilenameFix.csv", mode="r")
df = pd.read_csv(file)
# format instrument_calibrationDate
df['instrument_calibrationDate'] = pd.to_datetime(df['instrument_calibrationDate'], format='"%Y-%m-%d"')
for row in df.itertuples():
    print(f"Getting {getattr(row, 'instrument_calibrationDate')} and {getattr(row, 'instrument_calibrationReport')}")
    # check if it's already been updated
    xup = models.InstrumentCalibration.objects.filter(instrument_calibrationDate=getattr(row, 'instrument_calibrationDate'),
                                                      instrument_calibrationReport=getattr(row, 'instrument_calibrationReportNew'))
    # if not, update it
    if xup.first() is None:
        print("Updating...")
        x = models.InstrumentCalibration.objects.get(instrument_calibrationDate=getattr(row, 'instrument_calibrationDate'),
                                                     instrument_calibrationReport=getattr(row, 'instrument_calibrationReport'))
        x.instrument_calibrationReport = getattr(row, 'instrument_calibrationReportNew')
        x.save()
    else :
        print("Already updated.")