from dataclasses import dataclass


@dataclass
class EventoConfigurado:

    evento: object
    regra: object

    def __post_init__(self):

        if self.evento is None:
            raise ValueError(
                "Evento é obrigatório"
            )

        if self.regra is None:
            raise ValueError(
                "Regra é obrigatória"
            )