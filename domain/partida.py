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
    def simular_gols() -> int:
        # Método estático utilitário para gerar quantidade de gols
        return max(0, int(round(random.normalvariate(1.2, 1.0))))

    @abstractmethod
    def jogar(self):
        # Força as subclasses a implementarem este método
        pass

    def __str__(self) -> str:
        return f"[{self.fase}] {self.selecao_casa.nome_pais} x {self.selecao_visitante.nome_pais}"


class PartidaGrupo(Partida):
    def jogar(self):
        gols_casa = Partida.simular_gols()
        gols_visitante = Partida.simular_gols()
        
        print(f"[{self.fase}] {self.selecao_casa.nome_pais} {gols_casa} x {gols_visitante} {self.selecao_visitante.nome_pais}")

        self.selecao_casa.adicionar_gols(gols_casa, gols_visitante)
        self.selecao_visitante.adicionar_gols(gols_visitante, gols_casa)

        if gols_casa > gols_visitante:
            self.selecao_casa.adicionar_pontos(3)
        elif gols_visitante > gols_casa:
            self.selecao_visitante.adicionar_pontos(3)
        else:
            self.selecao_casa.adicionar_pontos(1)
            self.selecao_visitante.adicionar_pontos(1)


class PartidaMataMata(Partida):
    def jogar(self) -> Selecao:
        gols_casa = Partida.simular_gols()
        gols_visitante = Partida.simular_gols()
        
        print(f"[{self.fase}] {self.selecao_casa.nome_pais} {gols_casa} x {gols_visitante} {self.selecao_visitante.nome_pais}")

        if gols_casa == gols_visitante:
            print("Empate! Disputa de pênaltis...")
            penaltis_casa = 0
            penaltis_visitante = 0
            
            while penaltis_casa == penaltis_visitante:
                penaltis_casa = random.randint(3, 5)
                penaltis_visitante = random.randint(3, 5)
                if penaltis_casa == penaltis_visitante and random.choice([True, False]):
                    penaltis_casa += 1
            
            print(f"Pênaltis: {self.selecao_casa.nome_pais} {penaltis_casa} x {penaltis_visitante} {self.selecao_visitante.nome_pais}")
            if penaltis_casa > penaltis_visitante:
                return self.selecao_casa
            else:
                return self.selecao_visitante
        else:
            if gols_casa > gols_visitante:
                return self.selecao_casa
            else:
                return self.selecao_visitante
