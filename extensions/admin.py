import discord
from discord import app_commands
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self) -> None:
        super().__init__()

    @app_commands.command(name="clear", description="Clear messages.")
    @app_commands.describe(number="The number of messages to delete.")
    @app_commands.default_permissions(administrator=True)
    async def clear(self, interaction: discord.Interaction, number: int) -> None:
        await interaction.response.defer(thinking=True, ephemeral=True)
        if interaction.channel is None or not hasattr(interaction.channel, "purge"):
            await interaction.followup.send("This command can not be used here.", ephemeral=True)
            return
        deleted = await interaction.channel.purge(limit=number, reason="Clear command.")  # type: ignore
        await interaction.followup.send(f"{len(deleted)} message(s) deleted.", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Admin())