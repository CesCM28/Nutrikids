from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required
import json 
from math import pow

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

def truncate(n, decimals=0):
    multiplier = 10**decimals
    return int(n * multiplier) / multiplier


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
        cursor.execute(sqlIns)
        db.connection.commit()

    return redirect(url_for('docentes'))


@app.route('/update-docente/<int:id>', methods=['POST'])
@login_required
def updateDocente(id):
    cursor = db.connection.cursor()
    names = request.form['updateNames']
    lastName = request.form['updateLastName']
    secondLastName = request.form['updateSecondLastName']
    edad = request.form['updateEdad']
    idGenero = request.form.get('updateGenero')
    idPuesto = request.form.get('updatePuesto')
    idEscuela = request.form.get('updateEscuela')
    state = request.form.get('btnradio')

    if request.method == 'POST':
        sql = """update docente set names = "{}", lastName = "{}", secondLastName = "{}",
                    edad = {}, idGender = {}, idPosition = {}, idEscuela = {}, state = {} where id = {}
                    """.format(names, lastName, secondLastName, edad, idGenero, idPuesto, idEscuela, state, id)
        cursor.execute(sql)
        db.connection.commit()

    return redirect(url_for('docentes'))

#++++++++++++++++++++ Alumnos ++++++++++++++++++++
@app.route('/alumnos', methods=['POST', 'GET'])
@login_required
def alumnos():
    cursor = db.connection.cursor()

    if request.method == 'POST':
        nombre = request.form['nom']
        apellidos = request.form['ape']
        genero = request.form['gen']
        escuela = request.form['esc']
        sql = """SELECT a.id,a.names,a.lastName,a.secondLastName,a.edadA,a.edadM,a.peso,a.tallacm,a.IMC,a.state,a.idEscuela,a.idGender,a.idGrado,a.grupo
        FROM alumnos a 
            INNER JOIN escuela e ON e.id = a.idEscuela
            INNER JOIN genero g ON g.id = a.idGender
        WHERE a.idEscuela = {} and a.idGender = {} and a.names like '%{}%'
            and (a.lastName like '%{}%' or a.secondLastName like '%{}%');
        """.format(escuela, genero, nombre, apellidos, apellidos)
    else:
        sql = """SELECT a.id,a.names,a.lastName,a.secondLastName,a.edadA,a.edadM,a.peso,a.tallacm,a.IMC,a.state,a.idEscuela,a.idGender,a.idGrado,a.grupo
        FROM alumnos a 
        INNER JOIN escuela e ON e.id = a.idEscuela
        INNER JOIN genero g ON g.id = a.idGender;
        """

    cursor.execute(sql)
    alumnos = cursor.fetchall()

    sql = "SELECT id,name FROM escuela WHERE state = 1"
    cursor.execute(sql)
    escuelas = cursor.fetchall()

    sql = "SELECT id,name FROM genero WHERE state = 1"
    cursor.execute(sql)
    generos = cursor.fetchall()

    return render_template('catalogos/alumnos.html', alumnos=alumnos, escuelas=escuelas, generos=generos)


@app.route('/new-alumno', methods=['POST'])
@login_required
def newAlumno():
    cursor = db.connection.cursor()
    names = request.form['newNames']
    lastName = request.form['newLastName']
    secondLastName = request.form['newSecondLastName']
    edadA = request.form['newEdadA']
    edadM = request.form['newEdadM']
    peso = request.form['newPeso']
    talla = request.form.get('newTalla')
    idGenero = request.form.get('newGenero')
    idEscuela = request.form.get('NewEscuela')
    idGrado = request.form['newGrado']
    grupo = request.form['newGrupo']

    IMC = float(peso) / pow((float(talla) / 100 ), 2)

    conSql = "select * from resultados where idGenero = {} and edad = {} and {} between IMCmin and IMCmax;".format(idGenero, edadA, IMC)
    cursor.execute(conSql)
    resultado = cursor.fetchone()

    idResultado = resultado[0]

    if request.method == 'POST':
        sqlIns = """INSERT INTO alumnos (names, lastName, secondLastName, edadA, edadM, peso, tallacm, IMC, idGender, idEscuela, idResultado, idGrado, grupo) 
        VALUES ("{}", "{}", "{}", {}, {}, {}, {}, {}, {}, {}, {}, {}, "{}")""".format(names, lastName, secondLastName, edadA, edadM, peso, talla, truncate(IMC), idGenero, idEscuela, idResultado, idGrado, grupo)
        cursor.execute(sqlIns)
        db.connection.commit()

    return redirect(url_for('alumnos'))


@app.route('/update-alumno/<int:id>', methods=['POST'])
@login_required
def updateAlumnos(id):
    cursor = db.connection.cursor()
    names = request.form['updateNames']
    lastName = request.form['updateLastName']
    secondLastName = request.form['updateSecondLastName']
    edadA = request.form['updateEdadA']
    edadM = request.form['updateEdadM']
    peso = request.form['updatePeso']
    talla = request.form['updateTalla']
    idGenero = request.form.get('updateGenero')
    idEscuela = request.form.get('updateEscuela')
    state = request.form.get('btnradio')
    idGrado = request.form['updateGrado']
    grupo = request.form['updateGrupo']

    IMC = float(peso) / pow((float(talla) / 100.00 ), 2)

    conSql = "select * from resultados where idGenero = {} and edad = {} and {} between IMCmin and IMCmax;".format(idGenero, edadA, IMC)
    cursor.execute(conSql)
    resultado = cursor.fetchone()

    idResultado = resultado[0]

    if request.method == 'POST':
        sql = """update alumnos set names = "{}", lastName = "{}", secondLastName = "{}",
                    edadA = {}, edadM = {}, peso = {}, tallacm = {}, IMC = {}, idGender = {},
                    idEscuela = {}, idResultado = {}, state = {}, idGrado = {}, grupo = "{}" where id = {}
                    """.format(names, lastName, secondLastName, edadA, edadM, peso, talla, truncate(IMC, 1), idGenero, idEscuela, idResultado, state, idGrado, grupo, id)
        cursor.execute(sql)
        db.connection.commit()

    return redirect(url_for('alumnos'))

#++++++++++++++++++++ Graficas ++++++++++++++++++++
@app.route('/menuGraficas', methods=['GET'])
@login_required
def menuGraficas():
    return render_template('graficas/graficas.html')


@app.route('/graficapeso', methods=['POST', 'GET'])
@login_required
def graficapeso():
    filtros = {
        "tipoGrafica": "1",
        "escuela": "0",
        "grado": "0",
        "grupo": "0"
    }

    cursor = db.connection.cursor()

    sql = "SELECT id,name FROM escuela WHERE state = 1"
    cursor.execute(sql)
    escuelas = cursor.fetchall()

    if request.method == 'POST' and request.form["tipoGrafica"] != '1':
        filtros['tipoGrafica'] = request.form["tipoGrafica"]
        filtros['escuela'] = request.form["escuela"]
        filtros['grado'] = request.form["grado"]
        filtros['grupo'] = request.form["grupo"]

        if request.form["tipoGrafica"] == '2':
            conSql = """select resultado,count(resultado) 
                    from alumnos a, peso p
                    where a.peso between p.pesoMin and p.pesoMax
                    and a.idGender = p.IdGenero
                    and a.edadA = p.edad
                    and a.idEscuela = {}
                    group by resultado""".format(request.form["escuela"])
            
        if request.form["tipoGrafica"] == '3':
            conSql = """select resultado,count(resultado) 
                    from alumnos a, peso p
                    where a.peso between p.pesoMin and p.pesoMax
                    and a.idGender = p.IdGenero
                    and a.edadA = p.edad
                    and a.idGrado = {}
                    and (a.idEscuela = {} or {} = 0)
                group by resultado""".format(request.form["grado"], request.form["escuela"], request.form["escuela"])
            
        if request.form["tipoGrafica"] == '4':
            conSql = """select resultado,count(resultado) 
                    from alumnos a, peso p
                    where a.peso between p.pesoMin and p.pesoMax
                    and a.idGender = p.IdGenero
                    and a.edadA = p.edad
                    and a.grupo = "{}"
                    and (a.idGrado = {} or {} = 0)
                    and (a.idEscuela = {} or {} = 0)
                group by resultado""".format(request.form["grupo"], request.form["grado"], request.form["grado"], request.form["escuela"], request.form["escuela"])

    else:
        conSql = """select resultado,count(resultado) 
                    from alumnos a, peso p
                    where a.peso between p.pesoMin and p.pesoMax
                    and a.idGender = p.IdGenero
                    and a.edadA = p.edad
                    group by resultado"""
    
    cursor.execute(conSql)
    resultado = cursor.fetchall()

    Debajo3, Percentil3, Entre310, Percentil10, Entre1025, Percentil25, Entre2550, Percentil50 = 0, 0, 0, 0, 0, 0, 0, 0
    Entre5075, Percentil75, Entre7590, Percentil90, Entre9097, Percentil97, Arriba97 = 0, 0, 0, 0, 0, 0, 0

    for res in resultado:
        if res[0] == 'Debajo 3':
            Debajo3 = res[1]
        elif res[0] == 'Percentil 3':
            Percentil3 = res[1]
        elif res[0] == 'Entre 3 - 10':
            Entre310 = res[1]
        elif res[0] == 'Percentil 10':
            Percentil10 = res[1]
        elif res[0] == 'Entre 10 - 25':
            Entre1025 = res[1]
        elif res[0] == 'Percentil 25':
            Percentil25 = res[1]
        elif res[0] == 'Entre 25 - 50':
            Entre2550 = res[1]
        elif res[0] == 'Percentil 50':
            Percentil50 = res[1]
        elif res[0] == 'Entre 50 - 75':
            Entre5075 = res[1]
        elif res[0] == 'Percentil 75':
            Percentil75 = res[1]
        elif res[0] == 'Entre 75 - 90':
            Entre7590 = res[1]
        elif res[0] == 'Percentil 90':
            Percentil90 = res[1]
        elif res[0] == 'Entre 90 - 97':
            Entre9097 = res[1]
        elif res[0] == 'Percentil 97':
            Percentil97 = res[1]
        elif res[0] == 'Arriba 97':
            Arriba97 = res[1]


    variable = {
        'label': '# de niños',
        'data': [Debajo3, Percentil3, Entre310, Percentil10, Entre1025, Percentil25, Entre2550, Percentil50,
                Entre5075, Percentil75, Entre7590, Percentil90, Entre9097, Percentil97, Arriba97],
        'backgroundColor': [
            'rgb(75, 192, 192)',
            'rgb(0, 192, 192)',
            'rgb(75, 0, 192)',
            'rgb(75, 192, 1)'
        ],
        'borderColor': [
            'rgb(75, 192, 192)',
            'rgb(0, 192, 192)',
            'rgb(75, 0, 192)',
            'rgb(75, 192, 1)'
        ]
    }

    return render_template('graficas/graficaPeso.html', escuelas=escuelas, filtros=filtros, variable=json.dumps(variable))


@app.route('/graficaestatura', methods=['POST', 'GET'])
@login_required
def graficaestatura():
    filtros = {
        "tipoGrafica": "1",
        "escuela": "0",
        "grado": "0",
        "grupo": "0"
    }

    cursor = db.connection.cursor()

    sql = "SELECT id,name FROM escuela WHERE state = 1"
    cursor.execute(sql)
    escuelas = cursor.fetchall()

    if request.method == 'POST' and request.form["tipoGrafica"] != '1':
        filtros['tipoGrafica'] = request.form["tipoGrafica"]
        filtros['escuela'] = request.form["escuela"]
        filtros['grado'] = request.form["grado"]
        filtros['grupo'] = request.form["grupo"]

        if request.form["tipoGrafica"] == '2':
            conSql = """select resultado,count(resultado) 
                    from alumnos a, estatura p
                    where a.tallacm between p.estaturaMin and p.estaturaMax
                    and a.idGender = p.IdGenero
                    and a.edadA = p.edad 
                    and a.idEscuela = {}
                group by resultado""".format(request.form["escuela"])
            
        if request.form["tipoGrafica"] == '3':
            conSql = """select resultado,count(resultado) 
                    from alumnos a, estatura p
                    where a.tallacm between p.estaturaMin and p.estaturaMax
                    and a.idGender = p.IdGenero
                    and a.edadA = p.edad 
                    and a.idGrado = {}
                    and (a.idEscuela = {} or {} = 0)
                group by resultado""".format(request.form["grado"], request.form["escuela"], request.form["escuela"])
            
        if request.form["tipoGrafica"] == '4':
            conSql = """select resultado,count(resultado) 
                    from alumnos a, estatura p
                    where a.tallacm between p.estaturaMin and p.estaturaMax
                    and a.idGender = p.IdGenero
                    and a.edadA = p.edad 
                    and a.grupo = "{}"
                    and (a.idGrado = {} or {} = 0)
                    and (a.idEscuela = {} or {} = 0)
                group by resultado""".format(request.form["grupo"], request.form["grado"], request.form["grado"], request.form["escuela"], request.form["escuela"])

    else:
        conSql = """select resultado,count(resultado) 
                    from alumnos a, estatura p
                    where a.tallacm between p.estaturaMin and p.estaturaMax
                    and a.idGender = p.IdGenero
                    and a.edadA = p.edad
                    group by resultado"""
    
    cursor.execute(conSql)
    resultado = cursor.fetchall()

    Debajo3, Percentil3, Entre310, Percentil10, Entre1025, Percentil25, Entre2550, Percentil50 = 0, 0, 0, 0, 0, 0, 0, 0
    Entre5075, Percentil75, Entre7590, Percentil90, Entre9097, Percentil97, Arriba97 = 0, 0, 0, 0, 0, 0, 0

    for res in resultado:
        if res[0] == 'Debajo 3':
            Debajo3 = res[1]
        elif res[0] == 'Percentil 3':
            Percentil3 = res[1]
        elif res[0] == 'Entre 3 - 10':
            Entre310 = res[1]
        elif res[0] == 'Percentil 10':
            Percentil10 = res[1]
        elif res[0] == 'Entre 10 - 25':
            Entre1025 = res[1]
        elif res[0] == 'Percentil 25':
            Percentil25 = res[1]
        elif res[0] == 'Entre 25 - 50':
            Entre2550 = res[1]
        elif res[0] == 'Percentil 50':
            Percentil50 = res[1]
        elif res[0] == 'Entre 50 - 75':
            Entre5075 = res[1]
        elif res[0] == 'Percentil 75':
            Percentil75 = res[1]
        elif res[0] == 'Entre 75 - 90':
            Entre7590 = res[1]
        elif res[0] == 'Percentil 90':
            Percentil90 = res[1]
        elif res[0] == 'Entre 90 - 97':
            Entre9097 = res[1]
        elif res[0] == 'Percentil 97':
            Percentil97 = res[1]
        elif res[0] == 'Arriba 97':
            Arriba97 = res[1]


    variable = {
        'label': '# de niños',
        'data': [Debajo3, Percentil3, Entre310, Percentil10, Entre1025, Percentil25, Entre2550, Percentil50,
                Entre5075, Percentil75, Entre7590, Percentil90, Entre9097, Percentil97, Arriba97],
        'backgroundColor': [
            'rgb(75, 192, 192)',
            'rgb(0, 192, 192)',
            'rgb(75, 0, 192)',
            'rgb(75, 192, 1)'
        ],
        'borderColor': [
            'rgb(75, 192, 192)',
            'rgb(0, 192, 192)',
            'rgb(75, 0, 192)',
            'rgb(75, 192, 1)'
        ]
    }

    return render_template('graficas/graficaEstatura.html', escuelas=escuelas, filtros=filtros, variable=json.dumps(variable))


@app.route('/graficas', methods=['POST', 'GET'])
@login_required
def graficas():
    filtros = {
        "tipoGrafica": "1",
        "escuela": "0",
        "grado": "0",
        "grupo": "0"
    }

    cursor = db.connection.cursor()

    sql = "SELECT id,name FROM escuela WHERE state = 1"
    cursor.execute(sql)
    escuelas = cursor.fetchall()

    if request.method == 'POST' and request.form["tipoGrafica"] != '1':
        filtros['tipoGrafica'] = request.form["tipoGrafica"]
        filtros['escuela'] = request.form["escuela"]
        filtros['grado'] = request.form["grado"]
        filtros['grupo'] = request.form["grupo"]

        if request.form["tipoGrafica"] == '2':
            conSql = """select resultado,count(resultado) from alumnos a 
                inner join resultados r on a.idResultado = r.id
                where a.idEscuela = {}
                group by resultado""".format(request.form["escuela"])
            
        if request.form["tipoGrafica"] == '3':
            conSql = """select resultado,count(resultado) from alumnos a 
                inner join resultados r on a.idResultado = r.id
                where a.idGrado = {}
                    and (a.idEscuela = {} or {} = 0)
                group by resultado""".format(request.form["grado"], request.form["escuela"], request.form["escuela"])
            
        if request.form["tipoGrafica"] == '4':
            conSql = """select resultado,count(resultado) from alumnos a 
                inner join resultados r on a.idResultado = r.id
                where a.grupo = "{}"
                    and (a.idGrado = {} or {} = 0)
                    and (a.idEscuela = {} or {} = 0)
                group by resultado""".format(request.form["grupo"], request.form["grado"], request.form["grado"], request.form["escuela"], request.form["escuela"])

    else:
        conSql = """select resultado,count(resultado) from alumnos a 
                inner join resultados r on a.idResultado = r.id
                group by resultado"""
    
    cursor.execute(conSql)
    resultado = cursor.fetchall()

    d, pn, sp, o = 0, 0, 0, 0
    
    for res in resultado:
        if res[0] == 'DESNUTRICION':
            d = res[1]
        elif res[0] == 'PESO NORMAL':
            pn = res[1]
        elif res[0] == 'SOBRE PESO':
            sp = res[1]
        elif res[0] == 'OBESIDAD':
            o = res[1]


    variable = {
        'label': '# de niños',
        'data': [d, pn, sp, o],
        'backgroundColor': [
            'rgb(75, 192, 192)',
            'rgb(0, 192, 192)',
            'rgb(75, 0, 192)',
            'rgb(75, 192, 1)'
        ],
        'borderColor': [
            'rgb(75, 192, 192)',
            'rgb(0, 192, 192)',
            'rgb(75, 0, 192)',
            'rgb(75, 192, 1)'
        ]
    }

    return render_template('graficas/grafica.html', escuelas=escuelas, filtros=filtros, variable=json.dumps(variable))

#++++++++++++++++++++ Graficas ++++++++++++++++++++

def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(debug=True)