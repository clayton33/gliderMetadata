import io
import pandas as pd
from gliderMetadataApp import models


def initiate_ContributorPeople():
    file = io.FileIO(file=r".\initializationData\contributor\contributorPeople2.csv", mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        cp = models.ContributorPeople(contributor_lastName=getattr(row, "contributor_lastName"),
                                      contributor_firstName=getattr(row, "contributor_firstName"),
                                      contributor_email=getattr(row, "contributor_email"))

        cp.save()

initiate_ContributorPeople()