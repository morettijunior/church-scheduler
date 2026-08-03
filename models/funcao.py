from dataclasses import dataclass, field


@dataclass
class Funcao:
    nome: str
    ativo: bool = True
    id: int = field(init=False)

    _proximo_id = 1

    def __post_init__(self):
        self.id = Funcao._proximo_id
        Funcao._proximo_id += 1

        self.nome = self.nome.strip()

        if not self.nome:
            raise ValueError("Nome obrigatório")