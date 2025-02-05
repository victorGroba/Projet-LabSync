from flask import Blueprint, render_template, request
import os
import pandas as pd
from openpyxl import load_workbook
import xlwings as xw

# Criar o Blueprint
projeto2_blueprint = Blueprint('projeto2', __name__, template_folder='templates', static_folder='static')

# Caminho da planilha
file_path = "C:/Users/victo/OneDrive/Documentos/Controle de estoque/projeto_gestao_estoque/relatorio_producao.xlsx"

def carregar_dados():
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

        with xw.App(visible=False) as app:
            wb = app.books.open(file_path)
            wb.save()  # Salva o arquivo após recalcular as fórmulas
            wb.close()

        wb = load_workbook(file_path, data_only=True)
        sheet = wb["Produção Anual"]
        data = sheet.values
        columns = next(data)
        df = pd.DataFrame(data, columns=columns)

        df = df.loc[:, ~df.columns.isnull()]

        if 'ANO' not in df.columns or 'MEIO' not in df.columns or 'FRASCOS 500g' not in df.columns:
            raise ValueError("A planilha não contém as colunas necessárias.")

        df['ANO'] = pd.to_numeric(df['ANO'], errors='coerce')
        df = df.dropna(subset=['ANO'])
        df['ANO'] = df['ANO'].astype(int)

        return df

    except Exception as e:
        print(f"Erro ao carregar os dados: {e}")
        return None

@projeto2_blueprint.route("/", methods=['GET', 'POST'])
def index():
    df = carregar_dados()

    if df is None:
        return "Erro ao carregar os dados da planilha."

    ano_filtro = request.args.get('ano', default=None, type=int)
    meio_filtro = request.args.get('meio', default=None, type=str)

    if ano_filtro:
        df = df[df['ANO'] == ano_filtro]
    if meio_filtro:
        df = df[df['MEIO'].str.contains(meio_filtro, case=False, na=False)]

    colunas_selecionadas = request.args.getlist('colunas')
    
    if colunas_selecionadas:
        df = df[colunas_selecionadas]
    else:
        df = df

    return render_template('relatorio_meios.html', 
                           tabelas=[df.to_html(classes='table table-striped table-bordered')], 
                           anos=df['ANO'].unique(), 
                           colunas=df.columns)
