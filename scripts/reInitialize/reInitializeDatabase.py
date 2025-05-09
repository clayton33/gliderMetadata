import io
import pandas as pd
from gliderMetadataApp import models
import reInitializePlatform
import reInitializeMisc
import reInitializeMission
import reInitializeInstrument
import reInitializeContributor
import reInitializeContributorMission
import reInitializeContributingInstitutionMission
import reInitializeVariable
## define path to .csv files of a previous state of the database
path = './initializationData/20241210reload'
## commented out calls to functions indicates that the tables were initialized
## note that if the database has to be re-initialized, some care should be taken
## for the primary key call (see comments next to applicable functions)
## Platform
# initiate_PlatformCompany(path)
# initiate_PlatformName(path) # primary key call to PlatformCompany
# initiate_PlatformPayload(path) # primary key call to PlatformName
# initiate_PlatformNavigationFirmware(path)
# initiate_PlatformPayloadFirmware(path)
# initiate_PlatformBattery(path)
# initiate_PlatformRelease(path)
## Miscellaneous
# initiate_Institute(path)
# initiate_ArgosTagPTT(path)
# initiate_ArgosTagSerialNumber(path)
# initiate_Vessel(path)
## Mission
# initiate_Mission(path)
## Instrument
# initiate_InstrumentMake(path)
# initiate_InstrumentType(path)
# initiate_InstrumentModel(path) # primary key to make and type and original platform
# initiate_InstrumentSerialNumber(path) # primary key call to model
# initiate_InstrumentCalibration(path) # primary key call to serial number
# initiate_InstrumentMission(path) # primary key call to instrumentCalibration and Mission
# initiate_InstrumentSeaBird43FOxygenCalibrationCoefficients(path) # primary key call to InstrumentCalibration
## Contributor
#initiate_ContributorPeople(path)
#initiate_Role(path)
#initiate_ContributorMission(path)
#initiate_ContributingInstitutionMission(path)
## Variable
# initiate_Vocabulary()
# initiate_UnitCFStandard(path)
# initiate_VariableCFStandard(path)
# initiate_VariableNERCStandard(path)
# initiate_Variable(path)
# initiate_InstrumentVariable(path)
# initiate_PlatformVariable(path)