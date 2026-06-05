class CopaException(Exception):
    """Classe base para as exceções da Copa do Mundo."""
    pass

class SelecaoNaoEncontradaError(CopaException):
    def __init__(self, selecao: str):
        super().__init__(f"Seleção não encontrada: {selecao}")
        self.selecao = selecao

class ArquivoNaoEncontradoError(CopaException):
    def __init__(self, caminho: str):
        super().__init__(f"Arquivo não encontrado: {caminho}")
        self.caminho = caminho

class DadosCSVInvalidosError(CopaException):
    def __init__(self, campos_faltantes: set):
        super().__init__(f"Dados CSV inválidos. Campos ausentes: {campos_faltantes}")
        self.campos_faltantes = campos_faltantes

class NomeInvalidoError(CopaException):
    def __init__(self, nome: str):
        super().__init__(f"Nome inválido para a seleção: {nome}")
        self.nome = nome