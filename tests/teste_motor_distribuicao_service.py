from datetime import date

from models.pessoa import Pessoa
from models.evento import Evento
from models.ocorrencia import Ocorrencia
from services.motor_distribuicao import MotorDistribuicao


def test_distribuir_todas_as_funcoes_f1_ate_f7():

    # =========================================================
    # PESSOAS
    # =========================================================

    pessoas = [
        Pessoa(
            nome="A",
            telefone="99999",
            funcoes=["F1", "F2", "F4", "F6"],
            restricoes=[],
        ),
        Pessoa(
            nome="B",
            telefone="99999",
            funcoes=["F1", "F3", "F5", "F7"],
            restricoes=[],
        ),
        Pessoa(
            nome="C",
            telefone="99999",
            funcoes=[
                "F1",
                "F2",
                "F3",
                "F4",
                "F5",
                "F6",
                "F7",
            ],
            restricoes=[],
        ),
        Pessoa(
            nome="D",
            telefone="99999",
            funcoes=["F1", "F4", "F6"],
            restricoes=[],
        ),
        Pessoa(
            nome="E",
            telefone="99999",
            funcoes=["F1", "F2", "F3", "F5", "F7"],
            restricoes=[],
        ),
        Pessoa(
            nome="F",
            telefone="99999",
            funcoes=["F1", "F2", "F4", "F5", "F6"],
            restricoes=[],
        ),
        Pessoa(
            nome="G",
            telefone="99999",
            funcoes=["F2", "F3", "F5", "F6", "F7"],
            restricoes=[],
        ),
        Pessoa(
            nome="H",
            telefone="99999",
            funcoes=["F2", "F3", "F4", "F6", "F7"],
            restricoes=[],
        ),
        Pessoa(
            nome="I",
            telefone="99999",
            funcoes=["F3", "F4", "F5", "F7"],
            restricoes=[
                date(2026, 10, 14),
            ],
        ),
        Pessoa(
            nome="J",
            telefone="99999",
            funcoes=["F4", "F5", "F6", "F7"],
            restricoes=[],
        ),
    ]

    # =========================================================
    # EVENTO
    # =========================================================

    evento = Evento(
        nome="EVENTO",
        funcoes_necessarias=[
            "F1",
            "F2",
            "F3",
            "F4",
            "F5",
            "F6",
            "F7",
        ],
    )

    # =========================================================
    # DATAS
    # =========================================================

    datas = [
        date(2026, 10, 10),
        date(2026, 10, 11),
        date(2026, 10, 12),
        date(2026, 10, 13),
        date(2026, 10, 14),
        date(2026, 10, 15),
        date(2026, 10, 16),
        date(2026, 10, 17),
    ]

    ocorrencias = [
        Ocorrencia(
            data=data,
            evento=evento,
        )
        for data in datas
    ]

    # =========================================================
    # MOTOR
    # =========================================================

    motor = MotorDistribuicao()

    # =========================================================
    # ÚNICA CHAMADA AO MOTOR
    # =========================================================

    pessoas_f1 = motor.encontrar_pessoas_da_funcao(
        pessoas,
        "F1",
    )

    pessoa_inicial_f1 = pessoas_f1[0]

    motor.distribuir_todas_as_funcoes(
        pessoas=pessoas,
        ocorrencias=ocorrencias,
        funcoes_necessarias=evento.funcoes_necessarias,
        pessoa_inicial_f1=pessoa_inicial_f1,
        deslocamento=3,
    )

    # =========================================================
    # RESULTADOS
    # =========================================================

    resultados = [
        [
            ocorrencia.atribuicoes[indice]["pessoa"]
            for indice in range(7)
        ]
        for ocorrencia in ocorrencias
    ]

    # =========================================================
    # 1. TODAS AS 7 FUNÇÕES FORAM PREENCHIDAS
    # =========================================================

    for resultado in resultados:
        assert len(resultado) == 7
        assert all(resultado)

    # =========================================================
    # 2. NÃO PODE HAVER DUPLICIDADE NO MESMO DIA
    # =========================================================

    for resultado in resultados:
        assert len(resultado) == len(set(resultado))

    # =========================================================
    # 3. CADA PESSOA POSSUI A FUNÇÃO ATRIBUÍDA
    # =========================================================

    for ocorrencia in ocorrencias:

        for indice_funcao, funcao in enumerate(
            evento.funcoes_necessarias
        ):

            nome = ocorrencia.atribuicoes[
                indice_funcao
            ]["pessoa"]

            pessoa = next(
                pessoa
                for pessoa in pessoas
                if pessoa.nome == nome
            )

            assert funcao in pessoa.funcoes

    # =========================================================
    # 4. NINGUÉM É ATRIBUÍDO EM DIA DE RESTRIÇÃO
    # =========================================================

    for ocorrencia in ocorrencias:

        for atribuicao in ocorrencia.atribuicoes:

            nome = atribuicao["pessoa"]

            pessoa = next(
                pessoa
                for pessoa in pessoas
                if pessoa.nome == nome
            )

            assert (
                ocorrencia.data
                not in pessoa.restricoes
            )

    # =========================================================
    # 5. F1 DEVE COMEÇAR PELA PRIMEIRA PESSOA
    # =========================================================

    resultado_f1 = [
        ocorrencia.atribuicoes[0]["pessoa"]
        for ocorrencia in ocorrencias
    ]

    assert resultado_f1 == [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "A",
        "B",
    ]

    # =========================================================
    # 6. F2 ATÉ F7 DEVEM TER PRIMEIRAS PESSOAS
    # =========================================================

    primeiras_pessoas = [
        ocorrencia.atribuicoes[indice]["pessoa"]
        for indice in range(7)
        for ocorrencia in ocorrencias[:1]
    ]

    # Nenhuma função pode usar a mesma pessoa da função
    # imediatamente anterior no primeiro dia.

    for indice in range(1, 7):
        assert (
            primeiras_pessoas[indice]
            != primeiras_pessoas[indice - 1]
        )

    # =========================================================
    # 7. VERIFICAÇÃO DA CADEIA DE REFERÊNCIA
    # =========================================================

    # A primeira pessoa de cada função deve ser diferente
    # da primeira pessoa de todas as funções anteriores.

    for ocorrencia in ocorrencias:

        pessoas_do_dia = [
            ocorrencia.atribuicoes[indice]["pessoa"]
            for indice in range(7)
        ]

        assert len(pessoas_do_dia) == 7
        assert len(set(pessoas_do_dia)) == 7
