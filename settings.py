import os
from builtins import bool
from dataclasses import dataclass
from types import NoneType
from typing import Union

from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")
plasmo_token = os.getenv("PLASMO_TOKEN")


class DevServer:
    """
    Config for development(logging) server (digital drugs)
    """
    guild_id: int = 828683007635488809
    bot_logs_channel_id: int = 935571295276503100
    ban_logs_channel_id: int = 935571311936278599
    role_logs_channel_id: int = 935571326335320135
    nicknames_channel_id: int = 935571360393068614


class PlasmoRPGuild:
    """
    Config for Plasmo RP guild
    """
    guild_id: int = 672312131760291842  # Discord server id
    invite_url: str = "https://discord.gg/VJtCjwh"  # Discord invite
    admin_role_id: int = 704364763248984145  # Administration role id
    mko_head_role_id: int = 810492714235723777
    mko_helper_role_id: int = 826366703591620618
    interpol_role_id: int = 751723033357451335
    banker_role_id: int = 826367015014498314


@dataclass
class PlasmoStructureGuild:
    """
    Represents an official child plasmo guild, like interpol or economics
    """

    guild_id: int
    name: str
    player_role_id: int
    support_role_id: int
    member_role_id: int
    fusion_role_id: int
    interpol_role_id: int
    structure_head_helper_role_id: int
    structure_head_role_id: int
    dev_role_id: int
    admin_role_id: int
    public_information_channel_id: int
    news_channel_id: int
    public_announcements_channel_id: int
    public_announcements_webhook_url: str

    chat_channel_id: int
    members_announcements_channel_id: int
    members_announcements_webhook_url: str
    members_chat_channel_id: int
    members_voice_channel_id: int
    dev_logs_channel_id: int
    server_logs_channel_id: int
    plasmo_logs_channel_id: int
    admin_chat_channel_id: int
    guest_chat_channel_id: Union[int, None] = None
    members_information_channel_id: Union[int, None] = None
    mko_head_role_id: Union[int, None] = None
    mko_helper_role_id: Union[int, None] = None
    mko_president_role_id: Union[int, None] = None
    banker_role_id: Union[int, None] = None

    invite_url: Union[str, None] = None
    structure_roles_dict: Union[dict[str, int], None] = None

    is_payouts_enabled: bool = False
    payouts_card: str = "0001"
    bearer_plasmo_token: str = "Bearer None"


# INTERPOL
old_interpol_announcements_webhook_url = os.getenv("INTERPOL_ANNOUNCEMENTS_WEBHOOK_URL")
old_interpol_vacation_webhook_url = os.getenv("INTERPOL_VACATION_WEBHOOK_URL")
old_interpol_court_announcements_webhook_url = os.getenv(
    "INTERPOL_COURT_ANNOUNCEMENTS_WEBHOOK_URL"
)

old_interpol = {
    "card": 2777,  # Card
    "interpol": 841024765183262750,  # Интерпол роль
    "arbiter": 928729647271796746,  # Судья роль
    "secretary": 928729800980459530,  # Секретарь роль
    "deputy": 928733147552690226,  # Заместитель роль
    "lowactive": 928978122852925490,  # Малоактивный роль
    "player": 841098135376101377,  # Игрок роль
    "vacation": 929132315890831410,  # Отпуск роль
    "interpol_head": 929146239918952459,  # Глава Интерпола роль
    "CP_test_passed": 932723009247125615,  # Аттестация по корпротекту пройдена
    "logs": 928768552733933639,  # Канал с логами
    "payouts": 933059866380087326,
    "payout_logs": 933059899972268063,
    "event_reaction": "🎪",
    "fake_call_reaction": "🤡",
    "payed_reaction": "✅",
    "event_keywords": ["ивент", "мко", "суд", "набор", "шоу"],
}

old_infrastructure = {
    "id": 756750263351771146,  # Guild
    "card": 2777,  # Card
    "deputy": 895736618156167188,  # Зам роль
    "player": 810985435903557685,  # Игрок роль
    "keeper": 918075165919817778,
    "logs": 941750297619988521,  # Канал с логами
    "payouts": 870664569419354192,
    "payout_logs": 941750297619988521,
}

old_infrastructure_announcements_webhook_url = (
    "https://discord.com/api/webhooks/941475496728870972/"
    "Ck6a8nSda7Nzjiv-RHg1UxRANHoLjNU7eBnPVlkNVKjchcuBvTX1AttlxoGe2s6LuPB4"
)

old_texts = {
    "interpol": "Интерпол",
    "arbiter": "Судья",
    "secretary": "Секретарь",
    "deputy": "Заместитель",
    "lowactive": "Малоактивный",
}

# BAC
bac = {
    "id": 855532780187156501,
    "banned": 860799809123778560,
    "pass": 860799590721388574,
    "no_pass": 928688505033474069,
    "invite": "https://discord.gg/KNaZPxxMHC",
}

# DD

# Logs:
# Bans + Unbans
# Roles like interpol, banker, helper, admin etc
#
digital_drugs = {
    "id": 828683007635488809,
    "errors": 935571295276503100,
    "bans": 935571311936278599,
    "roles": 935571326335320135,
    "nicknames": 935571360393068614,
}


test_guild = PlasmoStructureGuild(
    guild_id=841024625102422016,
    name="%STRUCTURENAME%",

    player_role_id=956985954395111494,
    support_role_id=956985476013756508,
    member_role_id=943982915413508186,
    interpol_role_id=956985149785002065,
    fusion_role_id=841056624915513385,
    structure_head_helper_role_id=956972234952552468,
    structure_head_role_id=956972855420153867,
    dev_role_id=956972132573786133,
    admin_role_id=956972026487242842,
    public_information_channel_id=951204944571170896,
    news_channel_id=956971841229037678,
    public_announcements_channel_id=956984850433339442,
    public_announcements_webhook_url=os.getenv(
        "TEST_GUILD_PUBLIC_ANNOUNCEMENTS_WEBHOOK_URL"
    ),
    chat_channel_id=956992137122185276,
    members_announcements_channel_id=956992719438364742,
    members_announcements_webhook_url=os.getenv(
        "TEST_GUILD_MEMBERS_ANNOUNCEMENTS_WEBHOOK_URL"
    ),
    members_chat_channel_id=956993138646450206,
    members_voice_channel_id=956993257248792596,
    dev_logs_channel_id=956986667800076368,
    server_logs_channel_id=956990641647284256,
    plasmo_logs_channel_id=956990708164747264,
    admin_chat_channel_id=956990679274356747,
    guest_chat_channel_id=956994964586377296,
    members_information_channel_id=956992880747102228,
    mko_head_role_id=957243719638204476,
    mko_helper_role_id=957243840954265670,
    mko_president_role_id=957243616865165392,
    invite_url="https://discord.gg/4p9j2zKMJT",
    is_payouts_enabled=True,
    payouts_card="3666",
    bearer_plasmo_token="Bearer " + os.getenv("TEST_GUILD_BEARER_PLASMO_TOKEN"),
    structure_roles_dict={
        "Верховный судья": 0,
        "Судья": 0,
        "Судья(Предварительно)": 0,
        "Секретарь": 0,
        "Секретарь(Предварительно)": 0,
        "Главный Прокурор": 0,
        "Прокурор": 0,
        "Прокурор(Предварительно)": 0,
        "Главный Адвокат": 0,
        "Адвокат": 0,
        "Адвокат(Предварительно)": 0,

    },
)

interpol_guild = PlasmoStructureGuild(
    guild_id=828683007635488809,
    name="Интерпол",
    player_role_id=878987593482657833,
    support_role_id=957049290574930050,
    member_role_id=841024765183262750,
    interpol_role_id=841024765183262750,
    fusion_role_id=957049392634925077,
    structure_head_helper_role_id=940132122889441291,
    structure_head_role_id=813451633085120563,
    dev_role_id=928716499168927834,
    admin_role_id=945324756297711666,
    public_information_channel_id=813782278857162765,
    news_channel_id=867045987130146847,
    public_announcements_channel_id=947352237049524234,
    public_announcements_webhook_url=os.getenv(
        "INTERPOL_PUBLIC_ANNOUNCEMENTS_WEBHOOK_URL"
    ),
    chat_channel_id=813451608871796770,
    members_announcements_channel_id=813783361113423893,
    members_announcements_webhook_url=os.getenv(
        "INTERPOL_MEMBERS_ANNOUNCEMENTS_WEBHOOK_URL"
    ),
    members_chat_channel_id=813783407581593621,
    members_voice_channel_id=944785443868786728,
    dev_logs_channel_id=957050026100666428,
    server_logs_channel_id=941948414646710273,
    plasmo_logs_channel_id=957050137228742696,
    admin_chat_channel_id=957050197698019408,
    guest_chat_channel_id=866714779090419772,
    members_information_channel_id=919906651111309374,
    mko_head_role_id=957052462664122369,
    mko_helper_role_id=957052685327142943,
    mko_president_role_id=881196023760949300,
    invite_url="https://discord.gg/n9YMfZB2kJ",
    is_payouts_enabled=False,
    payouts_card="0001",
    bearer_plasmo_token="Bearer " + os.getenv("INTERPOL_BEARER_PLASMO_TOKEN"),
    structure_roles_dict={
        "Интерпол": 0,
        "Ученик": 0,
    },
)
economics_guild = PlasmoStructureGuild(
    guild_id=828683007635488809,
    name="Экономика",
    player_role_id=878987593482657833,
    support_role_id=957049290574930050,
    member_role_id=841024765183262750,
    interpol_role_id=841024765183262750,
    fusion_role_id=957049392634925077,
    structure_head_helper_role_id=940132122889441291,
    structure_head_role_id=813451633085120563,
    dev_role_id=928716499168927834,
    admin_role_id=945324756297711666,
    public_information_channel_id=813782278857162765,
    news_channel_id=867045987130146847,
    public_announcements_channel_id=947352237049524234,
    public_announcements_webhook_url=os.getenv(
        "economics_PUBLIC_ANNOUNCEMENTS_WEBHOOK_URL"
    ),
    chat_channel_id=813451608871796770,
    members_announcements_channel_id=813783361113423893,
    members_announcements_webhook_url=os.getenv(
        "economics_MEMBERS_ANNOUNCEMENTS_WEBHOOK_URL"
    ),
    members_chat_channel_id=813783407581593621,
    members_voice_channel_id=944785443868786728,
    dev_logs_channel_id=957050026100666428,
    server_logs_channel_id=941948414646710273,
    plasmo_logs_channel_id=957050137228742696,
    admin_chat_channel_id=957050197698019408,
    guest_chat_channel_id=866714779090419772,
    members_information_channel_id=919906651111309374,
    mko_head_role_id=957052462664122369,
    mko_helper_role_id=957052685327142943,
    mko_president_role_id=881196023760949300,
    invite_url="https://discord.gg/n9YMfZB2kJ",
    is_payouts_enabled=False,
    payouts_card="0001",
    bearer_plasmo_token="Bearer " + os.getenv("economics_BEARER_PLASMO_TOKEN"),
)
infrastructure_guild = PlasmoStructureGuild(
    guild_id=828683007635488809,
    name="Инфраструктура",
    player_role_id=878987593482657833,
    support_role_id=957049290574930050,
    member_role_id=841024765183262750,
    interpol_role_id=841024765183262750,
    fusion_role_id=957049392634925077,
    structure_head_helper_role_id=940132122889441291,
    structure_head_role_id=813451633085120563,
    dev_role_id=928716499168927834,
    admin_role_id=945324756297711666,
    public_information_channel_id=813782278857162765,
    news_channel_id=867045987130146847,
    public_announcements_channel_id=947352237049524234,
    public_announcements_webhook_url=os.getenv(
        "infrastructure_PUBLIC_ANNOUNCEMENTS_WEBHOOK_URL"
    ),
    chat_channel_id=813451608871796770,
    members_announcements_channel_id=813783361113423893,
    members_announcements_webhook_url=os.getenv(
        "infrastructure_MEMBERS_ANNOUNCEMENTS_WEBHOOK_URL"
    ),
    members_chat_channel_id=813783407581593621,
    members_voice_channel_id=944785443868786728,
    dev_logs_channel_id=957050026100666428,
    server_logs_channel_id=941948414646710273,
    plasmo_logs_channel_id=957050137228742696,
    admin_chat_channel_id=957050197698019408,
    guest_chat_channel_id=866714779090419772,
    members_information_channel_id=919906651111309374,
    mko_head_role_id=957052462664122369,
    mko_helper_role_id=957052685327142943,
    mko_president_role_id=881196023760949300,
    invite_url="https://discord.gg/n9YMfZB2kJ",
    is_payouts_enabled=False,
    payouts_card="0001",
    bearer_plasmo_token="Bearer " + os.getenv("infrastructure_BEARER_PLASMO_TOKEN"),
)
mko_guild = PlasmoStructureGuild(
    guild_id=828683007635488809,
    name="МКО",
    player_role_id=878987593482657833,
    support_role_id=957049290574930050,
    member_role_id=841024765183262750,
    interpol_role_id=841024765183262750,
    fusion_role_id=957049392634925077,
    structure_head_helper_role_id=940132122889441291,
    structure_head_role_id=813451633085120563,
    dev_role_id=928716499168927834,
    admin_role_id=945324756297711666,
    public_information_channel_id=813782278857162765,
    news_channel_id=867045987130146847,
    public_announcements_channel_id=947352237049524234,
    public_announcements_webhook_url=os.getenv("mko_PUBLIC_ANNOUNCEMENTS_WEBHOOK_URL"),
    chat_channel_id=813451608871796770,
    members_announcements_channel_id=813783361113423893,
    members_announcements_webhook_url=os.getenv(
        "mko_MEMBERS_ANNOUNCEMENTS_WEBHOOK_URL"
    ),
    members_chat_channel_id=813783407581593621,
    members_voice_channel_id=944785443868786728,
    dev_logs_channel_id=957050026100666428,
    server_logs_channel_id=941948414646710273,
    plasmo_logs_channel_id=957050137228742696,
    admin_chat_channel_id=957050197698019408,
    guest_chat_channel_id=866714779090419772,
    members_information_channel_id=919906651111309374,
    mko_head_role_id=957052462664122369,
    mko_helper_role_id=957052685327142943,
    mko_president_role_id=881196023760949300,
    invite_url="https://discord.gg/n9YMfZB2kJ",
    is_payouts_enabled=False,
    payouts_card="0001",
    bearer_plasmo_token="Bearer " + os.getenv("INTERPOL_BEARER_PLASMO_TOKEN"),
)
culrure_guild = PlasmoStructureGuild(
    guild_id=828683007635488809,
    name="Культура",
    player_role_id=878987593482657833,
    support_role_id=957049290574930050,
    member_role_id=841024765183262750,
    interpol_role_id=841024765183262750,
    fusion_role_id=957049392634925077,
    structure_head_helper_role_id=940132122889441291,
    structure_head_role_id=813451633085120563,
    dev_role_id=928716499168927834,
    admin_role_id=945324756297711666,
    public_information_channel_id=813782278857162765,
    news_channel_id=867045987130146847,
    public_announcements_channel_id=947352237049524234,
    public_announcements_webhook_url=os.getenv(
        "culrure_PUBLIC_ANNOUNCEMENTS_WEBHOOK_URL"
    ),
    chat_channel_id=813451608871796770,
    members_announcements_channel_id=813783361113423893,
    members_announcements_webhook_url=os.getenv(
        "culrure_MEMBERS_ANNOUNCEMENTS_WEBHOOK_URL"
    ),
    members_chat_channel_id=813783407581593621,
    members_voice_channel_id=944785443868786728,
    dev_logs_channel_id=957050026100666428,
    server_logs_channel_id=941948414646710273,
    plasmo_logs_channel_id=957050137228742696,
    admin_chat_channel_id=957050197698019408,
    guest_chat_channel_id=866714779090419772,
    members_information_channel_id=919906651111309374,
    mko_head_role_id=957052462664122369,
    mko_helper_role_id=957052685327142943,
    mko_president_role_id=881196023760949300,
    invite_url="https://discord.gg/n9YMfZB2kJ",
    is_payouts_enabled=False,
    payouts_card="0001",
    bearer_plasmo_token="Bearer " + os.getenv("INTERPOL_BEARER_PLASMO_TOKEN"),
)

court_guild = PlasmoStructureGuild(
    guild_id=828683007635488809,
    name="Суды",
    player_role_id=878987593482657833,
    support_role_id=957049290574930050,
    member_role_id=841024765183262750,
    interpol_role_id=841024765183262750,
    fusion_role_id=957049392634925077,
    structure_head_helper_role_id=940132122889441291,
    structure_head_role_id=813451633085120563,
    dev_role_id=928716499168927834,
    admin_role_id=945324756297711666,
    public_information_channel_id=813782278857162765,
    news_channel_id=867045987130146847,
    public_announcements_channel_id=947352237049524234,
    public_announcements_webhook_url=os.getenv(
        "court_PUBLIC_ANNOUNCEMENTS_WEBHOOK_URL"
    ),
    chat_channel_id=813451608871796770,
    members_announcements_channel_id=813783361113423893,
    members_announcements_webhook_url=os.getenv(
        "court_MEMBERS_ANNOUNCEMENTS_WEBHOOK_URL"
    ),
    members_chat_channel_id=813783407581593621,
    members_voice_channel_id=944785443868786728,
    dev_logs_channel_id=957050026100666428,
    server_logs_channel_id=941948414646710273,
    plasmo_logs_channel_id=957050137228742696,
    admin_chat_channel_id=957050197698019408,
    guest_chat_channel_id=866714779090419772,
    members_information_channel_id=919906651111309374,
    mko_head_role_id=957052462664122369,
    mko_helper_role_id=957052685327142943,
    mko_president_role_id=881196023760949300,
    invite_url="https://discord.gg/NUz2Cpq68Z",
    is_payouts_enabled=False,
    payouts_card="0001",
    bearer_plasmo_token="Bearer " + os.getenv("court_BEARER_PLASMO_TOKEN"),
)

plasmo_child_guilds = [
    test_guild,
    interpol_guild,
    infrastructure_guild,
    court_guild,
    mko_guild,
    culrure_guild,
]
