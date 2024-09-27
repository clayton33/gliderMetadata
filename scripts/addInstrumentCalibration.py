import io
import operator
import pandas as pd
import re
from gliderMetadataApp import models
# read in file
file = io.FileIO(file=r".\initializationData\instrument\instrumentCalibrationUpdate01.csv", mode="r")
df = pd.read_csv(file)
# format instrument_calibrationDate
df['instrument_calibrationDate'] = pd.to_datetime(df['instrument_calibrationDate'], format='"%Y-%m-%d"')
for row in df.itertuples():
    print(f"Getting {getattr(row, 'instrument_model')} with SN {getattr(row, 'instrument_serialNumber')}"
          f" with calibration date {getattr(row, 'instrument_calibrationDate')}")
    # get the instrument model pk
    imQ = models.InstrumentModel.objects.get(instrument_model = getattr(row, 'instrument_model'))
    # get instrument serial number
    isnQ = models.InstrumentSerialNumber.objects.get(instrument_serialNumberModel = imQ.pk,
                                                     instrument_serialNumber = getattr(row, 'instrument_serialNumber'))
    # check if new calibration has been added
    icdQ = models.InstrumentCalibration.objects.filter(instrument_calibrationSerial = isnQ,
                                                       instrument_calibrationDate = getattr(row, 'instrument_calibrationDate'))
    # if not there, add it
    if icdQ.first() is None:
        print("Adding...")
    # now set the new calibration date and other info
        icd = models.InstrumentCalibration(instrument_calibrationSerial = isnQ,
                                           instrument_calibrationDate = getattr(row, 'instrument_calibrationDate'),
                                           instrument_calibrationReport = getattr(row, 'instrument_calibrationReport'),
                                           instrument_calibrationReportNotes = getattr(row, 'instrument_calibrationReportNotes'),
                                           instrument_calibrationDateNotes = getattr(row, 'instrument_calibrationDateNotes'))
        icd.save()
    else:
        print("Already in database.")