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
        f"FUNÇÕES"
    )

    for pessoa in pessoas:
        funcoes = ", ".join(pessoa.funcoes)

        print(
            f"{pessoa.id:<5}"
            f"{pessoa.nome:<25}"
            f"{pessoa.telefone:<20}"
            f"{funcoes}"
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
        f"FUNÇÕES"
    )

    for pessoa in pessoas:
        funcoes = ", ".join(pessoa.funcoes)

        print(
            f"{pessoa.id:<5}"
            f"{pessoa.nome:<25}"
            f"{pessoa.telefone:<20}"
            f"{funcoes}"
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
        f"FUNÇÕES"
    )

    for pessoa in pessoas:
        if pessoa.ativo:
            status = "ATIVO"
        else:
            status = "INATIVO"

        funcoes = ", ".join(pessoa.funcoes)

        print(
            f"{pessoa.id:<5}"
            f"{pessoa.nome:<25}"
            f"{pessoa.telefone:<20}"
            f"{status:<10}"
            f"{funcoes}"
        )


def cadastrar(pessoa_service, funcao_service):
    print()
    print("=== CADASTRAR PESSOA ===")
    print()

    nome = input("Nome: ")
    telefone = input("Telefone: ")

    funcoes = selecionar_funcoes(funcao_service)

    restricoes = []

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
        funcoes = selecionar_funcoes(funcao_service)
    else:
        funcoes = pessoa.funcoes

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

    entrada = input("IDs das funções: ").strip()

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

        ids_selecionados.add(id_funcao)

    return funcoes_selecionadas


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
