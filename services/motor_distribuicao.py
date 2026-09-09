class MotorDistribuicao:

    def possui_restricao(self, pessoa, data):
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

    def encontrar_pessoas_da_funcao(
        self,
        pessoas,
        funcao
    ):
        pessoas_da_funcao = [
            pessoa
            for pessoa in pessoas
            if pessoa.ativo
            and funcao in pessoa.funcoes
        ]

        pessoas_da_funcao.sort(
            key=lambda pessoa: pessoa.nome
        )

        return pessoas_da_funcao

    def gerar_sequencia(
        self,
        pessoas,
        pessoa_inicial
    ):
        indice_inicial = pessoas.index(
            pessoa_inicial
        )

        return (
            pessoas[indice_inicial:]
            + pessoas[:indice_inicial]
        )

    def encontrar_inicio_funcao(
        self,
        pessoas,
        pessoa_referencia,
        funcao,
        deslocamento
    ):
        indice_referencia = pessoas.index(
            pessoa_referencia
        )

        indice = (
            indice_referencia + deslocamento
        ) % len(pessoas)

        while True:
            pessoa = pessoas[indice]

            if (
                pessoa.ativo
                and funcao in pessoa.funcoes
            ):
                return pessoa

            indice = (
                indice + 1
            ) % len(pessoas)

    def encontrar_indice_funcao(
        self,
        ocorrencia,
        funcao
    ):
        for indice, atribuicao in enumerate(
            ocorrencia.atribuicoes
        ):
            if atribuicao["funcao"] == funcao:
                return indice

        return None

    def pessoa_disponivel(
        self,
        pessoa,
        ocorrencia,
        pessoas_ja_utilizadas
    ):
        if pessoa.nome in pessoas_ja_utilizadas:
            return False

        if self.possui_restricao(
            pessoa,
            ocorrencia.data
        ):
            return False

        return True

    def distribuir_f1(
        self,
        ocorrencias,
        sequencia,
        funcao
    ):
        fila_prioridade = []
        indice_sequencia = 0

        for ocorrencia in ocorrencias:

            pessoa = None

            for pessoa_prioritaria in fila_prioridade:

                if not self.possui_restricao(
                    pessoa_prioritaria,
                    ocorrencia.data
                ):
                    pessoa = pessoa_prioritaria

                    fila_prioridade.remove(
                        pessoa_prioritaria
                    )

                    break

            if pessoa is None:

                while True:

                    pessoa = sequencia[
                        indice_sequencia
                    ]

                    if not self.possui_restricao(
                        pessoa,
                        ocorrencia.data
                    ):
                        break

                    if pessoa not in fila_prioridade:
                        fila_prioridade.append(
                            pessoa
                        )

                    indice_sequencia = (
                        indice_sequencia + 1
                    ) % len(sequencia)

                indice_sequencia = (
                    indice_sequencia + 1
                ) % len(sequencia)

            indice_atribuicao = (
                self.encontrar_indice_funcao(
                    ocorrencia,
                    funcao
                )
            )

            if indice_atribuicao is None:
                raise ValueError(
                    f"Função {funcao} não encontrada "
                    "na ocorrência."
                )

            ocorrencia.atribuicoes[
                indice_atribuicao
            ]["pessoa"] = pessoa.nome

    def distribuir_funcao(
        self,
        ocorrencias,
        sequencia,
        indice_funcao,
        funcoes_necessarias
    ):
        funcao_atual = (
            funcoes_necessarias[indice_funcao]
        )

        fila_prioridade = []
        indice_sequencia = 0

        for ocorrencia in ocorrencias:

            pessoa = None

            pessoas_ja_utilizadas = set()

            for funcao_anterior in (
                funcoes_necessarias[:indice_funcao]
            ):
                indice_anterior = (
                    self.encontrar_indice_funcao(
                        ocorrencia,
                        funcao_anterior
                    )
                )

                if indice_anterior is None:
                    continue

                nome_pessoa = (
                    ocorrencia.atribuicoes[
                        indice_anterior
                    ]["pessoa"]
                )

                if nome_pessoa:
                    pessoas_ja_utilizadas.add(
                        nome_pessoa
                    )

            for pessoa_prioritaria in fila_prioridade:

                if self.pessoa_disponivel(
                    pessoa_prioritaria,
                    ocorrencia,
                    pessoas_ja_utilizadas
                ):
                    pessoa = pessoa_prioritaria

                    fila_prioridade.remove(
                        pessoa_prioritaria
                    )

                    break

            if pessoa is None:

                tentativas = 0

                while tentativas < len(sequencia):

                    pessoa = sequencia[
                        indice_sequencia
                    ]

                    if self.pessoa_disponivel(
                        pessoa,
                        ocorrencia,
                        pessoas_ja_utilizadas
                    ):
                        break

                    if pessoa not in fila_prioridade:
                        fila_prioridade.append(
                            pessoa
                        )

                    indice_sequencia = (
                        indice_sequencia + 1
                    ) % len(sequencia)

                    tentativas += 1

                if tentativas >= len(sequencia):
                    raise ValueError(
                        f"Não foi possível encontrar "
                        f"pessoa disponível para a função "
                        f"{funcao_atual} em "
                        f"{ocorrencia.data.strftime('%d/%m/%Y')}."
                    )

                indice_sequencia = (
                    indice_sequencia + 1
                ) % len(sequencia)

            indice_atribuicao = (
                self.encontrar_indice_funcao(
                    ocorrencia,
                    funcao_atual
                )
            )

            if indice_atribuicao is None:
                raise ValueError(
                    f"Função {funcao_atual} não encontrada "
                    "na ocorrência."
                )

            ocorrencia.atribuicoes[
                indice_atribuicao
            ]["pessoa"] = pessoa.nome

    def distribuir_todas_as_funcoes(
        self,
        pessoas,
        ocorrencias,
        funcoes_necessarias,
        pessoa_inicial_f1,
        deslocamento=3
    ):
        quantidade_funcoes = len(
            funcoes_necessarias
        )

        if quantidade_funcoes == 0:
            return

        if quantidade_funcoes > 7:
            raise ValueError(
                "O motor suporta no máximo 7 funções."
            )

        funcao_f1 = (
            funcoes_necessarias[0]
        )

        pessoas_f1 = (
            self.encontrar_pessoas_da_funcao(
                pessoas,
                funcao_f1
            )
        )

        if pessoa_inicial_f1 not in pessoas_f1:
            raise ValueError(
                "A pessoa inicial da F1 "
                "não possui a função F1."
            )

        if self.possui_restricao(
            pessoa_inicial_f1,
            ocorrencias[0].data
        ):
            raise ValueError(
                "A pessoa inicial da F1 possui "
                "restrição na primeira ocorrência."
            )

        sequencia_f1 = (
            self.gerar_sequencia(
                pessoas_f1,
                pessoa_inicial_f1
            )
        )

        self.distribuir_f1(
            ocorrencias,
            sequencia_f1,
            funcao_f1
        )

        for indice_funcao in range(
            1,
            quantidade_funcoes
        ):
            funcao_atual = (
                funcoes_necessarias[
                    indice_funcao
                ]
            )

            indice_funcao_anterior = (
                indice_funcao - 1
            )

            funcao_anterior = (
                funcoes_necessarias[
                    indice_funcao_anterior
                ]
            )

            indice_atribuicao_anterior = (
                self.encontrar_indice_funcao(
                    ocorrencias[0],
                    funcao_anterior
                )
            )

            if indice_atribuicao_anterior is None:
                raise ValueError(
                    f"Função {funcao_anterior} "
                    "não encontrada na primeira ocorrência."
                )

            nome_pessoa_referencia = (
                ocorrencias[0]
                .atribuicoes[
                    indice_atribuicao_anterior
                ]["pessoa"]
            )

            pessoa_referencia = next(
                (
                    pessoa
                    for pessoa in pessoas
                    if pessoa.nome
                    == nome_pessoa_referencia
                ),
                None
            )

            if pessoa_referencia is None:
                raise ValueError(
                    "A pessoa de referência da função "
                    f"{funcao_atual} não foi encontrada."
                )

            pessoas_funcao = (
                self.encontrar_pessoas_da_funcao(
                    pessoas,
                    funcao_atual
                )
            )

            if not pessoas_funcao:
                raise ValueError(
                    f"Nenhuma pessoa possui a função "
                    f"{funcao_atual}."
                )

            pessoa_inicial = (
                self.encontrar_inicio_funcao(
                    pessoas=pessoas,
                    pessoa_referencia=pessoa_referencia,
                    funcao=funcao_atual,
                    deslocamento=deslocamento
                )
            )

            sequencia = (
                self.gerar_sequencia(
                    pessoas_funcao,
                    pessoa_inicial
                )
            )

            self.distribuir_funcao(
                ocorrencias=ocorrencias,
                sequencia=sequencia,
                indice_funcao=indice_funcao,
                funcoes_necessarias=funcoes_necessarias
            )