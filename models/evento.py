from dataclasses import dataclass, field


@dataclass
class Evento:
    nome: str
    funcoes_necessarias: list = field(default_factory=list)

    id: int | None = None

    _proximo_id = 1

    def __post_init__(self):

        self.nome = self.nome.strip()

        if not self.nome:
            raise ValueError("Nome obrigatório")

        if self.id is None:
            self.id = Evento._proximo_id

        if self.id >= Evento._proximo_id:
            Evento._proximo_id = self.id + 1