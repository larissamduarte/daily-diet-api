from database import db

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Nome
    name = db.Column(db.String(50), nullable=False)
    # Descrição
    description = db.Column(db.String(500))
    # Quantidade de calorias
    calories = db.Column(db.Integer)
    # Data e Hora
    time = db.Column(db.Datetime, nullable=False)
    # Está dentro ou não da dieta
    on_diet = db.Column(db.Boolean, nullable=False)