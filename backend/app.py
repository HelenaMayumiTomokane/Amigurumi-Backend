from flask import request, jsonify, render_template, redirect
from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info, Tag
from sqlalchemy import desc, cast, Integer

from config import DevelopmentConfig
from database import db

from error_schema import *
from schema import *
from table import *

info = Info(title="Minha API de Amigurumi", version="1.0.0", description="API para gerenciar informações dos Amigurumis")
app = OpenAPI(__name__, info=info)

app.config["SQLALCHEMY_DATABASE_URI"] = DevelopmentConfig.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = DevelopmentConfig.SQLALCHEMY_TRACK_MODIFICATIONS

foundation_tag = Tag(name="Foundation", description="Endpoints relacionados à adição, manipulação, busca e exclusão de dados sobre os amigurumis")
stichbook_sequence_tag = Tag(name="Stitchbook Element", description="Endpoints relacionados à adição, manipulação, busca e exclusão de elementos dos amigurumis e sua ordem de execução")
stichbook_tag = Tag(name="Stichbook", description="Endpoints relacionados à adição, manipulação, busca e exclusão das carreiras utilizadas na construção dos amigurumis")
image_tag = Tag(name="Image", description="Endpoints relacionados à adição, manipulação, busca e exclusão de imagem dos amigurumi")
material_tag = Tag(name="Material", description="Endpoints relacionados à adição, manipulação, busca e exclusão de materiais utilizados na construção dos amigurumis")
support_tag = Tag(name="suporte", description="Endpoint para geração da documentação dos APIs")

CORS(app)

db.init_app(app)

#criação das tabelas automaticamente
with app.app_context(): 
    db.create_all() 

register_validation_error_handler(app)

#----------------------------------- API Suporte ------------------------------#
#renderização de novas abas
@app.get('/<page>', tags=[support_tag])  
def render_page(page):
    try:
        return render_template(f'{page}.html')
    except:
        return "Página não encontrada", 404


#Geração do OpenApi
@app.get('/openapi', tags=[support_tag])
def openapi():
    doc_type = request.args.get('doc', 'swagger') 

    if doc_type == 'redoc':
        return redirect("/redoc")
    
    elif doc_type == 'rapidoc':
        return redirect("/rapidoc")
    
    elif doc_type == 'swagger':
        return redirect("/swagger")
    
    elif doc_type == 'scalar':
        return redirect("/scalar")
    
    elif doc_type == 'rapipdf':
        return redirect("/rapipdf")
    
    elif doc_type == 'elements':
        return redirect("/elements")
    



#----------------------------------- API para a tabela Foundation List----------#
@app.get('/foundation_list', tags=[foundation_tag], responses={"200": FoundationListSchema_All, "422": ValidationErrorResponse},
         summary="Requisição para puxar todos os amigurumis cadastrados")
def get_foundation_list():
    with app.app_context():
        amigurumis = FoundationList.query.all()

    if not amigurumis:
        return jsonify({"error": "Nenhum amigurumi encontrado"}), 404

    result = [
        {key: value for key, value in amigurumi.__dict__.items() if not key.startswith('_')}
        for amigurumi in amigurumis
    ]

    return jsonify(result)



@app.post('/foundation_list', tags=[foundation_tag], responses={"200": FoundationListSchema_No_Auto, "422": ValidationErrorResponse},
         summary="Requisição para cadastrar um novo amigurumi")
def add_foundation_list(body: FoundationListSchema_No_Auto):
    data = body.dict() 
    new_amigurumi = FoundationList(**data)
    db.session.add(new_amigurumi)
    db.session.commit()

    return jsonify({
        "message": f"Amigurumi {new_amigurumi.name} adicionado com sucesso!",
        "amigurumi_id": new_amigurumi.amigurumi_id,
    })




@app.put('/foundation_list/amigurumi_id', tags=[foundation_tag], responses={"200": FoundationListSchema_All, "422": ValidationErrorResponse},
         summary="Requisição para alterar os dados do amigurumi cadastrado")
def update_foundation_list(body: FoundationListSchema_All):
    data = body.dict() 
    amigurumi_id = int(data.get('amigurumi_id'))
    amigurumi = FoundationList.query.get(amigurumi_id)  

    if not amigurumi:
        return jsonify({"error": "Amigurumi não encontrado"}), 404

    for key, value in data.items():
        if hasattr(amigurumi, key):
            setattr(amigurumi, key, value)

    db.session.commit()

    return jsonify({
        "message": f"Amigurumi {amigurumi.name} atualizado com sucesso!",
        "amigurumi_id": amigurumi.amigurumi_id,
    })




@app.delete('/foundation_list/amigurumi_id', tags=[foundation_tag], responses={"200": FoundationListSchema_PrimaryKey, "422": ValidationErrorResponse},
         summary="Requisição para deletar o amigurumi cadastrado")
def delete_foundation_list(body: FoundationListSchema_PrimaryKey):
    data = body.dict() 
    amigurumi_id = int(data.get('amigurumi_id'))
    amigurumi = FoundationList.query.get(amigurumi_id) 

    if not amigurumi:
        return jsonify({"error": "Amigurumi não encontrado"}), 404

    db.session.delete(amigurumi) 
    db.session.commit() 

    return jsonify({
        "message": f"Amigurumi {amigurumi.name} removido com sucesso!",
        "amigurumi_id": amigurumi.amigurumi_id,
    })




#----------------------------------- API para a tabela StichBook ------------------------#
@app.get('/stitchbook', tags=[stichbook_tag], responses={"200": StitchBookSchema_All, "422": ValidationErrorResponse},
         summary="Requisição para puxar todas as linhas de receitas cadastradas")
def get_all_stichbook():
    amigurumi_stiches = db.session.query(StitchBookSequence, StitchBook).outerjoin(
        StitchBook,
        (StitchBook.amigurumi_id == StitchBookSequence.amigurumi_id) & 
        (StitchBook.element_id == StitchBookSequence.element_id)
    ).order_by(
        cast(StitchBookSequence.amigurumi_id, Integer).asc(),
        cast(StitchBookSequence.element_order, Integer).asc(),
        cast(StitchBook.number_row, Integer).asc()
    ).all()

    result = []
    for sequence, stitch in amigurumi_stiches:
        sequence_data = {key: value for key, value in sequence.__dict__.items() if not key.startswith('_')}
        
        stitch_data = {}
        if stitch is not None:
            stitch_data = {key: value for key, value in stitch.__dict__.items() if not key.startswith('_')}

        combined_data = {**sequence_data, **stitch_data}
        result.append(combined_data)

    return jsonify(result)



@app.post('/stitchbook', tags=[stichbook_tag], responses={"200": StitchBookSchema_No_Auto, "422": ValidationErrorResponse},
         summary="Requisição para cadastrar uma nova linha de receita")
def add_stichbook(body: StitchBookSchema_No_Auto):
    data = body.dict() 
    amigurumi_id = int(data.get('amigurumi_id'))
    amigurumi = FoundationList.query.get(amigurumi_id)

    if not amigurumi:
        return jsonify({"error": "Amigurumi não cadastrado"}), 404

    new_recipe = StitchBook(**data)
    db.session.add(new_recipe)
    db.session.commit()

    return jsonify({
        "message": f"Linha a adicionada com sucesso para o amigurumi {amigurumi.amigurumi_id}!",
        "line_id": new_recipe.line_id,
    })



@app.put('/stitchbook/line_id', tags=[stichbook_tag], responses={"200": StitchBookSchema_All, "422": ValidationErrorResponse},
         summary="Requisição para alterar uma linha de receita cadastrada")
def update_stichbook_line(body: StitchBookSchema_All):
    data = body.dict() 
    line_id = int(data.get('line_id'))
    lineID = StitchBook.query.get(line_id)  

    if not lineID:
        return jsonify({"error": "Linha não encontrada"}), 404

    for key, value in data.items():
        if hasattr(lineID, key):
            setattr(lineID, key, value)

    db.session.commit()

    return jsonify({
        "message": f"Linha {line_id} atualizada com sucesso!",
        "line_id": line_id,
    })



@app.delete('/stitchbook/line_id', tags=[stichbook_tag], responses={"200": StitchBookSchema_PrimaryKey, "422": ValidationErrorResponse},
         summary="Requisição para deletar uma linha de receita cadastrada")
def delete_stichbook_line(body: StitchBookSchema_PrimaryKey):
    data = body.dict() 
    line_id = int(data.get('line_id'))
    lineID = StitchBook.query.get(line_id) 

    if not lineID:
        return jsonify({"error": "Linha não encontrada"}), 404

    db.session.delete(lineID) 
    db.session.commit() 

    return jsonify({
        "message": f"Linha {line_id} removida com sucesso!",
        "line_id": line_id,
    })



#----------------------------------- API para a tabela Image -------------------#
@app.get('/image', tags=[image_tag], responses={"200": ImageSchema_All, "422": ValidationErrorResponse},
         summary="Requisição para puxar todas as imagens dos amigurumis cadastrados")
def get_all_image():
    amigurumi_images = Image.query.order_by(desc(Image.main_image)).all()

    results = [
        {key: value for key, value in amigurumi.__dict__.items() if not key.startswith('_')}
        for amigurumi in amigurumi_images
    ]

    return jsonify(results)



@app.post('/image', tags=[image_tag], responses={"200": ImageSchema_No_Auto, "422": ValidationErrorResponse},
         summary="Requisição para cadastrar uma nova imagem de um amigurumi")
def add_image(body: ImageSchema_No_Auto):
    data = body.dict()
    amigurumi_id = int(data.get('amigurumi_id'))
    amigurumi = FoundationList.query.get(amigurumi_id)
    main_image = True if str(data.get('main_image')).lower() == "true" else False
    data["main_image"] = main_image    
    
    if not amigurumi:
        return jsonify({"error": "Amigurumi não encontrado"}), 404

    if main_image:  
        Image.query.filter_by(amigurumi_id=amigurumi_id, main_image=True).update({"main_image": False})
        db.session.commit()

    new_image = Image(**data)
    db.session.add(new_image)
    db.session.commit()

    image_id = new_image.image_id

    return jsonify({
        "message": f"Imagem salva com sucesso",
        "image_id": image_id,
    })



@app.put('/image/image_id', tags=[image_tag], responses={"200": ImageSchema_All, "422": ValidationErrorResponse},
         summary="Requisição para alterar informações sobre uma imagem cadastrada de um amigurumi")
def update_image(body: ImageSchema_All):
    data = body.dict() 
    image_id = int(data.get('image_id'))
    amigurumi_id = int(data.get('amigurumi_id'))
    main_image = str(data.get("main_image", "false")).lower() == "true"

    if main_image:  
        Image.query.filter_by(amigurumi_id=amigurumi_id, main_image=True).update({"main_image": False})
        db.session.commit()

    image_obj = Image.query.get(image_id)

    if not image_obj:
        return jsonify({"error": "Imagem não encontrada"}), 404

    for key, value in data.items():
        if hasattr(image_obj, key):
            setattr(image_obj, key, value)

    db.session.commit()

    return jsonify({
        "message": "Imagem alterada com sucesso",
        "image_id": image_obj.image_id,
    })



@app.delete('/image/image_id', tags=[image_tag], responses={"200": ImageSchema_PrimaryKey, "422": ValidationErrorResponse},
    summary="Requisição para deletar uma imagem cadastrada de um amigurumi")
def delete_image_line(body: ImageSchema_PrimaryKey):
    data = body.dict() 
    image_id = int(data.get('image_id'))
    image = Image.query.get(image_id)

    if not image:
        return jsonify({"error": "Imagem não encontrada"}), 404
    
    db.session.delete(image)
    db.session.commit()

    return jsonify({
        "message": f"Imagem {image_id} removida com sucesso!",
        "image_id": image_id,
    })



#----------------------------------- API para a tabela Material ------------------#
@app.get('/material_list', tags=[material_tag], responses={"200": MaterialListSchema_All, "422": ValidationErrorResponse},
         summary="Requisição para puxar todos os materiais utilizados na construção do amigurumi")
def get_all_material_list():
    amigurumi_material = MaterialList.query.order_by(
        cast(MaterialList.amigurumi_id, Integer).asc(),
        cast(MaterialList.list_id, Integer).asc(),
        cast(MaterialList.colour_id, Integer).asc()
    ).all()

    result = [
        {key: value for key, value in amigurumi.__dict__.items() if not key.startswith('_')}
        for amigurumi in amigurumi_material
    ]

    return jsonify(result)



@app.post('/material_list', tags=[material_tag], responses={"200": MaterialListSchema_No_Auto, "422": ValidationErrorResponse},
         summary="Requisição para cadastrar novos materiais utilizados na construção do amigurumi") 
def add_material_list(body: MaterialListSchema_No_Auto):
    data = body.dict() 
    amigurumi_id = int(data.get('amigurumi_id'))
    amigurumi = FoundationList.query.get(amigurumi_id)

    if not amigurumi:
        return jsonify({"error": "Amigurumi não encontrado"}), 404

    new_material_list = MaterialList(**data)
    db.session.add(new_material_list)
    db.session.commit()

    return jsonify({
        "message": f"Amigurumi {new_material_list.amigurumi_id} adicionado com sucesso!",
        "material_id": new_material_list.material_id,
    })



@app.put('/material_list/material_id', tags=[material_tag], responses={"200": MaterialListSchema_All, "422": ValidationErrorResponse},
         summary="Requisição para alterar um materiais utilizados na construção do amigurumi")
def update_material_list_line(body: MaterialListSchema_All):
    data = body.dict() 
    material_id = int(data.get('material_id'))
    materialListID = MaterialList.query.get(material_id)  

    if not materialListID:
        return jsonify({"error": "Material não encontrado"}), 404

    for key, value in data.items():
        if hasattr(materialListID, key):
            setattr(materialListID, key, value)

    db.session.commit()

    return jsonify({
        "message": f"Material {material_id} atualizado com sucesso!",
        "material_id": material_id,
    })



@app.delete('/material_list/material_id', tags=[material_tag], responses={"200": MaterialListSchema_PrimaryKey, "422": ValidationErrorResponse},
         summary="Requisição para deletar um materiais utilizados na construção do amigurumi")
def delete_material_list_line(body: MaterialListSchema_PrimaryKey):
    data = body.dict() 
    material_id = int(data.get('material_id'))
    materialListID = MaterialList.query.get(material_id) 

    if not materialListID:
        return jsonify({"error": "Material não encontrado"}), 404

    db.session.delete(materialListID) 
    db.session.commit() 

    return jsonify({
        "message": f"Material {material_id} foi removido com sucesso!",
        "material_id": material_id,
    })




#----------------------------------- API para a tabela StichBook Sequence ------------------------#
@app.get('/stitchbook_sequence', tags=[stichbook_sequence_tag], responses={"200": StitchBookSequenceSchema_All, "422": ValidationErrorResponse},
         summary="Requisição para puxar todas as partes cadastradas dos amigurumis")
def get_all_stichbook_sequence():
    amigurumi_stiches = StitchBookSequence.query.order_by(
        cast(StitchBookSequence.amigurumi_id, Integer).asc(),
       cast(StitchBookSequence.element_order, Integer).asc()
    ).all() 

    result = [
        {key: value for key, value in amigurumi.__dict__.items() if not key.startswith('_')}
        for amigurumi in amigurumi_stiches
    ]

    return jsonify(result)



@app.post('/stitchbook_sequence', tags=[stichbook_sequence_tag], responses={"200": StitchBookSequenceSchema_No_Auto, "422": ValidationErrorResponse},
         summary="Requisição para cadastrar uma nova parte à um amigurumi")
def add_stichbook_sequence(body: StitchBookSequenceSchema_No_Auto):
    data = body.dict() 
    amigurumi_id = int(data.get('amigurumi_id'))
    amigurumi = FoundationList.query.get(amigurumi_id)

    if not amigurumi:
        return jsonify({"error": "Amigurumi não encontrado"}), 404

    new_receita = StitchBookSequence(**data)
    db.session.add(new_receita)
    db.session.commit()

    return jsonify({
        "message": f"Linha a adicionada com sucesso!",
        "element_id": new_receita.element_id,
    })




@app.put('/stitchbook_sequence/element_id', tags=[stichbook_sequence_tag], responses={"200": StitchBookSequenceSchema_All, "422": ValidationErrorResponse},
         summary="Requisição para alterar uma parte cadastrada de um amigurumi")
def update_stichbook_sequence_element(body: StitchBookSequenceSchema_All):
    data = body.dict() 
    element_id = int(data.get('element_id'))
    elementID = StitchBookSequence.query.get(element_id)  

    if not elementID:
        return jsonify({"error": "Elemento não encontrado"}), 404

    for key, value in data.items():
        if hasattr(elementID, key):
            setattr(elementID, key, value)

    db.session.commit()

    return jsonify({
        "message": f"Linha {elementID.element_id} atualizada com sucesso!",
        "element_id": element_id,
    })




@app.delete('/stitchbook_sequence/element_id', tags=[stichbook_sequence_tag], responses={"200": StitchBookSequenceSchema_PrimaryKey, "422": ValidationErrorResponse},
         summary="Requisição para deletar uma parte cadastrada de um amigurumi")
def delete_stichbook_sequence_elementId(body: StitchBookSequenceSchema_PrimaryKey):
    data = body.dict() 
    element_id = int(data.get('element_id'))
    elementID = StitchBookSequence.query.get(element_id)  

    if not elementID:
        return jsonify({"error": "Elemento não encontrado"}), 404

    db.session.delete(elementID) 
    db.session.commit() 

    return jsonify({
        "message": f"Element_id {element_id} foi removido com sucesso!",
        "element_id": element_id,
    })