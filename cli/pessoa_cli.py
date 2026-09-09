from datetime import datetime


def iniciar(pessoa_service, funcao_service):
    alterado = False

    while True:
        print()
        print("=== PESSOAS ===")
        print()
        print("1 - Listar pessoas ativas")
        print("2 - Listar pessoas inativas")
        print("3 - Listar todas")
        print("4 - Cadastrar")
        print("5 - Atualizar")
        print("6 - Ativar")
        print("7 - Inativar")
        print("0 - Voltar")
        print()

        opcao = input("Escolha uma opção: ")

        if opcao == "0":
            return alterado

        elif opcao == "1":
            listar_ativos(pessoa_service)

        elif opcao == "2":
            listar_inativos(pessoa_service)

        elif opcao == "3":
            listar_todas(pessoa_service)

        elif opcao == "4":
            resultado = cadastrar(
                pessoa_service,
                funcao_service
            )

            if resultado["alterado"]:
                alterado = True

        elif opcao == "5":
            resultado = atualizar(
                pessoa_service,
                funcao_service
            )

            if resultado["alterado"]:
                alterado = True

        elif opcao == "6":
            resultado = ativar(pessoa_service)

            if resultado["alterado"]:
                alterado = True

        elif opcao == "7":
            resultado = inativar(pessoa_service)

            if resultado["alterado"]:
                alterado = True

        else:
            print("Opção inválida.")


def listar_ativos(pessoa_service):
    pessoas = pessoa_service.listar_ativos()

    print()
    print("=== PESSOAS ATIVAS ===")
    print()

    if not pessoas:
        print("Nenhuma pessoa ativa cadastrada.")
        return

    print(
        f"{'ID':<5}"
        f"{'NOME':<25}"
        f"{'TELEFONE':<20}"
        f"{'FUNÇÕES':<25}"
        f"RESTRIÇÕES"
    )

    for pessoa in pessoas:
        funcoes = ", ".join(pessoa.funcoes)
        restricoes = formatar_restricoes(
            pessoa.restricoes
        )

        print(
            f"{pessoa.id:<5}"
            f"{pessoa.nome:<25}"
            f"{pessoa.telefone:<20}"
            f"{funcoes:<25}"
            f"{restricoes}"
        )


def listar_inativos(pessoa_service):
    pessoas = pessoa_service.listar_inativos()

    print()
    print("=== PESSOAS INATIVAS ===")
    print()

    if not pessoas:
        print("Nenhuma pessoa inativa cadastrada.")
        return

    print(
        f"{'ID':<5}"
        f"{'NOME':<25}"
        f"{'TELEFONE':<20}"
        f"{'FUNÇÕES':<25}"
        f"RESTRIÇÕES"
    )

    for pessoa in pessoas:
        funcoes = ", ".join(pessoa.funcoes)
        restricoes = formatar_restricoes(
            pessoa.restricoes
        )

        print(
            f"{pessoa.id:<5}"
            f"{pessoa.nome:<25}"
            f"{pessoa.telefone:<20}"
            f"{funcoes:<25}"
            f"{restricoes}"
        )


def listar_todas(pessoa_service):
    pessoas = pessoa_service.listar_todos()

    print()
    print("=== TODAS AS PESSOAS ===")
    print()

    if not pessoas:
        print("Nenhuma pessoa cadastrada.")
        return

    print(
        f"{'ID':<5}"
        f"{'NOME':<25}"
        f"{'TELEFONE':<20}"
        f"{'STATUS':<10}"
        f"{'FUNÇÕES':<25}"
        f"RESTRIÇÕES"
    )

    for pessoa in pessoas:

        if pessoa.ativo:
            status = "ATIVO"
        else:
            status = "INATIVO"

        funcoes = ", ".join(pessoa.funcoes)

        restricoes = formatar_restricoes(
            pessoa.restricoes
        )

        print(
            f"{pessoa.id:<5}"
            f"{pessoa.nome:<25}"
            f"{pessoa.telefone:<20}"
            f"{status:<10}"
            f"{funcoes:<25}"
            f"{restricoes}"
        )


def cadastrar(pessoa_service, funcao_service):
    print()
    print("=== CADASTRAR PESSOA ===")
    print()

    nome = input("Nome: ")
    telefone = input("Telefone: ")

    funcoes = selecionar_funcoes(
        funcao_service
    )

    restricoes = selecionar_restricoes()

    resultado = pessoa_service.cadastrar(
        nome,
        telefone,
        funcoes,
        restricoes
    )

    print()
    print(resultado["mensagem"])

    return resultado


def atualizar(pessoa_service, funcao_service):
    print()
    print("=== ATUALIZAR PESSOA ===")
    print()

    try:
        id = int(input("ID da pessoa: "))
    except ValueError:
        print()
        print("Digite um ID válido.")

        return {
            "sucesso": False,
            "alterado": False,
            "mensagem": "Digite um ID válido"
        }

    pessoa = pessoa_service.buscar_por_id(id)

    if pessoa is None:
        print()
        print("Digite um ID válido")

        return {
            "sucesso": False,
            "alterado": False,
            "mensagem": "Digite um ID válido"
        }

    print()
    print(f"Nome atual: {pessoa.nome}")

    novo_nome = input(
        "Novo nome (ENTER mantém o atual): "
    ).strip()

    if novo_nome == "":
        nome = pessoa.nome
    else:
        nome = novo_nome

    print()
    print(f"Telefone atual: {pessoa.telefone}")

    novo_telefone = input(
        "Novo telefone (ENTER mantém o atual): "
    ).strip()

    if novo_telefone == "":
        telefone = pessoa.telefone
    else:
        telefone = novo_telefone

    print()
    print("Funções atuais:")

    if pessoa.funcoes:
        for funcao in pessoa.funcoes:
            print(f"- {funcao}")
    else:
        print("Nenhuma função cadastrada.")

    print()

    alterar_funcoes = input(
        "Deseja alterar as funções? (S/N): "
    ).strip().upper()

    if alterar_funcoes == "S":
        funcoes = selecionar_funcoes(
            funcao_service
        )
    else:
        funcoes = pessoa.funcoes

    print()
    print("Restrições atuais:")

    restricoes_atuais = formatar_restricoes(
        pessoa.restricoes
    )

    print(restricoes_atuais)

    print()

    alterar_restricoes = input(
        "Deseja alterar as restrições? (S/N): "
    ).strip().upper()

    if alterar_restricoes == "S":
        restricoes = selecionar_restricoes()
    else:
        restricoes = pessoa.restricoes

    resultado = pessoa_service.atualizar(
        id,
        nome,
        telefone,
        funcoes,
        restricoes
    )

    print()
    print(resultado["mensagem"])

    return resultado


def selecionar_funcoes(funcao_service):
    funcoes_ativas = funcao_service.listar_ativos()

    print()
    print("=== SELECIONAR FUNÇÕES ===")
    print()

    if not funcoes_ativas:
        print("Nenhuma função ativa cadastrada.")
        return []

    for funcao in funcoes_ativas:
        print(
            f"{funcao.id} - {funcao.nome}"
        )

    print()
    print(
        "Digite os IDs das funções separados por vírgula."
    )
    print(
        "Exemplo: 1,2,3"
    )
    print(
        "Deixe vazio caso a pessoa não tenha função."
    )
    print()

    entrada = input(
        "IDs das funções: "
    ).strip()

    if entrada == "":
        return []

    ids_texto = entrada.split(",")

    funcoes_selecionadas = []
    ids_selecionados = set()

    for id_texto in ids_texto:

        id_texto = id_texto.strip()

        if not id_texto.isdigit():
            print(
                f"ID inválido ignorado: {id_texto}"
            )
            continue

        id_funcao = int(id_texto)

        if id_funcao in ids_selecionados:
            continue

        funcao = funcao_service.buscar_por_id(
            id_funcao
        )

        if funcao is None:
            print(
                f"Função não encontrada: {id_funcao}"
            )
            continue

        if not funcao.ativo:
            print(
                f"Função inativa não pode ser atribuída: "
                f"{funcao.nome}"
            )
            continue

        funcoes_selecionadas.append(
            funcao.nome
        )

        ids_selecionados.add(
            id_funcao
        )

    return funcoes_selecionadas


def selecionar_restricoes():
    restricoes = []

    while True:

        print()
        print("=== RESTRIÇÕES ===")
        print()
        print("1 - Não pode em dias da semana")
        print("2 - Não pode em datas específicas")
        print("3 - Remover todas as restrições")
        print("0 - Finalizar")
        print()

        opcao = input(
            "Escolha uma opção: "
        ).strip()

        if opcao == "0":
            break

        elif opcao == "1":
            novas_restricoes = selecionar_dias_semana()

            for restricao in novas_restricoes:
                if restricao not in restricoes:
                    restricoes.append(restricao)

        elif opcao == "2":
            novas_restricoes = selecionar_datas()

            for restricao in novas_restricoes:
                if restricao not in restricoes:
                    restricoes.append(restricao)

        elif opcao == "3":
            restricoes = []

            print()
            print("Todas as restrições foram removidas.")

        else:
            print("Opção inválida.")

    return restricoes


def selecionar_dias_semana():
    dias = [
        (1, "SEGUNDA-FEIRA"),
        (2, "TERÇA-FEIRA"),
        (3, "QUARTA-FEIRA"),
        (4, "QUINTA-FEIRA"),
        (5, "SEXTA-FEIRA"),
        (6, "SÁBADO"),
        (7, "DOMINGO")
    ]

    print()
    print("=== DIAS DA SEMANA ===")
    print()

    for numero, nome in dias:
        print(
            f"{numero} - {nome}"
        )

    print()
    print(
        "Digite os números separados por vírgula."
    )
    print(
        "Exemplo: 1,3,7"
    )
    print()

    entrada = input(
        "Dias: "
    ).strip()

    if entrada == "":
        return []

    restricoes = []

    for valor in entrada.split(","):

        valor = valor.strip()

        if not valor.isdigit():
            print(
                f"Dia inválido ignorado: {valor}"
            )
            continue

        numero = int(valor)

        if numero < 1 or numero > 7:
            print(
                f"Dia inválido ignorado: {numero}"
            )
            continue

        restricao = {
            "tipo": "DIA_SEMANA",
            "valor": numero - 1
        }

        if restricao not in restricoes:
            restricoes.append(
                restricao
            )

    return restricoes


def selecionar_datas():
    print()
    print("=== DATAS ESPECÍFICAS ===")
    print()
    print(
        "Digite as datas no formato DD/MM/AAAA."
    )
    print(
        "Separe várias datas por vírgula."
    )
    print(
        "Exemplo: 10/09/2026,25/12/2026"
    )
    print()

    entrada = input(
        "Datas: "
    ).strip()

    if entrada == "":
        return []

    restricoes = []

    for valor in entrada.split(","):

        valor = valor.strip()

        try:
            data = datetime.strptime(
                valor,
                "%d/%m/%Y"
            ).date()

        except ValueError:
            print(
                f"Data inválida ignorada: {valor}"
            )
            continue

        restricao = {
            "tipo": "DATA",
            "valor": data.strftime("%d/%m/%Y")
        }

        if restricao not in restricoes:
            restricoes.append(
                restricao
            )

    return restricoes


def formatar_restricoes(restricoes):
    if not restricoes:
        return "NENHUMA"

    nomes_dias = {
        0: "SEG",
        1: "TER",
        2: "QUA",
        3: "QUI",
        4: "SEX",
        5: "SAB",
        6: "DOM"
    }

    resultado = []

    for restricao in restricoes:

        if not isinstance(restricao, dict):
            continue

        tipo = restricao.get("tipo")
        valor = restricao.get("valor")

        if tipo == "DIA_SEMANA":

            try:
                dia = int(valor)
            except (TypeError, ValueError):
                continue

            nome_dia = nomes_dias.get(
                dia,
                "?"
            )

            resultado.append(
                f"NÃO {nome_dia}"
            )

        elif tipo == "DATA":

            resultado.append(
                f"NÃO {valor}"
            )

    if not resultado:
        return "NENHUMA"

    return ", ".join(resultado)


def ativar(pessoa_service):
    print()
    print("=== ATIVAR PESSOA ===")
    print()

    try:
        id = int(input("ID da pessoa: "))
    except ValueError:
        print()
        print("Digite um ID válido.")

        return {
            "sucesso": False,
            "alterado": False,
            "mensagem": "Digite um ID válido"
        }

    pessoa = pessoa_service.buscar_por_id(id)

    if pessoa is None:
        print()
        print("Digite um ID válido")

        return {
            "sucesso": False,
            "alterado": False,
            "mensagem": "Digite um ID válido"
        }

    resultado = pessoa_service.ativar(id)

    print()
    print(resultado["mensagem"])

    return resultado


def inativar(pessoa_service):
    print()
    print("=== INATIVAR PESSOA ===")
    print()

    try:
        id = int(input("ID da pessoa: "))
    except ValueError:
        print()
        print("Digite um ID válido.")

        return {
            "sucesso": False,
            "alterado": False,
            "mensagem": "Digite um ID válido"
        }

    pessoa = pessoa_service.buscar_por_id(id)

    if pessoa is None:
        print()
        print("Digite um ID válido")

        return {
            "sucesso": False,
            "alterado": False,
            "mensagem": "Digite um ID válido"
        }

    resultado = pessoa_service.desativar(id)

    print()
    print(resultado["mensagem"])

    return resultado