import io
import operator
import pandas as pd
import re
from gliderMetadataApp import models
# can either put information in a .csv file, or create a dataframe here with comments
# need 6 columns,
# 'instrument_model'
# 'instrument_serialNumber'
# 'instrument_calibrationDate'
# 'instrument_calibrationReportNotes'
# 'instrument_calibrationDateNotes'

# read in file
# file = io.FileIO(file=r".\initializationData\instrument\instrumentCalibrationUpdate01.csv", mode="r")
# df = pd.read_csv(file)
# 20250509 - add SX Legato and coda instruments
data = {'instrument_model' :['RBR Legato3',
                             'RBR Legato3', 'RBR Legato3', 'RBR Legato3', 'RBR Legato3',
                             'RBR Legato3',
                             'RBR Legato3',
                             'RBR Coda T.ODO',
                             'RBR Coda T.ODO'],
        'instrument_serialNumber' : ['"205045"',
                                     '"210185"', '"210185"', '"210185"', '"210185"',
                                     '"212531"',
                                     '"214386"',
                                     '"212279"',
                                     '"212973"'],
        'instrument_calibrationDate' : ['"2020-07-29"',
                                        '"2023-01-09"', '"2023-09-06"', '"2023-11-15"', '"2024-09-16"',
                                        '"2025-04-16"',
                                        '"2025-04-17"',
                                        '"2025-03-26"',
                                        '"2025-03-25"'],
        'instrument_calibrationReport' : ['LEGATO_205045-20200729.pdf',
                                          'LEGATO_210185_20230109.pdf', 'LEGATO_210185_20230906.pdf', 'LEGATO_210185_20231115.pdf', 'LEGATO_210185_20240916.pdf',
                                          'LEGATO_212531_20250416.pdf',
                                          'LEGATO_214386_20250417.pdf',
                                          'CODA_212279_20250326.pdf',
                                          'CODA_212973_20250325.pdf'],
        'instrument_calibrationReportNotes' : ['',
                                               '', '', '', '',
                                               '',
                                               '',
                                               '',
                                               ''],
        'instrument_calibrationDateNotes' : ['',
                                            '', '','','',
                                            '',
                                            '',
                                            '',
                                            '']}
df = pd.DataFrame(data)
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