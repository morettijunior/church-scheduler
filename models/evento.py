from dataclasses import dataclass, field
from datetime import date


@dataclass
class Evento:
    data: date
    nome: str
    funcoes_necessarias: list = field(default_factory=list)

    id: int = field(init=False)

    _proximo_id: int = 1

    def __post_init__(self):
        self.id = Evento._proximo_id
        Evento._proximo_id += 1

        self.nome = self.nome.strip()

        if not self.nome:
            raise ValueError("Nome obrigatório")

        if not self.data:
            raise ValueError("Data obrigatória")