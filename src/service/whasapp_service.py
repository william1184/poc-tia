import requests
from aws_lambda_powertools import Logger

from src.config.environment_config import EnvironmentConfig

logger = Logger()


class WhatsappService:
    _host: str
    _token: str

    def __init__(self, environment_config: EnvironmentConfig):
        self._host = environment_config.obter_whatsapp_host_url()
        self._token = environment_config.obter_whatsapp_token()

    def enviar_mensagem(self, numero: str, mensagem: str):
        try:
            logger.info(
                msg='WHATSAPP_SERVICE__ENVIO_MENSAGEM_INICIO'
            )

            if len(numero) == 12:
                self._adicionar_nono_digito(numero=numero)

            url_completa = f'{self._host}/200768079779392/messages'

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self._token}'
            }

            dados_requisicao = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": numero,
                "type": "text",
                "text": {
                    "preview_url": False,
                    "body": mensagem
                }
            }

            logger.info(
                msg='WHATSAPP_SERVICE__ENVIO_MENSAGEM',
                extra={
                    'payload': {
                        'dados_requisicao': dados_requisicao,
                        'url_completa': url_completa,
                        'headers': headers
                    }
                }
            )

            response = requests.post(
                url=url_completa,
                headers=headers,
                json=dados_requisicao
            )

            if response.ok:
                dados_resposta = response.json()
                logger.info(
                    msg='WHATSAPP_SERVICE__MENSAGEM_ENVIADA_COM_SUCESSO',
                    extra={
                        'payload': {
                            'response': dados_resposta
                        }
                    }
                )

                return dados_resposta

            response.raise_for_status()

        except Exception:
            logger.exception(
                msg='WHATSAPP_SERVICE__ERRO_GENERICO',
                extra={
                    'payload': {
                        'numero': numero,
                        'mensagem': mensagem
                    }
                }
            )

        finally:
            logger.info(
                msg='WHATSAPP_SERVICE__ENVIO_MENSAGEM_FIM'
            )

    def _adicionar_nono_digito(self, numero):
        posicao = 4
        return numero[:posicao] + '9' + numero[posicao:]