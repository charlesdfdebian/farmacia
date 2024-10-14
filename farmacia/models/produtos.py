import mysql.connector

class Produtos:
    def __init__(self, nome_produto, preco, estoque):
        self.nome_produto = nome_produto
        self.preco = preco
        self.estoque = estoque

    # Método para salvar produto no banco de dados
    def salvar(self, db):
       try:
            cursor = db.cursor()
            
            query = "INSERT INTO produtos(NomeProduto, preco, estoque) VALUES (%s, %s, %s)"
            cursor.execute(query, (self.nome_produto, self.preco, self.estoque))
            db.commit()
            
       except mysql.connector.Error as err:
            print(f"Erro: {err}")
       finally:
            cursor.close()
            db.close()
        
        
