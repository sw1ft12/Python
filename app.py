from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Ad.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'c4ca4238a0b923820dcc509a6f75849b'
db = SQLAlchemy(app)
manager = LoginManager(app)


class Ads(db.Model):
    #__tablename__ = 'ads'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='ads')

    def __repr__(self):
        return '<Article %r>' % self.id


class User(UserMixin, db.Model):
    #__tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(100))
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


db.create_all()


@manager.user_loader
def load_user(id):
    return db.session.query(User).get(id)


@app.route('/')
def index():
        ad = Ads.query.order_by(Ads.id.desc()).first()
        if len(Ads.query.all()) > 0:
            obj = Ads.query.filter(Ads.id > ad.id - 3).all()
            return render_template("index.html", obj=obj)
        return render_template("index.html")


@app.route('/ads')
def ads():
    ad = Ads.query.order_by(Ads.date.desc()).all()
    return render_template("ads.html", ads=ad)


@app.route('/ads/<int:id>')
def ad_detail(id):
    ad = Ads.query.get(id)
    return render_template("ad-detail.html", ad=ad)


@app.route('/create-ad', methods=['POST', 'GET'])
@login_required
def createAd():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']
        ad = Ads(title=title, text=text)
        #username = current_user.username
        #user = User.query.filter_by(username=username)
        #user.ads.append(ad)
        try:
            db.session.add(ad)
            db.session.commit()
            return redirect('/ads')
        except:
            return "Error"
    return render_template('create-ad.html')


@app.route('/ads/<int:id>/update', methods=['POST', 'GET'])
@login_required
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
@login_required
def ad_delete(id):
    ad = Ads.query.get_or_404(id)
    try:
        db.session.delete(ad)
        db.session.commit()
        return redirect('/ads')
    except:
        return "Error"


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        if not (username or password or password2):
            flash("Заполните все поля")
        elif password != password2:
            flash("Пароли не совпадают")
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(username=username, password=hash_pwd)
            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect('/')
            except:
                return "Error"

    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect('/')
            else:
                flash("Неверный логин или пароль")
        else:
            flash("Заполните все поля")

    return render_template("login.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/myads')
@login_required
def myads():
    id = current_user.id
    user = User.query.filter_by(id=id).first()
    ad = user.ads
    return render_template('myads.html', ads=ad)


if __name__ == "__main__":
    app.run(debug=True)

