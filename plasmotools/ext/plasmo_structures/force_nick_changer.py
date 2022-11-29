import logging

import disnake
from disnake.ext import commands

from plasmotools import settings
from plasmotools.utils.database import plasmo_structures as database

logger = logging.getLogger(__name__)


class ForceNickChanger(commands.Cog):
    def __init__(self, bot: disnake.ext.commands.Bot):
        self.bot = bot

    @commands.Cog.listener("on_member_update")
    async def force_nick_changer(self, before: disnake.Member, after: disnake.Member):
        """
        Change user's nickname if it differs in structure and on Plasmo
        """
        if before.nick == after.nick:
            return
        if before.guild.id == settings.PlasmoRPGuild.guild_id:
            return

        if database.get_guild(before.guild.id) is None:
            return
        plasmo_guild = self.bot.get_guild(settings.PlasmoRPGuild.guild_id)
        if plasmo_guild is None:
            if settings.DEBUG:
                return
            raise RuntimeError("Plasmo guild not found")

        plasmo_member = plasmo_guild.get_member(before.id)
        if plasmo_member is None:
            return

        if plasmo_member.display_name != after.display_name:
            await after.edit(nick=after.display_name, reason="Nickname change in structures is not allowed")

    async def cog_load(self):
        """
        Called when disnake bot object is ready
        """

        logger.info("%s Ready", __name__)


def setup(bot: disnake.ext.commands.Bot):
    """
    Disnake internal setup function
    """
    bot.add_cog(ForceNickChanger(bot))
