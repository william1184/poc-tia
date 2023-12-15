from typing import Dict

from aws_lambda_powertools import Logger
from flask import Flask, request, jsonify
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOpenAI

from src.config.environment_config import EnvironmentConfig
from src.service.base_conhecimento_service import BaseConhecimentoService
from src.service.ia_service import IAService
from src.service.whasapp_service import WhatsappService

app = Flask(__name__)
logger = Logger()

env_config = EnvironmentConfig()

client = ChatOpenAI(
    openai_api_key=env_config.obter_openai_apikey(),
    model="gpt-4"
)

base_conhecimento_service = BaseConhecimentoService(
    environment_config=env_config
)

ia_service = IAService(
    base_conhecimento_service=base_conhecimento_service,
    client_ia=client,
    environment_config=env_config
)

whatsapp_service = WhatsappService(
    environment_config=env_config
)


# Rota para receber os webhooks
@app.route('/webhook', methods=['POST'])
def post_webhook():
    data = {}
    try:
        data = request.json  # Os dados do webhook serão recebidos aqui

        logger.info(
            'RECEBIMENTO_WEBHOOK_POST_INICIO',
            extra={
                'payload': {
                    'input': data
                }
            }
        )

        # Lógica para processar eventos de webhook recebidos
        if data:
            input_value = data['entry'][0]['changes'][0]['value']

            if 'messages' in input_value:
                processar_webhook_mensagem(input_value=input_value)

        return jsonify({}), 200  # Responde com vazio (status 200 OK) para outros casos
    except Exception as e:
        logger.exception(
            'FALHA_AO_PROCESSAR_WEBHOOK',
            extra={
                'payload': {
                    'input': data
                }
            }
        )

        return e.args[0], 500
    finally:
        logger.info(
            'RECEBIMENTO_WEBHOOK_POST_FIM'
        )


def processar_webhook_mensagem(input_value: Dict):
    numero_usuario = input_value['messages'][0]['from']

    if 'text' in input_value['messages'][0]:
        mensagem_usuario = input_value['messages'][0]['text']['body']

        resposta = 'Por favor, tente ser o mais claro possível.'
        if len(mensagem_usuario) <= 200:
            resposta = ia_service.enviar_dados_para_ia(mensagem_usuario=mensagem_usuario)

        whatsapp_service.enviar_mensagem(numero=numero_usuario, mensagem=resposta)


@app.route('/webhook', methods=['GET'])
def get_webhook():
    # Extrai o desafio (challenge) dos parâmetros da URL
    challenge = request.args.get('hub.challenge', '')

    # Retorna o desafio como resposta para validar o webhook
    return challenge, 200


if __name__ == '__main__':
    app.run(port=5000)
