from flask import Flask
from models.meal import Meal
from database import db

app = Flask(__name__)

app.config["SECRET_KEY"] = "my_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:admin123@127.0.0.1:3306/daily-diet"

db.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)