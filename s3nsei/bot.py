import discord
import os
import boto3
import datetime
from datetime import datetime
from discord.ext import commands
from discord import app_commands
from s3nsei.lex_handler import consultar_lex
from s3nsei.logs_bucket import upload_log_to_s3
from s3nsei.stickers import cargar_stickers, obtener_url_sticker, autocompletar_stickers


intents = discord.Intents.all()
intents.message_content = True  #Necesario para leer mensajes
bot = commands.Bot(command_prefix='!', intents=intents)
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
tareasdb = dynamodb.Table('Tareas') 
recursosdb = dynamodb.Table('Recursos')


@bot.event
async def on_ready():
    print(f'🧠 S3nsei conectado como {bot.user}')

    try:
        cargar_stickers()
        await bot.tree.sync()
    except Exception as e:
        log_text = f"""
        🔴 ERROR al sincronizar slash commands
        Error: {e}
        Fecha: {datetime.now()}
        """
        upload_log_to_s3(log_text, filename_prefix="sync_error")
        print(f"Error al sincronizar slash commands: {e}")


#Recursos
@bot.tree.command(name="recursos", description="Enlaces útiles y recursos del curso AWS re/Start 📚")
async def recursos(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    
    try:
        response = recursosdb.scan()
        datos = response['Items']

        if not datos:
            await interaction.followup.send("❌ No hay recursos aún.")
            return

        mensaje = "📚 **Lista de recursos:**:\n\n"
        for r in datos:
            mensaje += f"• **{r['recurso']}** \n"

        await interaction.followup.send(mensaje)

    except Exception as e:
        log_text = f"""
                    🔴 ERROR al leer recursos
                    Usuario: {interaction.user}
                    Error: {e}
                    Fecha: {datetime.now()}
                    """
        upload_log_to_s3(log_text, filename_prefix="leer_recursos_error")
        await interaction.followup.send("⚠️ No pude leer los recursos.")
        print(e)

#Tareas
@bot.tree.command(name="tareas", description="Lista de tareas pendientes 📅")
async def tarea(interaction: discord.Interaction):
    try:
        response = tareasdb.scan()  #Escanea todas las tareas
        tareas = response['Items']  #Obtiene la lista de tareas

        if not tareas:
            await interaction.response.send_message("✅ No hay tareas pendientes. ¡Buen trabajo, equipo!")
            return

        mensaje = "📚 **Lista de tareas:**\n\n"
        for tarea in tareas:
            mensaje += f"• **{tarea['titulo']}** – 🗓️ {tarea['fecha']}\n   _{tarea['detalle']}_\n\n"

        await interaction.response.send_message(mensaje)

    except Exception as e:
        log_text = f"""
                    🔴 ERROR al leer tareas
                    Usuario: {interaction.user}
                    Error: {e}
                    Fecha: {datetime.now()}
                    """
        upload_log_to_s3(log_text, filename_prefix="leer_tareas_error")
        await interaction.response.send_message("⚠️ No pude leer las tareas.")
        print(e)

#Stickers    
@bot.tree.command(name="stickers", description="Envía un sticker de S3nsei")
@app_commands.describe(nombre="Nombre del sticker")
@app_commands.autocomplete(nombre=autocompletar_stickers)
async def sticker_command(interaction: discord.Interaction, nombre: str):
    url = obtener_url_sticker(nombre)
    embed = discord.Embed(title=f"Sticker: {nombre}")
    embed.set_image(url=url)
    await interaction.response.send_message(embed=embed)



#Ayuda
@bot.tree.command(name="ayuda", description="Una guía de como podemos hablar 💡")
async def ayuda(interaction: discord.Interaction):
    await interaction.response.send_message('📖 Comandos disponibles:\n`/tarea` - Próxima tarea o entrega\n`/recursos` - Recursos útiles\nPuedes preguntarme sobre algunos `servicios de AWS`')


#Conexion con Amazon Lex 
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    #Si está en canal grupal y fue mencionado o escriben "s3nsei"
    if bot.user.mentioned_in(message) or "s3nsei" in message.content.lower():

        #Limpiamos mención si es que viene con <@botID>
        texto = message.content.replace(f'<@{bot.user.id}>', '').strip()
        respuesta = consultar_lex(texto, user_id=message.author.id)
        await message.channel.send(f"☁️ {respuesta}")

    #Si está en un DM (mensaje directo), responde siempre
    elif isinstance(message.channel, discord.DMChannel):
        respuesta = consultar_lex(message.content.strip(), user_id=message.author.id)
        await message.channel.send(f"☁️ {respuesta}")

    await bot.process_commands(message)



