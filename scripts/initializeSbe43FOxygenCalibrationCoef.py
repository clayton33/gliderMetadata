import io
import re
import pandas as pd
from gliderMetadataApp import models

def initiatecalibrationSeabird43F():
    file = io.FileIO(file=r".\initializationData\instrument\seaExplorerOxygenCalibrationCoefficients.csv")
    df = pd.read_csv(file)
    for row in df.itertuples():
        print(f"Checking for Seabird 43F Oxygen sensor with serial number {getattr(row, 'serialNumber')} and"
              f" calibration date {getattr(row, 'calibrationDate')}")
        # get pk from instrumentModel for instrument_model = '43F'
        instModel = models.InstrumentModel.objects.filter(instrument_model = '43F')
        # get pk from instrumentSerialNumber using above pk and the row.serialNumber
        instSN = models.InstrumentSerialNumber.objects.filter(instrument_serialNumberModel = instModel.first().pk,
                                                              instrument_serialNumber = '"' + getattr(row, 'serialNumber') + '"')
        # get pk from instrumentCalibration using above pk and row.calibrationDate
        instCalib = models.InstrumentCalibration.objects.filter(instrument_calibrationSerial=instSN.first().pk,
                                                            instrument_calibrationDate=pd.to_datetime(getattr(row, 'calibrationDate'),
                                                                                                      format = '%Y-%m-%d'))
        if instCalib.exists():
            print(f"Sensor with associated calibration date exists in database, initializing coefficient")
            x = models.InstrumentSeabird43FOxygenCalibrationCoefficients(calibrationSeaBird43F_calibration=instCalib.first(),
                                                                         calibrationSeaBird43F_Soc=getattr(row, 'Soc'),
                                                                         calibrationSeaBird43F_Foffset=getattr(row, 'Foffset'),
                                                                         calibrationSeaBird43F_Tau20=getattr(row, 'Tau20'),
                                                                         calibrationSeaBird43F_A=getattr(row, 'A'),
                                                                         calibrationSeaBird43F_B=getattr(row, 'B'),
                                                                         calibrationSeaBird43F_C=getattr(row, 'C'),
                                                                         calibrationSeaBird43F_Enom=getattr(row, 'Enom'))
            x.save()
        else:
            if instSN.exists():
                print(f"Sensor exists in database, associated calibration date does not.")
            else:
                print(f"Sensor does not exists in database.")

initiatecalibrationSeabird43F()


