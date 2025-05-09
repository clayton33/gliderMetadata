import io
import pandas as pd
from gliderMetadataApp import models
from scripts.createPygliderIOOSyaml import platform_company, platform_model

# InstrumentVariable needs A LOT of info
# see example 'data' below for addition of new variables
data = {'instrument_variablePlatformCompany':['Alseamar', 'Alseamar', 'Alseamar'],
        'instrument_variablePlatformModel':['SeaExplorer', 'SeaExplorer', 'SeaExplorer'],
        'instrument_variableInstrumentModel':['RBR Coda T.ODO', 'RBR Coda T.ODO', 'RBR Coda T.ODO'],
        'instrument_nercVariable':[None, 'DOXY', 'TEMP_DOXY'],
        'instrument_cfVariable':[None, 'mole_concentration_of_dissolved_molecular_oxygen_in_sea_water', 'temperature_of_sensor_for_oxygen_in_sea_water'],
        'instrument_variableSourceName':['LEGATO_CODA_CORR_PHASE', 'LEGATO_CODA_DO', 'LEGATO_CODA_TEMPERATURE'],
        'instrument_variableSourceUnits':['', 'umol l-1', 'Celsius'],
        'instrument_gcmdKeyword':[None, 'Earth Science > Oceans > Ocean Chemistry > Dissolved Gases', None],
        'instrument_accuracy':[None, None, None],
        'instrument_precision':[None, None, None],
        'instrument_resolution':[None, None, None],
        'instrument_validMin':[None, None, None],
        'instrument_validMax':[None, None, None]}
df = pd.DataFrame(data)
for row in df.itertuples():
        print(f"Getting {getattr(row, 'instrument_variableSourceName')} for a {getattr(row, 'instrument_variablePlatformModel')} "
              f"for instrument {getattr(row, 'instrument_variableInstrumentModel')}")
        # get platform company
        ipQ = models.PlatformCompany.objects.get(platform_company=getattr(row, 'instrument_variablePlatformCompany'),
                                                 platform_model=getattr(row, 'instrument_variablePlatformModel'))
        # get instrument model
        iimQ = models.InstrumentModel.objects.get(instrument_model=getattr(row, 'instrument_variableInstrumentModel'))
        # get nerc variable (can be None)
        if getattr(row, 'instrument_nercVariable') is None:
                invQ = None
        else:
                invQ = models.VariableNERCStandard.objects.get(variable_nerc_variableName=getattr(row, 'instrument_nercVariable'))
        # get cf name (can be None)
        if getattr(row, 'instrument_cfVariable') is None:
                icfQ = None
        else:
                icfQ = models.VariableCFStandard.objects.get(variable_standardName=getattr(row, 'instrument_cfVariable'))
        # check if the variable is already in the table
        ivQ = models.InstrumentVariable.objects.filter(instrument_cfVariable=icfQ,
                                                       instrument_nercVariable=invQ,
                                                       instrument_variableInstrumentModel=iimQ,
                                                       instrument_variablePlatformCompany=ipQ,
                                                       instrument_variableSourceName=getattr(row, 'instrument_variableSourceName'))
        if ivQ.first() is None:
                print('Adding...')
                iv = models.InstrumentVariable(instrument_cfVariable=icfQ,
                                               instrument_nercVariable=invQ,
                                               instrument_variableInstrumentModel=iimQ,
                                               instrument_variablePlatformCompany=ipQ,
                                               instrument_variableSourceName=getattr(row, 'instrument_variableSourceName'),
                                               instrument_variableSourceUnits=getattr(row, 'instrument_variableSourceUnits'),
                                               instrument_gcmdKeyword=getattr(row, 'instrument_gcmdKeyword'),
                                               instrument_accuracy=getattr(row, 'instrument_accuracy'),
                                               instrument_precision=getattr(row, 'instrument_precision'),
                                               instrument_resolution=getattr(row, 'instrument_resolution'),
                                               instrument_validMax=getattr(row, 'instrument_validMax'),
                                               instrument_validMin=getattr(row, 'instrument_validMin')
                                               )
                iv.save()
        else:
                print('Already in database.')