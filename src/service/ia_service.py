from typing import List

from aws_lambda_powertools import Logger
from openai.types.chat import ChatCompletionMessage

from service.base_conhecimento_service import BaseConhecimentoService
from src.config.environment_config import EnvironmentConfig

logger = Logger()


class IAService:
    _base_conhecimento_service: BaseConhecimentoService = None
    _client_ia = None
    _environment_config: EnvironmentConfig = None

    def __init__(
            self,
            base_conhecimento_service,
            client_ia,
            environment_config
    ):
        self._base_conhecimento_service = base_conhecimento_service
        self._client_ia = client_ia
        self._environment_config = environment_config

    def enviar_dados_para_ia(self, mensagem: str):
        try:
            logger.info(
                msg='IA_SERVICE__ENVIO_MENSAGEM_INICIO'
            )

            dados_base_conhecimento = self._base_conhecimento_service.obter_dados_base_conhecimento()

            itens_base_conhecimento = self._preparar_itens_base_conhecimento(
                itens_base_conhecimento=dados_base_conhecimento
            )

            mensagens = itens_base_conhecimento

            mensagens.append(
                {"role": "user", "content": mensagem}
            )

            completion = self._client_ia.chat.completions.create(
                model="gpt-4",
                messages=mensagens
            )

            message: ChatCompletionMessage = completion.choices[0].message

            return message.content

        except Exception:
            logger.exception(
                'IA_SERVICE'
            )
            raise
        finally:
            logger.info(
                msg='IA_SERVICE__ENVIO_MENSAGEM_FIM'
            )

    def _preparar_itens_base_conhecimento(self, itens_base_conhecimento: List[str]) -> List:
        itens = []
        for item in itens_base_conhecimento:
            itens.append({"role": "system", "content": item.strip()})

        return itens
