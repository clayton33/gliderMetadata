import io
import pandas as pd
from gliderMetadataApp import models

# change instrument type for some instruments
# FLB from optics to fluorometer
flbQ = models.InstrumentModel.objects.get(instrument_model='FLBBCDEXP')
tQ = models.InstrumentType.objects.get(instrument_type='fluorometer')
flbQ.instrument_modelType = tQ
flbQ.save()

# Minifluo from optics to uvFluorometer
miflQ = models.InstrumentModel.objects.get(instrument_model='MFL#27')
tQ = models.InstrumentType.objects.get(instrument_type='uvFluorometer')
miflQ.instrument_modelType = tQ
miflQ.save()