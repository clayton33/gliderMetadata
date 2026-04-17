import io
import operator
import numpy as np
import pandas as pd
import re
from gliderMetadataApp import models

m = [['"019"', '182V'],
     ['"021"', '185E'],
     ['"022"', '18XZ'],
     ['"024"', '18X0'],
     ['"032"', '18GV']]

for var in m:
    x = models.PlatformName.objects.get(platform_serial = var[0])
    if not (len(var[1]) == 0):
        y = x.platform_ices
        if y is None:
            x.platform_ices = var[1]
            x.save()