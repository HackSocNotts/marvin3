import discord

from config import DISCORD_TOKEN, DISCORD_SV_ID
from db import init_db, verify_student_exists


class Bot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self):
        await init_db()

        guild = discord.Object(id=DISCORD_SV_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

bot = Bot()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.tree.command(name="verify", description="Verify using your Student ID")
async def verify(interaction: discord.Interaction, student_id: str):
    exists = await verify_student_exists(student_id)

    if exists:
        await interaction.response.send_message("Verification message")
    else:
        await interaction.response.send_message("NOT verified")

bot.run(DISCORD_TOKEN)