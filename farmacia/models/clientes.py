import mysql.connector
import hashlib

class Clientes:
    def __init__(self, nome, email,  telefone, senha):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.senha = self._gerar_senha_md5(senha)

   # Função para gerar a senha em MD5
    def _gerar_senha_md5(self, senha):
        """Gera o hash MD5 da senha fornecida."""
        md5_hash = hashlib.md5()
        md5_hash.update(senha.encode('utf-8'))
        return md5_hash.hexdigest()
        
    # Método para salvar cliente no banco de dados
    def salvar(self, db):
        """Salva o usuário no banco de dados."""
        try:
            cursor = db.cursor()
            query = "INSERT INTO clientes (NomeCliente, EmailCliente, TelefoneCliente,SenhaClienteMD5) VALUES (%s, %s, %s,%s)"
            cursor.execute(query, ( self.nome, self.email,  self.telefone, self.senha))
        except mysql.connector.Error as err:
            print(f"Erro: {err}")
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def verificar_login( username, senha, db):
        """Verifica o login de um usuário, comparando a senha fornecida com a armazenada."""
        try:
            cursor = db.cursor()


            sql = "SELECT SenhaClienteMD5 FROM clientes WHERE EmailCliente = %s"
            cursor.execute(sql, (username,))
            resultado = cursor.fetchone()

            if resultado:
                senha_md5_banco = resultado[0]
                senha_md5_input = Clientes._gerar_senha_md5_static(senha)

                return senha_md5_banco == senha_md5_input

            return False

        except mysql.connector.Error as err:
            print(f"Erro: {err}")
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def _gerar_senha_md5_static(senha):
        """Gera o hash MD5 de uma senha para comparação."""
        md5_hash = hashlib.md5()
        md5_hash.update(senha.encode('utf-8'))
        return md5_hash.hexdigest()

    
