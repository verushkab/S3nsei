import discord
import json
import os
import random
import datetime
from discord.ext.commands import has_role, CheckFailure
from discord.ext import commands, tasks
from dotenv import load_dotenv
import boto3


load_dotenv('ini.env')  #Carga el archivo .env
TOKEN = os.getenv("DISCORD_TOKEN")  #Obtiene el valor de la variable
CANAL_ID = os.getenv("CANAL_ID")  #Obtiene el valor del Canal ID a donde se enviaran los tipsintents = discord.Intents.all()
intents = discord.Intents.all()
intents.message_content = True  #Necesario para leer mensajes
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'🧠 S3nsei conectado como {bot.user}')
    enviar_tip_diario.start()

    try:
        synced = await bot.tree.sync()
    except Exception as e:
        log_text = f"""
        🔴 ERROR al sincronizar slash commands
        Error: {e}
        Fecha: {datetime.datetime.now()}
        """
        upload_log_to_s3(log_text, filename_prefix="sync_error")
        print(f"Error al sincronizar slash commands: {e}")

#Saludo
@bot.tree.command(name="saludo", description="Saluda con sabiduría cloud ☁️")
async def saludo(interaction: discord.Interaction):
    await interaction.response.send_message("¡Hola! Soy S3nsei 🧠☁️, tu guía en el mundo AWS.")

#Recursos
@bot.tree.command(name="recursos", description="Enlaces útiles y recursos del curso AWS re/Start 📚")
async def recursos(interaction: discord.Interaction):
    try:
        with open('recursos.json', 'r') as archivo:
            datos = json.load(archivo)

        if not datos:
            await interaction.response.send_message("X No hay recursos aún.")
            return

        mensaje = "📚 **Lista de recursos:**:\n\n"
        for r in datos:
            mensaje += f"• **{r['recurso']}** \n"

        await interaction.response.send_message(mensaje)

    except Exception as e:
        log_text = f"""
                    🔴 ERROR al leer recursos
                    Usuario: {interaction.user}
                    Error: {e}
                    Fecha: {datetime.datetime.now()}
                    """
        upload_log_to_s3(log_text, filename_prefix="leer_recursos_error")
        await interaction.response.send_message("⚠️ No pude leer los recursos.")
        print(e)

#Tareas
@bot.tree.command(name="tareas", description="Lista de tareas pendientes 📅")
async def tarea(interaction: discord.Interaction):
    try:
        with open('tareas.json', 'r') as archivo:
            datos = json.load(archivo)

        if not datos:
            await interaction.response.send_message("✅ No hay tareas pendientes. ¡Buen trabajo, equipo!")
            return

        mensaje = "📚 **Lista de tareas:**:\n\n"
        for r in datos:
            mensaje += f"• **{r['titulo']}** – 🗓️ {r['fecha']}\n   _{r['detalle']}_\n"

        await interaction.response.send_message(mensaje)

    except Exception as e:
        log_text = f"""
                    🔴 ERROR al leer tareas
                    Usuario: {interaction.user}
                    Error: {e}
                    Fecha: {datetime.datetime.now()}
                    """
        upload_log_to_s3(log_text, filename_prefix="leer_tareas_error")
        await interaction.response.send_message("⚠️ No pude leer las tareas.")
        print(e)

#Agregar tarea
@bot.command()  
@has_role("Instructor")  #Añadir Tareas por un role especifico
async def agregar_tarea(ctx, titulo: str, fecha: str, *, detalle: str,):
    nueva_tarea = {
        "titulo": titulo,
        "fecha": fecha,
        "detalle": detalle
    }

    try:
        if not os.path.exists('tareas.json'):
            with open('tareas.json', 'w') as f:
                json.dump([], f)

        with open('tareas.json', 'r') as archivo:
            tareas = json.load(archivo)

        tareas.append(nueva_tarea)

        with open('tareas.json', 'w') as archivo:
            json.dump(tareas, archivo, indent=4)

        log_text = f"""
                    ✅ TAREA AGREGADA
                    Usuario: {discord.user}
                    Contenido: {tarea} 
                    Fecha: {datetime.datetime.now()}
                    """
        upload_log_to_s3(log_text, filename_prefix="tarea_agregada")

        await ctx.send(f"✅ Tarea **{titulo}** añadida correctamente para el {fecha}.")
    except Exception as e:
        await ctx.send("⚠️ No se pudo agregar la tarea.")
        print(e)

@agregar_tarea.error #Role no autorizado
async def agregar_tarea_error(ctx, error):
    if isinstance(error, CheckFailure):
        log_text = f"""
                    🔴 ERROR al usar /agregar_tarea
                    Usuario: {discord.user}
                    Error: {error}
                    Fecha: {datetime.datetime.now()}
                    """
        upload_log_to_s3(log_text, filename_prefix="agregar_tarea_error")
        await ctx.send("⛔ No tienes permiso para usar este comando. Solo roles autorizados pueden agregar tareas.")

#Tip del día
@bot.tree.command(name="tip", description="Consejo del día para dominar AWS paso a paso ☁️📘")
async def tip(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    with open("tips.json", "r") as archivo:
            tips = json.load(archivo)
            tip_aleatorio = random.choice(tips)
            await interaction.followup.send(tip_aleatorio["tip"])

#Enviar tips automatizado a una hora
@tasks.loop(minutes=1) 
async def enviar_tip_diario():
    ahora = datetime.datetime.now().strftime("%H:%M")

    #Enviar a las 10:00am 
    if ahora == "10:00":
        canal = bot.get_channel(CANAL_ID)

        if canal:
            with open("tips.json", "r") as archivo:
                tips = json.load(archivo)
                tip_aleatorio = random.choice(tips) #Necesito almacenarlo para luego mostrarlo cuando sea solicitado en "Tip del día"
                await canal.send(tip_aleatorio) 

#Logs a S3
def upload_log_to_s3(log_text, filename_prefix="log"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{filename_prefix}_{timestamp}.txt"

    #Archivo temporal
    with open(filename, "w") as file:
        file.write(log_text)
    try:
        s3 = boto3.client("s3")
        bucket_name = "s3nsei-logs"
        s3.upload_file(filename, bucket_name, filename)
        print(f"✅ Log subido a S3: {filename}")
    except Exception as e:
        print(f"❌ Error al subir log a S3: {e}")
    finally:
        if os.path.exists(filename):
            os.remove(filename)  #Eliminando archivo temporal

#Comando de prueba para logs en S3
@bot.command(name="logtest")
async def logtest(ctx):
    log_text = f"""LOG DE COMANDO:
    Usuario: {ctx.author}
    Mensaje: {ctx.message.content}
    Canal: {ctx.channel}
    Fecha: {datetime.datetime.now()}
    """
    upload_log_to_s3(log_text, filename_prefix="comando_logtest")
    await ctx.send("📤 Tu mensaje ha sido guardado como log en S3.")

#Ayuda
@bot.tree.command(name="ayuda", description="Una guía de como podemos hablar 💡")
async def ayuda(interaction: discord.Interaction):
    await interaction.response.send_message('📖 Comandos disponibles:\n`/saludo` - Saludo de S3nsei\n`/tarea` - Próxima tarea o entrega\n`/tip` - Tip del curso del dia\n`/recursos` - Recursos útiles')

bot.run(TOKEN)

