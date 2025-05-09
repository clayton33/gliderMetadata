import io
import pandas as pd
from gliderMetadataApp import models


def initiate_Vessel():
#    file = io.FileIO(file=r".\initializationData\misc\vessel02.csv", mode="r")
    file = io.FileIO(file=r".\initializationData\misc\vessel03.csv", mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        ve = models.Vessel(vessel_name=getattr(row, "vessel_name"))
        ve.save()


initiate_Vessel()