from domain.selecao import Selecao
from domain.partida import PartidaGrupo

class Grupo:
    def __init__(self, _nome_grupo: str):
        self._nome_grupo = _nome_grupo
        self._lista_selecoes = []

    @property
    def nome_grupo(self) -> str:
        return self._nome_grupo

    @property
    def lista_selecoes(self) -> list:
        return self._lista_selecoes

    def adicionar_selecao(self, selecao: Selecao):
        self._lista_selecoes.append(selecao)

    def simular_jogos_do_grupo(self):
        print(f"\n=== Jogos do {self.nome_grupo} ===")
        # Cada seleção joga contra todas as outras (round-robin)
        for i in range(len(self._lista_selecoes)):
            for j in range(i + 1, len(self._lista_selecoes)):
                # Uso de Polimorfismo, chamando jogar da classe concreta PartidaGrupo
                partida = PartidaGrupo(self._lista_selecoes[i], self._lista_selecoes[j], fase="Grupos")
                partida.jogar()

    def classificar_selecoes(self):
        # A ordenação ocorre pelos pontos, seguido de saldo de gols e gols marcados usando os getters (@property)
        self._lista_selecoes.sort(key=lambda s: (s.pontos, s.saldo_gols, s.gols_marcados), reverse=True)

    def obter_classificados(self) -> list:
        self.classificar_selecoes()
        return self._lista_selecoes[:2]

    def obter_terceiro_colocado(self) -> Selecao:
        self.classificar_selecoes()
        if len(self._lista_selecoes) >= 3:
            return self._lista_selecoes[2]
        return None
        
    def exibir_classificacao(self):
        self.classificar_selecoes()
        print(f"\nClassificação {self.nome_grupo}:")
        for idx, t in enumerate(self._lista_selecoes, 1):
            print(f"{idx}º {t.nome_pais} ({t.sigla}) - {t.pontos} Pts, SG: {t.saldo_gols}, GP: {t.gols_marcados}")

    def __str__(self) -> str:
        return f"Grupo: {self.nome_grupo} com {len(self.lista_selecoes)} seleções"