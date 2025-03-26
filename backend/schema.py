from table import *
from pydantic import create_model, BaseModel
from typing import Optional
from sqlalchemy.inspection import inspect


#--------------------------------- Foudation Table ---------------------------------------------#
def FoundationList_All(model_class):
    columns = inspect(model_class).c
    annotations = {}
    
    for column in columns:
        column_type = column.type.python_type  
        
        if column.nullable:
            column_type = Optional[column_type]  
            annotations[column.name] = (column_type, None)

        else:
            annotations[column.name] = (column_type, ...)
 
    return create_model(f"{model_class.__name__}Schema", **annotations)

FoundationListSchema_All = FoundationList_All(FoundationList)



def FoundationList_AmigurumiID(model_class):
    class FoundationListAmigurumiID(BaseModel):
        amigurumi_id: int
        
    return FoundationListAmigurumiID

FoundationListSchema_AmigurumiID = FoundationList_AmigurumiID(FoundationList)



#--------------------------------- Material Table ---------------------------------------------#
def MaterialList_All(model_class):
    columns = inspect(model_class).c
    annotations = {}
    
    for column in columns:
        column_type = column.type.python_type  
        
        if column.nullable:
            column_type = Optional[column_type]  
            annotations[column.name] = (column_type, None)

        else:
            annotations[column.name] = (column_type, ...)
 
    return create_model(f"{model_class.__name__}Schema", **annotations)

MaterialListSchema_All = MaterialList_All(MaterialList)



def MaterialList_MaterialID(model_class):
    class MaterialListMaterialID(BaseModel):
        material_list_id: int
        
    return MaterialListMaterialID

MaterialListSchema_MaterialID = MaterialList_MaterialID(MaterialList)



#--------------------------------- Image Table ---------------------------------------------#
def Image_All(model_class):
    columns = inspect(model_class).c
    annotations = {}
    
    for column in columns:
        column_type = column.type.python_type  
        
        if column.nullable:
            column_type = Optional[column_type]  
            annotations[column.name] = (column_type, None)

        else:
            annotations[column.name] = (column_type, ...)
 
    return create_model(f"{model_class.__name__}Schema", **annotations)

ImageSchema_All = Image_All(Image)



def Image_ImageID(model_class):
    class ImageImageID(BaseModel):
        image_id: int
        
    return ImageImageID

ImageSchema_ImageID = Image_ImageID(Image)



#--------------------------------- StitchBook Table ---------------------------------------------#
def StitchBook_All(model_class):
    columns = inspect(model_class).c
    annotations = {}
    
    for column in columns:
        column_type = column.type.python_type  
        
        if column.nullable:
            column_type = Optional[column_type]  
            annotations[column.name] = (column_type, None)

        else:
            annotations[column.name] = (column_type, ...)
 
    return create_model(f"{model_class.__name__}Schema", **annotations)

StitchBookSchema_All = StitchBook_All(StitchBook)


def StitchBook_LineID(model_class):
    class StitchBookLineID(BaseModel):
        line_id: int
        
    return StitchBookLineID

StitchBookSchema_LineID = StitchBook_LineID(StitchBook)




#--------------------------------- StitchBook Sequence Table ---------------------------------------------#
def StitchBookSequence_All(model_class):
    columns = inspect(model_class).c
    annotations = {}
    
    for column in columns:
        column_type = column.type.python_type  
        
        if column.nullable:
            column_type = Optional[column_type]  
            annotations[column.name] = (column_type, None)

        else:
            annotations[column.name] = (column_type, ...)
 
    return create_model(f"{model_class.__name__}Schema", **annotations)

StitchBookSequenceSchema_All = StitchBook_All(StitchBookSequence)



def StitchBook_ElementID(model_class):
    class StitchBookElementID(BaseModel):
        element_id: int
        
    return StitchBookElementID

StitchBookSequenceSchema_ElementID = StitchBook_ElementID(StitchBookSequence)