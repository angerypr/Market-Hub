from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, Usuario, Producto

app = Flask(__name__)
app.secret_key = 'clave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/markethub'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']
        user = Usuario.query.filter_by(username=usuario).first()
        if user and user.password == clave:
            session['usuario'] = usuario
            return redirect('/dashboard')
        else:
            flash('Usuario o contraseña incorrecta.')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario' in session:
        return render_template('dashboard.html')
    return redirect('/login')

@app.route('/productos')
def productos():
    if 'usuario' in session:
        productos = Producto.query.all()
        return render_template('productos.html', productos=productos)
    return redirect('/login')

@app.route('/agregar', methods=['POST'])
def agregar():
    if 'usuario' in session:
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        cantidad = int(request.form['cantidad'])
        nuevo = Producto(nombre=nombre, precio=precio, cantidad=cantidad)
        db.session.add(nuevo)
        db.session.commit()
        return redirect('/productos')
    return redirect('/login')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if 'usuario' in session:
        producto = Producto.query.get(id)
        if request.method == 'POST':
            producto.nombre = request.form['nombre']
            producto.precio = float(request.form['precio'])
            producto.cantidad = int(request.form['cantidad'])
            db.session.commit()
            return redirect('/productos')
        return render_template('editar.html', producto=producto)
    return redirect('/login')

@app.route('/eliminar/<int:id>')
def eliminar(id):
    if 'usuario' in session:
        producto = Producto.query.get(id)
        db.session.delete(producto)
        db.session.commit()
        return redirect('/productos')
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect('/login')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

