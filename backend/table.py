from database import db
from datetime import date

class FoundationList(db.Model):
    """
    A tabela Foundation tem como objetivo listar todos os amigurumis cadastrados na base de dados, pegando apenas as suas informações básicas. 
    Esses amigurumis podem ser os principais, ou podem ser também os relacionados com a receita principal
    """
    __tablename__ = 'foundation_list'

    amigurumi_id = db.Column(db.Integer, primary_key=True, autoincrement=True, 
                    info={"description": "chave primária dos amigurumis"})
    
    date = db.Column(db.Date, default=date.today, nullable=True, 
                    info={"description": "registro da data de input"})
    
    name = db.Column(db.String(100), nullable=False, 
                    info={"description": "nome do amigurumi"})
    
    size = db.Column(db.Float(), nullable=False, 
                    info={"description": "tamanho em cm"})
    
    autor = db.Column(db.String(100), nullable=False, 
                    info={"description": "dono da receita"})
    
    link = db.Column(db.String(), 
                    info={"description": "link da receita original"})
    
    amigurumi_id_of_linked_amigurumi = db.Column(db.Integer, db.ForeignKey('foundation_list.amigurumi_id', ondelete="SET NULL"), nullable=True, 
                    info={"description": "id do amigurumi principal, no qual esta receita está relacionada"})
    

    #declaração de relacionamento
    linked_amigurumi = db.relationship('FoundationList', backref=db.backref('related_amigurumis', lazy=True), remote_side=[amigurumi_id], single_parent=True)
    materials = db.relationship("MaterialList", backref="amigurumi", cascade="all, delete-orphan", lazy=True)
    image = db.relationship("Image", backref="amigurumi", cascade="all, delete-orphan", lazy=True)
    stitchBook = db.relationship("StitchBook", backref="amigurumi", cascade="all, delete-orphan", lazy=True)
    stitchBook_sequence = db.relationship("StitchBookSequence", backref="amigurumi", cascade="all, delete-orphan", lazy=True)


    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)



class MaterialList(db.Model):
    """
    A tabela Material List tem como objetivo listar todos os materiais utilizados na construção do amigurumi
    Esta lista pode ter mais de 1 conjunto de materiais, pois há diversas formas de construir um amigurumi com a mesma receita
    """
    __tablename__ = 'material_list'

    material_list_id = db.Column(db.Integer, primary_key=True, autoincrement=True, 
                    info={"description": "chave primária dos materiais"})

    amigurumi_id = db.Column(db.Integer, db.ForeignKey('foundation_list.amigurumi_id', ondelete='CASCADE'), nullable=False, 
                    info={"description": "chave estrangeira, para indicação do amigurumi"})
    
    material_name = db.Column(db.String(100), nullable=False, 
                    info={"description": "nome do material utilizado"})

    quantity = db.Column(db.String(50), nullable=False, 
                    info={"description": "quantidade de material utilizado"})

    recipe_id = db.Column(db.Integer, nullable=False, 
                    info={"description": "define o conjunto de materiais utilizados"})

    colour_id = db.Column(db.Integer, db.ForeignKey('stitchbook.colour_id'), nullable=True, 
                    info={"description": "chave estrangeira, exclusiva para as linhas de amigurumi, para idenificação das cores"})

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)



class Image(db.Model):
    """
    A tabela Image é destinada para controle das imagens relacionadas as amigurumis
    """
    __tablename__ = 'image'

    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True, 
                    info={"description": "chave primária das imagens"})
    
    amigurumi_id = db.Column(db.Integer, db.ForeignKey('foundation_list.amigurumi_id', ondelete='CASCADE'), nullable=False, 
                    info={"description": "chave estrangeira, para indicação do amigurumi"})
    
    main_image = db.Column(db.Boolean, default = False, 
                    info={"description": "ordenação das imagens, sendo TRUE como sendo a primeira"})

    recipe_id = db.Column(db.Integer, db.ForeignKey('material_list.recipe_id'), nullable=False, 
                    info={"description": "chave estrangeira, para identificação da receita"})
    
    image_base64 = db.Column(db.String, nullable=False, 
                    info={"description": "imagem criptografada em base64"})

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)



class StitchBook(db.Model):
    """
    A tabela Stitchbook é destinada para controle todas as receitas dos amigurumis
    """
    __tablename__ = 'stitchbook'

    line_id = db.Column(db.Integer, primary_key=True, autoincrement=True, 
                    info={"description": "chave primária das carreiras"})
    
    amigurumi_id = db.Column(db.Integer, db.ForeignKey('foundation_list.amigurumi_id', ondelete='CASCADE'), nullable=False, 
                    info={"description": "chave estrangeira, para indicação do amigurumi"})
    
    observation = db.Column(db.String, nullable=False, 
                    info={"description": "comentário sobre a carreira"})
    
    element_id = db.Column(db.Integer, db.ForeignKey('stitchbook_sequence.element_id'), nullable=False, 
                    info={"description": "chave estrangeira, para identificação das partes do amigurumi"})
    
    number_row = db.Column(db.Integer, nullable=False, 
                    info={"description": "sequência das carreiras"})
    
    colour_id = db.Column(db.Integer, nullable=False, 
                    info={"description": "cor utilizada na carreira"})
    
    stich_sequence = db.Column(db.String, nullable=False, 
                    info={"description": "pontos utilizados na carreira"})

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)



class StitchBookSequence(db.Model):
    """
    A tabela Stitchbook Sequence, é uma tabela que organiza os dados da tabelas Stichbook e consolida as partes dos amigurumis
    """
    __tablename__ = 'stitchbook_sequence'

    element_id = db.Column(db.Integer, primary_key=True, autoincrement=True, 
                    info={"description": "chave primária, das partes dos amigurumis"})
    
    amigurumi_id = db.Column(db.Integer, db.ForeignKey('foundation_list.amigurumi_id', ondelete='CASCADE'), nullable=False, 
                    info={"description": "chave estrangeira, para indicação do amigurumi"})
    
    element_order = db.Column(db.Integer, nullable=False, 
                    info={"description": "ordem de construção das partes do amigurumi"})
    
    element_name = db.Column(db.String, nullable=False, 
                    info={"description": "nome das partes do amigurumi"})
    
    repetition = db.Column(db.Integer, nullable=False, 
                    info={"description": "quantidade de cada parte"})

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)