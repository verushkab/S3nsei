import boto3
import os
from dotenv import load_dotenv


load_dotenv('ini.env')  #Carga el archivo .env
lex_client = boto3.client('lexv2-runtime', region_name='us-west-2')
BOT_ID = os.getenv("BOT_ID")  #Obtiene id del botLex
BOTALIAS_ID = os.getenv("BOTALIAS_ID")  #Obtiene id del botLexalias
LOCALE_ID = os.getenv("LOCALE_ID") 


def consultar_lex(texto, user_id):
    try:
        lex_response = lex_client.recognize_text(
            botId=BOT_ID,
            botAliasId=BOTALIAS_ID,
            localeId=LOCALE_ID,
            sessionId=str(user_id),
            text=texto
        )

        mensajes = lex_response.get("messages", [])
        if mensajes:
            return mensajes[0]["content"]
        else:
            return "🤖 No tengo una respuesta para eso todavía."

    except Exception as e:
        print(f"❌ Error al consultar a Lex: {e}")
        return "⚠️ No pude consultar a mi sabiduría en la nube (Lex)."
