import io
import pandas as pd
from gliderMetadataApp import models

def initiate_PlatformCompany():
    #  initialize PlatformCompany
    file = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_platformcompany.csv", mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        print(getattr(row, "platform_company"))
        pc = models.PlatformCompany(platform_company=getattr(row, "platform_company"),
                                    platform_model=getattr(row, "platform_model"))
        pc.save()


def initiate_PlatformName():
    file = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_platformname.csv", mode="r")
    df = pd.read_csv(file)
    # b/c the pk of the reinitialized may or may not match up with the new pk, have to cross reference
    file2 = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_platformcompany.csv", mode="r")
    df2 = pd.read_csv(file2)
    for row in df.itertuples():
        # have to filter based on the match between 'platform_companyId_id' in file to 'id' in file2
        df2sub = df2[df2['id'] == getattr(row, 'platform_companyId_id')].iloc[0]
        pc = models.PlatformCompany.objects.get(platform_company=df2sub["platform_company"],
                                    platform_model=df2sub["platform_model"])
        pn = models.PlatformName(platform_companyId=pc,
                                 platform_serial=getattr(row, "platform_serial"),
                                 platform_name=getattr(row, "platform_name"),
                                 platform_wmo=getattr(row, "platform_wmo"))
        pn.save()


def initiate_PlatformNavigationFirmware():
    file = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_platformnavigationfirmware.csv", mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        pnf = models.PlatformNavigationFirmware(platform_navFirmwareVersion=getattr(row, "platform_navFirmwareVersion"),
                                                platform_navFirmwareComments=getattr(row, "platform_navFirmwareComments"))
        pnf.save()


def initiate_PlatformPayload():
    file = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_platformpayload.csv", mode="r")
    df = pd.read_csv(file)
    file2 = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_platformname.csv", mode="r")
    df2 = pd.read_csv(file2)
    for row in df.itertuples():
        df2sub = df2[df2["id"] == getattr(row, "platform_payloadOriginalPlatform_id")].iloc[0]
        pn = models.PlatformName.objects.get(platform_serial=df2sub["platform_serial"],
                                             platform_name=df2sub["platform_name"],
                                             platform_wmo=df2sub["platform_wmo"])
        pp = models.PlatformPayload(platform_payloadSerialNumber=getattr(row, "platform_payloadSerialNumber"),
                                    platform_payloadOriginalPlatform=pn)
        pp.save()


def initiate_PlatformPayloadFirmware():
    file = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_platformpayloadfirmware.csv", mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        ppf = models.PlatformPayloadFirmware(platform_payloadFirmwareVersion=getattr(row, "platform_payloadFirmwareVersion"),
                                             platform_payloadFirmwareVersionComments=getattr(row, "platform_payloadFirmwareVersionComments"))
        ppf.save()


def initiate_PlatformBattery():
    file = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_platformbattery.csv", mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        pb = models.PlatformBattery(platform_batteryType=getattr(row, "platform_batteryType"),
                                    platform_batteryGeneration=getattr(row, "platform_batteryGeneration"))
        pb.save()


def initiate_PlatformRelease():
    file = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_platformrelease.csv", mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        pr = models.PlatformRelease(platform_releaseType=getattr(row, "platform_releaseType"),
                                    platform_releaseAttachMethod=getattr(row, "platform_releaseAttachMethod"))
        pr.save()


# commented out calls to functions indicates that the tables were initialized
# note that if the database has to be re-initialized, some care should be taken
# for the primary key call (see comments next to applicable functions)
# initiate_PlatformCompany()
# initiate_PlatformName() # primary key call to PlatformCompany
# initiate_PlatformNavigationFirmware()
# initiate_PlatformPayload() # primary key call to PlatformName
# initiate_PlatformPayloadFirmware()
# initiate_PlatformBattery()
# initiate_PlatformRelease()