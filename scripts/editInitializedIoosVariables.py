import io
import pandas as pd
from gliderMetadataApp import models

editVariableComments = ['profile_id',
                        'profile_time',
                        'profile_lat',
                        'profile_lon',
                        'time_uv',
                        'lat_uv',
                        'lon_uv',
                        'u',
                        'v']

for var in editVariableComments:
    print(f"Changing comment for {var}")
    i = models.Variable.objects.get(variable_parameterName=var)
    i.variable_parameterNameComment = 'ioosProfile'
    i.save()