import os
from dotenv import load_dotenv
from s3nsei.bot import bot  # <- Aquí traes el objeto, no el módulo

load_dotenv("ini.env")
TOKEN = os.getenv("DISCORD_TOKEN")

if __name__ == "__main__":
    bot.run(TOKEN)
