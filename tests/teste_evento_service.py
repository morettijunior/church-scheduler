from models.funcao import Funcao
from storage.evento_storage import EventoStorage
from services.evento_service import EventoService


evento_storage = EventoStorage()

eventos = evento_storage.carregar()


funcoes = [
    Funcao(nome="ATRIO"),
    Funcao(nome="PORTA"),
    Funcao(nome="PATIO")
]


service = EventoService(
    eventos,
    funcoes
)


resultado = service.atualizar(
    1,
    []
)

print(resultado)
print(service.buscar_por_id(1))