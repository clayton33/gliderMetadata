import io
import pandas as pd
from gliderMetadataApp import models

def checkNa(x):
    return None if pd.isna(x) else x

def initiate_Mission():
    file = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_mission.csv", mode="r")
    df = pd.read_csv(file)
    # read in files for primary key calls in mission
    # platformName
    filepn = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_platformname.csv", mode="r")
    dfpn = pd.read_csv(filepn)
    # platformNavigationFirmware
    filepnf = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_platformnavigationfirmware.csv",
                mode="r")
    dfpnf = pd.read_csv(filepnf)
    # platformBattery
    filepb = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_platformbattery.csv", mode="r")
    dfpb = pd.read_csv(filepb)
    # platformRelease
    filepr = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_platformrelease.csv", mode="r")
    dfpr = pd.read_csv(filepr)
    # platformPayload
    filepp = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_platformpayload.csv", mode="r")
    dfpp = pd.read_csv(filepp)
    # platformPayloadFirmware
    fileppf = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_platformpayloadfirmware.csv",
                mode="r")
    dfppf = pd.read_csv(fileppf)
    # vessel
    filev = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_vessel.csv", mode="r")
    dfv = pd.read_csv(filev)
    # argosTagSerialNumber (do I need PTT as well ?)
    fileatsn = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_argostagserialnumber.csv",
                 mode="r")
    dfatsn = pd.read_csv(fileatsn)
    # institute
    filei = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_institute.csv", mode="r")
    dfi = pd.read_csv(filei)
    for row in df.itertuples():
        # get pk's
        # platformName
        dfpnsub = dfpn[dfpn["id"] == getattr(row, "mission_platformName_id")].iloc[0]
        pn = models.PlatformName.objects.get(platform_serial=dfpnsub["platform_serial"],
                                             platform_name=dfpnsub["platform_name"],
                                             platform_wmo=dfpnsub["platform_wmo"])
        # check if it was already entered into database
        imQ = models.Mission.objects.filter(mission_platformName=pn,
                                            mission_number=getattr(row, 'mission_number'))
        if imQ.first() is None:
            # platformNavigationFirmware
            if(pd.isna(getattr(row, "mission_platformNavFirmware_id"))):
                pnf = None
            else :
                dfpnfsub = dfpnf[dfpnf["id"] == getattr(row, "mission_platformNavFirmware_id")].iloc[0]
                pnf = models.PlatformNavigationFirmware.objects.get(
                    platform_navFirmwareVersion=dfpnfsub["platform_navFirmwareVersion"])
            # platformBattery
            dfpbsub = dfpb[dfpb["id"] == getattr(row, "mission_platformBattery_id")].iloc[0]
            pb = models.PlatformBattery.objects.get(platform_batteryType=dfpbsub["platform_batteryType"],
                                                    platform_batteryGeneration=dfpbsub["platform_batteryGeneration"])
            # platformRelease
            dfprsub = dfpr[dfpr["id"] == getattr(row, "mission_platformRelease_id")].iloc[0]
            pr = models.PlatformRelease.objects.get(platform_releaseType=dfprsub["platform_releaseType"],
                                                    platform_releaseAttachMethod=dfprsub["platform_releaseAttachMethod"])
            # platformPayload
            dfppsub = dfpp[dfpp["id"] == getattr(row, "mission_platformPayload_id")].iloc[0]
            pp = models.PlatformPayload.objects.get(platform_payloadSerialNumber=dfppsub["platform_payloadSerialNumber"])
            # platformPayloadFirmware
            dfppfsub = dfppf[dfppf["id"] == getattr(row, "mission_platformPayloadFirmware_id")].iloc[0]
            ppf = models.PlatformPayloadFirmware.objects.get(
                platform_payloadFirmwareVersion=dfppfsub["platform_payloadFirmwareVersion"])
            # vessel
            ## deployment
            if(pd.isna(getattr(row, "mission_deploymentVessel_id"))):
                vd = None
            else :
                dfvd = dfv[dfv["id"] == getattr(row, "mission_deploymentVessel_id")].iloc[0]
                vd = models.Vessel.objects.get(vessel_name=dfvd["vessel_name"])
            ## recovery
            if(pd.isna(getattr(row, "mission_recoveryVessel_id"))):
                vr = None
            else :
                dfvr = dfv[dfv["id"] == getattr(row, "mission_recoveryVessel_id")].iloc[0]
                vr = models.Vessel.objects.get(vessel_name=dfvr["vessel_name"])
            # argosTagSerialNumber
            dfatsnsub = dfatsn[dfatsn["id"] == getattr(row, "mission_argosTag_id")].iloc[0]
            atsn = models.ArgosTagSerialNumber.objects.get(argosTag_serialNumber=dfatsnsub["argosTag_serialNumber"])
            # institute - created a new table, contributing institution mission, don't need this anymore
            # dfisub = dfi[dfi["id"] == getattr(row, "mission_institute_id")].iloc[0]
            # i = models.Institute.objects.get(institute_name=dfisub["institute_name"])
            # initialize mission
            im = models.Mission(mission_platformName=pn,
                                mission_number=checkNa(getattr(row, 'mission_number')),
                                mission_cruiseNumber=checkNa(getattr(row, 'mission_cruiseNumber')),
                                mission_platformNavFirmware=pnf,
                                mission_platformBattery=pb,
                                mission_platformRelease=pr,
                                mission_platformPayload=pp,
                                mission_platformPayloadFirmware=ppf,
                                mission_deploymentDate=checkNa(getattr(row, 'mission_deploymentDate')),
                                mission_recoveryDate=checkNa(getattr(row, 'mission_recoveryDate')),
                                mission_batteryMax=checkNa(getattr(row, 'mission_batteryMax')),
                                mission_batteryMin=checkNa(getattr(row, 'mission_batteryMin')),
                                mission_deploymentVessel=vd,
                                mission_deploymentLongitude=checkNa(getattr(row, 'mission_deploymentLongitude')),
                                mission_deploymentLatitude=checkNa(getattr(row, 'mission_deploymentLatitude')),
                                mission_recoveryVessel=vr,
                                mission_recoveryLongitude=checkNa(getattr(row, 'mission_recoveryLongitude')),
                                mission_recoveryLatitude=checkNa(getattr(row, 'mission_recoveryLatitude')),
                                mission_minimumLongitude=checkNa(getattr(row, 'mission_minimumLongitude')),
                                mission_minimumLatitude=checkNa(getattr(row, 'mission_minimumLatitude')),
                                mission_maximumLongitude=checkNa(getattr(row, 'mission_maximumLongitude')),
                                mission_maximumLatitude=checkNa(getattr(row, 'mission_maximumLatitude')),
                                mission_waypointsGiven=checkNa(getattr(row, 'mission_waypointsGiven')),
                                mission_distanceTravelled=checkNa(getattr(row, 'mission_distanceTravelled')),
                                mission_numberOfYos=checkNa(getattr(row, 'mission_numberOfYos')),
                                mission_numberOfScienceYos=checkNa(getattr(row, 'mission_numberOfScienceYos')),
                                mission_profilingScheme=checkNa(getattr(row, 'mission_profilingScheme')),
                                mission_numberOfAlarms=checkNa(getattr(row, 'mission_numberOfAlarms')),
                                mission_numberOfAlarmsWithOT=checkNa(getattr(row, 'mission_numberOfAlarmsWithOT')),
                                mission_hoursOfOT=checkNa(getattr(row, 'mission_hoursOfOT')),
                                mission_ballastedDensity=checkNa(getattr(row, 'mission_ballastedDensity')),
                                mission_argosTag=atsn,
                                mission_institute=None,
                                mission_comments=checkNa(getattr(row, 'mission_comments'))
                                )
            im.save()
        else:
            print(
                f"There is already a mission for glider {imQ.first().mission_platformName.platform_name} mission {getattr(row, 'mission_number')}, "
                f"proceeding to next mission.")

initiate_Mission()