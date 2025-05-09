import io
import pandas as pd
from gliderMetadataApp import models


def initiate_ContributingInstitutionMission(path):
    filename = "gliderMetadataApp_contributinginstitutionmission.csv"
    pathfile = path + '/' + filename
    file = io.FileIO(file=pathfile, mode="r")
    df = pd.read_csv(file)
    # Mission
    filenamem = "gliderMetadataApp_mission.csv"
    pathfilem = path + '/' + filenamem
    filem = io.FileIO(file=pathfilem, mode="r")
    dfm = pd.read_csv(filem)
    # Institute
    filenamei = "gliderMetadataApp_institute.csv"
    pathfilei = path + '/' + filenamei
    filei = io.FileIO(file=pathfilei, mode="r")
    dfi = pd.read_csv(filei)
    # Role
    filenamer = "gliderMetadataApp_role.csv"
    pathfiler = path + '/' + filenamer
    filer = io.FileIO(file=filenamer, mode="r")
    dfr = pd.read_csv(filer)
    for row in df.itertuples():
        dfmsub = dfm[dfm['id'] == getattr(row, 'contributingInstitution_mission_id')].iloc[0]
        dfisub = dfi[dfi['id'] == getattr(row, 'contributingInstitution_missionInstitute_id')].iloc[0]
        dfrsub = dfr[dfr['id'] == getattr(row, 'contributingInstitution_missionRole_id')].iloc[0]
        m = models.Mission.objects.get(mission_number=dfmsub['mission_number'],
                                       mission_cruiseNumber=dfmsub['mission_cruiseNumber'])
        i = models.Institute.objects.get(institute_name=dfisub['institute_name'])
        r = models.Role.objects.get(role_name=dfrsub['role_name'])
        cim = models.ContributingInstitutionMission(contributingInstitution_mission=m,
                                                    contributingInstitution_missionInstitute=i,
                                                    contributingInstitution_missionRole=r)
        cim.save()