import io
import pandas as pd
from gliderMetadataApp import models
data = {'instrument_type' : ['current profilers',
                             'microstructure sensors']}
df = pd.DataFrame(data)
for row in df.itertuples():
    print(f"Getting {getattr(row, 'instrument_type')}")
    # query to get instrument_type
    itQ = models.InstrumentType.objects.filter(instrument_type=getattr(row, 'instrument_type'))
    if itQ.first() is None:
        print('Adding ...')
        it = models.InstrumentType(instrument_type=getattr(row, 'instrument_type'))
        it.save()
    else:
        print('Already in database.')