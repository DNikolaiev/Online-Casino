from flask_wtf import FlaskForm
from wtforms import TextField, StringField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField
from flask import Flask, render_template, request, flash
from wtforms import validators, ValidationError


class ProfileForm(FlaskForm):

   userMoney = StringField("TotalBalance $")

   userName = StringField("Fullname")

   userAge = StringField("Age")

   userMail = StringField("Email", [validators.DataRequired(""), validators.Email("Wrong format")])



