import io
import pandas as pd
from gliderMetadataApp import models


def initiate_InstrumentMake():
    file = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_instrumentmake.csv", mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        im = models.InstrumentMake(instrument_make=getattr(row, "instrument_make"))
        im.save()


def initiate_InstrumentType():
    file = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_instrumenttype.csv", mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        it = models.InstrumentType(instrument_type=getattr(row, "instrument_type"))
        it.save()


def initiate_InstrumentModel():
    file = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_instrumentmodel.csv", mode="r")
    df = pd.read_csv(file)
    fileim = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_instrumentmake.csv", mode="r")
    dfim = pd.read_csv(fileim)
    fileit = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_instrumenttype.csv", mode="r")
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


def initiate_InstrumentSerialNumber():
    file = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_instrumentserialnumber.csv", mode="r")
    df = pd.read_csv(file)
    fileim = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_instrumentmodel.csv", mode="r")
    dfim = pd.read_csv(fileim)
    filepn = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_platformname.csv", mode="r")
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


def initiate_InstrumentCalibration():
    file = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_instrumentcalibration.csv", mode="r")
    df = pd.read_csv(file)
    # not sure if I should get instrument_serialNumberModel as well...
    fileisn = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_instrumentserialnumber.csv", mode="r")
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

def initiate_InstrumentMission():
    file = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_instrumentmission.csv", mode="r")
    df = pd.read_csv(file)
    # calibration
    fileic = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_instrumentcalibration.csv",
                        mode="r")
    dfic = pd.read_csv(fileic)
    # mission
    filem = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_mission.csv", mode="r")
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


# commented out calls to functions indicates that the tables were initialized
# note that if the database has to be re-initialized, some care should be taken
# for the primary key call (see comments next to applicable functions)
# initiate_InstrumentMake()
# initiate_InstrumentType()
# initiate_InstrumentModel() # primary key to make and type and original platform
# initiate_InstrumentSerialNumber() # primary key call to model
# initiate_InstrumentCalibration() # primary key call to serial number
# initiate_InstrumentMission() # primary key call to instrumentCalibration and Mission