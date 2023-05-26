from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required

from config import config

# Models:
from models.ModelUser import ModelUser

# Entities:
from models.entities.User import User

app = Flask(__name__)

app.config['MYSQL_HOST'] = config['development'].MYSQL_HOST
app.config['MYSQL_USER'] = config['development'].MYSQL_USER
app.config['MYSQL_PASSWORD'] = config['development'].MYSQL_PASSWORD
app.config['MYSQL_DB'] = config['development'].MYSQL_DB
app.config['SECRET_KEY'] = config['development'].SECRET_KEY

db = MySQL(app)
login_manager_app = LoginManager(app)


@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(0, request.form['username'], request.form['password'], "")
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Invalid password...")
                return render_template('auth/login.html')
        else:
            flash("User not found...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/home')
@login_required
def home():
    return render_template('home.html')

#++++++++++++++++++++ Estados ++++++++++++++++++++
@app.route('/estados')
@login_required
def estados():
    cursor = db.connection.cursor()
    sql = """SELECT id, name, state FROM estados"""
    cursor.execute(sql)
    estados = cursor.fetchall()

    return render_template('catalogos/estados.html', estados=estados)


@app.route('/new-estado', methods=['POST'])
@login_required
def newEstados():
    cursor = db.connection.cursor()
    name = request.form['name']
    if request.method == 'POST':
        sqlIns = 'INSERT INTO estados (name) VALUES ("{}")'.format(name)
        cursor.execute(sqlIns)
        db.connection.commit()

    return redirect(url_for('estados'))


@app.route('/update-estado/<int:id>', methods=['POST'])
@login_required
def updateEstados(id):
    cursor = db.connection.cursor()
    name = request.form['update-name']
    if request.method == 'POST':
        sqlIns = 'UPDATE estados SET name = "{}" WHERE id = {}'.format(name, id)
        cursor.execute(sqlIns)
        db.connection.commit()

    return redirect(url_for('estados'))

#++++++++++++++++++++ Municipios ++++++++++++++++++++
@app.route('/municipios')
@login_required
def municipios():
    cursor = db.connection.cursor()
    sql = """SELECT m.id,m.name,e.name,m.state,m.idEstado FROM municipio m 
    INNER JOIN estados e ON e.id = m.idEstado"""
    cursor.execute(sql)
    municipios = cursor.fetchall()

    cursor = db.connection.cursor()
    sql = """SELECT id, name, state FROM estados WHERE state = 1"""
    cursor.execute(sql)
    estados = cursor.fetchall()

    return render_template('catalogos/municipios.html', municipios=municipios, estados=estados)


@app.route('/new-municipio', methods=['POST'])
@login_required
def newMunicipio():
    cursor = db.connection.cursor()
    name = request.form['name']
    idEstado = request.form.get('estados')
    if request.method == 'POST':
        sqlIns = 'INSERT INTO municipio (name, idEstado) VALUES ("{}", {})'.format(name, idEstado)
        cursor.execute(sqlIns)
        db.connection.commit()

    return redirect(url_for('municipios'))


@app.route('/update-municipio/<int:id>', methods=['POST'])
@login_required
def updateMunicipio(id):
    cursor = db.connection.cursor()
    name = request.form['update-name']
    state = request.form.get('btnradio')
    idEstado = request.form.get('inputEstados')
    if request.method == 'POST':
        sqlIns = 'UPDATE municipio SET name = "{}",idEstado = {}, state = {} WHERE id = {}'.format(name, idEstado, state, id)
        cursor.execute(sqlIns)
        db.connection.commit()

    return redirect(url_for('municipios'))


#++++++++++++++++++++ Colonia ++++++++++++++++++++
@app.route('/colonias')
@login_required
def colonias():
    cursor = db.connection.cursor()
    sql = """SELECT c.id,c.name,m.name,c.cp,c.state,c.idMunicipio FROM colonia c
    INNER JOIN municipio m ON m.id = c.idMunicipio"""
    cursor.execute(sql)
    colonias = cursor.fetchall()

    sql = """SELECT id, name, state FROM municipio WHERE state = 1"""
    cursor.execute(sql)
    municipios = cursor.fetchall()

    return render_template('catalogos/colonias.html', colonias=colonias, municipios=municipios)


@app.route('/new-colonia', methods=['POST'])
@login_required
def newColonia():
    cursor = db.connection.cursor()
    name = request.form['name']
    idMunicipio = request.form.get('municipio')
    cp = request.form['cp']
    if request.method == 'POST':
        sqlIns = 'INSERT INTO colonia (name, idMunicipio, cp) VALUES ("{}", {}, "{}")'.format(name, idMunicipio, cp)
        cursor.execute(sqlIns)
        db.connection.commit()

    return redirect(url_for('colonias'))


@app.route('/update-colonia/<int:id>', methods=['POST'])
@login_required
def updateColonia(id):
    cursor = db.connection.cursor()
    name = request.form['update-name']
    state = request.form.get('btnradio')
    idMunicipio = request.form.get('inputMunicipio')
    cp = request.form['update-cp']
    if request.method == 'POST':
        sqlIns = 'UPDATE colonia SET name = "{}", idMunicipio = {}, cp = {}, state = {} WHERE id = {}'.format(name, idMunicipio, cp, state, id)
        cursor.execute(sqlIns)
        db.connection.commit()

    return redirect(url_for('colonias'))

#++++++++++++++++++++ Escuelas ++++++++++++++++++++
@app.route('/escuelas')
@login_required
def escuelas():
    cursor = db.connection.cursor()
    sql = """SELECT e.id, e.name, c.name, e.street, e.number, e.cp, e.state, e.idColonia FROM escuela e 
    INNER JOIN colonia c ON c.id = e.idColonia"""
    cursor.execute(sql)
    escuelas = cursor.fetchall()
    
    sql = """SELECT id, name, state FROM colonia WHERE state = 1"""
    cursor.execute(sql)
    colonias = cursor.fetchall()

    return render_template('catalogos/escuelas.html', escuelas=escuelas, colonias=colonias)

@app.route('/new-escuela', methods=['POST'])
@login_required
def newEscuela():
    cursor = db.connection.cursor()
    name = request.form['name']
    idColonia = request.form.get('colonia')
    street = request.form['calle']
    number = request.form['numero']
    cp = request.form['cp']
    if request.method == 'POST':
        sqlIns = 'INSERT INTO escuela (name, idColonia, street, number, cp) VALUES ("{}", {}, "{}", "{}", "{}")'.format(name, idColonia, street, number, cp)
        cursor.execute(sqlIns)
        db.connection.commit()

    return redirect(url_for('escuelas'))


@app.route('/update-escuela/<int:id>', methods=['POST'])
@login_required
def updateEscuela(id):
    cursor = db.connection.cursor()
    name = request.form['update-name']
    state = request.form.get('btnradio')
    idColonia = request.form.get('inputColonia')
    street = request.form['update-street']
    number = request.form['update-number']
    cp = request.form['update-cp']
    if request.method == 'POST':
        sqlIns = """UPDATE escuela SET name = "{}", idColonia = {}, street = "{}", number = "{}", cp = "{}", state = {}
                    WHERE id = {}""".format(name, idColonia, street, number, cp, state, id)
        cursor.execute(sqlIns)
        db.connection.commit()

    return redirect(url_for('escuelas'))

#++++++++++++++++++++ Docentes ++++++++++++++++++++
#TODO: editar, asi como la creación de la tabla
@app.route('/docentes')
@login_required
def docentes():
    cursor = db.connection.cursor()
    sql = """SELECT d.id,d.names,d.lastName,d.secondLastName,d.edad,d.state,d.idEscuela,d.idPosition,d.idGender
    FROM docente d 
    INNER JOIN escuela e ON e.id = d.idEscuela
    INNER JOIN puesto p ON p.id = d.idPosition
    INNER JOIN genero g ON g.id = d.idGender;
    """
    cursor.execute(sql)
    docentes = cursor.fetchall()

    sql = "SELECT id,name FROM escuela WHERE state = 1"
    cursor.execute(sql)
    escuelas = cursor.fetchall()

    sql = "SELECT id,name FROM puesto WHERE state = 1"
    cursor.execute(sql)
    puestos = cursor.fetchall()

    sql = "SELECT id,name FROM genero WHERE state = 1"
    cursor.execute(sql)
    generos = cursor.fetchall()

    return render_template('catalogos/docentes.html', docentes=docentes, escuelas=escuelas, puestos=puestos, generos=generos)


@app.route('/new-docente', methods=['POST'])
@login_required
def newDocente():
    cursor = db.connection.cursor()
    names = request.form['newNames']
    lastName = request.form['newLastName']
    secondLastName = request.form['newSecondLastName']
    edad = request.form['newEdad']
    idGenero = request.form.get('newGenero')
    idPuesto = request.form.get('NewPuesto')
    idEscuela = request.form.get('NewEscuela')

    if request.method == 'POST':
        sqlIns = """INSERT INTO docente (names, lastName, secondLastName, edad, idGender, idPosition, idEscuela) 
        VALUES ("{}", "{}", "{}", {}, {}, {}, {})""".format(names, lastName, secondLastName, edad, idGenero, idPuesto, idEscuela)
        print(sqlIns)
        cursor.execute(sqlIns)
        db.connection.commit()

    return redirect(url_for('docentes'))

#++++++++++++++++++++ Alumnos ++++++++++++++++++++


def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(debug=True)