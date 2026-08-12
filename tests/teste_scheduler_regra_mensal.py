from datetime import date

from scheduler.regra_mensal import RegraMensal

print("\nTESTE 5 - PRIMEIRA TERÇA-FEIRA")

regra = RegraMensal(
    dia_semana=1,
    semana=1
)

resultado = regra.corresponde(
    date(2026, 7, 7)
)

print("Resultado:", resultado)


print("\nTESTE 6 - SEGUNDA TERÇA-FEIRA")

resultado = regra.corresponde(
    date(2026, 7, 14)
)

print("Resultado:", resultado)


print("\nTESTE 7 - DIA DA SEMANA DIFERENTE")

resultado = regra.corresponde(
    date(2026, 7, 8)
)

print("Resultado:", resultado)


print("\nTESTE 8 - QUINTA OCORRÊNCIA")

regra = RegraMensal(
    dia_semana=1,
    semana=5
)

resultado = regra.corresponde(
    date(2026, 7, 28)
)

print("Resultado:", resultado)