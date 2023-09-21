from gliderMetadataApp import models

# I'm going to prioritize ioos vars, so if I know there is one, i'll use that, if not, argo
# going kind of in order of variable_instrument.csv/variable_platform.csv
# GPCTD/LEGATO
# temperature
varpk = models.Variable.objects.get(variable_parameterName='temperature')
i = models.InstrumentVariable.objects.get(instrument_variableSourceName='GPCTD_TEMPERATURE')
i.instrument_variableStandardName = varpk
i.save()
i = models.InstrumentVariable.objects.get(instrument_variableSourceName='LEGATO_TEMPERATURE')
i.instrument_variableStandardName = varpk
i.save()
# conductivity
varpk = models.Variable.objects.get(variable_parameterName='conductivity')
i = models.InstrumentVariable.objects.get(instrument_variableSourceName='GPCTD_CONDUCTIVITY')
i.instrument_variableStandardName = varpk
i.save()
i = models.InstrumentVariable.objects.get(instrument_variableSourceName='LEGATO_CONDUCTIVITY')
i.instrument_variableStandardName = varpk
i.save()
# salinity
varpk = models.Variable.objects.get(variable_parameterName='salinity')
i = models.InstrumentVariable.objects.get(instrument_variableSourceName='LEGATO_SALINITY')
i.instrument_variableStandardName = varpk
i.save()
# pressure
varpk = models.Variable.objects.get(variable_parameterName='pressure')
i = models.InstrumentVariable.objects.get(instrument_variableSourceName='GPCTD_PRESSURE')
i.instrument_variableStandardName = varpk
i.save()
i = models.InstrumentVariable.objects.get(instrument_variableSourceName='LEGATO_PRESSURE')
i.instrument_variableStandardName = varpk
i.save()
# oxygen
varpk = models.Variable.objects.get(variable_parameterName='FREQUENCY_DOXY')
i = models.InstrumentVariable.objects.get(instrument_variableSourceName='GPCTD_DOF')
i.instrument_variableStandardName = varpk
i.save()
# ecopuck
# chl a count
varpk = models.Variable.objects.get(variable_parameterName='FLUORESCENCE_CHLA')
i = models.InstrumentVariable.objects.get(instrument_variableSourceName='FLBBCD_CHL_COUNT')
i.instrument_variableStandardName = varpk
i.save()
# chl a
varpk = models.Variable.objects.get(variable_parameterName='CHLA')
i = models.InstrumentVariable.objects.get(instrument_variableSourceName='FLBBCD_CHL_SCALED')
i.instrument_variableStandardName = varpk
i.save()
# backscatter700 count - none might be beta_backscattering700
# backscatter700
varpk = models.Variable.objects.get(variable_parameterName='BBP700')
i = models.InstrumentVariable.objects.get(instrument_variableSourceName='FLBBCD_BB_700_SCALED')
i.instrument_variableStandardName = varpk
i.save()
# cdom count
varpk = models.Variable.objects.get(variable_parameterName='FLUORESCENCE_CDOM')
i = models.InstrumentVariable.objects.get(instrument_variableSourceName='FLBBCD_CDOM_COUNT')
i.instrument_variableStandardName = varpk
i.save()
# cdom
varpk = models.Variable.objects.get(variable_parameterName='CDOM')
i = models.InstrumentVariable.objects.get(instrument_variableSourceName='FLBBCD_CDOM_SCALED')
i.instrument_variableStandardName = varpk
i.save()
# optical oxygen
# oxygen temperature
varpk = models.Variable.objects.get(variable_parameterName='TEMP_DOXY')
i = models.InstrumentVariable.objects.get(instrument_variableSourceName='AROD_FT_TEMP')
i.instrument_variableStandardName = varpk
i.save()
# oxygen concentration
varpk = models.Variable.objects.get(variable_parameterName='DOXY')
i = models.InstrumentVariable.objects.get(instrument_variableSourceName='AROD_FT_DO')
i.instrument_variableStandardName = varpk
i.save()
# glider navigation params
# heading, pitch, roll
varpk = models.Variable.objects.get(variable_parameterName='platform_orientation')
i = models.PlatformVariable.objects.get(platform_variableSourceName='Heading')
i.platform_variableStandardName = varpk
i.save()
varpk = models.Variable.objects.get(variable_parameterName='platform_pitch')
i = models.PlatformVariable.objects.get(platform_variableSourceName='Pitch')
i.platform_variableStandardName = varpk
i.save()
varpk = models.Variable.objects.get(variable_parameterName='platform_roll')
i = models.PlatformVariable.objects.get(platform_variableSourceName='Roll')
i.platform_variableStandardName = varpk
i.save()
# longitude and latitude
varpk = models.Variable.objects.get(variable_parameterName='lon')
i = models.PlatformVariable.objects.get(platform_variableSourceName='NAV_LONGITUDE')
i.platform_variableStandardName = varpk
i.save()
varpk = models.Variable.objects.get(variable_parameterName='lat')
i = models.PlatformVariable.objects.get(platform_variableSourceName='NAV_LATITUDE')
i.platform_variableStandardName = varpk
i.save()
# time
varpk = models.Variable.objects.get(variable_parameterName='time')
i = models.PlatformVariable.objects.get(platform_variableSourceName='Timestamp')
i.platform_variableStandardName = varpk
i.save()