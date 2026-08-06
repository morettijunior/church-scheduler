from models.funcao import Funcao
from storage.funcao_storage import FuncaoStorage


storage = FuncaoStorage()


funcoes = storage.carregar()


nova_funcao = Funcao(
    nome="EBI"
)


funcoes.append(nova_funcao)


storage.salvar(funcoes)


for funcao in funcoes:
    print(
        funcao.id,
        funcao.nome
    )