from flask import Flask, render_template, request, flash, make_response, redirect, session
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import json
import numpy
from auth import LOGIN
from auth import REG
from forms.login import LoginForm
from forms.reg import RegForm
from datetime import datetime, timedelta
from forms.casino import CasinoForm
from game import BET, GAME
from user import USER, BANK
from forms.accountDetails import ProfileForm
from forms.bank import BankForm
from forms.bankList import BankList
import  time
import stripe
from visualize import graph1

app = Flask(__name__)
app.secret_key = 'development key'
pub_key='pk_test_PyDI1DegIDtwfxe7yNCiMCvm'
secret_key='sk_test_lZGDTc7tG2QKeVxxG4ptccDt'
stripe.api_key=secret_key
globalVar=0

@app.route('/')
def start():
    response = make_response(redirect('/login'))
    return response


@app.route('/pay', methods=['POST'])
def pay():
    print(request.form)
    customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=5000,
        currency='usd',
        description='Chips'
    )
    user=USER()
    user.change_player_balance(getcookie(),50)
    return make_response(redirect('/profile'))


@app.route('/graph')
def visualize():
    graph=graph1()
    value = graph.user_maxbet()
    print(value)
    users=[]
    bets=[]
    for row in value:
        users+=[row[0]]
        bets+=[row[1]]

    users2=[]
    bets2=[]
    value2=graph.user_betcount()
    for row in value2:
        users2+=[row[0]]
        bets2+=[row[1]]

    data=go.Bar(x=users, y=bets)
    layout=go.Layout(title='Max bet on date', xaxis=dict(title='Date'), yaxis=dict(title='Max Bet',  rangemode='nonnegative',autorange=True))
    data2=[data]
    fig=go.Figure(data=data2,layout=layout)
    result=py.plot(fig)

    layout2 = go.Layout(title='Most frequent bets', xaxis=dict(title='Bet Field'),
                       yaxis=dict(title='Number of bets', rangemode='nonnegative', autorange=True))
    linearData=[go.Bar(x=users2, y=bets2)]
    figure=go.Figure(data=linearData, layout=layout2)
    py.plot(figure)

    graphJson=json.dumps(data2, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('graphs.html', graphJson=graphJson)




@app.route('/profile')
def profile():
    form = ProfileForm()
    bankList=BankList()
    user = USER()
    bank=BANK()

    if request.method == 'GET':
        if 'user' in session and getcookie() is None:
            response = make_response(redirect('/profile'))
            expires = datetime.now()
            expires += timedelta(days=60)
            response.set_cookie('userLogin', session['user'], expires=expires)
            return response
        if session.get('user') is False and getcookie() is not None:
            session['user'] = getcookie()
        login = request.cookies.get('userLogin')
        if login is None and 'user' not in session:
            return make_response(redirect('/login'))

    user = user.get_user(getcookie())
    accounts = bank.get_bank_info(getcookie())
    userMail=user[-1][-2]
    return render_template("profile.html", user=user, accounts=accounts, form=bankList, pub_key=pub_key, userMail=userMail)


@app.route('/deleteBank', methods=['POST'])
def delete_bank():
    if request.method=='POST':
        bank=BANK()
        if parse_int(request.form['card']) == 'FALSE' or len(request.form['card']) != 16:
            flash('Input must be 16-decimal integer')
            return make_response(redirect('/profile'))
        res = bank.delete_bank(getcookie(),request.form['card'])
        if res=='TRUE':
            flash('Deleted successfully')
        else:
            flash('Something went wrong')
    return make_response(redirect('/profile'))


def parse_int(number):
    try:
        val=int(number)
        return 'TRUE'
    except ValueError:
        return 'FALSE'


@app.route('/updateUser', methods=['POST', 'GET'])
def update_user():
    if request.method=='GET':
        if session.get('user') is None:
            return make_response(redirect('/login'))
        else:
            return make_response(redirect('/profile'))
    if request.method=='POST':
        user=USER()
        form = ProfileForm()
        userInfo=user.get_user(getcookie())
        form.userName.data=userInfo[-1][-4]
        form.userAge.data = userInfo[-1][-3]
        form.userMail.data = userInfo[-1][-2]

    return render_template("updateUser.html", form=form)


@app.route('/updateBank', methods=['POST', 'GET'])
def update_bank():
    if request.method=='GET':
        if session.get('user') is None:
            return make_response(redirect('/login'))
        else:
            return make_response(redirect('/profile'))
    if request.method=='POST':
        if parse_int(request.form['card']) == 'FALSE' or len(request.form['card']) != 16:
            flash('Input must be 16-decimal integer')
            return make_response(redirect('/profile'))
        bank=BANK()
        form = BankForm()
        global globalVar
        globalVar = request.form['card']
        globalVar=int(globalVar)
        print(globalVar)
        bankInfo = bank.get_bank_info(globalVar)
        form.adress.data=bankInfo[-1][-1]
        return render_template("updateBank.html", form=form)


@app.route('/confirmUserUpdate', methods=['POST'])
def confirm_user_update():
    if request.method=='POST':
        form2=ProfileForm(request.form)
        if not form2.validate():
            flash('error')
            return make_response(redirect('/profile'))
        user=USER()
        res = user.update_user(getcookie(),getcookie(),request.form['userMail'], request.form['userAge'], request.form['userName'])
        if res == 'TRUE':
            flash('Personal info edited')
        else:
            flash('Something went wrong. Data is invalid')
        print(res)
        return make_response(redirect('/profile'))


@app.route('/confirmBankUpdate', methods=['POST'])
def confirm_update():
    if request.method=='POST':
        if parse_int(request.form['card']) == 'FALSE' or len(request.form['card']) != 16:
            flash('Input must be 16-decimal integer')
            return make_response(redirect('/profile'))
        bank=BANK()
        oldCardNum=globalVar
        print(oldCardNum)
        res = bank.update_bank(getcookie(),oldCardNum,request.form['card'],request.form['expDate'],request.form['adress'])
        if res == 'TRUE':
            flash('Payment info updated')
        else:
            flash('Something went wrong. Data is invalid or card number is not yours')
        print(res)
        return make_response(redirect('/profile'))



@app.route('/addBank', methods=['POST', 'GET'])
def add_bank():
    form = BankForm()
    bank=BANK()
    if request.method=='GET':
        if getcookie() is None:
            return make_response(redirect('/login'))
    if request.method=='POST':
        if parse_int(request.form['card']) == 'FALSE' or len(request.form['card']) != 16:
            flash('Input must be 16-decimal integer')
            return make_response(redirect('/profile'))
        res = bank.add_bank(getcookie(),request.form['card'], request.form['expDate'], request.form['adress'])
        print(res)
        if res =='TRUE':
            flash('Added')
            return make_response(redirect('/profile'))
        else:
            flash('Card already exists or input is invalid')
            return make_response(redirect('/profile'))
    return render_template("addBank.html", form=form)


@app.route('/index', methods=['post', 'get'])
def index():
    form=CasinoForm()
    bet = BET()

    if request.method =='GET':

        if 'user' in session and getcookie() is None:
            response = make_response(redirect('/index'))
            expires = datetime.now()
            expires += timedelta(days=60)
            response.set_cookie('userLogin', session['user'], expires=expires)
            return response
        if session.get('user') is False and getcookie() is not None:
            session['user'] = getcookie()
        login = request.cookies.get('userLogin')
        if login is None and 'user' not in session:
            return make_response(redirect('/login'))
    if request.method == 'POST':
        form2=CasinoForm(request.form)
        if not form2.validate():
            flash('All fields must be integer.')
            return make_response(redirect('/index'))
        else:
            form.userMoney.data = get_user_money()
            betsList = bet.get_bet(getcookie())
            value=request.form['betField']
            if parse_int(value) == 'FALSE' or int(value) > 36:
                flash('Bet field is not valid')
                return make_response(redirect('/index'))
            res = bet.create_bet(getcookie(),bet.generate_id(),request.form['betMoney'],2,time.strftime("%d/%m/%Y"),request.form['betField'])
            if res == 'TRUE':
                response = make_response(redirect('/index'))
                return response
            else:
                render_template('index.html', form=form, userLogin=getcookie(), bets=betsList)
    form.userMoney.data = get_user_money()
    betsList = bet.get_bet(getcookie())
    return render_template('index.html', form=form, userLogin=getcookie(), bets=betsList)


@app.route('/doubleBet', methods=['post', 'get'])
def double_bet():
    login = getcookie()
    bet=BET()
    betsList = bet.get_bets_id(getcookie())
    if len(betsList) == 0:
        flash('No bets')
        return make_response(redirect('/index'))
    bet.double_bet(login)
    return make_response(redirect('/index'))


@app.route('/cancelBet', methods = ['POST', 'GET'])
def cancel_bet():

    if request.method=='GET':
        if getcookie() is None or session.get('user') is False:
            return make_response(redirect('/index'))
    login=getcookie()
    bet=BET()
    print(login)
    betsList = bet.get_bets_id(getcookie())
    print (betsList)
    if len(betsList) == 0:
        flash('No bets')
        return make_response(redirect('/index'))
    else:
        bet.cancel_bet(getcookie())
        del betsList[-1]
        response = make_response(redirect('/index'))
        return response;


@app.route('/play', methods=['post', 'get'])
def play():
    game=GAME()
    login = getcookie()
    bet = BET()
    betsList = bet.get_bets_id(getcookie())
    if len(betsList) == 0:
        flash('no bets in casino')
        return make_response(redirect('/index'))
    number=game.generate_random_number()
    result = game.play_game(login,number)
    if result == 'TRUE':
        print('win')
        flash('You win'+ ' '+number)
        response = make_response(redirect('/index'))
    else:
        print('loose')
        flash('You loose'+' '+number)
        response= make_response(redirect('/index'))
    return response


def get_user_money():
    user=USER()
    if 'user' in session:
        result=user.get_money(session['user'])
        return result
    if getcookie() is not None:
        result=user.get_money(getcookie())
        return result+'$';
    else:
        return 'undefined'


@app.route('/registrate', methods=['GET', 'POST'])
def registrate():
    form=RegForm()

    if request.method == 'GET':
        if 'user' in session and getcookie() is None:
            response = make_response(redirect('/index'))
            expires = datetime.now()
            expires += timedelta(days=60)
            response.set_cookie('userLogin', session['user'], expires=expires)
            return response
        if session.get('user') is False and getcookie() is not None:
            session['user'] = getcookie()
        login = request.cookies.get('userLogin')
        if login is None and 'user' not in session:
            return render_template('reg.html', form=form)
        return 'You logged in'

    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template('reg.html', form=form)
        else:
            reg = REG()
            reg.__enter__()
            res = reg.reg_user(request.form['login'], request.form['password'], request.form['email'], request.form['age'], request.form['name'])
            if res == 'TRUE':
                session['user'] = request.form['login']
                print(session)
                response = make_response(redirect('/index'))
                expires = datetime.now()
                expires += timedelta(days=60)
                response.set_cookie('userLogin', request.form['login'], expires=expires)
                return response
            else:
                flash('User exists or input is incorrect')
                render_template('reg.html', form=form)

    return render_template('reg.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'GET':
        if 'user' in session and getcookie() is None:
            response = make_response(redirect('/index'))
            expires = datetime.now()
            expires += timedelta(days=60)
            response.set_cookie('userLogin', session['user'], expires=expires)
            return response
        if session.get('user') is False and getcookie() is not None:
            session['user'] = getcookie()
        login = getcookie()
        if login is None and 'user' not in session:
            return render_template('login.html', form=form)
        response=make_response(redirect('/index'))
        return response;

    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template('login.html', form=form)
        else:
            login = LOGIN()
            login.__enter__()
            res = login.login_user(request.form['login'],request.form['password'])
            if res == 'TRUE':
                session['user']=request.form['login']
                print(session)
                response = make_response(redirect('/index'))
                expires = datetime.now()
                expires += timedelta(days=60)
                response.set_cookie('userLogin', request.form['login'], expires=expires)
                return response
            else:
                flash('Invalid login/password')
                render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/getcookie')
def getcookie():
   login = request.cookies.get('userLogin')
   return login


@app.route('/logout')
def delete_cookie():
    response = make_response(redirect('/login'))
    response.set_cookie('userLogin', '', expires=0)
    session.pop('user', None)
    return response


def getsession():
    return session['user']


if __name__ == '__main__':
    app.run(debug=True)