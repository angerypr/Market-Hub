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
        usuario = request.form['usuario'].strip()
        clave = request.form['clave'].strip()

        if not usuario or not clave:
            flash("Por favor, completa todos los campos.")
            return redirect("/login")

        if usuario == 'admin' and clave == 'markethub123':
            session['usuario'] = usuario  
            return redirect("/dashboard")

        else:
            flash("Usuario o contraseña incorrectos.")
            return redirect("/login")

    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    if 'usuario' in session:
        productos = Producto.query.all()
        return render_template('dashboard.html', productos=productos)
    return redirect('/login')

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if 'usuario' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        precio = float(request.form['precio'])
        cantidad = int(request.form['cantidad'])

        if len(nombre) > 100:
            flash('El nombre del producto no puede tener más de 100 caracteres.', 'danger')
            return render_template('agregar.html')

        producto_existente = Producto.query.filter_by(nombre=nombre).first()
        if producto_existente:
            flash('Ya existe un producto con ese nombre.', 'danger')
            return render_template('agregar.html')  

        nuevo = Producto(nombre=nombre, precio=precio, cantidad=cantidad)
        db.session.add(nuevo)
        db.session.commit()
        
        flash('¡Producto agregado correctamente!', 'success')
        return redirect('/dashboard')  
    
    return render_template('agregar.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if 'usuario' in session:
        producto = Producto.query.get(id)
        if request.method == 'POST':
            nuevo_nombre = request.form['nombre']
            precio = float(request.form['precio'])
            cantidad = int(request.form['cantidad'])
            
            if len(nuevo_nombre.strip()) > 100:
               flash('El nombre del producto no puede tener más de 100 caracteres.', 'danger')
               return render_template('editar.html', producto=producto)

            producto.nombre = nuevo_nombre
            producto.precio = precio
            producto.cantidad = cantidad
            db.session.commit()
            flash('Producto actualizado correctamente.', 'success')
            return redirect('/dashboard')

        return render_template('editar.html', producto=producto)
    return redirect('/login')

@app.route('/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar(id):
    if 'usuario' not in session:
        return redirect('/login')

    producto = Producto.query.get(id)
    if not producto:
        flash('Producto no encontrado.', 'danger')
        return redirect('/dashboard')

    if request.method == 'POST':
        if request.form['confirmar'] == 'si':
            db.session.delete(producto)
            db.session.commit()
            flash('Producto eliminado correctamente.', 'success')
            return redirect('/dashboard')
        else:
            flash('Eliminación cancelada.', 'info')
            return redirect('/dashboard')

    return render_template('eliminar.html', producto=producto)

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect('/login')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

