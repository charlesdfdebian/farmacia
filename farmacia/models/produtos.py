import mysql.connector
from decimal import Decimal

class Produtos:
    def __init__(self, nome_produto, preco, estoque):
        self.nome_produto = nome_produto
        self.preco = Decimal(preco)
        self.estoque = estoque

    # Método para salvar produto no banco de dados
    def salvar(self, db):
       try:
            cursor = db.cursor()
            
            id = Produtos.proximoproduto(db)
            
            query = "INSERT INTO produtos(id,NomeProduto, preco, estoque) VALUES (%s,%s, %s, %s)"
            cursor.execute(query, (id, self.nome_produto, self.preco, self.estoque))
            db.commit()
            
       except mysql.connector.Error as err:
            print(f"Erro: {err}")
       finally:
            cursor.close()
            db.close()
        
    # Função para obter todos os produtos do banco de dados
    @staticmethod
    def listaproduto(db):
         try:
  
            cursor = db.cursor(dictionary=True)
            
            sql="SELECT id,NomeProduto ,preco FROM produtos"
            cursor.execute(sql)
            produtos = cursor.fetchall()
            
            return produtos            
            
         except mysql.connector.Error as err:
            print(f"Erro: {err}")
         finally:
            cursor.close()
            db.close()
            
    @staticmethod
    def proximoproduto(db):
         try:      
           
             cursor = db.cursor()
            
             sql="SELECT max(id)+1 FROM produtos"
             cursor.execute(sql)
             produtos = cursor.fetchone()
             
             if produtos:
                 maximoID = produtos[0]
            
             return maximoID   
             
         except mysql.connector.Error as err:
            print(f"Erro: {err}")
  
