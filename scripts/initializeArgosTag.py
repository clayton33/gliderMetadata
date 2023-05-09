import io
import pandas as pd
from gliderMetadataApp import models

def initiate_ArgosTagPTT():
    file = io.FileIO(file=r".\initializationData\argosTag\argosTagPTT.csv", mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        cp = models.ArgosTagPTT(argosTag_PTT=getattr(row, "argosTag_PTT"))
        cp.save()


def initiate_ArgosTagSN():
    file = io.FileIO(file=r".\initializationData\argosTag\argosTagSerialNumber.csv", mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        cp = models.ArgosTagSerialNumber(argosTag_PTTNumber=models.ArgosTagPTT.objects.get(pk=getattr(row, "argosTagPTT_id")),
                                         argosTag_serialNumber=getattr(row, "argosTagSN"))
        cp.save()

initiate_ArgosTagPTT()
initiate_ArgosTagSN()