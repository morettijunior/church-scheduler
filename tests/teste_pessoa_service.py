from datetime import date

from models.pessoa import Pessoa
from services.pessoa_service import PessoaService


pessoas = [

    Pessoa(
        nome="FELIX",
        telefone="00000000000",
        funcoes=["ATRIO", "PORTA"],
        restricoes=[]
    ),

    Pessoa(
        nome="MARCOS",
        telefone="00000000000",
        funcoes=["PORTA"],
        restricoes=[]
    ),

    Pessoa(
        nome="MAURO",
        telefone="00000000000",
        funcoes=["ATRIO"],
        restricoes=[]
    ),

    Pessoa(
        nome="SILVIO",
        telefone="00000000000",
        funcoes=["PATIO"],
        restricoes=[
            date(2026, 8, 9)
        ]
    ),

    Pessoa(
        nome="SOCRATES",
        telefone="00000000000",
        funcoes=["ATRIO", "PORTA"],
        restricoes=[]
    )
]


# SOCRATES será usado para testar pessoa inativa

pessoas[4].ativo = False


service = PessoaService(pessoas)


print("\n1 - PESSOA NÃO CADASTRADA")

resultado = service.validar_aptidao(
    999,
    "ATRIO",
    date(2026, 8, 9)
)

print(resultado)


print("\n2 - PESSOA INATIVA")

resultado = service.validar_aptidao(
    pessoas[4].id,
    "ATRIO",
    date(2026, 8, 9)
)

print(resultado)


print("\n3 - PESSOA NÃO EXECUTA A FUNÇÃO")

resultado = service.validar_aptidao(
    pessoas[2].id,
    "PORTA",
    date(2026, 8, 9)
)

print(resultado)


print("\n4 - PESSOA COM RESTRIÇÃO NA DATA")

resultado = service.validar_aptidao(
    pessoas[3].id,
    "PATIO",
    date(2026, 8, 9)
)

print(resultado)


print("\n5 - PESSOA APTA")

resultado = service.validar_aptidao(
    pessoas[0].id,
    "ATRIO",
    date(2026, 8, 9)
)

print(resultado)