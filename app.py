from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Ad.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#login_manager = LoginManager(app)


class Ads(db.Model):
    __tablename__ = 'ads'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@app.route('/')
def index():
        ad = Ads.query.order_by(Ads.id.desc()).first()
        if len(Ads.query.all()) > 0:
            obj = Ads.query.filter(Ads.id > ad.id - 3).all()
            return render_template("index.html", obj=obj)
        return render_template("index.html")


@app.route('/ads')
def ads():
    q = request.args.get('q')
    ad = []
    if q:
        for k in Ads.query.order_by(Ads.date).all():
            if q in k.title:
                ad.append(k)
        return render_template("results.html", ads=ad)
    ad = Ads.query.order_by(Ads.date.desc()).all()
    return render_template("ads.html", ads=ad)


@app.route('/ads/<int:id>')
def ad_detail(id):
    ad = Ads.query.get(id)
    return render_template("ad-detail.html", ad=ad)


@app.route('/create-ad', methods=['POST', 'GET'])
def creteAd():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']
        ad = Ads(title=title, text=text)
        try:
            db.session.add(ad)
            db.session.commit()
            return redirect('/ads')
        except:
            return "Error"
    return render_template('create-ad.html')


@app.route('/ads/<int:id>/update', methods=['POST', 'GET'])
def ad_update(id):
    ad = Ads.query.get(id)
    if request.method == "POST":
        ad.title = request.form['title']
        ad.text = request.form['text']
        try:
            db.session.commit()
            return redirect('/ads')
        except:
            return "Error"
    return render_template("ad-update.html", ad=ad)


@app.route('/ads/<int:id>/delete', methods=['POST', 'GET'])
def ad_delete(id):
    ad = Ads.query.get_or_404(id)
    try:
        db.session.delete(ad)
        db.session.commit()
        return redirect('/ads')
    except:
        return "Error"


if __name__ == "__main__":
    app.run(debug=True)
