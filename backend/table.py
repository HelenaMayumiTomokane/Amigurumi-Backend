from database import db
from datetime import date

class FoundationList(db.Model):
    __tablename__ = 'foundation_list'

    amigurumi_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, default=date.today, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String())
    amigurumi_id_of_linked_amigurumi = db.Column(db.Integer, db.ForeignKey('foundation_list.amigurumi_id'), nullable=True)
    obs = db.Column(db.String())

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)



class MaterialList(db.Model):
    __tablename__ = 'material_list'

    material_list_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amigurumi_id = db.Column(db.Integer, db.ForeignKey('foundation_list.amigurumi_id'), nullable=False)
    material = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)



class Image(db.Model):
    __tablename__ = 'image'

    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amigurumi_id = db.Column(db.Integer, db.ForeignKey('foundation_list.amigurumi_id'), nullable=False)
    image_route = db.Column(db.String, nullable=True)
    observation = db.Column(db.String, nullable=True)
    main_image = db.Column(db.Boolean, default = False)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)



class StitchBook(db.Model):
    __tablename__ = 'stitchbook'

    line_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amigurumi_id = db.Column(db.Integer, db.ForeignKey('foundation_list.amigurumi_id'), nullable=False)
    observation = db.Column(db.String, nullable=False)
    element = db.Column(db.String(100), nullable=False)
    number_row = db.Column(db.Integer, nullable=False)
    colour = db.Column(db.Integer, nullable=False)
    stich_sequence = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)