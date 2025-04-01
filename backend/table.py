from database import db
from datetime import date

class FoundationList(db.Model):
    """
    A tabela Foundation tem como objetivo listar todos os amigurumis cadastrados na base de dados, pegando apenas as suas informações básicas. 
    Esses amigurumis podem ser os principais, ou podem ser também os relacionados com a receita principal
    """
    __tablename__ = 'foundation_list'

    amigurumi_id = db.Column(db.Integer, primary_key=True, autoincrement=True, 
                    info={"description": "é a chave primária dos amigurumis, usada para relacionar todas as tabelas, e puxar todas as informações referentes aquele amigurumi"})
    
    date = db.Column(db.Date, default=date.today, nullable=False, 
                    info={"description": "registro da data de cadastramento desse amigurumi, adicionado automaticamente pelo código"})
    
    name = db.Column(db.String(100), nullable=False, 
                    info={"description": "nome dado para o amigurumi, que será utilizado para localiza-lo pelo front"})
    
    size = db.Column(db.Integer, nullable=False, 
                    info={"description": "registro do tamanho do amigurumi em cm"})
    
    autor = db.Column(db.String(100), nullable=False, 
                    info={"description": "registro de dono da receita"})
    
    link = db.Column(db.String(), 
                    info={"description": "registro do link original da receita"})
    
    amigurumi_id_of_linked_amigurumi = db.Column(db.Integer, db.ForeignKey('foundation_list.amigurumi_id'), nullable=True, 
                    info={"description": "registro do id do amigurumi principal, no qual esta receita está relacionada"})
    
    obs = db.Column(db.String(), 
                    info={"description": "comentários sobre o amigurumi"})

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


# A tabela Material List tem como objetivo listar todos os materiais utilizados na construção do amigurumi
# Esta lista pode ter mais de 1 receita por amigurumi, pois há diversas formas de construir um amigurumi com a mesma receita
class MaterialList(db.Model):
    __tablename__ = 'material_list'

    material_list_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amigurumi_id = db.Column(db.Integer, db.ForeignKey('foundation_list.amigurumi_id'), nullable=False)
    material = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(50), nullable=False)
    material_class = db.Column(db.String(100), nullable=False)
    recipe_id = db.Column(db.Integer, nullable=False)
    colour_id = db.Column(db.Integer, db.ForeignKey('stitchbook.colour_id'), nullable=False)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


# A tabela Image é destinada para o cadastro de todas as imagens referente aos amigurumis, linkando-as com as receitas utilizadas, e
# podendo definir uma uma imagem principal (main_image), para ser sempre mostrada como primeira
class Image(db.Model):
    __tablename__ = 'image'

    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amigurumi_id = db.Column(db.Integer, db.ForeignKey('foundation_list.amigurumi_id'), nullable=False)
    image_route = db.Column(db.String, nullable=True)
    observation = db.Column(db.String, nullable=True)
    main_image = db.Column(db.Boolean, default = False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('material_list.recipe_id'), nullable=False)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


# A tabela Stitchbook é destinada para o cadastro das receitas
class StitchBook(db.Model):
    __tablename__ = 'stitchbook'

    line_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amigurumi_id = db.Column(db.Integer, db.ForeignKey('foundation_list.amigurumi_id'), nullable=False)
    observation = db.Column(db.String, nullable=False)
    element_id = db.Column(db.Integer, db.ForeignKey('stitchbook_sequence.element_id'), nullable=False)
    number_row = db.Column(db.Integer, nullable=False)
    colour_id = db.Column(db.Integer, nullable=False)
    stich_sequence = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


# A tabela Stitchbook Sequence, é uma tabela que organiza os dados da tabelas Stichbook e consolida as partes dos amigurumis
class StitchBookSequence(db.Model):
    __tablename__ = 'stitchbook_sequence'

    element_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amigurumi_id = db.Column(db.Integer, db.ForeignKey('foundation_list.amigurumi_id'), nullable=False)
    element_order = db.Column(db.Integer, nullable=False)
    element_name = db.Column(db.String, nullable=False)
    repetition = db.Column(db.Integer, nullable=False)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)