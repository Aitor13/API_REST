from flask import Flask, jsonify, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

# Hecho en deployment en Heroku
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://tcncwrqssasksf:34dd1a83e2c1f46c16647da84db10691f049fe432ddf7c0a9d99c3be110727ac@ec2-34-251-118-151.eu-west-1.compute.amazonaws.com/d2qkutr0arlq2g'
# Dejamos la sentencia para arrancar en local y realizar pruebas
#app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql+psycopg2://Aitor:Cerdanyola26@localhost/Clientes'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
CORS(app)

db = SQLAlchemy(app)
mm = Marshmallow(app)

class Clientes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    empresa = db.Column(db.String(50))
    
    def __init__(self, nombre, empresa):
        self.nombre = nombre
        self.empresa = empresa
        
db.create_all()
        
# con este esquema configuramos los datos a mostrar en la peticiones get
class schema(mm.Schema):
    class Meta:
        fields = ('id','nombre', 'empresa')  # siempre hay que darle el nombre fields sino no funciona
        
esquema = schema()
esquemas = schema(many=True)

# En index ya cogermos los datos del formulario web en caso de rellenarse
@app.route('/',methods=['POST', 'GET'])
@app.route('/indice', methods=['POST', 'GET'])
def indice():
    mensaje = ''
    if request.method == 'POST':
        nombre = request.form['nombre']
        empresa = request.form['empresa']
        cliente = Clientes(nombre, empresa)
        db.session.add(cliente)
        db.session.commit()
        mensaje = 'Registro insertado con éxito!'
    return render_template('indice.html',mensaje=mensaje)


# con esta url instermanos datos desde Heroku por la url
@app.route('/heroku_insert/<string:nombre>/<string:empresa>')
def insert_heroku(nombre, empresa):
    datos_registrados = Clientes(nombre,empresa)
    db.session.add(datos_registrados)
    db.session.commit()
    return esquema.jsonify(datos_registrados)

# devolvemos todos los clientes con esta petición
@app.route('/clientes')
def get_clientes():
    clientes = Clientes.query.all()
    return render_template('clientes.html', clientes=clientes)

# Insertamos un cliente
@app.route('/insert_cliente', methods=['POST'])
def insert_clientes():
    nombre = request.json['nombre']
    empresa = request.json['empresa']
    cliente = Clientes(nombre,empresa)
    db.session.add(cliente)
    db.session.commit()
    return esquema.jsonify(cliente)

# devolvemos un cliente por la id que nos pasan
@app.route('/cliente/<int:id>')
def get_cliente(id):
    resultado = Clientes.query.get(id)
    return esquema.jsonify(resultado) if resultado else jsonify({'error':'dato no existente'})
    
@app.route('/delete_client/<int:id>', methods=['GET'])
def delete_client(id):
    resultado = Clientes.query.get(id)
    db.session.delete(resultado)
    db.session.commit()
    return jsonify({'message':'registro eliminado'})

# Recoger datos a traves del formulario web


if __name__ == '__main__':
    app.run(port=2000)