from cli import pessoa_cli
from cli import funcao_cli
from cli import evento_cli
from cli import escala_cli


def iniciar(
    pessoa_service,
    funcao_service,
    evento_service,
    escala_service,
    gerador_escala_service,
    motor_distribuicao
):
    while True:
        print()
        print("=== CHURCH SCHEDULER ===")
        print()
        print("1 - Pessoas")
        print("2 - Funções")
        print("3 - Eventos")
        print("4 - Escalas")
        print("0 - Sair")
        print()

        opcao = input(
            "Escolha uma opção: "
        )

        if opcao == "0":
            print()
            print("Encerrando...")
            return None

        elif opcao == "1":
            resultado = pessoa_cli.iniciar(
                pessoa_service,
                funcao_service
            )

            if resultado:
                return "pessoa"

        elif opcao == "2":
            resultado = funcao_cli.iniciar(
                funcao_service
            )

            if resultado:
                return "funcao"

        elif opcao == "3":
            resultado = evento_cli.iniciar(
                evento_service,
                funcao_service
            )

            if resultado:
                return "evento"

        elif opcao == "4":
            resultado = escala_cli.iniciar(
                escala_service,
                pessoa_service,
                evento_service,
                gerador_escala_service,
                motor_distribuicao
            )

            if resultado:
                return "escala"

        else:
            print()
            print("Opção inválida.")

