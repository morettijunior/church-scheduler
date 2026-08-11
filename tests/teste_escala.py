from datetime import date

from models.evento import Evento
from models.ocorrencia import Ocorrencia
from models.escala import Escala


evento = Evento(
    nome="CULTO",
    funcoes_necessarias=[
        "ATRIO",
        "PORTA",
        "PORTA",
        "PATIO"
    ]
)


ocorrencia1 = Ocorrencia(
    data=date(2026, 8, 2),
    evento=evento
)

ocorrencia2 = Ocorrencia(
    data=date(2026, 8, 5),
    evento=evento
)


escala = Escala(
    ocorrencias=[
        ocorrencia1,
        ocorrencia2
    ]
)


print(escala)