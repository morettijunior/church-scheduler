from models.escala import Escala


class EscalaService:

    def __init__(self, escalas: list[Escala]):
        self._escalas = escalas

    def listar_todas(self) -> list[Escala]:

        todas = []

        for escala in self._escalas:
            todas.append(escala)

        todas.sort(key=lambda escala: escala.id)

        return todas

    def buscar_por_id(self, id: int) -> Escala | None:

        for escala in self._escalas:

            if escala.id == id:
                return escala

        return None

    def criar(self, nome, ocorrencias):

        ocorrencias_ordenadas = self._ordenar_ocorrencias(
            ocorrencias
        )

        escala = Escala(
            nome=nome,
            ocorrencias=ocorrencias_ordenadas
        )

        self._escalas.append(escala)

        return escala

    def _ordenar_ocorrencias(self, ocorrencias):

        ocorrencias_ordenadas = sorted(
            ocorrencias,
            key=lambda ocorrencia: (
                ocorrencia.data,
                self._prioridade_evento(ocorrencia.evento)
            )
        )

        return ocorrencias_ordenadas

    def _prioridade_evento(self, evento):

        prioridades = {
            "RJM": 1,
            "ENSAIO": 2,
            "CULTO": 3
        }

        return prioridades.get(evento.nome, 999)

    def buscar_ocorrencia_por_id(
        self,
        escala: Escala,
        id_ocorrencia: int
    ):

        for ocorrencia in escala.ocorrencias:

            if ocorrencia.id == id_ocorrencia:
                return ocorrencia

        return None

    def buscar_atribuicao(
        self,
        ocorrencia,
        posicao: int
    ):

        if posicao < 1 or posicao > len(ocorrencia.atribuicoes):
            return None

        return ocorrencia.atribuicoes[posicao - 1]

    def alterar_atribuicao(
        self,
        escala: Escala,
        id_ocorrencia: int,
        posicao: int,
        id_pessoa: int,
        pessoa_service
    ):

        ocorrencia = self.buscar_ocorrencia_por_id(
            escala,
            id_ocorrencia
        )

        if ocorrencia is None:
            return {
                "sucesso": False,
                "alterado": False,
                "mensagem": "Ocorrência não encontrada"
            }

        atribuicao = self.buscar_atribuicao(
            ocorrencia,
            posicao
        )

        if atribuicao is None:
            return {
                "sucesso": False,
                "alterado": False,
                "mensagem": "Posição de atribuição inválida"
            }

        funcao = atribuicao["funcao"]

        resultado = pessoa_service.validar_aptidao(
            id_pessoa,
            funcao,
            ocorrencia.data
        )

        if not resultado["sucesso"]:
            return {
                "sucesso": False,
                "alterado": False,
                "mensagem": resultado["mensagem"]
            }

        pessoa = pessoa_service.buscar_por_id(id_pessoa)

        for outra_atribuicao in ocorrencia.atribuicoes:

            if outra_atribuicao is atribuicao:
                continue

            if outra_atribuicao["pessoa"] == pessoa.nome:
                return {
                    "sucesso": False,
                    "alterado": False,
                    "mensagem": (
                        "Pessoa já está escalada "
                        "nesta ocorrência"
                    )
                }

        atribuicao["pessoa"] = pessoa.nome

        return {
            "sucesso": True,
            "alterado": True,
            "mensagem": "Atribuição alterada"
        }