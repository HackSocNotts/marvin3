import discord

from config import DISCORD_TOKEN, DISCORD_SV_ID, MEMBER_ROLE_ID
import db
import sums

class Bot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self):
        await db.init_db()

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

    student = await db.get_student(student_id)
    if not student:
        await interaction.edit_original_response(content=f"Student ID {student_id} not found - do you have a HackSoc membership?)")
        return
    elif student.expired:
        await interaction.edit_original_response(content=f"Student ID {student_id} is expired - have you renewed your membership?")
        return    

    sender_discord_id = str(interaction.user.id)
    ref_discord_id = student.discord_id
    if sender_discord_id != ref_discord_id:
        if ref_discord_id is not None or await db.discord_id_exists(sender_discord_id):
            await interaction.edit_original_response(content=f"Discord ID {sender_discord_id} is already paired with a student ID")
            return          
            
        await db.update_discord_id(student_id, sender_discord_id)

    await db.update_student_verified_at(student_id)

    # role assignment
    role = interaction.guild.get_role(MEMBER_ROLE_ID)
    if role is None:
        await interaction.edit_original_response(content=f"Error: Role **\"{role.name}\"** not found; does it exist?")
        return

    if role in interaction.user.roles:
        await interaction.edit_original_response(content=f"User {sender_discord_id} is already verified")
        return

    await interaction.user.add_roles(role)
    await interaction.edit_original_response(content=f"Student ID {student_id} verified (User: {sender_discord_id})")


@bot.tree.command(name="sync", description="Sync SUMS members to the database")
async def sync(interaction: discord.Interaction):

    await interaction.response.defer()

    try:
        new_members = await sums.sync()
    except Exception as e:
        await interaction.edit_original_response(content=f"SUMS sync failed: {e}")
        return
    
    await interaction.edit_original_response(content=f"SUMS sync completed ({new_members} members added)")

@bot.tree.command(name="purge", description="Mark expired memberships in the database")
async def purge(interaction: discord.Interaction):

    await interaction.response.defer()

    purged_members = await db.update_expired_members()
    
    await interaction.edit_original_response(content=f"Updated expired members successfully ({purged_members} marked as expired)")


bot.run(DISCORD_TOKEN)