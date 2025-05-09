import io
import pandas as pd
from gliderMetadataApp import models

data = {'instrument_make' : ['RBR', 'RBR'],
        'instrument_type' : ['CTD', 'dissolved gas sensors'],
        'instrument_model' : ['RBR Legato3', 'RBR Coda T.ODO'],
        'instrument_longname' : ['RBR Legato3 CTD', 'RBR Coda T.ODO Temperature and Dissolved Oxygen Sensor'],
        'instrument_vocabulary' : ['https://vocab.nerc.ac.uk/collection/L22/current/TOOL1745/', 'https://vocab.nerc.ac.uk/collection/L22/current/TOOL1717/']}
df = pd.DataFrame(data)
for row in df.itertuples():
    print(f"Getting {getattr(row, 'instrument_model')} with vocabulary {getattr(row, 'instrument_vocabulary')}")
    # query to get instrument_make
    immQ = models.InstrumentMake.objects.filter(instrument_make=getattr(row, 'instrument_make'))
    if immQ.first() is None:
        print('instrument_make not in database yet, please add.')
        print(f"Skipping  {getattr(row, 'instrument_model')} with vocabulary {getattr(row, 'instrument_vocabulary')}")
        continue
    else :
        instrumentModelQ = immQ.first()
    # query to get instrument_type
    itQ = models.InstrumentType.objects.filter(instrument_type=getattr(row, 'instrument_type'))
    if itQ.first() is None:
        print('instrument_type no in database yet, please add')
        print(f"Skipping  {getattr(row, 'instrument_model')} with vocabulary {getattr(row, 'instrument_vocabulary')}")
        continue
    else :
        instrumentTypeQ = itQ.first()
    # check if data has already been added
    imQ = models.InstrumentModel.objects.filter(instrument_model=getattr(row, 'instrument_model'),
                                                instrument_vocabulary=getattr(row, 'instrument_vocabulary'))
    if imQ.first() is None:
        print('Adding ...')
        im = models.InstrumentModel(instrument_modelMake = instrumentModelQ,
                                    instrument_modelType = instrumentTypeQ,
                                    instrument_model=getattr(row, 'instrument_model'),
                                    instrument_longname=getattr(row, 'instrument_longname'),
                                    instrument_vocabulary=getattr(row, 'instrument_vocabulary'))
        im.save()
    else :
        print("Already in database.")