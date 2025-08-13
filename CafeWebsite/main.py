import os
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
API_KEY = os.environ.get('API_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'cafes.db')
db = SQLAlchemy()
db.init_app(app)
bootstrap = Bootstrap5(app)

class Cafe(db.Model):
    __tablename__ = 'cafe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.String(10), nullable=False)
    has_wifi = db.Column(db.String(10), nullable=False)
    has_sockets = db.Column(db.String(10), nullable=False)
    can_take_calls = db.Column(db.String(10), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

class CafeForm(FlaskForm):
    name = StringField('Cafe Name', validators=[DataRequired()])
    map_url = StringField('Cafe Location (Google Maps URL)', validators=[DataRequired(), URL()])
    img_url = StringField('Cafe Image (URL)', validators=[DataRequired(), URL()])
    location = StringField('Cafe Area (e.g. Peckham)', validators=[DataRequired()])
    seats = StringField('Number of Seats (e.g. 20-30)', validators=[DataRequired()])
    coffee_price = StringField('Coffee Price (e.g. £3.50)', validators=[DataRequired()])
    has_sockets = SelectField('Has Sockets?', choices=["Yes", "No"], validators=[DataRequired()])
    has_toilet = SelectField('Has a Toilet?', choices=["Yes", "No"], validators=[DataRequired()])
    has_wifi = SelectField('Has Wifi?', choices=["Yes", "No"], validators=[DataRequired()])
    can_take_calls = SelectField('Can Take Calls?', choices=["Yes", "No"], validators=[DataRequired()])
    submit = SubmitField('Add Cafe')

@app.route("/")
def home():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()
    return render_template("index.html", cafes=all_cafes, api_key=API_KEY)


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            seats=form.seats.data,
            coffee_price=form.coffee_price.data,
            has_sockets=form.has_sockets.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            can_take_calls=form.can_take_calls.data,
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', form=form)


@app.route("/delete/<int:cafe_id>")
def delete_cafe(cafe_id):
    api_key_received = request.args.get("api_key")
    if api_key_received == API_KEY:
        cafe_to_delete = db.get_or_404(Cafe, cafe_id)
        db.session.delete(cafe_to_delete)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403


if __name__ == '__main__':
    app.run(debug=True)
