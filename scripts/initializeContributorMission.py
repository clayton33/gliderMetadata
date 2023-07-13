import io
import operator

import pandas as pd
import re
from gliderMetadataApp import models
from scripts import fn_readMissionFile as rmf


def convert_date(date):
    return pd.to_datetime(date.apply(lambda d: str(d)[0:8]), errors='coerce')

df = rmf.readMissionFile()

# ContributionMission table
# PI
contributorPIName = df['PI']
contributorPIfirstName = [x.split(' ')[0] for x in contributorPIName]
contributorPIlastName = [x.split(' ')[1] for x in contributorPIName]
# Operator
contributorOpName = df['Operator']
contributorOpfirstName = [x.split(' ')[0] for x in contributorOpName]
contributorOplastName = [x.split(' ')[1] for x in contributorOpName]
# look into different contributor roles