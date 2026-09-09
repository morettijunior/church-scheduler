from models.pessoa import Pessoa


class PessoaService:

    def __init__(self, pessoas: list[Pessoa]):
        self._pessoas = pessoas

    def listar_ativos(self) -> list[Pessoa]:
        ativos = []

        for pessoa in self._pessoas:
            if pessoa.ativo:
                ativos.append(pessoa)

        ativos.sort(key=lambda pessoa: pessoa.nome)

        return ativos

    def listar_inativos(self) -> list[Pessoa]:
        inativos = []

        for pessoa in self._pessoas:
            if not pessoa.ativo:
                inativos.append(pessoa)

        inativos.sort(key=lambda pessoa: pessoa.nome)

        return inativos

    def listar_todos(self) -> list[Pessoa]:
        todos = []

        for pessoa in self._pessoas:
            todos.append(pessoa)

        todos.sort(key=lambda pessoa: pessoa.id)

        return todos

    def buscar_por_id(self, id: int) -> Pessoa | None:
        for pessoa in self._pessoas:
            if pessoa.id == id:
                return pessoa

        return None

    def cadastrar(
        self,
        nome: str,
        telefone: str,
        funcoes: list,
        restricoes: list
    ):
        nome = nome.strip()
        telefone = telefone.strip()

        if nome == "":
            return {
                "sucesso": False,
                "alterado": False,
                "mensagem": "Necessário cadastrar nome de usuário"
            }

        if telefone == "":
            return {
                "sucesso": False,
                "alterado": False,
                "mensagem": "Necessário cadastrar telefone"
            }

        nome = nome.upper()

        for pessoa in self._pessoas:
            if pessoa.nome.strip().upper() == nome:
                return {
                    "sucesso": False,
                    "alterado": False,
                    "mensagem": (
                        f"Usuário já cadastrado "
                        f"(ID nº {pessoa.id})"
                    )
                }

        pessoa = Pessoa(
            nome=nome,
            telefone=telefone,
            funcoes=funcoes,
            restricoes=restricoes
        )

        self._pessoas.append(pessoa)

        return {
            "sucesso": True,
            "alterado": True,
            "mensagem": "Pessoa cadastrada"
        }

    def atualizar(
        self,
        id: int,
        nome: str,
        telefone: str,
        funcoes: list,
        restricoes: list
    ):
        pessoa = self.buscar_por_id(id)

        if pessoa is None:
            return {
                "sucesso": False,
                "alterado": False,
                "mensagem": "Digite um ID válido"
            }

        nome = nome.strip()
        telefone = telefone.strip()

        if nome == "":
            return {
                "sucesso": False,
                "alterado": False,
                "mensagem": "Necessário cadastrar nome de usuário"
            }

        if telefone == "":
            return {
                "sucesso": False,
                "alterado": False,
                "mensagem": "Necessário cadastrar telefone"
            }

        nome = nome.upper()

        for outra_pessoa in self._pessoas:
            if (
                outra_pessoa.nome.strip().upper() == nome
                and outra_pessoa.id != id
            ):
                return {
                    "sucesso": False,
                    "alterado": False,
                    "mensagem": (
                        f"Usuário já cadastrado "
                        f"(ID nº {outra_pessoa.id})"
                    )
                }

        pessoa.nome = nome
        pessoa.telefone = telefone
        pessoa.funcoes = funcoes
        pessoa.restricoes = restricoes

        return {
            "sucesso": True,
            "alterado": True,
            "mensagem": "Pessoa atualizada"
        }

    def desativar(self, id: int):
        pessoa = self.buscar_por_id(id)

        if pessoa is None:
            return {
                "sucesso": False,
                "alterado": False,
                "mensagem": "Digite um ID válido"
            }

        pessoa.ativo = False

        return {
            "sucesso": True,
            "alterado": True,
            "mensagem": "Pessoa inativada"
        }

    def ativar(self, id: int):
        pessoa = self.buscar_por_id(id)

        if pessoa is None:
            return {
                "sucesso": False,
                "alterado": False,
                "mensagem": "Digite um ID válido"
            }

        pessoa.ativo = True

        return {
            "sucesso": True,
            "alterado": True,
            "mensagem": "Pessoa ativada"
        }

    def possui_restricao(self, pessoa: Pessoa, data) -> bool:
        for restricao in pessoa.restricoes:

            if not isinstance(restricao, dict):
                continue

            tipo = restricao.get("tipo")
            valor = restricao.get("valor")

            if tipo == "DIA_SEMANA":
                try:
                    dia_semana = int(valor)
                except (TypeError, ValueError):
                    continue

                if data.weekday() == dia_semana:
                    return True

            elif tipo == "DATA":
                if valor == data.strftime("%d/%m/%Y"):
                    return True

        return False

    def validar_aptidao(
        self,
        id: int,
        funcao: str,
        data
    ):
        pessoa = self.buscar_por_id(id)

        if pessoa is None:
            return {
                "sucesso": False,
                "mensagem": "Pessoa não cadastrada"
            }

        if not pessoa.ativo:
            return {
                "sucesso": False,
                "mensagem": "Pessoa está inativa"
            }

        if funcao not in pessoa.funcoes:
            return {
                "sucesso": False,
                "mensagem": (
                    f"Pessoa não executa a função {funcao}"
                )
            }

        if self.possui_restricao(pessoa, data):
            return {
                "sucesso": False,
                "mensagem": (
                    "Pessoa possui restrição para esta data"
                )
            }

        return {
            "sucesso": True,
            "mensagem": "Pessoa apta para a função"
        }