from pathlib import Path
import json

from models.escala import Escala


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
            "eventos": escala.eventos
        }

    def _dict_para_escala(self, dados):

        return Escala(
            id=dados["id"],
            eventos=dados["eventos"]
        )