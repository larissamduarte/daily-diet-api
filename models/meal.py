from database import db

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Nome
    name = db.Column(db.String(50), nullable=False)
    # Descrição
    description = db.Column(db.String(500), default="")
    # Quantidade de calorias
    calories = db.Column(db.Integer, default=0)
    # Data e Hora
    time = db.Column(db.DateTime, nullable=False)
    # Está dentro ou não da dieta
    diet = db.Column(db.Boolean, nullable=False)

    def to_dict(self):
        return {meal.name: getattr(self, meal.name) for meal in self.__table__.columns}