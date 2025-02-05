from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from projeto1.projeto1 import projeto1_blueprint
from projeto2.projeto2 import projeto2_blueprint
from projeto3.projeto3 import projeto3_blueprint
from projeto4.projeto4 import projeto4_blueprint  # Importando o novo projeto

# Configuração do Flask
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Usuários simulados
users = {
    "admin": {"password": "password123"}
}

class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Função que carrega o usuário
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route("/", methods=["GET", "POST"])
def home():
    if current_user.is_authenticated:
        return render_template("home.html")  # Página inicial com links para as rotas dos projetos
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if username in users and users[username]["password"] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash("Usuário ou senha inválidos!", "danger")
            return redirect(url_for("login"))
    
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

# Registrar os blueprints
app.register_blueprint(projeto1_blueprint, url_prefix="/projeto1")
app.register_blueprint(projeto2_blueprint, url_prefix="/projeto2")
app.register_blueprint(projeto3_blueprint, url_prefix="/projeto3")
app.register_blueprint(projeto4_blueprint, url_prefix="/projeto4")  # Novo projeto registrado

if __name__ == "__main__":
    # Garanta que o Flask estará acessível na rede local
    app.run(host="0.0.0.0", port=5000, debug=True)
