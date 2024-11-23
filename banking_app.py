from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash
import os


app = Flask(__name__,template_folder="./templates")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banking.db"
app.config["SECRET_KEY"] = os.urandom(24)
db = SQLAlchemy(app)

migrate = Migrate(app, db)


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(13), unique=True, nullable=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), index=True, unique=True, nullable=False)
    balance = db.Column(db.Float, default=0.0)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Account %r, Balance %r>' % (self.id, self.balance)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = Account.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            return redirect(url_for("home_page"))
        else:
            return render_template("index.html", error="Invalid email or password")

    return render_template("index.html")


@app.route("/create_account", methods=["POST"])
def create_account():
        name = request.form.get("name")
        email = request.form.get("email")
        user_id = request.form.get("user_id")
        password = request.form.get("password")


        try:
            if Account.query.filter_by(email=email).first():
                return render_template("create_account.html", error="An account with this email already exist. Please use a different email")
        
            if Account.query.filter_by(user_id=user_id).first():
                return render_template("create_account", error="An account with this ID already exist.")
            
            new_account = Account(name=name, email=email, user_id=user_id)
            new_account.set_password(password)


            db.session.add(new_account)
            db.session.commit()

            session["user_id"] = new_account.id
            return redirect(url_for("home_page"))
        
        except Exception as e:
            db.session.rollback()
            return render_template("create_account.html", error=f"An error occurred: {e}")

@app.route("/home_page", methods=["GET"])
def home_page():
    if "user_id" not in session:
        return redirect(url_for("index"))
    
    user = Account.query.get(session["user_id"])
    return render_template("home_page.html", user=user)

@app.route('/withdraw', methods=["POST"])
def withdraw():
    if "user_id" not in session:
        return redirect(url_for("index"))
    user = Account.query.get(session["user_id"])
    amount_str = request.form.get("amount")

    if not amount_str:
        flash("Please enter an amount.", "error")
        return render_template("withdraw.html", user=user, error="Please enter an amount.")

    try:
        amount = float(amount_str)
    except ValueError:
        flash("Invalid amount entered.", "error")
        return render_template("withdraw.html", user=user, error="Invalid amount entered.")

    if amount > user.balance:
        flash("Insufficient funds.", "error")
        render_template("withdraw.html", user=user, error="Insufficient funds")

    user.balance -= amount

    try:
        db.session.commit()
        flash("Withdrawal succesful!", "success")
        return redirect(url_for("home_page"))

    except Exception as e:
            db.session.rollback()
            return render_template("create_account.html", error=f"An error occurred: {e}")


@app.route('/deposit')
def deposit():
    # Logic for deposit action
    return render_template('deposit.html')

@app.route("/update_account", methods=["GET", "POST"])
def update_account():
    return "This is a placeholder for the update account functionality."

@app.route("/delete_account", methods=["GET"])
def delete_account():
    if request.method == "GET":
        name = request.form.get("name")
        email = request.form.get("email")
        user_id = request.form.get("user_id")
        password = request.form.get("password")

        print(f"Received - Name: {name}, Email: {email}, User ID: {user_id}, Password: {password}")

        try:
            user_exist_email = Account.query.filter_by(email=email).first()
            if not user_exist_email:
                return render_template("create_account.html", error="email does not exist")
        
            user_exist_id = Account.query.filter_by(user_id=user_id).first()
            if not user_exist_id:
                return render_template("create_account", error="An account with this ID does not  exist.")

        except: 
            pass
    return render_template("Delete_account.html")

@app.route("/transactions")
def transactions():
    return "This is a placeholder for the transactions functionality."


@app.route("/view_balance", methods=["GET", "POST"])
def view_balance():
    return render_template("view_balance.html")


if __name__ == "__main__":
    app.run(debug=True)