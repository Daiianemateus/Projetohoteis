from flask import Flask, jsonify
from flask_restx import Api
from resources.hotel import Hoteis, Hotel
from resources.usuario import User, UserRegister, UserLogin, UserLogout
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST
from sql_alchemy import banco
import os
import sqlite3



app = Flask(__name__)

# Definindo o caminho do banco de dados na pasta 'instance'
base_dir = os.path.abspath(os.path.dirname(__file__))
caminho_banco = os.path.join(base_dir, 'instance', 'banco.db')


app.config['SQLALCHEMY_DATABASE_URI'] = r"sqlite:///C:\\Users\\020705631\\Desktop\\REST API com Python e Flask\\instance\\banco.db"
print(f"Banco de dados localizado em: {os.path.join(app.instance_path, 'banco.db')}")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLOCKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)


@app.before_request
def cria_banco():
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()
    with app.app_context():
        banco.create_all()
        print("Tabelas criadas com sucesso!")

@jwt.token_in_blocklist_loader
def verifica_blacklist(token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidado():
    return jsonify({'message':'You have been logged out'}), 401 #Unauthorized

api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
    from sql_alchemy import banco 
    banco.init_app(app)
    app.run(debug=True, port=5000)

#http://127.0.0.1:5000/hoteis

