from flask_restx import Resource, reqparse
from models.models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import hmac
from blacklist import BLACKLIST

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, help="The field 'login'cannot be left blanket")
atributos.add_argument('senha', type=str, help="The field 'senha'cannot be left blanket") 

class User (Resource):
     # /usuarios/{user_id}  
    def get (self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404 #not found


    def delete (self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'An error ocurred trying to delete'},500
            return {'message': 'User deleted'}
        return {'message': 'User not found.'}, 404
    
class UserRegister(Resource):
    # /cadastro
    def post (self):
        dados = atributos.parse_args()  

        if UserModel.find_by_login(dados['login']):
            return {"message": "The login '{}' already exists.".format(dados['login'])} 

        user = UserModel(**dados)
        user.save_user()
        return {'message': 'User created Successfully!'}, 201 #Created
    
class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args() 

        user = UserModel.find_by_login(dados['login'])

        if user and hmac.compare_digest(user.senha.encode('utf-8'), dados ['senha'].encode('utf-8')):
            token_de_acesso = create_access_token(identity = user.user_id)
            return {'acecess_token': token_de_acesso},200
        return {'message':'The username or password is incorrect.'}, 401 #Unauthorized

class UserLogout(Resource):

    @jwt_required
    def post (self):
        jwt_id = get_jwt()['jti'] #JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {'message':'Logged out successfully!'}, 200
    