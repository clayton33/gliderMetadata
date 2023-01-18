import io
import operator

import numpy as np
import pandas as pd
import re
from gliderMetadataApp import models


def convert_date(date):
    return pd.to_datetime(date.apply(lambda d: str(d)[0:8]), errors='coerce')


def readMissionFile():
    file = io.FileIO(file=r".\initializationData\GliderMission.xlsx", mode="r")
    dataframe = pd.read_excel(file, skiprows=1)
    # rename some columns
    dataframe = dataframe.rename(columns={"Unnamed: 0": "annualMissionIndex",
                                          "Mission #": "missionNumber",
                                          "# days": "numberOfDays",
                                          "# yo": "numberOfYos",
                                          "# sc profile": "numberOfScienceProfiles",
                                          "# alarm": "numberOfAlarms",
                                          "# alarm OT": "numberOfAlarmsWithOT",
                                          "Science every # yos": "scienceEveryNumberOfYos"})
    # remove special characters from column names
    # space
    dataframe.columns = dataframe.columns.str.replace(r' ', r'', regex=True)
    # '/'
    dataframe.columns = dataframe.columns.str.replace(r'/', '', regex=True)
    # '('
    dataframe.columns = dataframe.columns.str.replace(r'(', '', regex=True)
    # ')'
    dataframe.columns = dataframe.columns.str.replace(r')', '', regex=True)

    # Clean up and remove unnecessary rows
    # 1. Remove rows where 'annualMissionIndex' is NaN
    dataframe = dataframe.dropna(subset=['annualMissionIndex'])

    # Covert dates to something useful
    dataframe['Deploymentdate'] = convert_date(dataframe['Deploymentdate'])
    dataframe['Recoverydate'] = convert_date(dataframe['Recoverydate'])

    return dataframe


df = readMissionFile()
# Pull out information from sheet to match with database
# refer to 'relationDiagram.png' going to follow the order in the 'Mission' table

# mission_platformName
# reformat df['Glider'] to be able to match it with database
gliderSerial = [re.sub('SEA(\\d+)', '\\1', x) for x in df['Glider']]
gliderSerial = ['"' + x + '"' for x in gliderSerial]
# get pk from models.PlatformName
platformNamePk = []
for i in gliderSerial:
    platformNameQ = models.PlatformName.objects.filter(platform_serial=i).first()
    if platformNameQ is None:
        print(f"Unable to find primary key value for glider with serial number {i}")
        platformNamePk.append(None)
    else:
        platformNamePk.append(platformNameQ.pk)

# mission_platformNavFirmware
# remove leading spaces
gliderNavFirm = [x.lstrip() for x in df['Navfirmware']]
# get only the version (sometimes there's comments separated by a space)
gliderNavFirm = [x.split(' ')[0] for x in gliderNavFirm]
# some indicies do not have a 'v' in the front, add it to ones that are missing
gliderNavFirm = ['v' + x if operator.not_(bool(re.search('v', x))) else x for x in gliderNavFirm]
# add '-r' to ones that are missing it
gliderNavFirm = [x + '-r' if operator.not_(bool(re.search('-r|-cr', x))) else x for x in gliderNavFirm]
# get pk from models.PlatformNavigationFirmware
platformNavFirmPk = []
for i in gliderNavFirm:
    platformNavFirmQ = models.PlatformNavigationFirmware.objects.filter(platform_navFirmwareVersion=i).first()
    if platformNavFirmQ is None:
        print(f"Unable to find primary key value for navigation firmware for version {i}")
        platformNavFirmPk.append(None)
    else:
        platformNavFirmPk.append(platformNavFirmQ.pk)

# mission_platformBattery
gliderBattery = df['Battery']
gliderBattery = [re.sub('(\\d+)\\w+ gen', '\\1', x) for x in gliderBattery]
# get pk from models.PlatformBattery
platformBatteryPk = []
for i in gliderBattery:
    platformBatteryQ = models.PlatformBattery.objects.filter(platform_batteryGeneration=i).first()
    if platformBatteryQ is None:
        print(f"Unable to find primary key value for battery with generation {i}")
        platformBatteryPk.append(None)
    else:
        platformBatteryPk.append(platformBatteryQ.pk)

# mission_platformRelease
gliderRelease = df['Release']
gliderRelease = gliderRelease.tolist()
gliderRelease = [x.replace('-', ', ') for x in gliderRelease]
gliderRelease = [x.split(', ') for x in gliderRelease]
# need both the release type and attach method for database
gliderReleaseType = [x[0] for x in gliderRelease]
gliderReleaseType = [x.replace('Mag', 'Magnetic') for x in gliderReleaseType]
gliderReleaseType = [x.replace('wire', 'Wire') for x in gliderReleaseType]
gliderReleaseAttach = [x[1] if x.__len__() > 1 else 'NULL' for x in gliderRelease] # might have to replace 'NULL' with None
# capitalize releaseAttach
gliderReleaseAttach = [x.capitalize() for x in gliderReleaseAttach]
# replace 'Null' with 'nan'
gliderReleaseAttach = [x.replace('Null', 'nan') for x in gliderReleaseAttach]
# get pk from models.PlatformBattery
gliderReleaseList = list(zip(gliderReleaseType, gliderReleaseAttach))
gliderReleaseDf = pd.DataFrame(gliderReleaseList, columns=['Type', 'Attach'])
platformReleasePk = []
for i in gliderReleaseDf.itertuples():
    platformReleaseQ = models.PlatformRelease.objects.filter(platform_releaseType=getattr(i, 'Type'),
                                                             platform_releaseAttachMethod=getattr(i, 'Attach')).first()
    if platformReleaseQ is None:
        print(f"Unable to find primary key value for release system type {getattr(i, 'Type')}"
              f"with attach method {getattr(i, 'Attach')}")
        platformReleasePk.append(None)
    else:
        platformReleasePk.append(platformReleaseQ.pk)

# mission_platformPayload
# useful : np.array(df.columns)
gliderPldSN = df['PLDSN']
# convert to string for matching up with platform
gliderPldSN = [str(int(x)) for x in gliderPldSN]
# get pk from models.PlatformPayload
platformPayloadPk = []
for i in gliderPldSN:
    platformPayloadQ = models.PlatformPayload.objects.filter(platform_payloadSerialNumber=i).first()
    if platformPayloadQ is None:
        print(f"Unable to find primary key value for payload with serial number {i}")
        platformPayloadPk.append(None)
    else:
        platformPayloadPk.append(platformPayloadQ.pk)

# mission_platformPayloadFirmware
gliderPldFirm = df['pldfirmware']
# remove notes
gliderPldFirm = [x.split(' ')[0] for x in gliderPldFirm]
# get pk from models.PlatformPayloadFirmware
platformPayloadFirmPk = []
for i in gliderPldFirm:
    platformPayloadFirmQ = models.PlatformPayloadFirmware.objects.filter(platform_payloadFirmwareVersion=i).first()
    if platformPayloadFirmQ is None:
        print(f"Unable to find primary key value for payload firmware with version {i}")
        platformPayloadFirmPk.append(None)
    else:
        platformPayloadFirmPk.append(platformPayloadFirmQ.pk)

# vessel for recovery and deployment
vessel = df['boatdeprev']
# meaning of vessel objects : deployment/recovery
# mission_deploymentVessel
deploymentVessel = [x.split('/')[0] for x in vessel]
# remove '-'
deploymentVessel = [re.sub('-', ' ', x) for x in deploymentVessel]
# mission_recoveryVessel
recoveryVessel = [x.split('/')[1] for x in vessel]
# remove '-'
recoveryVessel = [re.sub('-', ' ', x) for x in recoveryVessel]
# get pk from models.Vessels
# go through deployment and recovery separately
# note that we'll have to match them based on partial knowledge on the vessel name provided in excel file
modelsVessels = models.Vessel.objects.values_list('vessel_name', flat=True).distinct()
depVesselPk = [ ]
for i in deploymentVessel:
    # find which one it best matches with
    ok = [bool(re.search(i, x)) for x in modelsVessels] # True, False
    ok = [i for i, x in enumerate(ok) if x] # index
    # get the first index so it's easier to use
    if len(ok) == 0:
        print(f"Unable to find a match for deployment vessel {i}")
        depVesselPk.append(None)
    else:
        if len(ok) > 1:
            print(f"Found more than 1 match for deployment vessel {i}. The matches are {[modelsVessels[x] for x in ok]}")
            print(f"Using the first one")
            ok = ok[0]
        else :
            ok = ok[0]
        okvessel = modelsVessels[ok]
        depVesselQ = models.Vessel.objects.filter(vessel_name=okvessel).first() # first() is a bit redundant
        depVesselPk.append(depVesselQ.pk)

recVesselPk = [ ]
for i in recoveryVessel:
    # find which one it best matches with
    ok = [bool(re.search(i, x)) for x in modelsVessels] # True, False
    ok = [i for i, x in enumerate(ok) if x] # index
    # get the first index so it's easier to use
    if len(ok) == 0:
        print(f"Unable to find a match for recovery vessel {i}")
        recVesselPk.append(None)
    else:
        if len(ok) > 1:
            print(f"Found more than 1 match for recovery vessel {i}. The matches are {[modelsVessels[x] for x in ok]}")
            print(f"Using the first one")
            ok = ok[0]
        else :
            ok = ok[0]
        okvessel = modelsVessels[ok]
        recVesselQ = models.Vessel.objects.filter(vessel_name=okvessel).first()  # first() is a bit redundant
        recVesselPk.append(recVesselQ.pk)


# mission_argosTag - need serial number and(/or?) PTT
# argosTag_serialNumber
argosTagSerial = df['ArgosTagsn']
# argosTag_PTT
argosTagPTT = df['ArgosTagPTT']
# get pk from models.ArgosTag
argosTagList = list(zip(argosTagSerial, argosTagPTT))
argosTagDf = pd.DataFrame(argosTagList, columns=['serialNumber', 'PTT'])
argosTagPk = []
for i in argosTagDf.itertuples():
    argosTagQ = models.ArgosTag.objects.filter(argosTag_serialNumber=getattr(i, 'serialNumber'),
                                               argosTag_PTT=getattr(i, 'PTT')).first()
    if argosTagQ is None:
        print(f"Unable to find primary key value for argos tag with serial number  {getattr(i, 'serialNumber')}"
              f" with PTT {getattr(i, 'PTT')}")
        argosTagPk.append(None)
    else:
        argosTagPk.append(argosTagQ.pk)


# ContributionMission table
contributorPIName = df['PI']
contributorPIfirstName = [x.split(' ')[0] for x in contributorPIName]
contributorPIlastName = [x.split(' ')[1] for x in contributorPIName]
# not sure what 'operator' should be. Leaving this for now
# look into different contributor roles


# InstrumentMission table
# have to iterate through each for since there are multiple instruments on the glider per mission
instrumentAbbrev = ['GPCTD',
                    'GPCTDDO',
                    'Rinko',
                    'Ecopuck',
                    'LEGATO',
                    'PAM']
for d in df.itertuples():
    for i in instrumentAbbrev:
        # get the serial number
        serialNumberName = i + 'SN'
        serialNumber = getattr(d, serialNumberName)
        #print(f"Serial number : {serialNumber}")
        # get the calibration date
        # PAM does not have calibration date, so set as nan
        if i == 'PAM':
            calibrationDate = 'nan'
        else:
            calibrationDateName = i + 'caldate'
            calibrationDate = getattr(d, calibrationDateName)
        # get warmup
        # PAM does not have warmup, so set as nan
        if i == 'PAM':
            warmUp = 'nan'
        else:
            # GPCTD DO warm up is same as GPCTD
            if i == 'GPCTDDO':
                i = 'GPCTD'
            warmUpName = i + 'warmup'
            warmUp = getattr(d, warmUpName)