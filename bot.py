import discord
from discord import app_commands

from config import DISCORD_TOKEN
import db

class Bot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await db.init()
        await self.tree.sync()


bot = Bot()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.tree.command(name="verify", description="Verify using your Student ID")
async def verify(interaction: discord.Interaction):
    await interaction.response.send_message("Verification message")

bot.run(DISCORD_TOKEN)