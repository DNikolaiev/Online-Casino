from flask_wtf import FlaskForm
from wtforms import TextField, StringField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, PasswordField
from flask import Flask, render_template, request, flash
from wtforms import validators, ValidationError


class LoginForm(FlaskForm):

   login = StringField("Login",[ validators.DataRequired("Please enter your login.")])

   password = PasswordField("Password", [validators.DataRequired("Please enter your password."),
                                         validators.Length(5,15,"password should be from 3 to 10 symbols")])

   submit = SubmitField("Send")