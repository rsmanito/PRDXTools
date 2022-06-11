"""
Cog-file for synchronization nicknames and roles at GCA discord guild
"""
import logging

import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands

from plasmotools import settings

logger = logging.getLogger(__name__)


class GCATools(commands.Cog):
    """
    Cog for GCA(Grand Court of Appeal) tools - announcements
    """

    def __init__(self, bot: disnake.ext.commands.Bot):
        self.bot = bot

    async def log_for_admins(
            self,
            user: disnake.Member,
            result: str,
            clear_inventory: bool,
            additions: str,
            reset_pass: bool,
            conditions: str,
    ):
        """
        Logs data about unbanned / or

        """
        msg = (
            await self.bot.get_guild(settings.BACGuild.guild_id)
                .get_channel(settings.BACGuild.dev_logs_channel_id)
                .send(
                embed=disnake.Embed(
                    description=" | ".join(
                        [
                            user.display_name,
                            str(user),
                            result,
                            "Очищать инвентарь: " + str(clear_inventory),
                            "Сбрасывать проходку: " + str(reset_pass),
                            additions,
                            conditions,
                        ]
                    ),
                )
            )
        )

        await msg.add_reaction("✔")

    @commands.slash_command(
        name="заявка",
        guild_ids=[settings.BACGuild.guild_id],
    )
    async def request_placeholder(self, inter: ApplicationCommandInteraction):
        """
        Placeholder for sub commands
        """
        pass

    @request_placeholder.sub_command(
        name="отклонена",
        guild_ids=[settings.BACGuild.guild_id],
    )
    async def request_declined(
            self,
            inter: ApplicationCommandInteraction,
            user: disnake.Member,
            tripetto_id: str,
            reason: str,
    ):
        """
        Заявка отклонена

        Parameters
        ----------
        user: Игрок
        tripetto_id: ID заявки
        reason: Причина отклонения
        inter: ApplicationCommandInteraction object

        """
        await inter.response.defer(ephemeral=True)

        await (
            await self.bot.get_guild(settings.BACGuild.guild_id)
                .get_channel(settings.BACGuild.announcements_channel_id)
                .webhooks()
        )[0].send(
            content=user.mention,
            embed=disnake.Embed(
                title="🟥 Заявка отклонена",
                color=disnake.Color.red(),
                description=reason,
            ).set_footer(
                text=f"{inter.author.display_name} ㆍ ID: {tripetto_id}",
                icon_url=f"https://rp.plo.su/avatar/{inter.author.display_name}",
            ),
        )

        await inter.edit_original_message(content="Дело сделано")

    @request_placeholder.sub_command(
        name="одобрена",
        guild_ids=[settings.BACGuild.guild_id],
    )
    async def request_accepted(
            self,
            inter: ApplicationCommandInteraction,
            user: disnake.Member,
            tripetto_id: str,
            result: str = commands.Param(
                autocomplete=lambda *args: [
                    "Разбан",
                    "Красный варн снимается",
                    "Два красных варна снимаются",
                    "Разбан, красный варн снимается",
                    "Разбан, два красных варна снимаются",
                ]
            ),
            conditions: str = "",
            clear_inventory: bool = False,
            reset_pass: bool = False,
            additions: str = "",
    ):
        """
        Заявка одобрена

        Parameters
        ----------
        user: Игрок
        tripetto_id: ID заявки
        result: Тип рассмотренной заявки
        conditions: Условия
        clear_inventory: Очистить инвентарь
        reset_pass: Сбросить проходку
        additions: Дополнительные условия, например снятие красных при разбане
        inter: ApplicationCommandInteraction object


        """
        await inter.response.defer(ephemeral=True)

        embed = disnake.Embed(
            title="🟩 Заявка одобрена",
            color=disnake.Color.dark_green(),
            description=f"Положительно - **{result}{(', проходка обнуляется' if reset_pass else '')}**\n\n{additions}",
        ).set_footer(
            text=f"{inter.author.display_name} ㆍ ID: {tripetto_id}",
            icon_url=f"https://rp.plo.su/avatar/{inter.author.display_name}",
        )

        if conditions:
            embed.add_field(name="Требования к игроку", value=conditions)

        self.announcements_channel: disnake.NewsChannel
        await (
            await self.bot.get_guild(settings.BACGuild.guild_id)
                .get_channel(settings.BACGuild.announcements_channel_id)
                .webhooks()
        )[0].send(content=user.mention, embed=embed)

        await inter.edit_original_message(content="Дело сделано")

        await self.log_for_admins(
            user=user,
            result=result,
            additions=additions,
            conditions=conditions,
            clear_inventory=clear_inventory,
            reset_pass=reset_pass,
        )

    @request_placeholder.sub_command(
        name="допущена",
        guild_ids=[settings.BACGuild.guild_id],
    )
    async def request_approved(
            self,
            inter: ApplicationCommandInteraction,
            user: disnake.Member,
            tripetto_id: str,
    ):
        """
        Заявка будет рассмотрена в суде

        Parameters
        ----------
        user: Игрок
        tripetto_id: ID заявки
        inter: ApplicationCommandInteraction object


        """
        await inter.response.defer(ephemeral=True)

        gca_guild = self.bot.get_guild(settings.BACGuild.guild_id)

        self.announcements_channel: disnake.NewsChannel
        await (
            await gca_guild.get_channel(
                settings.BACGuild.announcements_channel_id
            ).webhooks()
        )[0].send(
            content=user.mention,
            embed=disnake.Embed(
                title="🟨 Заявка будет рассмотрена в суде",
                color=disnake.Color.yellow(),
            ).set_footer(
                text=f"{inter.author.display_name} ㆍ ID: {tripetto_id}",
                icon_url=f"https://rp.plo.su/avatar/{inter.author.display_name}",
            ),
        )

        await inter.edit_original_message(content="Дело сделано")
        await user.add_roles(
            gca_guild.get_role(settings.BACGuild.defendant_role_id),
            reason="Дело будет рассмотрено в суде",
        )

    @commands.slash_command(
        name="суд",
        guild_ids=[settings.BACGuild.guild_id],
    )
    async def court_placeholder(self, inter: ApplicationCommandInteraction):
        """
        Placeholder for sub commands
        """
        pass

    @court_placeholder.sub_command(
        name="отрицательно",
        guild_ids=[settings.BACGuild.guild_id],
    )
    async def court_declined(
            self,
            inter: ApplicationCommandInteraction,
            user: disnake.Member,
            tripetto_id: str,
            addition: str = "Вы сможете позже подать заявку на следующий апелляционный суд",
    ):
        """
        Заявка рассмотрена в суде

        Parameters
        ----------
        user: Игрок
        tripetto_id: ID заявки
        addition: Примечание для игрока
        inter: ApplicationCommandInteraction object

        """
        await inter.response.defer(ephemeral=True)

        embed = disnake.Embed(
            title="🟥 Заявка рассмотрена в суде",
            color=disnake.Color.red(),
            description="Результат - **Отрицательно**",
        ).set_footer(
            text=f"{inter.author.display_name} ㆍ ID: {tripetto_id}",
            icon_url=f"https://rp.plo.su/avatar/{inter.author.display_name}",
        )

        embed.add_field(name="Примечание", value=addition)

        gca_guild = self.bot.get_guild(settings.BACGuild.guild_id)

        self.announcements_channel: disnake.NewsChannel
        await (
            await gca_guild.get_channel(
                settings.BACGuild.announcements_channel_id
            ).webhooks()
        )[0].send(
            content=user.mention,
            embed=embed,
        )

        defendant_role = gca_guild.get_role(settings.BACGuild.defendant_role_id)

        if defendant_role in user.roles:
            await user.remove_roles(defendant_role)

        await inter.edit_original_message(content="Дело сделано")

    @court_placeholder.sub_command(
        name="положительно",
        guild_ids=[settings.BACGuild.guild_id],
    )
    async def court_accepted(
            self,
            inter: ApplicationCommandInteraction,
            user: disnake.Member,
            tripetto_id: str,
            result: str = commands.Param(
                autocomplete=lambda *args: [
                    "Разбан",
                    "Красный варн снимается",
                    "Два красных варна снимаются",
                    "Разбан, красный варн снимается",
                    "Разбан, два красных варна снимаются",
                ]
            ),
            conditions: str = "",
            clear_inventory: bool = False,
            reset_pass: bool = False,
            additions: str = "",
    ):
        """
        Заявка рассмотрена в суде

        Parameters
        ----------
        user: Игрок
        tripetto_id: ID заявки
        result: Тип рассмотренной заявки
        conditions: Условия
        clear_inventory: Очистить инвентарь
        reset_pass: Сбросить проходку
        additions: Дополнительные условия, например снятие красных при разбане
        inter: ApplicationCommandInteraction object

        """
        await inter.response.defer(ephemeral=True)

        embed = disnake.Embed(
            title="🟩 Заявка рассмотрена в суде",
            color=disnake.Color.dark_green(),
            description="Положительно - **{0}{1}**\n\n{2}".format(
                result, (f", проходка обнуляется" if reset_pass else ""), additions
            ),
        ).set_footer(
            text=f"{inter.author.display_name} ㆍ ID: {tripetto_id}",
            icon_url=f"https://rp.plo.su/avatar/{inter.author.display_name}",
        )

        if conditions:
            embed.add_field(name="Требования к игроку", value=conditions)

        gca_guild = self.bot.get_guild(settings.BACGuild.guild_id)

        self.announcements_channel: disnake.NewsChannel
        await (
            await gca_guild.get_channel(
                settings.BACGuild.announcements_channel_id
            ).webhooks()
        )[0].send(
            content=user.mention,
            embed=embed,
        )

        defendant_role = gca_guild.get_role(settings.BACGuild.defendant_role_id)

        if defendant_role in user.roles:
            await user.remove_roles(defendant_role)

        await inter.edit_original_message(content="Дело сделано")

        await self.log_for_admins(
            user=user,
            result=result,
            additions=additions,
            conditions=conditions,
            clear_inventory=clear_inventory,
            reset_pass=reset_pass,
        )

    async def cog_load(self):
        """
        Called when disnake bot object is ready
        """

        logger.info("%s Ready", __name__)


def setup(client):
    """
    Disnake internal setup function
    """
    client.add_cog(GCATools(client))
