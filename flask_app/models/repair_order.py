from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app import app
from flask import flash, session
import re
from flask_bcrypt import Bcrypt

class Repair_Order:
    db = 'burbankauto'

    def __init__( self , data ):
        self.id = data['id']
        self.vehicle_id = data['vehicle_id']
        self.date = data['date']
        self.price = data['price']
        self.breif_descrip = data['breif_descrip']
        self.full_descrip = data['full_descrip']
        self.mileage = data['mileage']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_repair_order(cls, data):
        if cls.validate_repair_order(data):
            query = """
            INSERT INTO repair_orders (vehicle_id, date, price, breif_descrip, full_descrip, mileage)
            VALUES (%(vehicle_id)s, %(date)s, %(price)s, %(breif_descrip)s, %(full_descrip)s, %(mileage)s)
            ;"""
            return MySQLConnection(cls.db).query_db(query, data)

    @classmethod
    def get__vehicles_repair_orders(cls, data):
        query = """
        SELECT *
        FROM repair_orders
        WHERE vehicle_id = %(id)s
        ;"""
        result = MySQLConnection(cls.db).query_db(query, data)
        repair_orders = []
        for row in result:
            repair_orders.append(cls(row))
        print(repair_orders)
        return repair_orders

    @classmethod
    def get_repair_order_vehicle_and_customer_info_by_vehicle_id(cls,data):
        query  = """SELECT *
        FROM repair_orders
        LEFT JOIN vehicles
        ON repair_orders.vehicle_id = vehicles.id
        LEFT JOIN customers
        ON vehicles.customer_id = customers.id
        WHERE repair_orders.id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query,data)
        return result[0]

    @classmethod
    def edit_repair_order(cls,data):
        if cls.validate_repair_order(data):
            query = """
            UPDATE repair_orders
            SET vehicle_id=%(vehicle_id)s, date=%(date)s, price=%(price)s, breif_descrip=%(breif_descrip)s, full_descrip=%(full_descrip)s, mileage=%(mileage)s
            WHERE id = %(id)s
            ;"""
            MySQLConnection(cls.db).query_db(query,data)
            return True

    @classmethod
    def delete_repair_order(cls,data):
        query = """
        DELETE FROM repair_orders
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def validate_repair_order(data):
        is_valid = True
        if data['date'] == "":
            flash('Enter date of repair.')
            is_valid = False
        if len(data['price']) < 1 :
            flash('Enter price.')
            is_valid = False
        if len(data['mileage']) < 1 :
            flash('Enter mileage.')
            is_valid = False
        if len(data['breif_descrip']) < 1:
            flash('Enter breif description.')
            is_valid = False
        if len(data['breif_descrip']) > 46:
            flash('Breif description can be no more than 45 characters.')
            is_valid = False
        if len(data['full_descrip']) < 1:
            flash('Enter full description of repair.')
            is_valid = False
        return is_valid