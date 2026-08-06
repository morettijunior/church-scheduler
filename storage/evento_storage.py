import json
from datetime import date
from pathlib import Path

from models.evento import Evento


class EventoStorage:

    def __init__(self):
        self._arquivo = Path("data/eventos.json")
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

    def salvar(self, eventos):
        dados = [
            self._evento_para_dict(evento)
            for evento in eventos
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

        eventos = [
            self._dict_para_evento(dado)
            for dado in dados
        ]

        return eventos

    def _evento_para_dict(self, evento):
        return {
            "id": evento.id,
            "nome": evento.nome,
            "funcoes_necessarias": evento.funcoes_necessarias,
            "data": evento.data.isoformat()
        }


    def _dict_para_evento(self, dados):
        data = date.fromisoformat(dados["data"])

        return Evento(
            id=dados["id"],
            nome=dados["nome"],
            funcoes_necessarias=dados["funcoes_necessarias"],
            data=data
        )