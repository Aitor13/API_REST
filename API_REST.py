from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Aitor:Cerdanyola26@localhost/Clientes'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

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

# devolvemos todos los clientes con esta petición
@app.route('/clientes', methods=['GET'])
def get_clientes():
    clientes = Clientes.query.all()
    return esquemas.jsonify(clientes)

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
    
@app.route('/delete_client/<int:id>', methods=['DELETE'])
def delete_client(id):
    resultado = Clientes.query.get(id)
    db.session.delete(resultado)
    db.session.commit()
    return jsonify({'message':'registro eliminado'})

if __name__ == '__main__':
    app.run(port=2000)