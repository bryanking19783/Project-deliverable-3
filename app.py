from flask import Flask, render_template, request, redirect, session
from sqlalchemy import create_engine, text
from Models.models import *
import hashlib


app = Flask(__name__)
app.secret_key="ImKingy"
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+mysqlconnector://root:horizon300411@localhost:3306/idata'
engine = create_engine(app.config ['SQLALCHEMY_DATABASE_URI'], echo=True)

Base.metadata.create_all(engine)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/Login')
def Login():
    return render_template('Login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup_register():
    msg =""
    if request.method == 'POST' and 'Username' in request.form and 'Password' in request.form:
        #get the form values
        Username = request.form['Username'].lower()
        cusername = request.form['Confirm Username'].lower()
        Password = request.form['Password']
        cpassword = request.form['Confirm Password']
        if Username!=cusername:
            msg = "Usernames do not match"
            return render_template('signup.html', msg=msg)
        if Password!=cpassword:
            msg = "Passwords do not match"
            return render_template('signup.html', msg=msg)
        with engine.connect() as con:
            result = con.execute(text(f"Select * from users where username = '{Username}'"))
            account = result.fetchone()
            con.commit()
        if account:
            msg = "Account already exists"
            return render_template('signup.html', msg=msg)
        
        if not Username or not Password or not cusername or not cpassword:
                msg = "Please fill out the form"
                return render_template('signup.html', msg=msg)
        else:
            #encrypt the password
            hash = password + app.secret_key
            hash = hashlib.sha256(hash.encode())
            password = hash.hexdigest()
            #insert the user into the database
            with engine.connect() as con:
                con.execute(text(f"Insert into users (username, password) values ('{Username}', '{Password}')"))
                con.commit()
            msg = "Account created successfully"
            return redirect('Login.html', msg=msg)
    return render_template('signup.html', msg=msg)

