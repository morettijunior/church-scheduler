from dataclasses import dataclass, field


@dataclass
class Pessoa:
    nome: str
    telefone: str
    funcoes: list = field(default_factory=list)
    ativo: bool = True
    restricoes: list = field(default_factory=list)

    id: int | None = None

    _proximo_id = 1

    def __post_init__(self):

        if not self.nome:
            raise ValueError("Nome obrigatório")

        if not self.telefone:
            raise ValueError("Telefone obrigatório")

        if self.id is None:
            self.id = Pessoa._proximo_id

        if self.id >= Pessoa._proximo_id:
            Pessoa._proximo_id = self.id + 1