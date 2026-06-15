from exceptions.copa_exceptions import DadosCSVInvalidosError, NomeInvalidoError

class Selecao:
    # Atributo de classe (compartilhado)
    total_selecoes = 0

    def __init__(self, _nome_pais: str, _sigla: str, _grupo: str, _forca: float = 3.0):
        # Atributos de instância encapsulados
        self.nome_pais = _nome_pais  # Passa pelo setter para validação
        self.sigla = _sigla          # Passa pelo setter
        self.grupo = _grupo          # Passa pelo setter
        self.forca = _forca          # Passa pelo setter
        self._pontos = 0
        self._gols_marcados = 0
        self._gols_sofridos = 0
        Selecao.total_selecoes += 1

    @property
    def nome_pais(self) -> str:
        return self._nome_pais

    @nome_pais.setter
    def nome_pais(self, valor: str):
        if not valor or len(valor.strip()) < 2:
            raise NomeInvalidoError(valor)
        self._nome_pais = valor.strip()

    @property
    def nome(self) -> str:
        return self.nome_pais

    @property
    def sigla(self) -> str:
        return self._sigla

    @sigla.setter
    def sigla(self, valor: str):
        self._sigla = valor

    @property
    def grupo(self) -> str:
        return self._grupo

    @grupo.setter
    def grupo(self, valor: str):
        self._grupo = valor

    @property
    def forca(self) -> float:
        return self._forca

    @forca.setter
    def forca(self, valor: float):
        self._forca = float(valor)

    @property
    def pontos(self) -> int:
        return self._pontos

    @property
    def gols_marcados(self) -> int:
        return self._gols_marcados

    @property
    def gols_sofridos(self) -> int:
        return self._gols_sofridos

    @property
    def saldo_gols(self) -> int:
        return self._gols_marcados - self._gols_sofridos

    def adicionar_pontos(self, valor: int):
        self._pontos += valor

    def adicionar_gols(self, pro: int, sofridos: int):
        self._gols_marcados += pro
        self._gols_sofridos += sofridos

    def zerar_estatisticas(self):
        self._pontos = 0
        self._gols_marcados = 0
        self._gols_sofridos = 0

    @classmethod
    def from_dict(cls, _dados: dict) -> "Selecao":
        campos = {"nome_pais", "sigla", "grupo"}
        faltando = campos - _dados.keys()
        if faltando:
            raise DadosCSVInvalidosError(faltando)
        
        # Se 'forca' for None ou string vazia, assume 3.0
        valor_forca = _dados.get("forca")
        forca = float(valor_forca) if valor_forca not in (None, "") else 3.0
        
        return cls(_dados["nome_pais"], _dados["sigla"], _dados["grupo"], forca)


    def __str__(self) -> str:
        return f"Seleção: {self.nome_pais} ({self.sigla}) - Grupo {self.grupo}"

