from flask_wtf import FlaskForm
from wtforms import TextField, StringField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField
from flask import Flask, render_template, request, flash
from wtforms import validators, ValidationError


class RegForm(FlaskForm):

   login = StringField("Login",[ validators.DataRequired("Please enter your login.")])

   password = StringField("Password", [validators.DataRequired("Please enter your password.")])

   email = StringField("Email", [validators.DataRequired("Enter valid email address"), validators.Email("Wrong format")])

   name = StringField("Name", [validators.DataRequired("Please enter your name.")])

   age = StringField("Age", [validators.DataRequired("Please enter your age.")])

   submit = SubmitField("OK")