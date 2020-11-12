from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow



app = Flask(__name__)
user = 'usuario'
password = 'password'
base_datos = 'DB'
# Para mysql --> mysql+pymysql:// ....
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql+psycopg2://{}:{}@localhost/{}'.format(user,password,base_datos)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False


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


# Insertamos datos desde la url
@app.route('/API/insert/<string:nombre>/<string:calle>/<string:comida>',methods=['POST'])
def insert_heroku(nombre, calle, comida):
    if request.method == 'POST':
        datos_registrados = Restaurante(nombre, calle, comida)
        db.session.add(datos_registrados)
        db.session.commit()
        return esquema.jsonify(datos_registrados)


# Devolvemos todos los restaurantes como un json
@app.route('/API/get_restaurantes')
def get_api_restaurantes():
    restaurantes = Restaurante.query.all()
    return esquemas.jsonify(restaurantes)
    
    
# Insertamos un restaurante con un json
@app.route('/API/insert_restaurante', methods=['POST'])
def insert_clientes():
    nombre = request.json['nombre']
    calle = request.json['calle']
    comida = request.json['comida']
    restaurante = Restaurante(nombre,calle,comida)
    db.session.add(restaurante)
    db.session.commit()
    return esquema.jsonify(restaurante)


# Devolvemos un restaurante por la id que nos pasan
@app.route('/API/restaurante/<int:id>')
def get_restaurante(id):
    resultado = Restaurante.query.get(id)
    return esquema.jsonify(resultado) if resultado else jsonify({'error':'dato no existente'})


# Eliminamos un restaurante por su id
@app.route('/API/delete_restaurante/<int:id>', methods=['DELETE'])
def delete_client(id):
    resultado = Restaurante.query.get(id)
    db.session.delete(resultado)
    db.session.commit()
    return jsonify({'message':'registro eliminado'})



if __name__ == '__main__':
    app.run(port=2000)