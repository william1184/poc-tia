from aws_lambda_powertools import Logger

from src.config.environment_config import EnvironmentConfig

logger = Logger()


class BaseConhecimentoService:
    _environment_config = None

    def __init__(
            self,
            environment_config: EnvironmentConfig
    ):
        self._environment_config = environment_config

    def obter_dados_base_conhecimento(self):
        try:
            logger.info(
                msg='BASECONHECIMENTO_SERVICE__ENVIO_MENSAGEM_INICIO'
            )

            lista_linhas = []
            arquivo = open(file="src/file/base_conhecimento.txt", mode="r", encoding='utf-8')

            for linha in arquivo:
                lista_linhas.append(linha)

            return lista_linhas
        except Exception:
            logger.exception(
                'BASECONHECIMENTO_SERVICE__ENVIO_MENSAGEM_ERRO_GENERICO'
            )
            raise
        finally:
            logger.info(
                msg='BASECONHECIMENTO_SERVICE__ENVIO_MENSAGEM_FIM'
            )
