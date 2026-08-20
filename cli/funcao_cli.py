def iniciar(funcao_service):

    alterado = False

    while True:

        print()
        print("=== FUNÇÕES ===")
        print()
        print("1 - Listar funções ativas")
        print("2 - Listar funções inativas")
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
            listar_ativos(funcao_service)

        elif opcao == "2":
            listar_inativos(funcao_service)

        elif opcao == "3":
            listar_todas(funcao_service)

        elif opcao == "4":
            resultado = cadastrar(funcao_service)

            if resultado["alterado"]:
                alterado = True

        elif opcao == "5":
            resultado = atualizar(funcao_service)

            if resultado["alterado"]:
                alterado = True

        elif opcao == "6":
            resultado = ativar(funcao_service)

            if resultado["alterado"]:
                alterado = True

        elif opcao == "7":
            resultado = inativar(funcao_service)

            if resultado["alterado"]:
                alterado = True

        else:
            print("Opção inválida.")


def listar_ativos(funcao_service):

    funcoes = funcao_service.listar_ativos()

    print()
    print("=== FUNÇÕES ATIVAS ===")
    print()

    if not funcoes:
        print("Nenhuma função ativa cadastrada.")
        return

    print(f"{'ID':<5}{'NOME'}")

    for funcao in funcoes:
        print(
            f"{funcao.id:<5}"
            f"{funcao.nome}"
        )


def listar_inativos(funcao_service):

    funcoes = funcao_service.listar_inativos()

    print()
    print("=== FUNÇÕES INATIVAS ===")
    print()

    if not funcoes:
        print("Nenhuma função inativa cadastrada.")
        return

    print(f"{'ID':<5}{'NOME'}")

    for funcao in funcoes:
        print(
            f"{funcao.id:<5}"
            f"{funcao.nome}"
        )


def listar_todas(funcao_service):

    funcoes = funcao_service.listar_todos()

    print()
    print("=== TODAS AS FUNÇÕES ===")
    print()

    if not funcoes:
        print("Nenhuma função cadastrada.")
        return

    print(f"{'ID':<5}{'NOME':<20}{'STATUS'}")

    for funcao in funcoes:

        if funcao.ativo:
            status = "ATIVO"
        else:
            status = "INATIVO"

        print(
            f"{funcao.id:<5}"
            f"{funcao.nome:<20}"
            f"{status}"
        )


def cadastrar(funcao_service):

    print()
    print("=== CADASTRAR FUNÇÃO ===")
    print()

    nome = input("Nome da função: ")

    resultado = funcao_service.cadastrar(nome)

    print()
    print(resultado["mensagem"])

    return resultado


def atualizar(funcao_service):

    print()
    print("=== ATUALIZAR FUNÇÃO ===")
    print()

    id = int(input("ID da função: "))

    funcao = funcao_service.buscar_por_id(id)

    if funcao is None:
        print()
        print("Digite um ID válido")
        return {
            "sucesso": False,
            "alterado": False,
            "mensagem": "Digite um ID válido"
        }

    nome = input("Novo nome da função: ")

    resultado = funcao_service.atualizar(
        id,
        nome
    )

    print()
    print(resultado["mensagem"])

    return resultado


def ativar(funcao_service):

    print()
    print("=== ATIVAR FUNÇÃO ===")
    print()

    id = int(input("ID da função: "))

    funcao = funcao_service.buscar_por_id(id)

    if funcao is None:
        print()
        print("Digite um ID válido")
        return {
            "sucesso": False,
            "alterado": False,
            "mensagem": "Digite um ID válido"
        }

    resultado = funcao_service.ativar(id)

    print()
    print(resultado["mensagem"])

    return resultado


def inativar(funcao_service):

    print()
    print("=== INATIVAR FUNÇÃO ===")
    print()

    id = int(input("ID da função: "))

    funcao = funcao_service.buscar_por_id(id)

    if funcao is None:
        print()
        print("Digite um ID válido")
        return {
            "sucesso": False,
            "alterado": False,
            "mensagem": "Digite um ID válido"
        }

    resultado = funcao_service.desativar(id)

    print()
    print(resultado["mensagem"])

    return resultado