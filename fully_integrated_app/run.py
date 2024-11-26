# from flask import Flask, render_template, url_for, flash, redirect

# from flask_sqlalchemy import SQLAlchemy

# # from forms import RegistrationForm, LoginForm

# app = Flask(__name__)

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.site'

# db = SQLAlchemy(app)


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     username = db.Column(db.String(20), unique=True, nullable = False)
#     password = db.Column(db.String(60), nullable = False)
#     image_file = db.Column(db.String(20), nullable=False, default = 'default.jpg')


# def repr(__self__):
#     return f"User('{self.username}', '{self.password}', '{self.image_file}')"


#separating routes into its own modue l: routes.py


from safebay import app



if __name__ == '__main__':
    app.run(debug = True)