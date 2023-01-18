from django.db import models


class PlatformCompany(models.Model):
    platform_company = models.CharField(max_length=50, null=True)
    platform_model = models.CharField(max_length=50, null=True)


class PlatformName(models.Model):
    platform_companyId = models.ForeignKey(PlatformCompany, on_delete=models.SET_NULL, null=True)
    platform_serial = models.CharField(max_length=6, null=True)
    platform_name = models.CharField(max_length=20, null=True)
    platform_wmo = models.IntegerField(null=True)


class PlatformMaintenance(models.Model):
    platform_nameId = models.ForeignKey(PlatformName, on_delete=models.SET_NULL, null=True)
    platform_maintenanceDate = models.DateField(null=True)
    platform_maintenanceComments = models.CharField(max_length=200, null=True)


class PlatformNavigationFirmware(models.Model):
    platform_navFirmwareVersion = models.CharField(max_length=20, null=True)
    platform_navFirmwareComments = models.CharField(max_length=100, null=True)


# not sure about this table. might reinstate it if we decide knowing the date the firmware was upgraded is important.
# class PlatformFirmwareUpgrade(models.Model):
#     platform_maintenance = models.ForeignKey(PlatformMaintenance, on_delete=models.SET_NULL, null=True)
#     platform_navFirmware = models.ForeignKey(PlatformNavigationFirmware, on_delete=models.SET_NULL, null=True)
#     platform_navFirmwareUpgradeDate = models.DateField(null=True)


class PlatformPayload(models.Model):
    platform_payloadSerialNumber = models.CharField(max_length=10, null=True)
    platform_payloadOriginalPlatform = models.ForeignKey(PlatformName, on_delete=models.SET_NULL, null=True)


class PlatformPayloadFirmware(models.Model):
    platform_payloadFirmwareVersion = models.CharField(max_length=20, null=True)
    platform_payloadFirmwareVersionComments = models.CharField(max_length=200, null=True)


# same as PlatformFirmwareUpgrade. might reinstate it if we decide knowing the date the firmware
# was upgraded is important.
# class PlatformPayloadFirmwareUpgrade(models.Model):
#     platform_payload = models.ForeignKey(PlatformPayload, on_delete=models.SET_NULL, null=True)
#     platform_payloadFirmware = models.ForeignKey(PlatformPayloadFirmware, on_delete=models.SET_NULL, null=True)
#     platform_payloadFirmwareUpgradeDate = models.DateField(null=True)


class PlatformBattery(models.Model):
    platform_batteryType = models.CharField(max_length=50, null=True)
    platform_batteryGeneration = models.CharField(max_length=10, null=True)  # might not be CharField ?


class PlatformRelease(models.Model):
    platform_releaseType = models.CharField(max_length=20, null=True)
    platform_releaseAttachMethod = models.CharField(max_length=20, null=True)


# might not need this since one platform is associated with each mission
# class PlatformMission(models.Model):
#     platform_missionFirmware = models.ForeignKey(PlatformFirmwareUpgrade, on_delete=models.SET_NULL, null=True)
#     platform_missionPayloadFirmware = models.ForeignKey(PlatformPayloadFirmwareUpgrade, on_delete=models.SET_NULL,
#                                                         null=True)
#     platform_missionBattery = models.ForeignKey(PlatformBattery, on_delete=models.SET_NULL, null=True)
#     platform_missionRelease = models.ForeignKey(PlatformRelease, on_delete=models.SET_NULL, null=True)
#     # platform_missionId = models.ForeignKey(Mission)  # not yet created


class InstrumentMake(models.Model):
    instrument_make = models.CharField(max_length=50)


class InstrumentType(models.Model):
    instrument_type = models.CharField(max_length=50)


class InstrumentModel(models.Model):
    instrument_modelMake = models.ForeignKey(InstrumentMake, on_delete=models.SET_NULL, null=True)
    instrument_modelType = models.ForeignKey(InstrumentType, on_delete=models.SET_NULL, null=True)
    instrument_model = models.CharField(max_length=50)
    instrument_longname = models.CharField(max_length=100)  # should check how long they can get


class InstrumentSerialNumber(models.Model):
    instrument_serialNumberModel = models.ForeignKey(InstrumentModel, on_delete=models.SET_NULL, null=True)
    instrument_originalPlatform = models.ForeignKey(PlatformName, on_delete=models.SET_NULL, null=True)
    instrument_serialNumber = models.CharField(max_length=20)


class InstrumentCalibration(models.Model):
    instrument_calibrationSerial = models.ForeignKey(InstrumentSerialNumber, on_delete=models.SET_NULL, null=True)
    instrument_calibrationDate = models.DateField(null=True)
    instrument_calibrationReport = models.CharField(max_length=200)
    instrument_calibrationReportNotes = models.CharField(max_length=20, null=True)
    instrument_calibrationDateNotes = models.CharField(max_length=50, null=True)


# might move this one to the end with PlatformMission
class InstrumentMission(models.Model):
    instrument_calibration = models.ForeignKey(InstrumentCalibration, on_delete=models.SET_NULL, null=True)
    instrument_warmUp = models.CharField(max_length=20)
    instrument_samplingRate = models.CharField(max_length=20)
    # instrument_mission = models.ForeignKey(Mission)  # not yet created


class ContributorPeople(models.Model):
    contributor_lastName = models.CharField(max_length=50)
    contributor_firstName = models.CharField(max_length=50)
    contributor_email = models.CharField(max_length=50)


class ContributorRole(models.Model):
    contributor_role = models.CharField(max_length=50)


class Institute(models.Model):
    institute_name = models.CharField(max_length=100)
    institute_agency = models.CharField(max_length=100)
    institute_city = models.CharField(max_length=50)
    institute_country = models.CharField(max_length=50)


class ArgosTag(models.Model):
    argosTag_PTT = models.CharField(max_length=20)
    argosTag_serialNumber = models.CharField(max_length=10)


class Vessel(models.Model):
    vessel_name = models.CharField(max_length=50)