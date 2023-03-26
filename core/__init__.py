import datetime


class SystemInfo:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_time():
        agora = datetime.datetime.now()
        resposta = f"São {agora.hour} e {agora.minute} minutos"
        return resposta

    @staticmethod
    def get_date():
        agora = datetime.datetime.now()
        resposta = f"Hoje é dia {agora.day} de {agora.month} de {agora.year}"
        return resposta
