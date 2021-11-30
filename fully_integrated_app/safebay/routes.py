from pathlib import Path
from flask import render_template, url_for, flash, redirect, request, session, Response
from flask_session import Session
from safebay import app, db, bcrypt
from safebay.forms import AuthenticationForm, RegistrationForm, LoginForm, UpdateAccountForm, AuthenticationForm
from safebay.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required

# all imports from facelogin app, slowly whittling down
import os
import re
import io
import zlib
from werkzeug.utils import secure_filename
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session ,url_for
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import face_recognition
from PIL import Image
from base64 import b64encode, b64decode
import re


from pathlib import Path



posts = [
    {
        'author': 'example user',
        'wallet_name': 'Metamask Wallet 1 Recovery Phrase',
        'seedphrase': 'DISCLAIMER THIS IS A PROOF OF CONCEPT, DO NOT ATTEMPT TO POST ANY SEEDPHRASE INFORMATION UNTIL WE CONDUCT A 3RD-PARTY SECURITY AUDIT',
        'date_posted': 'November 26, 2021'

    },
    {
        'author': 'example user',
        'wallet_name': 'Ledger Nano S Recovery Phrase',
        'seedphrase': 'DISCLAIMER THIS IS A PROOF OF CONCEPT, DO NOT ATTEMPT TO POST ANY SEEDPHRASE INFORMATION UNTIL WE CONDUCT A 3RD-PARTY SECURITY AUDIT',
        'date_posted': 'November 23, 2021'
        
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created, you are now able to login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        # if form.email.data == 'admin@blog.com' and form.password.data == 'password':
        #     flash('You have been logged in!', 'success')
        #     return redirect(url_for('home'))
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    # image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    # return render_template('account.html', title='Account', image_file=image_file, form=form)
    return render_template('account.html', title='Account', form=form)

@app.route("/coming_soon")
def coming_soon():
    return render_template('coming_soon.html')

@app.route("/fuckinshit")
def fuckinshit():
    return render_template('fuckinshit.html"')


# starting to integrate from functional facelogin app

@app.route("/authentication", methods=["GET", "POST"])
@login_required
def authentication():
    """Register user"""

    # TRYING TO ADD FORM LOGIC WITH FLASK FORMS REFER TO FORMS.PY
    form = AuthenticationForm()
    if form.validate_on_submit():
        # if form.email.data == 'admin@blog.com' and form.password.data == 'password':
        #     flash('You have been logged in!', 'success')
        #     return redirect(url_for('home'))
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # return render_template("camera.html")
            return redirect("facesetup")
        else:
            flash('Authentication Unsuccessful. Please check email and password', 'danger')
    return render_template('face_register_gate.html', title='Authentication', form=form)



# Face Setup ROUTE
@app.route("/facesetup", methods=["GET", "POST"])
@login_required
def facesetup():
    if request.method == "POST":

        image = (request.form.get("pic"))

        encoded_image = (request.form.get("pic")+"==").encode('utf-8')
        # print(session["user_id"])


        id_ = current_user.get_id()
        # id_=db.session.execute("SELECT id FROM user WHERE id = :user_id", user_id=session["user_id"])[0]["id"]
        # id_ = db.execute("SELECT id FROM users WHERE id = :user_id", user_id=session["user_id"])[0]["id"]    
        compressed_data = zlib.compress(encoded_image, 9) 
        
        uncompressed_data = zlib.decompress(compressed_data)
        decoded_data = b64decode(uncompressed_data)

        # (TO ADD DECODED DATA TO DATABASE)
        # current_user.image_file = decoded_data
        # db.session.commit()

        # safebay/static/face/test_pic_capture1.jpg

        img_path = ('./safebay/static/face/test_pic_capture{}.jpg').format(id_)
        print(img_path)

        open (img_path, 'w').close()
        
        new_image_handle = open(img_path, 'wb')
        # print(new_image_handle)
        final_pic = new_image_handle.write(decoded_data)
        final_pic
        new_image_handle.close()

        current_user.image_file = final_pic
        db.session.commit()


    return render_template("face.html")


# Face Recognition / Comparison Route
@app.route("/facereg", methods=["GET", "POST"])
def facereg():

   
    # session.clear()
    if request.method == "POST":


        encoded_image = (request.form.get("pic")+"==").encode('utf-8')
        
        username = request.form.get("name")
        name = db.session.execute(f"SELECT * FROM user WHERE username = '{username}'").fetchall()
        print(len(name))
              
        if len(name) != 1:
            return render_template("camera.html",message = 1)


        # UPDATED ID RETRIEVAL TEST
        id_ = current_user.get_id()
        print(id_)

        compressed_data = zlib.compress(encoded_image, 9) 
        
        uncompressed_data = zlib.decompress(compressed_data)
        
        decoded_data = b64decode(uncompressed_data)

        # img_path = ('./static/face/'+str(id_)+'.jpg', 'wb')

        img_path = ('./safebay/static/face/test_pic_capture{}.jpg').format(id_)

        face_trial_img_path = ('./safebay/static/face_trial/test_pic_capture{}.jpg').format(id_)
        print(face_trial_img_path)

        open (face_trial_img_path, 'w').close()
        
        # new_image_handle = open('./static/face/'+str(id_)+'.jpg', 'wb')

        # new_image_handle = open(img_path)
        

        new_image_handle = open(face_trial_img_path, 'wb')
        new_image_handle.write(decoded_data)
        new_image_handle.close()
        try:
            image_of_bill = face_recognition.load_image_file(img_path)
        except:
            return render_template("camera.html",message = 5)

        bill_face_encoding = face_recognition.face_encodings(image_of_bill)[0]

        unknown_image = face_recognition.load_image_file(face_trial_img_path)
        try:
            unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
        except:
            return render_template("camera.html",message = 2)


#  compare faces
        results = face_recognition.compare_faces(
        [bill_face_encoding], unknown_face_encoding)

        if results[0]:
            # username = db.execute("SELECT * FROM user WHERE username = 'swa'")
            # session["user_id"] = username[0]["id"]
            return redirect("seed")
        else:
            return "You're not allowed"
            return render_template("camera.html",message=3)


    else:
        return render_template("camera.html")

@app.route("/seed")
@login_required
def seed():
    return render_template("seed.html", posts=posts)

@app.route("/whitepaper")
def whitepaper():
    return render_template("whitepaper.html")

@app.route("/whitelist")
def whitelist():
    return render_template("whitelist.html")

@app.route("/token_allocation")
def token_allocation():
    return render_template("token_allocation.html")    

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template("error.html",e = e)