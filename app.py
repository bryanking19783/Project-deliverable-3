from flask import Flask, render_template, request, redirect, session
from sqlalchemy import create_engine, text
from Models.models import *
import hashlib

app = Flask(__name__)
app.secret_key="ImKingy"
app.config= [SQLALCHEMY_DATABASE_URI] ='mysql+mysqlconnector://root:horizon300411@localhost:3306/idata'
engine = create_engine(app.config ['SQLALCHEMY_DATABASE_URI'], echo=True)

Base.metadata.create_all(engine)

@app.route('index.html')
def index():
    return render_template('index.html')

@app.route('signup.html')
def signup():
    return render_template('signup.html')

@app.route('Login.html')
def Login():
    return render_template('Login.html')

@app.route('Login.html')
def home():
    if 'loggedin' in session:
        return render_template('index.html', username=session['username'])
    return redirect('Login.html')

@app.route('Login.html', methods=['GET', 'POST'])
def login():
    msg =""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        #get the form values
        username = request.form['Username'].lower()
        password_entered = request.form['Password']
        #decrypt the password
        hash = password_entered + app.secret_key
        hash = hashlib.sha256(hash.encode())
        password = hash.hexdigest()
        #check if the user exists in the database
        with engine.connect() as con:
            result = con.execute(text(f"Select * from user where username = '{username}' and password = '{password}'"))
            account = result.fetchone()
            con.commit()

        if account:
            session['loggedin'] = True
            session['id'] = account.id
            session['username'] = account.username
            msg = "Logged in successfully"
            return redirect('index.html', msg=msg)
        else:
            msg = "Incorrect username/password"
    return render_template('Login.html', msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg =""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        #get the form values
        Username = request.form['Username'].lower()
        Confirm_Username = request.form['Confirm Username'].lower()
        Password = request.form['Password']
        Confirm_Password = request.form['Confirm Password']
        if Username!=Confirm_Username:
            msg = "Usernames do not match"
            return render_template('signup.html', msg=msg)
        if Password!=Confirm_Password:
            msg = "Passwords do not match"
            return render_template('signup.html', msg=msg)
        with engine.connect() as con:
            result = con.execute(text(f"Select * from user where username = '{Username}'"))
            account = result.fetchone()
            con.commit()
        if account:
            msg = "Account already exists"
            return render_template('signup.html', msg=msg)
        
        if not Username or not password or not Confirm_Username or not Confirm_Password:
                msg = "Please fill out the form"
                return render_template('signup.html', msg=msg)
        else:
            #encrypt the password
            hash = password + app.secret_key
            hash = hashlib.sha256(hash.encode())
            password = hash.hexdigest()
            #insert the user into the database
            with engine.connect() as con:
                con.execute(text(f"Insert into user (username, password) values ('{Username}', '{Password}')"))
                con.commit()
            msg = "Account created successfully"
            return redirect('Login.html', msg=msg)
    return render_template('signup.html', msg=msg)





