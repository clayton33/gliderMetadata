import io
import pandas as pd
from gliderMetadataApp import models


def initiate_ContributorPeople():
    file = io.FileIO(file=r".\initializationData\contributor\contributorPeople.csv", mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        cp = models.ContributorPeople(contributor_lastName=getattr(row, "contributor_lastName"),
                                      contributor_firstName=getattr(row, "contributor_firstName"),
                                      contributor_email=getattr(row, "contributor_email"))

        cp.save()


def initiate_ContributorRole():
    file = io.FileIO(file=r".\initializationData\contributor\contributorRole.csv", mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        cr = models.ContributorRole(contributor_vocabulary = models.Vocabulary.objects.get(pk=getattr(row, 'contributor_vocabulary')),
                                    contributor_role=getattr(row, "contributor_role"))
        cr.save()



initiate_ContributorPeople()
initiate_ContributorRole()
