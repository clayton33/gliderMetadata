import io
import pandas as pd
from gliderMetadataApp import models
# added 20250509
data = {'instrument_make' : ['RBR'],
        'instrument_vocabulary' : ['https://vocab.nerc.ac.uk/collection/L35/current/MAN0049/']}
df = pd.DataFrame(data)
for row in df.itertuples():
    print(f"Getting {getattr(row, 'instrument_make')} with vocabulary {getattr(row, 'instrument_vocabulary')}")
    # check if data has already been added
    imQ = models.InstrumentMake.objects.filter(instrument_make=getattr(row, 'instrument_make'),
                                            instrument_vocabulary=getattr(row, 'instrument_vocabulary'))
    if imQ.first() is None:
        print('Adding ...')
        im = models.InstrumentMake(instrument_make=getattr(row, 'instrument_make'),
                                   instrument_vocabulary=getattr(row, 'instrument_vocabulary'))
        im.save()
    else :
        print("Already in database.")