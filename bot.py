import discord
import json
import os
import random
import datetime
from discord.ext.commands import has_role, CheckFailure
from discord.ext import commands, tasks
from dotenv import load_dotenv


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
        await interaction.response.send_message("⚠️ No pude leer las tareas.")
        print(e)

#Agregar tarea
@bot.command()  
@has_role("Instructor")  #Añadir Tareas por un role especifico
async def agregar_tarea(ctx, titulo: str, fecha: str, *, detalle: str):
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

        await ctx.send(f"✅ Tarea **{titulo}** añadida correctamente para el {fecha}.")
    except Exception as e:
        await ctx.send("⚠️ No se pudo agregar la tarea.")
        print(e)

@agregar_tarea.error #Role no autorizado
async def agregar_tarea_error(ctx, error):
    if isinstance(error, CheckFailure):
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
                
#Ayuda
@bot.tree.command(name="ayuda", description="Una guía de como podemos hablar 💡")
async def ayuda(interaction: discord.Interaction):
    await interaction.response.send_message('📖 Comandos disponibles:\n`/saludo` - Saludo de S3nsei\n`/tarea` - Próxima tarea o entrega\n`/tip` - Tip del curso del dia\n`/recursos` - Recursos útiles')

bot.run(TOKEN)

