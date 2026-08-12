from dataclasses import dataclass, field
from datetime import date


@dataclass
class ConfiguracaoEscala:

    data_inicio: date
    data_fim: date
    eventos: list = field(default_factory=list)

    def __post_init__(self):

        if self.data_inicio > self.data_fim:
            raise ValueError(
                "A data inicial não pode ser maior que a data final"
            )

        if not self.eventos:
            raise ValueError(
                "Deve existir pelo menos um evento configurado"
            )