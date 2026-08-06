from models.escala import Escala
from storage.escala_storage import EscalaStorage


storage = EscalaStorage()


escala1 = Escala(
    eventos=[
        {
            "nome": "CULTO",
            "data": "10/08/2026",
            "alocacoes": [
                {
                    "funcao": "Atrio",
                    "pessoa": "Felix"
                }
            ]
        }
    ]
)


escalas = [
    escala1
]


storage.salvar(escalas)


for escala in escalas:
    print(escala.id)