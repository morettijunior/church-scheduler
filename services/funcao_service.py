from models.funcao import Funcao


class FuncaoService:

    def __init__(self, funcoes: list[Funcao]):
        self._funcoes = funcoes

    def listar_ativos(self) -> list[Funcao]:

        ativos = []

        for funcao in self._funcoes:

            if funcao.ativo:
                ativos.append(funcao)

        ativos.sort(key=lambda funcao: funcao.nome)

        return ativos

    def listar_inativos(self) -> list[Funcao]:

        inativos = []

        for funcao in self._funcoes:

            if not funcao.ativo:
                inativos.append(funcao)

        inativos.sort(key=lambda funcao: funcao.nome)

        return inativos

    def listar_todos(self) -> list[Funcao]:

        todos = []

        for funcao in self._funcoes:
            todos.append(funcao)

        todos.sort(key=lambda funcao: funcao.id)

        return todos

    def buscar_por_id(self, id: int) -> Funcao | None:

        for funcao in self._funcoes:

            if funcao.id == id:
                return funcao

        return None

    def cadastrar(self, nome: str):

        nome = nome.strip().upper()

        if nome == "":
            return {
                "sucesso": False,
                "alterado": False,
                "mensagem": "Necessário cadastrar nome de função"
            }

        for funcao in self._funcoes:

            if funcao.nome.strip().upper() == nome:
                return {
                    "sucesso": False,
                    "alterado": False,
                    "mensagem": f"Função já cadastrada (ID nº {funcao.id})"
                }

        funcao = Funcao(
            nome=nome
        )

        self._funcoes.append(funcao)

        return {
            "sucesso": True,
            "alterado": True,
            "mensagem": "Função cadastrada"
        }

    def atualizar(self, id: int, nome: str):

        funcao = self.buscar_por_id(id)

        if funcao is None:
            return {
                "sucesso": False,
                "alterado": False,
                "mensagem": "Digite um ID válido"
            }

        nome = nome.strip().upper()

        if nome == "":
            return {
                "sucesso": False,
                "alterado": False,
                "mensagem": "Necessário cadastrar nome de função"
            }

        for outra_funcao in self._funcoes:

            if outra_funcao.nome.strip().upper() == nome and outra_funcao.id != id:
                return {
                    "sucesso": False,
                    "alterado": False,
                    "mensagem": f"Função já cadastrada (ID nº {outra_funcao.id})"
                }

        funcao.nome = nome

        return {
            "sucesso": True,
            "alterado": True,
            "mensagem": "Função atualizada"
        }

    def desativar(self, id: int):

        funcao = self.buscar_por_id(id)

        if funcao is None:
            return {
                "sucesso": False,
                "alterado": False,
                "mensagem": "Digite um ID válido"
            }

        funcao.ativo = False

        return {
            "sucesso": True,
            "alterado": True,
            "mensagem": "Função inativada"
        }

    def ativar(self, id: int):

        funcao = self.buscar_por_id(id)

        if funcao is None:
            return {
                "sucesso": False,
                "alterado": False,
                "mensagem": "Digite um ID válido"
            }

        funcao.ativo = True

        return {
            "sucesso": True,
            "alterado": True,
            "mensagem": "Função ativada"
        }