from flask import Flask, render_template

app=Flask(__name__)
#activar entorno virtual en linux mac: source venv/bin/activate

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


@app.route('/formulario')
def inicio():
    return render_template("formulario.html")


if __name__=='__main__':
    app.run(debug=True,port=5000)
    

        














