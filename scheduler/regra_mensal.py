from dataclasses import dataclass
from datetime import date


@dataclass
class RegraMensal:

    dia_semana: int
    semana: int

    def __post_init__(self):

        if (
            not isinstance(self.dia_semana, int)
            or self.dia_semana < 0
            or self.dia_semana > 6
        ):
            raise ValueError(
                "Dia da semana inválido"
            )

        if (
            not isinstance(self.semana, int)
            or self.semana < 1
            or self.semana > 5
        ):
            raise ValueError(
                "Semana do mês inválida"
            )

    def corresponde(self, data: date) -> bool:

        if data.weekday() != self.dia_semana:
            return False

        semana = (data.day - 1) // 7 + 1

        return semana == self.semana