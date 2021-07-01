from flask import Flask,render_template, request, redirect, url_for
from wtforms import TextAreaField, validators
from flask_wtf import FlaskForm
from datetime import datetime
from flask_bootstrap import Bootstrap
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
import pickle
import sqlite3
import os
import numpy as np
from sklearn.externals import joblib
from flask_sqlalchemy import SQLAlchemy
loaded_model=joblib.load("./model/model.pkl")
loaded_stop=joblib.load("./model/stopwords.pkl")
loaded_vec=joblib.load("./model/vectorizer.pkl")
app = Flask(__name__)

bootstrap = Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SECRET_KEY'] = 'secrectkey'
db = SQLAlchemy(app)
class Movies(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    categorie = db.Column(db.String(200),nullable = False)
    date_created = db.Column(db.DateTime,default= datetime.utcnow)
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(15), unique = True)
    password = db.Column(db.String(80))
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4,max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4,max=15)])
@app.route('/admin')
def admin_login():
    form = LoginForm()
    return render_template("login.html",form=form)
    
def __repr__(self):
    return '<Name %r>' % self.id
def classify(document):
 label = {0: 'negative', 1: 'positive'}
 X = loaded_vec.transform([document])
 y = loaded_model.predict(X)[0]
 proba = np.max(loaded_model.predict_proba(X))
 return label[y], proba
class ReviewForm(FlaskForm):
 moviereview = TextAreaField('',[validators.DataRequired(),validators.length(min=15)])
@app.route('/add_movie', methods=['POST', 'GET'])
def add_movie():
    if request.method == "POST":
        movie_name = request.form['name']
        movie_categorie = request.form['categorie']
        new_movie = Movies(name=movie_name,categorie=movie_categorie)
        try:
            db.session.add(new_movie)
            db.session.commit()
            print("khdama katghawat")
            return redirect('add_movie')
        except:
            return "ERROR LOL"
    else:
        movies = Movies.query.order_by(Movies.date_created)
        return render_template("add_movie.html",movies = movies )
    return render_template("add_movie.html")
@app.route('/review')
def index():
 form = ReviewForm(request.form)
 return render_template('reviewform.html', form=form)
@app.route('/results', methods=['POST'])
def results():
 form = ReviewForm(request.form)
 #if request.method == 'POST' and form.validate():
 review = request.form['moviereview']
 y, proba = classify(review)
 return render_template('results.html',content=review,prediction=y,probability=round(proba*100, 2))
 return render_template('reviewform.html', form=form)
if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')

