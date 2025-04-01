from database import db
from datetime import date

class FoundationList(db.Model):
    """
    A tabela Foundation tem como objetivo listar todos os amigurumis cadastrados na base de dados, pegando apenas as suas informações básicas. 
    Esses amigurumis podem ser os principais, ou podem ser também os relacionados com a receita principal
    """
    __tablename__ = 'foundation_list'

    amigurumi_id = db.Column(db.Integer, primary_key=True, autoincrement=True, 
                    info={"description": "chave primária dos amigurumis, usada para relacionar todas as tabelas pelo amigurumi_id e são adicionadas automaticamente pelo código"})
    
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



class MaterialList(db.Model):
    """
    A tabela Material List tem como objetivo listar todos os materiais utilizados na construção do amigurumi
    Esta lista pode ter mais de 1 receita por amigurumi, pois há diversas formas de construir um amigurumi com a mesma receita
    """
    __tablename__ = 'material_list'

    material_list_id = db.Column(db.Integer, primary_key=True, autoincrement=True, 
                    info={"description": "chave primária dos materiais utilizados na construção do amigurumi e são adicionadas automaticamente pelo código"})

    amigurumi_id = db.Column(db.Integer, db.ForeignKey('foundation_list.amigurumi_id'), nullable=False, 
                    info={"description": "chave estrangeira, para localização dos dados do amigurumi"})
    
    material_name = db.Column(db.String(100), nullable=False, 
                    info={"description": "registro do material utilizado na construção do amigurumi"})

    quantity = db.Column(db.String(50), nullable=False, 
                    info={"description": "quantidade de material utilizado na constução do amigurumi"})

    recipe_id = db.Column(db.Integer, nullable=False, 
                    info={"description": "o número da receita, que esse material é referente"})

    colour_id = db.Column(db.Integer, db.ForeignKey('stitchbook.colour_id'), nullable=False, 
                    info={"description": "este é um caso exclusivo para as linhas, no qual esse número é para dar match com o colour_id da tabela stitchbook"
                    "para identificação de qual cor, é utilizada para cada carreira"})

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)



class Image(db.Model):
    """
    A tabela Image é destinada para o cadastro de todas as imagens referente aos amigurumis
    """
    __tablename__ = 'image'

    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True, 
                    info={"description": "chave primária das imagens dos amigurumis e são adicionadas automaticamente pelos códigos"})
    
    amigurumi_id = db.Column(db.Integer, db.ForeignKey('foundation_list.amigurumi_id'), nullable=False, 
                    info={"description": "chave estrangeira, para localização dos dados do amigurumi"})
    
    image_route = db.Column(db.String, nullable=True, 
                    info={"description": "esta informação é gerada automaticamente ao adicionar o arquivo"})
    
    main_image = db.Column(db.Boolean, default = False, 
                    info={"description": "definição se a imagem deve ser a primeira a aparacere, sendo TRUE como a principal"})

    recipe_id = db.Column(db.Integer, db.ForeignKey('material_list.recipe_id'), nullable=False, 
                    info={"description": "número utilizado para classificar os materiais utilizados na receita, no qual a imagem está atrelada"})

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)



class StitchBook(db.Model):
    """
    A tabela Stitchbook é destinada para o cadastro das receitas
    """
    __tablename__ = 'stitchbook'

    line_id = db.Column(db.Integer, primary_key=True, autoincrement=True, 
                    info={"description": "chave primária das carreiras das receitas dos amigurumis e são adicionadas automaticamente pelo código"})
    
    amigurumi_id = db.Column(db.Integer, db.ForeignKey('foundation_list.amigurumi_id'), nullable=False, 
                    info={"description": "chave estrangeira, para localização dos dados do amigurumi"})
    
    observation = db.Column(db.String, nullable=False, 
                    info={"description": "comentário sobre a linha da receita"})
    
    element_id = db.Column(db.Integer, db.ForeignKey('stitchbook_sequence.element_id'), nullable=False, 
                    info={"description": "chave estrangeira, para conectar com a tabela stitchbook_sequence"})
    
    number_row = db.Column(db.Integer, nullable=False, 
                    info={"description": "número da carreira da receita"})
    
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
                    info={"description": "chave primária, para as partes dos amigurumis e são adicionadas automaticamente pelo código"})
    
    amigurumi_id = db.Column(db.Integer, db.ForeignKey('foundation_list.amigurumi_id'), nullable=False, 
                    info={"description": "chave estrangeira, para definição do amigurumi"})
    
    element_order = db.Column(db.Integer, nullable=False, 
                    info={"description": "ordem de construção das partes do amigurumi"})
    
    element_name = db.Column(db.String, nullable=False, 
                    info={"description": "nome das partes do amigurumi"})
    
    repetition = db.Column(db.Integer, nullable=False, 
                    info={"description": "número de vezes em que uma parte deve ser repetida"})

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)