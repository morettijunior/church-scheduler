from datetime import date

from models.configuracao_escala import ConfiguracaoEscala
from scheduler.evento_configurado import EventoConfigurado


def iniciar(
    escala_service,
    pessoa_service,
    evento_service,
    gerador_escala_service,
    motor_distribuicao
):
    while True:
        print()
        print("=== ESCALAS ===")
        print()
        print("1 - Listar escalas")
        print("2 - Visualizar escala")
        print("3 - Gerar nova escala")
        print("0 - Voltar")
        print()

        opcao = input("Escolha uma opção: ")

        if opcao == "0":
            return False

        elif opcao == "1":
            listar(
                escala_service
            )

        elif opcao == "2":
            visualizar(
                escala_service
            )

        elif opcao == "3":
            gerar_nova_escala(
                escala_service,
                pessoa_service,
                evento_service,
                gerador_escala_service,
                motor_distribuicao
            )

        else:
            print("Opção inválida.")


def listar(escala_service):
    escalas = escala_service.listar_todas()

    print()
    print("=== ESCALAS ===")
    print()

    if not escalas:
        print("Nenhuma escala cadastrada.")
        return

    print(
        f"{'ID':<5}"
        f"{'NOME':<25}"
        f"{'PERÍODO'}"
    )

    for escala in escalas:
        periodo = obter_periodo(
            escala
        )

        print(
            f"{escala.id:<5}"
            f"{escala.nome:<25}"
            f"{periodo}"
        )


def visualizar(escala_service):
    print()
    print("=== VISUALIZAR ESCALA ===")
    print()

    try:
        id_escala = int(
            input("ID da escala: ")
        )
    except ValueError:
        print()
        print("ID inválido.")
        return

    escala = escala_service.buscar_por_id(
        id_escala
    )

    if escala is None:
        print()
        print("Digite um ID válido.")
        return

    print()
    print(
        f"=== ESCALA: {escala.nome} ==="
    )
    print()

    if not escala.ocorrencias:
        print(
            "Esta escala não possui ocorrências."
        )
        return

    print(
        f"{'ID':<5}"
        f"{'DATA':<15}"
        f"{'EVENTO':<20}"
        f"{'FUNÇÃO':<20}"
        f"{'PESSOA'}"
    )

    for ocorrencia in escala.ocorrencias:
        data = ocorrencia.data.strftime(
            "%d/%m/%Y"
        )

        for atribuicao in (
            ocorrencia.atribuicoes
        ):
            print(
                f"{ocorrencia.id:<5}"
                f"{data:<15}"
                f"{ocorrencia.evento.nome:<20}"
                f"{atribuicao['funcao']:<20}"
                f"{atribuicao['pessoa']}"
            )


def gerar_nova_escala(
    escala_service,
    pessoa_service,
    evento_service,
    gerador_escala_service,
    motor_distribuicao
):
    print()
    print("=== GERAR NOVA ESCALA ===")
    print()

    # --------------------------------------------------
    # NOME
    # --------------------------------------------------

    nome = input(
        "Nome da escala: "
    ).strip()

    if not nome:
        print()
        print(
            "Nome da escala é obrigatório."
        )
        return

    # --------------------------------------------------
    # DATA INICIAL
    # --------------------------------------------------

    data_inicio = ler_data(
        "Data inicial (DD/MM/AAAA): "
    )

    if data_inicio is None:
        return

    # --------------------------------------------------
    # DATA FINAL
    # --------------------------------------------------

    data_fim = ler_data(
        "Data final (DD/MM/AAAA): "
    )

    if data_fim is None:
        return

    if data_inicio > data_fim:
        print()
        print(
            "A data inicial não pode ser maior "
            "que a data final."
        )
        return

    # --------------------------------------------------
    # EVENTOS
    # --------------------------------------------------

    eventos = evento_service.listar_todos()

    if not eventos:
        print()
        print(
            "Nenhum evento cadastrado."
        )
        return

    print()
    print("=== EVENTOS DISPONÍVEIS ===")
    print()

    for evento in eventos:
        funcoes = ", ".join(
            evento.funcoes_necessarias
        )

        print(
            f"{evento.id} - "
            f"{evento.nome} "
            f"[{funcoes}]"
        )

    print()

    entrada = input(
        "Digite os IDs dos eventos separados por vírgula: "
    )

    ids = entrada.split(",")

    eventos_selecionados = []

    for valor in ids:
        valor = valor.strip()

        if not valor:
            continue

        try:
            id_evento = int(valor)

        except ValueError:
            print()
            print(
                f"ID de evento inválido: {valor}"
            )
            return

        evento = evento_service.buscar_por_id(
            id_evento
        )

        if evento is None:
            print()
            print(
                f"Evento inválido: {id_evento}"
            )
            return

        eventos_selecionados.append(
            evento
        )

    if not eventos_selecionados:
        print()
        print(
            "É necessário selecionar pelo menos "
            "um evento."
        )
        return

    # --------------------------------------------------
    # CONFIGURAÇÃO DAS REGRAS DOS EVENTOS
    # --------------------------------------------------

    eventos_configurados = []

    indice_evento = 0

    while indice_evento < len(
        eventos_selecionados
    ):
        evento = eventos_selecionados[
            indice_evento
        ]

        resultado = criar_evento_configurado(
            evento
        )

        # 0 na escolha da regra:
        # volta para a seleção dos eventos.

        if resultado is None:
            print()
            print(
                "Voltando para a seleção dos eventos."
            )
            return

        eventos_configurados.append(
            resultado
        )

        indice_evento += 1

    # --------------------------------------------------
    # CRIA CONFIGURAÇÃO
    # --------------------------------------------------

    configuracao = ConfiguracaoEscala(
        nome=nome,
        data_inicio=data_inicio,
        data_fim=data_fim,
        eventos=eventos_configurados
    )

    print()
    print("Configuração criada.")
    print()

    print(
        "Nome:",
        configuracao.nome
    )

    print(
        "Período:",
        configuracao.data_inicio.strftime(
            "%d/%m/%Y"
        ),
        "a",
        configuracao.data_fim.strftime(
            "%d/%m/%Y"
        )
    )

    print("Eventos:")

    for evento_configurado in (
        configuracao.eventos
    ):
        print(
            f"- {evento_configurado.evento.nome}"
        )

        print(
            f"  Regra: "
            f"{nome_da_regra(evento_configurado.regra)}"
        )

    # --------------------------------------------------
    # GERAR OCORRÊNCIAS
    # --------------------------------------------------

    print()
    print(
        "Gerando ocorrências..."
    )

    ocorrencias = (
        gerador_escala_service.gerar_ocorrencias(
            configuracao
        )
    )

    print()
    print(
        f"Ocorrências geradas: "
        f"{len(ocorrencias)}"
    )

    if not ocorrencias:
        print()
        print(
            "Nenhuma ocorrência foi gerada."
        )
        return

    print()
    print("=== OCORRÊNCIAS ===")
    print()

    for ocorrencia in ocorrencias:
        print(
            f"{ocorrencia.data.strftime('%d/%m/%Y')}"
            f" - "
            f"{ocorrencia.evento.nome}"
        )

    print()
    print("Scheduler concluído.")

    # --------------------------------------------------
    # IDENTIFICAR FUNÇÕES
    # --------------------------------------------------

    funcoes_necessarias = (
        gerador_escala_service.encontrar_funcoes(
            ocorrencias
        )
    )

    if not funcoes_necessarias:
        print()
        print(
            "Nenhuma função foi encontrada "
            "nas ocorrências."
        )
        return

    print()
    print("=== FUNÇÕES DA ESCALA ===")
    print()

    for indice, funcao in enumerate(
        funcoes_necessarias,
        start=1
    ):
        print(
            f"F{indice} - {funcao}"
        )

    # --------------------------------------------------
    # ESCOLHER PESSOA INICIAL DA F1
    # --------------------------------------------------

    funcao_f1 = funcoes_necessarias[0]

    pessoas_iniciais = (
        gerador_escala_service.encontrar_pessoas_iniciais_f1(
            ocorrencias,
            funcao_f1
        )
    )

    if not pessoas_iniciais:
        print()
        print(
            f"Nenhuma pessoa disponível "
            f"para iniciar a F1 ({funcao_f1})."
        )
        return

    print()
    print(
        f"=== PESSOA INICIAL DA F1: "
        f"{funcao_f1} ==="
    )
    print()

    for indice, pessoa in enumerate(
        pessoas_iniciais,
        start=1
    ):
        print(
            f"{indice} - {pessoa.nome}"
        )

    print()
    print("0 - Voltar")
    print()

    while True:
        entrada = input(
            "Escolha a pessoa que inicia a F1: "
        ).strip()

        if entrada == "0":
            print()
            print(
                "Geração da escala cancelada."
            )
            return

        try:
            indice_pessoa = int(entrada)

        except ValueError:
            print()
            print(
                "Opção inválida."
            )
            continue

        if (
            indice_pessoa < 1
            or indice_pessoa > len(pessoas_iniciais)
        ):
            print()
            print(
                "Opção inválida."
            )
            continue

        pessoa_inicial_f1 = (
            pessoas_iniciais[
                indice_pessoa - 1
            ]
        )

        break

    print()
    print(
        f"Pessoa inicial da F1: "
        f"{pessoa_inicial_f1.nome}"
    )

    # --------------------------------------------------
    # MOTOR DE DISTRIBUIÇÃO
    # --------------------------------------------------

    print()
    print(
        "Distribuindo funções..."
    )

    try:
        motor_distribuicao.distribuir_todas_as_funcoes(
            pessoas=pessoa_service.listar_todos(),
            ocorrencias=ocorrencias,
            funcoes_necessarias=funcoes_necessarias,
            pessoa_inicial_f1=pessoa_inicial_f1
        )

    except ValueError as erro:
        print()
        print(
            "Erro na distribuição:"
        )
        print(erro)
        print()
        print(
            "A escala NÃO foi persistida."
        )
        return

    print()
    print(
        "Distribuição concluída."
    )

    # --------------------------------------------------
    # VALIDAR SE TODAS AS ATRIBUIÇÕES FORAM PREENCHIDAS
    # --------------------------------------------------

    if not validar_distribuicao(ocorrencias):
        print()
        print(
            "A distribuição não foi concluída "
            "corretamente."
        )
        print()
        print(
            "A escala NÃO foi persistida."
        )
        return

    # --------------------------------------------------
    # PERSISTÊNCIA
    #
    # SOMENTE AQUI a escala é criada no serviço.
    # --------------------------------------------------

    escala = escala_service.criar(
        nome,
        ocorrencias
    )

    print()
    print(
        "=== ESCALA GERADA COM SUCESSO ==="
    )
    print()

    print(
        f"ID: {escala.id}"
    )

    print(
        f"Nome: {escala.nome}"
    )

    print(
        f"Ocorrências: "
        f"{len(escala.ocorrencias)}"
    )

    print()
    print(
        "Scheduler concluído."
    )

    print(
        "Motor de distribuição concluído."
    )

    print(
        "Escala persistida com sucesso."
    )


def validar_distribuicao(ocorrencias):
    """
    Garante que nenhuma atribuição ficou sem pessoa.
    """

    for ocorrencia in ocorrencias:
        for atribuicao in ocorrencia.atribuicoes:
            if not atribuicao["pessoa"]:
                return False

    return True


def criar_evento_configurado(evento):
    regra = escolher_regra(
        evento
    )

    if regra is None:
        return None

    return EventoConfigurado(
        evento=evento,
        regra=regra
    )


def escolher_regra(evento):
    while True:
        print()
        print(
            f"=== REGRA DO EVENTO: "
            f"{evento.nome} ==="
        )
        print()

        print("0 - Voltar")
        print("1 - Semanal")
        print("2 - Mensal")
        print()

        opcao = input(
            "Escolha a regra: "
        )

        if opcao == "0":
            return None

        elif opcao == "1":
            regra = criar_regra_semanal()

            if regra is not None:
                return regra

        elif opcao == "2":
            regra = criar_regra_mensal()

            if regra is not None:
                return regra

        else:
            print()
            print(
                "Opção inválida."
            )


def criar_regra_semanal():
    from scheduler.regra_semanal import (
        RegraSemanal
    )

    print()
    print("=== REGRA SEMANAL ===")
    print()

    print("Dias da semana:")
    print("0 - Segunda")
    print("1 - Terça")
    print("2 - Quarta")
    print("3 - Quinta")
    print("4 - Sexta")
    print("5 - Sábado")
    print("6 - Domingo")
    print()

    entrada = input(
        "Digite os dias separados por vírgula: "
    )

    dias = []

    for valor in entrada.split(","):
        valor = valor.strip()

        if not valor:
            continue

        try:
            dia = int(valor)

        except ValueError:
            print()
            print(
                f"Dia inválido: {valor}"
            )
            return None

        dias.append(dia)

    try:
        return RegraSemanal(
            dias=dias
        )

    except ValueError as erro:
        print()
        print(erro)
        return None


def criar_regra_mensal():
    from scheduler.regra_mensal import (
        RegraMensal
    )

    print()
    print("=== REGRA MENSAL ===")
    print()

    print("Dias da semana:")
    print("0 - Segunda")
    print("1 - Terça")
    print("2 - Quarta")
    print("3 - Quinta")
    print("4 - Sexta")
    print("5 - Sábado")
    print("6 - Domingo")
    print()

    try:
        dia_semana = int(
            input("Dia da semana: ")
        )

        semana = int(
            input(
                "Semana do mês (1 a 5): "
            )
        )

        return RegraMensal(
            dia_semana=dia_semana,
            semana=semana
        )

    except ValueError as erro:
        print()
        print(
            f"Valor inválido: {erro}"
        )
        return None


def nome_da_regra(regra):
    nome_classe = (
        regra.__class__.__name__
    )

    if nome_classe == "RegraSemanal":
        return "Semanal"

    if nome_classe == "RegraMensal":
        return "Mensal"

    return nome_classe


def ler_data(mensagem):
    entrada = input(
        mensagem
    ).strip()

    try:
        dia, mes, ano = map(
            int,
            entrada.split("/")
        )

        return date(
            ano,
            mes,
            dia
        )

    except ValueError:
        print()
        print(
            "Data inválida. "
            "Use o formato DD/MM/AAAA."
        )
        return None


def obter_periodo(escala):
    if not escala.ocorrencias:
        return "Sem ocorrências"

    primeira_data = (
        escala.ocorrencias[0].data
    )

    ultima_data = (
        escala.ocorrencias[-1].data
    )

    return (
        f"{primeira_data.strftime('%d/%m/%Y')} "
        f"a "
        f"{ultima_data.strftime('%d/%m/%Y')}"
    )
