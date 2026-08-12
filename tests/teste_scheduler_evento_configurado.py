from models.evento import Evento
from scheduler.regra_semanal import RegraSemanal
from scheduler.evento_configurado import EventoConfigurado


print("TESTE 1 - EVENTO CONFIGURADO VÁLIDO")

evento = Evento(
    nome="CULTO",
    funcoes_necessarias=[
        "ATRIO",
        "PORTA",
        "PATIO"
    ]
)

regra = RegraSemanal(
    dias=[2, 5, 6]
)

configurado = EventoConfigurado(
    evento=evento,
    regra=regra
)

print(configurado)


print("\nTESTE 2 - EVENTO AUSENTE")

try:

    EventoConfigurado(
        evento=None,
        regra=regra
    )

except ValueError as erro:

    print("Erro esperado:", erro)


print("\nTESTE 3 - REGRA AUSENTE")

try:

    EventoConfigurado(
        evento=evento,
        regra=None
    )

except ValueError as erro:

    print("Erro esperado:", erro)