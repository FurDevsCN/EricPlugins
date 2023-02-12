from creart import it

from library.model.bot_list import BotList
from module.fdcn_bot_source.fetch import FDCNBotSource

it(BotList).register_source(FDCNBotSource())
