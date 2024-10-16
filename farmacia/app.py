from flask import Flask, render_template, request, redirect, session, url_for
#import mysql.connector
from db_config import get_db_connection
from models.clientes import Clientes
from models.produtos import Produtos

app = Flask(__name__)
app.secret_key = '8714f3545df770ac8b40d7235a59562d'  # Necessário para exibir mensagens flash


# Rota principal (Página inicial com os botões de Login e Cadastro)
@app.route('/')
def home():
       return render_template('index.html')

@app.route('/sobre')
def sobre():
       return render_template('sobre.html')

## Página de login
@app.route('/login')
def login():
     return render_template('login.html')
    
# Verificar login
@app.route('/login', methods=['POST'])
def verificar_login():
    username = request.form['username']
    senha = request.form['password']
    db = get_db_connection()
    

    # Verificar login
    if Clientes.verificar_login( username, senha, db):
        #return render_template('result.html', message="Login bem-sucedido!")
        session['logged_in'] = True
        return   render_template('funcionario.html')

    else:
        session['logged_in'] = False
        return  render_template('result.html', message="Usuário ou senha incorretos!")
    
    db.close()

# Cadastro de clientes
@app.route('/inseri_clientes', methods=['GET', 'POST'])
def inseri_clientes():
    if request.method == 'POST':
        # Coleta os dados do formulário
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        senha = request.form['senha']

        # Cria um objeto Customer e salva no banco de dados
        clientes = Clientes(nome, email,  telefone, senha)        
        db = get_db_connection()
        clientes.salvar(db)
        db.close()

        return redirect(url_for('success', message='Cliente cadastrado com sucesso!'))

    return render_template('inseri_clientes.html')

# Cadastro de produtos
@app.route('/inseri_produtos', methods=['GET', 'POST'])
def inseri_produtos():
    if 'logged_in' in session:

        if request.method == 'POST':
            # Coleta os dados do formulário
            nome_produto = request.form['nome_produto']
            preco = request.form['preco']
            estoque = request.form['estoque']

            preco = preco.replace(",", ".")
            
            # Cria um objeto Product e salva no banco de dados
            produtos = Produtos(nome_produto, preco, estoque)        
            db = get_db_connection()
            produtos.salvar(db)
            db.close()

            return redirect(url_for('success', message='Produto cadastrado com sucesso!'))

        return render_template('inseri_produtos.html')
    return render_template('index.html')
 
 # Função para obter todos os produtos do banco de dados
def obter_produtos():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    connection.close()
    return produtos
    
# lista  de produtos
@app.route('/listaproduto')
def listaproduto():
  #  if 'logged_in' in session:

#if request.method == 'POST':
            
#            produtos = Produtos("",1.1, 1)
            db = get_db_connection()
            produtos =Produtos.listaproduto(db)
    #        produtos = obter_produtos()
            return render_template('listaproduto.html', produtos=produtos)
            db.close()
  #  return render_template('index.html') 
    
# Página de sucesso
@app.route('/success')
def success():
    message = request.args.get('message')
    return render_template('success.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
