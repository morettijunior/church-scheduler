from datetime import timedelta

from models.ocorrencia import Ocorrencia


class Scheduler:

    def gerar_ocorrencias(self, configuracao):

        ocorrencias = []

        data_atual = configuracao.data_inicio

        while data_atual <= configuracao.data_fim:

            for evento_configurado in configuracao.eventos:

                regra = evento_configurado.regra

                if regra.corresponde(data_atual):

                    ocorrencia = Ocorrencia(
                        data=data_atual,
                        evento=evento_configurado.evento
                    )

                    ocorrencias.append(ocorrencia)

            data_atual += timedelta(days=1)

        return ocorrencias