import io
import pandas as pd
from gliderMetadataApp import models

def initiate_ContributorPeople(path):
    filename = "gliderMetadataApp_contributorpeople.csv"
    pathfile = path + '/' + filename
    file = io.FileIO(file=pathfile, mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        cp = models.ContributorPeople(contributor_lastName=getattr(row, 'contributor_lastName'),
                                      contributor_firstName=getattr(row, 'contributor_firstName'),
                                      contributor_email=getattr(row, 'contributor_email'))
        cp.save()

def initiate_Role(path):
    filename = "gliderMetadataApp_role.csv"
    pathfile = path + '/' + filename
    file = io.FileIO(file=pathfile, mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        r = models.Role(role_vocabulary=getattr(row, 'role_vocabulary'),
                        role_name=getattr(row, 'role_name'))
        r.save()

def initiate_ContributorMission(path):
    filename = "gliderMetadataApp_contributormission.csv"
    pathfile = path + '/' + filename
    file = io.FileIO(file=pathfile, mode="r")
    df = pd.read_csv(file)
    # only pk calls
    # contributorPeople
    filenamecp = "gliderMetadataApp_contributorpeople.csv"
    pathfilecp = path + '/' + filenamecp
    filecp = io.FileIO(file=pathfilecp, mode="r")
    dfcp = pd.read_csv(filecp)
    # Role
    filenamer = "gliderMetadataApp_role.csv"
    pathfiler = path + '/' + filenamer
    filer = io.FileIO(file=pathfiler, mode="r")
    dfr = pd.read_csv(filer)
    # Mission
    filenamem = "gliderMetadataApp_mission.csv"
    pathfilem = path + '/' + filenamem
    filem = io.FileIO(file=pathfilem, mode="r")
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