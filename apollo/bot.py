import dotenv
import os
import discord
from discord.ext import commands

from cogs.Greeting import Greeting
from cogs.Minecraft import Minecraft

dotenv.load_dotenv()

TOKEN = os.environ["TOKEN"]
if not TOKEN:
    print("TOKEN environment variable is not present.")
    exit(1)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix=">")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    await bot.add_cog(Greeting(bot))
    await bot.add_cog(Minecraft(bot))


bot.run(TOKEN)
