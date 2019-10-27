from flask_wtf import FlaskForm
from wtforms import TextField, StringField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField
from flask import Flask, render_template, request, flash
from wtforms import validators, ValidationError
from wtforms.fields.html5 import DateField


class BankForm(FlaskForm):

   card = IntegerField("Card",[ validators.DataRequired("Please enter your login.")])

   expDate = DateField("Expiration Date", format='%Y/%m/%d')

   adress = StringField("Adress", [validators.DataRequired("Please enter your password.")])

   oldcard=IntegerField("OldCard")