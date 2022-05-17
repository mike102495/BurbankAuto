from flask_app import app
from flask import render_template,redirect,request, session, flash
from flask_app.models import customer, vehicle

@app.route('/create_customer', methods = ['POST'])
def create_customer():
    if 'user_id' in session:
        this_customer = customer.Customer.create_customer(request.form)
        if this_customer:
            return redirect('/users/home')
        else:
            return redirect('/customers/new')
    else:
        return redirect('/')

@app.route('/customers/new')
def new_customer():
    if 'user_id' in session:
        return render_template('add_customer.html')
    else:
        return redirect('/')

@app.route('/customers/<int:id>')
def view_customer(id):
    if 'user_id' in session:
        data ={ "id" : id }
        return render_template("view_customer.html", customer = customer.Customer.get_customer_by_id(data), vehicles = vehicle.Vehicle.get_customers_vehicles(data))
    else:
        return redirect('/')

@app.route('/customers/edit/<int:id>')
def edit_customer(id):
    if 'user_id' in session:
            data ={ "id" : id }
            return render_template("edit_customer.html", customer = customer.Customer.get_customer_by_id(data))
    else:
        return redirect('/')

@app.route('/edit_customer', methods = ['POST'])
def edit_customer_submit():
    if 'user_id' in session:
        this_customer = customer.Customer.edit_customer(request.form)
        customer_id = request.form['id']
        if this_customer:
            return redirect(f'/customers/{customer_id}')
        else:
            return redirect(f'/customers/edit/{customer_id}')
    else:
        return redirect('/')

@app.route('/customers/delete/<int:id>')
def delete_customer(id):
    if 'user_id' in session:
        data ={ "id":id }
        customer.Customer.delete_customer(data)
        return redirect('/users/home')
    else:
        return redirect('/')