import io
import pandas as pd
from gliderMetadataApp import models


def initiate_PlatformCompany():
    #  initialize PlatformCompany
    file = io.FileIO(file=r".\initializationData\platform\platformCompany.csv", mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        print(getattr(row, "platform_company"))
        pc = models.PlatformCompany(platform_company=getattr(row, "platform_company"),
                                    platform_model=getattr(row, "platform_model"))
        pc.save()


def initiate_PlatformName():
    file = io.FileIO(file=r".\initializationData\platform\platformName.csv", mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        pn = models.PlatformName(platform_companyId=models.PlatformCompany.objects.get(pk=getattr(row, "platform_companyId")),
                                 platform_serial=getattr(row, "platform_serial"),
                                 platform_name=getattr(row, "platform_name"),
                                 platform_wmo=getattr(row, "platform_wmo"))
        pn.save()


def initiate_PlatformNavigationFirmware():
    file = io.FileIO(file=r".\initializationData\platform\platformNavigationFirmware.csv", mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        pnf = models.PlatformNavigationFirmware(platform_navFirmwareVersion=getattr(row, "platformNavigationFirmware"),
                                                platform_navFirmwareVersionNotes=getattr(row, "platformNavigationFirmwareNotes"))
        pnf.save()


def initiate_PlatformPayload():
    file = io.FileIO(file=r".\initializationData\platform\platformPayload.csv", mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        pp = models.PlatformPayload(platform_payloadSerialNumber=getattr(row, "platformPayloadSerialNumber"),
                                    platform_payloadOriginalPlatform=models.PlatformName.objects.get(pk=getattr(row, "platformPayloadOriginalPlatform")))
        pp.save()


def initiate_PlatformPayloadFirmware():
    file = io.FileIO(file=r".\initializationData\platform\platformPayloadFirmware.csv", mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        ppf = models.PlatformPayloadFirmware(platform_payloadFirmwareVersion=getattr(row, "platformPayloadFirmwareVersion"),
                                             platform_payloadFirmwareVersionNotes=getattr(row, "platformPayloadFirmwareVersionNotes"))
        ppf.save()


def initiate_PlatformBattery():
    file = io.FileIO(file=r".\initializationData\platform\platformBattery.csv", mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        pb = models.PlatformBattery(platform_batteryType=getattr(row, "platformBatteryType"),
                                    platform_batteryGeneration=getattr(row, "platformBatteryGeneration"))
        pb.save()


def initiate_PlatformRelease():
    file = io.FileIO(file=r".\initializationData\platform\platformRelease.csv", mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        pr = models.PlatformRelease(platform_releaseType=getattr(row, "platform_releaseType"),
                                    platform_releaseAttachMethod=getattr(row, "platformReleaseAttachMethod"))
        pr.save()




