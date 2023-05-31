from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateField, FloatField
from wtforms.validators import DataRequired
import requests
    
content = []

app = Flask(__name__)

app.config['SECRET_KEY'] = '***********************'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////Users/programing/Desktop/top10.db"
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
class top(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    year = db.Column(db.Integer)
    desc = db.Column(db.String)
    ranking = db.Column(db.Integer)
    img_url = db.Column(db.String)
    rev = db.Column(db.String)

    def __repr__(self):
        return f'<Book {self.title}>'
class my(db.Model):
    _id_my = db.Column(db.Integer, primary_key=True)
    rev = db.Column(db.String)

    def __repr__(self):
        return f'<Book {self.raiting}>'
app.app_context().push()
db.create_all()
Bootstrap(app)

class addForm(FlaskForm):
    title = StringField('Name', validators=[DataRequired()])
    submit = SubmitField("Submit")
class editForm(FlaskForm):
    rating = FloatField("Change Raiting", validators=[DataRequired()])
    review = StringField("My Review", validators=[DataRequired()])
    submit = SubmitField("Done")
def search_movie(n):
    url = "https://api.themoviedb.org/3/search/movie"

    header = {
        'api_key': '*************************',
        'query': f'{n}',
        'original_language': 'en'
    }

    return requests.get(url,params=header)


@app.route("/")
def home():
    overview = db.session.query(top).all()
    return render_template("index.html", i = overview, k = 1)

@app.route("/add", methods=["GET","POST"])
def add():
    global content
    form = addForm()
    content = []
    if request.method == "POST":
        name = request.form['title']
        content = search_movie(name).json()['results']        
    return render_template('add.html', form = form, c = content)

@app.route('/redirect<k>')
def redirect_id(k):
    for i in content:
        if str(i["id"]) == str(k):
            db.session.add(top(title = i["title"], year = i['release_date'], ranking = i['vote_average'],desc = i['overview'],img_url = f'https://image.tmdb.org/t/p/w500/{i["poster_path"]}', rev = 'love it'))
            db.session.commit()
    return redirect(url_for('home'))
@app.route('/redirect/delete<k>')
def redirect_delete(k):
    deleted_item = db.session.query(top).filter(top._id == k)
    deleted_item.delete()
    db.session.commit()
    print(f"test{deleted_item}")
    return redirect(url_for('home'))
    
@app.route('/update/movie/<k>', methods=["GET","POST"])
def update(k):
    form = editForm()
    if request.method == "POST":
        review = form.data['review']
        rating = form.data['rating']
        row_for_update = db.session.query(top).get(k)
        row_for_update.ranking = rating
        row_for_update.rev = review
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', form = form)

if __name__ == '__main__':
    app.run(debug=True)
