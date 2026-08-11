from storage.funcao_storage import FuncaoStorage
from services.funcao_service import FuncaoService


storage = FuncaoStorage()
funcoes = storage.carregar()

service = FuncaoService(funcoes)


resultado = service.desativar(1)

print(resultado)
print(service.buscar_por_id(1))

resultado = service.desativar(1)

print(resultado)

resultado = service.desativar(999)

print(resultado)

resultado = service.ativar(1)

print(resultado)
print(service.buscar_por_id(1))

resultado = service.ativar(999)

print(resultado)

