if __name__ == '__main__':
    import os

    os.environ['WHATSAPP_TOKEN'] = 'TOKEN'
    os.environ['WHATSAPP_HOST_URL'] = 'https://graph.facebook.com/v17.0'
    os.environ['OPENAI_API_KEY'] = 'TOKEN_APÍ_KEY'
    env_config = EnvironmentConfig()

    base_conhecimento_service = BaseConhecimentoService(environment_config=env_config)

    conhecimento = base_conhecimento_service.obter_dados_base_conhecimento()

    client = OpenAI()

    ia_service = IAService(
        base_conhecimento_service=base_conhecimento_service,
        client_ia=client,
        environment_config=env_config
    )

    ia_service.enviar_dados_para_ia('Olá gostaria de tirar uma dúvida')

    whatsapp_service = WhatsappService(
        environment_config=env_config
    )

    resposta = whatsapp_service.enviar_mensagem(numero='5513999999999',
                                                mensagem='Olá faço parte do Risco Sacado, no que poderia te ajudar? Fale-me')
    print(resposta)
