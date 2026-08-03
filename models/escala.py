from dataclasses import dataclass, field

from models.evento import Evento


@dataclass
class Escala:
    evento: Evento

    id: int = field(init=False)

    _proximo_id: int = 1

    def __post_init__(self):
        self.id = Escala._proximo_id
        Escala._proximo_id += 1