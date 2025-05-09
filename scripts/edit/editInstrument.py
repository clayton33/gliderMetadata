import io
import pandas as pd
from gliderMetadataApp import models
# 20250508
# implement BODC NERC naming scheme
# have to modify InstrumentMake, InstrumentType, and InstrumentModel
# InstrumentMake
## Sea-Bird
q = models.InstrumentMake.objects.get(instrument_make='Sea-Bird')
q.instrument_make = 'Sea-Bird Scientific'
q.instrument_vocabulary = 'https://vocab.nerc.ac.uk/collection/L35/current/MAN0013/'
q.save()
## Wetlabs
q = models.InstrumentMake.objects.get(instrument_make='Wetlabs')
q.instrument_make = 'WET Labs'
q.instrument_vocabulary = 'https://vocab.nerc.ac.uk/collection/L35/current/MAN0026/'
q.save()
## RBR
q = models.InstrumentMake.objects.get(instrument_make='RBR')
### don't have to change make, already correct
q.instrument_vocabulary = 'https://vocab.nerc.ac.uk/collection/L35/current/MAN0049/'
q.save()
## JFE Advantech Co.
q = models.InstrumentMake.objects.get(instrument_make='JFE Advantech Co.')
q.instrument_make = 'JFE Advantech'
q.instrument_vocabulary = 'https://vocab.nerc.ac.uk/collection/L35/current/MAN0053/'
q.save()
## Alseamar
q = models.InstrumentMake.objects.get(instrument_make='Alseamar')
q.instrument_make = 'Alsemar Alcen'
q.instrument_vocabulary = 'https://vocab.nerc.ac.uk/collection/L35/current/MAN0328/'
q.save()
# InstrumentType
## ctd
q = models.InstrumentType.objects.get(instrument_type='ctd')
q.instrument_type='CTD'
q.instrument_vocabulary='https://vocab.nerc.ac.uk/collection/L05/current/130/'
q.save()
## fluorometer
q = models.InstrumentType.objects.get(instrument_type='fluorometer')
q.instrument_type='fluorometers'
q.instrument_vocabulary='https://vocab.nerc.ac.uk/collection/L05/current/113/'
q.save()
## oxygen
q = models.InstrumentType.objects.get(instrument_type='oxygen')
q.instrument_type='dissolved gas sensors'
q.instrument_vocabulary='https://vocab.nerc.ac.uk/collection/L05/current/351/'
q.save()
## optic
q = models.InstrumentType.objects.get(instrument_type='optic')
q.instrument_type='optical backscatter sensors'
q.instrument_vocabulary='https://vocab.nerc.ac.uk/collection/L05/current/123/'
q.save()
## acoustic - waiting until I get WASP
## uvFluorometer - not in vocabulary
# InstrumentModel
# !! going to use alternative labels for model name
# !! and then the preferred label as longname
## GPCTD
q = models.InstrumentModel.objects.get(instrument_model='GPCTD')
q.instrument_model = 'SBE GPCTD'
q.instrument_longname = 'Sea-Bird SBE Glider Payload CTD (GPCTD)'
q.instrument_vocabulary = 'https://vocab.nerc.ac.uk/collection/L22/current/TOOL1026/'
q.save()
## FLBBCDEXP
q = models.InstrumentModel.objects.get(instrument_model='FLBBCDEXP')
## 43F
q = models.InstrumentModel.objects.get(instrument_model = '43F')
q.instrument_model = 'SBE 43F DO'
q.instrument_longname = 'Sea-Bird SBE 43F Dissolved Oxygen Sensor'
q.instrument_vocabulary = 'https://vocab.nerc.ac.uk/collection/L22/current/TOOL0037/'
q.save()
## Legato3|fast16
q = models.InstrumentModel.objects.get(instrument_model = 'Legato3|fast16')
q.instrument_model = 'RBR Legato3'
q.instrument_longname = 'RBR Legato3 CTD'
q.instrument_vocabulary = 'https://vocab.nerc.ac.uk/collection/L22/current/TOOL1745/'
q.save()
## AROD-FT-CE
q = modelsInstrumentModel.objects.get(instrument_model = 'AROD-FT-CE')
q.instrument_model = 'JFE Rinko ARO-FT'
q.instrument_longname = 'JFE Advantech Rinko FT ARO-FT oxygen sensor'
q.instrument_vocabulary = 'https://vocab.nerc.ac.uk/collection/L22/current/TOOL1783/'
q.save()
## MFL#27 - not in vocabulary
