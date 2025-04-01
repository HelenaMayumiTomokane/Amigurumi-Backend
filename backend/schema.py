from table import *
from pydantic import create_model, Field
from typing import Optional
from sqlalchemy.inspection import inspect


#--------------------------------- trazer todas as colunas ---------------------------------------------#
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
 
    return create_model(f"{model_class.__name__}Schema", **annotations)

FoundationListSchema_All = bringAllCollumns(FoundationList)
MaterialListSchema_All = bringAllCollumns(MaterialList)
ImageSchema_All = bringAllCollumns(Image)
StitchBookSchema_All = bringAllCollumns(StitchBook)
StitchBookSequenceSchema_All = bringAllCollumns(StitchBookSequence)



#--------------------------------- trazer tudo menos a chave primária  ---------------------------------------------#
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
 
    return create_model(f"{model_class.__name__}Schema", **annotations)

FoundationListSchema_No_Auto = bringOnlyNoPrimaryKeyCollumns(FoundationList)
MaterialListSchema_No_Auto = bringOnlyNoPrimaryKeyCollumns(MaterialList)
ImageSchema_No_Auto = bringOnlyNoPrimaryKeyCollumns(Image)
StitchBookSchema_No_Auto = bringOnlyNoPrimaryKeyCollumns(StitchBook)
StitchBookSequenceSchema_No_Auto = bringOnlyNoPrimaryKeyCollumns(StitchBookSequence)



#--------------------------------- Trazer apenas a chave primária ---------------------------------------------#
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
 
    return create_model(f"{model_class.__name__}Schema", **annotations)

FoundationListSchema_AmigurumiID = bringOnlyPrimaryKey(FoundationList)
MaterialListSchema_MaterialID = bringOnlyPrimaryKey(MaterialList)
ImageSchema_ImageID = bringOnlyPrimaryKey(Image)
StitchBookSchema_LineID = bringOnlyPrimaryKey(StitchBook)
StitchBookSequenceSchema_ElementID = bringOnlyPrimaryKey(StitchBookSequence)


