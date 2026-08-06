from pathlib import Path
import json

from models.funcao import Funcao


class FuncaoStorage:

    def __init__(self):
        self._arquivo = Path("data/funcoes.json")
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

    def salvar(self, funcoes):

        dados = [
            self._funcao_para_dict(funcao)
            for funcao in funcoes
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

        funcoes = [
            self._dict_para_funcao(dado)
            for dado in dados
        ]

        return funcoes

    def _funcao_para_dict(self, funcao):

        return {
            "id": funcao.id,
            "nome": funcao.nome,
            "ativo": funcao.ativo
        }

    def _dict_para_funcao(self, dados):

        return Funcao(
            id=dados["id"],
            nome=dados["nome"],
            ativo=dados["ativo"]
        )