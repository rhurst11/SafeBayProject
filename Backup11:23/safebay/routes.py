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
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


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
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/coming_soon")
def coming_soon():
    return render_template('coming_soon.html', posts=posts)


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

    # return render_template("face_register_gate.html")



    # # User reached route via POST (as by submitting a form via POST)
    # if request.method == "POST":

    #     # Assign inputs to variables
    #     input_username = request.form.get("username")
    #     input_password = request.form.get("password")
    #     input_confirmation = request.form.get("confirmation")

    #     # Ensure username was submitted
    #     if not input_username:
    #         return render_template("register.html",messager = 1)

    #     # Ensure password was submitted
    #     elif not input_password:
    #         return render_template("register.html",messager = 2)

    #     # Ensure passwsord confirmation was submitted
    #     elif not input_confirmation:
    #         return render_template("register.html",messager = 4)

    #     elif not input_password == input_confirmation:
    #         return render_template("register.html",messager = 3)

    #     # Query database for username
    #     username = db.execute("SELECT username FROM users WHERE username = :username",
    #                           username=input_username)

    #     # Ensure username is not already taken
    #     if len(username) == 1:
    #         return render_template("register.html",messager = 5)

    #     # Query database to insert new user
    #     else:
    #         new_user = db.session.execute("INSERT INTO users (username, hash) VALUES (:username, :password)",
    #                               username=input_username,
    #                               password=generate_password_hash(input_password, method="pbkdf2:sha256", salt_length=8),)

    #         if new_user:
    #             # Keep newly registered user logged in
    #             session["user_id"] = new_user

    #         # Flash info for the user
    #         flash(f"Registered as {input_username}")

    #         # Redirect user to homepage
    #         return redirect("/")

    # # User reached route via GET (as by clicking a link or via redirect)
    # else:
    #     return render_template("register.html")




@app.route("/facereg", methods=["GET", "POST"])
def facereg():

    # return render_template("camera.html")
    # return render_template("face.html")

   
    session.clear()
    if request.method == "POST":


        encoded_image = (request.form.get("pic")+"==").encode('utf-8')
        username = request.form.get("name")
        name = db.session.execute(f"SELECT * FROM user WHERE username = '{username}'").fetchall()
        print(len(name))
              
        if len(name) != 1:
            return render_template("camera.html",message = 1)

        id_ = name[0]['id']    
        compressed_data = zlib.compress(encoded_image, 9) 
        
        uncompressed_data = zlib.decompress(compressed_data)
        
        decoded_data = b64decode(uncompressed_data)

        # img_path = ('./static/face/'+str(id_)+'.jpg', 'wb')
        
        new_image_handle = open('./static/face/'+str(id_)+'.jpg', 'wb')

        # new_image_handle = open(img_path)
        
        new_image_handle.write(decoded_data)
        new_image_handle.close()
        try:
            image_of_bill = face_recognition.load_image_file(
            './static/face/'+str(id_)+'.jpg')
        except:
            return render_template("camera.html",message = 5)

        bill_face_encoding = face_recognition.face_encodings(image_of_bill)[0]

        unknown_image = face_recognition.load_image_file(
        './static/face/'+str(id_)+'.jpg')
        try:
            unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
        except:
            return render_template("camera.html",message = 2)


#  o    mpare faces
        results = face_recognition.compare_faces(
        [bill_face_encoding], unknown_face_encoding)

        if results[0]:
            username = db.execute("SELECT * FROM user WHERE username = 'swa'")
            session["user_id"] = username[0]["id"]
            return redirect("/")
        else:
            return "You'r not allowed"
            return render_template("camera.html",message=3)


    else:
        return render_template("camera.html")




# ORIGINAL ROUTE
@app.route("/facesetup", methods=["GET", "POST"])
@login_required
def facesetup():
    if request.method == "POST":

        encoded_image = (request.form.get("pic")+"==").encode('utf-8')
        # print(session["user_id"])


        # id_ = current_user.get_id()
        # id_=db.session.execute("SELECT id FROM user WHERE id = :user_id", user_id=session["user_id"])[0]["id"]
        # id_ = db.execute("SELECT id FROM users WHERE id = :user_id", user_id=session["user_id"])[0]["id"]    
        compressed_data = zlib.compress(encoded_image, 9) 
        
        uncompressed_data = zlib.decompress(compressed_data)
        decoded_data = b64decode(uncompressed_data)

        current_user.image_file = decoded_data

        db.session.commit()



        # image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

        # img_path = Path('./static/face/'+str(id_)+'.jpg', 'wb')

        img_path = ('/Users/raymondhurst/Desktop/SafeBay_Bucket/SafeBayProject/integration_app_duplicate/safebay/static/face')

        # with open(img_path+str(id_)+'.jpg', 'w') as test: 
        #      test.write("test")

        # ('/Users/raymondhurst/Desktop/SafeBay_Bucket/SafeBayProject/integration_app_duplicate/safebay/static/face'+str(id_)+'.jpg', 'wb')
        
# ('./static/face/'+str(id_)+'.jpg', 'wb')


    #     new_image_handle = open('./static/face/'+str(id_)+'.jpg', 'wb')
    #     # new_image_handle = open(img_path)
    
    #     new_image_handle.write(decoded_data)
    #     new_image_handle.close()
    #     image_of_bill = face_recognition.load_image_file(
    #     './static/face/'+str(id_)+'.jpg')    
    #     try:
    #         bill_face_encoding = face_recognition.face_encodings(image_of_bill)[0]
    #     except:    
    #         return render_template("face.html",message = 1)
    #     return redirect("/home")

    # else:
        # return render_template("face.html")
    return render_template("face.html")


# MODIFIED FACESETUP ROUTE
# @app.route("/facesetup", methods=["GET", "POST"])
# def facesetup():
#     if request.method == "POST":


#         encoded_image = (request.form.get("pic")+"==").encode('utf-8')


#         id_=db.session.execute("SELECT id FROM users WHERE id = :user_id", user_id=session["user_id"])[0]["id"]
#         # id_ = db.execute("SELECT id FROM users WHERE id = :user_id", user_id=session["user_id"])[0]["id"]    
#         compressed_data = zlib.compress(encoded_image, 9) 
        
#         uncompressed_data = zlib.decompress(compressed_data)
#         decoded_data = b64decode(uncompressed_data)
        
#         new_image_handle = open('./static/face/'+str(id_)+'.jpg', 'wb')
        
#         new_image_handle.write(decoded_data)
#         new_image_handle.close()
#         image_of_bill = face_recognition.load_image_file(
#         './static/face/'+str(id_)+'.jpg')    
#         try:
#             bill_face_encoding = face_recognition.face_encodings(image_of_bill)[0]
#         except:    
#             return render_template("face.html",message = 1)
#         return redirect("/home")

#     else:
#         return render_template("face.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template("error.html",e = e)