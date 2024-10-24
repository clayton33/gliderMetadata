from django.db import models

class Vocabulary(models.Model):
    vocabulary_name = models.CharField(max_length=100, null=False)
    vocabulary_note = models.CharField(max_length=50, null=True)


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


class InstrumentSeabird43FOxygenCalibrationCoefficients(models.Model):
    calibrationSeaBird43F_calibration = models.ForeignKey(InstrumentCalibration, on_delete=models.SET_NULL, null = True)
    calibrationSeaBird43F_Soc = models.DecimalField(max_digits=10, decimal_places=8)
    calibrationSeaBird43F_Foffset = models.DecimalField(max_digits=6, decimal_places=2)
    calibrationSeaBird43F_Tau20 = models.DecimalField(max_digits=4, decimal_places=2)
    calibrationSeaBird43F_A = models.DecimalField(max_digits=7, decimal_places=5)
    calibrationSeaBird43F_B = models.DecimalField(max_digits=8, decimal_places=6)
    calibrationSeaBird43F_C = models.DecimalField(max_digits=12, decimal_places=10)
    calibrationSeaBird43F_Enom = models.DecimalField(max_digits=5, decimal_places=3)

class ContributorPeople(models.Model):
    contributor_lastName = models.CharField(max_length=50)
    contributor_firstName = models.CharField(max_length=50)
    contributor_email = models.CharField(max_length=50)


class Role(models.Model):
    role_vocabulary = models.CharField(max_length=200)
    role_name = models.CharField(max_length=50)


class VariableCFStandard(models.Model):
    variable_nameVocabulary = models.ForeignKey(Vocabulary, on_delete=models.SET_NULL, null=True)
    variable_standardName = models.CharField(max_length=100)


class VariableNERCStandard(models.Model):
    variable_nerc_variableName = models.CharField(max_length=100, null=True)
    variable_nerc_variableLongName = models.CharField(max_length=200, null=True)
    variable_nerc_variableVocabulary = models.CharField(max_length=100, null=True)
    variable_nerc_unit = models.CharField(max_length=50, null=True)
    variable_nerc_unitLongName = models.CharField(max_length=100, null=True)
    variable_nerc_unitVocabulary = models.CharField(max_length=100, null=True)


class UnitCFStandard(models.Model):
    variable_nameVocabulary = models.ForeignKey(Vocabulary, on_delete=models.SET_NULL, null=True)
    variable_unit = models.CharField(max_length=25)


class Variable(models.Model):
    variable_parameterName = models.CharField(max_length=50)
    variable_longName = models.CharField(max_length=75)
    variable_parameterNameComment = models.CharField(max_length=50, null=True)
    variable_cfName = models.ForeignKey(VariableCFStandard, on_delete=models.SET_NULL, null=True)
    variable_cfUnit = models.ForeignKey(UnitCFStandard, on_delete=models.SET_NULL, null=True)
    variable_nercName = models.ForeignKey(VariableNERCStandard, on_delete=models.SET_NULL, null=True)


class InstrumentVariable(models.Model):
    instrument_variablePlatformCompany = models.ForeignKey(PlatformCompany, on_delete=models.SET_NULL, null=True)
    instrument_variableInstrumentModel = models.ForeignKey(InstrumentModel, on_delete=models.SET_NULL, null=True)
   # instrument_variableStandardName = models.ForeignKey(Variable, on_delete=models.SET_NULL, null=True)
    instrument_nercVariable = models.ForeignKey(VariableNERCStandard, on_delete=models.SET_NULL, null=True)
    instrument_cfVariable = models.ForeignKey(VariableCFStandard, on_delete=models.SET_NULL, null=True)
    instrument_variableSourceName = models.CharField(max_length=50)
    instrument_variableSourceUnits = models.CharField(max_length=50, null=True)
    instrument_gcmdKeyword = models.CharField(max_length=200, null=True)
    instrument_accuracy = models.DecimalField(max_digits=12, decimal_places=6, null=True)
    instrument_precision = models.DecimalField(max_digits=12, decimal_places=6, null=True)
    instrument_resolution = models.DecimalField(max_digits=12, decimal_places=6, null=True)
    instrument_validMin = models.DecimalField(max_digits=12, decimal_places=6, null=True)
    instrument_validMax = models.DecimalField(max_digits=12, decimal_places=6, null=True)


class PlatformVariable(models.Model):
    platform_variablePlatformCompany = models.ForeignKey(PlatformCompany, on_delete=models.SET_NULL, null=True)
    platform_nercVariable = models.ForeignKey(VariableNERCStandard, on_delete=models.SET_NULL, null=True)
    platform_cfVariable = models.ForeignKey(VariableCFStandard, on_delete=models.SET_NULL, null=True)
    platform_variableSourceName = models.CharField(max_length=50)
    platform_variableSourceUnits = models.CharField(max_length=50, null=True)


class Institute(models.Model):
    institute_name = models.CharField(max_length=100)
    institute_vocabulary = models.CharField(max_length=200)


class ArgosTagPTT(models.Model):
    argosTag_PTT = models.CharField(max_length=20)


class ArgosTagSerialNumber(models.Model):
    argosTag_PTTNumber = models.ForeignKey(ArgosTagPTT, on_delete=models.SET_NULL, null=True)
    argosTag_serialNumber = models.CharField(max_length=10)


class Vessel(models.Model):
    vessel_name = models.CharField(max_length=50)


class Mission(models.Model):
    mission_platformName = models.ForeignKey(PlatformName, on_delete=models.SET_NULL, null=True)
    mission_number = models.IntegerField()
    mission_cruiseNumber = models.CharField(max_length=20)
    mission_platformNavFirmware = models.ForeignKey(PlatformNavigationFirmware, on_delete=models.SET_NULL, null=True)
    mission_platformBattery = models.ForeignKey(PlatformBattery, on_delete=models.SET_NULL, null=True)
    mission_platformRelease = models.ForeignKey(PlatformRelease, on_delete=models.SET_NULL, null=True)
    mission_platformPayload = models.ForeignKey(PlatformPayload, on_delete=models.SET_NULL, null=True)
    mission_platformPayloadFirmware = models.ForeignKey(PlatformPayloadFirmware, on_delete=models.SET_NULL, null=True)
    mission_deploymentDate = models.DateField(null=True)
    mission_recoveryDate = models.DateField(null=True)
    mission_batteryMax = models.DecimalField(max_digits=3, decimal_places=1)
    mission_batteryMin = models.DecimalField(max_digits=3, decimal_places=1)
    mission_deploymentVessel = models.ForeignKey(Vessel, related_name='deploymentVessel', on_delete=models.SET_NULL, null=True)
    mission_deploymentLongitude = models.DecimalField(max_digits=7, decimal_places=4)
    mission_deploymentLatitude = models.DecimalField(max_digits=6, decimal_places=4)
    mission_recoveryVessel = models.ForeignKey(Vessel, related_name='recoveryVessel', on_delete=models.SET_NULL, null=True)
    mission_recoveryLongitude = models.DecimalField(max_digits=7, decimal_places=4, null=True)
    mission_recoveryLatitude = models.DecimalField(max_digits=6, decimal_places=4, null=True)
    mission_minimumLongitude = models.DecimalField(max_digits=7, decimal_places=4, null=True)
    mission_minimumLatitude = models.DecimalField(max_digits=6, decimal_places=4, null=True)
    mission_maximumLongitude = models.DecimalField(max_digits=7, decimal_places=4, null=True)
    mission_maximumLatitude = models.DecimalField(max_digits=6, decimal_places=4, null=True)
    mission_waypointsGiven = models.CharField(max_length=100)
    mission_distanceTravelled = models.DecimalField(max_digits=6, decimal_places=2)
    mission_numberOfYos = models.IntegerField()
    mission_numberOfScienceYos = models.CharField(max_length=20)
    mission_profilingScheme = models.CharField(max_length=20)
    mission_numberOfAlarms = models.CharField(max_length=5)
    mission_numberOfAlarmsWithOT = models.IntegerField()
    mission_hoursOfOT = models.IntegerField()
    mission_ballastedDensity = models.DecimalField(max_digits=6, decimal_places=2)
    mission_argosTag = models.ForeignKey(ArgosTagSerialNumber, on_delete=models.SET_NULL, null=True)
    mission_institute = models.ForeignKey(Institute, on_delete=models.SET_NULL, null=True)
    mission_comments = models.CharField(max_length=300)
    mission_summary = models.CharField(max_length=1200, null=True)
    mission_network = models.CharField(max_length=1500, null=True)
    mission_project = models.CharField(max_length=300, null=True)


class InstrumentMission(models.Model):
    instrument_mission = models.ForeignKey(Mission, on_delete=models.SET_NULL, null=True)
    instrument_calibration = models.ForeignKey(InstrumentCalibration, on_delete=models.SET_NULL, null=True)
    instrument_warmUp = models.CharField(max_length=20)
    instrument_samplingRate = models.CharField(max_length=20)


class ContributorMission(models.Model):
    contributor_mission = models.ForeignKey(Mission, on_delete=models.SET_NULL, null=True)
    contributor_missionPerson = models.ForeignKey(ContributorPeople, on_delete=models.SET_NULL, null=True)
    contributor_missionRole = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

class ContributingInstitutionMission(models.Model):
    contributingInstitution_mission = models.ForeignKey(Mission, on_delete=models.SET_NULL, null=True)
    contributingInstitution_missionRole = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    contributingInstitution_missionInstitute = models.ForeignKey(Institute, on_delete=models.SET_NULL, null=True)