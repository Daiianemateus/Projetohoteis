
import os

# Caminho do banco de dados
caminho_banco = 'C:\\Users\\020705631\\Desktop\\REST API com Python e Flask\\banco.db'


# Verificar se o arquivo existe antes de deletar
if os.path.exists(caminho_banco):
    os.remove(caminho_banco)
    print("Banco de dados deletado com sucesso.")
else:
    print("O banco de dados não foi encontrado.")
