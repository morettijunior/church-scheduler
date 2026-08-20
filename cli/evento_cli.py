def iniciar(evento_service, funcao_service):

    alterado = False

    while True:

        print()
        print("=== EVENTOS ===")
        print()
        print("1 - Listar eventos")
        print("2 - Atualizar evento")
        print("0 - Voltar")
        print()

        opcao = input("Escolha uma opção: ")

        if opcao == "0":
            return alterado

        elif opcao == "1":
            listar(evento_service)

        elif opcao == "2":
            resultado = atualizar(
                evento_service,
                funcao_service
            )

            if resultado["alterado"]:
                alterado = True

        else:
            print("Opção inválida.")


def listar(evento_service):

    eventos = evento_service.listar_todos()

    print()
    print("=== EVENTOS ===")
    print()

    if not eventos:
        print("Nenhum evento cadastrado.")
        return

    print(
        f"{'ID':<5}"
        f"{'EVENTO':<20}"
        f"FUNÇÕES NECESSÁRIAS"
    )

    for evento in eventos:

        funcoes = ", ".join(evento.funcoes_necessarias)

        print(
            f"{evento.id:<5}"
            f"{evento.nome:<20}"
            f"{funcoes}"
        )


def atualizar(evento_service, funcao_service):

    print()
    print("=== ATUALIZAR EVENTO ===")
    print()

    id = int(input("ID do evento: "))

    evento = evento_service.buscar_por_id(id)

    if evento is None:
        print()
        print("Digite um ID válido")

        return {
            "sucesso": False,
            "alterado": False,
            "mensagem": "Digite um ID válido"
        }

    funcoes = funcao_service.listar_ativos()

    if not funcoes:
        print()
        print("Nenhuma função ativa cadastrada.")

        return {
            "sucesso": False,
            "alterado": False,
            "mensagem": "Nenhuma função ativa cadastrada"
        }

    print()
    print("=== FUNÇÕES DISPONÍVEIS ===")
    print()

    for funcao in funcoes:
        print(
            f"{funcao.id} - {funcao.nome}"
        )

    print()

    entrada = input(
        "Digite os IDs das funções separados por vírgula: "
    )

    ids = entrada.split(",")

    funcoes_necessarias = []

    for valor in ids:

        valor = valor.strip()

        if not valor:
            continue

        try:
            id_funcao = int(valor)
        except ValueError:
            print()
            print(f"ID de função inválido: {valor}")

            return {
                "sucesso": False,
                "alterado": False,
                "mensagem": "ID de função inválido"
            }

        funcao = funcao_service.buscar_por_id(id_funcao)

        if funcao is None or not funcao.ativo:
            print()
            print(f"Função inválida: {id_funcao}")

            return {
                "sucesso": False,
                "alterado": False,
                "mensagem": "Função inválida"
            }

        funcoes_necessarias.append(funcao.nome)

    resultado = evento_service.atualizar(
        id,
        funcoes_necessarias
    )

    print()
    print(resultado["mensagem"])

    return resultado