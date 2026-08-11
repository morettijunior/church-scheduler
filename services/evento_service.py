from models.evento import Evento
from models.funcao import Funcao


class EventoService:

    def __init__(
        self,
        eventos: list[Evento],
        funcoes: list[Funcao]
    ):
        self._eventos = eventos
        self._funcoes = funcoes

    def listar_todos(self) -> list[Evento]:

        todos = []

        for evento in self._eventos:
            todos.append(evento)

        todos.sort(key=lambda evento: evento.id)

        return todos

    def buscar_por_id(self, id: int) -> Evento | None:

        for evento in self._eventos:

            if evento.id == id:
                return evento

        return None

    def atualizar(
        self,
        id: int,
        funcoes_necessarias: list
    ):

        evento = self.buscar_por_id(id)

        if evento is None:
            return {
                "sucesso": False,
                "alterado": False,
                "mensagem": "Digite um ID válido"
            }

        funcoes_normalizadas = []

        for nome_funcao in funcoes_necessarias:

            nome_funcao = nome_funcao.strip().upper()

            funcoes_normalizadas.append(nome_funcao)

        for nome_funcao in funcoes_normalizadas:

            existe = False

            for funcao in self._funcoes:

                if funcao.nome == nome_funcao:
                    existe = True
                    break

            if not existe:
                return {
                    "sucesso": False,
                    "alterado": False,
                    "mensagem": f"Função não cadastrada: {nome_funcao}"
                }

        evento.funcoes_necessarias = funcoes_normalizadas

        return {
            "sucesso": True,
            "alterado": True,
            "mensagem": "Evento atualizado"
        }