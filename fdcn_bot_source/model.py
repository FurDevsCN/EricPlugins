from pydantic import BaseModel, Field

from library.model.bot_list import BotType, Bot


class _BotProgram(BaseModel):
    id: int
    name: str
    repo: list[str]
    description: str
    author: list[str] = []

    def __hash__(self):
        return hash(self.id)

    @property
    def type(self) -> BotType:
        return BotType(name=self.name, repo=self.repo, description=self.description)


class _FDCNStore:
    programs: set[_BotProgram]

    def __init__(self):
        self.programs = set()

    def get_by_id(self, _id: int) -> _BotProgram | None:
        return next(filter(lambda x: x.id == _id, self.programs), None)


_store = _FDCNStore()


class _Bot(BaseModel):
    id: int
    name: str
    num: int
    description: str
    site: str
    maintainer: list[str]
    program_num: list[int] = Field([], alias="program")

    def __hash__(self):
        return hash(self.id)

    @property
    def program(self) -> list[_BotProgram]:
        programs = [_store.get_by_id(_id) for _id in self.program_num]
        return [x for x in programs if x is not None]

    @property
    def bot(self) -> Bot:
        bot_types = [x.type for x in self.program]
        for bot_type in bot_types:
            bot_type.site = self.site
        return Bot(id=self.id, nickname=self.name, maintainers=self.maintainer, type=bot_types[0])
