import discord

from config import DISCORD_TOKEN, DISCORD_SV_ID, MEMBER_ROLE_ID
from db import get_discord_id, init_db, update_discord_id, update_student_verified_at, student_exists


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

    await interaction.response.defer()

    student = await student_exists(student_id)
    if not student:
        await interaction.edit_original_response(content=f"Student ID {student_id} not found (Is your HackSoc membership valid?)")
        return

    sender_discord_id = str(interaction.user.id)
    ref_discord_id = await get_discord_id(student_id)
    if sender_discord_id != ref_discord_id:
        if ref_discord_id is not None:
            await interaction.edit_original_response(content=f"Discord ID {sender_discord_id} is already paired with a student ID")
            return

        await update_discord_id(student_id, sender_discord_id)

    await update_student_verified_at(student_id)

    # role assignment
    role = interaction.guild.get_role(MEMBER_ROLE_ID)
    if role is None:
        await interaction.edit_original_response(content=f"Error: Role **\"{role.name}\"** not found; does it exist?")
        return

    if role in interaction.user.roles:
        await interaction.edit_original_response(content=f"{sender_discord_id} is already verified")
        return

    await interaction.user.add_roles(role)
    await interaction.edit_original_response(content=f"Student ID {student_id} verified (User: {sender_discord_id})")

bot.run(DISCORD_TOKEN)