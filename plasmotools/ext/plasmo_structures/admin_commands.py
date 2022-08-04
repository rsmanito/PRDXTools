import logging
from typing import Optional

import disnake
from aiohttp import ClientSession
from disnake import ApplicationCommandInteraction
from disnake.ext import commands

from plasmotools import settings
from plasmotools.utils import formatters, autocompleters
from plasmotools.utils.api import bank
from plasmotools.utils.api.tokens import get_token_scopes
from plasmotools.utils.database import plasmo_structures as database

logger = logging.getLogger(__name__)


# todo: Rewrite with buttons


class AdminCommands(commands.Cog):
    def __init__(self, bot: disnake.ext.commands.Bot):
        self.bot = bot

    @commands.is_owner()
    @commands.guild_only()
    @commands.slash_command()
    @commands.default_member_permissions(administrator=True)
    async def register_guild(
            self,
            inter: ApplicationCommandInteraction,
            alias: str,
            player_role: disnake.Role,
            head_role: disnake.Role,
            public_chat: disnake.TextChannel,
            logs_channel: disnake.TextChannel,
    ):
        """
        Регистрация/редактирование сервера в базе данных
        """
        guild: database.Guild = await database.get_guild(inter.guild.id)
        if guild is not None:
            embed = disnake.Embed(
                title="GUILD CHANGELOG",
                description=f"""
                `alias`: {guild.alias} -> {alias}
                `player_role`: {guild.player_role_id} -> {player_role.name}
                `head_role`: {guild.head_role_id} -> {head_role.name}
                `public_chat`: {guild.public_chat_channel_id} -> {public_chat.name}
                `logs_channel`: {guild.logs_channel_id} -> {logs_channel.name}
                """,
                color=disnake.Color.green(),
            )
            await inter.send(embed=embed, ephemeral=True)
        guild: database.Guild = await database.register_guild(
            discord_id=inter.guild.id,
            alias=alias,
            player_role_id=player_role.id,
            head_role_id=head_role.id,
            public_chat_channel_id=public_chat.id,
            logs_channel_id=logs_channel.id,
        )
        await inter.send(
            embed=disnake.Embed(
                color=disnake.Color.green(),
                title="Успех",
                description=f"Сервер {inter.guild.name} зарегистрирован как офицальная структура.",
            ).add_field(
                name="guild data",
                value=f"""
            `alias`: {guild.alias}
            `player_role`: {guild.player_role_id}
            `head_role`: {guild.head_role_id}
            `public_chat`: {guild.public_chat_channel_id}
            `logs_channel`: {guild.logs_channel_id}
            """,
            ),
            ephemeral=True,
        )

    @commands.is_owner()
    @commands.guild_only()
    @commands.slash_command()
    @commands.default_member_permissions(administrator=True)
    async def wipe_guild(self, inter: ApplicationCommandInteraction):
        """
        Удалить сервер из базы данных
        """
        guild = await database.get_guild(inter.guild.id)
        if guild is None:
            await inter.send(
                embed=disnake.Embed(
                    color=disnake.Color.red(),
                    title="Ошибка",
                    description="Сервер не зарегистрирован как офицальная структура.\n",
                ),
                ephemeral=True,
            )
            return

        projects = await database.get_projects(guild.id)
        roles = await database.get_roles(guild.id)
        [await project.delete() for project in projects]
        [await role.delete() for role in roles]
        await guild.delete()
        await inter.send(
            embed=disnake.Embed(
                color=disnake.Color.green(),
                title="Успех",
                description=f"Сервер {inter.guild.name} и все привязанные к нему проекты и роли "
                            f"удалены из БД **PlasmoTools.**",
            ),
            ephemeral=True,
        )

    @commands.guild_only()
    @commands.slash_command()
    @commands.default_member_permissions(administrator=True)
    async def get_guild_data(self, inter: ApplicationCommandInteraction):
        """
        Получить данные о сервере
        """
        guild = await database.get_guild(inter.guild.id)
        if guild is None:
            await inter.send(
                embed=disnake.Embed(
                    color=disnake.Color.red(),
                    title="Ошибка",
                    description="404, Not Found",
                ),
                ephemeral=True,
            )
            return
        await inter.send(
            embed=disnake.Embed(
                color=disnake.Color.green(),
                title="Успех",
                description=f"Сервер {inter.guild.name} зарегистрирован как офицальная структура.",
            ).add_field(
                name="guild data",
                value=f"""
            `alias`: {guild.alias}
            `player_role`: <@&{guild.player_role_id}> / {guild.player_role_id} 
            `head_role`: <@&{guild.head_role_id}> / {guild.head_role_id} 
            `public_chat`: <#{guild.public_chat_channel_id}> / {guild.public_chat_channel_id} 
            `logs_channel`: <#{guild.logs_channel_id}> / {guild.logs_channel_id} 
            """,
            ),
            ephemeral=True,
        )

    @commands.guild_only()
    @commands.slash_command(name="роли-список")
    @commands.default_member_permissions(administrator=True)
    async def roles_list(self, inter: ApplicationCommandInteraction):
        """
        Получить список ролей в сервере
        """
        roles = await database.get_roles(inter.guild.id)
        embed = disnake.Embed(
            color=disnake.Color.green(),
            title=f"Все роли {inter.guild.name}",
        )
        if len(roles) == 0:
            embed.add_field(
                name="Роли не найдены",
                value="Добавьте через `/роли-добавить`",
            )
        else:
            embed.add_field(
                name="Название роли",
                value="[Доступна ли роль] Пинг роли / Айди роли\nВебхук",
            )
            for role in roles:
                embed.add_field(
                    name=f"{role.name}",
                    value=f"{settings.Emojis.enabled if role.available else settings.Emojis.disabled} "
                          f"<@&{role.role_discord_id}> / `{role.role_discord_id}` \n ||{role.webhook_url}||",
                    inline=False,
                )

        await inter.send(embed=embed, ephemeral=True)

    @commands.guild_only()
    @commands.slash_command(name="роли-добавить")
    @commands.default_member_permissions(administrator=True)
    async def roles_add(
            self,
            inter: ApplicationCommandInteraction,
            role: disnake.Role,
            name: str,
            webhook_url: str,
            available: bool = True,
    ):
        """
        Добавить роль в базу данных

        Parameters
        ----------
        role: Роль
        webhook_url: Ссылка на вебхук для отправки уведомлений (в формате https://discord.com/api/webhooks/...)
        available: Доступна ли роль для найма и снятия
        name: Название роли, например "Интерпол"

        """
        # TODO: Check webhook url with regex
        guild = await database.get_guild(inter.guild.id)
        if guild is None:
            await inter.send(
                embed=disnake.Embed(
                    color=disnake.Color.red(),
                    title="Ошибка",
                    description="Сервер не зарегистрирован как офицальная структура.\n"
                                "Если вы считаете что это ошибка - обратитесь в "
                                f"[поддержку digital drugs technologies]({settings.DevServer.support_invite})",
                ),
                ephemeral=True,
            )
            return

        if role.id == guild.player_role_id or role.id == guild.head_role_id:
            await inter.send(
                embed=disnake.Embed(
                    color=disnake.Color.red(),
                    title="Ошибка",
                    description="Эта роль не может быть закреплена как нанимаемая\n"
                                "Если вы считаете что это ошибка - обратитесь в "
                                f"[поддержку digital drugs technologies]{settings.DevServer.support_invite}",
                ),
                ephemeral=True,
            )
            return
        await inter.response.defer(ephemeral=True)
        db_role = await database.get_role(role.id)
        if db_role is not None:
            await db_role.edit(
                name=name,
                webhook_url=webhook_url,
                available=available,
            )
            await inter.edit_original_message(
                embed=disnake.Embed(
                    color=disnake.Color.green(),
                    title="Роль обновлена",
                    description=f"Роль `{name}` обновлена",
                ),
            )
        else:
            await database.add_role(
                guild_discord_id=inter.guild.id,
                role_discord_id=role.id,
                name=name,
                webhook_url=webhook_url,
                available=available,
            )
            await inter.edit_original_message(
                embed=disnake.Embed(
                    color=disnake.Color.green(),
                    title="Роль создана",
                    description=f"Роль `{name}` зарегистрирована",
                ),
            )

    @commands.guild_only()
    @commands.slash_command(name="роли-удалить")
    @commands.default_member_permissions(administrator=True)
    async def roles_delete(
            self,
            inter: ApplicationCommandInteraction,
            role: disnake.Role,
    ):
        """
        Удалить роль из базы данных
        """
        db_role = await database.get_role(role.id)
        if db_role is None:
            await inter.send(
                embed=disnake.Embed(
                    color=disnake.Color.red(),
                    title="Ошибка",
                    description="Роль не найдена в базе данных",
                ),
                ephemeral=True,
            )
            return
        await db_role.delete()

        await inter.send(
            embed=disnake.Embed(
                color=disnake.Color.green(),
                title="Роль удалена",
            ),
            ephemeral=True,
        )

    @commands.guild_only()
    @commands.slash_command(name="роли-редактировать")
    @commands.default_member_permissions(administrator=True)
    async def roles_edit(
            self,
            inter: ApplicationCommandInteraction,
            role: disnake.Role,
            name: str = None,
            webhook_url: str = None,
            available: bool = None,
    ):
        """
        Редактировать роль в базе данных

        Parameters
        ----------
        role: Роль
        webhook_url: Ссылка на вебхук для отправки уведомлений (https://discordapp.com/api/webhooks/{id}/{token})
        available: Доступна ли роль для найма и снятия
        name: Название роли, например "Интерпол"

        """
        db_role = await database.get_role(role.id)
        if db_role is None:
            await inter.send(
                embed=disnake.Embed(
                    color=disnake.Color.red(),
                    title="Ошибка",
                    description="Роль не найдена в базе данных",
                ),
                ephemeral=True,
            )
            return
        await db_role.edit(
            name=name,
            webhook_url=webhook_url,
            available=available,
        )

        await inter.send(
            embed=disnake.Embed(
                color=disnake.Color.green(),
                title="Роль отредактирована",
            ),
            ephemeral=True,
        )

    # TODO: Projects / payouts statistics

    # TODO: move roles, projects and payouts to separate files

    @commands.guild_only()
    @commands.slash_command(name="проекты")
    async def projects(self, inter: ApplicationCommandInteraction):
        """
        Помощь по проектам и выплатам
        """
        guild = await database.get_guild(inter.guild.id)
        if guild is None:
            await inter.send(
                embed=disnake.Embed(
                    color=disnake.Color.red(),
                    title="Ошибка",
                    description="Сервер не зарегистрирован как офицальная структура.\n"
                                "Если вы считаете что это ошибка - обратитесь в "
                                f"[поддержку digital drugs technologies]({settings.DevServer.support_invite})",
                ),
                ephemeral=True,
            )
            return
        await inter.send(
            embed=disnake.Embed(
                color=disnake.Color.green(),
                description="Проекты в Plasmo Tools - это упрощение системы выплат. Создайте проект через "
                            "/проекты-создать чтобы получить доступ к /выплата\n\n"
                            f"**plasmo_token**: Чтобы получить токен плазмо - "
                            f"откройте тикет в [дискорде DDT]({settings.DevServer.support_invite}). (Как только мне "
                            f"будет не лень я сделаю адекватное автоматическое получение токена)",
            ),
            ephemeral=True,
        )

    @commands.guild_only()
    @commands.slash_command(name="проекты-создать")
    @commands.default_member_permissions(administrator=True)
    async def projects_create(
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
        name: Название проекта, например "Интерпол"
        webhook_url: Ссылка на вебхук для отправки уведомлений (в формате https://discord.com/api/webhooks/...)
        from_card: Номер карты, с которой будет производиться выплата
        plasmo_bearer_token: Токен плазмо, используйте /проекты, чтобы узнать как его получить
        """
        # todo: автокопмлит для карт
        guild = await database.get_guild(inter.guild.id)
        if guild is None:
            await inter.send(
                embed=disnake.Embed(
                    color=disnake.Color.red(),
                    title="Ошибка",
                    description="Сервер не зарегистрирован как офицальная структура.\n"
                                "Если вы считаете что это ошибка - обратитесь в "
                                f"[поддержку digital drugs technologies]({settings.DevServer.support_invite})",
                ),
                ephemeral=True,
            )
            return
        await inter.response.defer(ephemeral=True)
        await inter.edit_original_message(
            embed=disnake.Embed(
                color=disnake.Color.dark_green(),
                title="Верифицирую токен...",
            ),
        )
        scopes = await get_token_scopes(plasmo_bearer_token)
        if "bank:transfer" not in scopes and "bank:manage" not in scopes:
            await inter.edit_original_message(
                embed=disnake.Embed(
                    color=disnake.Color.red(),
                    title="Ошибка",
                    description="Указан неправильный токен. ||Missing bank:manage / bank:transfer scopes||\n"
                                f"Получите новый в [поддержке DDT]({settings.DevServer.support_invite})",
                ),
            )
            return
        await inter.edit_original_message(
            embed=disnake.Embed(
                color=disnake.Color.dark_green(),
                title="Регистрирую проект...",
            ),
        )
        db_project = await database.register_project(
            name=name,
            guild_discord_id=inter.guild.id,
            is_active=True,
            webhook_url=webhook_url,
            from_card=from_card,
            plasmo_bearer_token=plasmo_bearer_token,
        )
        await inter.edit_original_message(
            embed=disnake.Embed(
                color=disnake.Color.green(),
                title="Проект успешно зарегистрирован",
                description=f"Проект: {name}\n"
                            f"Вебхук: {webhook_url}\n"
                            f"Карта: {from_card}\n"
                            f"Токен: ||{plasmo_bearer_token[:-5]}\\*\\*\\*\\*||\n"
                            f"ID: {db_project.id}",
            ),
        )

    @commands.guild_only()
    @commands.slash_command(name="проекты-редактировать")
    @commands.default_member_permissions(administrator=True)
    async def projects_edit(
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
        project_id: Айди проекта
        webhook_url: Ссылка на вебхук для отправки уведомлений (https://discordapp.com/api/webhooks/{id}/{token})
        is_active: Доступен ли проект
        name: Название проекта, например "Интерпол" или "Постройка суда"
        from_card: Номер карты, с которой будет производиться выплата
        plasmo_bearer_token: Токен плазмо, используйте /проекты, чтобы узнать как его получить
        """
        await inter.response.defer(ephemeral=True)
        db_project = await database.get_project(project_id)
        if db_project is None:
            await inter.send(
                embed=disnake.Embed(
                    color=disnake.Color.red(),
                    title="Ошибка",
                    description="Проект не найден",
                ),
                ephemeral=True,
            )
            return
        await db_project.edit(
            name=name,
            is_active=is_active,
            webhook_url=webhook_url,
            from_card=from_card,
            plasmo_bearer_token=plasmo_bearer_token,
        )

        await inter.send(
            embed=disnake.Embed(
                color=disnake.Color.green(),
                title="Проект отредактирован",
            ),
            ephemeral=True,
        )

    @commands.guild_only()
    @commands.slash_command(name="проекты-удалить")
    @commands.default_member_permissions(administrator=True)
    async def projects_delete(
            self,
            inter: ApplicationCommandInteraction,
            project_id: int,
    ):
        """
        Удалить проект из базы данных

        Parameters
        ----------
        project_id: Айди проекта

        """
        await inter.response.defer(ephemeral=True)
        db_project = await database.get_project(project_id)
        if db_project is None:
            await inter.edit_original_message(
                embed=disnake.Embed(
                    color=disnake.Color.red(),
                    title="Ошибка",
                    description="Проект не найден",
                ),
            )
            return
        await db_project.delete()

        await inter.edit_original_message(
            embed=disnake.Embed(
                color=disnake.Color.green(),
                title="Проект удален",
            ),
        )

    @commands.guild_only()
    @commands.slash_command(name="проекты-список")
    @commands.default_member_permissions(administrator=True)
    async def roles_list(self, inter: ApplicationCommandInteraction):
        """
        Получить список проектов на сервере
        """
        await inter.response.defer(ephemeral=True)
        projects = await database.get_projects(guild_discord_id=inter.guild.id)
        embed = disnake.Embed(
            color=disnake.Color.green(),
            title=f"Все проекты {inter.guild.name}",
        ).set_footer(
            text="[Пока не доступно] Используйте /статистика, чтобы просмотреть статистику по проекту",
        )
        if len(projects) == 0:
            embed.add_field(
                name="Проекты не найдены",
                value="Создайте первый через `/проекты-создать`",
            )
        else:
            embed.add_field(
                name="[Доступность] Название проекта",
                value="Айди / Карта / Токен \nВебхук",
            )
            for project in projects:
                project: database.Project
                embed.add_field(
                    name=f"{project.name} - {'Активен' if project.is_active else 'Неактивен'}  ",
                    value=f"{project.id} / {formatters.format_bank_card(project.from_card)} / ||{project.plasmo_bearer_token[:-5]}\\*\\*\\*\\*||\n"
                          f"||{project.webhook_url}||",
                    inline=False,
                )

        await inter.edit_original_message(embed=embed)

    @commands.guild_only()
    @commands.slash_command(name="выплата")
    @commands.default_member_permissions(administrator=True)
    async def payout_command(
            self,
            inter: ApplicationCommandInteraction,
            user: disnake.Member,
            amount: int,
            project: str = commands.Param(
                autocomplete=autocompleters.payouts_projects_autocompleter
            ),
            message: str = "",
    ):
        """
        Выплатить игроку алмазы

        Parameters
        ----------
        user: Игрок, которому нужно выплатить алмазы
        amount: Количество алмазов, которое нужно выплатить
        project: Проект, от имени которого производится выплата
        message: Сообщение, которое будет отправлено игроку
        """
        await inter.response.defer(ephemeral=True)
        try:
            db_project = await database.get_project(int(project))
            if db_project is None:
                raise ValueError("Проект не найден")
        except ValueError:
            await inter.edit_original_message(
                embed=disnake.Embed(
                    color=disnake.Color.red(),
                    title="Ошибка",
                    description="Проект не найден",
                ),
            )
            return
        guild = await database.get_guild(inter.guild.id)
        if guild is None:
            await inter.edit_original_message(
                embed=disnake.Embed(
                    color=disnake.Color.red(),
                    title="Ошибка",
                    description="Сервер не зарегистрирован как офицальная структура.\n"
                                "Если вы считаете что это ошибка - обратитесь в "
                                f"[поддержку digital drugs technologies]({settings.DevServer.support_invite})",
                ),
            )
            return
        await inter.edit_original_message(
            embed=disnake.Embed(
                color=disnake.Color.yellow(), description="Проверяю игрока..."
            )
        )
        plasmo_user = self.bot.get_guild(settings.PlasmoRPGuild.guild_id).get_member(
            user.id
        )
        if (
                user.bot
                or plasmo_user is None
                or plasmo_user.guild.get_role(settings.PlasmoRPGuild.player_role_id)
                not in plasmo_user.roles
        ):
            await inter.edit_original_message(
                embed=disnake.Embed(
                    color=disnake.Color.red(),
                    title="Ошибка",
                    description="Невозможно выплатить этому пользователю",
                ),
            )
            return
        # todo: get saved cards from database
        await inter.edit_original_message(
            embed=disnake.Embed(
                color=disnake.Color.yellow(), description="Получаю карту для выплаты..."
            )
        )
        from_card = db_project.from_card
        user_cards = sorted(
            [
                card
                for card in await bank.search_cards(
                token=db_project.plasmo_bearer_token,
                query=plasmo_user.display_name,
            )
                if card["id"] != from_card
                   and card["holder_type"] == 0
                   and card["holder"] == plasmo_user.display_name
            ],
            key=lambda card: card["value"],
            reverse=True,
        )
        if len(user_cards) == 0:
            await inter.edit_original_message(
                embed=disnake.Embed(
                    color=disnake.Color.red(),
                    title="Ошибка",
                    description="Не удалось найти карту для выплаты, Plasmo Tools уведомит игрока об этом",
                ),
            )
            try:
                await user.send(
                    embed=disnake.Embed(
                        color=disnake.Color.red(),
                        title="⚠ Plasmo Tools не смог произвести выплату",
                        description="Не удалось найти карту для выплаты, чтобы в дальнейшем получать выплаты от "
                                    "структур оформите карту на свой аккаунт или укажите любую карту через "
                                    "/установить-карту-для-выплат",
                    )
                )
            except disnake.Forbidden:
                await inter.send(
                    embed=disnake.Embed(
                        color=disnake.Color.red(),
                        title="Ошибка",
                        description=f"У {user.mention} закрыты личные сообщения, вам придется лично попросить игрока "
                                    f"установить карту через /установить-карту-для-выплат",
                    ),
                    ephemeral=True,
                )
            return
        await inter.edit_original_message(
            embed=disnake.Embed(
                color=disnake.Color.yellow(), description="Перевожу алмазы..."
            )
        )
        status, error_message = await bank.transfer(
            token=db_project.plasmo_bearer_token,
            from_card=from_card,
            to_card=user_cards[0]["id"],
            amount=amount,
            message=message,
        )
        if not status:
            await inter.edit_original_message(
                embed=disnake.Embed(
                    color=disnake.Color.red(),
                    title="Ошибка",
                    description="API вернуло ошибку:" + error_message,
                ),
            )
            return
        await inter.edit_original_message(
            embed=disnake.Embed(
                color=disnake.Color.yellow(),
                description="Отправляю оповещение о выплате...",
            )
        )

        embed = disnake.Embed(
            color=disnake.Color.green(),
            description=f"{user.mention} получает выплату в размере **{amount}** алм. ",
        ).set_author(
            name=plasmo_user.display_name,
            icon_url="https://rp.plo.su/avatar/" + plasmo_user.display_name,
        )
        if message != "":
            embed.add_field(name="Комментарий", value=message)

        async with ClientSession() as session:
            webhook = disnake.Webhook.from_url(db_project.webhook_url, session=session)
            try:
                await webhook.send(
                    content=user.mention,
                    embed=embed,
                )
            except disnake.errors.NotFound:

                await inter.edit_original_message(
                    embed=disnake.Embed(
                        color=disnake.Color.red(),
                        title="Ошибка",
                        description="Не удалось получить доступ к вебхуку. Оплата прошла, но игрок не был оповещен",
                    ),
                )

        await self.bot.get_channel(guild.logs_channel_id).send(
            embed=embed
            .add_field("Выплатил", inter.author.mention, inline=False)
            .add_field("Проект", db_project.name, inline=False)
            .add_field("С карты", formatters.format_bank_card(from_card), inline=False)
            .add_field("На карту", formatters.format_bank_card(user_cards[0]["id"]), inline=False)
        )

        await inter.edit_original_message(
            embed=disnake.Embed(
                color=disnake.Color.green(),
                title="Успех",
                description=f"{user.mention} получил выплату в размере **{amount}** {settings.Emojis.diamond} на "
                            f"карту {formatters.format_bank_card(user_cards[0]['id'])}",
            ),
        )
        # todo: save failed payments and retry them later
        await database.register_payout_entry(
            project_id=db_project.id,
            user_id=user.id,
            amount=amount,
            message=message,
            from_card=from_card,
            to_card=user_cards[0]["id"],
            is_payed=True
        )

    async def cog_load(self):
        """
        Called when disnake bot object is ready
        """

        logger.info("%s Ready", __name__)


def setup(bot: disnake.ext.commands.Bot):
    """
    Disnake internal setup function
    """
    bot.add_cog(AdminCommands(bot))
