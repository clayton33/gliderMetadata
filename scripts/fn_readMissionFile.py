import io
import pandas as pd

def convert_date(date):
    return pd.to_datetime(date.apply(lambda d: str(d)[0:8]), errors='coerce')

def readMissionFile():
    file = io.FileIO(file=r".\initializationData\GliderMission.xlsx", mode="r")
    dataframe = pd.read_excel(file, skiprows=1)
    # rename some columns
    dataframe = dataframe.rename(columns={"Unnamed: 0": "annualMissionIndex",
                                          "Mission #": "missionNumber",
                                          "# days": "numberOfDays",
                                          "# yo": "numberOfYos",
                                          "# sc profile": "numberOfScienceProfiles",
                                          "# alarm": "numberOfAlarms",
                                          "# alarm OT": "numberOfAlarmsWithOT",
                                          "Science every # yos": "scienceEveryNumberOfYos"})
    # remove special characters from column names
    # space
    dataframe.columns = dataframe.columns.str.replace(r' ', r'', regex=True)
    # '/'
    dataframe.columns = dataframe.columns.str.replace(r'/', '', regex=True)
    # '('
    dataframe.columns = dataframe.columns.str.replace(r'(', '', regex=True)
    # ')'
    dataframe.columns = dataframe.columns.str.replace(r')', '', regex=True)
    # Clean up and remove unnecessary rows
    # 1. Remove rows where 'annualMissionIndex' is NaN
    dataframe = dataframe.dropna(subset=['annualMissionIndex'])
    # Covert dates to something useful
    dataframe['Deploymentdate'] = convert_date(dataframe['Deploymentdate'])
    dataframe['Recoverydate'] = convert_date(dataframe['Recoverydate'])
    dataframe['GPCTDcaldate'] = convert_date(dataframe['GPCTDcaldate'])
    dataframe['GPCTDDOcaldate'] = convert_date(dataframe['GPCTDDOcaldate'])
    dataframe['Rinkocaldate'] = convert_date(dataframe['Rinkocaldate'])
    # dataframe['Ecopuckcaldate'] = convert_date(dataframe['Ecopuckcaldate']) # already in format
    dataframe['LEGATOcaldate'] = convert_date(dataframe['LEGATOcaldate'])
    dataframe['Minifluocaldate'] = convert_date(dataframe['Minifluocaldate'])
    # specify format for some columns
    dataframe = dataframe.astype(dict(ArgosTagPTT=str))
    return dataframe