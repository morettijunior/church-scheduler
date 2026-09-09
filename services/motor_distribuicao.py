class MotorDistribuicao:

    def encontrar_pessoas_da_funcao(
        self,
        pessoas,
        funcao
    ):
        """
        Retorna somente as pessoas ativas que possuem a função.
        A lista é ordenada alfabeticamente.
        """

        pessoas_da_funcao = [
            pessoa
            for pessoa in pessoas
            if pessoa.ativo and funcao in pessoa.funcoes
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
        """
        Gera uma sequência circular começando pela
        pessoa inicial.
        """

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
        """
        Encontra a pessoa inicial de uma função.

        A partir da pessoa de referência:

        1. Avança o deslocamento definido.
        2. Verifica se a pessoa possui a função.
        3. Se não possuir, continua procurando a próxima
           pessoa que possua a função.

        O deslocamento é utilizado somente para encontrar
        o ponto inicial da função.
        """

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
        """
        Encontra a posição real de uma função dentro
        das atribuições da ocorrência.

        A posição pode variar de uma ocorrência para outra.

        Exemplo:

            CULTO:
                ATRIO -> posição 0
                PORTA -> posição 1

            ENSAIO:
                PORTA -> posição 0
                ATRIO -> posição 1
        """

        for indice, atribuicao in enumerate(
            ocorrencia.atribuicoes
        ):
            if atribuicao["funcao"] == funcao:
                return indice

        return None

    def distribuir_f1(
        self,
        ocorrencias,
        sequencia,
        funcao
    ):
        """
        Distribui a F1.

        A F1 é a função-base da distribuição.

        Utiliza:

        - sequência circular;
        - restrições;
        - fila de prioridade.

        A posição da F1 é encontrada pela função,
        e não assumida como posição 0.
        """

        fila_prioridade = []
        indice_sequencia = 0

        for ocorrencia in ocorrencias:

            pessoa = None

            # =================================================
            # 1. TENTA A FILA DE PRIORIDADE
            # =================================================

            for pessoa_prioritaria in fila_prioridade:

                if (
                    ocorrencia.data
                    not in pessoa_prioritaria.restricoes
                ):

                    pessoa = pessoa_prioritaria

                    fila_prioridade.remove(
                        pessoa_prioritaria
                    )

                    break

            # =================================================
            # 2. SE NÃO CONSEGUIU, USA A SEQUÊNCIA NORMAL
            # =================================================

            if pessoa is None:

                while True:

                    pessoa = sequencia[
                        indice_sequencia
                    ]

                    if (
                        ocorrencia.data
                        not in pessoa.restricoes
                    ):
                        break

                    # Pessoa restrita:
                    # entra na fila de prioridade.

                    if (
                        pessoa
                        not in fila_prioridade
                    ):
                        fila_prioridade.append(
                            pessoa
                        )

                    indice_sequencia = (
                        indice_sequencia + 1
                    ) % len(sequencia)

                # Pessoa utilizada pela sequência.

                indice_sequencia = (
                    indice_sequencia + 1
                ) % len(sequencia)

            # =================================================
            # LOCALIZA A POSIÇÃO REAL DA FUNÇÃO
            # =================================================

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
        """
        Distribui qualquer função a partir da F2.

        indice_funcao:

            1 = F2
            2 = F3
            3 = F4
            4 = F5
            5 = F6
            6 = F7

        Uma função nunca depende do estado de distribuição
        da função anterior.

        Ela somente consulta as funções anteriores para
        verificar duplicidade no mesmo dia.

        A posição física da função dentro da ocorrência
        pode variar.
        """

        funcao_atual = (
            funcoes_necessarias[indice_funcao]
        )

        fila_prioridade = []
        indice_sequencia = 0

        for ocorrencia in ocorrencias:

            pessoa = None

            # =================================================
            # FUNÇÕES ANTERIORES
            # =================================================

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

            # =================================================
            # 1. TENTA A FILA DE PRIORIDADE
            # =================================================

            for pessoa_prioritaria in fila_prioridade:

                pessoa_duplicada = (
                    pessoa_prioritaria.nome
                    in pessoas_ja_utilizadas
                )

                pessoa_restrita = (
                    ocorrencia.data
                    in pessoa_prioritaria.restricoes
                )

                if (
                    not pessoa_restrita
                    and not pessoa_duplicada
                ):

                    pessoa = pessoa_prioritaria

                    fila_prioridade.remove(
                        pessoa_prioritaria
                    )

                    break

            # =================================================
            # 2. SE NÃO CONSEGUIU, USA A SEQUÊNCIA
            # =================================================

            if pessoa is None:

                while True:

                    pessoa = sequencia[
                        indice_sequencia
                    ]

                    pessoa_duplicada = (
                        pessoa.nome
                        in pessoas_ja_utilizadas
                    )

                    pessoa_restrita = (
                        ocorrencia.data
                        in pessoa.restricoes
                    )

                    if (
                        not pessoa_restrita
                        and not pessoa_duplicada
                    ):
                        break

                    # Pessoa indisponível:
                    # entra na fila de prioridade.

                    if (
                        pessoa
                        not in fila_prioridade
                    ):
                        fila_prioridade.append(
                            pessoa
                        )

                    indice_sequencia = (
                        indice_sequencia + 1
                    ) % len(sequencia)

                # Pessoa utilizada pela sequência.

                indice_sequencia = (
                    indice_sequencia + 1
                ) % len(sequencia)

            # =================================================
            # LOCALIZA A POSIÇÃO REAL DA FUNÇÃO
            # =================================================

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
        """
        Distribui todas as funções, da F1 até a F7.

        A F1 é iniciada pela pessoa escolhida.

        A partir da F2:

        - a referência é a primeira pessoa efetivamente
          utilizada pela função anterior;
        - aplica o deslocamento;
        - encontra a primeira pessoa da nova função;
        - gera a sequência;
        - distribui a função.

        Cada função possui seu próprio estado.

        A posição da função dentro da ocorrência é
        determinada pelo nome da função.
        """

        quantidade_funcoes = len(
            funcoes_necessarias
        )

        if quantidade_funcoes == 0:
            return

        if quantidade_funcoes > 7:

            raise ValueError(
                "O motor suporta no máximo 7 funções."
            )

        # =========================================================
        # F1
        # =========================================================

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

        # =========================================================
        # F2 ATÉ F7
        # =========================================================

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

            # -----------------------------------------------------
            # Primeira pessoa efetivamente utilizada
            # pela função anterior.
            # -----------------------------------------------------

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

            # -----------------------------------------------------
            # Pessoas que possuem a função atual.
            # -----------------------------------------------------

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

            # -----------------------------------------------------
            # Encontra o ponto inicial usando:
            #
            # função anterior + deslocamento
            # -----------------------------------------------------

            pessoa_inicial = (
                self.encontrar_inicio_funcao(
                    pessoas=pessoas,
                    pessoa_referencia=pessoa_referencia,
                    funcao=funcao_atual,
                    deslocamento=deslocamento
                )
            )

            # -----------------------------------------------------
            # Cria uma sequência independente para esta função.
            # -----------------------------------------------------

            sequencia = (
                self.gerar_sequencia(
                    pessoas_funcao,
                    pessoa_inicial
                )
            )

            # -----------------------------------------------------
            # Distribui a função.
            # -----------------------------------------------------

            self.distribuir_funcao(
                ocorrencias=ocorrencias,
                sequencia=sequencia,
                indice_funcao=indice_funcao,
                funcoes_necessarias=funcoes_necessarias
            )