from flask import Flask, render_template, url_for, request
from markupsafe import escape
from datetime import datetime

app = Flask(__name__)

# filtros personalizados
@app.add_template_filter
def today(fecha):
    return fecha.strftime("%d-%m-%Y")

# otra forma de registrar filtro es usar
# app.add_template_filter(today, 'today')


# funcion personalizada
@app.add_template_global
def repetir(s, n):
    return s * n

@app.route("/")
def index():
    nombre = "Ricardo"
    # usamos una lista para probar el for en Jinja2
    lenguajes = ["C", "C++", "Java", "Python"]
    fecha = datetime.now()
    return render_template("index.html", 
                           nombre = nombre, 
                           lenguajes = lenguajes, 
                           fecha = fecha)
#repetir = repetir) # para evitar enviar registrar globalmente el filtro

@app.route("/hola")
@app.route("/hola/<nombre>")
@app.route("/hola/<nombre>/<int:edad>")
@app.route("/hola/<nombre>/<int:edad>/<email>")
def hola(nombre = None, edad = None, email = None):
    mydata = {
        "nombre": nombre,
        "edad": edad,
        "email": email
    }
    return render_template('hola.html', data = mydata)
    
#@app.route("/code/<code>")  # si es así no acepta como codigo debe usar path
@app.route("/code/<path:code>") # acepta pero se ejecuta el código por lo que debo usar markupsafe
def code(code):
    return f"<code> { escape(code) }</code>"

@app.route("/auth/registro", methods=['GET', 'POST']) # get para renderizar y post para recibir los datos.
def registro():
    if request.method == 'POST':
        # recibe los datos y los despliega como texto de plano en una página web sin formato
        usuario = request.form['username']
        passw = request.form['password']
        user_long = len(usuario)
        passw_long = len(passw)
        if user_long >= 4 and user_long <= 25 and passw_long >= 6 and passw_long <= 40:
            return f"Nombre del usuario {usuario}, Contraseña {passw}"
        else:
            error = '''
                El nombre de usuario debe tener entre 4 y 25 caracteres.\n
                La contraseña debe tener entre 6 y 40 caracteres.
            '''
            return render_template('auth/registro.html', error = error)
    return render_template('auth/registro.html')