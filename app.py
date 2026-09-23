from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)

app.secret_key = 'clave_secreta_super_segura'

# Diccionario de usuarios
usuarios = {
    "juan": "1234",
    "maria": "abcd",
    "pedro": "2026"
}

# Lista de cursos
cursos_data = [
    {"nombre": "Programación Web", "docente": "Luis Pérez", "cupos": 15},
    {"nombre": "Bases de Datos", "docente": "Ana López", "cupos": 8},
    {"nombre": "Inteligencia Artificial", "docente": "Carlos Rojas", "cupos": 0}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('username')
        password = request.form.get('password')
        # Validar si el usuario existe y la contraseña coincide
        if usuario in usuarios and usuarios[usuario] == password:
            session['usuario'] = usuario  # 1. Guardar el nombre del usuario en sesión
            flash(f'¡Bienvenido, {usuario}!', 'success')  # 3. Mensaje de bienvenida
            return redirect(url_for('cursos'))  # 2. Redireccionar a /cursos
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

# Ruta /cursos protegida
@app.route('/cursos')
def cursos():
    # Verificar si el usuario está autenticado
    if 'usuario' not in session:
        flash('Debes iniciar sesión para acceder a cursos.', 'danger')
        return redirect(url_for('login'))
    return render_template('cursos.html', cursos=cursos_data)

# Ruta protegida /perfil
@app.route('/perfil')
def perfil():
    # Si un usuario no autenticado intenta acceder, redireccionar a /login
    if 'usuario' not in session:
        flash('Debes iniciar sesión para ver tu perfil.', 'danger')
        return redirect(url_for('login'))
    
    return render_template('perfil.html', usuario=session['usuario'])

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)