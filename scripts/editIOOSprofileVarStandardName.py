import pandas as pd
import yaml
import re
from gliderMetadataApp import models

# profile_time
x = models.Variable.objects.get(variable_parameterName='profile_time',
                                   variable_parameterNameComment='ioosProfile')
xadd = models.VariableCFStandard.objects.get(variable_standardName='time')
x.variable_cfName=xadd
x.save()
# profile_lat
x = models.Variable.objects.get(variable_parameterName='profile_lat',
                                   variable_parameterNameComment='ioosProfile')
xadd = models.VariableCFStandard.objects.get(variable_standardName='latitude')
x.variable_cfName=xadd
x.save()
# profile_lon
x = models.Variable.objects.get(variable_parameterName='profile_lon',
                                   variable_parameterNameComment='ioosProfile')
xadd = models.VariableCFStandard.objects.get(variable_standardName='longitude')
x.variable_cfName=xadd
x.save()
# lat_uv
x = models.Variable.objects.get(variable_parameterName='lat_uv',
                                   variable_parameterNameComment='ioosProfile')
xadd = models.VariableCFStandard.objects.get(variable_standardName='latitude')
x.variable_cfName=xadd
x.save()
# lon_uv
x = models.Variable.objects.get(variable_parameterName='lon_uv',
                                   variable_parameterNameComment='ioosProfile')
xadd = models.VariableCFStandard.objects.get(variable_standardName='longitude')
x.variable_cfName=xadd
x.save()

