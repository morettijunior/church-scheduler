from dataclasses import dataclass, field


@dataclass
class Pessoa:
    nome: str
    telefone: str
    funcoes: list = field(default_factory=list)
    ativo: bool = True
    restricoes: list = field(default_factory=list)

    id: int = field(init=False)

    _proximo_id = 1

    def __post_init__(self):
        self.id = Pessoa._proximo_id
        Pessoa._proximo_id += 1

        self.nome = self.nome.strip()
        self.telefone = self.telefone.strip()

        if not self.nome:
            raise ValueError("Nome obrigatório")

        if not self.telefone:
            raise ValueError("Telefone obrigatório")