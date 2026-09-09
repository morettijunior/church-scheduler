from pathlib import Path

import json

from models.pessoa import Pessoa


class PessoaStorage:

    def __init__(self):
        self._arquivo = Path("data/pessoas.json")
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

    def salvar(self, pessoas):
        dados = [
            self._pessoa_para_dict(pessoa)
            for pessoa in pessoas
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

        pessoas = [
            self._dict_para_pessoa(dado)
            for dado in dados
        ]

        return pessoas

    def _pessoa_para_dict(self, pessoa):
        return {
            "id": pessoa.id,
            "nome": pessoa.nome,
            "telefone": pessoa.telefone,
            "funcoes": pessoa.funcoes,
            "ativo": pessoa.ativo,
            "restricoes": pessoa.restricoes
        }

    def _dict_para_pessoa(self, dados):
        restricoes = dados.get(
            "restricoes",
            []
        )

        return Pessoa(
            id=dados["id"],
            nome=dados["nome"],
            telefone=dados["telefone"],
            funcoes=dados.get("funcoes", []),
            ativo=dados.get("ativo", True),
            restricoes=restricoes
        )

