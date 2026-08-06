from dataclasses import dataclass, field


@dataclass
class Escala:
    eventos: list = field(default_factory=list)

    id: int | None = None

    _proximo_id = 1

    def __post_init__(self):

        if self.id is None:
            self.id = Escala._proximo_id

        if self.id >= Escala._proximo_id:
            Escala._proximo_id = self.id + 1