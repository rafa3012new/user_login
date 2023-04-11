import os

from re import T
from tkinter import ttk

from flask import flash
from flask_login.config.mysqlconnection import connectToMySQL
from flask_login.models import modelo_base
from flask_login.utils.regex import REGEX_CORREO_VALIDO
from itsdangerous import URLSafeTimedSerializer , TimedSerializer, BadTimeSignature, BadSignature, URLSafeSerializer


class Usuario(modelo_base.ModeloBase):

    modelo = 'usuarios'
    campos = ['usuario', 'nombre','apellido','email','password']

    def __init__(self, data):
        self.id = data['id']
        self.usuario = data['usuario']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']




    @classmethod
    def buscar(cls, dato):
        query = "select * from usuarios where usuario = %(dato)s OR email = %(dato)s"
        data = { 'dato' : dato }
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)

        if len(results) < 1:
            return False
        return cls(results[0])


    @classmethod
    def update(cls,data):
        query = """UPDATE usuarios
                        SET nombre = %(nombre)s,
                        SET apellido = %(apellido)s,
                        SET email = %(email)s,
                        SET password = %(password)s,
                        SET usuario = %(usuario)s,
                        updated_at=NOW()
                    WHERE id = %(id)s"""
        resultado = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)
        print("RESULTADO: ", resultado)
        return resultado

    @classmethod
    def update_password(cls,data):
        query = """UPDATE usuarios 
                        SET password = %(password_reg)s,
                        updated_at=NOW()
                    WHERE id = %(id)s"""
        resultado = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)
        print("RESULTADO: ", resultado)
        return resultado


    @staticmethod
    def validar_largo(data, campo, largo):
        is_valid = True
        if len(data[campo]) <= largo:
            flash(f'El largo del {campo} no puede ser menor o igual {largo}', 'error')
            is_valid = False
        return is_valid

    @classmethod
    def validar(cls, data):

        is_valid = True
        #se crea una variable no_create para evitar la sobre escritura de la variable is_valid
        #pero a la vez se vean todos los errores al crear el usuario
        #y no tener que hacer un return por cada error
        no_create = is_valid


        if 'user' in data:
            is_valid = cls.validar_largo(data, 'user', 3)

            if is_valid == False: no_create = False

            if cls.validar_existe('usuario', data['user']):
                flash('el usuario ya esta ingresado', 'error')
                is_valid = False

            if is_valid == False: no_create = False


        if 'name' in data:
            is_valid = cls.validar_largo(data, 'name', 1)
            if is_valid == False: no_create = False
        
        if 'lastname' in data:
            is_valid = cls.validar_largo(data, 'lastname', 1)
            if is_valid == False: no_create = False

        if 'password_reg' in data:
            is_valid = cls.validar_largo(data, 'password_reg', 7)
            if is_valid == False: no_create = False

            if 'cpassword_reg' in data:
                if data['password_reg'] != data['cpassword_reg']:
                    flash('la contraseña de confirmacion no concide con la contraseña', 'error')
                    is_valid = False
                if is_valid == False: no_create = False

        if 'email' in data:
            if not REGEX_CORREO_VALIDO.match(data['email']):
                flash('El correo no es válido', 'error')
                is_valid = False

            if is_valid == False: no_create = False

            if cls.validar_existe('email', data['email']):
                flash('el correo ya fue ingresado', 'error')
                is_valid = False

            if is_valid == False: no_create = False


        return no_create

    @classmethod
    def update(cls,data):
        query = """UPDATE usuarios
                        SET nombre = %(nombre)s,
                        SET apellido = %(apellido)s,
                        SET email = %(email)s,
                        SET password = %(password)s,
                        SET usuario = %(usuario)s,
                        updated_at=NOW()
                    WHERE id = %(id)s"""
        resultado = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)
        print("RESULTADO: ", resultado)
        return resultado


  
