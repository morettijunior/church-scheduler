from storage.evento_storage import EventoStorage


storage = EventoStorage()

eventos = storage.carregar()

print(eventos)