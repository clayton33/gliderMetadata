import pandas as pd
from gliderMetadataApp import models

# fix a number of calibration dates in InstrumentsCalibration table
# these errors were identified when doing initial tests to initialize the InstrumentsMission table
# notes for each fix will be provided

# GPCTD 0188 2016 calibration
ic = models.InstrumentCalibration.objects.get(pk=31)
ic.instrument_calibrationDate = pd.to_datetime("2016-05-07", format='%Y-%m-%d').date()
ic.save()

# GPCTD 0188 2018 calibration
ic = models.InstrumentCalibration.objects.get(pk=32)
ic.instrument_calibrationDate = pd.to_datetime("2018-07-26", format='%Y-%m-%d').date()
ic.save()

# GPCTD 0188 2020 calibration
ic = models.InstrumentCalibration.objects.get(pk=34)
ic.instrument_calibrationDate = pd.to_datetime("2020-12-30", format='%Y-%m-%d').date()
ic.save()

# GPCTD 0241  2017 calibration
ic = models.InstrumentCalibration.objects.get(pk=40)
ic.instrument_calibrationDate = pd.to_datetime("2017-11-02", format='%Y-%m-%d').date()
ic.save()

# GPCTD 0241 2019 calibration
ic = models.InstrumentCalibration.objects.get(pk=41)
ic.instrument_calibrationDate = pd.to_datetime("2019-12-29", format='%Y-%m-%d').date()
ic.save()

# GPCTD 0184 2019 calibration
ic = models.InstrumentCalibration.objects.get(pk=15)
ic.instrument_calibrationDate = pd.to_datetime("2019-12-29", format='%Y-%m-%d').date()
ic.save()

# GPCTD 0184 2022 calibration
ic = models.InstrumentCalibration.objects.get(pk=16)
ic.instrument_calibrationDate = pd.to_datetime("2022-02-10", format='%Y-%m-%d').date()
ic.save()

# GPCTD 0186 2020 calibration
ic = models.InstrumentCalibration.objects.get(pk=4)
ic.instrument_calibrationDate = pd.to_datetime("2020-11-27", format='%Y-%m-%d').date()
ic.save()

# GPCTD DO 43-3336 2018 calibration
ic = models.InstrumentCalibration.objects.get(pk=18)
ic.instrument_calibrationDate = pd.to_datetime("2018-08-18", format='%Y-%m-%d').date()
ic.save()

# GPCTD DO 43-3336 2019 calibration
ic = models.InstrumentCalibration.objects.get(pk=19)
ic.instrument_calibrationDate = pd.to_datetime("2019-12-20", format='%Y-%m-%d').date()
ic.save()

# GPCTD DO 43-3365 2019 calibration
ic = models.InstrumentCalibration.objects.get(pk=37)
ic.instrument_calibrationDate = pd.to_datetime("2019-08-18", format='%Y-%m-%d').date()
ic.save()

# GPCTD DO 43-3338 2021 calibration
ic = models.InstrumentCalibration.objects.get(pk=9)
ic.instrument_calibrationDate = pd.to_datetime("2021-02-06", format='%Y-%m-%d').date()
ic.save()

# LEGATO, change instrumentCalibration to the Legato with serial 210185 calibrated on 2023-01-09
ic = models.InstrumentCalibration.objects.get(pk=49)
ic.instrument_calibrationSerial_id = 18
ic.save()

# Minifluo, 2020 calibration
ic = models.InstrumentCalibration.objects.get(pk=45)
ic.instrument_calibrationDate = pd.to_datetime("2020-03-16", format='%Y-%m-%d').date()
ic.save()

# GPCTD 0175 2022 calibration
ic = models.InstrumentCalibration.objects.get(pk=25)
ic.instrument_calibrationDate = pd.to_datetime("2022-02-19", format='%Y-%m-%d').date()
ic.save()

# GPCTD DO 43-3276 2022 calibration (end of year 2021)
ic = models.InstrumentCalibration.objects.get(pk=29)
ic.instrument_calibrationDate = pd.to_datetime("2021-12-22", format='%Y-%m-%d').date()
ic.save()
