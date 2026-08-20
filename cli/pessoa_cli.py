def iniciar(pessoa_service):

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
            resultado = cadastrar(pessoa_service)

            if resultado["alterado"]:
                alterado = True

        elif opcao == "5":
            resultado = atualizar(pessoa_service)

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

    print(f"{'ID':<5}{'NOME':<25}{'TELEFONE'}")

    for pessoa in pessoas:

        print(
            f"{pessoa.id:<5}"
            f"{pessoa.nome:<25}"
            f"{pessoa.telefone}"
        )


def listar_inativos(pessoa_service):

    pessoas = pessoa_service.listar_inativos()

    print()
    print("=== PESSOAS INATIVAS ===")
    print()

    if not pessoas:
        print("Nenhuma pessoa inativa cadastrada.")
        return

    print(f"{'ID':<5}{'NOME':<25}{'TELEFONE'}")

    for pessoa in pessoas:

        print(
            f"{pessoa.id:<5}"
            f"{pessoa.nome:<25}"
            f"{pessoa.telefone}"
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
        f"{'STATUS'}"
    )

    for pessoa in pessoas:

        if pessoa.ativo:
            status = "ATIVO"
        else:
            status = "INATIVO"

        print(
            f"{pessoa.id:<5}"
            f"{pessoa.nome:<25}"
            f"{pessoa.telefone:<20}"
            f"{status}"
        )


def cadastrar(pessoa_service):

    print()
    print("=== CADASTRAR PESSOA ===")
    print()

    nome = input("Nome: ")
    telefone = input("Telefone: ")

    # Temporariamente vazias.
    # Vamos implementar funções e restrições
    # depois, através dos respectivos menus.
    funcoes = []
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


def atualizar(pessoa_service):

    print()
    print("=== ATUALIZAR PESSOA ===")
    print()

    id = int(input("ID da pessoa: "))

    pessoa = pessoa_service.buscar_por_id(id)

    if pessoa is None:
        print()
        print("Digite um ID válido")

        return {
            "sucesso": False,
            "alterado": False,
            "mensagem": "Digite um ID válido"
        }

    nome = input("Novo nome: ")
    telefone = input("Novo telefone: ")

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


def ativar(pessoa_service):

    print()
    print("=== ATIVAR PESSOA ===")
    print()

    id = int(input("ID da pessoa: "))

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

    id = int(input("ID da pessoa: "))

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