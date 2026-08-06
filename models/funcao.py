from dataclasses import dataclass, field


@dataclass
class Funcao:
    nome: str
    ativo: bool = True
    id: int | None = None

    _proximo_id = 1

    def __post_init__(self):

        self.nome = self.nome.strip()

        if not self.nome:
            raise ValueError("Nome obrigatório")
        
        if self.id is None:
            self.id = Funcao._proximo_id

        if self.id >= Funcao._proximo_id:
            Funcao._proximo_id = self.id + 1