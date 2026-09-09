from models.configuracao_escala import ConfiguracaoEscala
from scheduler.scheduler import Scheduler


class GeradorEscalaService:

    def __init__(
        self,
        pessoas,
        scheduler=None
    ):
        self._pessoas = pessoas
        self._scheduler = scheduler or Scheduler()

    def gerar_ocorrencias(
        self,
        configuracao: ConfiguracaoEscala
    ):
        return self._scheduler.gerar_ocorrencias(
            configuracao
        )

    def encontrar_funcoes(
        self,
        ocorrencias
    ):
        funcoes = []

        for ocorrencia in ocorrencias:
            for atribuicao in ocorrencia.atribuicoes:

                funcao = atribuicao["funcao"]

                if funcao not in funcoes:
                    funcoes.append(funcao)

        return funcoes

    def determinar_ordem_funcoes(
        self,
        ocorrencias
    ):
        return self.encontrar_funcoes(
            ocorrencias
        )

    def mapear_funcoes(
        self,
        ocorrencias
    ):
        mapa = {}

        for ocorrencia in ocorrencias:

            for indice, atribuicao in enumerate(
                ocorrencia.atribuicoes
            ):

                funcao = atribuicao["funcao"]

                if funcao not in mapa:
                    mapa[funcao] = []

                mapa[funcao].append({
                    "ocorrencia": ocorrencia,
                    "indice": indice
                })

        return mapa

    def preparar_distribuicao(
        self,
        ocorrencias
    ):
        ordem_funcoes = self.determinar_ordem_funcoes(
            ocorrencias
        )

        mapa = self.mapear_funcoes(
            ocorrencias
        )

        distribuicao = []

        for indice_funcao, funcao in enumerate(
            ordem_funcoes
        ):

            distribuicao.append({
                "indice_funcao": indice_funcao,
                "funcao": funcao,
                "ocorrencias": mapa[funcao]
            })

        return distribuicao

    def encontrar_pessoas_iniciais_f1(
        self,
        ocorrencias,
        funcao_f1
    ):
        """
        Retorna as pessoas que podem ser escolhidas
        como pessoa inicial da F1.

        Critérios:
        - pessoa ativa;
        - possui a função F1;
        - não possui restrição na primeira ocorrência.
        """

        if not ocorrencias:
            return []

        primeira_ocorrencia = ocorrencias[0]

        pessoas_disponiveis = []

        for pessoa in self._pessoas:

            if not pessoa.ativo:
                continue

            if funcao_f1 not in pessoa.funcoes:
                continue

            if primeira_ocorrencia.data in pessoa.restricoes:
                continue

            pessoas_disponiveis.append(pessoa)

        pessoas_disponiveis.sort(
            key=lambda pessoa: pessoa.nome
        )

        return pessoas_disponiveis