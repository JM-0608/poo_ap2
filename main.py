import csv
import random
import os
import sys

# Ajuste para renderização de caracteres em português no Windows (Acentos)
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Importação dos módulos do domínio e exceções personalizadas
from domain.selecao import Selecao
from domain.grupo import Grupo
from domain.partida import PartidaMataMata
from exceptions.copa_exceptions import (
    ArquivoNaoEncontradoError,
    DadosCSVInvalidosError,
    NomeInvalidoError
)

def carregar_dados_e_montar_grupos(caminho_arquivo: str) -> dict:
    if not os.path.exists(caminho_arquivo):
        # Uso de exceção customizada
        raise ArquivoNaoEncontradoError(caminho_arquivo)

    grupos = {}
    
    with open(caminho_arquivo, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            nome = row.get('nome_pais')
            sigla = row.get('sigla', 'N/A')
            nome_grupo = row.get('grupo', '')
            
            nome_grupo = nome_grupo.replace('Group ', 'Grupo ') if 'Group ' in nome_grupo else nome_grupo
            
            if not nome:
                continue

            if nome_grupo not in grupos:
                grupos[nome_grupo] = Grupo(nome_grupo)
            
            dados_dict = {
                "nome_pais": nome,
                "sigla": sigla,
                "grupo": nome_grupo
            }
            
            # Tratamento de exceções
            try:
                # Uso do método de classe para instanciar o objeto
                nova_selecao = Selecao.from_dict(dados_dict)
                grupos[nome_grupo].adicionar_selecao(nova_selecao)
            except (DadosCSVInvalidosError, NomeInvalidoError) as erro:
                print(f"[ERRO ao instanciar Seleção] {erro}")
                
    return grupos

def simular_fase_eliminatoria(nome_fase, times_classificados):
    print(f"\n=== {nome_fase.upper()} ===")
    vencedores = []
    
    random.shuffle(times_classificados)
    
    for i in range(0, len(times_classificados), 2):
        time1 = times_classificados[i]
        time2 = times_classificados[i+1]
        
        # Polimorfismo sendo usado, PartidaMataMata tem o jogar() que retorna o vencedor
        partida = PartidaMataMata(time1, time2, fase=nome_fase)
        vencedor = partida.jogar()
        vencedores.append(vencedor)
        
    return vencedores

def main():
    caminho_csv = 'selecoes_copa_2026.csv'
    
    try:
        print("Carregando seleções e montando os grupos...")
        grupos_copa = carregar_dados_e_montar_grupos(caminho_csv)
        
        print("\n" + "="*40)
        print(" INICIANDO A FASE DE GRUPOS")
        print("="*40)
        
        classificados_1_e_2 = []
        terceiros_colocados = []
        
        nomes_grupos_ordenados = sorted(grupos_copa.keys())
        
        for nome_g in nomes_grupos_ordenados:
            grupo_atual = grupos_copa[nome_g]
            
            grupo_atual.simular_jogos_do_grupo()
            grupo_atual.exibir_classificacao()
            
            top_2 = grupo_atual.obter_classificados()
            classificados_1_e_2.extend(top_2)
            
            terceiro = grupo_atual.obter_terceiro_colocado()
            if terceiro:
                terceiros_colocados.append(terceiro)
        
        # Acesso às propriedades usando encapsulamento (@property)
        terceiros_colocados.sort(key=lambda s: (s.pontos, s.saldo_gols, s.gols_marcados), reverse=True)
        melhores_terceiros = terceiros_colocados[:8]
        
        fase_mata_mata = classificados_1_e_2 + melhores_terceiros
        
        print("\n=== CLASSIFICADOS PARA 16-AVOS DE FINAL ===")
        for idx, selecao in enumerate(fase_mata_mata, 1):
            # Imprime invocando o __str__ de Seleção indiretamente
            print(f"{idx:02d} - {selecao}")
            
        print("\n" + "="*40)
        print(" INICIANDO O MATA-MATA")
        print("="*40)
        
        vencedores_16 = simular_fase_eliminatoria("16-avos de Final", fase_mata_mata)
        vencedores_oitavas = simular_fase_eliminatoria("Oitavas de Final", vencedores_16)
        vencedores_quartas = simular_fase_eliminatoria("Quartas de Final", vencedores_oitavas)
        
        print(f"\n=== SEMIFINAIS ===")
        finalistas = []
        disputa_terceiro = []
        
        p1 = PartidaMataMata(vencedores_quartas[0], vencedores_quartas[1], fase="Semifinal")
        v1 = p1.jogar()
        finalistas.append(v1)
        disputa_terceiro.append(vencedores_quartas[0] if v1 != vencedores_quartas[0] else vencedores_quartas[1])
        
        p2 = PartidaMataMata(vencedores_quartas[2], vencedores_quartas[3], fase="Semifinal")
        v2 = p2.jogar()
        finalistas.append(v2)
        disputa_terceiro.append(vencedores_quartas[2] if v2 != vencedores_quartas[2] else vencedores_quartas[3])
        
        print(f"\n=== DISPUTA DE 3º LUGAR ===")
        p_terceiro = PartidaMataMata(disputa_terceiro[0], disputa_terceiro[1], fase="Disputa de 3º Lugar")
        terceiro_lugar = p_terceiro.jogar()
        print(f"\nO 3º LUGAR vai para: {terceiro_lugar.nome_pais}!")
        
        print(f"\n=== FINAL ===")
        p_final = PartidaMataMata(finalistas[0], finalistas[1], fase="Final")
        campeao = p_final.jogar()
        
        print("\n" + "="*40)
        print(f" 🏆 CAMPEÃO DA COPA DO MUNDO 2026: {campeao.nome_pais.upper()} 🏆 ")
        print(f" Total de seleções instanciadas (Atributo de Classe): {Selecao.total_selecoes}")
        print("="*40)

    except ArquivoNaoEncontradoError as e:
        print(f"[ERRO CRÍTICO] {e}")
    except Exception as e:
        print(f"[ERRO INESPERADO] {e}")

if __name__ == '__main__':
    main()
