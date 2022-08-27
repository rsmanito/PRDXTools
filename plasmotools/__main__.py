import asyncio
import logging

from plasmotools import log
from plasmotools import settings
from plasmotools.bot import PlasmoSync
from plasmotools.utils.database import banker
from plasmotools.utils.database import compulsory_service
from plasmotools.utils.database import plasmo_structures

log.setup()

bot = PlasmoSync.create()
logger = logging.getLogger(__name__)

bot.load_extensions("plasmotools/ext")
asyncio.run(plasmo_structures.setup_database())
asyncio.run(compulsory_service.setup_database())
asyncio.run(banker.setup_database())

bot.run(settings.TOKEN)
