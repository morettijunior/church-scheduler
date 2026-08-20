def iniciar(escala_service):

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
            listar(escala_service)

        elif opcao == "2":
            visualizar(escala_service)

        elif opcao == "3":
            print()
            print("Geração de escala ainda não implementada.")

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

        periodo = obter_periodo(escala)

        print(
            f"{escala.id:<5}"
            f"{escala.nome:<25}"
            f"{periodo}"
        )


def visualizar(escala_service):

    print()
    print("=== VISUALIZAR ESCALA ===")
    print()

    id_escala = int(input("ID da escala: "))

    escala = escala_service.buscar_por_id(id_escala)

    if escala is None:
        print()
        print("Digite um ID válido.")
        return

    print()
    print(f"=== ESCALA: {escala.nome} ===")
    print()

    if not escala.ocorrencias:
        print("Esta escala não possui ocorrências.")
        return

    print(
        f"{'ID':<5}"
        f"{'DATA':<15}"
        f"{'EVENTO':<20}"
        f"{'FUNÇÃO':<20}"
        f"{'PESSOA'}"
    )

    for ocorrencia in escala.ocorrencias:

        data = ocorrencia.data.strftime("%d/%m/%Y")

        for atribuicao in ocorrencia.atribuicoes:

            print(
                f"{ocorrencia.id:<5}"
                f"{data:<15}"
                f"{ocorrencia.evento.nome:<20}"
                f"{atribuicao['funcao']:<20}"
                f"{atribuicao['pessoa']}"
            )


def obter_periodo(escala):

    if not escala.ocorrencias:
        return "Sem ocorrências"

    primeira_data = escala.ocorrencias[0].data
    ultima_data = escala.ocorrencias[-1].data

    return (
        f"{primeira_data.strftime('%d/%m/%Y')} "
        f"a "
        f"{ultima_data.strftime('%d/%m/%Y')}"
    )