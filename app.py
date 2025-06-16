from datetime import datetime
from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
from models.meal import Meal
from database import db

app = Flask(__name__)
swagger = Swagger(app)

app.config["SECRET_KEY"] = "my_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db.init_app(app)

@app.route("/meal", methods=["POST"])
@swag_from("docs/add_meal.yml")
def add_meal():
    data = request.json
    name = data.get("name")
    description = data.get("description")
    calories = data.get("calories")
    time = data.get("time")
    diet = data.get("diet")

    if not name or not time:
        return jsonify({"message": "Missing required fields: 'name' and 'time'."}), 400
    
    try:
        format_time = datetime.fromisoformat(time)
    except ValueError:
        return jsonify({"message": "Invalid date format. Use ISO format."}), 400

    meal = Meal(name=name,description=description, calories=calories, time=format_time, diet=diet)
    db.session.add(meal)
    db.session.commit()
    return jsonify({"message": "Meal created."}), 201

@app.route("/meals/<time>", methods=["GET"])
@swag_from("docs/read_meals.yml")
def read_meals(time):
    try:
        format_time = datetime.fromisoformat(time)
    except ValueError:
        return jsonify({"message": "Invalid date format. Use ISO format."}), 400

    start_date = datetime.combine(format_time.date(), datetime.min.time())
    end_date = datetime.combine(format_time.date(), datetime.max.time())

    meals = Meal.query.filter(Meal.time >= start_date,
            Meal.time <= end_date).all()
    if meals:
        return jsonify([m.to_dict() for m in meals])
    else:
        return jsonify([])

@app.route("/meal/<int:id>", methods=["GET"])
@swag_from("docs/read_meal_by_id.yml")
def read_meal_by_id(id):
    meal = Meal.query.get(id)
    if meal:
        return jsonify(meal.to_dict())
    else:
        return jsonify({"message": "Meal not found."}), 404

@app.route("/meal/<int:id>", methods=["PATCH"])
@swag_from("docs/update_meal.yml")
def update_meal(id):
    data = request.json
    meal = Meal.query.get(id)
    
    if not meal:
        return jsonify({"message": "Meal not found."}), 404
    
    for field in ["name", "description", "calories", "diet"]:
        if field in data:
            setattr(meal, field, data[field])

    db.session.commit()
    return jsonify({"message": "Meal updated."})

@app.route("/meal/<int:id>", methods=["DELETE"])
@swag_from("docs/delete_meal.yml")
def delete_meal(id):
    meal = Meal.query.get(id)
    if meal:
        db.session.delete(meal)
        db.session.commit()
        return '', 204
    else:
        return jsonify({"message": "Meal not found."}), 404

if __name__ == "__main__":
    app.run(debug=True)