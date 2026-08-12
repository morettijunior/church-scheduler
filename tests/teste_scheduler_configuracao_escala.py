from datetime import date

from scheduler.configuracao_escala import ConfiguracaoEscala


print("\nTESTE 3 - NENHUM EVENTO")

try:

    ConfiguracaoEscala(
        data_inicio=date(2026, 7, 1),
        data_fim=date(2027, 1, 31),
        eventos=[]
    )

except ValueError as erro:

    print("Erro esperado:", erro)