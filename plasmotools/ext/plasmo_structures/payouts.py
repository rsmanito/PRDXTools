import datetime
import logging
from typing import Optional

import disnake
import orm
from aiohttp import ClientSession
from disnake import ApplicationCommandInteraction
from disnake.ext import commands

from plasmotools import checks, settings
from plasmotools.checks import is_guild_registered
from plasmotools.utils import api, formatters
from plasmotools.utils import models
from plasmotools.utils.api import bank
from plasmotools.utils.api.tokens import get_token_scopes
from plasmotools.utils.autocompleters.bank import search_bank_cards_autocompleter
from plasmotools.utils.autocompleters.plasmo_structures import (
    payouts_projects_autocompleter,
)
from plasmotools.utils.embeds import build_simple_embed

logger = logging.getLogger(__name__)


# todo: Rewrite with buttons


class Payouts(commands.Cog):
    def __init__(self, bot: disnake.ext.commands.Bot):
        self.bot = bot

    # TODO:  payouts statistics
    # TODO: remove create/read/update/delete commands and combine it to /projects

    @commands.guild_only()
    @commands.slash_command(
        name="projects",
        dm_permission=False,
    )
    @is_guild_registered()
    @checks.blocked_users_slash_command_check()
    async def projects(self, inter: ApplicationCommandInteraction):
        """
        Помощь по проектам и выплатам {{PROJECTS_COMMAND}}
        """
        await inter.send(
            embed=disnake.Embed(
                color=disnake.Color.dark_green(),
                description="Проекты в Plasmo Tools - это упрощение системы выплат. Создайте проект через "
                "/проекты-создать чтобы получить доступ к </payout:1077320503632609291>\n\n"
                f"**Получение plasmo_token**\n Когда перейдете по ссылке, авторизуйте приложение.\n"
                f"Вас перенаправит на сайт, где вам нужно будет скопировать ваш токен из адресной строки:\n"
                f"pt.haffk.tech/oauth/#access_token=***123TOKEN123**&scope=...&token_type=...",
            ),
            ephemeral=True,
            components=[
                disnake.ui.Button(
                    url=settings.oauth2_url_for_projects,
                    emoji="🔗",
                    label="Получить plasmo token",
                )
            ],
        )

    @commands.guild_only()
    @commands.slash_command(name="проекты-создать", dm_permission=False)
    @commands.default_member_permissions(administrator=True)
    @checks.is_guild_registered()
    async def projects_create(  # todo: remove
        self,
        inter: ApplicationCommandInteraction,
        name: str,
        webhook_url: str,
        plasmo_bearer_token: str,
        from_card: int = commands.Param(gt=0, lt=10000),
    ):
        """
        Зарегистрировать проект

        Parameters
        ----------
        inter
        name: Название проекта, например "Интерпол"
        webhook_url: Ссылка на вебхук для отправки уведомлений (в формате https://discord.com/api/webhooks/...)
        from_card: Номер карты, с которой будет производиться выплата
        plasmo_bearer_token: Токен плазмо, используйте /проекты, чтобы узнать как его получить
        """
        # todo: autocomplete for from_card
        await inter.response.defer(ephemeral=True)
        await inter.edit_original_message(
            embed=disnake.Embed(
                color=disnake.Color.yellow(),
                title="Верифицирую токен...",
            ),
        )
        scopes = await get_token_scopes(plasmo_bearer_token)
        if "bank:transfer" not in scopes and "bank:manage" not in scopes:
            await inter.edit_original_message(
                embed=build_simple_embed(
                    "Указан неправильный токен. ||Missing bank:manage / bank:transfer scopes||\n"
                    f"Получите новый в [поддержке DDT]({settings.DevServer.support_invite})",
                    failure=True,
                ),
            )
            return
        await inter.edit_original_message(
            embed=disnake.Embed(
                color=disnake.Color.yellow(),
                title="Регистрирую проект...",
            ),
        )
        db_project = await models.StructureProject.objects.create(
            name=name,
            is_active=True,
            guild_discord_id=inter.guild.id,
            webhook_url=webhook_url,
            from_card=from_card,
            plasmo_bearer_token=plasmo_bearer_token,
        )
        await inter.edit_original_message(
            embed=disnake.Embed(
                color=disnake.Color.dark_green(),
                title="Проект успешно зарегистрирован",
                description=f"Проект: {name}\n"
                f"Вебхук: {webhook_url}\n"
                f"Карта: {from_card}\n"
                f"Токен: ||{plasmo_bearer_token[:-5]}...||\n"
                f"ID: {db_project.id}",
            ),
        )

    @commands.guild_only()
    @commands.slash_command(name="проекты-редактировать", dm_permission=False)
    @commands.default_member_permissions(administrator=True)
    @checks.blocked_users_slash_command_check()
    @is_guild_registered()
    async def projects_edit(  # todo: remove
        self,
        inter: ApplicationCommandInteraction,
        project_id: int,
        name: Optional[str] = None,
        webhook_url: Optional[str] = None,
        is_active: Optional[bool] = None,
        from_card: Optional[int] = commands.Param(default=None),
        plasmo_bearer_token: Optional[str] = None,
    ):
        """
        Редактировать проект в базе данных

        Parameters
        ----------
        inter
        project_id: Айди проекта
        webhook_url: Ссылка на вебхук для отправки уведомлений (https://discordapp.com/api/webhooks/{id}/{token})
        is_active: Доступен ли проект
        name: Название проекта, например "Интерпол" или "Постройка суда"
        from_card: Номер карты, с которой будет производиться выплата
        plasmo_bearer_token: Токен плазмо, используйте /проекты, чтобы узнать как его получить
        """
        await inter.response.defer(ephemeral=True)
        if not (
            await models.StructureProject.objects.filter(
                id=project_id, guild_discord_id=inter.guild.id
            ).exists()
        ):
            return await inter.send(
                embed=build_simple_embed("Проект не найден", failure=True),
                ephemeral=True,
            )

        db_project = await models.StructureProject.objects.get(
            id=project_id, guild_discord_id=inter.guild.id
        )
        await db_project.update(
            name=name if name is not None else db_project.name,
            is_active=is_active if is_active is not None else db_project.is_active,
            from_card=from_card if from_card is not None else db_project.from_card,
            plasmo_bearer_token=plasmo_bearer_token
            if plasmo_bearer_token is not None
            else db_project.plasmo_bearer_token,
            webhook_url=webhook_url
            if webhook_url is not None
            else db_project.webhook_url,
        )
        await inter.send(
            embed=build_simple_embed(
                "Проект отредактирован",
            ),
            ephemeral=True,
        )

    @commands.guild_only()
    @commands.slash_command(name="проекты-удалить", dm_permission=False)
    @commands.default_member_permissions(administrator=True)
    @checks.blocked_users_slash_command_check()
    @is_guild_registered()
    async def projects_delete(  # todo: remove
        self,
        inter: ApplicationCommandInteraction,
        project_id: int,
    ):
        """
        Удалить проект из базы данных

        Parameters
        ----------
        inter
        project_id: Айди проекта

        """
        await inter.response.defer(ephemeral=True)
        await models.StructureProject.objects.filter(
            id=project_id, guild_discord_id=inter.guild.id
        ).delete()
        await inter.edit_original_message(
            embed=build_simple_embed(
                "Проект удален",
            ),
        )

    @commands.guild_only()
    @commands.slash_command(name="проекты-список", dm_permission=False)
    @commands.default_member_permissions(administrator=True)
    @checks.blocked_users_slash_command_check()
    @is_guild_registered()
    async def projects_list(self, inter: ApplicationCommandInteraction):  # todo: remove
        """
        Получить список проектов на сервере
        """
        await inter.response.defer(ephemeral=True)
        db_projects = await models.StructureProject.objects.filter(
            guild_discord_id=inter.guild.id
        ).all()
        embed = disnake.Embed(
            color=disnake.Color.dark_green(),
            title=f"Все проекты {inter.guild.name}",
        ).set_footer(
            text="[Coming soon] Используйте /статистика, чтобы просмотреть статистику по проекту",
        )
        embed.add_field(
            name="Название проекта - [Доступность]",
            value="Айди / Карта для выплат / Токен \nВебхук",
        )
        for project in db_projects:
            embed.add_field(
                name=f"{project.name} - {'Активен' if project.is_active else 'Неактивен'}  ",
                value=f"{project.id} / {formatters.format_bank_card(project.from_card)} / "
                f"||{project.plasmo_bearer_token[:-5]}...||\n"
                f"||{project.webhook_url}||",
                inline=False,
            )

        await inter.edit_original_message(embed=embed)

    async def payout(
        self,
        interaction: disnake.Interaction,
        user: disnake.Member,
        amount: int,
        project,
        message: str,
        transaction_message: str = None,
    ) -> bool:
        if transaction_message is None:
            transaction_message = message

        if amount <= 0 or amount > 69420:
            await interaction.edit_original_message(
                embed=build_simple_embed(
                    "Сумма выплаты должна находиться в диапазоне 0 < `amount` <= 69420)",
                    failure=True,
                ),
            )
            return False

        if user.bot:
            await interaction.edit_original_message(
                embed=build_simple_embed("Ботам выплачивать нельзя", failure=True),
            )
            return False

        if not settings.DEBUG:
            plasmo_user = self.bot.get_guild(
                settings.PlasmoRPGuild.guild_id
            ).get_member(user.id)

            if plasmo_user is None or (
                plasmo_user.guild.get_role(settings.PlasmoRPGuild.player_role_id)
                not in plasmo_user.roles
                and plasmo_user.guild.get_role(
                    settings.PlasmoRPGuild.new_player_role_id
                )
                not in plasmo_user.roles
            ):
                await interaction.edit_original_message(
                    embed=build_simple_embed(
                        "Выплаты возможны только игрокам Plasmo RP", failure=True
                    ),
                )
                return False
            await interaction.edit_original_message(
                embed=disnake.Embed(
                    color=disnake.Color.yellow(),
                    description="Получаю карту для выплаты...",
                )
            )
        else:
            plasmo_user = user

        from_card = project.from_card
        user_card = (
            await models.PersonalSettings.objects.get_or_create(
                discord_id=user.id, defaults={}
            )
        )[0].saved_card
        if user_card is None:
            user_cards = sorted(
                [
                    card
                    for card in await bank.search_cards(
                        token=project.plasmo_bearer_token,
                        query=plasmo_user.display_name,
                    )
                    if card["id"] != from_card
                    and card["holder_type"] == 0  # User
                    and card["holder"]
                    == plasmo_user.display_name  # fixme: new nicknames system
                ],
                key=lambda card: card["value"],
                reverse=True,
            )

            if len(user_cards) == 0:
                await interaction.edit_original_message(
                    embed=build_simple_embed(
                        "Не удалось найти карту для выплаты, Plasmo Tools уведомит игрока об этом",
                        failure=True,
                    ),
                )
                try:
                    await user.send(
                        embed=disnake.Embed(
                            color=disnake.Color.dark_red(),
                            title="⚠ Plasmo Tools не смог произвести выплату",
                            description="Не удалось найти карту для выплаты, чтобы в дальнейшем получать выплаты от "
                            "структур оформите карту на свой аккаунт или укажите любую карту через "
                            "/установить-карту-для-выплат",
                        )
                    )
                except disnake.Forbidden:
                    await interaction.send(
                        embed=build_simple_embed(
                            f"У {user.mention} закрыты личные сообщения,"
                            f" вам придется лично попросить игрока "
                            f"установить карту через /установить-карту-для-выплат",
                            failure=True,
                        ),
                        ephemeral=True,
                    )
                return False

            user_card: int = user_cards[0]["id"]
            try:
                await user.send(
                    embed=disnake.Embed(
                        color=disnake.Color.dark_red(),
                        title="⚠ У вас не установлена карта для выплат",
                        description=f"Вы не установили карту для выплат. Бот установил карту "
                        f"**{formatters.format_bank_card(user_card)}** как основную.\n\n"
                        f"Воспользуйтесь **/установить-карту-для-выплат**, если хотите получать выплаты "
                        f"на другую карту",
                    )
                )
            except disnake.Forbidden:
                pass

            await models.PersonalSettings.objects.filter(discord_id=user.id).update(
                saved_card=user_card
            )

        await interaction.edit_original_message(
            embed=disnake.Embed(
                color=disnake.Color.yellow(), description="Перевожу алмазы..."
            )
        )
        if from_card == user_card:
            await interaction.edit_original_message(
                embed=build_simple_embed(
                    "Невозможно первести алмазы на эту карту", failure=True
                ),
            )
            return False
        status, error_message = await bank.transfer(
            token=project.plasmo_bearer_token,
            from_card=from_card,
            to_card=user_card,
            amount=amount,
            message=transaction_message,
        )
        if not status:
            await interaction.edit_original_message(
                embed=build_simple_embed(
                    "API вернуло ошибку: **" + error_message + "**", failure=True
                ),
            )
            return False
        await interaction.edit_original_message(
            embed=disnake.Embed(
                color=disnake.Color.yellow(),
                description="Отправляю оповещение о выплате...",
            )
        )

        embed = disnake.Embed(
            color=disnake.Color.dark_green(),
            description=f"{user.mention} получает выплату в размере **{amount}** алм. ",
        ).set_author(
            name=plasmo_user.display_name,
            icon_url="https://rp.plo.su/avatar/" + plasmo_user.display_name,
        )
        if message != "":
            embed.add_field(name="Комментарий", value=message)

        async with ClientSession() as session:
            webhook = disnake.Webhook.from_url(project.webhook_url, session=session)
            try:
                await webhook.send(
                    content=user.mention,
                    embed=embed,
                )
            except disnake.errors.NotFound:
                await interaction.edit_original_message(
                    embed=build_simple_embed(
                        "Не удалось получить доступ к вебхуку. Оплата прошла, но игрок не был оповещен",
                        failure=True,
                    ),
                )

        db_guild = await models.StructureGuild.objects.get(
            discord_id=interaction.guild.id
        )
        await self.bot.get_channel(db_guild.logs_channel_id).send(
            embed=embed.add_field("Выплатил", interaction.author.mention, inline=False)
            .add_field(
                name="Комментарий к переводу", value=transaction_message, inline=False
            )
            .add_field("Проект", project.name, inline=False)
            .add_field("С карты", formatters.format_bank_card(from_card), inline=False)
            .add_field(
                "На карту",
                formatters.format_bank_card(user_card),
                inline=False,
            )
        )

        await interaction.edit_original_message(
            embed=build_simple_embed(
                f"{user.mention} получил выплату в размере **{amount}** {settings.Emojis.diamond} на "
                f"карту {formatters.format_bank_card(user_card)}",
            ),
        )
        # todo: save failed payments and retry them later
        await models.StructurePayout.objects.create(
            project_id=project.id,
            user_id=user.id,
            payer_id=interaction.author.id,
            is_paid=True,
            from_card=from_card,
            to_card=user_card,
            amount=amount,
            message=message,
            date=datetime.datetime.now(),
        )
        await self.bot.get_channel(settings.DevServer.transactions_channel_id).send(
            embed=disnake.Embed(
                description=f"{formatters.format_bank_card(from_card)} -> "
                f"{amount} {settings.Emojis.diamond} -> {formatters.format_bank_card(user_card)}\n"
                f"Author {interaction.author.display_name} {interaction.author.mention}\n Message: {message}",
            )
        )
        return True

    @commands.guild_only()
    @commands.slash_command(dm_permission=False, name="payout")
    @checks.blocked_users_slash_command_check()
    @commands.default_member_permissions(administrator=True)
    @is_guild_registered()
    async def payout_command(
        self,
        inter: ApplicationCommandInteraction,
        user: disnake.Member = commands.Param(),
        amount: int = commands.Param(),
        project_id: str = commands.Param(
            autocomplete=payouts_projects_autocompleter,
        ),
        message: str = commands.Param(),
    ):
        """
        Payout diamonds to player {{PAYOUT_COMMAND}}

        Parameters
        ----------
        inter
        user: Player to pay {{PAYOUT_PLAYER}}
        amount: Amount of diamonds to payout {{PAYOUT_AMOUNT}}
        project_id: Payout project {{PAYOUT_PROJECT}}
        message: Comment to payout {{PAYOUT_MESSAGE}}
        """
        await inter.response.defer(ephemeral=True)
        if not project_id.isdigit():
            await inter.edit_original_message(
                embed=build_simple_embed("Проект не найден", failure=True),
            )
            return
        try:
            db_project = await models.StructureProject.objects.get(
                id=int(project_id), is_active=True, guild_discord_id=inter.guild.id
            )
        except orm.NoMatch:
            await inter.edit_original_message(
                embed=build_simple_embed(
                    f"Проект {project_id} не найден", failure=True
                ),
            )
            return

        await self.payout(inter, user, amount, db_project, message)

    @commands.slash_command(
        name="set-payouts-card",
    )
    @checks.blocked_users_slash_command_check()
    async def set_saved_card(
        self,
        inter: disnake.ApplicationCommandInteraction,
        card: str = commands.Param(
            autocomplete=search_bank_cards_autocompleter,
        ),
    ):
        """
        Set up your card for payouts {{SET_PAYOUTS_CARD_COMMAND}}

        Parameters
        ----------
        inter
        card: Card number, format: 9000 or EB-9000. EB-0142 -> 142. EB-3666 -> 3666 {{SET_PAYOUTS_CARD_PARAM}}
        """
        await inter.response.defer(ephemeral=True)
        try:
            card_id = int(card.replace(" ", "").replace("EB-", "").replace("ЕВ-", ""))
            if card_id < 0 or card_id > 9999:
                raise ValueError
        except ValueError:
            await inter.edit_original_message(
                embed=build_simple_embed(
                    "Не удалось распознать номер карты", failure=True
                ),
            )
            return

        await inter.edit_original_message(
            embed=disnake.Embed(
                color=disnake.Color.yellow(), description="Получаю данные о карте..."
            )
        )

        api_card = await api.bank.get_card_data(card_id)
        if api_card is None:
            await inter.edit_original_message(
                embed=build_simple_embed(
                    "Не удалось получить данные о карте", failure=True
                ),
            )
            return

        await models.PersonalSettings.objects.update_or_create(
            discord_id=inter.author.id,
            defaults={
                "saved_card": card_id,
            },
        )
        await inter.edit_original_message(
            embed=build_simple_embed(
                "Карта для выплат успешно обновлена\n"
                f" {formatters.format_bank_card(card_id)} - {api_card['name']}\n"
                f"Принадлежит {api_card['holder']}",
            )
        )

    async def cog_load(self):
        logger.info("%s loaded", __name__)


def setup(bot: disnake.ext.commands.Bot):
    """
    Disnake internal setup function
    """
    bot.add_cog(Payouts(bot))
