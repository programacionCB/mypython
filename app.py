from flask import Flask, render_template,url_for,request, redirect
from controlador import *
from math import sin, pi

app=Flask(__name__)
app.config['MYSQL_HOST']='cbtis151.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER']='cbtis151'
app.config['MYSQL_PASSWORD']='micontra123'
app.config['MYSQL_DB']='cbtis151$escuela'
app.config['MYSQL_PORT'] = 3306

conexion=MySQL(app)

@app.route("/")
def index():
    miscursos=['php','python','kotlin','swift']
    datos={
        'titulo':'hola',
        'bienvenida':"Saludos",
        'edad':15,
        'cursos':miscursos,
        'numerocursos':len(miscursos)

    }
    return render_template('index.html',data=datos)

def eco(nombre,edad):
    datos={
        'titulo':'ecosistemas',
        'usuario':nombre,
        'edad':edad
    }
    return render_template('baseambiental.html',data=datos)

@app.route('/equilibrio')
def equilibrio():

    image_file = url_for('static', filename='im_equilibrio.jpg')
    datos={
        'titulo':'Equilibrio',
        'W':200,
        'Wg':90,
        'TA':150,
        'TB':120
    }
    return render_template('equilibrio.html',data=datos,sin=sin,pi=pi,round=round,image_file=image_file)

#URL VARIABLE
#import request

def query_string():
    print(request)
    print(request.args)
    print(request.args.get('param1'))
    print(request.args.get('param2'))
    return "ok"

#/consultaparametros?param1=juan
#/consultaparametros?param1=juan&param2=60

def paginanoencontrada(error):
    return render_template('404.html'),404
    #return redirect(url_for('index'))

@app.route("/agregarjuego")
def formularioagregarjuego():
    return render_template("agregarjuego.html")

@app.route("/guardarjuego", methods=["POST"])
def guardarjuego():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    insertarjuego(nombre, descripcion, precio,conexion)

    return redirect("/")

@app.route('/procesar', methods=['POST'])
def procesar():
    nombre = request.form.get("nombre")
    edad = request.form.get("edad")
    return render_template("mostrar.html", nombre=nombre, edad=edad)

@app.route('/tabla')
def tabla():
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT * FROM alumno"
        cursor.execute(sql)
        alumnos=cursor.fetchall()
        nombrecampos=[i[0] for i in cursor.description]
        return render_template("tabla.html", datos=alumnos, campos=nombrecampos)
    except Exception as ex:
        return str(ex)

@app.route("/juegos")
def juegos():
    juegos = obtener_juegos(conexion)
    return render_template("juegos.html", juegos=juegos)

@app.route("/eliminar_juego", methods=["POST"])
def eliminar_juego():
    eliminar(request.form["id"],conexion)
    return redirect("/juegos")

@app.route("/formulario_editar_juego/<string:id>")
def editar_juego(id):
    j = obtener_juego_por_id(id,conexion)
    return render_template("editar_juego.html", juego=j)

@app.route("/actualizarjuego", methods=["POST"])
def actualizar_j():
    id = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    actualizar_juego(nombre, descripcion, precio, id,conexion)
    return redirect("/juegos")

@app.route('/suma')
def inicio():
    return render_template("suma.html")


@app.route("/sumadosnum",methods=["GET","POST"])
def sumar():
    n1 = request.form.get("numero1")
    n2 = request.form.get("numero2")
    res=n1+n2
    return render_template("sumados.html",n1=n1,n2=n2,res=res)

@app.route("/examen")
def formularioagregar():
    return render_template("agregarexamen.html")

@app.route("/guardarexamen", methods=["POST"])
def guardarexa():
    ciclo = request.form["ciclo"]
    carrera1 = request.form["carrera1"]
    insertarjuego(ciclo, carrera1,conexion)

    return redirect("/")


if __name__=='__main__':
    app.add_url_rule('/consultaparametros',view_func=query_string)
    app.register_error_handler(404,paginanoencontrada)
    app.run(debug=True,port=5000)
