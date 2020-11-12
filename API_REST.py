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

class Restaurante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    calle = db.Column(db.String(50))
    comida = db.Column(db.String(50))
    
    def __init__(self, nombre, calle, comida):
        self.nombre = nombre
        self.calle = calle
        self.comida = comida
        
db.create_all()
        
# con este esquema configuramos los datos a mostrar en la peticiones get
class schema(mm.Schema):
    class Meta:
        fields = ('id','nombre', 'calle', 'comida')  # siempre hay que darle el nombre fields sino no funciona
        
esquema = schema()
esquemas = schema(many=True)

# En index ya cogermos los datos del formulario web en caso de rellenarse
@app.route('/',methods=['POST', 'GET'])
@app.route('/indice', methods=['POST', 'GET'])
def indice():
    mensaje = ''
    if request.method == 'POST':
        nombre = request.form['nombre']
        calle = request.form['calle']
        comida = request.form['comida']
        restaurante = Restaurante(nombre, calle, comida)
        db.session.add(restaurante)
        db.session.commit()
        mensaje = 'Registro insertado con éxito!'
    return render_template('indice.html',mensaje=mensaje)


# con esta url insertamos datos desde Heroku por la url
@app.route('/API/heroku_insert/<string:nombre>/<string:calle>/<string:comida>')
def insert_heroku(nombre, calle, comida):
    datos_registrados = Restaurante(nombre, calle, comida)
    db.session.add(datos_registrados)
    db.session.commit()
    return esquema.jsonify(datos_registrados)

# devolvemos todos los restaurantes con esta petición
@app.route('/restaurantes')
def get_restaurantes():
    restaurantes = Restaurante.query.all()
    return render_template('restaurantes.html', restaurantes=restaurantes)

# devolvemos todos los restaurantes como un json
@app.route('/API/get_restaurantes')
def get_api_restaurantes():
    restaurantes = Restaurante.query.all()
    return esquemas.jsonify(restaurantes)
    
# Insertamos un cliente
@app.route('/API/insert_restaurante', methods=['POST'])
def insert_clientes():
    nombre = request.json['nombre']
    calle = request.json['calle']
    comida = request.json['comida']
    restaurante = Restaurante(nombre,calle,comida)
    db.session.add(restaurante)
    db.session.commit()
    return esquema.jsonify(restaurante)

# devolvemos un cliente por la id que nos pasan
@app.route('/API/restaurante/<int:id>')
def get_restaurante(id):
    resultado = Restaurante.query.get(id)
    return esquema.jsonify(resultado) if resultado else jsonify({'error':'dato no existente'})
    
@app.route('/API/delete_restaurante/<int:id>', methods=['GET'])
def delete_client(id):
    resultado = Restaurante.query.get(id)
    db.session.delete(resultado)
    db.session.commit()
    return jsonify({'message':'registro eliminado'})



if __name__ == '__main__':
    app.run(port=2000)