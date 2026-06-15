import random
from abc import ABC, abstractmethod
from domain.selecao import Selecao

class Partida(ABC):
    def __init__(self, selecao_casa: Selecao, selecao_visitante: Selecao, fase: str):
        self._selecao_casa = selecao_casa
        self._selecao_visitante = selecao_visitante
        self._fase = fase

    @property
    def selecao_casa(self) -> Selecao:
        return self._selecao_casa

    @property
    def selecao_visitante(self) -> Selecao:
        return self._selecao_visitante

    @property
    def fase(self) -> str:
        return self._fase

    @staticmethod
    def simular_gols(forca: float) -> int:
        # Força média é 3.0. Força afeta a média da distribuição normal.
        media_gols = 1.2 * (forca / 3.0)
        return max(0, int(round(random.normalvariate(media_gols, 1.0))))

    def atualizar_forca(self, vencedor: Selecao, perdedor: Selecao, empate: bool = False):
        K = 0.1
        if empate:
            diff = abs(vencedor.forca - perdedor.forca)
            if diff > 1.5:
                # O mais fraco ganha um pouco, o mais forte perde um pouco
                mais_forte = vencedor if vencedor.forca > perdedor.forca else perdedor
                mais_fraco = perdedor if vencedor == mais_forte else vencedor
                
                ganho = min(0.5, (mais_forte.forca / mais_fraco.forca) * K)
                mais_fraco.forca += ganho
                mais_forte.forca -= ganho
        else:
            # Ganho baseado na força do oponente
            ganho = min(0.5, (perdedor.forca / vencedor.forca) * K)
            perda = min(0.5, (vencedor.forca / perdedor.forca) * K)
            
            vencedor.forca += ganho
            perdedor.forca -= perda

    @abstractmethod
    def jogar(self):
        # Força as subclasses a implementarem este método
        pass

    def __str__(self) -> str:
        return f"[{self.fase}] {self.selecao_casa.nome_pais} x {self.selecao_visitante.nome_pais}"


class PartidaGrupo(Partida):
    def jogar(self):
        gols_casa = Partida.simular_gols(self.selecao_casa.forca)
        gols_visitante = Partida.simular_gols(self.selecao_visitante.forca)
        
        self.selecao_casa.adicionar_gols(gols_casa, gols_visitante)
        self.selecao_visitante.adicionar_gols(gols_visitante, gols_casa)

        if gols_casa > gols_visitante:
            self.selecao_casa.adicionar_pontos(3)
            self.atualizar_forca(self.selecao_casa, self.selecao_visitante)
        elif gols_visitante > gols_casa:
            self.selecao_visitante.adicionar_pontos(3)
            self.atualizar_forca(self.selecao_visitante, self.selecao_casa)
        else:
            self.selecao_casa.adicionar_pontos(1)
            self.selecao_visitante.adicionar_pontos(1)
            self.atualizar_forca(self.selecao_casa, self.selecao_visitante, empate=True)
        
        return gols_casa, gols_visitante


class PartidaMataMata(Partida):
    def jogar(self) -> Selecao:
        gols_casa = Partida.simular_gols(self.selecao_casa.forca)
        gols_visitante = Partida.simular_gols(self.selecao_visitante.forca)
        
        vencedor = None
        perdedor = None
        detalhes = {"gols_casa": gols_casa, "gols_visitante": gols_visitante, "penaltis": None}

        if gols_casa == gols_visitante:
            p1, p2 = 0, 0
            while p1 == p2:
                p1, p2 = random.randint(3, 5), random.randint(3, 5)
            detalhes["penaltis"] = f"{p1} x {p2}"
            if p1 > p2:
                vencedor, perdedor = self.selecao_casa, self.selecao_visitante
            else:
                vencedor, perdedor = self.selecao_visitante, self.selecao_casa
            
            # Pênaltis conta como "empate" para evolução de força? 
            # Geralmente sim, mas aqui vamos considerar quem passou como vencedor com ganho reduzido ou tratar como empate.
            # Vamos tratar como empate para evolução de força conforme sua regra de 1.5 de diferença.
            self.atualizar_forca(self.selecao_casa, self.selecao_visitante, empate=True)
        else:
            if gols_casa > gols_visitante:
                vencedor, perdedor = self.selecao_casa, self.selecao_visitante
            else:
                vencedor, perdedor = self.selecao_visitante, self.selecao_casa
            self.atualizar_forca(vencedor, perdedor)
        
        return vencedor, detalhes
