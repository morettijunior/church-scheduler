from dataclasses import dataclass
from datetime import date


@dataclass
class RegraSemanal:

    dias: list[int]

    def __post_init__(self):

        if not self.dias:
            raise ValueError(
                "Deve existir pelo menos um dia da semana"
            )

        if any(
            not isinstance(dia, int) or dia < 0 or dia > 6
            for dia in self.dias
        ):
            raise ValueError(
                "Dia da semana inválido"
            )

        if len(self.dias) != len(set(self.dias)):
            raise ValueError(
                "Não pode haver dias da semana duplicados"
            )

    def corresponde(self, data: date) -> bool:

        return data.weekday() in self.dias