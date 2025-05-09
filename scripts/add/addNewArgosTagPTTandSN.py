import io
import operator
import pandas as pd
import re
from gliderMetadataApp import models
# read in file
file = io.FileIO(file=r".\initializationData\argosTag\argosTagPTTAndSerialNumberUpdate01.csv", mode="r")
df = pd.read_csv(file)
for row in df.itertuples():
    # check to see if the PTT is in the database
    agpttQ = models.ArgosTagPTT.objects.filter(argosTag_PTT=getattr(row, 'argosTagPTT'))
    # if not, add it
    if agpttQ.first() is None:
        print(f"Adding new PTT, {getattr(row, 'argosTagPTT')}")
        atp = models.ArgosTagPTT(argosTag_PTT=getattr(row, 'argosTagPTT'))
        atp.save()
    atpttQ = models.ArgosTagPTT.objects.get(argosTag_PTT=getattr(row, 'argosTagPTT'))
    # check if PTT and serial number combo is in database
    atsnQ = models.ArgosTagSerialNumber.objects.filter(argosTag_PTTNumber=atpttQ,
                                                       argosTag_serialNumber=getattr(row, 'argosTagSN'))
    # if not, add it
    if atsnQ.first() is None:
        print(f"Adding new serial number, {getattr(row, 'argosTagSN')} for PTT {getattr(row, 'argosTagPTT')}")
        atsn = models.ArgosTagSerialNumber(argosTag_PTTNumber=atpttQ,
                                           argosTag_serialNumber=getattr(row, 'argosTagSN'))
        atsn.save()
    else:
        print(f"Serial number, {getattr(row, 'argosTagSN')} for PTT {getattr(row, 'argosTagPTT')} already exist.")