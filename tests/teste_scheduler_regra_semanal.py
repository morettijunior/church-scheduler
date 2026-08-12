from datetime import date
from scheduler.regra_semanal import RegraSemanal


print("TESTE 1 - REGRA VÁLIDA")

regra = RegraSemanal(
    dias=[2, 5, 6]
)

print(regra)


print("\nTESTE 2 - NENHUM DIA")

try:

    RegraSemanal(
        dias=[]
    )

except ValueError as erro:

    print("Erro esperado:", erro)


print("\nTESTE 3 - DIA INVÁLIDO")

try:

    RegraSemanal(
        dias=[2, 7]
    )

except ValueError as erro:

    print("Erro esperado:", erro)


print("\nTESTE 4 - DIA DUPLICADO")

try:

    RegraSemanal(
        dias=[2, 2, 6]
    )

except ValueError as erro:

    print("Erro esperado:", erro)

print("\nTESTE 5 - DATA CORRESPONDE")

regra = RegraSemanal(
    dias=[2, 5, 6]
)

resultado = regra.corresponde(
    date(2026, 7, 1)
)

print("Resultado:", resultado)


print("\nTESTE 6 - DATA NÃO CORRESPONDE")

resultado = regra.corresponde(
    date(2026, 7, 2)
)

print("Resultado:", resultado)