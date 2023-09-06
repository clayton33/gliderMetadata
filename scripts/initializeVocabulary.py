import io
import pandas as pd
from gliderMetadataApp import models


def initiate_Vocabulary():
    file = io.FileIO(file=r".\initializationData\vocabulary\vocabulary.csv", mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        v = models.Vocabulary(vocabulary_name=getattr(row, "vocabulary_name"),
                                     vocabulary_note=getattr(row, "vocabulary_notes"))

        v.save()

initiate_Vocabulary()