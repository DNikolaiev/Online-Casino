from flask_wtf import FlaskForm
from wtforms import TextField, StringField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, DecimalField
from flask import Flask, render_template, request, flash
from wtforms import validators, ValidationError
from wtforms.fields.html5 import DateField


class BankList(FlaskForm):
    card = IntegerField("Card", [validators.InputRequired()])

