from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from domain.repositorio_selecao import RepositorioSelecao
from domain.simulador_service import SimuladorService
from domain.selecao import Selecao
import os

app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')
app.secret_key = 'supersecretkey' # Para mensagens de flash

repo = RepositorioSelecao('selecoes_copa_2026.csv')
simulador = SimuladorService(repo)

@app.route('/')
def index():
    tab = request.args.get('tab', 'simulator')
    selecoes = []
    if tab == 'management':
        selecoes = repo.listar_todas()
    
    return render_template('index.html', tab=tab, selecoes=selecoes)

@app.route('/api/selecoes', methods=['GET'])
def get_selecoes():
    selecoes = repo.listar_todas()
    return jsonify([{
        "nome": s.nome_pais,
        "sigla": s.sigla,
        "grupo": s.grupo,
        "forca": s.forca
    } for s in selecoes])

@app.route('/selecoes/nova', methods=['POST'])
def add_selecao():
    nome = request.form.get('nome')
    sigla = request.form.get('sigla')
    grupo = request.form.get('grupo')
    forca = request.form.get('forca', 3.0)
    try:
        nova = Selecao(nome, sigla, grupo, float(forca))
        repo.adicionar(nova)
        flash('Seleção adicionada com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro: {e}', 'error')
    return redirect(url_for('index', tab='management'))

@app.route('/selecoes/editar', methods=['POST'])
def update_selecao():
    sigla = request.form.get('sigla')
    nome = request.form.get('nome')
    grupo = request.form.get('grupo')
    forca = request.form.get('forca')
    try:
        repo.atualizar(sigla, {"nome_pais": nome, "grupo": grupo, "forca": forca})
        flash('Seleção atualizada com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro: {e}', 'error')
    return redirect(url_for('index', tab='management'))

@app.route('/simular')
def simular():
    try:
        resultado = simulador.simular_copa()
        return render_template('index.html', tab='simulator', resultado=resultado)
    except Exception as e:
        flash(f'Erro na simulação: {e}', 'error')
        return redirect(url_for('index', tab='simulator'))

if __name__ == '__main__':
    print("Servidor rodando em http://localhost:5000")
    app.run(debug=True, port=5000)
