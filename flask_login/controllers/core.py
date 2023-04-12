import os
from flask import redirect, render_template, request, flash, session, url_for
from flask_login import app
from flask_bcrypt import Bcrypt
from flask_login.models.usuario import Usuario
from datetime import datetime

bcrypt = Bcrypt(app)


@app.route("/")
def index():

    if 'usuario' not in session:
        flash('Primero tienes que logearte', 'error')
        return redirect('/login')

    nombre_sistema = os.environ.get("NOMBRE_SISTEMA")
    return render_template("index.html", sistema=nombre_sistema)

@app.route("/login")
def login():

    if 'usuario' in session:
        flash('Ya estás LOGEADO!', 'warning')
        return redirect('/')

    return render_template("login.html")

@app.route("/procesar_registro", methods=["POST"])
def procesar_registro():

    #validaciones del objeto usuario
    if not Usuario.validar(request.form):
        return redirect('/login')


    pass_hash = bcrypt.generate_password_hash(request.form['password_reg'])

    data = {
        'usuario' : request.form['user'],
        'nombre' : request.form['name'],
        'apellido' : request.form['lastname'],
        'email' : request.form['email'],
        'password' : pass_hash,
    }

    resultado = Usuario.save(data)

    if not resultado:
        flash("error al crear el usuario", "error")
        return redirect("/login")

    flash("Usuario creado correctamente", "success")
    return redirect("/login")


@app.route("/procesar_login", methods=["POST"])
def procesar_login():

    usuario = Usuario.buscar(request.form['identification'])

    if not usuario:
        flash("Usuario/Correo/Clave Invalidas", "error")
        return redirect("/login")

    if not bcrypt.check_password_hash(usuario.password, request.form['password']):
        flash("Usuario/Correo/Clave Invalidas", "error")
        return redirect("/login")

    session['idusuario'] = usuario.id
    session['usuario'] = usuario.nombre + " " + usuario.apellido



    try:
        print("antes de enviar el correo en el core",flush=True)
        print("despues de enviar el correo en el core",flush=True)
    except Exception as error:
        print("error",error,sep=" ", flush=True)
    finally:
        print("fin al intentar enviar el email",flush=True)

    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')



