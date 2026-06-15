import csv
import os
from domain.selecao import Selecao
from exceptions.copa_exceptions import ArquivoNaoEncontradoError, DadosCSVInvalidosError

class RepositorioSelecao:
    def __init__(self, caminho_arquivo: str):
        self.caminho_arquivo = caminho_arquivo

    def listar_todas(self) -> list:
        if not os.path.exists(self.caminho_arquivo):
            raise ArquivoNaoEncontradoError(self.caminho_arquivo)
        
        selecoes = []
        with open(self.caminho_arquivo, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    # Garantindo que os campos existem
                    dados = {
                        "nome_pais": row.get('nome_pais'),
                        "sigla": row.get('sigla'),
                        "grupo": row.get('grupo'),
                        "forca": row.get('forca') # Pode vir None se a coluna não existir
                    }

                    if not dados["nome_pais"]: continue
                    
                    selecao = Selecao.from_dict(dados)
                    selecoes.append(selecao)
                except Exception as e:
                    print(f"Erro ao ler linha do CSV: {e}")
        return selecoes

    def salvar_todas(self, selecoes: list):
        with open(self.caminho_arquivo, mode='w', encoding='utf-8', newline='') as f:
            fieldnames = ['nome_pais', 'sigla', 'grupo', 'forca']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for s in selecoes:
                writer.writerow({
                    'nome_pais': s.nome_pais,
                    'sigla': s.sigla,
                    'grupo': s.grupo,
                    'forca': s.forca
                })

    def adicionar(self, nova_selecao: Selecao):
        selecoes = self.listar_todas()
        # Verificar duplicata por sigla ou nome
        for s in selecoes:
            if s.sigla == nova_selecao.sigla or s.nome_pais == nova_selecao.nome_pais:
                raise ValueError(f"Seleção {nova_selecao.nome_pais} ou sigla {nova_selecao.sigla} já existe.")
        
        selecoes.append(nova_selecao)
        self.salvar_todas(selecoes)

    def atualizar(self, sigla: str, dados_atualizados: dict):
        selecoes = self.listar_todas()
        encontrada = False
        for i, s in enumerate(selecoes):
            if s.sigla == sigla:
                if "nome_pais" in dados_atualizados:
                    s.nome_pais = dados_atualizados["nome_pais"]
                if "grupo" in dados_atualizados:
                    s.grupo = dados_atualizados["grupo"]
                if "forca" in dados_atualizados:
                    s.forca = float(dados_atualizados["forca"])
                encontrada = True
                break
        
        if not encontrada:
            raise ValueError(f"Seleção com sigla {sigla} não encontrada.")
            
        self.salvar_todas(selecoes)
