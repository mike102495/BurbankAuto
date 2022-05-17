from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app import app
from flask import flash, session
import re
from flask_bcrypt import Bcrypt

class Customer:
    db = 'burbankauto'

    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.address = data['address']
        self.email = data['email']
        self.phone_number = data['phone_number']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_customer(cls, data):
        if cls.validate_customer(data):
            query = """
        INSERT INTO customers (first_name, last_name, address, email, phone_number)
        VALUES (%(first_name)s, %(last_name)s, %(address)s, %(email)s, %(phone_number)s)
        ;"""
            return MySQLConnection(cls.db).query_db(query, data)

    @classmethod
    def get_customers(cls):
        query = """
        SELECT *
        FROM customers
        ;"""
        result = MySQLConnection(cls.db).query_db(query)
        customers = []
        for row in result:
            customers.append(cls(row))
        return customers

    @classmethod
    def get_customer_by_id(cls,data):
        query  = """SELECT *
        FROM customers
        WHERE id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query,data)
        print(result[0])
        return cls(result[0])

    @classmethod
    def edit_customer(cls,data):
        if cls.validate_customer(data):
            query = """
            UPDATE customers
            SET first_name=%(first_name)s, last_name=%(last_name)s, address=%(address)s, email=%(email)s, phone_number=%(phone_number)s
            WHERE id = %(id)s
            ;"""
            MySQLConnection(cls.db).query_db(query,data)
            return True

    @classmethod
    def delete_customer(cls,data):
        query = """
        DELETE FROM customers
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def validate_customer(data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash('First name must be at least 2 characters.')
            is_valid = False
        if len(data['last_name']) < 2:
            flash('Last name must be at least 2 characters.')
            is_valid = False
        if len(data['phone_number']) < 7 :
            flash('Phone number must be at least 7 characters.')
            is_valid = False
        return is_valid