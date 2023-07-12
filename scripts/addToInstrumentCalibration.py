import io
import pandas as pd
from gliderMetadataApp import models

def initiate_InstrumentCalibration():
    file = io.FileIO(file=r".\initializationData\instrument\instrumentCalibration03.csv", mode="r")
    df = pd.read_csv(file)
    # format instrument_calibrationDate
    df['instrument_calibrationDate'] = pd.to_datetime(df['instrument_calibrationDate'], format='"%Y-%m-%d"')
    for row in df.itertuples():
        ic = models.InstrumentCalibration(instrument_calibrationSerial=models.InstrumentSerialNumber.objects.get(pk=getattr(row, "instrumentSerialNumber_id")),
                                          instrument_calibrationDate=getattr(row, "instrument_calibrationDate"),
                                          instrument_calibrationReport=getattr(row, "instrument_calibrationReport"),
                                          instrument_calibrationReportNotes=getattr(row, "instrument_calibrationReportNotes"),
                                          instrument_calibrationDateNotes=getattr(row, "instrument_calibrationDateNotes"))
        ic.save()


initiate_InstrumentCalibration()