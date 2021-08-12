from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'senha'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cadastro.sqlite3'
db = SQLAlchemy(app)

class Cadastro(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    produto = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.String(350), nullable=False)
    email = db.Column(db.String(150), nullable=False)

    def __init__(self, produto, descricao, email):
        self.produto = produto
        self.descricao = descricao
        self.email = email

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro')
def cad():
    produtos = Cadastro.query.all()
    return render_template('cadastro.html', produtos=produtos)

@app.route('/novoproduto')
def novo():
    return render_template('novoproduto.html')

@app.route('/add', methods=['GET', 'POST'])
def newprod():
    if request.method == 'POST':
        cadastro = Cadastro(
            request.form['produto'],
            request.form['descricao'],
            request.form['email']
        )
    db.session.add(cadastro)
    db.session.commit()
    return redirect('/cadastro')

@app.route('/<id>')
def get_id(id):
    cadastro = Cadastro.query.get(id)
    produtos = Cadastro.query.all()
    return render_template('cadastro.html', cadastroDelete=cadastro, produtos=produtos)    

@app.route('/editar/<id>', methods=['GET', 'POST'])
def edit(id):
    cadastro = Cadastro.query.get(id)
    produtos = Cadastro.query.all()
    if request.method == "POST":
        cadastro.produto = request.form['produto']
        cadastro.descricao = request.form['descricao']
        cadastro.email = request.form['email']
        db.session.commit()
        return redirect('/cadastro')
    return render_template('editar.html', cadastro=cadastro, produtos=produtos) 

@app.route('/delete/<id>') 
def delete(id):
    cadastro = Cadastro.query.get(id)
    db.session.delete(cadastro)
    db.session.commit()
    return redirect('/cadastro')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)







