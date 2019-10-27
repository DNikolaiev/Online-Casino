from flask_wtf import FlaskForm
from wtforms import TextField, StringField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField
from flask import Flask, render_template, request, flash
from wtforms import validators, ValidationError


class CasinoForm(FlaskForm):

   userMoney = StringField("TotalBalance")

   betMoney = IntegerField("Bet$", [validators.DataRequired("Make a bet.")])

   betField = IntegerField("Field", [validators.InputRequired("Enter field name")])

   submit = SubmitField("Create Bet")


