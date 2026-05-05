import io
import pandas as pd
from gliderMetadataApp import models

data = {'instrument_make' : ['RBR',
                             'RBR',
                             'RBR',
                             'Pro Oceanus',
                             'Rockland Scientific',
                             'Nortek'],
        'instrument_type' : ['CTD',
                             'dissolved gas sensors',
                             'optical backscatter sensors',
                             'dissolved gas sensors',
                             'microstructure sensors',
                             'current profilers'],
        'instrument_model' : ['RBR Legato3',
                              'RBR Coda T.ODO',
                              'RBR tridente',
                              'Pro-Oceanus Mini pCO2',
                              'Rockland MicroRider-1000G',
                              'Nortek Glider1000 AD2CP'],
        'instrument_longname' : ['RBR Legato3 CTD',
                                 'RBR Coda T.ODO Temperature and Dissolved Oxygen Sensor',
                                 'RBR tridente scattering fluorescence sensor',
                                 'Pro-Oceanus Mini CO2 submersible pCO2 analyser',
                                 'Rockland Scientific MicroRider-1000G turbulence microstructure profiler',
                                 'Nortek Glider1000 AD2CP Acoustic Doppler Current Profiler'],
        'instrument_vocabulary' : ['https://vocab.nerc.ac.uk/collection/L22/current/TOOL1745/',
                                   'https://vocab.nerc.ac.uk/collection/L22/current/TOOL1717/',
                                   'https://vocab.nerc.ac.uk/collection/L22/current/TOOL2149/',
                                   'https://vocab.nerc.ac.uk/collection/L22/current/TOOL1319/',
                                   'https://vocab.nerc.ac.uk/collection/L22/current/TOOL2265/',
                                   'https://vocab.nerc.ac.uk/collection/L22/current/TOOL1774/']}
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