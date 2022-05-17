from flask_app import app
from flask import render_template,redirect,request, session, flash
from flask_app.models import customer, repair_order, vehicle

@app.route('/create_repair_order', methods = ['POST'])
def create_repair_order():
    if 'user_id' in session:
        this_repair_order = repair_order.Repair_Order.create_repair_order(request.form)
        vehicle_id = request.form['vehicle_id']
        if this_repair_order:
            return redirect(f'/vehicles/{vehicle_id}')
        else:
            return redirect(f'/repair_orders/new/{vehicle_id}')
    else:
        return redirect('/')

@app.route('/repair_orders/new/<int:id>')
def new_repair_order(id):
    if 'user_id' in session:
        data ={ "id" : id }
        return render_template('add_repair_order.html', vehicle = vehicle.Vehicle.get_vehicle_and_customer_info_by_vehicle_id(data))
    else:
        return redirect('/')

@app.route('/repair_orders/<int:id>')
def view_repair_order(id):
    if 'user_id' in session:
        data ={ "id" : id }
        return render_template("view_repair_order.html", repair_order = repair_order.Repair_Order.get_repair_order_vehicle_and_customer_info_by_vehicle_id(data))
    else:
        return redirect('/')

@app.route('/repair_orders/edit/<int:id>')
def edit_repair_order(id):
    if 'user_id' in session:
        data ={ "id" : id }
        return render_template("edit_repair_order.html", repair_order = repair_order.Repair_Order.get_repair_order_vehicle_and_customer_info_by_vehicle_id(data))
    else:
        return redirect('/')

@app.route('/edit_repair_order', methods = ['POST'])
def edit_repair_order_submit():
    if 'user_id' in session:
        this_repair_order = repair_order.Repair_Order.edit_repair_order(request.form)
        repair_order_id = request.form['id']
        if this_repair_order:
            return redirect(f'/repair_orders/{repair_order_id}')
        else:
            return redirect(f'/repair_orders/edit/{repair_order_id}')
    else:
        return redirect('/')

@app.route('/repair_orders/delete/<int:vehicle_id>/<int:id>')
def delete_repair_order(vehicle_id, id):
    if 'user_id' in session:
        data ={ "id":id }
        vehicle_id = vehicle_id
        repair_order.Repair_Order.delete_repair_order(data)
        return redirect(f'/vehicles/{vehicle_id}')
    else:
        return redirect('/')