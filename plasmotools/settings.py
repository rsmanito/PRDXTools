import logging
import os
from builtins import bool
from dataclasses import dataclass

import dotenv
import yaml

logger = logging.getLogger(__name__)

dotenv.load_dotenv()

with open("config.yml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)
    config = config["SETTINGS"]

DEBUG = bool(int(os.getenv("BOT_DEBUG", "0")))
TOKEN = os.getenv("TOKEN", None)
PT_PLASMO_TOKEN = os.getenv("PLASMO_TOKEN", None)
if PT_PLASMO_TOKEN is None:
    logger.critical("PLASMO_TOKEN is missing")
PT_PLASMO_COOKIES = os.getenv("PLASMO_COOKIE", None)
if PT_PLASMO_COOKIES is None:
    logger.critical("PLASMO_COOKIE is missing")
__version__ = "1.6.0" + ("-alpha" if DEBUG else "")

DATABASE_PATH = config["DATABASE_PATH"]
HELP_URL = config["HELP_URL"]
oauth2_url_for_projects = config["OAUTH2_URL_FOR_PROJECTS"]

blocked_users_ids = config["BLOCKED_USER_IDS"]
owner_ids = config["OWNER_IDS"]

INTERPOL_UNMANAGED_PENALTIES_CHANNEL_ID = config[
    "INTERPOL_UNMANAGED_PENALTIES_CHANNEL_ID"
]
ECONOMY_ARTODEL_LICENSE_ROLE_ID = config["ECONOMY_ARTODEL_LICENSE_ROLE_ID"]
ECONOMY_DD_OPERATIONS_CHANNEL_ID = config["ECONOMY_DD_OPERATIONS_CHANNEL_ID"]
ECONOMY_PATENTS_PUBLIC_CHANNEL_ID = config["ECONOMY_PATENTS_PUBLIC_CHANNEL_ID"]
ECONOMY_PATENTS_MODERATOR_CHANNEL_ID = config["ECONOMY_PATENTS_MODERATOR_CHANNEL_ID"]
ECONOMY_PATENTS_MODERATOR_ROLE_ID = config["ECONOMY_PATENTS_MODERATOR_ROLE_ID"]
DD_BANK_PATENTS_CARD = config["DD_BANK_PATENTS_CARD"]
ECONOMY_PATENTS_TREASURY_CARD = config["ECONOMY_PATENTS_TREASURY_CARD"]
ECONOMY_MAIN_TREASURY_CARD = config["ECONOMY_MAIN_TREASURY_CARD"]
ECONOMY_FAILED_PAYMENTS_ROLE_ID = config["ECONOMY_FAILED_PAYMENTS_ROLE_ID"]
ECONOMY_PATENTS_NUMBERS_CHANNEL_ID = config["ECONOMY_PATENTS_NUMBERS_CHANNEL_ID"]


class LogsServer:
    guild_id = config["LogsServer"]["guild_id"]
    invite_url = config["LogsServer"]["invite_url"]
    ban_logs_channel_id = config["LogsServer"]["ban_logs_channel_id"]
    role_logs_channel_id = config["LogsServer"]["role_logs_channel_id"]
    messages_channel_id = config["LogsServer"]["messages_channel_id"]
    rrs_logs_channel_id = config["LogsServer"]["rrs_logs_channel_id"]
    rrs_verification_channel_id = config["LogsServer"]["rrs_verification_channel_id"]
    leave_logs_channel_id = config["LogsServer"]["leave_logs_channel_id"]
    moderators_channel_id = config["LogsServer"]["moderators_channel_id"]
    daily_check_channel_id = config["LogsServer"]["daily_check_channel_id"]
    roles_notifications_role_id = config["LogsServer"]["roles_notifications_role_id"]
    errors_notifications_role_id = config["LogsServer"]["errors_notifications_role_id"]
    moderator_role_id = config["LogsServer"]["moderator_role_id"]
    rrs_verifications_notifications_role_id = config["LogsServer"][
        "rrs_verifications_notifications_role_id"
    ]
    rrs_alerts_role_id = config["LogsServer"]["rrs_alerts_role_id"]
    pride_month_event_id = config["LogsServer"]["pride_month_event_id"]


class Emojis:
    plasmo_sync_logo = config["Emojis"]["plasmo_sync_logo"]
    plasmo_tools = config["Emojis"]["plasmo_tools"]
    enabled = config["Emojis"]["enabled"]
    disabled = config["Emojis"]["disabled"]
    diamond = config["Emojis"]["diamond"]
    loading = config["Emojis"]["loading"]
    loading2 = config["Emojis"]["loading2"]
    online = config["Emojis"]["online"]
    offline = config["Emojis"]["offline"]
    site_offline = config["Emojis"]["site_offline"]
    site_online = config["Emojis"]["site_online"]
    s1mple = config["Emojis"]["s1mple"]
    komaru = config["Emojis"]["komaru"]
    diana = config["Emojis"]["diana"]
    ru_flag = config["Emojis"]["ru_flag"]


class Gifs:
    v_durku = config["Gifs"]["v_durku"]
    amazed = config["Gifs"]["amazed"]
    est_slova = config["Gifs"]["est_slova"]
    dont_ping_me = config["Gifs"]["dont_ping_me"]


word_emojis = {
    "симпл": Emojis.s1mple,
    "ДИАНА": Emojis.diana,
    "помидоры": Emojis.ru_flag,
    "комар": Emojis.komaru,
}


class DevServer:
    """
    Config for development(logging) server (digital drugs)
    """

    guild_id = config["DevServer"]["guild_id"]
    bot_logs_channel_id = config["DevServer"]["bot_logs_channel_id"]
    errors_channel_id = config["DevServer"]["errors_channel_id"]
    transactions_channel_id = config["DevServer"]["transactions_channel_id"]
    penalty_logs_channel_id = config["DevServer"]["penalty_logs_channel_id"]
    support_invite = config["DevServer"]["support_invite"]


class PlasmoRPGuild:
    """
    Config for Plasmo RP guild
    """

    guild_id = config["PlasmoRPGuild"]["guild_id"]
    invite_url = config["PlasmoRPGuild"]["invite_url"]
    admin_role_id = config["PlasmoRPGuild"]["admin_role_id"]
    president_role_id = config["PlasmoRPGuild"]["president_role_id"]
    mko_head_role_id = config["PlasmoRPGuild"]["mko_head_role_id"]
    mko_helper_role_id = config["PlasmoRPGuild"]["mko_helper_role_id"]
    interpol_role_id = config["PlasmoRPGuild"]["interpol_role_id"]
    banker_role_id = config["PlasmoRPGuild"]["banker_role_id"]
    player_role_id = config["PlasmoRPGuild"]["player_role_id"]
    new_player_role_id = config["PlasmoRPGuild"]["new_player_role_id"]
    keeper_role_id = config["PlasmoRPGuild"]["keeper_role_id"]
    ne_komar_role_id = config["PlasmoRPGuild"]["ne_komar_role_id"]
    fusion_role_id = config["PlasmoRPGuild"]["fusion_role_id"]
    helper_role_id = config["PlasmoRPGuild"]["helper_role_id"]
    moderator_role_id = config["PlasmoRPGuild"]["moderator_role_id"]

    monitored_roles = config["PlasmoRPGuild"]["monitored_roles"]

    notifications_channel_id = config["PlasmoRPGuild"]["notifications_channel_id"]
    game_channel_id = config["PlasmoRPGuild"]["game_channel_id"]
    anticheat_logs_channel_id = config["PlasmoRPGuild"]["anticheat_logs_channel_id"]
    server_logs_channel_id = config["PlasmoRPGuild"]["server_logs_channel_id"]
    logs_channel_id = config["PlasmoRPGuild"]["logs_channel_id"]
    moderators_channel_id = config["PlasmoRPGuild"]["moderators_channel_id"]
    messages_channel_id = config["PlasmoRPGuild"]["messages_channel_id"]


disallowed_to_rrs_roles = config["disallowed_to_rrs_roles"]

api_roles = config["api_roles"]


@dataclass
class GCAGuild:
    guild_id: int
    invite_url: str
    admin_role_id: int
    banned_role_id: int
    has_pass_role_id: int
    without_pass_role_id: int
    culture_member_role_id: int
    staff_role_id: int
    defendant_role_id: int
    committee_defendant_role_id: int
    juror_role_id: int
    announcements_channel_id: int
    dev_logs_channel_id: int
    mc_logs_channel_id: int


gca_guild_config = config["GCAGuild"]
gca_guild = GCAGuild(
    guild_id=gca_guild_config["guild_id"],
    invite_url=gca_guild_config["invite_url"],
    admin_role_id=gca_guild_config["admin_role_id"],
    banned_role_id=gca_guild_config["banned_role_id"],
    has_pass_role_id=gca_guild_config["has_pass_role_id"],
    without_pass_role_id=gca_guild_config["without_pass_role_id"],
    culture_member_role_id=gca_guild_config["culture_member_role_id"],
    staff_role_id=gca_guild_config["staff_role_id"],
    defendant_role_id=gca_guild_config["defendant_role_id"],
    committee_defendant_role_id=gca_guild_config["committee_defendant_role_id"],
    juror_role_id=gca_guild_config["juror_role_id"],
    announcements_channel_id=gca_guild_config["announcements_channel_id"],
    dev_logs_channel_id=gca_guild_config["dev_logs_channel_id"],
    mc_logs_channel_id=gca_guild_config["mc_logs_channel_id"],
)


@dataclass
class PlasmoStructureGuild:
    alias: str
    name: str
    discord_id: int
    invite_url: str
    player_role_id: int
    structure_head_role_id: int
    public_chat_channel_id: int
    pt_logs_channel_id: int
    original_avatar_url: str


structure_guilds = []
plasmo_structure_guilds_config = config["PlasmoStructureGuilds"]

for guild_config in plasmo_structure_guilds_config:
    guild = PlasmoStructureGuild(
        alias=guild_config["alias"],
        name=guild_config["name"],
        discord_id=guild_config["discord_id"],
        invite_url=guild_config["invite_url"],
        player_role_id=guild_config["player_role_id"],
        structure_head_role_id=guild_config["structure_head_role_id"],
        public_chat_channel_id=guild_config["public_chat_channel_id"],
        pt_logs_channel_id=guild_config["pt_logs_channel_id"],
        original_avatar_url=guild_config["original_avatar_url"],
    )
    structure_guilds.append(guild)
