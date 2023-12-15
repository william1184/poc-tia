
# POC-TIA Conversa com IA CHAT GPT
Esta poc engloba, recebimento e envio de mensagem para o whatsapp bussiness e envio de mensagem usando langchain para a openai

## Itens necessários para execução do projeto
    Variaveis de ambiente OBRIGATÓRIAS: 
    WHATSAPP_TOKEN=TOKEN_OBTIDO_NA_META_FOR_DEVELOPERS
    OPENAI_API_KEY=TOKEN_OBTIDO_NA_OPEN_IA
    WHATSAPP_HOST_URL=https://graph.facebook.com/v17.0

## Executando localmente
Após instalar as libs

    python main.py

## Expondo o projeto local na web
Para expor o projeto que está rodando localmente na web será  necessário o uso do ngrok após o download da ferramenta
    
Comando:

        ngrok http 5000

## LINKS UTEIS
[LangChain](https://python.langchain.com/) - Site onde encontramos a documentação da lib langchain responsavel por intermediar acesso ao LLM

[Open AI](https://platform.openai.com/) - Site onde cadastramos o token da open api

[Meta Developers](https://developers.facebook.com/?no_redirect=1) - Site onde cadastramos o token do whatsapp bussiness

[NgRok](https://ngrok.com/) - Site onde nos cadastramos e baixamos um executavel que ajuda a expor a nossa aplicação local