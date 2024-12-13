import io
import pandas as pd
from gliderMetadataApp import models


def initiate_Institute():
    file = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_institute.csv", mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        ins = models.Institute(institute_name=getattr(row, "institute_name"),
                               institute_vocabulary=getattr(row, "institute_vocabulary"))
        ins.save()

def initiate_ArgosTagPTT():
    file = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_argostagptt.csv", mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        at =  models.ArgosTagPTT(argosTag_PTT=getattr(row, 'argosTag_PTT'))
        at.save()

def initiate_ArgosTagSerialNumber():
    file = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_argostagserialnumber.csv", mode="r")
    df = pd.read_csv(file)
    file2 = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_argostagptt.csv", mode="r")
    df2 = pd.read_csv(file2)
    for row in df.itertuples():
        df2sub = df2[df2["id"] == getattr(row, "argosTag_PTTNumber_id")].iloc[0]
        atptt = models.ArgosTagPTT.objects.get(argosTag_PTT=df2sub['argosTag_PTT'])
        # check if PTT and serial number combo is in database
        atsn = models.ArgosTagSerialNumber(argosTag_PTTNumber=atptt,
                                           argosTag_serialNumber=getattr(row, 'argosTag_serialNumber'))
        atsn.save()



def initiate_Vessel():
    file = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_vessel.csv", mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        ve = models.Vessel(vessel_name=getattr(row, "vessel_name"))
        ve.save()


# initiate_Institute()
# initiate_ArgosTagPTT()
# initiate_ArgosTagSerialNumber()
# initiate_Vessel()