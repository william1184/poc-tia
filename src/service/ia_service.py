from typing import List

from aws_lambda_powertools import Logger
from langchain_community.callbacks import get_openai_callback
from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

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
            client_ia: ChatOpenAI,
            environment_config
    ):
        self._base_conhecimento_service = base_conhecimento_service
        self._client_ia = client_ia
        self._environment_config = environment_config

    def enviar_dados_para_ia(self, mensagem_usuario: str):
        try:
            logger.info(
                msg='IA_SERVICE__ENVIO_MENSAGEM_INICIO'
            )

            dados_base_conhecimento = self._base_conhecimento_service.obter_dados_base_conhecimento()

            itens_base_conhecimento = self._converter_itens_para_o_formato(
                itens_base_conhecimento=dados_base_conhecimento
            )

            mensagens = itens_base_conhecimento + [HumanMessage(content=mensagem_usuario)]

            with get_openai_callback() as cb:
                resposta = self._client_ia(messages=mensagens)

                logger.info(
                    'IA_SERVICE__CUSTO',
                    extra={
                        'total_tokens': cb.total_tokens,
                        'prompt_tokens': cb.prompt_tokens,
                        'completion_tokens': cb.completion_tokens,
                        'total_cost': cb.total_cost,
                    }
                )

            return resposta.content

        except Exception:
            logger.exception(
                'IA_SERVICE_ERRO_GENERICO'
            )
            raise
        finally:
            logger.info(
                msg='IA_SERVICE__ENVIO_MENSAGEM_FIM'
            )

    def _converter_itens_para_o_formato(self, itens_base_conhecimento: List[str]) -> List:
        itens_no_formato = []
        for item in itens_base_conhecimento:
            itens_no_formato.append(SystemMessage(content=item))

        return itens_no_formato
