from storage.pessoa_storage import PessoaStorage
from storage.funcao_storage import FuncaoStorage
from storage.evento_storage import EventoStorage
from storage.escala_storage import EscalaStorage

from services.pessoa_service import PessoaService
from services.funcao_service import FuncaoService
from services.evento_service import EventoService
from services.escala_service import EscalaService
from services.gerador_escala_service import GeradorEscalaService
from services.motor_distribuicao import MotorDistribuicao

from cli.menu import iniciar


def main():

    pessoa_storage = PessoaStorage()
    funcao_storage = FuncaoStorage()
    evento_storage = EventoStorage()
    escala_storage = EscalaStorage()

    pessoas = pessoa_storage.carregar()
    funcoes = funcao_storage.carregar()
    eventos = evento_storage.carregar()
    escalas = escala_storage.carregar()

    pessoa_service = PessoaService(
        pessoas
    )

    funcao_service = FuncaoService(
        funcoes
    )

    evento_service = EventoService(
        eventos,
        funcoes
    )

    escala_service = EscalaService(
        escalas
    )

    gerador_escala_service = GeradorEscalaService(
        pessoas
    )

    motor_distribuicao = MotorDistribuicao()

    resultado = iniciar(
        pessoa_service,
        funcao_service,
        evento_service,
        escala_service,
        gerador_escala_service,
        motor_distribuicao
    )

    if resultado == "pessoa":
        pessoa_storage.salvar(
            pessoas
        )

    if resultado == "funcao":
        funcao_storage.salvar(
            funcoes
        )

    if resultado == "evento":
        evento_storage.salvar(
            eventos
        )

    if resultado == "escala":
        escala_storage.salvar(
            escalas
        )


if __name__ == "__main__":
    main()
