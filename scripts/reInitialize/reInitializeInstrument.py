import io
import pandas as pd
from gliderMetadataApp import models


def initiate_InstrumentMake(path):
    filename = "gliderMetadataApp_instrumentmake.csv"
    pathfile = path + '/' + filename
    file = io.FileIO(file=pathfile, mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        im = models.InstrumentMake(instrument_make=getattr(row, "instrument_make"))
        im.save()


def initiate_InstrumentType(path):
    filename = "gliderMetadataApp_instrumenttype.csv"
    pathfile = path + '/' + filename
    file = io.FileIO(file=filename, mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        it = models.InstrumentType(instrument_type=getattr(row, "instrument_type"))
        it.save()


def initiate_InstrumentModel(path):
    filename = "gliderMetadataApp_instrumentmodel.csv"
    pathfile = path + '/' + filename
    file = io.FileIO(file=pathfile, mode="r")
    df = pd.read_csv(file)
    # instrument make
    filenameim = "gliderMetadataApp_instrumentmake.csv"
    pathfileim = path + '/' + filenameim
    fileim = io.FileIO(file=pathfileim, mode="r")
    dfim = pd.read_csv(fileim)
    # instrument type
    filenameit = "gliderMetadataApp_instrumenttype.csv"
    pathfileit = path + '/' + filenameit
    fileit = io.FileIO(file=pathfileit, mode="r")
    dfit = pd.read_csv(fileit)
    for row in df.itertuples():
        dfimsub = dfim[dfim['id'] == getattr(row, 'instrument_modelMake_id')].iloc[0]
        dfitsub = dfit[dfit['id'] == getattr(row, 'instrument_modelType_id')].iloc[0]
        ima = models.InstrumentMake.objects.get(instrument_make=dfimsub['instrument_make'])
        it = models.InstrumentType.objects.get(instrument_type=dfitsub['instrument_type'])
        im = models.InstrumentModel(instrument_modelMake=ima,
                                    instrument_modelType=it,
                                    instrument_model=getattr(row, "instrument_model"),
                                    instrument_longname=getattr(row, "instrument_longname"))
        im.save()


def initiate_InstrumentSerialNumber(path):
    filename = "gliderMetadataApp_instrumentserialnumber.csv"
    pathfile = path + '/' + filename
    file = io.FileIO(file=pathfile, mode="r")
    df = pd.read_csv(file)
    # instrument model
    filenameim = "gliderMetadataApp_instrumentmodel.csv"
    pathfileim = path + '/' + filenameim
    fileim = io.FileIO(file=pathfileim, mode="r")
    dfim = pd.read_csv(fileim)
    # platform name
    filenamepn = "gliderMetadataApp_platformname.csv"
    pathfilepn = path + '/' + filenamepn
    filepn = io.FileIO(file=pathfilepn, mode="r")
    dfpn = pd.read_csv(filepn)
    for row in df.itertuples():
        dfimsub = dfim[dfim['id'] == getattr(row, 'instrument_serialNumberModel_id')].iloc[0]
        dfpnsub = dfpn[dfpn['id'] == getattr(row, 'instrument_originalPlatform_id')].iloc[0]
        im = models.InstrumentModel.objects.get(instrument_model=dfimsub['instrument_model'])
        pn = models.PlatformName.objects.get(platform_wmo=dfpnsub["platform_wmo"])
        isn = models.InstrumentSerialNumber(instrument_serialNumberModel=im,
                                            instrument_originalPlatform=pn,
                                            instrument_serialNumber=getattr(row, "instrument_serialNumber"))
        isn.save()


def initiate_InstrumentCalibration(path):
    filename = "gliderMetadataApp_instrumentcalibration.csv"
    pathfile = path + '/' + filename
    file = io.FileIO(file=pathfile, mode="r")
    df = pd.read_csv(file)
    # not sure if I should get instrument_serialNumberModel as well...
    filenameisn = "gliderMetadataApp_instrumentserialnumber.csv"
    pathfileisn = path + '/' + filenameisn
    fileisn = io.FileIO(file=pathfileisn, mode="r")
    dfisn = pd.read_csv(fileisn)
    # format instrument_calibrationDate
    # df['instrument_calibrationDate'] = pd.to_datetime(df['instrument_calibrationDate'], format='"%Y-%m-%d"')
    for row in df.itertuples():
        dfisnsub = dfisn[dfisn['id'] == getattr(row, 'instrument_calibrationSerial_id')].iloc[0]
        isn = models.InstrumentSerialNumber.objects.get(instrument_serialNumber=dfisnsub['instrument_serialNumber'])
        ic = models.InstrumentCalibration(instrument_calibrationSerial=isn,
                                          instrument_calibrationDate=getattr(row, "instrument_calibrationDate"),
                                          instrument_calibrationReport=getattr(row, "instrument_calibrationReport"),
                                          instrument_calibrationReportNotes=getattr(row, "instrument_calibrationReportNotes"),
                                          instrument_calibrationDateNotes=getattr(row, "instrument_calibrationDateNotes"))
        ic.save()

def initiate_InstrumentMission(path):
    filename = "gliderMetadataApp_instrumentmission.csv"
    pathfile = path + '/' + filename
    file = io.FileIO(file=pathfile, mode="r")
    df = pd.read_csv(file)
    # calibration
    filenameic = "gliderMetadataApp_instrumentcalibration.csv"
    pathfileic = path + '/' + filenameic
    fileic = io.FileIO(file=pathfileic,
                        mode="r")
    dfic = pd.read_csv(fileic)
    # mission
    filenamem = "gliderMetadataApp_mission.csv"
    pathfilem = path + '/' + filenamem
    filem = io.FileIO(file=pathfilem, mode="r")
    dfm = pd.read_csv(filem)
    for row in df.itertuples():
        dficsub = dfic[dfic['id'] == getattr(row, 'instrument_calibration_id')].iloc[0]
        dfmsub = dfm[dfm['id'] == getattr(row, 'instrument_mission_id')].iloc[0]
        ic = models.InstrumentCalibration.objects.get(instrument_calibrationDate=dficsub['instrument_calibrationDate'],
                                                      instrument_calibrationReport=dficsub['instrument_calibrationReport'])
        m = models.Mission.objects.get(mission_number=dfmsub['mission_number'],
                                       mission_cruiseNumber=dfmsub['mission_cruiseNumber'])
        im = models.InstrumentMission(instrument_mission=m,
                                      instrument_calibration =ic,
                                      instrument_warmUp = getattr(row, 'instrument_warmUp'),
                                      instrument_samplingRate = getattr(row, 'instrument_samplingRate'))
        im.save()


def initiate_InstrumentSeaBird43FOxygenCalibrationCoefficients(path):
    filename = "gliderMetadataApp_instrumentseabird43foxygencalibrationcoefficients.csv"
    pathfile = path + '/' + filename
    file = io.FileIO(file=pathfile, mode="r")
    df = pd.read_csv(file)
    # calibration
    filenameic = "gliderMetadataApp_instrumentcalibration.csv"
    pathfileic = path + '/' + filenameic
    fileic = io.FileIO(file=pathfileic,
                       mode="r")
    dfic = pd.read_csv(fileic)
    for row in df.itertuples():
        dficsub = dfic[dfic['id'] == getattr(row, 'calibrationSeaBird43F_calibration_id')].iloc[0]
        ic = models.InstrumentCalibration.objects.get(instrument_calibrationDate=dficsub['instrument_calibrationDate'],
                                                      instrument_calibrationReport=dficsub['instrument_calibrationReport'])
        iocc = models.InstrumentSeabird43FOxygenCalibrationCoefficients(calibrationSeaBird43F_calibration=ic,
                                                                         calibrationSeaBird43F_Soc=getattr(row, 'calibrationSeaBird43F_Soc'),
                                                                         calibrationSeaBird43F_Foffset=getattr(row, 'calibrationSeaBird43F_Foffset'),
                                                                         calibrationSeaBird43F_Tau20=getattr(row, 'calibrationSeaBird43F_Tau20'),
                                                                         calibrationSeaBird43F_A=getattr(row, 'calibrationSeaBird43F_A'),
                                                                         calibrationSeaBird43F_B=getattr(row, 'calibrationSeaBird43F_B'),
                                                                         calibrationSeaBird43F_C=getattr(row, 'calibrationSeaBird43F_C'),
                                                                         calibrationSeaBird43F_Enom=getattr(row, 'calibrationSeaBird43F_Enom'))
        iocc.save()