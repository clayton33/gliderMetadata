import io
import pandas as pd
from gliderMetadataApp import models

def initiate_ArgosTagSN():
    file = io.FileIO(file=r".\initializationData\argosTag\argosTagSerialNumber02.csv", mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        cp = models.ArgosTagSerialNumber(argosTag_PTTNumber=models.ArgosTagPTT.objects.get(pk=getattr(row, "argosTagPTT_id")),
                                         argosTag_serialNumber=getattr(row, "argosTagSN"))
        cp.save()

initiate_ArgosTagSN()