from flask_app import app
from flask import render_template,redirect,request, session, flash
from flask_app.models import vehicle, customer

@app.route('/create_vehicle', methods = ['POST'])
def create_vehicle():
    if 'user_id' in session:
        this_vehicle = vehicle.Vehicle.create_vehicle(request.form)
        customer_id = request.form['customer_id']
        if this_vehicle:
            return redirect(f'/customers/{customer_id}')
        else:
            return redirect(f'/vehicles/new/{customer_id}')
    else:
        return redirect('/')

@app.route('/vehicles/new/<int:id>')
def new_vehicle(id):
    if 'user_id' in session:
        data ={ "id" : id }
        return render_template('add_vehicle.html', customer = customer.Customer.get_customer_by_id(data))
    else:
        return redirect('/')

@app.route('/vehicles/<int:id>')
def view_vehicle(id):
    if 'user_id' in session:
        data ={ "id" : id }
        return render_template("view_vehicle.html", vehicle = vehicle.Vehicle.get_vehicle_and_customer_info_by_vehicle_id(data))
    else:
        return redirect('/')

@app.route('/vehicles/edit/<int:id>')
def edit_vehicle(id):
    if 'user_id' in session:
        data ={ "id" : id }
        return render_template("edit_vehicle.html", vehicle = vehicle.Vehicle.get_vehicle_and_customer_info_by_vehicle_id(data))
    else:
        return redirect('/')

@app.route('/edit_vehicle', methods = ['POST'])
def edit_vehicle_submit():
    if 'user_id' in session:
        this_vehicle = vehicle.Vehicle.edit_vehicle(request.form)
        customer_id = request.form['customer_id']
        vehicle_id = request.form['id']
        if this_vehicle:
            return redirect(f'/customers/{customer_id}')
        else:
            return redirect(f'/vehicles/edit/{vehicle_id}')
    else:
        return redirect('/')

@app.route('/vehicles/delete/<int:customer_id>/<int:id>')
def delete_vehicle(customer_id, id):
    if 'user_id' in session:
        data ={ "id":id }
        customer_id = customer_id
        vehicle.Vehicle.delete_vehicle(data)
        return redirect(f'/customers/{customer_id}')
    else:
        return redirect('/')