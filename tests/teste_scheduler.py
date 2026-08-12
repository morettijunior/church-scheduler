from datetime import date

from models.evento import Evento

from scheduler.configuracao_escala import ConfiguracaoEscala
from scheduler.evento_configurado import EventoConfigurado
from scheduler.regra_semanal import RegraSemanal
from scheduler.regra_mensal import RegraMensal
from scheduler.scheduler import Scheduler


scheduler = Scheduler()


# ============================================================
# TESTE 1 - PERÍODO INCLUI DATA INICIAL E DATA FINAL
# ============================================================

print("TESTE 1 - LIMITES DO PERÍODO")


evento = Evento(
    nome="CULTO",
    funcoes_necessarias=[
        "ATRIO",
        "PATIO"
    ]
)

regra = RegraSemanal(
    dias=[2, 5, 6]
)

evento_configurado = EventoConfigurado(
    evento=evento,
    regra=regra
)

configuracao = ConfiguracaoEscala(
    data_inicio=date(2026, 7, 1),
    data_fim=date(2026, 7, 5),
    eventos=[
        evento_configurado
    ]
)

ocorrencias = scheduler.gerar_ocorrencias(
    configuracao
)

print("Quantidade:", len(ocorrencias))

for ocorrencia in ocorrencias:

    print(
        ocorrencia.data,
        "→",
        ocorrencia.evento.nome
    )


# ============================================================
# TESTE 2 - PERÍODO SEM OCORRÊNCIAS
# ============================================================

print("\nTESTE 2 - PERÍODO SEM OCORRÊNCIAS")


configuracao = ConfiguracaoEscala(
    data_inicio=date(2026, 7, 2),
    data_fim=date(2026, 7, 3),
    eventos=[
        evento_configurado
    ]
)

ocorrencias = scheduler.gerar_ocorrencias(
    configuracao
)

print("Quantidade:", len(ocorrencias))
print("Resultado esperado: lista vazia")


# ============================================================
# TESTE 3 - QUINTA OCORRÊNCIA INEXISTENTE
# ============================================================

print("\nTESTE 3 - QUINTA OCORRÊNCIA INEXISTENTE")


evento_ensaio = Evento(
    nome="ENSAIO",
    funcoes_necessarias=[
        "ATRIO",
        "PATIO"
    ]
)

regra_ensaio = RegraMensal(
    dia_semana=1,
    semana=5
)

evento_configurado_ensaio = EventoConfigurado(
    evento=evento_ensaio,
    regra=regra_ensaio
)

configuracao = ConfiguracaoEscala(
    data_inicio=date(2026, 7, 1),
    data_fim=date(2026, 7, 31),
    eventos=[
        evento_configurado_ensaio
    ]
)

ocorrencias = scheduler.gerar_ocorrencias(
    configuracao
)

print("Quantidade:", len(ocorrencias))
print("Resultado esperado: lista vazia")


# ============================================================
# TESTE 4 - CULTO + RJM + ENSAIO
# ============================================================

print("\nTESTE 4 - MÚLTIPLOS EVENTOS E REGRAS")


evento_rjm = Evento(
    nome="RJM",
    funcoes_necessarias=[
        "ATRIO",
        "PATIO"
    ]
)

regra_rjm = RegraSemanal(
    dias=[6]
)

evento_configurado_rjm = EventoConfigurado(
    evento=evento_rjm,
    regra=regra_rjm
)


regra_ensaio = RegraMensal(
    dia_semana=1,
    semana=1
)

evento_configurado_ensaio = EventoConfigurado(
    evento=evento_ensaio,
    regra=regra_ensaio
)


configuracao = ConfiguracaoEscala(
    data_inicio=date(2026, 7, 1),
    data_fim=date(2026, 7, 31),
    eventos=[
        evento_configurado,
        evento_configurado_rjm,
        evento_configurado_ensaio
    ]
)

ocorrencias = scheduler.gerar_ocorrencias(
    configuracao
)

print("Quantidade:", len(ocorrencias))

for ocorrencia in ocorrencias:

    print(
        ocorrencia.data,
        "→",
        ocorrencia.evento.nome
    )