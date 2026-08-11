from datetime import date

from models.pessoa import Pessoa
from models.evento import Evento
from models.ocorrencia import Ocorrencia
from services.pessoa_service import PessoaService
from services.escala_service import EscalaService


# ============================================================
# PESSOAS
# ============================================================

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


pessoa_service = PessoaService(pessoas)


# ============================================================
# EVENTO
# ============================================================

evento_culto = Evento(
    nome="CULTO",
    funcoes_necessarias=[
        "ATRIO",
        "PORTA",
        "PORTA",
        "PATIO"
    ]
)


# ============================================================
# OCORRÊNCIA
# ============================================================

ocorrencia = Ocorrencia(
    data=date(2026, 8, 9),
    evento=evento_culto
)


# ============================================================
# ESCALA
# ============================================================

escalas = []

escala_service = EscalaService(escalas)

escala = escala_service.criar(
    [ocorrencia]
)


print("\nESCALA CRIADA")

print(escala)


# ============================================================
# 1 - PESSOA APTA
# ============================================================

print("\n1 - PESSOA APTA")

resultado = escala_service.alterar_atribuicao(
    escala=escala,
    id_ocorrencia=ocorrencia.id,
    posicao=1,
    id_pessoa=pessoas[0].id,
    pessoa_service=pessoa_service
)

print(resultado)
print(ocorrencia.atribuicoes)


# ============================================================
# 2 - PESSOA NÃO CADASTRADA
# ============================================================

print("\n2 - PESSOA NÃO CADASTRADA")

resultado = escala_service.alterar_atribuicao(
    escala=escala,
    id_ocorrencia=ocorrencia.id,
    posicao=2,
    id_pessoa=999,
    pessoa_service=pessoa_service
)

print(resultado)
print(ocorrencia.atribuicoes)


# ============================================================
# 3 - PESSOA INATIVA
# ============================================================

print("\n3 - PESSOA INATIVA")

resultado = escala_service.alterar_atribuicao(
    escala=escala,
    id_ocorrencia=ocorrencia.id,
    posicao=2,
    id_pessoa=pessoas[4].id,
    pessoa_service=pessoa_service
)

print(resultado)
print(ocorrencia.atribuicoes)


# ============================================================
# 4 - PESSOA NÃO EXECUTA A FUNÇÃO
# ============================================================

print("\n4 - PESSOA NÃO EXECUTA A FUNÇÃO")

resultado = escala_service.alterar_atribuicao(
    escala=escala,
    id_ocorrencia=ocorrencia.id,
    posicao=4,
    id_pessoa=pessoas[2].id,
    pessoa_service=pessoa_service
)

print(resultado)
print(ocorrencia.atribuicoes)


# ============================================================
# 5 - PESSOA COM RESTRIÇÃO NA DATA
# ============================================================

print("\n5 - PESSOA COM RESTRIÇÃO NA DATA")

resultado = escala_service.alterar_atribuicao(
    escala=escala,
    id_ocorrencia=ocorrencia.id,
    posicao=4,
    id_pessoa=pessoas[3].id,
    pessoa_service=pessoa_service
)

print(resultado)
print(ocorrencia.atribuicoes)


# ============================================================
# 6 - PESSOA JÁ ESCALADA NA MESMA OCORRÊNCIA
# ============================================================

print("\n6 - PESSOA JÁ ESCALADA NA MESMA OCORRÊNCIA")

resultado = escala_service.alterar_atribuicao(
    escala=escala,
    id_ocorrencia=ocorrencia.id,
    posicao=2,
    id_pessoa=pessoas[0].id,
    pessoa_service=pessoa_service
)

print(resultado)
print(ocorrencia.atribuicoes)


# ============================================================
# 7 - ALTERAÇÃO DE OUTRA POSIÇÃO
# ============================================================

print("\n7 - ALTERAÇÃO DE OUTRA POSIÇÃO")

resultado = escala_service.alterar_atribuicao(
    escala=escala,
    id_ocorrencia=ocorrencia.id,
    posicao=2,
    id_pessoa=pessoas[1].id,
    pessoa_service=pessoa_service
)

print(resultado)
print(ocorrencia.atribuicoes)


# ============================================================
# RESULTADO FINAL
# ============================================================

print("\nESCALA FINAL")

print(escala)