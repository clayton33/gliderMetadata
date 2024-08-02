import io
import re
import pandas as pd
from gliderMetadataApp import models

def updateVariableNerc():
    file = io.FileIO(file=r".\initializationData\variable\OG1NERCVariables.csv")
    df = pd.read_csv(file)
    for row in df.itertuples():
        x = models.VariableNERCStandard.objects.get(variable_nerc_variableName=getattr(row, 'variableName'))
        if not(x is None):
            x.variable_nerc_longName = getattr(row, 'variableLongName')
            x.save()

updateVariableNerc()

