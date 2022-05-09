from flask_app import app
from flask import render_template,redirect,request, session, flash
from flask_app.models import user, customer

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('users/home')
    else:
        return render_template('index.html')

@app.route('/create', methods=['POST'])
def create_user():
    user_id = user.User.create_user(request.form)
    if user_id :
        user.User.login_user(request.form)
        return redirect('/users/home')
    else:
        return redirect('/')

@app.route('/users/home')
def home():
    if 'user_id' in session:
        customers = customer.Customer.get_customers()
        return render_template('home.html', customers = customers)
    else:
        return redirect('/')

@app.route('/login', methods = ['POST'])
def login():
    if user.User.login_user(request.form):
        return redirect('/users/home')
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')