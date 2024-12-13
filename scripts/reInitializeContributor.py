import io
import pandas as pd
from gliderMetadataApp import models

def initiate_ContributorPeople():
    file = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_contributorpeople.csv", mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        cp = models.ContributorPeople(contributor_lastName=getattr(row, 'contributor_lastName'),
                                      contributor_firstName=getattr(row, 'contributor_firstName'),
                                      contributor_email=getattr(row, 'contributor_email'))
        cp.save()

def initiate_Role():
    file = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_role.csv", mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        r = models.Role(role_vocabulary=getattr(row, 'role_vocabulary'),
                        role_name=getattr(row, 'role_name'))
        r.save()

def initiate_ContributorMission():
    file = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_contributormission.csv", mode="r")
    df = pd.read_csv(file)
    # only pk calls
    # contributorPeople
    filecp = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_contributorpeople.csv", mode="r")
    dfcp = pd.read_csv(filecp)
    # Role
    filer = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_role.csv", mode="r")
    dfr = pd.read_csv(filer)
    # Mission
    filem = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_mission.csv", mode="r")
    dfm = pd.read_csv(filem)
    for row in df.itertuples():
        dfcpsub=dfcp[dfcp['id'] == getattr(row, 'contributor_missionPerson_id')].iloc[0]
        dfrsub=dfr[dfr['id'] == getattr(row, 'contributor_missionRole_id')].iloc[0]
        dfmsub=dfm[dfm['id'] == getattr(row, 'contributor_mission_id')].iloc[0]
        cp = models.ContributorPeople.objects.get(contributor_lastName=dfcpsub['contributor_lastName'],
                                              contributor_firstName=dfcpsub['contributor_firstName'],
                                              contributor_email=dfcpsub['contributor_email'])
        r = models.Role.objects.get(role_name=dfrsub['role_name'])
        m = models.Mission.objects.get(mission_number=dfmsub['mission_number'],
                                       mission_cruiseNumber=dfmsub['mission_cruiseNumber'])
        cm = models.ContributorMission(contributor_mission=m,
                                       contributor_missionPerson=cp,
                                       contributor_missionRole=r)
        cm.save()

#initiate_ContributorPeople()
#initiate_Role()
#initiate_ContributorMission()