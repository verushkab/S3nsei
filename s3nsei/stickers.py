import boto3
from discord import app_commands

BUCKET_NAME = "s3nsei"
PREFIX = "stickers/"
STICKERS = []  #Lista de stickers

def cargar_stickers():
    global STICKERS
    s3 = boto3.client('s3')
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX)
        STICKERS = []

        if 'Contents' in response:
            for obj in response['Contents']:
                key = obj['Key']
                if key != PREFIX and not key.endswith('/'):
                    nombre = key.replace(PREFIX, '').split('.')[0]
                    STICKERS.append(nombre)
                    
    except Exception as e:
        print(f"[⚠️] Error cargando stickers: {e}")

def obtener_url_sticker(nombre: str) -> str:
    return f"https://{BUCKET_NAME}.s3.us-west-2.amazonaws.com/{PREFIX}{nombre}.png"

def sugerencias_autocompletado(entrada: str) -> list:
    if not entrada:
        #Si no hay texto escrito, muestra los primeros 10
        return STICKERS[:10]
    return [s for s in STICKERS if entrada.lower() in s.lower()][:10]


async def autocompletar_stickers(interaction, current: str):
    from .stickers import sugerencias_autocompletado
    try:
        opciones = sugerencias_autocompletado(current)
        return [
            app_commands.Choice(name=nombre, value=nombre)
            for nombre in opciones
        ]
    except Exception as e:
        print(f"[⚠️] Error en autocompletar_stickers: {e}")
        return []  

