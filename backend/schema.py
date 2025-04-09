from table import *
from pydantic import create_model, Field
from typing import Optional
from sqlalchemy.inspection import inspect


#---------------------------------------------------------------------------#
# Código padrão para trazer todas as colunas de cada tabela, identificação da sua formatação, descriçao da coluna e obrigatoriedade de preenchimento
def bringAllCollumns(model_class):
    columns = inspect(model_class).c
    annotations = {}

    for column in columns:
        column_type = column.type.python_type  
        description = column.info.get("description", "Campo sem descrição")
        
        if column.nullable:
            column_type = Optional[column_type]  
            annotations[column.name] = (column_type, Field(None, description=description))

        else:
            annotations[column.name] = (column_type, Field(..., description=description))
 
    return create_model(f"{model_class.__name__}Schema_All", **annotations)

FoundationListSchema_All = bringAllCollumns(FoundationList)
MaterialListSchema_All = bringAllCollumns(MaterialList)
ImageSchema_All = bringAllCollumns(Image)
StitchBookSchema_All = bringAllCollumns(StitchBook)
StitchBookSequenceSchema_All = bringAllCollumns(StitchBookSequence)


#---------------------------------------------------------------------------#
# Código padrão para trazer todas as colunas de cada tabela, com excessão das colunas de chave principal, identificação da sua formatação, 
# descriçao da coluna e obrigatoriedade de preenchimento
def bringOnlyNoPrimaryKeyCollumns(model_class):
    columns = inspect(model_class).c
    annotations = {}

    for column in columns:
        if not column.primary_key:
            column_type = column.type.python_type  
            description = column.info.get("description", "Campo sem descrição")
            
            if column.nullable:
                column_type = Optional[column_type]  
                annotations[column.name] = (column_type, Field(None, description=description))

            else:
                annotations[column.name] = (column_type, Field(..., description=description))
 
    return create_model(f"{model_class.__name__}Schema_No_Auto", **annotations)

FoundationListSchema_No_Auto = bringOnlyNoPrimaryKeyCollumns(FoundationList)
MaterialListSchema_No_Auto = bringOnlyNoPrimaryKeyCollumns(MaterialList)
ImageSchema_No_Auto = bringOnlyNoPrimaryKeyCollumns(Image)
StitchBookSchema_No_Auto = bringOnlyNoPrimaryKeyCollumns(StitchBook)
StitchBookSequenceSchema_No_Auto = bringOnlyNoPrimaryKeyCollumns(StitchBookSequence)



#---------------------------------------------------------------------------#
# Código padrão para trazer apenas a coluna de chave principal, identificação da sua formatação, descriçao da coluna e obrigatoriedade de preenchimento
def bringOnlyPrimaryKey(model_class):
    columns = inspect(model_class).c
    annotations = {}

    for column in columns:
        if column.primary_key:
            column_type = column.type.python_type  
            description = column.info.get("description", "Campo sem descrição")
            
            if column.nullable:
                column_type = Optional[column_type]  
                annotations[column.name] = (column_type, Field(None, description=description))

            else:
                annotations[column.name] = (column_type, Field(..., description=description))
 
    return create_model(f"{model_class.__name__}Schema_PrimaryKey", **annotations)

FoundationListSchema_PrimaryKey = bringOnlyPrimaryKey(FoundationList)
MaterialListSchema_PrimaryKey = bringOnlyPrimaryKey(MaterialList)
ImageSchema_PrimaryKey = bringOnlyPrimaryKey(Image)
StitchBookSchema_PrimaryKey = bringOnlyPrimaryKey(StitchBook)
StitchBookSequenceSchema_PrimaryKey = bringOnlyPrimaryKey(StitchBookSequence)


