import os


class EnvironmentConfig:
    _whatsapp_host_url: str
    _whatsapp_token: str
    _openai_apikey: str

    def __init__(self):
        self._whatsapp_host_url = self.obter_do_environment('WHATSAPP_HOST_URL')
        self._whatsapp_token = self.obter_do_environment('WHATSAPP_TOKEN')
        self._openai_apikey = self.obter_do_environment(nome_variavel='OPENAI_API_KEY')

    def obter_whatsapp_token(self) -> str:
        return self._whatsapp_token

    def obter_whatsapp_host_url(self) -> str:
        return self._whatsapp_host_url

    def obter_openai_apikey(self) -> str:
        return self._openai_apikey

    @staticmethod
    def obter_do_environment(nome_variavel: str, valor_padrao=None) -> str:
        if nome_variavel in os.environ:
            return os.environ[nome_variavel]

        if valor_padrao:
            return valor_padrao

        raise ValueError(f'{nome_variavel} nao existe no environment')
