from dataclasses import dataclass, field
from datetime import date


@dataclass
class ConfiguracaoEscala:

    nome: str
    data_inicio: date
    data_fim: date
    eventos: list = field(default_factory=list)
    atrio_fixo: bool = False

    def __post_init__(self):

        self.nome = self.nome.strip()

        if not self.nome:
            raise ValueError(
                "Nome da escala é obrigatório"
            )

        if self.data_inicio > self.data_fim:
            raise ValueError(
                "A data inicial não pode ser maior que a data final"
            )

        if not self.eventos:
            raise ValueError(
                "Deve existir pelo menos um evento configurado"
            )