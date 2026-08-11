from dataclasses import dataclass, field
from datetime import date

from models.evento import Evento


@dataclass
class Ocorrencia:

    data: date
    evento: Evento
    atribuicoes: list = field(default_factory=list)

    id: int | None = None

    _proximo_id = 1

    def __post_init__(self):

        if self.id is None:
            self.id = Ocorrencia._proximo_id

        if self.id >= Ocorrencia._proximo_id:
            Ocorrencia._proximo_id = self.id + 1

        if not self.atribuicoes:
            self.atribuicoes = [
                {
                    "funcao": funcao,
                    "pessoa": ""
                }
                for funcao in self.evento.funcoes_necessarias
            ]