from pathlib import Path
import json
from datetime import date

from models.escala import Escala
from models.ocorrencia import Ocorrencia
from models.evento import Evento


class EscalaStorage:

    def __init__(self):
        self._arquivo = Path("data/escalas.json")
        self._preparar_arquivo()

    def _preparar_arquivo(self):

        self._arquivo.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self._arquivo.exists():
            self._arquivo.write_text(
                "[]",
                encoding="utf-8"
            )

    def salvar(self, escalas):

        dados = [
            self._escala_para_dict(escala)
            for escala in escalas
        ]

        self._arquivo.write_text(
            json.dumps(
                dados,
                indent=4,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

    def carregar(self):

        dados = json.loads(
            self._arquivo.read_text(
                encoding="utf-8"
            )
        )

        escalas = [
            self._dict_para_escala(dado)
            for dado in dados
        ]

        return escalas

    def _escala_para_dict(self, escala):

        return {
            "id": escala.id,
            "nome": escala.nome,
            "ocorrencias": [
                self._ocorrencia_para_dict(ocorrencia)
                for ocorrencia in escala.ocorrencias
            ]
        }

    def _ocorrencia_para_dict(self, ocorrencia):

        return {
            "id": ocorrencia.id,
            "data": ocorrencia.data.isoformat(),
            "evento": {
                "id": ocorrencia.evento.id,
                "nome": ocorrencia.evento.nome,
                "funcoes_necessarias": ocorrencia.evento.funcoes_necessarias
            },
            "atribuicoes": ocorrencia.atribuicoes
        }

    def _dict_para_escala(self, dados):

        ocorrencias = [
            self._dict_para_ocorrencia(ocorrencia)
            for ocorrencia in dados["ocorrencias"]
        ]

        return Escala(
            id=dados["id"],
            nome=dados["nome"],
            ocorrencias=ocorrencias
        )

    def _dict_para_ocorrencia(self, dados):

        evento = Evento(
            id=dados["evento"]["id"],
            nome=dados["evento"]["nome"],
            funcoes_necessarias=dados["evento"]["funcoes_necessarias"]
        )

        return Ocorrencia(
            id=dados["id"],
            data=date.fromisoformat(dados["data"]),
            evento=evento,
            atribuicoes=dados["atribuicoes"]
        )