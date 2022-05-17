from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app import app
from flask import flash, session
import re
from flask_bcrypt import Bcrypt

class Vehicle:
    db = 'burbankauto'

    def __init__( self , data ):
        self.id = data['id']
        self.customer_id = data['customer_id']
        self.make = data['make']
        self.model = data['model']
        self.vin = data['vin']
        self.year = data['year']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_vehicle(cls, data):
        if cls.validate_vehicle(data):
            query = """
            INSERT INTO vehicles (make, model, vin, year, customer_id)
            VALUES (%(make)s, %(model)s, %(vin)s, %(year)s, %(customer_id)s)
            ;"""
            return MySQLConnection(cls.db).query_db(query, data)

    @classmethod
    def get_customers_vehicles(cls, data):
        query = """
        SELECT *
        FROM vehicles
        WHERE customer_id = %(id)s
        ;"""
        result = MySQLConnection(cls.db).query_db(query, data)
        vehicles = []
        for row in result:
            vehicles.append(cls(row))
        return vehicles

    @classmethod
    def get_vehicle_and_customer_info_by_vehicle_id(cls,data):
        query  = """
        SELECT *
        FROM vehicles
        JOIN customers
        ON customers.id = vehicles.customer_id
        WHERE vehicles.id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query,data)
        return result[0]

    @classmethod
    def edit_vehicle(cls,data):
        if cls.validate_vehicle(data):
            query = """
            UPDATE vehicles
            SET make=%(make)s, model=%(model)s, vin=%(vin)s, year=%(year)s, customer_id=%(customer_id)s
            WHERE id = %(id)s
            ;"""
            MySQLConnection(cls.db).query_db(query,data)
            return True

    @classmethod
    def delete_vehicle(cls,data):
        query = """
        DELETE FROM vehicles
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def validate_vehicle(data):
        is_valid = True
        if len(data['make']) < 2:
            flash('Vehicle make must be at least 2 characters.')
            is_valid = False
        if len(data['model']) < 2:
            flash('Vehicle model must be at least 2 characters.')
            is_valid = False
        if len(data['year']) < 2 :
            flash('Vehicle year must be at least 2 characters.')
            is_valid = False
        if len(data['vin']) < 7 :
            flash('VIN must be at least 7 characters.')
            is_valid = False
        return is_valid