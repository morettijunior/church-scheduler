from storage.pessoa_storage import PessoaStorage
from models.pessoa import Pessoa


storage = PessoaStorage()

pessoas = storage.carregar()


nova = Pessoa(
    nome="Maria",
    telefone="555555555",
    funcoes=["Porta"]
)


pessoas.append(nova)


for pessoa in pessoas:
    print(pessoa.id, pessoa.nome)