from flask import Flask, Blueprint, render_template, request, jsonify, current_app
import os
import datetime

# Criar o Blueprint para o projeto 3 com um nome exclusivo
projeto3_blueprint = Blueprint('projeto3', __name__, template_folder='templates', static_folder='static')

# Rota principal que renderiza o formulário
@projeto3_blueprint.route('/')
def form():
    return render_template('form.html')

# Rota para registrar um novo pedido
@projeto3_blueprint.route('/registrar', methods=['POST'])
def registrar():
    nome = request.form['nome']
    material = request.form['material']
    quantidade = request.form['quantidade']
    data_hora = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Caminho do arquivo de registro
    arquivo_registro = os.path.join(os.getcwd(), 'registros.txt')

    try:
        with open(arquivo_registro, 'a') as f:
            f.write(f'{data_hora} | Nome: {nome}, Material: {material}, Quantidade: {quantidade}\n')
        current_app.logger.info('Registro salvo com sucesso no arquivo.')
    except Exception as e:
        current_app.logger.error(f'Erro ao salvar registro no arquivo: {e}')

    registro = {
        'nome': nome,
        'material': material,
        'quantidade': quantidade,
        'data_hora': data_hora
    }

    # Alteração no redirecionamento usando o nome correto do blueprint
    return jsonify(registro)

# Rota para limpar os registros exibidos na página (opcional)
@projeto3_blueprint.route('/limpar_registros_exibidos', methods=['POST'])
def limpar_registros_exibidos():
    return 'Registros exibidos limpos com sucesso.'

# Inicialização da aplicação Flask
app = Flask(__name__)

# Registra o blueprint do Projeto 3 com o prefixo correto
app.register_blueprint(projeto3_blueprint, url_prefix='/projeto3')

if __name__ == '__main__':
    app.run(debug=True)
