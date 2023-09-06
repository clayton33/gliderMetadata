import io
import pandas as pd
from gliderMetadataApp import models

# 4 tables need to be initialized using ARGO parameters
# variableCFStandard (have to check what is already there)
# variableNERCStandard
# unitCFStandard
# unitNERCStandard
# then the major table, Variable, will use those 4 tables, we'll hook everything up by
# using the ARGO file

def initiate_VariableCFStandard():
    file = io.FileIO(file=r".\initializationData\variable\variable_CFStandard_ARGO.csv")
    df = pd.read_csv(file)
    for row in df.itertuples():
        # check if the standardName is already in the table if not, initialize
         vcf = models.VariableCFStandard(variable_nameVocabulary = models.Vocabulary.objects.get(pk=getattr(row, 'variable_nameVocabulary')),
                                         variable_standardName = getattr(row, 'variable_standardName'))
         vcf.save()

def initiate_VariableNERCStandard():
    file = io.FileIO(file=r".\initializationData\variable\variable_NERCStandard_ARGO.csv")
    df = pd.read_csv(file)
    for row in df.itertuples():
        # check if the standardName is already in the table if not, initialize
         vcf = models.VariableCFStandard(variable_nameVocabulary = models.Vocabulary.objects.get(pk=getattr(row, 'variable_nameVocabulary')),
                                         variable_standardName = getattr(row, 'variable_standardName'))
         vcf.save()