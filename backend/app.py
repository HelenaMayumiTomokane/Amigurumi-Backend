from flask import request, jsonify, render_template,redirect
from flask_cors import CORS
from database import db
from config import DevelopmentConfig
from table import *
import os
from flask_openapi3 import OpenAPI, Info, Tag
from errorSchema import *
from schema import *
from sqlalchemy import desc, cast, Integer

UPLOAD_FOLDER = "backend/bd_image"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

info = Info(title="Minha API de Amigurumi", version="1.0.0", description="API para gerenciar amigurumis, receitas, imagens e materiais.")
app = OpenAPI(__name__, info=info)

app.config["SQLALCHEMY_DATABASE_URI"] = DevelopmentConfig.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = DevelopmentConfig.SQLALCHEMY_TRACK_MODIFICATIONS

openAPI_tag = Tag(name="OpenAPI", description="Endpoints para geração da documentação dos APIs")
foundation_tag = Tag(name="Foudantion", description="Endpoints relacionados à lista de amigurumis")
foundation_element_tag = Tag(name="Foudantion Element", description="Endpoints relacionados elementos e sua ordem de execução, dos amigurumis")
stichbook_tag = Tag(name="Stichbook", description="Endpoints relacionados às carreiras das receitas")
image_tag = Tag(name="Image", description="Endpoints relacionados à imagem do amigurumi")
material_tag = Tag(name="Material", description="Endpoints relacionados ao material utilizado na construção dos amigurumis")

CORS(app)



#----------------------------------- Criar Rotas ------------------------------#
@app.get('/<page>')
def render_page(page):
    try:
        return render_template(f'{page}.html')
    except:
        return "Página não encontrada", 404
db.init_app(app)



#----------------------------------- Criar tabelas automaticamente ------------------------------#
with app.app_context():
    db.create_all() 



#----------------------------------- API Swagger ------------------------------#

@app.get('/openapi', tags=[openAPI_tag])
def openapi():
    doc_type = request.args.get('doc', 'swagger') 

    if doc_type == 'redoc':
        return redirect("http://127.0.0.1:5000/redoc")
    
    elif doc_type == 'rapidoc':
        return redirect("http://127.0.0.1:5000/rapidoc")
    
    elif doc_type == 'swagger':
        return redirect("http://127.0.0.1:5000/swagger")
    
    elif doc_type == 'scalar':
        return redirect("http://127.0.0.1:5000/scalar")
    
    elif doc_type == 'rapipdf':
        return redirect("http://127.0.0.1:5000/rapipdf")
    
    elif doc_type == 'elements':
        return redirect("http://127.0.0.1:5000/elements")


#-----------------------------------API Foundation List Table----------#
@app.get('/foundation_list', tags=[foundation_tag], responses={"200": FoundationListSchema_All, "404":ErrorResponse},
         summary="Requisição para puxar todos os amigurumis listados no banco de dados")
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




@app.post('/foundation_list', tags=[foundation_tag], responses={"200": FoundationListSchema_All, "404":ErrorResponse},
         summary="Requisição para imputar um novo amigurumi no banco de dados")
def add_foundation_list():
    data = request.get_json()
    new_amigurumi = FoundationList()

    for key, value in data.items():
        if hasattr(new_amigurumi, key): 
            setattr(new_amigurumi, key, value) 

    db.session.add(new_amigurumi)
    db.session.commit()

    return jsonify({
        "message": f"Amigurumi '{new_amigurumi.name}' adicionado com sucesso!",
        "amigurumi_id": new_amigurumi.amigurumi_id
    })




@app.put('/foundation_list/amigurumi_id', tags=[foundation_tag], responses={"200": FoundationListSchema_All, "404":ErrorResponse},
         summary="Requisição para alterar dados do amigurumi no banco de dados")
def update_foundation_list():
    data = request.get_json()
    amigurumi_id = int(data.get('amigurumi_id'))

    amigurumi = FoundationList.query.get(amigurumi_id)  

    if not amigurumi:
        return jsonify({"error": "Amigurumi não encontrado"}), 404

    for key, value in data.items():
        if hasattr(amigurumi, key):
            setattr(amigurumi, key, value)

    db.session.commit()

    return jsonify({
        "message": f"Amigurumi '{amigurumi.name}' atualizado com sucesso!",
        "amigurumi_id": amigurumi.amigurumi_id
    })




@app.delete('/foundation_list/amigurumi_id', tags=[foundation_tag], responses={"200": FoundationListSchema_AmigurumiID, "404":ErrorResponse},
         summary="Requisição para deletar os dados do amigurumi do banco de dados")
def delete_foundation_list():
    data = request.get_json()
    amigurumi_id = int(data.get('amigurumi_id'))
    amigurumi = FoundationList.query.get(amigurumi_id) 

    if not amigurumi:
        return jsonify({"error": "Amigurumi não encontrado"}), 404

    db.session.delete(amigurumi) 
    db.session.commit() 

    return jsonify({
        "message": f"Amigurumi '{amigurumi.name}' removido com sucesso!",
        "amigurumi_id": amigurumi.amigurumi_id
    })




#-----------------------------------API StichBook Table------------------------#
@app.get('/stitchbook', tags=[stichbook_tag], responses={"200": StitchBookSchema_All, "404": ErrorResponse},
         summary="Requisição para puxar todas as linhas de receita, para a fabricação do amigurumi")
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



@app.post('/stitchbook', tags=[stichbook_tag], responses={"200": StitchBookSchema_All, "404":ErrorResponse},
         summary="Requisição para adicionar uma nova linha de receita, para a fabricação do amigurumi")
def add_stichbook():
    data = request.get_json()

    amigurumi_id = data.get('amigurumi_id')

    amigurumi = FoundationList.query.get(amigurumi_id)
    if not amigurumi:
        return jsonify({"error": "Amigurumi não cadastrado"}), 404

    new_receita = StitchBook(**data)
    db.session.add(new_receita)
    db.session.commit()

    return jsonify({
        "message": f"Linha a adicionada com sucesso!",
        "amigurumi_id": amigurumi.amigurumi_id,
        "line_id": new_receita.line_id,
    })



@app.put('/stitchbook/line_id', tags=[stichbook_tag], responses={"200": StitchBookSchema_All, "404":ErrorResponse},
         summary="Requisição para alterar uma linha de receita")
def update_stichbook_line():
    data = request.get_json()
    line_id = int(data.get('line_id'))

    amigurumi = StitchBook.query.get(line_id)  

    if not amigurumi:
        return jsonify({"error": "Amigurumi não encontrado"}), 404

    for key, value in data.items():
        if hasattr(amigurumi, key):
            setattr(amigurumi, key, value)

    db.session.commit()

    return jsonify({
        "message": f"Linha '{amigurumi.line_id}' atualizada com sucesso!",
    })




@app.delete('/stitchbook/amigurumi_id', tags=[stichbook_tag], responses={"200": StitchBookSchema_AmigurumiID, "404":ErrorResponse},
         summary="Requisição para deletar todas as linhas de uma amigurumi em específico")
def delete_stichbook_all():
    data = request.get_json()
    amigurumi_id = int(data.get('amigurumi_id'))
    amigurumis = StitchBook.query.filter(StitchBook.amigurumi_id == amigurumi_id).all()

    if not amigurumis:
        return jsonify({"error": "Amigurumi não encontrado"}), 404

    for amigurumi in amigurumis:
        db.session.delete(amigurumi)
    
    db.session.commit()

    return jsonify({
        "message": f"Todas as receitas do Amigurumi com amigurumi_id '{amigurumi_id}' foram removidas com sucesso!",
    })




@app.delete('/stitchbook/line_id', tags=[stichbook_tag], responses={"200": StitchBookSchema_LineID, "404":ErrorResponse},
         summary="Requisição para deletar uma linha de receita")
def delete_stichbook_line():
    data = request.get_json()
    line_id = int(data.get('line_id'))
    amigurumi = StitchBook.query.get(line_id) 

    if not amigurumi:
        return jsonify({"error": "Amigurumi não encontrado"}), 404

    db.session.delete(amigurumi) 
    db.session.commit() 

    return jsonify({
        "message": f"Linha '{amigurumi.line_id}' removida com sucesso!",
    })



#-----------------------------------API Image Table -------------------#
@app.get('/image', tags=[image_tag], responses={"200": ImageSchema_All, "404":ErrorResponse},
         summary="Requisição para puxar todas as imagens disponíveis dos amigurumis no banco de dados")
def get_all_image():
    amigurumi_images = Image.query.order_by(desc(Image.main_image)).all()

    results = [
        {key: value for key, value in amigurumi.__dict__.items() if not key.startswith('_')}
        for amigurumi in amigurumi_images
    ]

    return jsonify(results)



@app.delete('/image/amigurumi_id', tags=[image_tag], responses={"200": ImageSchema_AmigurumiID, "404":ErrorResponse},
         summary="Requisição para remover todas as imagens disponíveis no banco de dados, de um amigurumi em específico")
def delete_image_all():
    data = request.get_json()
    amigurumi_id = int(data.get('amigurumi_id'))
    amigurumis = Image.query.filter(Image.amigurumi_id == amigurumi_id).all()

    if not amigurumis:
        return jsonify({"error": "Amigurumi não encontrado"}), 404

    for amigurumi in amigurumis:
        file_path = os.path.join(UPLOAD_FOLDER, amigurumi.image_route)

        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                return jsonify({"error": f"Erro ao deletar o arquivo: {str(e)}"}), 500
        else:
            return jsonify({"error": f"Arquivo {amigurumi.image_route} não encontrado no sistema de arquivos"}), 404

        db.session.delete(amigurumi)

    db.session.commit()

    return jsonify({
        "message": f"Todas as imagens do Amigurumi '{amigurumi_id}' foram removidas com sucesso!",
    })




@app.delete('/image/image_id', tags=[image_tag], responses={"200": ImageSchema_ImageID, "404":ErrorResponse},
         summary="Requisição para deletar apenas uma imagem do amigurumi no banco de dados")  # Remover 1 imagem do amigurumi
def delete_image_line():
    data = request.get_json()
    image_id = int(data.get('image_id'))
    image = Image.query.get(image_id)

    if not image:
        return jsonify({"error": "Imagem não encontrada"}), 404

    file_path = os.path.join(UPLOAD_FOLDER, image.image_route)

    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            return jsonify({"error": f"Erro ao deletar o arquivo: {str(e)}"}), 500
    else:
        return jsonify({"error": "Arquivo não encontrado no sistema de arquivos"}), 404
    
    db.session.delete(image)
    db.session.commit()

    return jsonify({
        "message": f"Imagem com ID {image_id} removida com sucesso!",
    })


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.post('/image', tags=[image_tag], responses={"200": ImageSchema_All, "404": ErrorResponse},
         summary="Requisição para adicionar uma nova imagem do amigurumi no banco de dados")
def add_image():
    data = request.form
    data = data.to_dict()

    amigurumi_id = data.get("amigurumi_id")
    amigurumi = FoundationList.query.get(amigurumi_id)

    main_image = True if str(data.get("main_image")).lower() == "true" else False
    data["main_image"] = main_image    

    image_route = request.files.get('image_route')
    if not image_route:
        return jsonify({"error": "Imagem não fornecida"}), 400

    if not amigurumi:
        return jsonify({"error": "amigurumi_id não encontrado"}), 404

    
    if not image_route:
        return jsonify({"error": "A URL da imagem (image_route) é obrigatória"}), 400

    if main_image:  
        Image.query.filter_by(amigurumi_id=amigurumi_id, main_image=True).update({"main_image": False})
        db.session.commit()

    new_image = Image(**data)
    db.session.add(new_image)
    db.session.commit()

    image_id = new_image.image_id
    unique_name = f"image_id_{image_id}.png" 
    file_path = os.path.join(UPLOAD_FOLDER, unique_name)
    
    image_route.save(file_path)

    new_image.main_image = main_image
    new_image.image_route = unique_name
    db.session.commit()

    return jsonify({
        "message": f"Imagem salva com sucesso no caminho: {file_path}",
        "image_path": file_path
    })



@app.put('/image/image_id', tags=[image_tag], responses={"200": ImageSchema_All, "404": ErrorResponse},
         summary="Requisição para alterar informações sobre uma imagem")
def update_image():
    data = request.get_json()

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
        "image_id": image_obj.image_id
    })





#-----------------------------------API Material Table------------------#

@app.post('/material_list', tags=[material_tag], responses={"200": MaterialListSchema_All, "404":ErrorResponse},
         summary="Requisição para adicionar novos materiais utilizados na construção do amigurumi") 
def add_material_list():
    data = request.get_json()
    amigurumi_id = int(data.get('amigurumi_id'))
    amigurumi = FoundationList.query.get(amigurumi_id)

    if not amigurumi:
        return jsonify({"error": "amigurumi_id não encontrado"}), 404

    new_material_list = MaterialList(**data)

    db.session.add(new_material_list)
    db.session.commit()

    return jsonify({
        "message": f"Amigurumi '{new_material_list.amigurumi_id}' adicionado com sucesso!",
    })


@app.get('/material_list', tags=[material_tag], responses={"200": MaterialListSchema_All, "404":ErrorResponse},
         summary="Requisição para puxar todos os materiais utilizados na construção do amigurumi")
def get_all_material_list():
    amigurumi_material = MaterialList.query.all()

    result = [
        {key: value for key, value in amigurumi.__dict__.items() if not key.startswith('_')}
        for amigurumi in amigurumi_material
    ]

    return jsonify(result)



@app.put('/material_list/material_list_id', tags=[material_tag], responses={"200": MaterialListSchema_All, "404":ErrorResponse},
         summary="Requisição para alterar um materiais utilizados na construção do amigurumi")
def update_material_list_line():
    data = request.get_json()
    material_list_id = int(data.get('material_list_id'))

    amigurumi = MaterialList.query.get(material_list_id)  

    if not amigurumi:
        return jsonify({"error": "Amigurumi não encontrado"}), 404

    for key, value in data.items():
        if hasattr(amigurumi, key):
            setattr(amigurumi, key, value)

    db.session.commit()

    return jsonify({
        "message": f"Material '{amigurumi.material_list_id}' atualizado com sucesso!",
    })




@app.delete('/material_list/amigurumi_id', tags=[material_tag], responses={"200": MaterialListSchema_AmigurumiID, "404":ErrorResponse},
         summary="Requisição para deletar todos os materiais utilizados na construção de um amigurumi em específico")
def delete_material_list_all():
    data = request.get_json()
    amigurumi_id = int(data.get('amigurumi_id'))
    amigurumis = MaterialList.query.filter(MaterialList.amigurumi_id == amigurumi_id).all()

    if not amigurumis:
        return jsonify({"error": "Amigurumi não encontrado"}), 404

    for amigurumi in amigurumis:
        db.session.delete(amigurumi)
    
    db.session.commit()

    return jsonify({
        "message": f"Todos os materiais do amigurumi '{amigurumi_id}' foram removidas com sucesso!",
    })




@app.delete('/material_list/material_list_id', tags=[material_tag], responses={"200": MaterialListSchema_MaterialID, "404":ErrorResponse},
         summary="Requisição para deletar um materiais utilizados na construção do amigurumi")
def delete_material_list_line():
    data = request.get_json()
    material_list_id = int(data.get('material_list_id'))
    amigurumi = MaterialList.query.get(material_list_id) 

    if not amigurumi:
        return jsonify({"error": "Amigurumi não encontrado"}), 404

    db.session.delete(amigurumi) 
    db.session.commit() 

    return jsonify({
        "message": f"Material '{amigurumi.material_list_id}' foi removido com sucesso!",
    })




#-----------------------------------API StichBook Sequence Table------------------------#
@app.get('/stitchbook_sequence', tags=[stichbook_tag], responses={"200": StitchBookSequenceSchema_All, "404":ErrorResponse},
         summary="Requisição para puxar todos os elementos de uma receita")
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



@app.post('/stitchbook_sequence', tags=[stichbook_tag], responses={"200": StitchBookSequenceSchema_All, "404":ErrorResponse},
         summary="Requisição para adicionar um novo elemento a uma receita")
def add_stichbook_sequence():
    data = request.get_json()

    amigurumi_id = data.get('amigurumi_id')

    amigurumi = FoundationList.query.get(amigurumi_id)
    if not amigurumi:
        return jsonify({"error": "Amigurumi não cadastrado"}), 404

    new_receita = StitchBookSequence(**data)
    db.session.add(new_receita)
    db.session.commit()

    return jsonify({
        "message": f"Linha a adicionada com sucesso!",
        "amigurumi_id": amigurumi.amigurumi_id,
        "element_id": new_receita.element_id,
    })




@app.put('/stitchbook_sequence/element_id', tags=[stichbook_tag], responses={"200": StitchBookSequenceSchema_All, "404":ErrorResponse},
         summary="Requisição para alterar um elemento de uma receita")
def update_stichbook_sequence_element():
    data = request.get_json()
    element_id = int(data.get('element_id'))

    elementID = StitchBookSequence.query.get(element_id)  

    if not elementID:
        return jsonify({"error": "Elemento não encontrado"}), 404

    for key, value in data.items():
        if hasattr(elementID, key):
            setattr(elementID, key, value)

    db.session.commit()

    return jsonify({
        "message": f"Linha '{elementID.element_id}' atualizada com sucesso!",
    })




@app.delete('/stitchbook_sequence/element_id', tags=[stichbook_tag], responses={"200": StitchBookSequenceSchema_ElementID, "404":ErrorResponse},
         summary="Requisição para deletar um elemento de uma receita")
def delete_stichbook_sequence_elementId():
    data = request.get_json()
    element_id = int(data.get('element_id'))
    element_ids = StitchBookSequence.query.filter(StitchBookSequence.element_id == element_id).all()

    if not element_ids:
        return jsonify({"error": "Amigurumi não encontrado"}), 404

    for element_id in element_ids:
        db.session.delete(element_id)
    
    db.session.commit()

    return jsonify({
        "message": f"Element_id '{element_id}' foi removido com sucesso!",
    })