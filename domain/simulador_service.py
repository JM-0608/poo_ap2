import random
from domain.grupo import Grupo
from domain.partida import PartidaMataMata, PartidaGrupo
from domain.repositorio_selecao import RepositorioSelecao

class SimuladorService:
    def __init__(self, repositorio: RepositorioSelecao):
        self.repositorio = repositorio

    def simular_copa(self):
        selecoes = self.repositorio.listar_todas()
        grupos_dict = {}

        # Montar Grupos
        for s in selecoes:
            s.zerar_estatisticas() # Reset para nova simulação
            if s.grupo not in grupos_dict:
                grupos_dict[s.grupo] = Grupo(s.grupo)
            grupos_dict[s.grupo].adicionar_selecao(s)

        resultado_fase_grupos = []
        classificados_1_e_2 = []
        terceiros_colocados = []

        # Simular Fase de Grupos
        for nome_g in sorted(grupos_dict.keys()):
            grupo = grupos_dict[nome_g]
            
            jogos_grupo = []
            for i in range(len(grupo.lista_selecoes)):
                for j in range(i + 1, len(grupo.lista_selecoes)):
                    s1, s2 = grupo.lista_selecoes[i], grupo.lista_selecoes[j]
                    partida = PartidaGrupo(s1, s2, fase="Grupos")
                    g1, g2 = partida.jogar()
                    
                    jogos_grupo.append({
                        "casa": s1.nome_pais, "gols_casa": g1,
                        "visitante": s2.nome_pais, "gols_visitante": g2,
                        "forca_casa": round(s1.forca, 2), "forca_visitante": round(s2.forca, 2)
                    })

            grupo.classificar_selecoes()
            classificacao = []
            for s in grupo.lista_selecoes:
                classificacao.append({
                    "nome": s.nome_pais, "sigla": s.sigla, "forca": round(s.forca, 2),
                    "pontos": s.pontos, "saldo": s.saldo_gols, "gols": s.gols_marcados
                })
            
            resultado_fase_grupos.append({
                "grupo": nome_g,
                "jogos": jogos_grupo,
                "classificacao": classificacao
            })

            classificados_1_e_2.extend(grupo.obter_classificados())
            terceiro = grupo.obter_terceiro_colocado()
            if terceiro: terceiros_colocados.append(terceiro)

        terceiros_colocados.sort(key=lambda s: (s.pontos, s.saldo_gols, s.gols_marcados), reverse=True)
        melhores_terceiros = terceiros_colocados[:8]
        fase_mata_mata = classificados_1_e_2 + melhores_terceiros
        random.shuffle(fase_mata_mata)

        # Mata-mata
        def simular_rodada(selecoes_fase, nome_fase):
            vencedores = []
            jogos = []
            for i in range(0, len(selecoes_fase), 2):
                s1, s2 = selecoes_fase[i], selecoes_fase[i+1]
                partida = PartidaMataMata(s1, s2, fase=nome_fase)
                vencedor, detalhes = partida.jogar()
                
                vencedores.append(vencedor)
                res = {
                    "casa": s1.nome_pais, "visitante": s2.nome_pais, 
                    "gols_casa": detalhes["gols_casa"], "gols_visitante": detalhes["gols_visitante"], 
                    "penaltis": detalhes["penaltis"], "vencedor": vencedor.nome_pais,
                    "forca_casa": round(s1.forca, 2), "forca_visitante": round(s2.forca, 2)
                }
                jogos.append(res)
            return vencedores, jogos

        v16, j16 = simular_rodada(fase_mata_mata, "16-avos")
        vo, jo = simular_rodada(v16, "Oitavas")
        vq, jq = simular_rodada(vo, "Quartas")
        vs, js = simular_rodada(vq, "Semifinal")
        
        finalistas = vs
        perdedores_semi = []
        for v in vq:
            if v not in vs: perdedores_semi.append(v)
            
        v3, j3 = simular_rodada(perdedores_semi, "3º Lugar")
        vf, jf = simular_rodada(finalistas, "Final")

        return {
            "fase_grupos": resultado_fase_grupos,
            "mata_mata": {
                "16_avos": j16,
                "oitavas": jo,
                "quartas": jq,
                "semifinal": js,
                "terceiro_lugar": j3[0],
                "final": jf[0],
                "campeao": jf[0]["vencedor"]
            }
        }
