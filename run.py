import os
from s3nsei.bot import bot  
from s3nsei.secrets import load_secrets

secrets = load_secrets("discord-bot-token")
TOKEN = os.getenv("DISCORD_TOKEN")

if __name__ == "__main__":
    bot.run(TOKEN)
