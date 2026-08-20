from dataclasses import dataclass, field

from models.ocorrencia import Ocorrencia


@dataclass
class Escala:

    nome: str
    ocorrencias: list[Ocorrencia] = field(default_factory=list)

    id: int | None = None

    _proximo_id = 1

    def __post_init__(self):

        self.nome = self.nome.strip()

        if not self.nome:
            raise ValueError("Nome obrigatório")

        if self.id is None:
            self.id = Escala._proximo_id

        if self.id >= Escala._proximo_id:
            Escala._proximo_id = self.id + 1