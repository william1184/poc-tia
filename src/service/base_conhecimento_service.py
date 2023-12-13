from src.config.environment_config import EnvironmentConfig


class BaseConhecimentoService:
    _environment_config = None

    def __init__(
            self,
            environment_config: EnvironmentConfig
    ):
        self._environment_config = environment_config

    def obter_dados_base_conhecimento(self):
        lista_linhas = []
        arquivo = open(file="../file/base_conhecimento.txt", mode="r", encoding='utf-8')

        for linha in arquivo:
            lista_linhas.append(linha)

        return lista_linhas
