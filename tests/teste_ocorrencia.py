from datetime import date

from models.evento import Evento
from models.ocorrencia import Ocorrencia


evento = Evento(
    nome="CULTO",
    funcoes_necessarias=[
        "ATRIO",
        "PORTA",
        "PORTA",
        "PATIO"
    ]
)


ocorrencia = Ocorrencia(
    data=date(2026, 8, 2),
    evento=evento
)


print(ocorrencia)