from model import Users, Notepad
from peewee import create_model_tables
from flask import Flask, request, render_template, redirect, url_for, session
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.secret_key = 'super_secret_key'


def setup_db():
    create_model_tables([Users, Notepad], fail_silently=True)

setup_db()


@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    try:
        if request.method == 'POST':
            session['email'] = request.form['mail']
            email = request.form['mail']
            password = request.form['password']
            name = request.form['name']
            user = Users(password=password, email=email, name=name)
            user.save()
            fid = user.id
            return render_template('note.html', fid=fid, name=name)
        else:
            return render_template('signup.html')
    except:
        msg = "Email was already taken"
        return render_template('signup.html', msg=msg)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['mail']
        password = request.form['password']
        user = Users.select().where(Users.email == email).first()
        if user is not None and user.verify_password(password):
            fid = user.id
            name = user.name
            session['email'] = email
            return render_template('note.html', fid=fid, name=name)
        else:
            return "invalid password/email id"
    else:
        return render_template('signin.html')


@app.route('/save/<fid>', methods=['GET', 'POST'])
def save(fid):
    if request.method == 'POST':
        note = Notepad(area=request.form['area'], user_id=fid)
        area = request.form['area']
        note.save()
        user_id = fid
        b = Users.select().where(Users.id == user_id).first()
        msgs = Notepad.select().where(Notepad.user_id == fid)
        text = []
        for msg in msgs:
            text.append(msg.area)
        return render_template('show.html', text=text, fid=fid)


@app.route('/posts/<fid>', methods=['GET'])
def posts(fid):
    b = Users.select().where(Users.id == fid).first()
    msgs = Notepad.select().where(Notepad.user_id == fid)
    text = []
    for msg in msgs:
        text.append(msg.area)
    return render_template('show.html', text=text, fid=fid)


@app.route('/goback/<fid>')
def goback(fid):
    return render_template('note.html', fid=fid)


@app.route('/logout')
def logout():
    session.pop('email')
    return redirect(url_for('welcome'))


if __name__ == '__main__':
    app.run(debug=True)
