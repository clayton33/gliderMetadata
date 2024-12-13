import io
import pandas as pd
from gliderMetadataApp import models


def initiate_ContributingInstitutionMission():
    file = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_contributinginstitutionmission.csv", mode="r")
    df = pd.read_csv(file)
    filem = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_mission.csv", mode="r")
    dfm = pd.read_csv(filem)
    filei = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_institute.csv", mode="r")
    dfi = pd.read_csv(filei)
    filer = io.FileIO(file=r".\initializationData\20241210reload\gliderMetadataApp_role.csv", mode="r")
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

initiate_ContributingInstitutionMission()
