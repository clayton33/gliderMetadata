import io
import pandas as pd
from gliderMetadataApp import models

def checkNa(x):
    return None if pd.isna(x) else x

def initiate_Vocabulary(path):
    filename = "gliderMetadataApp_vocabulary.csv"
    pathfile = path + '/' + filename
    file = io.FileIO(file=pathfile, mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        v = models.Vocabulary(vocabulary_name=getattr(row, 'vocabulary_name'),
                              vocabulary_note=getattr(row, 'vocabulary_note'))
        v.save()

def initiate_UnitCFStandard(path):
    filename = "gliderMetadataApp_unitcfstandard.csv"
    pathfile = path + '/' + filename
    file = io.FileIO(file=pathfile, mode="r")
    df = pd.read_csv(file)
    filenamev = "gliderMetadataApp_vocabulary.csv"
    pathfilev = path + '/' + filenamev
    filev = io.FileIO(file=pathfilev, mode="r")
    dfv = pd.read_csv(filev)
    for row in df.itertuples():
        dfvsub = dfv[dfv['id'] == getattr(row, 'variable_nameVocabulary_id')].iloc[0]
        v = models.Vocabulary.objects.get(vocabulary_name=dfvsub['vocabulary_name'])
        us = models.UnitCFStandard(variable_nameVocabulary=v,
                                   variable_unit=getattr(row, 'variable_unit'))
        us.save()

def initiate_VariableCFStandard(path):
    filename = "gliderMetadataApp_variablecfstandard.csv"
    pathfile = path + '/' + filename
    file = io.FileIO(file=pathfile, mode="r")
    df = pd.read_csv(file)
    filenamev = "gliderMetadataApp_vocabulary.csv"
    pathfilev = path + '/' + filenamev
    filev = io.FileIO(file=pathfilev, mode="r")
    dfv = pd.read_csv(filev)
    for row in df.itertuples():
        dfvsub = dfv[dfv['id'] == getattr(row, 'variable_nameVocabulary_id')].iloc[0]
        v = models.Vocabulary.objects.get(vocabulary_name=dfvsub['vocabulary_name'])
        vs = models.VariableCFStandard(variable_nameVocabulary=v,
                                       variable_standardName=getattr(row, 'variable_standardName'))
        vs.save()

def initiate_VariableNERCStandard(path):
    filename = "gliderMetadataApp_variablenercstandard.csv"
    pathfile = path + '/' + filename
    file = io.FileIO(file=pathfile, mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        vn = models.VariableNERCStandard(variable_nerc_unit=getattr(row, 'variable_nerc_unit'),
                                         variable_nerc_unitLongName=getattr(row, 'variable_nerc_unitLongName'),
                                         variable_nerc_unitVocabulary=getattr(row, 'variable_nerc_unitVocabulary'),
                                         variable_nerc_variableLongName=getattr(row, 'variable_nerc_variableLongName'),
                                         variable_nerc_variableName=getattr(row, 'variable_nerc_variableName'),
                                         variable_nerc_variableVocabulary=getattr(row, 'variable_nerc_variableVocabulary')
                                         )
        vn.save()

def initiate_Variable(path):
    filename = "gliderMetadataApp_variable_mod.csv"
    pathfile = path + '/' + filename
    file = io.FileIO(file=pathfile, mode="r")
    df = pd.read_csv(file)
    # cf variable
    filenamevcs = "gliderMetadataApp_variablecfstandard.csv"
    pathfilevcs = path + '/' + filenamevcs
    filevcs = io.FileIO(file=pathfilevcs, mode="r")
    dfvcs = pd.read_csv(filevcs)
    # cf unit
    filenamevcu = "gliderMetadataApp_unitcfstandard.csv"
    pathfilevcu = path + '/' + filenamevcu
    filevcu = io.FileIO(file=pathfilevcu, mode="r")
    dfvcu = pd.read_csv(filevcu)
    # nerc variable
    filenamevns = "gliderMetadataApp_variablenercstandard.csv"
    pathfilevns = path + '/' + filenamevns
    filevns = io.FileIO(file=pathfilevns, mode="r")
    dfvns = pd.read_csv(filevns)
    for row in df.itertuples():
        # cfVariable
        dfvcssub = dfvcs[dfvcs['id'] == getattr(row, 'variable_cfName_id')]
        if dfvcssub.empty:
            vcs = None
        else:
            dfvcssub = dfvcssub.iloc[0]
            vcs = models.VariableCFStandard.objects.get(variable_standardName=dfvcssub['variable_standardName'])
        # cfUnit
        dfvcusub = dfvcu[dfvcu['id'] == getattr(row, 'variable_cfUnit_id')]
        if dfvcusub.empty:
            vcu = None
        else:
            dfvcusub = dfvcusub.iloc[0]
            vcu = models.UnitCFStandard.objects.get(variable_unit=dfvcusub['variable_unit'])
        # nercVariable
        dfvnssub = dfvns[dfvns['id'] == getattr(row, 'variable_nercName_id')]
        if dfvnssub.empty:
            vns = None
        else:
            dfvnssub = dfvnssub.iloc[0]
            vns = models.VariableNERCStandard.objects.get(variable_nerc_variableName=dfvnssub['variable_nerc_variableName'])
        iv = models.Variable(variable_parameterName = checkNa(getattr(row, 'variable_parameterName')),
                             variable_longName = checkNa(getattr(row, 'variable_longName')),
                             variable_parameterNameComment = checkNa(getattr(row, 'variable_parameterNameComment')),
                             variable_cfName = vcs,
                             variable_cfUnit = vcu,
                             variable_nercName = vns)
        iv.save()



def initiate_InstrumentVariable(path):
    filename = "gliderMetadataApp_instrumentvariable.csv"
    pathfile = path + '/' + filename
    file = io.FileIO(file=pathfile, mode="r")
    df = pd.read_csv(file)
    # cf variable
    filenamevcs = "gliderMetadataApp_variablecfstandard.csv"
    pathfilevcs = path + '/' + filenamevcs
    filevcs = io.FileIO(file=pathfilevcs, mode="r")
    dfvcs = pd.read_csv(filevcs)
    # nerc variable
    filenamevns = "gliderMetadataApp_variablenercstandard.csv"
    pathfilevns = path + '/' + filenamevns
    filevns = io.FileIO(file=pathfilevns, mode="r")
    dfvns = pd.read_csv(filevns)
    # instrument model
    filenameim = "gliderMetadataApp_instrumentmodel.csv"
    pathfileim = path + '/' + filenameim
    fileim = io.FileIO(file=pathfileim, mode="r")
    dfim = pd.read_csv(fileim)
    # platform company
    filenamepc = "gliderMetadataApp_platformcompany.csv"
    pathfilepc = path + '/' + filenamepc
    filepc = io.FileIO(file=pathfilepc, mode="r")
    dfpc = pd.read_csv(filepc)
    for row in df.itertuples():
        ivcheck = models.InstrumentVariable.objects.filter(instrument_variableSourceName=getattr(row, 'instrument_variableSourceName'))
        if ivcheck.first() is None:
            # get pk calls
            # cfVariable
            dfvcssub = dfvcs[dfvcs['id'] == getattr(row, 'instrument_cfVariable_id')]
            if dfvcssub.empty:
                vcs = None
            else :
                dfvcssub = dfvcssub.iloc[0]
                vcs = models.VariableCFStandard.objects.get(variable_standardName=dfvcssub['variable_standardName'])
            # nercVariable
            dfvnssub = dfvns[dfvns['id'] == getattr(row, 'instrument_nercVariable_id')]
            if dfvnssub.empty:
                vns = None
            else :
                dfvnssub = dfvnssub.iloc[0]
                vns = models.VariableNERCStandard.objects.get(variable_nerc_variableName=dfvnssub['variable_nerc_variableName'])
            # instrumentModel
            dfimsub = dfim[dfim['id'] == getattr(row, 'instrument_variableInstrumentModel_id')]
            if dfimsub.empty:
                im = None
            else :
                dfimsub = dfimsub.iloc[0]
                im = models.InstrumentModel.objects.get(instrument_model=dfimsub['instrument_model'])
            # platformCompany
            dfpcsub = dfpc[dfpc['id'] == getattr(row, 'instrument_variablePlatformCompany_id')]
            if dfpcsub.empty:
                pc = None
            else:
                dfpcsub = dfpcsub.iloc[0]
                pc = models.PlatformCompany.objects.get(platform_company=dfpcsub['platform_company'])

            iv = models.InstrumentVariable(instrument_cfVariable=vcs,
                                           instrument_nercVariable=vns,
                                           instrument_variableInstrumentModel=im,
                                           instrument_variablePlatformCompany=pc,
                                           instrument_variableSourceName=checkNa(getattr(row, 'instrument_variableSourceName')),
                                           instrument_variableSourceUnits=checkNa(getattr(row, 'instrument_variableSourceUnits')),
                                           instrument_gcmdKeyword=checkNa(getattr(row, 'instrument_gcmdKeyword')),
                                           instrument_accuracy=checkNa(getattr(row, 'instrument_accuracy')),
                                           instrument_precision=checkNa(getattr(row, 'instrument_precision')),
                                           instrument_resolution=checkNa(getattr(row, 'instrument_resolution')),
                                           instrument_validMax=checkNa(getattr(row, 'instrument_validMax')),
                                           instrument_validMin=checkNa(getattr(row, 'instrument_validMin'))
                                           )
            iv.save()
        else:
            print(
                f"There is already a variable with name {ivcheck.first().instrument_variableSourceName}, "
                f"proceeding to next variable.")

def initiate_PlatformVariable(path):
    filename = "gliderMetadataApp_platformvariable.csv"
    pathfile = path + '/' + filename
    file = io.FileIO(file=pathfile, mode="r")
    df = pd.read_csv(file)
    # cf variable
    filenamevcs = "gliderMetadataApp_variablecfstandard.csv"
    pathfilevcs = path + '/' + filenamevcs
    filevcs = io.FileIO(file=pathfilevcs, mode="r")
    dfvcs = pd.read_csv(filevcs)
    # nerc variable
    filenamevns = "gliderMetadataApp_variablenercstandard.csv"
    pathfilevns = path + '/' + filenamevns
    filevns = io.FileIO(file=pathfilevns, mode="r")
    dfvns = pd.read_csv(filevns)
    # platform company
    filenamepc = "gliderMetadataApp_platformcompany.csv"
    pathfilepc = path + '/' + filenamepc
    filepc = io.FileIO(file=pathfilepc, mode="r")
    dfpc = pd.read_csv(filepc)
    for row in df.itertuples():
        # cfVariable
        dfvcssub = dfvcs[dfvcs['id'] == getattr(row, 'platform_cfVariable_id')]
        if dfvcssub.empty:
            vcs = None
        else:
            dfvcssub = dfvcssub.iloc[0]
            vcs = models.VariableCFStandard.objects.get(variable_standardName=dfvcssub['variable_standardName'])
        # nercVariable
        dfvnssub = dfvns[dfvns['id'] == getattr(row, 'platform_nercVariable_id')]
        if dfvnssub.empty:
            vns = None
        else:
            dfvnssub = dfvnssub.iloc[0]
            vns = models.VariableNERCStandard.objects.get(
                variable_nerc_variableName=dfvnssub['variable_nerc_variableName'])
        dfpcsub = dfpc[dfpc['id'] == getattr(row, 'platform_variablePlatformCompany_id')].iloc[0]
        pc = models.PlatformCompany.objects.get(platform_company=dfpcsub['platform_company'])
        pv = models.PlatformVariable(platform_cfVariable=vcs,
                                     platform_nercVariable=vns,
                                     platform_variablePlatformCompany=pc,
                                     platform_variableSourceName=checkNa(getattr(row, 'platform_variableSourceName')),
                                     platform_variableSourceUnits=checkNa(getattr(row, 'platform_variableSourceUnits')))
        pv.save()