import json

from creart import it
from kayaku import create

from library.model.bot_list import BotSource, Bot, BotList
from library.model.config import EricConfig
from library.util.session_container import SessionContainer
from module.fdcn_bot_source.model import _BotProgram, _store, _Bot

_cfg: EricConfig = create(EricConfig)


class FDCNBotSource(BotSource):
    name: str = "FurDevsCN"
    url: str = "https://raw.github.com/FurDevsCN/furry-bot-list/main/JSON/bot.json"
    program_url: str = (
        "https://raw.github.com/FurDevsCN/furry-bot-list/main/JSON/botProgram.json"
    )

    async def fetch(self) -> set[Bot]:
        await self.fetch_programs()
        session = await it(SessionContainer).get()
        async with session.get(self.url, proxy=_cfg.proxy) as resp:
            data = json.loads(await resp.text())
            return {_Bot(**x).bot for x in data}

    async def fetch_programs(self) -> set[_BotProgram]:
        session = await it(SessionContainer).get()
        async with session.get(self.program_url, proxy=_cfg.proxy) as resp:
            data = json.loads(await resp.text())
            programs = {_BotProgram(**x) for x in data}
            _store.programs = programs
            return programs
